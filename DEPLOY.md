# Grant Watch ⌛ — Complete Deployment Guide

---

## STEP 1 — Create the GitHub repo

1. Go to https://github.com/new
2. Repository name: `grantwatch`
3. Visibility: **Public** (required for free GitHub Pages)
4. Do NOT initialise with README, .gitignore, or license
5. Click **Create repository**

---

## STEP 2 — Set up locally in WSL

Open WSL terminal. Run these commands one by one:

```bash
# Navigate to where you want the project
cd ~

# Download all the files you got from Claude
# (unzip the downloaded folder, or copy it here)
# Your folder should be named: grantwatch

cd grantwatch

# Create and activate conda environment
conda create -n grantwatch python=3.11 -y
conda activate grantwatch

# Install Python dependencies
pip install -r requirements.txt
```

---

## STEP 3 — One-time setup (sets your username everywhere)

```bash
python setup.py pranavathiyani
```

This replaces `YOUR_USERNAME` with `pranavathiyani` in:
- `generate_feed.py`
- `generate_api.py`
- `update_readme.py`
- `scrapers/par_indiabioscience_scrapers.py`
- `scrapers/icgeb_scraper.py`
- `README.md`

You will see output like:
```
Setting up Grant Watch ⌛ for GitHub user: pranavathiyani
  ✓ generate_feed.py (2 replacements)
  ✓ generate_api.py (3 replacements)
  ...
✅ Done. 6 file(s) updated.
Your portal will be live at:
  https://pranavathiyani.github.io/grantwatch
```

---

## STEP 4 — Move index.html to root

GitHub Pages serves from the root of your repo. The portal lives in `frontend/`
but needs to be at the root level:

```bash
cp frontend/index.html ./index.html
```

Your folder should now have `index.html` at the top level alongside `run_scrapers.py`.

---

## STEP 5 — Run scrapers locally to populate data

This fills `data/grants.json` with real data before you push:

```bash
python run_scrapers.py
```

You will see each scraper run. Some `.gov.in` sites may fail (they block
datacenter IPs) — that is fine. The seed data already has 13+ entries.
After this run you should have 50–100 grants in `data/grants.json`.

Then generate the feed and API:

```bash
python generate_feed.py
python generate_api.py
python update_readme.py
```

---

## STEP 6 — Preview locally (optional but recommended)

```bash
# From the repo root (not inside frontend/)
python -m http.server 8080
```

Open http://localhost:8080 in your browser.
You should see the portal with grant cards loaded.
Check that filters work, urgency banner shows if any deadlines are close.

Press Ctrl+C to stop the server when done.

---

## STEP 7 — Push to GitHub

```bash
git init
git add .
git commit -m "init: Grant Watch ⌛ — SASTRA Research Funding Portal"
git branch -M main
git remote add origin https://github.com/pranavathiyani/grantwatch.git
git push -u origin main
```

GitHub will ask for your credentials if this is your first push.
Use your GitHub username and a Personal Access Token (not your password).

**To create a Personal Access Token:**
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token → select `repo` scope → copy the token
3. Use it as the password when git asks

---

## STEP 8 — Enable GitHub Pages

1. Go to https://github.com/pranavathiyani/grantwatch
2. Click **Settings** tab
3. Left sidebar → **Pages**
4. Under "Build and deployment":
   - Source: **Deploy from a branch**
   - Branch: **main**
   - Folder: **/ (root)**
5. Click **Save**

Wait 60–90 seconds. Refresh the Settings → Pages page.
You will see: *"Your site is live at https://pranavathiyani.github.io/grantwatch"*

---

## STEP 9 — Verify GitHub Actions

1. Go to your repo → **Actions** tab
2. You will see two workflows listed:
   - `Grant Watch ⌛ Bi-Weekly Refresh`
   - `Grant Watch ⌛ Daily Deadline Check`
3. They will run automatically on schedule
4. To test immediately: click a workflow → **Run workflow** button → **Run workflow**

Watch the run live. If everything is green, automation is working.

---

## STEP 10 — Done ✅

Your portal is live at:
**https://pranavathiyani.github.io/grantwatch**

RSS feed:
**https://pranavathiyani.github.io/grantwatch/data/feed.xml**

Community grant submission:
**https://github.com/pranavathiyani/grantwatch/issues/new/choose**

---

## What happens after this — automatically

| When | What GitHub does |
|------|-----------------|
| Every day at 12:00 IST | Reads grants.json, updates urgent.json + feed.xml. ~10 seconds. |
| 1st of month at 11:30 IST | Runs all 49 scrapers, updates grants.json. ~5 minutes. |
| 15th of month at 11:30 IST | Same as above. |
| Any time you push a change | GitHub Pages redeploys index.html instantly. |

You do nothing. The bot handles it.

---

## Files explained — what each one does

```
index.html          The portal itself. Static HTML+JS. Fetches data/grants.json
                    on load. Never needs to change unless you want UI updates.

run_scrapers.py     The main scraper runner. Calls all 49 scrapers, merges
                    results, writes data/grants.json + data/meta.json.

daily_check.py      Reads grants.json, computes deadline urgency, writes
                    data/urgent.json. No network requests.

generate_feed.py    Reads grants.json, writes data/feed.xml (Atom RSS).

generate_api.py     Reads grants.json, splits into category files under
                    data/by-type/ and data/by-country/. Also writes
                    data/grants-schema.json (JSON Schema).

update_readme.py    Reads grants.json + meta.json, rewrites README.md with
                    live stats. Also archives previous grants.json snapshot.

setup.py            One-time script. Replaces YOUR_USERNAME with your
                    real GitHub username across all files.

scrapers/           One Python file per agency or category. Each inherits
                    from base_scraper.py and implements scrape() → list.

data/grants.json    The master dataset. Everything the portal displays.
data/urgent.json    Grants closing ≤30 days. Updated daily.
data/feed.xml       Atom RSS feed. Subscribe in Feedly, Thunderbird, etc.
data/grants-schema.json  JSON Schema for the grant record format.

.github/workflows/  YAML files that tell GitHub Actions when and what to run.
                    monthly_refresh.yml = bi-weekly scrape
                    daily_check.yml     = daily lightweight check

.github/ISSUE_TEMPLATE/submit_grant.yml
                    Structured form on GitHub for anyone to submit a missing
                    grant. You review and add to grants.json manually.

requirements.txt    Python packages needed: requests, beautifulsoup4, lxml.
.gitignore          Keeps __pycache__ and temp files out of git.
```

---

## Troubleshooting

**Portal loads but shows no grants**
→ Check that `data/grants.json` exists and is valid JSON.
→ Run `python run_scrapers.py` locally and push again.

**Actions workflow fails**
→ Go to Actions tab → click the failed run → read the error log.
→ Most common: a `.gov.in` site blocked the request. This is fine — the
  scrapers catch errors silently and other agencies still run.

**Pages not updating**
→ Check that your `main` branch has the latest commit.
→ Settings → Pages → check it shows "Your site is live".
→ Hard refresh in browser: Ctrl+Shift+R.

**Git asks for password**
→ Use a Personal Access Token (see Step 7). GitHub removed password auth in 2021.

---

*Grant Watch ⌛ · Developed for SASTRA University by Pranavathiyani G ☮️ · Co-developed with Claude 💜*
