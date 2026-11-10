# ramtin.zone — Ramtin Tech Zone blog

Static blog for the English YouTube channel **@ramtintechzone**, built from
the channel's long-form videos plus the migrated WordPress articles from
netadminhub.com. No WordPress, no database, no server — plain HTML on
GitHub Pages at [ramtin.zone](https://ramtin.zone).

## How it works

- Content lives as Markdown in `content/posts/` (one file per tutorial)
  and `content/pages/` (About, Donate, Contact).
- `scripts/build.py` renders the whole site into `dist/`.
- GitHub Pages is deployed by `.github/workflows/deploy.yml`, which builds
  `dist/` and publishes it on every push to `main` (Actions-based
  Pages, custom domain `ramtin.zone` via the `CNAME` file in the build).
- Thumbnails come from the YouTube CDN (`i.ytimg.com`); article screenshots
  are stored in `assets/images/`.

## Local build

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build.py
# preview: cd dist && python3 -m http.server 8931
```

## Automatic updates

`.github/workflows/sync.yml` runs daily at 07:00 Tehran:

1. Checks the channel uploads for new **long-form** videos (Shorts skipped).
2. Fetches metadata + transcript, drafts a full article in Ramtin's
   structure (intro, what you will learn, chapter sections, commands),
   and writes `site/content/posts/<slug>.md` (`auto_generated: true`).
3. Rebuilds the site and commits the result.

Existing posts are never overwritten. Drafted articles are real content
from the transcript — Ramtin reviews new posts and edits them in the repo.

## Structure

```
content/posts/*.md      # tutorials (migrated + new)
  content/pages/*.md      # about / donate / contact
templates/              # Jinja2 templates
static/css|js|images/   # theme assets
scripts/build.py        # generator
scripts/sync.py         # daily YouTube -> post sync
scripts/migrate.py      # one-off WordPress -> Markdown migration
.github/workflows/      # daily sync + deploy workflows
```

## Design

Modern minimal dark theme, Inter font, Lucide + Simple Icons inlined as
SVG (zero external icon requests). Mobile-first, responsive grid.
