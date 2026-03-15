"""
Grant Watch ⌛ — ICGEB Scraper
International Centre for Genetic Engineering and Biotechnology
India is a founding member state. New Delhi component lab exists.

Programs:
  CRP Research Grants     — deadline 30 April 2026 (yearly)
  Early Career Return     — part of CRP, for young PIs
  SMART Fellowships       — deadline 31 March 2026 (mobility)
  Short-term PhD          — deadline 31 March 2026
  Biosecurity Fellowships — deadline 31 March 2026 (AMR-relevant)
  ICGEB-JNU PhD           — India-specific, annual
"""

import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from .base_scraper import BaseScraper

GRANT_WATCH_UA = (
    "GrantWatchBot/1.0 (SASTRA University research funding aggregator; "
    "non-commercial academic use; https://github.com/pranavathiyani/grantwatch)"
)


def _robots_allows(base_url, path):
    try:
        rp = RobotFileParser()
        rp.set_url(f"{base_url}/robots.txt")
        rp.read()
        return rp.can_fetch(GRANT_WATCH_UA, f"{base_url}{path}")
    except Exception:
        return True


class ICGEBScraper(BaseScraper):
    """
    ICGEB is an intergovernmental organisation — its grant listings are public
    information intended for researchers worldwide. India is a member state.
    We check robots.txt, use identified UA, 3s delay, read-only.
    """
    AGENCY_NAME    = "ICGEB"
    AGENCY_COUNTRY = "International"
    AGENCY_URL     = "https://www.icgeb.org/grants/"
    BASE           = "https://www.icgeb.org"

    def scrape(self) -> list:
        # Seed with well-verified programs + live deadlines from icgeb.org
        # Live scrape attempted below to catch any new calls
        grants = [
            # ── Research Grants ────────────────────────────────────────
            self.build_grant(
                title       = "ICGEB CRP Research Grant 2026",
                url         = "https://www.icgeb.org/grants/icgeb-research-grants-2023crp-collaborative-research-programme/",
                deadline    = "2026-04-30",
                description = (
                    "ICGEB Collaborative Research Programme (CRP). Supports original research "
                    "in basic science, human healthcare, industrial/agricultural biotechnology "
                    "and bioenergy. India is a member state — up to 3 CRP + 2 Early Career "
                    "Return grants per call. International collaboration mandatory."
                ),
                grant_type  = "Research Grant",
                eligibility = ["Faculty", "Researcher at ICGEB Member State institution"],
                disciplines = ["Biotechnology", "Life Sciences", "Biomedical",
                               "Agricultural Biotech", "Bioenergy", "AMR"],
                amount      = "Varies (project-based, USD)",
            ),
            self.build_grant(
                title       = "ICGEB Early Career Return Grant (CRP)",
                url         = "https://www.icgeb.org/grants/",
                deadline    = "2026-04-30",
                description = (
                    "Part of ICGEB CRP call. For young PIs returning to ICGEB Member States "
                    "after postdoctoral training abroad. Supports setting up independent labs. "
                    "Up to 2 awards per member country per call."
                ),
                grant_type  = "Research Grant",
                eligibility = ["Early Career PI (returning)", "ICGEB Member State"],
                disciplines = ["Life Sciences", "Biotechnology", "Biomedical"],
                amount      = "Competitive (USD)",
            ),
            # ── Fellowships ────────────────────────────────────────────
            self.build_grant(
                title       = "ICGEB Arturo Falaschi SMART Fellowship (Mar 2026)",
                url         = "https://www.icgeb.org/fellowships/smart-fellowships-2/",
                deadline    = "2026-03-31",
                description = (
                    "Scientific Mobility for Advanced Research Training. 3–9 months at any "
                    "ICGEB Member State lab (not home country). Open to PhD students and "
                    "postdocs (PhD ≤5 years). Stipend USD 800–2,000/month + bench fee + travel."
                ),
                grant_type  = "Travel Grant",
                eligibility = ["PhD Student", "Postdoc (PhD ≤5 years)", "Indian Researcher"],
                disciplines = ["Life Sciences", "Biotechnology", "Genetic Engineering"],
                amount      = "USD 800–2,000/month + travel + bench fee",
            ),
            self.build_grant(
                title       = "ICGEB Short-term PhD Fellowship (Mar 2026)",
                url         = "https://www.icgeb.org/fellowships/short-term-phd-fellowships/",
                deadline    = "2026-03-31",
                description = (
                    "1–12 months at ICGEB labs in Trieste (Italy), New Delhi (India), or "
                    "Cape Town (SA). For collaborative predoctoral research. Indian applicants "
                    "may apply to Trieste or Cape Town (not New Delhi — home country rule). "
                    "Monthly stipend + travel + health insurance."
                ),
                grant_type  = "Fellowship",
                eligibility = ["PhD Student (Indian)", "MSc holder", "ICGEB Member State national"],
                disciplines = ["Life Sciences", "Biotechnology", "Genetic Engineering"],
                amount      = "€1,500/month (Trieste) or ZAR 16,500/month (Cape Town) + travel",
            ),
            self.build_grant(
                title       = "ICGEB Biosecurity Fellowship — Biological Threat Training (Mar 2026)",
                url         = "https://www.icgeb.org/fellowships/icgeb-fellowships-for-scientists-in-biosecurity-march-2026/",
                deadline    = "2026-03-31",
                description = (
                    "2–6 months at ICGEB labs (Trieste, New Delhi, Cape Town). Focus: "
                    "molecular detection of biological threats, epidemiology, genomic "
                    "surveillance, drug discovery, vaccine development, diagnostics. "
                    "Co-funded by Norwegian Agency (UNODA/BWCISU). Directly relevant to AMR."
                ),
                grant_type  = "Fellowship",
                eligibility = ["Early-career Scientist", "OECD/DAC country national"],
                disciplines = ["AMR", "Infectious Disease", "Biosecurity",
                               "Genomic Surveillance", "Drug Discovery"],
                amount      = "USD 1,122/month (New Delhi) + travel + insurance",
            ),
            self.build_grant(
                title       = "ICGEB Arturo Falaschi Postdoctoral Fellowship",
                url         = "https://www.icgeb.org/fellowships/arturo-falaschi-postdoctoral-fellowships/",
                deadline    = None,   # biannual; next call ~Sep 2026
                description = (
                    "Postdoctoral training at ICGEB labs in Trieste, New Delhi, or Cape Town. "
                    "Average 2 years. Competitive package: stipend + health insurance + research costs. "
                    "Top fellows eligible for Early Career Return Grants after completion."
                ),
                grant_type  = "Fellowship",
                eligibility = ["PhD Holder", "International Applicant"],
                disciplines = ["Life Sciences", "Biotechnology", "Genetic Engineering"],
                amount      = "Competitive stipend + full benefits",
            ),
            self.build_grant(
                title       = "ICGEB-JNU PhD Fellowship (India-specific)",
                url         = "https://www.icgeb.org/fellowships/icgeb-jnu-phd-fellowships/",
                deadline    = None,   # annual, typically ~June each year
                description = (
                    "PhD positions at ICGEB New Delhi in collaboration with JNU. "
                    "Requires valid CSIR/UGC/ICMR/DBT/DST-INSPIRE/BINC JRF. Annual intake. "
                    "Full stipend + world-class research environment."
                ),
                grant_type  = "Fellowship",
                eligibility = ["Indian National", "Category-I NET/JRF holder", "MSc Graduate"],
                disciplines = ["Life Sciences", "Biotechnology", "Genetic Engineering",
                               "Computational Biology"],
                amount      = "Full PhD stipend (ICGEB norms)",
            ),
        ]

        # Live scrape for any new calls on icgeb.org/grants
        try:
            if _robots_allows(self.BASE, "/grants/"):
                time.sleep(3)
                resp = requests.get(
                    f"{self.BASE}/grants/",
                    headers={"User-Agent": GRANT_WATCH_UA},
                    timeout=20,
                )
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    for link in soup.find_all("a", href=True):
                        href  = link["href"]
                        title = link.get_text(strip=True)
                        if "/grants/" not in href or len(title) < 10:
                            continue
                        if not href.startswith("http"):
                            href = self.BASE + href
                        # Avoid duplicating seeded entries
                        if any(g["url"] == href for g in grants):
                            continue
                        grants.append(self.build_grant(
                            title       = title,
                            url         = href,
                            deadline    = None,
                            description = f"ICGEB grant opportunity: {title}",
                            grant_type  = "Research Grant",
                            eligibility = ["Researcher", "ICGEB Member State"],
                            disciplines = ["Life Sciences", "Biotechnology"],
                            amount      = "Varies",
                        ))
        except Exception as e:
            print(f"  [ICGEB live] {e}")

        return grants
