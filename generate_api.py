"""
Grant Watch ⌛ — Static API Generator
Splits grants.json into category-specific JSON files served by GitHub Pages.

Outputs (all under data/):
  data/by-type/fellowships.json
  data/by-type/travel.json
  data/by-type/bilateral.json
  data/by-type/startup.json
  data/by-type/conference.json
  data/by-type/research.json
  data/by-country/india.json
  data/by-country/international.json
  data/urgent.json            (from daily_check.py)
  data/feed.xml               (from generate_feed.py)

All accessible at:
  https://pranavathiyani.github.io/grantwatch/data/by-type/fellowships.json

Also generates a JSON Schema for the grant record format.
This supports:
  - Other SASTRA tools consuming specific grant categories
  - FAIR data compliance (citable, schema-documented)
  - Easy API consumption without a backend
"""

import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("data")


# Grant type groupings — maps display category → list of grant_type values
TYPE_GROUPS = {
    "fellowships":  ["Fellowship", "Postdoctoral Fellowship", "Award", "Award + Research Grant"],
    "travel":       ["Travel Grant"],
    "bilateral":    ["Collaborative Grant", "Seed / Networking Grant"],
    "startup":      ["Startup Grant", "Innovation Grant"],
    "conference":   ["Conference Grant"],
    "research":     ["Research Grant", "Infrastructure Grant", "Grand Challenge",
                     "Faculty Development Grant", "Reference Resource"],
}


def generate_static_api():
    if not (DATA_DIR / "grants.json").exists():
        print("grants.json not found")
        return

    with open(DATA_DIR / "grants.json") as f:
        grants = json.load(f)

    generated = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    open_grants = [g for g in grants if g.get("status") == "open"]

    # ── By type ───────────────────────────────────────────────
    type_dir = DATA_DIR / "by-type"
    type_dir.mkdir(exist_ok=True)

    for category, types in TYPE_GROUPS.items():
        filtered = [g for g in grants if g.get("grant_type") in types]
        filtered.sort(key=lambda g: (
            0 if g["status"] == "open" else 1,
            g.get("deadline") or "9999-12-31"
        ))
        out = {
            "category":   category,
            "generated":  generated,
            "total":      len(filtered),
            "open":       sum(1 for g in filtered if g["status"] == "open"),
            "grants":     filtered,
        }
        path = type_dir / f"{category}.json"
        path.write_text(json.dumps(out, indent=2, ensure_ascii=False))
        print(f"  → {path} ({len(filtered)} grants, {out['open']} open)")

    # ── By country ────────────────────────────────────────────
    country_dir = DATA_DIR / "by-country"
    country_dir.mkdir(exist_ok=True)

    for country_key in ("India", "International"):
        filtered = [g for g in grants if g.get("country") == country_key]
        filtered.sort(key=lambda g: g.get("deadline") or "9999-12-31")
        out = {
            "country":  country_key,
            "generated": generated,
            "total":    len(filtered),
            "open":     sum(1 for g in filtered if g["status"] == "open"),
            "grants":   filtered,
        }
        slug = country_key.lower().replace(" ", "_")
        path = country_dir / f"{slug}.json"
        path.write_text(json.dumps(out, indent=2, ensure_ascii=False))
        print(f"  → {path} ({len(filtered)} grants)")

    # ── Open grants only ──────────────────────────────────────
    out = {
        "description": "All currently open grant calls",
        "generated":   generated,
        "total":       len(open_grants),
        "grants":      open_grants,
    }
    (DATA_DIR / "open.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"  → data/open.json ({len(open_grants)} open grants)")

    print(f"\n✅ Static API endpoints generated under data/")


def generate_schema():
    """JSON Schema for the grant record — FAIR data compliance"""
    schema = {
        "$schema":     "https://json-schema.org/draft/2020-12/schema",
        "$id":         "https://pranavathiyani.github.io/grantwatch/data/grants-schema.json",
        "title":       "Grant Watch Grant Record",
        "description": "Schema for a single grant/fellowship/funding opportunity in Grant Watch ⌛",
        "type":        "object",
        "required":    ["id", "title", "agency", "country", "grant_type",
                        "amount", "url", "eligibility", "disciplines", "status"],
        "properties": {
            "id":          {"type": "string", "description": "Stable MD5-derived unique identifier"},
            "title":       {"type": "string", "description": "Full name of the funding opportunity"},
            "agency":      {"type": "string", "description": "Funding agency name"},
            "country":     {"type": "string", "enum": ["India", "International"],
                           "description": "Origin of funding"},
            "grant_type":  {"type": "string",
                           "description": "Category: Research Grant, Fellowship, Travel Grant, Collaborative Grant, etc."},
            "amount":      {"type": "string", "description": "Funding quantum (human-readable)"},
            "description": {"type": "string", "maxLength": 500},
            "url":         {"type": "string", "format": "uri",
                           "description": "Official application/information URL"},
            "deadline":    {"type": ["string", "null"], "format": "date",
                           "description": "Application deadline (ISO 8601 YYYY-MM-DD) or null if rolling"},
            "open_date":   {"type": ["string", "null"], "format": "date"},
            "eligibility": {"type": "array", "items": {"type": "string"},
                           "description": "Who can apply"},
            "disciplines": {"type": "array", "items": {"type": "string"},
                           "description": "Research disciplines covered"},
            "status":      {"type": "string", "enum": ["open", "closed"],
                           "description": "Current status"},
            "source":      {"type": "string", "description": "How this entry was obtained"},
            "last_updated":{"type": "string", "format": "date",
                           "description": "Date this record was last refreshed (YYYY-MM-DD)"},
        },
        "additionalProperties": True,
    }
    path = DATA_DIR / "grants-schema.json"
    path.write_text(json.dumps(schema, indent=2), encoding="utf-8")
    print(f"  → {path} (JSON Schema for FAIR data compliance)")


if __name__ == "__main__":
    print("Generating static API endpoints…")
    generate_static_api()
    print("\nGenerating JSON Schema…")
    generate_schema()
