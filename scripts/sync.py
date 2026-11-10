#!/usr/bin/env python3
"""Daily sync: turn new long-form @ramtintechzone videos into blog posts.

Runs in GitHub Actions (see .github/workflows/sync.yml) and locally:
  python3 scripts/sync.py [--dry-run]

What it does:
1. Fetches the channel uploads playlist with yt-dlp (flat, no downloads).
2. Skips Shorts (duration <= 90s) and videos that already have a post
   (matched by youtube_id in content/posts/*.md front matter).
3. For each new long video: fetches full metadata + English transcript,
   then drafts a short structured reference in Ramtin's structure (intro,
   what you will learn, key takeaways, commands, closing) and writes
   content/posts/<slug>.md.
4. Rebuilds the site (scripts/build.py).

The draft is a short reference distilled from the transcript, never a
paste of transcript prose. A transcript is spoken language (filler, ASR
errors, "you can see") and pasting it as the article body is wrong: the
18 articles generated that way in Nov 2026 were pulled off the live site
the same day. Full articles in Ramtin's voice are written by hand;
this generator only produces the short reference draft.
Ramtin reviews new posts and edits them in the repo;
later sync runs never overwrite an existing post file.
"""
import argparse
import json
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = HERE.parent
CONTENT = SITE / "content" / "posts"
CHANNEL = "https://www.youtube.com/@ramtintechzone/videos"

# YouTube bot-checks plain yt-dlp defaults from some IPs (this VM included):
# the first fetch pass failed 25/31 with "Sign in to confirm you're not a
# bot" and all subtitle downloads hit 429s. The Android player client plus
# sleeps between requests works; subtitles fall back to the timedtext URL
# straight from the video metadata. (2026-11-10 fetch run.)
YT_BASE = ["yt-dlp", "--extractor-args", "youtube:player_client=android"]

FILLER_STARTS = (
    "so ", "and so ", "you know ", "like ", "right? ", "okay ", "ok ",
    "um ", "uh ", "basically ", "actually ", "literally ",
)

CATEGORY_KEYWORDS = [
    (("mikrotik", "routeros", "chr", "winbox", "capsman"), "MikroTik"),
    (("openwrt", "openwrt"), "OpenWrt"),
    (("wireguard", "vpn", "tailscale", "netbird", "openconnect", "v2ray"), "VPN"),
    (("voip", "ucaas", "issabel", "sip"), "VoIP"),
    (("windows",), "Windows"),
    (("ai ", "ai-", "claude", "agent", "llm", "ollama", "copilot"), "AI×Networking"),
]


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, check=True, **kw)


def existing_ids():
    ids = set()
    for p in CONTENT.glob("*.md"):
        m = re.search(r"^youtube_id:\s*(\S+)", p.read_text(), re.MULTILINE)
        if m:
            ids.add(m.group(1))
    return ids


def slugify(title):
    s = title.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-+", "-", s).strip("-") or "untitled"
    if len(s) > 80:
        # Truncate at a word boundary so slugs never end mid-word.
        s = s[:80].rsplit("-", 1)[0]
    return s or "untitled"


def clean_description(desc):
    """First 2-3 real sentences of the video description, minus links/tags."""
    desc = re.sub(r"https?://\S+", "", desc or "")
    desc = re.sub(r"#\w+", "", desc)
    desc = re.sub(r"\n+", " ", desc)
    sentences = re.split(r"(?<=[.!?])\s+", desc.strip())
    keep = [s for s in sentences if len(s) > 40][:3]
    return " ".join(keep)


def clean_sentence(s):
    s = re.sub(r"\[.*?\]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    low = s.lower()
    for f in FILLER_STARTS:
        if low.startswith(f):
            s = s[len(f):]
            s = s[:1].upper() + s[1:] if s else s
            break
    return s


def transcript_sentences(vtt_path):
    """Parse a .vtt transcript into clean sentences."""
    text = Path(vtt_path).read_text(errors="ignore")
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith(("WEBVTT", "NOTE", "Kind:", "Language:")) or "-->" in line:
            continue
        if re.match(r"^\d+$", line):
            continue
        # strip <c> tags and timestamps
        line = re.sub(r"<[^>]+>", "", line)
        if line and (not lines or lines[-1] != line):
            lines.append(line)
    joined = " ".join(lines)
    parts = re.split(r"(?<=[.!?])\s+", joined)
    out = []
    for p in parts:
        s = clean_sentence(p)
        if len(s) > 50 and not re.search(r"(subscribe|like this video|comment below)", s, re.I):
            out.append(s)
    return out


def timedtext_transcript(video, tmp):
    """Fallback: download the auto-caption .vtt straight from the timedtext
    URL in the video metadata (no yt-dlp involved). Returns sentences or []."""
    for source in ("automatic_captions", "subtitles"):
        tracks = (video.get(source) or {}).get("en") or []
        for t in tracks:
            if t.get("ext") == "vtt" and t.get("url"):
                try:
                    req = urllib.request.Request(
                        t["url"], headers={"User-Agent": "Mozilla/5.0"})
                    data = urllib.request.urlopen(req, timeout=30).read()
                    tmp.write_bytes(data)
                    return transcript_sentences(tmp)
                except Exception:
                    continue
    return []


# Words that never appear in a real command line — ASR narration always
# contains some of them ("System and then resources, you can see...").
PROSE_WORDS = {
    "you", "can", "see", "then", "when", "this", "that", "with", "and",
    "the", "is", "are", "it", "your", "we", "i", "my", "me", "lets",
    "let", "now", "here", "there", "so", "just", "what", "how", "why",
    "who", "all", "any", "some", "no", "not", "only", "also", "still",
    "again", "first", "next", "last", "new", "good", "easy", "sure",
    "right", "well", "yeah", "yes", "please", "was", "were", "will",
    "would", "should", "could", "have", "has", "had", "do", "does",
    "did", "be", "been", "if", "but", "or", "he", "she", "they", "them",
    "his", "her", "their", "us", "our", "its", "that's", "don't",
    "can't", "gonna", "wanna", "really", "very", "much", "many", "more",
    "most", "other", "another", "same", "different", "way", "thing",
    "things", "video", "channel", "hello", "hi", "guys", "okay", "ok",
    "im", "i'm", "we're", "you're", "it's", "there's", "here's",
}


def key_takeaways(sentences, limit=8):
    """The most informative transcript sentences, as a short summary.

    A transcript is not an article: this picks a few substantive sentences
    (no filler starts, no questions, no "you can see" narration) instead
    of pasting the whole transcript. At most `limit` sentences.
    """
    narration = re.compile(
        r"(you can see|let me|let's|you know|right\?|as you can see|"
        r"thank you for watching|subscribe|like this video|comment below)",
        re.I)
    out = []
    for s in sentences:
        if len(out) >= limit:
            break
        low = s.lower()
        if low.startswith(FILLER_STARTS):
            continue
        if "?" in s or narration.search(s):
            continue
        if len(s) < 80:
            continue
        out.append(s)
    return out


def extract_commands(sentences):
    """Lines that look like real RouterOS / shell commands.

    The start pattern alone is not enough — ASR narration often begins with
    a command word ("System and then resources, you can see I'm on the
    7.26 beta 1."). A real command has no prose words and never ends with
    a sentence period, so both are required.
    """
    cmds = []
    pat = re.compile(r"^(/[\w-]+|ip |interface|system|user |ssh |docker |sudo |apt |set |add |print)", re.I)
    for s in sentences:
        if not pat.match(s) or len(s) > 120:
            continue
        if s.rstrip().endswith("."):
            continue
        words = re.findall(r"[a-z']+", s.lower())
        if any(w.strip("'") in PROSE_WORDS for w in words):
            continue
        cmds.append(s)
    return cmds[:12]


def infer_categories(title, description):
    hay = (title + " " + (description or "")).lower()
    cats = [name for keys, name in CATEGORY_KEYWORDS if any(k in hay for k in keys)]
    cats.append("Youtube Videos")
    return cats or ["Youtube Videos"]


def draft_article(video, transcript):
    title = video["title"]
    desc = video.get("description", "")
    chapters = video.get("chapters") or []
    sentences = transcript
    cmds = extract_commands(sentences)
    takeaways = key_takeaways(sentences)

    lines = []
    intro = clean_description(desc)
    if intro:
        lines.append(intro)
        lines.append("")
    lines.append(
        "The video above shows the full lab; below is the written reference "
        "so you can follow along or copy the commands."
    )
    lines.append("")
    if chapters:
        lines.append("## What you will learn")
        lines.append("")
        for ch in chapters:
            lines.append(f"- {ch.get('title', '').strip()}")
        lines.append("")
    # Short distilled summary only. NEVER paste transcript sentences as
    # prose: the whole-transcript "How it works" section this function
    # used to generate was wrong and its 18 articles were pulled from
    # the live site in Nov 2026.
    if takeaways:
        lines.append("## Key takeaways")
        lines.append("")
        for t in takeaways:
            lines.append(f"- {t}")
        lines.append("")
    if cmds:
        lines.append("## Commands used")
        lines.append("")
        lines.append("```")
        lines.extend(cmds)
        lines.append("```")
        lines.append("")
    lines.append("## Wrapping up")
    lines.append("")
    lines.append(
        "If this helped, subscribe to Ramtin Tech Zone on YouTube for more "
        "MikroTik, Linux, networking, VPN and AI tutorials — and if a script "
        "or tutorial saved you time, consider supporting the work on the "
        "Donate page."
    )
    lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    have = existing_ids()
    print(f"{len(have)} posts already exist")
    playlist = json.loads(
        run(YT_BASE + ["--flat-playlist", "-J", CHANNEL]).stdout
    )
    new = []
    for entry in playlist.get("entries", []):
        vid = entry["id"]
        if vid in have:
            continue
        new.append(entry)
    print(f"{len(new)} new videos to check")
    made = 0
    for entry in new:
        vid = entry["id"]
        try:
            video = json.loads(
                run(YT_BASE + ["-J", f"https://www.youtube.com/watch?v={vid}"]).stdout
            )
        except subprocess.CalledProcessError as e:
            print(f"  {vid}: metadata failed ({e.stderr[:120]})")
            continue
        time.sleep(3)
        duration = video.get("duration") or 0
        if duration <= 90:
            print(f"  {vid}: Short ({duration}s), skipped")
            continue
        # transcript
        transcript = []
        tmp = SITE / "data" / "transcripts" / f"{vid}.en.vtt"
        try:
            run(YT_BASE + [
                "--write-auto-subs", "--write-subs",
                "--sub-lang", "en", "--skip-download",
                "--sub-format", "vtt",
                "-o", str(tmp.with_suffix("")),
                f"https://www.youtube.com/watch?v={vid}",
            ])
            cand = list(tmp.parent.glob(f"{vid}*.vtt"))
            if cand:
                transcript = transcript_sentences(cand[0])
        except subprocess.CalledProcessError:
            print(f"  {vid}: yt-dlp subtitles failed, trying timedtext fallback")
        if not transcript:
            transcript = timedtext_transcript(video, tmp)
        if not transcript:
            print(f"  {vid}: no transcript available")
        time.sleep(3)
        article = draft_article(video, transcript)
        slug = slugify(video["title"])
        cats = infer_categories(video["title"], video.get("description", ""))
        fm = [
            "---",
            f'title: "{video["title"].replace(chr(34), chr(39))}"',
            f"date: {video['upload_date'][:4]}-{video['upload_date'][4:6]}-{video['upload_date'][6:]}",
            f"slug: {slug}",
            "categories: [" + ", ".join(f'"{c}"' for c in cats) + "]",
            f"youtube_id: {vid}",
            f"description: \"{clean_description(video.get('description', ''))[:200].replace(chr(34), chr(39))}\"",
            "auto_generated: true",
            "---",
            "",
        ]
        path = CONTENT / f"{slug}.md"
        if path.exists():
            print(f"  {vid}: {slug}.md already exists, skipped")
            continue
        if args.dry_run:
            print(f"  DRY RUN: would create {slug}.md ({len(article.split())} words)")
        else:
            path.write_text("\n".join(fm) + article, encoding="utf-8")
            print(f"  created {slug}.md ({len(article.split())} words)")
        made += 1
    print(f"done: {made} new posts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
