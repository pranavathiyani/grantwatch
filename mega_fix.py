#!/usr/bin/env python3
"""
Grant Watch ⌛ — MEGA FIX
Run: python mega_fix.py

Fixes everything in one shot:
  1. Remove duplicate ANRF scrapers from additional_fellowship_scrapers.py
  2. Remove duplicate NIH Fogarty scrapers from fellowship_scrapers.py
  3. Clean grants.json — remove all old ANRF/Fogarty/Various noise
  4. Re-run scrapers to repopulate cleanly
  5. Update index.html — stopwatch favicon + logo
  6. Git commit + push
"""

import os, sys, json, re, subprocess
from pathlib import Path
from collections import Counter

ROOT     = Path(__file__).parent
SCRAPERS = ROOT / "scrapers"

# ─────────────────────────────────────────────────────────────────────────────
print("\n=== STEP 1: Remove duplicate ANRF classes from additional scrapers ===\n")
# ─────────────────────────────────────────────────────────────────────────────

# These files contain ANRF-labelled scraper classes that duplicate anrf_scraper.py
DUPE_ANRF_CLASSES = [
    "ANRFNPDFScraper", "ANRFSRGScraper", "ANRFPMECRGScraper",
    "ANRFTAREScraper", "ANRFITSScraper", "ANRFCRGScraper",
    "ANRFRamanujanScraper", "ANRFJCBoseScraper", "ANRFIRGScraper",
    "ANRFNSCScraper", "ANRFATRIScraper", "ANRFMATRICScraper",
    "AdditionalANRFScraper",
]

DUPE_FOGARTY_CLASSES = [
    "NIHFogartyScraper2", "FogartyScraper", "NIHFogartyExtendedScraper",
]

def remove_class_from_file(filepath: Path, class_names: list) -> int:
    if not filepath.exists():
        return 0
    content = filepath.read_text(encoding='utf-8')
    removed = 0
    for cls in class_names:
        # Find class definition and remove until next class or EOF
        pattern = rf'\n\nclass {cls}\b.*?(?=\n\nclass |\Z)'
        new_content, n = re.subn(pattern, '', content, flags=re.DOTALL)
        if n:
            content = new_content
            removed += n
            print(f"  Removed {cls} from {filepath.name}")
    if removed:
        filepath.write_text(content, encoding='utf-8')
    return removed

for fname in ["additional_fellowship_scrapers.py", "fellowship_scrapers.py",
              "additional_agencies_scrapers.py", "new_agency_scrapers.py",
              "embo_conference_startup_scrapers.py"]:
    fpath = SCRAPERS / fname
    r1 = remove_class_from_file(fpath, DUPE_ANRF_CLASSES)
    r2 = remove_class_from_file(fpath, DUPE_FOGARTY_CLASSES)
    if r1 + r2 == 0:
        print(f"  {fname} — no duplicates found (ok)")

# Also remove from __init__.py registry
init_path = SCRAPERS / "__init__.py"
if init_path.exists():
    init = init_path.read_text(encoding='utf-8')
    original_init = init
    for cls in DUPE_ANRF_CLASSES + DUPE_FOGARTY_CLASSES:
        init = re.sub(rf'\s*{cls},?\s*#[^\n]*\n', '\n', init)
        init = re.sub(rf'\s*{cls},\n', '\n', init)
        init = re.sub(rf',\s*{cls}', '', init)
    if init != original_init:
        init_path.write_text(init, encoding='utf-8')
        print("  Updated __init__.py registry")

print("✓ Duplicate class check done")

# ─────────────────────────────────────────────────────────────────────────────
print("\n=== STEP 2: Clean grants.json ===\n")
# ─────────────────────────────────────────────────────────────────────────────

grants_path = ROOT / "data" / "grants.json"
with open(grants_path) as f:
    grants = json.load(f)

before = len(grants)

# Agency fixes
def fix_agency(g):
    agency = g["agency"]
    title  = g["title"]
    if agency == "Various":
        g["agency"] = "INSA/NASI/IASc"
    elif agency == "Various (Travel)":
        if "ACM" in title or "IARCS" in title:
            g["agency"] = "ACM-India"
        else:
            g["_delete"] = True
    elif agency == "Various (Startup)":
        if "NIDHI" in title or "DST-NIDHI" in title:
            g["agency"] = "DST"
        elif "BIRAC" in title:
            g["agency"] = "BIRAC"
        elif "Startup India" in title or "SISFS" in title:
            g["agency"] = "DPIIT"
        elif "TIDE" in title or "MeitY" in title:
            g["agency"] = "MeitY"
        else:
            g["agency"] = "DST"
    return g

def is_garbage(g):
    title = g.get("title", "").strip()
    agency = g.get("agency", "")
    if g.get("_delete"):                                          return True
    if set(title) <= set("-— \u2014\u2013"):                      return True
    if len(title) < 6:                                            return True
    if "MSR India Academic Outreach" in title:                    return True
    if "Google: Conference Scholarships" in title:                return True
    if title == "Call for Proposals" and agency in ("DST","ICMR"):return True
    if "MeitY-NSF" in title and agency == "DST (Bilateral)":     return True
    if agency == "NCBS":                                          return True
    if "ANRF PM Early Career Research Grant — Startup" in title:  return True
    # NIH noise — admin notices, training-only
    if agency in ("NIH", "NIH Fogarty") and any(x in title for x in [
        "NOT-", "Notice of", "Notice to", "Training Grant",
        "Loan Repayment", "AHRQ", "Supplement", "Chronic, Noncommunicable",
        "Global Infectious", "HIV Research Training", "International Bioethics",
    ]):
        return True
    return False

# Remove old scraped ANRF and NIH Fogarty entries (will repopulate from curated scrapers)
# Keep only entries with descriptions > 100 chars (curated) or known good ones
RECURATE_AGENCIES = {"ANRF", "NIH Fogarty"}

cleaned = []
for g in grants:
    g = fix_agency(g)
    if is_garbage(g):
        continue
    agency = g["agency"]
    # For re-curated agencies, drop entries with short/generic descriptions
    if agency in RECURATE_AGENCIES:
        desc = g.get("description", "")
        title = g["title"]
        # Drop if description is too short (scraped noise)
        if len(desc) < 100:
            continue
        # Drop generic scraped titles
        if title in ("NIH Fogarty International Center", "Fogarty",
                     "ANRF", "Call for Proposals", "Research Grants"):
            continue
    cleaned.append(g)

# Dedup by title
seen, deduped = {}, []
for g in cleaned:
    key = g["title"].lower().strip()
    if key not in seen:
        seen[key] = True
        deduped.append(g)

# Cap NIH Fogarty at 5 (curated entries only)
fogarty_count = 0
final = []
for g in deduped:
    if g["agency"] == "NIH Fogarty":
        if fogarty_count >= 5:
            continue
        fogarty_count += 1
    final.append(g)

with open(grants_path, "w") as f:
    json.dump(final, f, indent=2, ensure_ascii=False)

print(f"grants.json: {before} → {len(final)} (removed {before - len(final)})")
counts = Counter(g["agency"] for g in final)
print("\nAgencies after clean:")
for a, c in sorted(counts.items(), key=lambda x: -x[1]):
    print(f"  {c:3d}  {a}")

# ─────────────────────────────────────────────────────────────────────────────
print("\n=== STEP 3: Run scrapers to repopulate ===\n")
# ─────────────────────────────────────────────────────────────────────────────

subprocess.run([sys.executable, "run_scrapers.py"], cwd=ROOT)

# ─────────────────────────────────────────────────────────────────────────────
print("\n=== STEP 4: Regenerate feed, API, README ===\n")
# ─────────────────────────────────────────────────────────────────────────────

for script in ["generate_feed.py", "generate_api.py", "update_readme.py"]:
    if (ROOT / script).exists():
        subprocess.run([sys.executable, script], cwd=ROOT)

# ─────────────────────────────────────────────────────────────────────────────
print("\n=== STEP 5: Update index.html — stopwatch favicon + logo ===\n")
# ─────────────────────────────────────────────────────────────────────────────

html_path = ROOT / "index.html"
if not html_path.exists():
    html_path = ROOT / "frontend" / "index.html"

if html_path.exists():
    html = html_path.read_text(encoding='utf-8')

    # 1 — Favicon (inline SVG data URI — stopwatch)
    FAVICON = '''<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%23b45309'/%3E%3Ccircle cx='16' cy='19' r='9' fill='none' stroke='%23fef3c7' stroke-width='2'/%3E%3Ccircle cx='16' cy='19' r='9' fill='%2392400e' opacity='0.4'/%3E%3Crect x='13' y='7' width='6' height='3' rx='1.5' fill='%23fef3c7'/%3E%3Cline x1='12' y1='9' x2='10' y2='12' stroke='%23fef3c7' stroke-width='1.8' stroke-linecap='round'/%3E%3Cline x1='20' y1='9' x2='22' y2='12' stroke='%23fef3c7' stroke-width='1.8' stroke-linecap='round'/%3E%3Cline x1='16' y1='19' x2='16' y2='12' stroke='%23fef3c7' stroke-width='2' stroke-linecap='round'/%3E%3Cline x1='16' y1='19' x2='22' y2='16' stroke='%23f0b429' stroke-width='1.5' stroke-linecap='round'/%3E%3Ccircle cx='16' cy='19' r='1.8' fill='%23fef3c7'/%3E%3Cline x1='16' y1='11' x2='16' y2='12.5' stroke='%23fef3c7' stroke-width='1.2' stroke-linecap='round' opacity='0.6'/%3E%3Cline x1='25' y1='19' x2='23.5' y2='19' stroke='%23fef3c7' stroke-width='1.2' stroke-linecap='round' opacity='0.6'/%3E%3Cline x1='16' y1='27' x2='16' y2='25.5' stroke='%23fef3c7' stroke-width='1.2' stroke-linecap='round' opacity='0.6'/%3E%3Cline x1='7' y1='19' x2='8.5' y2='19' stroke='%23fef3c7' stroke-width='1.2' stroke-linecap='round' opacity='0.6'/%3E%3C/svg%3E">'''

    if '<link rel="icon"' not in html:
        html = html.replace('</title>', f'</title>\n{FAVICON}')
        print("  ✓ Favicon added")
    else:
        # Replace existing favicon
        html = re.sub(r'<link rel="icon"[^>]+>', FAVICON, html)
        print("  ✓ Favicon replaced")

    # 2 — Logo SVG (stopwatch replacing hourglass)
    NEW_SVG = '''    <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" style="flex-shrink:0;">
      <rect width="40" height="40" rx="10" fill="#b45309"/>
      <!-- Stopwatch body circle -->
      <circle cx="20" cy="25" r="12" fill="none" stroke="#fef3c7" stroke-width="2.2"/>
      <circle cx="20" cy="25" r="12" fill="#92400e" opacity="0.35"/>
      <!-- Crown / top button -->
      <rect x="16.5" y="9" width="7" height="3" rx="1.5" fill="#fef3c7"/>
      <!-- Left lug -->
      <line x1="14" y1="11" x2="11" y2="14" stroke="#fef3c7" stroke-width="2" stroke-linecap="round"/>
      <!-- Right lug -->
      <line x1="26" y1="11" x2="29" y2="14" stroke="#fef3c7" stroke-width="2" stroke-linecap="round"/>
      <!-- Minute hand — pointing to 12 -->
      <line x1="20" y1="25" x2="20" y2="16" stroke="#fef3c7" stroke-width="2.2" stroke-linecap="round"/>
      <!-- Second hand — amber, pointing to ~2 -->
      <line x1="20" y1="25" x2="28" y2="21" stroke="#f0b429" stroke-width="1.8" stroke-linecap="round"/>
      <!-- Center dot -->
      <circle cx="20" cy="25" r="2.2" fill="#fef3c7"/>
      <!-- Tick marks N E S W -->
      <line x1="20" y1="14" x2="20" y2="15.8" stroke="#fef3c7" stroke-width="1.5" stroke-linecap="round" opacity="0.55"/>
      <line x1="32" y1="25" x2="30.2" y2="25" stroke="#fef3c7" stroke-width="1.5" stroke-linecap="round" opacity="0.55"/>
      <line x1="20" y1="36" x2="20" y2="34.2" stroke="#fef3c7" stroke-width="1.5" stroke-linecap="round" opacity="0.55"/>
      <line x1="8" y1="25" x2="9.8" y2="25" stroke="#fef3c7" stroke-width="1.5" stroke-linecap="round" opacity="0.55"/>
    </svg>'''

    # Replace the old SVG (hourglass or any previous stopwatch)
    old_svg_pattern = r'<svg width="3[68]" height="3[68]".*?</svg>'
    new_html, n = re.subn(old_svg_pattern, NEW_SVG.strip(), html, count=1, flags=re.DOTALL)
    if n:
        html = new_html
        print("  ✓ Logo SVG replaced with stopwatch")
    else:
        print("  ⚠ Logo SVG pattern not matched — check header manually")

    # 3 — Dark mode toggle button (add if not present)
    if 'dark-toggle' not in html:
        html = html.replace(
            '<div class="meta-badge">Updated <b id="last-updated">—</b></div>\n  </div>',
            '<div class="meta-badge">Updated <b id="last-updated">—</b></div>\n    <button class="dark-toggle" onclick="toggleDark()" id="theme-btn" title="Toggle dark mode">🌙</button>\n  </div>'
        )
        print("  ✓ Dark mode toggle button added")

    # 4 — Dark mode CSS (add after :root block if not present)
    if '[data-theme="dark"]' not in html:
        dark_css = '''
  [data-theme="dark"] {
    --bg: #0d1117; --bg2: #161b22; --bg3: #1c2330;
    --border: #30363d; --text: #e6edf3; --text2: #8b949e; --text3: #6e7681;
    --accent: #f0b429; --accent2: #e09000;
    --india: #ff7043; --intl: #4fc3f7; --open: #56d364; --closed: #f85149;
  }
  body { transition: background 0.2s, color 0.2s; }
  .dark-toggle {
    background: var(--bg3); border: 1px solid var(--border);
    border-radius: 20px; padding: 4px 10px; font-size: 16px;
    cursor: pointer; color: var(--text2); line-height: 1;
    transition: background 0.2s;
  }
  .dark-toggle:hover { background: var(--border); }
  [data-theme="dark"] .sastra-badge { background:#1a2332; border-color:#2d4a7a; color:#4fc3f7; }
  [data-theme="dark"] select,
  [data-theme="dark"] input { background:var(--bg3); color:var(--text); border-color:var(--border); }
  [data-theme="dark"] #urgency-banner { background:#2a2000; border-color:#f0b429; color:#f0b429; }
  [data-theme="dark"] .tag.active { background:#2a2000; }'''

        html = html.replace('</style>', dark_css + '\n</style>')
        print("  ✓ Dark mode CSS added")

    # 5 — Dark mode JS (add if not present)
    if 'toggleDark' not in html:
        dark_js = '''
  function toggleDark() {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    document.documentElement.setAttribute('data-theme', isDark ? 'light' : 'dark');
    document.getElementById('theme-btn').textContent = isDark ? '🌙' : '☀️';
    localStorage.setItem('gw-theme', isDark ? 'light' : 'dark');
  }
  // Apply saved theme on load
  (function() {
    const saved = localStorage.getItem('gw-theme') || 'light';
    document.documentElement.setAttribute('data-theme', saved);
    window.addEventListener('DOMContentLoaded', function() {
      const btn = document.getElementById('theme-btn');
      if (btn) btn.textContent = saved === 'dark' ? '☀️' : '🌙';
    });
  })();'''
        html = html.replace('</script>', dark_js + '\n</script>')
        print("  ✓ Dark mode JS added")

    # 6 — Update tag-row to use category filter
    if 'data-filter="Fellowship"' in html and 'data-group="category"' not in html:
        old_tags = re.search(r'<div class="tag-row">.*?</div>', html, re.DOTALL)
        if old_tags:
            new_tags = '''<div class="tag-row">
  <span class="tag-label">Filter:</span>
  <span class="tag active" data-group="reset"    data-filter="all">All</span>
  <span class="tag india"  data-group="country"  data-filter="India">🇮🇳 Indian</span>
  <span class="tag intl"   data-group="country"  data-filter="International">🌐 International</span>
  <span class="tag"        data-group="status"   data-filter="open">Open now</span>
  <span class="tag"        data-group="type"     data-filter="Research Grant">Research</span>
  <span class="tag"        data-group="type"     data-filter="Fellowship">Fellowship</span>
  <span class="tag"        data-group="type"     data-filter="Travel Grant">Travel</span>
  <span class="tag"        data-group="type"     data-filter="Collaborative Grant">Bilateral</span>
  <span class="tag"        data-group="type"     data-filter="Startup Grant">Startup</span>
  <span class="tag"        data-group="type"     data-filter="Award">Awards</span>
</div>'''
            html = html[:old_tags.start()] + new_tags + html[old_tags.end():]
            print("  ✓ Filter tags updated")

    html_path.write_text(html, encoding='utf-8')
    print(f"  ✓ Saved {html_path}")
else:
    print("  ⚠ index.html not found at root or frontend/")

# ─────────────────────────────────────────────────────────────────────────────
print("\n=== STEP 6: Final count ===\n")
# ─────────────────────────────────────────────────────────────────────────────

with open(grants_path) as f:
    final = json.load(f)

counts = Counter(g["agency"] for g in final)
print(f"Total: {len(final)}  |  Open: {sum(1 for g in final if g.get('status')=='open')}")
print()
for a, c in sorted(counts.items(), key=lambda x: -x[1]):
    flag = " ⚠" if c > 20 else ""
    print(f"  {c:3d}  {a}{flag}")

# ─────────────────────────────────────────────────────────────────────────────
print("\n=== STEP 7: Git commit + push ===\n")
# ─────────────────────────────────────────────────────────────────────────────

cmds = [
    ["git", "add", "."],
    ["git", "commit", "-m",
     "fix: mega cleanup — dedup ANRF/Fogarty, clean Various, stopwatch logo+favicon, dark mode"],
    ["git", "push"],
]
for cmd in cmds:
    print(f"$ {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode != 0:
        print("⚠ Failed — check above")
        break

print("\n✅ Done. Live at https://pranavathiyani.github.io/grantwatch")
