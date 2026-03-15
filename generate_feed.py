"""
Grant Watch ⌛ — RSS Feed Generator
Produces data/feed.xml — a valid Atom feed of open grants with deadlines.

Researchers can subscribe in:
  - Feedly, Inoreader, NewsBlur (web RSS readers)
  - Thunderbird (email client)
  - Outlook (supports RSS)
  - Any RSS app on phone

No keys, no authentication, pure XML generation.
Called automatically by run_scrapers.py after each refresh.
"""

import json
from pathlib import Path
from datetime import datetime, timezone
from xml.sax.saxutils import escape

PORTAL_URL = "https://pranavathiyani.github.io/grantwatch"
FEED_URL   = f"{PORTAL_URL}/data/feed.xml"
AUTHOR     = "Grant Watch ⌛ · SASTRA University"
AUTHOR_EMAIL = "pranavathiyani@scbt.sastra.edu"


def generate_feed(grants_path: Path, output_path: Path, meta_path: Path) -> None:
    with open(grants_path) as f:
        grants = json.load(f)

    try:
        with open(meta_path) as f:
            meta = json.load(f)
        last_updated = meta.get("last_updated", datetime.now(timezone.utc).isoformat())
    except Exception:
        last_updated = datetime.now(timezone.utc).isoformat()

    # Only include open grants — prioritise those with deadlines
    open_grants = [g for g in grants if g.get("status") == "open"]
    open_grants.sort(key=lambda g: g.get("deadline") or "9999-12-31")

    # Limit to most relevant 100 entries
    feed_grants = open_grants[:100]

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<feed xmlns="http://www.w3.org/2005/Atom">',
        f'  <title>Grant Watch ⌛ — SASTRA Research Funding Portal</title>',
        f'  <subtitle>Curated research funding opportunities for Indian academics. Updated bi-weekly.</subtitle>',
        f'  <link href="{FEED_URL}" rel="self" type="application/atom+xml"/>',
        f'  <link href="{PORTAL_URL}" rel="alternate" type="text/html"/>',
        f'  <id>{FEED_URL}</id>',
        f'  <updated>{now_iso}</updated>',
        f'  <author><name>{escape(AUTHOR)}</name><email>{escape(AUTHOR_EMAIL)}</email></author>',
        f'  <rights>Data is publicly sourced. Grant Watch aggregates for SASTRA researchers.</rights>',
        '',
    ]

    for g in feed_grants:
        gid      = escape(g.get("id", ""))
        title    = escape(g.get("title", ""))
        agency   = escape(g.get("agency", ""))
        country  = escape(g.get("country", ""))
        gtype    = escape(g.get("grant_type", ""))
        amount   = escape(g.get("amount", "Varies"))
        deadline = g.get("deadline") or "Rolling / TBA"
        url      = g.get("url", PORTAL_URL)
        desc     = escape(g.get("description", ""))
        updated  = g.get("last_updated", "2026-01-01")
        discs    = ", ".join(g.get("disciplines", []))
        elig     = ", ".join(g.get("eligibility", []))
        status   = g.get("status", "open").upper()

        # Build a rich summary for the entry content
        content = (
            f"Agency: {agency} ({country}) | Type: {gtype} | Amount: {amount} | "
            f"Deadline: {deadline} | Status: {status} | "
            f"Disciplines: {discs} | Eligibility: {elig}. {desc}"
        )

        entry_id = f"{PORTAL_URL}#grant-{gid}"

        lines += [
            "  <entry>",
            f"    <id>{escape(entry_id)}</id>",
            f"    <title>[{escape(deadline)}] {title} — {agency}</title>",
            f"    <link href=\"{escape(url)}\" rel=\"alternate\"/>",
            f"    <updated>{updated}T00:00:00Z</updated>",
            f"    <summary type=\"text\">{escape(content[:500])}</summary>",
            f"    <category term=\"{escape(gtype)}\" label=\"{escape(gtype)}\"/>",
            f"    <category term=\"{escape(country)}\" label=\"{escape(country)}\"/>",
            "  </entry>",
            "",
        ]

    lines.append("</feed>")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  RSS feed written: {output_path} ({len(feed_grants)} entries)")


if __name__ == "__main__":
    base = Path("data")
    generate_feed(base / "grants.json", base / "feed.xml", base / "meta.json")
