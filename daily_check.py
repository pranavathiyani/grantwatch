"""
Grant Watch ⌛ — Daily Deadline Monitor
Runs daily (not bi-weekly). Reads existing grants.json, writes data/urgent.json.

This means the urgency banner in the portal refreshes EVERY DAY
not just bi-weekly — you'll catch deadlines that sneak up.

No scraping, no external requests. Pure local computation.
Called by .github/workflows/daily_check.yml
"""

import json
from pathlib import Path
from datetime import datetime, date

DATA_DIR   = Path("data")
GRANTS_FILE = DATA_DIR / "grants.json"
URGENT_FILE = DATA_DIR / "urgent.json"
META_FILE  = DATA_DIR / "meta.json"


def days_until(deadline_str: str) -> int | None:
    if not deadline_str:
        return None
    try:
        dl = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        return (dl - date.today()).days
    except ValueError:
        return None


def run():
    if not GRANTS_FILE.exists():
        print("grants.json not found — skipping")
        return

    with open(GRANTS_FILE) as f:
        grants = json.load(f)

    today = date.today().isoformat()
    urgent_7   = []   # closing in 7 days
    urgent_14  = []   # closing in 14 days
    urgent_30  = []   # closing in 30 days

    for g in grants:
        if g.get("status") != "open":
            continue
        d = days_until(g.get("deadline"))
        if d is None or d < 0:
            continue
        entry = {
            "id":       g["id"],
            "title":    g["title"],
            "agency":   g["agency"],
            "url":      g["url"],
            "deadline": g["deadline"],
            "days_left": d,
            "amount":   g.get("amount", ""),
            "grant_type": g.get("grant_type", ""),
        }
        if d <= 7:
            urgent_7.append(entry)
        elif d <= 14:
            urgent_14.append(entry)
        elif d <= 30:
            urgent_30.append(entry)

    # Sort each bucket by days_left
    for bucket in (urgent_7, urgent_14, urgent_30):
        bucket.sort(key=lambda x: x["days_left"])

    urgent_data = {
        "checked_on":  today,
        "closing_7d":  urgent_7,
        "closing_14d": urgent_14,
        "closing_30d": urgent_30,
        "summary": {
            "critical":  len(urgent_7),
            "warning":   len(urgent_14),
            "upcoming":  len(urgent_30),
        },
    }

    with open(URGENT_FILE, "w") as f:
        json.dump(urgent_data, f, indent=2, ensure_ascii=False)

    print(f"✅ urgent.json updated [{today}]")
    print(f"   Critical (≤7d):  {len(urgent_7)}")
    print(f"   Warning  (≤14d): {len(urgent_14)}")
    print(f"   Upcoming (≤30d): {len(urgent_30)}")

    if urgent_7:
        print("\n⚠ CRITICAL deadlines:")
        for g in urgent_7:
            print(f"   [{g['days_left']}d] {g['title']} — {g['agency']}")


if __name__ == "__main__":
    run()
