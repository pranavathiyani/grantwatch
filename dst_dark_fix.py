#!/usr/bin/env python3
"""
Grant Watch ⌛ — DST clean + Dark mode fix
Run: python dst_dark_fix.py
"""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).parent

# ─────────────────────────────────────────────────────────────────────────────
print("\n=== STEP 1: Clean DST noise from grants.json ===\n")
# ─────────────────────────────────────────────────────────────────────────────

# These are DST website navigation links that got scraped as "grants"
DST_DELETE = {
    "schemes/ programmes",
    "s&t capacity building programmes",
    "institutional capacity building programmes",
    "research & development programmes",
    "innovation and technology development programmes",
    "science for society programmes",
    "science, technology & innovation policy 2013",
    "awards/prize/result",
    "call for proposals",
    "international cooperation calls/announcements/results",
    "archive call for proposals",
}

grants_path = ROOT / "data" / "grants.json"
with open(grants_path) as f:
    grants = json.load(f)

before = len(grants)

# Also merge INSA → INSA/NASI/IASc while we're here
cleaned = []
for g in grants:
    title_l = g["title"].strip().lower()
    if g["agency"] == "DST" and title_l in DST_DELETE:
        print(f"  ✗ Removed: {g['title']}")
        continue
    if g["agency"] == "INSA":
        g["agency"] = "INSA/NASI/IASc"
    cleaned.append(g)

# Dedup by title
seen, deduped = {}, []
for g in cleaned:
    key = g["title"].lower().strip()
    if key not in seen:
        seen[key] = True
        deduped.append(g)

with open(grants_path, "w") as f:
    json.dump(deduped, f, indent=2, ensure_ascii=False)

from collections import Counter
counts = Counter(g["agency"] for g in deduped)
print(f"\nBefore: {before}  →  After: {len(deduped)}\n")
print("Agency counts:")
for a, c in sorted(counts.items(), key=lambda x: -x[1]):
    print(f"  {c:3d}  {a}")

# ─────────────────────────────────────────────────────────────────────────────
print("\n=== STEP 2: Fix dark mode in index.html ===\n")
# ─────────────────────────────────────────────────────────────────────────────

html_path = ROOT / "index.html"
if not html_path.exists():
    html_path = ROOT / "frontend" / "index.html"

if not html_path.exists():
    print("⚠ index.html not found")
    sys.exit(1)

html = html_path.read_text(encoding="utf-8")

# ── 1. Dark mode CSS ─────────────────────────────────────────────────────────
DARK_CSS = """
  /* ── Dark mode ── */
  [data-theme="dark"] {
    --bg: #0d1117;
    --bg2: #161b22;
    --bg3: #1c2330;
    --border: #30363d;
    --text: #e6edf3;
    --text2: #8b949e;
    --text3: #6e7681;
    --accent: #f0b429;
    --accent2: #e09000;
    --india: #ff7043;
    --intl: #4fc3f7;
    --open: #56d364;
    --closed: #f85149;
  }
  body { transition: background 0.25s, color 0.25s; }
  .dark-toggle {
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 5px 11px;
    font-size: 16px;
    cursor: pointer;
    color: var(--text2);
    line-height: 1;
    transition: background 0.2s;
    flex-shrink: 0;
  }
  .dark-toggle:hover { background: var(--border); }
  [data-theme="dark"] .sastra-badge {
    background: #1a2332;
    border-color: #2d4a7a;
    color: #4fc3f7;
  }
  [data-theme="dark"] select,
  [data-theme="dark"] input {
    background: var(--bg3);
    color: var(--text);
    border-color: var(--border);
  }
  [data-theme="dark"] #urgency-banner {
    background: #2a2000;
    border-color: #f0b429;
    color: #f0b429;
  }
  [data-theme="dark"] .tag.active { background: #2a2000; color: var(--accent); }
  [data-theme="dark"] .badge-open   { background: #0a200a; }
  [data-theme="dark"] .badge-closed { background: #200a0a; }
"""

if "[data-theme=\"dark\"]" not in html:
    html = html.replace("</style>", DARK_CSS + "</style>")
    print("  ✓ Dark mode CSS added")
else:
    # Replace existing dark mode CSS block cleanly
    html = re.sub(
        r'/\* ── Dark mode ──.*?(?=\n  /\*|\n</style>)',
        DARK_CSS.strip(),
        html, flags=re.DOTALL
    )
    print("  ✓ Dark mode CSS updated")

# ── 2. Dark toggle button in header ─────────────────────────────────────────
if 'dark-toggle' not in html:
    # Add button right before closing </div> of header-right
    html = html.replace(
        '<div class="meta-badge">Updated <b id="last-updated">—</b></div>\n  </div>',
        '<div class="meta-badge">Updated <b id="last-updated">—</b></div>\n    '
        '<button class="dark-toggle" id="theme-btn" onclick="toggleDark()" title="Toggle dark mode">🌙</button>\n  </div>'
    )
    print("  ✓ Dark toggle button added to header")
else:
    print("  ✓ Dark toggle button already present")

# ── 3. Dark mode JS — replace any broken version ─────────────────────────────
DARK_JS = """
  // ── Dark mode ──
  function toggleDark() {
    const root = document.documentElement;
    const isDark = root.getAttribute('data-theme') === 'dark';
    const next = isDark ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    const btn = document.getElementById('theme-btn');
    if (btn) btn.textContent = next === 'dark' ? '☀️' : '🌙';
    try { localStorage.setItem('gw-theme', next); } catch(e) {}
  }
  // Apply saved theme immediately (before paint)
  (function() {
    var saved = 'light';
    try { saved = localStorage.getItem('gw-theme') || 'light'; } catch(e) {}
    document.documentElement.setAttribute('data-theme', saved);
    document.addEventListener('DOMContentLoaded', function() {
      var btn = document.getElementById('theme-btn');
      if (btn) btn.textContent = saved === 'dark' ? '☀️' : '🌙';
    });
  })();
"""

# Remove any existing toggleDark function first
html = re.sub(
    r'\s*// ── Dark mode ──.*?(?=\n\s*//|\n\s*function (?!toggleDark)|\n</script>)',
    '',
    html, flags=re.DOTALL
)
html = re.sub(r'\s*function toggleDark\(\).*?\n  \}', '', html, flags=re.DOTALL)
html = re.sub(r'\s*\(function\(\) \{[^}]*gw-theme[^}]*\}\)\(\);', '', html, flags=re.DOTALL)

# Add clean version before </script>
if '</script>' in html:
    html = html.replace('</script>', DARK_JS + '\n</script>', 1)
    print("  ✓ Dark mode JS added/replaced")
else:
    # No script tag — add one before </body>
    html = html.replace('</body>', f'<script>{DARK_JS}\n</script>\n</body>')
    print("  ✓ Dark mode JS added in new script tag")

# ── 4. Stopwatch favicon (replace or add) ───────────────────────────────────
FAVICON = (
    "<link rel=\"icon\" type=\"image/svg+xml\" href=\"data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
    "%3Crect width='32' height='32' rx='8' fill='%23b45309'/%3E"
    "%3Ccircle cx='16' cy='19' r='9' fill='none' stroke='%23fef3c7' stroke-width='2'/%3E"
    "%3Ccircle cx='16' cy='19' r='9' fill='%2392400e' opacity='0.4'/%3E"
    "%3Crect x='13' y='7' width='6' height='3' rx='1.5' fill='%23fef3c7'/%3E"
    "%3Cline x1='12' y1='9' x2='10' y2='12' stroke='%23fef3c7' stroke-width='1.8' stroke-linecap='round'/%3E"
    "%3Cline x1='20' y1='9' x2='22' y2='12' stroke='%23fef3c7' stroke-width='1.8' stroke-linecap='round'/%3E"
    "%3Cline x1='16' y1='19' x2='16' y2='12' stroke='%23fef3c7' stroke-width='2' stroke-linecap='round'/%3E"
    "%3Cline x1='16' y1='19' x2='22' y2='16' stroke='%23f0b429' stroke-width='1.5' stroke-linecap='round'/%3E"
    "%3Ccircle cx='16' cy='19' r='1.8' fill='%23fef3c7'/%3E"
    "%3Cline x1='16' y1='11' x2='16' y2='12.5' stroke='%23fef3c7' stroke-width='1.2' stroke-linecap='round' opacity='0.6'/%3E"
    "%3Cline x1='25' y1='19' x2='23.5' y2='19' stroke='%23fef3c7' stroke-width='1.2' stroke-linecap='round' opacity='0.6'/%3E"
    "%3Cline x1='16' y1='27' x2='16' y2='25.5' stroke='%23fef3c7' stroke-width='1.2' stroke-linecap='round' opacity='0.6'/%3E"
    "%3Cline x1='7' y1='19' x2='8.5' y2='19' stroke='%23fef3c7' stroke-width='1.2' stroke-linecap='round' opacity='0.6'/%3E"
    "%3C/svg%3E\">"
)

if '<link rel="icon"' in html:
    html = re.sub(r'<link rel="icon"[^>]+>', FAVICON, html)
    print("  ✓ Favicon replaced")
else:
    html = html.replace('</title>', '</title>\n' + FAVICON)
    print("  ✓ Favicon added")

# ── 5. Stopwatch logo SVG ────────────────────────────────────────────────────
NEW_LOGO = '''<svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" style="flex-shrink:0;">
      <rect width="40" height="40" rx="10" fill="#b45309"/>
      <circle cx="20" cy="25" r="12" fill="none" stroke="#fef3c7" stroke-width="2.2"/>
      <circle cx="20" cy="25" r="12" fill="#92400e" opacity="0.35"/>
      <rect x="16.5" y="9" width="7" height="3" rx="1.5" fill="#fef3c7"/>
      <line x1="14" y1="11" x2="11" y2="14" stroke="#fef3c7" stroke-width="2" stroke-linecap="round"/>
      <line x1="26" y1="11" x2="29" y2="14" stroke="#fef3c7" stroke-width="2" stroke-linecap="round"/>
      <line x1="20" y1="25" x2="20" y2="16" stroke="#fef3c7" stroke-width="2.2" stroke-linecap="round"/>
      <line x1="20" y1="25" x2="28" y2="21" stroke="#f0b429" stroke-width="1.8" stroke-linecap="round"/>
      <circle cx="20" cy="25" r="2.2" fill="#fef3c7"/>
      <line x1="20" y1="14" x2="20" y2="15.8" stroke="#fef3c7" stroke-width="1.5" stroke-linecap="round" opacity="0.55"/>
      <line x1="32" y1="25" x2="30.2" y2="25" stroke="#fef3c7" stroke-width="1.5" stroke-linecap="round" opacity="0.55"/>
      <line x1="20" y1="36" x2="20" y2="34.2" stroke="#fef3c7" stroke-width="1.5" stroke-linecap="round" opacity="0.55"/>
      <line x1="8" y1="25" x2="9.8" y2="25" stroke="#fef3c7" stroke-width="1.5" stroke-linecap="round" opacity="0.55"/>
    </svg>'''

old_svg = re.search(r'<svg width="3\d" height="3\d".*?</svg>', html, re.DOTALL)
if old_svg:
    html = html[:old_svg.start()] + NEW_LOGO + html[old_svg.end():]
    print("  ✓ Logo replaced with stopwatch")
else:
    print("  ⚠ Logo SVG not found — check header manually")

html_path.write_text(html, encoding="utf-8")
print(f"  ✓ Saved {html_path}")

# ─────────────────────────────────────────────────────────────────────────────
print("\n=== STEP 3: Git commit + push ===\n")
# ─────────────────────────────────────────────────────────────────────────────

for cmd in [
    ["git", "add", "."],
    ["git", "commit", "-m", "fix: remove DST nav noise, fix dark mode JS/CSS, stopwatch logo+favicon"],
    ["git", "push"],
]:
    print(f"$ {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode != 0:
        print("⚠ Failed")
        break

print("\n✅ Done — https://pranavathiyani.github.io/grantwatch")
