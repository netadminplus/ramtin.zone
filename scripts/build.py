#!/usr/bin/env python3
"""Static site generator for ramtin.zone (Ramtin Tech Zone blog).

Reads Markdown posts/pages from content/, renders with Jinja2 + markdown,
writes the complete static site to dist/ (which is the GitHub Pages root).

Usage: python3 scripts/build.py [--out DIR]
Requires: markdown, jinja2, pyyaml (see requirements.txt).
"""
import argparse
import json
import math
import re
import shutil
import sys
import urllib.request
from datetime import datetime, date
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
import markdown as md_lib

HERE = Path(__file__).resolve().parent
SITE = HERE.parent
CONTENT = SITE / "content"
TEMPLATES = SITE / "templates"
STATIC = SITE / "static"
DATA = SITE / "data"

SITE_URL = "https://ramtin.zone"
SITE_NAME = "Ramtin Tech Zone"


def parse_post(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not m:
        raise ValueError(f"{path}: missing front matter")
    fm = yaml.safe_load(m.group(1))
    body = m.group(2)
    return fm, body


def render_md(body):
    return md_lib.markdown(
        body, extensions=["tables", "fenced_code", "smarty"], output_format="html5"
    )


def human_date(d):
    if isinstance(d, (datetime, date)):
        return d.strftime("%B %-d, %Y")
    return datetime.strptime(str(d)[:10], "%Y-%m-%d").strftime("%B %-d, %Y")


def fmt_views(n):
    if n is None:
        return None
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M".replace(".0", "")
    if n >= 1_000:
        return f"{n / 1_000:.1f}K".replace(".0", "")
    return str(n)


def fmt_duration(seconds):
    if not seconds:
        return None
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def relink(html, prefix):
    """Rewrite root-absolute internal links in rendered Markdown to the
    page-relative prefix, so pages work at any base path."""
    for token in ("assets/", "posts/", "about/", "donate/", "contact/", "projects/", "feed.xml"):
        html = html.replace(f'"/{token}', f'"{prefix}{token}')
    html = html.replace('href="/"', f'href="{prefix}"')
    return html


def thumb_available(url):
    """HEAD-check a YouTube thumbnail. HTTP 404 means the thumbnail is
    definitely gone (removed/private video) -> False. Any other error
    (network, rate limit, 403) means 'unknown' -> True, so the build never
    drops a good thumbnail over a flaky check."""
    import urllib.error
    try:
        req = urllib.request.Request(url, method="HEAD",
                                     headers={"User-Agent": "ramtin-zone-site-builder"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status == 200
    except urllib.error.HTTPError as e:
        return e.code != 404
    except Exception:
        return True


def load_video_meta():
    """Match videos.json (from yt-dlp) by YouTube ID for views/duration."""
    meta = {}
    vf = DATA / "videos.json"
    if vf.exists():
        for v in json.load(open(vf)):
            meta[v["id"]] = v
    return meta


def fetch_projects():
    """Live repo list from the public GitHub API, with a local fallback."""
    try:
        req = urllib.request.Request(
            "https://api.github.com/users/netadminplus/repos?per_page=100&type=public&sort=updated",
            headers={"User-Agent": "ramtin-zone-site-builder", "Accept": "application/vnd.github+json"},
        )
        repos = json.load(urllib.request.urlopen(req, timeout=20))
        out = [
            {
                "name": r["name"],
                "url": r["html_url"],
                "description": r.get("description") or "",
                "stars": r.get("stargazers_count", 0),
                "language": r.get("language") or "",
                "updated": (r.get("updated_at") or "")[:10],
            }
            for r in repos
            if not r.get("fork") and r["name"] not in ("ramtin.zone",)
        ]
        out.sort(key=lambda r: (-r["stars"], r["name"]))
        DATA.mkdir(parents=True, exist_ok=True)
        json.dump(out, open(DATA / "projects.json", "w"), indent=1)
        return out
    except Exception as e:
        print(f"projects API fetch failed ({e}); using snapshot", file=sys.stderr)
        snap = DATA / "projects.json"
        return json.load(open(snap)) if snap.exists() else []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(SITE / "dist"))
    args = ap.parse_args()
    out = Path(args.out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    env.filters["tojson"] = lambda v: json.dumps(v, ensure_ascii=False)

    video_meta = load_video_meta()

    # ---- posts ------------------------------------------------------
    posts = []
    for path in sorted((CONTENT / "posts").glob("*.md")):
        fm, body = parse_post(path)
        words = len(re.sub(r"<[^>]+>", " ", render_md(body)).split())
        yt = fm.get("youtube_id")
        v = video_meta.get(yt, {}) if yt else {}
        local_image = fm.get("image", "").lstrip("/") if fm.get("image") else None
        if yt:
            maxres = f"https://i.ytimg.com/vi/{yt}/maxresdefault.jpg"
            hq = f"https://i.ytimg.com/vi/{yt}/hqdefault.jpg"
            # Removed/private videos have no thumbnails (404). Fall back to
            # the post's own featured image instead of a broken card.
            if thumb_available(maxres):
                thumb, thumb_fallback, thumb_abs = maxres, hq, maxres
                thumb_is_local = False
            elif thumb_available(hq):
                thumb, thumb_fallback, thumb_abs = hq, hq, hq
                thumb_is_local = False
            elif local_image:
                thumb = thumb_fallback = local_image
                thumb_abs = f"{SITE_URL}/{local_image}"
                thumb_is_local = True
            else:
                thumb, thumb_fallback, thumb_abs = maxres, hq, maxres
                thumb_is_local = False
            image = local_image
        elif local_image:
            # Blog-only post: local featured image, stored without a leading
            # slash so templates can prefix it per page depth.
            thumb = thumb_fallback = local_image
            thumb_abs = f"{SITE_URL}/{local_image}"
            thumb_is_local = True
            image = local_image
        else:
            thumb = thumb_fallback = thumb_abs = ""
            thumb_is_local = True
            image = None
        posts.append(
            {
                "title": fm["title"],
                "slug": fm["slug"],
                "date": str(fm["date"])[:10],
                "date_human": human_date(fm["date"]),
                "categories": fm.get("categories", []),
                "description": fm.get("description", ""),
                "youtube_id": yt,
                "image": image,
                "thumb": thumb,
                "thumb_fallback": thumb_fallback,
                "thumb_abs": thumb_abs,
                "thumb_is_local": thumb_is_local,
                "views": fmt_views(v.get("view_count")),
                "duration": fmt_duration(v.get("duration")),
                "reading_time": max(1, math.ceil(words / 200)),
                "body_html": relink(render_md(body), "../../"),
                "words": words,
            }
        )
    posts.sort(key=lambda p: p["date"], reverse=True)
    categories = sorted({c for p in posts for c in p["categories"]})

    ctx = {
        "site": {
            "name": SITE_NAME,
            "url": SITE_URL,
            "description": "Practical tutorials about MikroTik, OpenWrt, VPNs, Linux and AI — hands-on guides from Ramtin Rahmani Nejad, a network engineer in IT since 2006.",
            "year": datetime.now().year,
            "og_image": posts[0]["thumb_abs"] if posts else f"{SITE_URL}/assets/images/favicon.svg",
        }
    }

    # ---- home -------------------------------------------------------
    # Asset/internal links are relative (prefix) so the site works both at
    # ramtin.zone (root) and at netadminplus.github.io/ramtin.zone/ (subpath).
    home = env.get_template("home.html").render(
        **ctx, posts=posts, categories=categories, active="home", canonical="/",
        prefix="",
    )
    (out / "index.html").write_text(home, encoding="utf-8")

    # ---- post pages -------------------------------------------------
    for i, post in enumerate(posts):
        related = [
            p for p in posts
            if p is not post and set(p["categories"]) & set(post["categories"])
        ][:3]
        html = env.get_template("post.html").render(
            **ctx,
            post=post,
            related=related,
            prev=posts[i - 1] if i > 0 else None,
            next=posts[i + 1] if i + 1 < len(posts) else None,
            canonical=f"/posts/{post['slug']}/",
            active="home",
            prefix="../../",
        )
        d = out / "posts" / post["slug"]
        d.mkdir(parents=True)
        (d / "index.html").write_text(html, encoding="utf-8")

    # ---- static pages ----------------------------------------------
    for path in sorted((CONTENT / "pages").glob("*.md")):
        fm, body = parse_post(path)
        html = env.get_template("page.html").render(
            **ctx,
            page={"title": fm["title"], "body_html": relink(render_md(body), "../"),
                  "description": fm.get("description")},
            canonical=f"/{fm['slug']}/",
            active=fm["slug"],
            prefix="../",
        )
        d = out / fm["slug"]
        d.mkdir(parents=True)
        (d / "index.html").write_text(html, encoding="utf-8")

    # ---- projects ---------------------------------------------------
    projects = fetch_projects()
    proj = env.get_template("projects.html").render(
        **ctx, projects=projects, canonical="/projects/", active="projects",
        prefix="../",
    )
    d = out / "projects"
    d.mkdir(parents=True)
    (d / "index.html").write_text(proj, encoding="utf-8")

    # ---- feeds ------------------------------------------------------
    feed_items = "".join(
        f"""  <item>
    <title>{p['title']}</title>
    <link>{SITE_URL}/posts/{p['slug']}/</link>
    <guid>{SITE_URL}/posts/{p['slug']}/</guid>
    <pubDate>{datetime.strptime(p['date'], '%Y-%m-%d').strftime('%a, %d %b %Y 00:00:00 +0000')}</pubDate>
    <description>{p['description']}</description>
  </item>
"""
        for p in posts[:20]
    )
    (out / "feed.xml").write_text(
        f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
  <title>{SITE_NAME} — Blog</title>
  <link>{SITE_URL}/</link>
  <description>Practical tutorials about MikroTik, OpenWrt, VPNs, Linux and AI.</description>
  <language>en</language>
{feed_items}</channel></rss>
""",
        encoding="utf-8",
    )

    urls = [("", posts[0]["date"] if posts else "2026-11-10")]
    for p in posts:
        urls.append((f"posts/{p['slug']}/", p["date"]))
    for slug in ("about", "donate", "contact", "projects"):
        urls.append((f"{slug}/", "2026-11-10"))
    sm = "".join(
        f"  <url><loc>{SITE_URL}/{u}</loc><lastmod>{lm}</lastmod></url>\n"
        for u, lm in urls
    )
    (out / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}</urlset>\n',
        encoding="utf-8",
    )
    (out / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8"
    )
    (out / "CNAME").write_text("ramtin.zone\n", encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")

    # ---- static assets ----------------------------------------------
    shutil.copytree(STATIC, out / "assets", dirs_exist_ok=True)
    # article screenshots live in the repo under static/images/
    if (STATIC / "images").exists():
        shutil.copytree(STATIC / "images", out / "assets" / "images", dirs_exist_ok=True)

    print(f"built {len(posts)} posts, {len(projects)} projects -> {out}")
    for p in posts:
        print(f"  {p['date']} {p['slug']} ({p['words']}w, {p['reading_time']} min)")


if __name__ == "__main__":
    main()
