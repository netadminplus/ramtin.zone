#!/usr/bin/env python3
"""Migrate WordPress static pages (About, Donate) to Markdown.

The Contact page is a form and is replaced by a hand-written contact.md.
Run: python3 scripts/migrate-pages.py
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from migrate import MDConverter

HERE = Path(__file__).resolve().parent
EXPORT = HERE.parent.parent / "netadminhub-export"
OUT = HERE.parent / "content" / "pages"


def main():
    pages = json.load(open(EXPORT / "pages.json"))
    OUT.mkdir(parents=True, exist_ok=True)
    for pg in pages:
        if pg["slug"] == "contact":
            continue  # form page -- replaced by hand-written contact.md
        conv = MDConverter()
        conv.feed(pg["content"]["rendered"])
        md = conv.get()
        title = pg["title"]["rendered"].replace("NetAdminHub", "Ramtin Tech Zone")
        fm = f"---\ntitle: \"{title.replace(chr(34), chr(39))}\"\nslug: {pg['slug']}\n---\n\n"
        (OUT / f"{pg['slug']}.md").write_text(fm + md, encoding="utf-8")
        print("wrote", pg["slug"], len(md.split()), "words")


if __name__ == "__main__":
    main()
