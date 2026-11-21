#!/usr/bin/env python3
"""Refresh YouTube view counts in data/videos.json.

The site's post cards show each video's view count from data/videos.json
(matched by youtube_id in build.py). That file was written once, when each
video was first fetched, and nothing ever updated it — so the counts on the
cards froze at first-fetch values (e.g. CMR stuck at 1,106 while the real
count passed 6,500).

What this does:
1. Fetches the channel uploads playlist with yt-dlp (flat, no downloads).
   One call returns id + view_count + duration for every video.
2. For each playlist entry: updates view_count (and duration) of the
   matching entry in data/videos.json; adds a minimal entry for a video
   that has a post but no videos.json entry yet (e.g. a video published
   after the last sync run).
3. Writes the file back only if something changed.

Videos that left the playlist (removed/private) are left untouched, never
deleted — a missing playlist entry is not proof the video is gone.

Runs in GitHub Actions from the daily sync workflow (see
.github/workflows/sync.yml) right after sync.py, so the counts refresh
every morning and the push triggers the Deploy rebuild. The workflow step
uses continue-on-error: a YouTube bot-check must never block the
new-video sync; the old counts simply stay for another day.

Local run:  python3 scripts/refresh_views.py
(yt-dlp must be on PATH; locally: PATH=~/workspace/bin:$PATH)
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = HERE.parent
DATA = SITE / "data"
CONTENT = SITE / "content" / "posts"
CHANNEL = "https://www.youtube.com/@ramtintechzone/videos"

# Same player-client workaround as sync.py: plain yt-dlp defaults get
# bot-checked from some IPs; the Android client plus no downloads works.
YT_BASE = ["yt-dlp", "--extractor-args", "youtube:player_client=android"]


def post_ids():
    ids = set()
    for p in CONTENT.glob("*.md"):
        m = re.search(r"^youtube_id:\s*(\S+)", p.read_text(), re.MULTILINE)
        if m:
            ids.add(m.group(1))
    return ids


def main():
    vf = DATA / "videos.json"
    videos = json.load(open(vf)) if vf.exists() else []
    by_id = {v["id"]: v for v in videos}
    have_posts = post_ids()

    try:
        playlist = json.loads(
            subprocess.run(
                YT_BASE + ["--flat-playlist", "-J", CHANNEL],
                capture_output=True, text=True, check=True,
            ).stdout
        )
    except subprocess.CalledProcessError as e:
        print(f"playlist fetch failed ({(e.stderr or '')[:200]})", file=sys.stderr)
        print("keeping existing view counts", file=sys.stderr)
        return 1

    updated, added = 0, 0
    movers = []
    for entry in playlist.get("entries", []):
        vid = entry["id"]
        vc = entry.get("view_count")
        if vc is None:
            continue
        if vid in by_id:
            old = by_id[vid].get("view_count")
            if old != vc:
                by_id[vid]["view_count"] = vc
                if entry.get("duration"):
                    by_id[vid]["duration"] = entry["duration"]
                updated += 1
                movers.append((vid, old, vc))
        elif vid in have_posts:
            by_id[vid] = {
                "id": vid,
                "title": entry.get("title", ""),
                "description": "",
                "view_count": vc,
                "duration": entry.get("duration"),
                "upload_date": entry.get("upload_date"),
            }
            videos.append(by_id[vid])
            added += 1

    if not updated and not added:
        print("no view-count changes")
        return 0

    json.dump(videos, open(vf, "w"), indent=2, ensure_ascii=False)
    print(f"updated {updated} view counts, added {added} missing videos")
    for vid, old, new in sorted(movers, key=lambda m: (m[2] or 0) - (m[1] or 0), reverse=True)[:5]:
        print(f"  {vid}: {old} -> {new}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
