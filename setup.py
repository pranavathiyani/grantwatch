#!/usr/bin/env python3
"""
Grant Watch ⌛ — One-time Setup Script
Run this ONCE after cloning, before pushing to GitHub.

Usage:
    python setup.py pranavathiyani

This replaces YOUR_USERNAME with your real GitHub username in all files.
"""

import sys
import re
from pathlib import Path

PLACEHOLDER = "YOUR_USERNAME"

FILES_TO_UPDATE = [
    "generate_feed.py",
    "generate_api.py",
    "update_readme.py",
    "scrapers/par_indiabioscience_scrapers.py",
    "scrapers/icgeb_scraper.py",
    "README.md",
]


def setup(username: str):
    username = username.strip().lstrip("@")
    if not re.match(r'^[a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,38}$', username):
        print(f"❌ '{username}' doesn't look like a valid GitHub username.")
        sys.exit(1)

    print(f"Setting up Grant Watch ⌛ for GitHub user: {username}\n")
    updated = []

    for fname in FILES_TO_UPDATE:
        path = Path(fname)
        if not path.exists():
            print(f"  skip (not found): {fname}")
            continue
        original = path.read_text(encoding="utf-8")
        if PLACEHOLDER not in original:
            print(f"  skip (already set): {fname}")
            continue
        updated_text = original.replace(PLACEHOLDER, username)
        path.write_text(updated_text, encoding="utf-8")
        count = original.count(PLACEHOLDER)
        print(f"  ✓ {fname} ({count} replacement{'s' if count > 1 else ''})")
        updated.append(fname)

    print(f"\n✅ Done. {len(updated)} file(s) updated.")
    print(f"\nYour portal will be live at:")
    print(f"  https://{username}.github.io/grantwatch")
    print(f"\nNext steps:")
    print(f"  1. python run_scrapers.py    ← populate grants.json")
    print(f"  2. python generate_feed.py   ← build RSS feed")
    print(f"  3. python generate_api.py    ← build static API")
    print(f"  4. python update_readme.py   ← update README")
    print(f"  5. git add . && git commit -m 'init: Grant Watch setup'")
    print(f"  6. git push")
    print(f"  7. GitHub repo → Settings → Pages → main → / (root)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python setup.py <your-github-username>")
        print("Example: python setup.py pranavathiyani")
        sys.exit(1)
    setup(sys.argv[1])
