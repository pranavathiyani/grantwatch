"""
Grant Watch ⌛ — Main Runner
Run this to refresh grants.json

Usage:
    python run_scrapers.py
    python run_scrapers.py --agency NIH        # single agency only
    python run_scrapers.py --dry-run           # print results, don't write
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from scrapers import ALL_SCRAPERS

DATA_DIR  = Path("data")
OUT_FILE  = DATA_DIR / "grants.json"
META_FILE = DATA_DIR / "meta.json"

DATA_DIR.mkdir(exist_ok=True)


def load_existing() -> dict:
    """Load existing grants keyed by ID"""
    if OUT_FILE.exists():
        with open(OUT_FILE) as f:
            return {g["id"]: g for g in json.load(f)}
    return {}


def merge(existing: dict, new_grants: list) -> list:
    """Merge new into existing — new wins on conflict"""
    merged = dict(existing)
    added = updated = 0
    for g in new_grants:
        if g["id"] not in merged:
            added += 1
        else:
            updated += 1
        merged[g["id"]] = g
    print(f"  Merge: +{added} new, ~{updated} updated, {len(merged)} total")
    return list(merged.values())


def expire_old(grants: list) -> list:
    """Mark grants past deadline as 'closed'"""
    today = datetime.utcnow().date()
    for g in grants:
        if g.get("deadline"):
            try:
                dl = datetime.strptime(g["deadline"], "%Y-%m-%d").date()
                if dl < today:
                    g["status"] = "closed"
            except ValueError:
                pass
    return grants


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--agency", help="Run only this agency scraper")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    scrapers = ALL_SCRAPERS
    if args.agency:
        scrapers = [s for s in ALL_SCRAPERS if s.AGENCY_NAME.lower() == args.agency.lower()]
        if not scrapers:
            print(f"Agency '{args.agency}' not found. Available: {[s.AGENCY_NAME for s in ALL_SCRAPERS]}")
            return

    existing = load_existing()
    print(f"Loaded {len(existing)} existing grants.\n")

    all_new = []
    for ScraperClass in scrapers:
        scraper = ScraperClass()
        results = scraper.run()
        all_new.extend(results)

    print(f"\nTotal scraped this run: {len(all_new)}")

    merged = merge(existing, all_new)
    merged = expire_old(merged)

    # Sort: open first, then by deadline ascending
    merged.sort(key=lambda g: (
        0 if g["status"] == "open" else 1,
        g.get("deadline") or "9999-12-31"
    ))

    if args.dry_run:
        print("\n[DRY RUN] Sample output:")
        for g in merged[:3]:
            print(json.dumps(g, indent=2))
        return

    with open(OUT_FILE, "w") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)

    meta = {
        "last_updated": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_grants": len(merged),
        "open_grants": sum(1 for g in merged if g["status"] == "open"),
        "agencies": list({g["agency"] for g in merged}),
    }
    with open(META_FILE, "w") as f:
        json.dump(meta, f, indent=2)

    print(f"\n✅ Written to {OUT_FILE}")
    print(f"   Total: {meta['total_grants']} | Open: {meta['open_grants']}")
    print(f"   Agencies: {', '.join(meta['agencies'])}")


if __name__ == "__main__":
    main()
