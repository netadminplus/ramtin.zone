#!/usr/bin/env python3
"""Mechanical checks for a ramtin.zone blog post draft.

Usage:
  python3 scripts/verify_article.py content/posts/<slug>.md [--log verification/<slug>.md]

Enforces the PIPELINE.md Stage 5 gates. Exit 0 when no errors are found
(warnings are allowed), 1 when any check fails. This checker catches form,
not truth: claim-to-source tracing is verified by reading the log, not by
this script.
"""
import argparse
import re
import sys
from pathlib import Path

BANNED = [
    # VTT junk and transcript filler
    "kind: captions", "language: en", "you can see", "you know",
    "right?", "uh,", "uh ", "let me show you",
    # AI filler / generic boilerplate
    "delve", "in today's fast-paced", "it's important to note",
    "moreover", "landscape", "crucial", "as an ai", "in conclusion",
    "in this tutorial i will walk you through",
    "in this tutorial i walk through the whole setup",
]
REQUIRED_FM = ["title:", "date:", "slug:", "categories:", "youtube_id:",
               "description:"]


def sections(body):
    """Split the body into (heading, text) pairs by ## headings."""
    parts = re.split(r"^## (.+)$", body, flags=re.M)
    out = []
    intro = parts[0].strip()
    if intro:
        out.append(("(intro)", intro))
    for i in range(1, len(parts), 2):
        heading = parts[i].strip()
        text = parts[i + 1].strip() if i + 1 < len(parts) else ""
        out.append((heading, text))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("post")
    ap.add_argument("--log")
    args = ap.parse_args()

    errors, warnings = [], []
    text = Path(args.post).read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        print("ERROR: no YAML front matter block")
        return 1
    fm, body = m.group(1), text[m.end():]

    for field in REQUIRED_FM:
        if field not in fm:
            errors.append(f"front matter missing {field}")
    if "auto_generated: true" in fm:
        warnings.append("auto_generated: true on this article — "
                        "hand-written articles must not carry it")

    words = len(body.split())
    if words < 300:
        errors.append(f"body is {words} words (minimum 300)")
    if words > 2100:
        errors.append(f"body is {words} words (maximum 2100)")

    low = body.lower()
    for phrase in BANNED:
        for i, line in enumerate(body.splitlines(), 1):
            if phrase in line.lower():
                errors.append(f'banned phrase "{phrase}" on line {i}')

    secs = sections(body)
    if not any(h != "(intro)" for h, _ in secs):
        errors.append("no ## sections found")
    for heading, sec in secs:
        n = len(sec.split())
        if n > 400:
            errors.append(f'section "{heading}" is {n} words '
                          f"(maximum 400 — a transcript dump hides here)")
        if heading.lower().startswith("commands used"):
            for line in sec.splitlines():
                line = line.strip().strip("`")
                if line and line.endswith("."):
                    errors.append(f"command line ends with a period "
                                  f"(narration, not a command): {line[:60]}")

    if args.log:
        log = Path(args.log)
        if not log.exists():
            errors.append(f"verification log missing: {args.log}")
        else:
            log_text = log.read_text(encoding="utf-8")
            if "| Verified" not in log_text and "Verified" not in log_text:
                errors.append("verification log has no verified claims")
            removed = re.findall(r"\| \"([^\"]+)\" \|", log_text)
            for claim in removed:
                if claim[:40] in body:
                    errors.append(f"removed claim still in article: "
                                  f"{claim[:60]}")

    for e in errors:
        print(f"ERROR: {e}")
    for w in warnings:
        print(f"WARN: {w}")
    print(f"{'FAIL' if errors else 'PASS'}: {args.post} "
          f"({words} words, {len(secs)} sections, "
          f"{len(errors)} errors, {len(warnings)} warnings)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
