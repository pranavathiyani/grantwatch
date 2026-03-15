# Contributing to Grant Watch ⌛

Grant Watch is a curated research funding portal for SASTRA University — and the wider Indian research community. Contributions are welcome from anyone.

---

## Ways to contribute

### 1. Submit a missing grant
Found a funding opportunity that should be here? Use the **[Submit a Grant](../../issues/new?template=submit_grant.yml)** issue template. Include:
- Agency name and scheme name
- Official URL
- Deadline (if known)
- Who can apply

We review and add verified entries within 2 weeks.

### 2. Report a bug
Wrong deadline, broken link, or closed grant still showing? Use the **[Bug Report](../../issues/new?template=bug_report.yml)** template.

### 3. Suggest an enhancement
New feature, filter, alert system, or UI improvement? Use the **[Enhancement](../../issues/new?template=enhancement.yml)** template.

### 4. Fix a scraper (code contribution)
If you're comfortable with Python and want to fix a broken scraper or add a new agency:

```bash
# Fork the repo, clone your fork
git clone https://github.com/YOUR_USERNAME/grantwatch.git
cd grantwatch

# Create a branch
git checkout -b fix/agency-name-scraper

# Install dependencies
pip install -r requirements.txt

# Test your scraper
python run_scrapers.py --agency "Agency Name"

# Commit and open a PR
git commit -m "fix: AgencyName scraper — description of fix"
git push origin fix/agency-name-scraper
```

**Scraper guidelines:**
- Prefer curated `build_grant()` calls over live HTML scraping — Indian govt sites are structurally noisy
- Every entry needs a real description (>80 chars), not just a title
- Deadlines should be `YYYY-MM-DD` format or `None` for rolling
- Always include `eligibility` and `disciplines` arrays

---

## Planned enhancements (good first issues)

These are confirmed useful features not yet built. Pick one up if you'd like to contribute:

| # | Feature | Difficulty |
|---|---------|-----------|
| 1 | Add Swarnajayanti Fellowship (DST) | Easy — add to dst scraper |
| 2 | Eligibility filter (Faculty / Student / Postdoc / Startup) | Medium — JS filter |
| 3 | SASTRA-eligible badge on relevant grant cards | Medium — data + CSS |
| 4 | CSIR schemes — expand from 5 to 10 curated entries | Easy — scraper |
| 5 | Groq "Match me" assistant — input research area, get top grants | Hard — LLM integration |
| 6 | WhatsApp/Telegram weekly digest bot | Hard — bot + GitHub Actions |
| 7 | Email alert subscription via RSS | Easy — UI only |
| 8 | SERB surviving schemes audit post-ANRF transition | Research task |

Label any issue you open with `good first issue` if it's beginner-friendly.

---

## Data format

Each grant in `data/grants.json` follows this schema:

```json
{
  "id": "agency-scheme-year",
  "title": "Full scheme name",
  "agency": "Agency Name",
  "agency_country": "India | International",
  "url": "https://official-url.gov.in",
  "deadline": "2026-06-30",
  "open_date": "2026-04-01",
  "status": "open | closed | rolling",
  "description": "Clear description of what the grant is for (>80 chars)",
  "grant_type": "Research Grant | Fellowship | Travel Grant | ...",
  "eligibility": ["Faculty", "PhD Student", "Indian Institution"],
  "disciplines": ["Biotechnology", "Life Sciences"],
  "amount": "₹30 Lakhs (3 years)"
}
```

---

## Code of conduct

- Be accurate — don't submit grants you haven't verified
- Be specific — vague entries help nobody
- Be respectful — this is a community resource

---

*Grant Watch ⌛ · Developed for SASTRA University by Pranavathiyani G ☮️ · Co-developed with Claude 💜*
