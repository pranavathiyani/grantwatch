"""
Grant Watch ⌛ — README Auto-Updater
Rewrites README.md with live stats from grants.json + meta.json.
Also archives the previous grants.json snapshot to data/archive/.

Called by both workflows — bi-weekly scrape and daily check.
"""

import json
import shutil
from pathlib import Path
from datetime import datetime

DATA_DIR    = Path("data")
ARCHIVE_DIR = DATA_DIR / "archive"
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

README_PATH = Path("README.md")
MAX_ARCHIVES = 6   # keep last 6 snapshots = 3 months


def archive_snapshot():
    """Keep a dated copy of grants.json before overwriting"""
    src = DATA_DIR / "grants.json"
    if not src.exists():
        return
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    dst = ARCHIVE_DIR / f"grants-{date_str}.json"
    if not dst.exists():
        shutil.copy2(src, dst)
        print(f"  Archived → {dst}")

    # Prune old archives
    archives = sorted(ARCHIVE_DIR.glob("grants-*.json"))
    while len(archives) > MAX_ARCHIVES:
        oldest = archives.pop(0)
        oldest.unlink()
        print(f"  Pruned old archive: {oldest.name}")


def update_readme():
    try:
        with open(DATA_DIR / "grants.json") as f:
            grants = json.load(f)
        with open(DATA_DIR / "meta.json") as f:
            meta = json.load(f)
    except Exception as e:
        print(f"Could not read data files: {e}")
        return

    total      = len(grants)
    open_g     = sum(1 for g in grants if g["status"] == "open")
    india_g    = sum(1 for g in grants if g["agency_country"] == "India")
    intl_g     = sum(1 for g in grants if g["agency_country"] == "International")
    fellows    = sum(1 for g in grants if "Fellowship" in g.get("grant_type",""))
    travel_g   = sum(1 for g in grants if g.get("grant_type") == "Travel Grant")
    collab_g   = sum(1 for g in grants if g.get("grant_type") == "Collaborative Grant")
    updated    = meta.get("last_updated", "N/A")[:10]
    agencies   = sorted({g["agency"] for g in grants})

    # Find grants closing within 30 days
    today = datetime.utcnow().date()
    upcoming = []
    for g in grants:
        if g.get("status") != "open" or not g.get("deadline"):
            continue
        try:
            dl = datetime.strptime(g["deadline"], "%Y-%m-%d").date()
            d  = (dl - today).days
            if 0 <= d <= 30:
                upcoming.append((d, g["title"], g["agency"], g["deadline"]))
        except ValueError:
            pass
    upcoming.sort()

    upcoming_rows = ""
    for d, title, agency, deadline in upcoming[:10]:
        tag = "🔴" if d <= 7 else "🟡"
        upcoming_rows += f"| {tag} **{d}d** | {title} | {agency} | {deadline} |\n"
    if not upcoming_rows:
        upcoming_rows = "| — | No grants closing in 30 days | — | — |\n"

    agency_list = "\n".join(f"- {a}" for a in agencies)

    readme = f"""# Grant Watch ⌛
**SASTRA Deemed University — Research Funding Portal**

> One-stop aggregator for Indian and international research funding calls.
> Auto-refreshed bi-weekly. Data is public. No login required.

🔗 **[Open Portal →](https://pranavathiyani.github.io/grantwatch)**
📡 **[Subscribe RSS →](https://pranavathiyani.github.io/grantwatch/data/feed.xml)**

---

## Live Stats · Last updated {updated}

| Metric | Count |
|--------|-------|
| 📋 Total grants indexed | **{total}** |
| ✅ Open calls | **{open_g}** |
| 🇮🇳 Indian agency grants | **{india_g}** |
| 🌍 International grants | **{intl_g}** |
| 🎓 Fellowships | **{fellows}** |
| ✈️ Travel grants | **{travel_g}** |
| 🤝 Bilateral collaborations | **{collab_g}** |

---

## ⚠ Closing within 30 days

| Urgency | Grant | Agency | Deadline |
|---------|-------|--------|----------|
{upcoming_rows}
---

## Quick Start (WSL / Ubuntu)

```bash
git clone https://github.com/pranavathiyani/grantwatch.git
cd grantwatch
conda create -n grantwatch python=3.11 -y && conda activate grantwatch
pip install -r requirements.txt
python run_scrapers.py          # refresh all grants
python generate_feed.py         # rebuild RSS feed
python generate_api.py          # rebuild static API endpoints
cd frontend && python -m http.server 8080   # preview locally
```

## Automation

| Workflow | Schedule | What it does |
|----------|----------|--------------|
| Bi-Weekly Refresh | 1st & 15th of month, 11:30 IST | Runs all scrapers, updates `grants.json` |
| Daily Deadline Check | Every day, 12:00 IST | Updates `urgent.json`, `feed.xml`, this README |

## Static API Endpoints (GitHub Pages)

All served from `data/` — no backend, pure JSON over GitHub Pages.

```
/data/grants.json             # Full dataset
/data/open.json               # Open grants only
/data/urgent.json             # Closing within 30 days (updated daily)
/data/feed.xml                # Atom RSS feed
/data/grants-schema.json      # JSON Schema (FAIR data)
/data/by-type/fellowships.json
/data/by-type/travel.json
/data/by-type/bilateral.json
/data/by-type/startup.json
/data/by-type/research.json
/data/by-country/india.json
/data/by-country/international.json
/data/archive/                # Last 6 bi-weekly snapshots
```

## Agencies Covered ({len(agencies)})

{agency_list}

---

*Developed for **SASTRA University** by **Pranavathiyani G** ☮️ · Co-developed with **Claude** 💜*
*Data is publicly sourced. Grant Watch aggregates for non-commercial academic use.*
"""

    README_PATH.write_text(readme, encoding="utf-8")
    print(f"  README.md updated ({total} grants, {open_g} open)")


if __name__ == "__main__":
    archive_snapshot()
    update_readme()
