# Grant Watch ⌛
**SASTRA Deemed University — Research Funding Portal**

> One-stop aggregator for Indian and international research funding calls.
> Auto-refreshed bi-weekly. Data is public. No login required.

🔗 **[Open Portal →](https://pranavathiyani.github.io/grantwatch)**
📡 **[Subscribe RSS →](https://pranavathiyani.github.io/grantwatch/data/feed.xml)**

---

## Live Stats · Last updated 2026-04-01

| Metric | Count |
|--------|-------|
| 📋 Total grants indexed | **188** |
| ✅ Open calls | **177** |
| 🇮🇳 Indian agency grants | **0** |
| 🌍 International grants | **2** |
| 🎓 Fellowships | **61** |
| ✈️ Travel grants | **22** |
| 🤝 Bilateral collaborations | **24** |

---

## ⚠ Closing within 30 days

| Urgency | Grant | Agency | Deadline |
|---------|-------|--------|----------|
| 🟡 **27d** | ICGEB CRP Research Grant 2026 | ICGEB | 2026-04-30 |
| 🟡 **27d** | ICGEB Early Career Return Grant (CRP) | ICGEB | 2026-04-30 |

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

## Agencies Covered (35)

- AICTE
- ANRF
- Alexander von Humboldt Foundation
- BIRAC
- CSIR
- DAAD
- DBT
- DST
- DST (Bilateral)
- EMBL
- EMBO
- FEBS
- Fulbright-Nehru
- Gates Foundation
- Google Research
- HFSP
- ICAR
- ICGEB
- ICMR
- IMPRINT (MoE)
- INSA
- IUSSTF
- MeitY
- NIH
- NIH Fogarty
- Novo Nordisk Foundation
- PAR Foundation
- PMRF (MoE)
- Royal Society
- SPARC (MoE)
- UGC
- Various
- Various (Startup)
- Various (Travel)
- Wellcome DBT India Alliance

---

*Developed for **SASTRA University** by **Pranavathiyani G** ☮️ · Co-developed with **Claude** 💜*
*Data is publicly sourced. Grant Watch aggregates for non-commercial academic use.*
