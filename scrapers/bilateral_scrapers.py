"""
Grant Watch ⌛ — Bilateral / International Collaborative Grants
Requires INDIAN PI + foreign co-PI. Indian-side funding confirmed.

Covered:
  CEFIPRA     — Indo-French (General + ICT tracks)
  IGSTC       — Indo-German (2+2, WISER, SING)
  DST-JSPS    — Indo-Japan Cooperative Science Programme
  ISJRP       — Indo-Swiss (ICMR+DBT+SNSF) ← deadline May 5 2026
  DST-DFG     — Indo-German (via ANRF/DST, science & engineering)
  UKRI/Newton — Indo-UK Newton-Bhabha Fund
  DST-NSF     — Indo-US (via IUSSTF / direct DST)
  DST-ISRAEL  — Indo-Israel (DST-MOST)
  DST-KOREA   — Indo-Korea (DST-NRF)
  DST-AUSTRALIA — Indo-Australia (DST-CSIRO, DST-ARC)
"""

from .base_scraper import BaseScraper


class BilateralGrantsScraper(BaseScraper):
    """
    Bilateral grants require matching proposals from both countries.
    Indian PI receives funding from Indian agency; foreign PI from their agency.
    All seeded — no reliable machine-parseable source for these.
    Monthly manual check recommended for deadline updates.
    """
    AGENCY_NAME    = "DST (Bilateral)"
    AGENCY_COUNTRY = "India"
    AGENCY_URL     = "https://dst.gov.in/international-cooperation"

    def scrape(self) -> list:
        return [

            # ── INDO-FRENCH ──────────────────────────────────────────────
            self.build_grant(
                title       = "CEFIPRA Indo-French Joint Research Project (General)",
                url         = "https://cefipra.org/programmes/joint-research-projects/",
                deadline    = None,
                description = (
                    "CEFIPRA/IFCPAR bilateral programme. Indian PI funded by DST; French PI by ANR. "
                    "Covers joint research, researcher exchanges, workshops. All STEM disciplines. "
                    "Proposals submitted in parallel to CEFIPRA (India) and ANR (France)."
                ),
                grant_type  = "Collaborative Grant",
                eligibility = ["Faculty (Indian PI)", "French Co-PI required"],
                disciplines = ["Science", "Engineering", "Technology", "Any STEM"],
                amount      = "₹40–60 Lakhs (Indian side, 3 years)",
            ),
            self.build_grant(
                title       = "CEFIPRA Indo-French ICT Research Programme",
                url         = "https://cefipra.org/programmes/ict/",
                deadline    = None,   # was Oct 2025; next call expected 2026
                description = (
                    "ICT-focused bilateral call. Indian PI submits via CEFIPRA online + hard copy to "
                    "CEFIPRA New Delhi; French PI submits to Inria separately. Focus: AI, networks, "
                    "security, systems."
                ),
                grant_type  = "Collaborative Grant",
                eligibility = ["Faculty (Indian PI)", "French Co-PI (Inria-affiliated)"],
                disciplines = ["AI/ML", "ICT", "Computer Science", "Networks", "Cybersecurity"],
                amount      = "₹40 Lakhs (Indian side) + French equivalent",
            ),

            # ── INDO-GERMAN ───────────────────────────────────────────────
            self.build_grant(
                title       = "IGSTC 2+2 Research Projects (Indo-German)",
                url         = "https://www.igstc.org/programme/2-2-projects",
                deadline    = None,
                description = (
                    "Indo-German Science & Technology Centre flagship programme. "
                    "2 Indian + 2 German partners (academia + industry on each side). "
                    "Applied research, technology transfer focus."
                ),
                grant_type  = "Collaborative Grant",
                eligibility = ["Faculty + Indian Industry Partner", "German Co-PI + German Industry"],
                disciplines = ["Engineering", "Technology", "Life Sciences", "Clean Energy", "IT"],
                amount      = "₹1.5 Crores (Indian side, 3 years)",
            ),
            self.build_grant(
                title       = "IGSTC WISER — Women in Science & Engineering Research (Indo-German)",
                url         = "https://www.igstc.org/programme/wiser",
                deadline    = "2026-03-31",
                description = (
                    "Promotes collaboration between women researchers in India and Germany. "
                    "Paired mode only — one Indian woman PI + one German woman PI required. "
                    "Covers research staff, consumables, travel, and capacity building."
                ),
                grant_type  = "Collaborative Grant",
                eligibility = ["Women Faculty/Researcher (Indian PI)", "German Woman Co-PI required",
                               "Min 5 years research experience"],
                disciplines = ["STEM — any", "Life Sciences", "Engineering", "Technology"],
                amount      = "₹39 Lakhs (Indian side) + €48,000 (German side) — 3 years",
            ),
            self.build_grant(
                title       = "IGSTC SING — Seed Networking Grant (Indo-German)",
                url         = "https://www.igstc.org/programme/sing",
                deadline    = None,
                description = (
                    "Seed funding for initiating bilateral India-Germany research connections. "
                    "Rolling call. Covers preliminary experiments, consumables, short visits, "
                    "conference registration. Low-barrier entry point for Indo-German collaboration."
                ),
                grant_type  = "Seed / Networking Grant",
                eligibility = ["Faculty", "Researcher", "Indian Institution"],
                disciplines = ["Any STEM"],
                amount      = "Small seed grant (INR equivalent)",
            ),
            self.build_grant(
                title       = "DST-DFG Indo-German Joint Research (Science & Engineering)",
                url         = "https://dst.gov.in/international-cooperation/bilateral/germany",
                deadline    = None,
                description = (
                    "Joint research projects between Indian (DST/ANRF-funded) and German "
                    "(DFG-funded) PIs. Proposals submitted in parallel — Indian PI to DST, "
                    "German PI to DFG via elan system. Both agencies must recommend funding."
                ),
                grant_type  = "Collaborative Grant",
                eligibility = ["Faculty (Indian PI)", "German Co-PI (DFG-eligible)"],
                disciplines = ["Science", "Engineering", "Technology"],
                amount      = "Varies (DST norms for Indian side)",
            ),

            # ── INDO-JAPAN ────────────────────────────────────────────────
            self.build_grant(
                title       = "DST-JSPS India-Japan Cooperative Science Programme (IJCSP)",
                url         = "https://dst.gov.in/international-cooperation/bilateral/japan",
                deadline    = None,   # annual call, typically Jun-Aug
                description = (
                    "Joint research projects and workshops/seminars between Indian (DST) and "
                    "Japanese (JSPS) researchers. Parallel submission required. Focus on "
                    "mobility — exchange visits, seminars. Results notified Apr/May following year."
                ),
                grant_type  = "Collaborative Grant",
                eligibility = ["Faculty (Indian PI)", "Japanese Co-PI (JSPS-eligible)"],
                disciplines = ["Physical Sciences", "Chemical Sciences", "Life Sciences",
                               "Mathematics & Computational Science", "Materials & Engineering"],
                amount      = "Mobility grant — travel, per diem, workshop costs",
            ),

            # ── INDO-SWISS ────────────────────────────────────────────────
            self.build_grant(
                title       = "Indo-Swiss Joint Research Programme (ISJRP) — ICMR/DBT/SNSF",
                url         = "https://www.icmr.gov.in/international-fellowships",
                deadline    = "2026-05-05",
                description = (
                    "Joint call by ICMR + DBT (India) and Swiss National Science Foundation (SNSF). "
                    "Indian PI funded by ICMR/DBT; Swiss PI funded by SNSF. Focus: biomedical, "
                    "health, and life sciences research. Live deadline: May 5, 2026."
                ),
                grant_type  = "Collaborative Grant",
                eligibility = ["Faculty/Researcher (Indian PI)", "Swiss Co-PI (SNSF-eligible)"],
                disciplines = ["Biomedical Research", "Public Health", "Life Sciences", "Biotechnology"],
                amount      = "Varies per ICMR/DBT norms",
            ),

            # ── INDO-UK ───────────────────────────────────────────────────
            self.build_grant(
                title       = "Newton-Bhabha Fund — Indo-UK Joint Research",
                url         = "https://www.britishcouncil.in/programmes/higher-education/newton-bhabha",
                deadline    = None,
                description = (
                    "UK-India bilateral fund managed by British Council and UKRI. Supports joint "
                    "research, PhD placements, researcher exchanges, and workshops. "
                    "Indian PI funded by DST/DBT/other Indian agency; UK PI by UKRI."
                ),
                grant_type  = "Collaborative Grant",
                eligibility = ["Faculty (Indian PI)", "UK Co-PI required"],
                disciplines = ["Science", "Engineering", "Health", "Sustainable Development"],
                amount      = "Varies by call stream",
            ),
            self.build_grant(
                title       = "UKRI-DST India Joint Initiative (via GCRF/IUK)",
                url         = "https://www.ukri.org/opportunity/?filter_opportunity_location=india",
                deadline    = None,
                description = (
                    "Various UKRI calls explicitly open to India-UK partnerships. "
                    "Indian partner typically funded by DST/DBT; UK partner by UKRI. "
                    "Check UKRI opportunity finder filtered by 'India' for current calls."
                ),
                grant_type  = "Collaborative Grant",
                eligibility = ["Faculty (Indian PI)", "UK Co-PI required"],
                disciplines = ["Any — check specific call"],
                amount      = "Varies by call",
            ),

            # ── INDO-US ───────────────────────────────────────────────────
            self.build_grant(
                title       = "IUSSTF Joint Research Projects (Indo-US)",
                url         = "https://www.iusstf.org/program/joint-research-projects",
                deadline    = None,
                description = (
                    "Indo-US Science & Technology Forum. Indian PI funded by DST; "
                    "US PI funded by NSF/NIH/DOE depending on theme. "
                    "Also includes Virtual Network Centres and Joint Workshops."
                ),
                grant_type  = "Collaborative Grant",
                eligibility = ["Faculty (Indian PI)", "US Co-PI required"],
                disciplines = ["Science", "Technology", "Engineering", "Any STEM"],
                amount      = "USD 60,000 (US side) + INR equivalent",
            ),
            self.build_grant(
                title       = "MeitY-NSF Joint Research Programme",
                url         = "https://www.meity.gov.in/content/announcement-1st-joint-call-porposal-under--research-colaboration",
                deadline    = None,
                description = (
                    "India-US bilateral for semiconductors, next-gen communications, cybersecurity, "
                    "green tech, intelligent transport. Indian PI applies to MeitY; US PI to NSF. "
                    "Single joint proposal, reviewed by NSF as coordinating agency."
                ),
                grant_type  = "Collaborative Grant",
                eligibility = ["Faculty (Indian PI)", "US Co-PI (NSF-eligible)"],
                disciplines = ["Semiconductors", "AI/ML", "Cybersecurity", "Green Tech", "IT"],
                amount      = "INR (MeitY norms) + USD (NSF norms)",
            ),

            # ── INDO-ISRAEL ───────────────────────────────────────────────
            self.build_grant(
                title       = "DST-MOST Indo-Israel Joint Research (S&T)",
                url         = "https://dst.gov.in/international-cooperation/bilateral/israel",
                deadline    = None,
                description = (
                    "Bilateral programme between DST (India) and Ministry of Science & Technology "
                    "(Israel). Joint research in all S&T areas. Proposals submitted in parallel. "
                    "Annual calls typically open Oct-Dec."
                ),
                grant_type  = "Collaborative Grant",
                eligibility = ["Faculty (Indian PI)", "Israeli Co-PI required"],
                disciplines = ["Science", "Technology", "Agriculture", "Water", "Health"],
                amount      = "Varies (DST norms)",
            ),

            # ── INDO-KOREA ────────────────────────────────────────────────
            self.build_grant(
                title       = "DST-NRF Indo-Korea Joint Research Programme",
                url         = "https://dst.gov.in/international-cooperation/bilateral/south-korea",
                deadline    = None,
                description = (
                    "Joint research between Indian (DST) and Korean (NRF) researchers. "
                    "Covers joint R&D projects and bilateral visits. Annual call."
                ),
                grant_type  = "Collaborative Grant",
                eligibility = ["Faculty (Indian PI)", "Korean Co-PI required"],
                disciplines = ["Science", "Engineering", "IT", "Materials", "Biotech"],
                amount      = "Varies (DST norms)",
            ),

            # ── INDO-AUSTRALIA ────────────────────────────────────────────
            self.build_grant(
                title       = "DST-CSIRO India-Australia Strategic Research Fund",
                url         = "https://dst.gov.in/international-cooperation/bilateral/australia",
                deadline    = None,
                description = (
                    "Joint bilateral fund between DST and CSIRO (Australia). Focus on areas of "
                    "mutual interest: agriculture, water, clean energy, health. "
                    "Indian PI funded by DST, Australian by CSIRO."
                ),
                grant_type  = "Collaborative Grant",
                eligibility = ["Faculty (Indian PI)", "Australian Co-PI required"],
                disciplines = ["Agriculture", "Water", "Clean Energy", "Health", "Environment"],
                amount      = "Varies (DST norms)",
            ),
        ]
