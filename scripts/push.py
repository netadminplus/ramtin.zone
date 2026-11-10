#!/usr/bin/env python3
"""Push the site/ tree to netadminplus/ramtin.zone via the Git Data API.

The repo contents ARE the site source (repo root == site/): content/,
templates/, static/, scripts/, .github/, requirements.txt, README.md.
The dist/ build output is NOT committed; the Deploy workflow builds it.

Usage: python3 scripts/push.py [--message "msg"] [--branch main]
Uses the stored custom.github credential via the surrogate exchange.
"""
import argparse
import base64
import json
import sys
import urllib.request
import urllib.error
from pathlib import Path

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request

HERE = Path(__file__).resolve().parent
SITE = HERE.parent
REPO = "netadminplus/ramtin.zone"
API = "https://api.github.com"

SKIP_DIRS = {"dist", "__pycache__", ".venv", ".git", "transcripts"}
SKIP_SUFFIXES = (".pyc",)


def api(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(API + path, data=data, method=method)
    if data:
        req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    add_surrogate_to_request(req, "custom.github", allowed_hosts=["api.github.com"])
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} {method} {path}: {e.read().decode()[:300]}", file=sys.stderr)
        raise


def collect_files():
    files = []
    for p in sorted(SITE.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(SITE)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if rel.suffix in SKIP_SUFFIXES:
            continue
        if rel.name == ".DS_Store":
            continue
        files.append((str(rel), p))
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--message", default="Initial site: migrated WordPress content + generator")
    ap.add_argument("--branch", default="main")
    args = ap.parse_args()

    files = collect_files()
    print(f"{len(files)} files to push")

    # The Git Data API refuses blobs in a totally empty repo, so bootstrap
    # the first commit through the Contents API when the branch is missing.
    parents = []
    try:
        ref = api("GET", f"/repos/{REPO}/git/ref/heads/{args.branch}")
        parents = [ref["object"]["sha"]]
        print("parent commit:", parents[0][:12])
    except urllib.error.HTTPError as e:
        if e.code in (404, 409):
            # 404: ref missing. 409 "Git Repository is empty": the repo has
            # no commits at all yet. Both mean: bootstrap the first commit.
            print("no existing branch -- bootstrapping with an initial commit")
            readme = (SITE / "README.md").read_bytes()
            api("PUT", f"/repos/{REPO}/contents/README.md",
                {"message": "Initial commit", "content": base64.b64encode(readme).decode()})
            ref = api("GET", f"/repos/{REPO}/git/ref/heads/{args.branch}")
            parents = [ref["object"]["sha"]]
            print("bootstrap commit:", parents[0][:12])
        else:
            raise

    blobs = []
    for rel, path in files:
        raw = path.read_bytes()
        b = api("POST", f"/repos/{REPO}/git/blobs",
                {"content": base64.b64encode(raw).decode(), "encoding": "base64"})
        blobs.append({"path": rel, "mode": "100644", "type": "blob", "sha": b["sha"]})
        print(f"  blob {rel} ({len(raw)}B)")
    tree = api("POST", f"/repos/{REPO}/git/trees", {"tree": blobs})
    print("tree:", tree["sha"][:12])

    commit = api("POST", f"/repos/{REPO}/git/commits",
                 {"message": args.message, "tree": tree["sha"], "parents": parents})
    print("commit:", commit["sha"])
    api("PATCH", f"/repos/{REPO}/git/refs/heads/{args.branch}", {"sha": commit["sha"]})
    print(f"pushed to {REPO}@{args.branch}: {commit['sha']}")
    print(f"https://github.com/{REPO}/commit/{commit['sha']}")


if __name__ == "__main__":
    main()
