#!/usr/bin/env python3
"""
Grant Watch ⌛ — Precise Fix
Run: python precise_fix.py

Targets exactly what's still wrong:
  1. ANRF 21 → inspect which files still have ANRF scrapers, show them
  2. NIH Fogarty missing → re-add 2 curated entries
  3. Various (Travel/Startup/plain) → reassign or delete directly in grants.json
  4. EMBO 23 → cap at 10 most relevant
  5. Git push
"""

import json, sys, subprocess
from pathlib import Path
from collections import Counter

ROOT     = Path(__file__).parent
SCRAPERS = ROOT / "scrapers"

# ─────────────────────────────────────────────────────────────────────────────
print("\n=== STEP 1: Find what's still generating ANRF entries ===\n")
# ─────────────────────────────────────────────────────────────────────────────

for f in sorted(SCRAPERS.glob("*.py")):
    txt = f.read_text(encoding='utf-8')
    if 'AGENCY_NAME.*ANRF' in txt or '"ANRF"' in txt or "'ANRF'" in txt:
        # Count how many classes output ANRF
        import re
        classes = re.findall(r'class (\w+Scraper)\b', txt)
        anrf_classes = []
        for cls in classes:
            # Find the class body
            m = re.search(rf'class {cls}.*?(?=\nclass |\Z)', txt, re.DOTALL)
            if m and ('ANRF' in m.group()):
                anrf_classes.append(cls)
        if anrf_classes:
            print(f"  {f.name}: {anrf_classes}")

# ─────────────────────────────────────────────────────────────────────────────
print("\n=== STEP 2: Direct grants.json surgery ===\n")
# ─────────────────────────────────────────────────────────────────────────────

grants_path = ROOT / "data" / "grants.json"
with open(grants_path) as f:
    grants = json.load(f)

before = len(grants)

# --- Show what ANRF entries exist ---
anrf = [g for g in grants if g['agency'] == 'ANRF']
print(f"Current ANRF entries ({len(anrf)}):")
for g in anrf:
    print(f"  [{g.get('deadline','—')}] {g['title'][:75]}")

print()

# --- Show Various* ---
various = [g for g in grants if g['agency'].startswith('Various')]
print(f"Various* entries ({len(various)}):")
for g in various:
    print(f"  [{g['agency']}] {g['title'][:65]}")

print()

# ─────────────────────────────────────────────────────────────────────────────
print("\n=== STEP 3: Clean grants.json ===\n")
# ─────────────────────────────────────────────────────────────────────────────

# Known good ANRF titles (our curated 11)
ANRF_KEEP = {
    "anrf advanced research grant (arg) — pre-proposals 2026",
    "anrf matrics 2026 (mathematics research grant)",
    "anrf national postdoctoral fellowship (n-pdf) 2026",
    "anrf prime minister early career research grant (pm-ecrg) 2026",
    "anrf ramanujan fellowship 2026",
    "anrf jc bose grant 2026",
    "anrf inclusivity research grant (irg) 2026 — new scheme",
    "anrf national science chair (nsc) 2026",
    "anrf-atri scheme 2026",
    "anrf tare (teachers associateship for research excellence)",
    "anrf international travel support (its)",
}

# Various agency fixes
TRAVEL_KEEP   = {"ACM", "IARCS"}
STARTUP_MAP   = {
    "NIDHI": "DST", "DST-NIDHI": "DST",
    "BIRAC": "BIRAC",
    "Startup India": "DPIIT", "SISFS": "DPIIT",
    "TIDE": "MeitY", "MeitY": "MeitY",
}

cleaned = []
embo_count = 0

for g in grants:
    agency = g['agency']
    title  = g['title'].strip()
    tl     = title.lower()

    # ── ANRF: keep only curated 11 ──────────────────────────────────────────
    if agency == 'ANRF':
        if tl not in ANRF_KEEP:
            continue   # drop duplicates / extra scraped entries

    # ── Various (Travel) ────────────────────────────────────────────────────
    elif agency == 'Various (Travel)':
        if any(k in title for k in TRAVEL_KEEP):
            g['agency'] = 'ACM-India'
        else:
            continue   # drop: ANRF ITS dup, CSIR travel dup, dashes, closed

    # ── Various (Startup) ───────────────────────────────────────────────────
    elif agency == 'Various (Startup)':
        matched = False
        for keyword, new_agency in STARTUP_MAP.items():
            if keyword in title:
                g['agency'] = new_agency
                matched = True
                break
        if not matched:
            g['agency'] = 'DST'
        # Drop ANRF dup
        if 'ANRF PM Early Career' in title and 'Startup' in title:
            continue

    # ── Various (plain) → INSA/NASI/IASc ───────────────────────────────────
    elif agency == 'Various':
        g['agency'] = 'INSA/NASI/IASc'

    # ── EMBO: cap at 12 ─────────────────────────────────────────────────────
    elif agency == 'EMBO':
        embo_count += 1
        if embo_count > 12:
            continue

    # ── General garbage ─────────────────────────────────────────────────────
    if set(title) <= set('-— \u2014\u2013'):
        continue
    if len(title) < 6:
        continue
    if title == 'Call for Proposals' and agency in ('DST', 'ICMR'):
        continue
    if 'MeitY-NSF' in title and agency == 'DST (Bilateral)':
        continue
    if 'MSR India Academic Outreach' in title:
        continue
    if 'Google: Conference Scholarships' in title:
        continue

    cleaned.append(g)

# Dedup by title
seen, deduped = {}, []
for g in cleaned:
    key = g['title'].lower().strip()
    if key not in seen:
        seen[key] = True
        deduped.append(g)

# ── Add NIH Fogarty curated entries (currently missing) ─────────────────────
fogarty_titles = {g['title'].lower() for g in deduped if g['agency'] == 'NIH Fogarty'}
fogarty_new = [
    {
        "id": "nih-fogarty-firca-2026",
        "title": "NIH Fogarty FIRCA — International Research Collaboration Award",
        "agency": "NIH Fogarty", "agency_country": "International",
        "url": "https://www.fic.nih.gov/Funding/Pages/default.aspx",
        "deadline": None, "open_date": None, "status": "open",
        "description": (
            "Designed specifically for researchers in LMICs including India. "
            "Indian PI collaborates with NIH-funded US researcher. "
            "Indian PI applies directly — best NIH entry point for Indian researchers."
        ),
        "grant_type": "Collaborative Grant",
        "eligibility": ["Faculty", "Researcher at Indian Institution"],
        "disciplines": ["Global Health", "Biomedical", "Infectious Disease"],
        "amount": "Up to USD 50,000/year (3 years)",
    },
    {
        "id": "nih-fogarty-global-health-2026",
        "title": "NIH Fogarty Global Health Research Training Programs",
        "agency": "NIH Fogarty", "agency_country": "International",
        "url": "https://www.fic.nih.gov/Funding/Pages/default.aspx",
        "deadline": None, "open_date": None, "status": "open",
        "description": (
            "Portfolio of Fogarty programmes in global health, infectious disease, "
            "neuroscience, and bioethics. India consistently a top recipient country."
        ),
        "grant_type": "Research Grant",
        "eligibility": ["Faculty", "Researcher", "Indian Institution"],
        "disciplines": ["Global Health", "Infectious Disease", "Neuroscience"],
        "amount": "Varies by specific FOA",
    },
]
for entry in fogarty_new:
    if entry['title'].lower() not in fogarty_titles:
        deduped.append(entry)
        print(f"  + Added: {entry['title']}")

# Sort: open first, deadline asc
deduped.sort(key=lambda g: (
    0 if g.get('status') == 'open' else 1,
    g.get('deadline') or '9999-12-31'
))

with open(grants_path, 'w') as f:
    json.dump(deduped, f, indent=2, ensure_ascii=False)

# ─────────────────────────────────────────────────────────────────────────────
print("\n=== STEP 4: Final count ===\n")
# ─────────────────────────────────────────────────────────────────────────────

counts = Counter(g['agency'] for g in deduped)
print(f"Total: {len(deduped)}  |  Before: {before}  |  Removed: {before - len(deduped)}")
print()
for a, c in sorted(counts.items(), key=lambda x: -x[1]):
    flag = ' ⚠ STILL HIGH' if c > 15 else ''
    print(f"  {c:3d}  {a}{flag}")

# Check no Various* remain
remaining_various = [g for g in deduped if g['agency'].startswith('Various')]
if remaining_various:
    print(f"\n  ⚠ Still has {len(remaining_various)} Various* entries:")
    for g in remaining_various:
        print(f"    [{g['agency']}] {g['title'][:60]}")
else:
    print("\n  ✓ No Various* entries remain")

# ─────────────────────────────────────────────────────────────────────────────
print("\n=== STEP 5: Git push ===\n")
# ─────────────────────────────────────────────────────────────────────────────

for cmd in [
    ["git", "add", "data/grants.json"],
    ["git", "commit", "-m", "fix: precise cleanup — ANRF dedup, fix Various, cap EMBO, add Fogarty"],
    ["git", "push"],
]:
    print(f"$ {' '.join(cmd)}")
    subprocess.run(cmd, cwd=ROOT)

print("\n✅ Done.")
