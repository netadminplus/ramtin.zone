#!/usr/bin/env python3
"""Migrate WordPress posts (netadminhub.com export) to Markdown with front matter.

Reads ../netadminhub-export/posts.json + image-map.json, writes
../site/content/posts/<slug>.md.

Rules:
- "Watch the Full Video" promo block is dropped (the template renders the
  video embed from front matter instead); the surrounding article stays.
- The "Video: This article is the command and configuration reference..."
  blockquote is dropped for the same reason.
- YouTube iframes / youtu.be links become front-matter `youtube_id`.
- Images are rewritten to local /assets/images/... paths (already downloaded).
- NetAdminHub brand -> Ramtin Tech Zone in prose (not in code or lab domains).
- Internal netadminhub.com post links -> /posts/<slug>/.
- h1 inside content is demoted to h2 (the page title is the h1).
"""
import json
import re
import sys
import html as html_lib
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPORT = HERE.parent.parent / "netadminhub-export"
OUT = HERE.parent / "content" / "posts"
IMAGE_MAP = json.load(open(HERE.parent.parent / "build" / "image-map.json"))


def clean_text(s):
    s = re.sub(r"\s+", " ", s)
    return s.strip()


class MDConverter(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.stack = []
        self.list_stack = []
        self.in_pre = False
        self.pre_buf = ""
        self.in_code = False
        self.table = None
        self.row = None
        self.cell = None
        self.skip = 0  # depth of elements to skip entirely (iframes)
        self.link_href = None
        self.link_text = ""
        self.in_link = False

    # -- helpers ---------------------------------------------------------
    def emit(self, s):
        if self.skip:
            return
        self.out.append(s)

    def cur(self):
        return self.stack[-1] if self.stack else None

    # -- parser ----------------------------------------------------------
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "iframe":
            self.skip += 1
            return
        if self.skip:
            return
        if tag in ("h1", "h2", "h3", "h4"):
            level = {"h1": 2, "h2": 2, "h3": 3, "h4": 4}[tag]
            self.emit("\n\n" + "#" * level + " ")
            self.stack.append(("heading", tag))
        elif tag == "p":
            self.emit("\n\n")
            self.stack.append(("p", tag))
        elif tag in ("strong", "b"):
            self.emit("**")
            self.stack.append(("strong", tag))
        elif tag in ("em", "i"):
            self.emit("*")
            self.stack.append(("em", tag))
        elif tag == "code" and not self.in_pre:
            self.emit("`")
            self.stack.append(("code", tag))
        elif tag == "pre":
            self.in_pre = True
            self.pre_buf = ""
            self.stack.append(("pre", tag))
        elif tag == "br":
            if self.in_pre:
                self.pre_buf += "\n"
            else:
                self.emit("  \n")
        elif tag == "ul":
            self.list_stack.append("ul")
            self.stack.append(("ul", tag))
        elif tag == "ol":
            self.list_stack.append("ol")
            self.stack.append(("ol", tag))
        elif tag == "li":
            depth = len(self.list_stack)
            marker = "- " if self.list_stack and self.list_stack[-1] == "ul" else "1. "
            self.emit("\n" + "  " * (depth - 1) + marker)
            self.stack.append(("li", tag))
        elif tag == "a":
            href = a.get("href", "")
            href = rewrite_link(href)
            self.link_href = href
            self.link_text = ""
            self.in_link = True
            self.stack.append(("a", tag))
        elif tag == "img":
            src = a.get("data-src") or a.get("src", "")
            if "transparent.gif" in src:
                return
            local = IMAGE_MAP.get(src)
            if local:
                src = local
            alt = a.get("alt", "")
            self.emit(f"\n\n![{alt}]({src})\n\n")
        elif tag == "blockquote":
            self.emit("\n\n")
            self.stack.append(("quote", tag))
        elif tag == "table":
            self.table = []
            self.stack.append(("table", tag))
        elif tag == "tr":
            self.row = []
            self.stack.append(("tr", tag))
        elif tag in ("td", "th"):
            self.cell = ""
            self.stack.append(("cell", tag))
        elif tag == "hr":
            self.emit("\n\n---\n\n")

    def handle_endtag(self, tag):
        if tag == "iframe":
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        # pop matching frame
        while self.stack:
            kind, t = self.stack.pop()
            if t == tag:
                break
        if tag == "pre":
            code = self.pre_buf.strip("\n")
            self.emit("\n\n```\n" + code + "\n```\n\n")
            self.in_pre = False
        elif tag == "code" and not self.in_pre:
            self.emit("`")
        elif tag in ("strong", "b"):
            self.emit("**")
        elif tag in ("em", "i"):
            self.emit("*")
        elif tag in ("ul", "ol"):
            if self.list_stack:
                self.list_stack.pop()
            self.emit("\n")
        elif tag == "a":
            text = clean_text(self.link_text)
            # Brand rewording also applies to link text (it bypasses
            # handle_data, which is where prose replacement happens).
            text = text.replace("NetAdminHub", "Ramtin Tech Zone")
            href = self.link_href or ""
            if href and text:
                self.emit(f"[{text}]({href})")
            elif text:
                self.emit(text)
            self.in_link = False
            self.link_href = None
        elif tag == "table":
            self.emit(render_table(self.table))
            self.table = None
        elif tag == "tr":
            if self.table is not None and self.row is not None:
                self.table.append(self.row)
            self.row = None
        elif tag in ("td", "th"):
            if self.row is not None and self.cell is not None:
                self.row.append(clean_text(self.cell))
            self.cell = None

    def handle_data(self, data):
        if self.skip:
            return
        if self.in_pre:
            self.pre_buf += data
            return
        if self.cell is not None and self.cur() and self.cur()[0] == "cell":
            self.cell += data
            return
        if self.in_link:
            self.link_text += data
            return
        # Collapse inter-element whitespace: raw "\n\n\n\n" between blocks
        # must not leak into the Markdown as blank lines. A lone space right
        # after a newline is dropped; other whitespace collapses to one space.
        data = re.sub(r"\s+", " ", data)
        if data == " " and (not self.out or self.out[-1].endswith("\n")):
            return
        # brand rewording in prose (not in code/pre). Only the brand NAME is
        # rewritten -- lab subdomains such as file.netadminhub.com are config
        # values shown in the video and must stay exactly as recorded.
        data = data.replace("NetAdminHub", "Ramtin Tech Zone")
        self.emit(data)

    def get(self):
        md = "".join(self.out)
        md = re.sub(r"\n{3,}", "\n\n", md)
        md = "\n".join(line.rstrip() for line in md.split("\n"))
        return md.strip() + "\n"


def rewrite_link(href):
    if not href:
        return href
    # Old English-channel handle -> new handle.
    href = href.replace("youtube.com/@netadminhub", "youtube.com/@ramtintechzone")
    m = re.match(r"https?://netadminhub\.com/([^/]+)/?$", href)
    if m:
        return f"/posts/{m.group(1)}/"
    if href.startswith("https://netadminhub.com/"):
        return href.replace("https://netadminhub.com", "https://ramtin.zone", 1)
    return href


def render_table(rows):
    if not rows:
        return ""
    lines = ["\n"]
    for i, r in enumerate(rows):
        lines.append("| " + " | ".join(r) + " |")
        if i == 0:
            lines.append("| " + " | ".join("---" for _ in r) + " |")
    lines.append("")
    return "\n".join(lines) + "\n"


YT_RE = re.compile(r"(?:youtube\.com/embed/|youtu\.be/|youtube\.com/watch\?v=)([A-Za-z0-9_-]{11})")


def extract_youtube(html):
    m = YT_RE.search(html)
    return m.group(1) if m else None


def drop_video_promo(html):
    """Remove the 'Watch the Full Video' promo block (heading + next 3 <p>)
    and the 'this article is the reference for the video' blockquote from
    the raw HTML. The template renders the video embed from front matter,
    so both would duplicate it."""
    html = re.sub(
        r'<h3[^>]*>Watch the Full Video</h3>\s*(?:<p[^>]*>.*?</p>\s*){1,3}',
        "",
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = re.sub(
        r"<blockquote[^>]*>.*?command and configuration reference.*?</blockquote>",
        "",
        html,
        count=1,
        flags=re.DOTALL,
    )
    return html


def main():
    posts = json.load(open(EXPORT / "posts.json"))
    media = json.load(open(EXPORT / "media.json"))
    byid = {m["id"]: m for m in media}
    # WP REST API returns category names HTML-escaped ("Tips &amp; Tricks");
    # unescape once here so templates escape exactly once.
    cats = {c["id"]: html_lib.unescape(c["name"]) for c in json.load(open(EXPORT / "categories.json"))}
    OUT.mkdir(parents=True, exist_ok=True)
    for p in posts:
        html = p["content"]["rendered"]
        yt = extract_youtube(html)
        html = drop_video_promo(html)
        conv = MDConverter()
        conv.feed(html)
        md = conv.get()
        # excerpt -> description (unescape entities: &#8217; etc.)
        desc = re.sub(r"<[^>]+>", "", p["excerpt"]["rendered"])
        desc = clean_text(html_lib.unescape(desc))
        desc = desc.replace("NetAdminHub", "Ramtin Tech Zone")
        categories = [cats[c] for c in p["categories"] if c in cats and cats[c] != "Uncategorized"]
        fm = ["---"]
        fm.append(f'title: "{html_lib.unescape(p["title"]["rendered"]).replace(chr(34), chr(39))}"')
        fm.append(f"date: {p['date'][:10]}")
        fm.append(f"slug: {p['slug']}")
        fm.append("categories: [" + ", ".join(f'"{c}"' for c in categories) + "]")
        if yt:
            fm.append(f"youtube_id: {yt}")
        else:
            # Blog-only posts (no video): use the WordPress featured image
            # as the card/hero image, served locally from the repo.
            feat = byid.get(p["featured_media"])
            if feat and feat["source_url"] in IMAGE_MAP:
                fm.append(f"image: {IMAGE_MAP[feat['source_url']]}")
        fm.append(f'description: "{desc.replace(chr(34), chr(39))}"')
        fm.append("migrated_from: netadminhub.com")
        fm.append("---")
        path = OUT / f"{p['slug']}.md"
        path.write_text("\n".join(fm) + "\n\n" + md, encoding="utf-8")
        words = len(md.split())
        print(f"{p['slug'][:55]:55s} yt={yt or '-':12s} {words:5d} words -> {path.name}")
    print("migrated", len(posts), "posts")


if __name__ == "__main__":
    main()
