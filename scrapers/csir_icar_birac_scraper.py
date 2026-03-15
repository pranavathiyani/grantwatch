"""
Grant Watch ⌛ — CSIR, ICAR, BIRAC Scrapers (Fixed)
ICAR: SSL cert is invalid on their end — use verify=False with warning suppression
CSIR/DBT/ICMR: Updated selectors and fallback URL list
"""

import re
import warnings
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .base_scraper import BaseScraper


def _parse_date(text: str):
    for fmt in ("%d-%m-%Y", "%d/%m/%Y", "%B %d, %Y", "%d %B %Y",
                "%Y-%m-%d", "%d.%m.%Y", "%b %d, %Y"):
        try:
            return datetime.strptime(text.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


GRANT_KEYWORDS = ["call", "proposal", "grant", "fellowship", "scheme",
                  "programme", "fund", "award", "project", "opportunity",
                  "application", "research", "innovation"]


class CSIRScraper(BaseScraper):
    AGENCY_NAME    = "CSIR"
    AGENCY_COUNTRY = "India"
    AGENCY_URL     = "https://www.csir.res.in/announcements"

    def scrape(self) -> list:
        grants = []
        urls = [
            "https://www.csir.res.in/announcements",
            "https://www.csir.res.in/funding-opportunities",
            "https://www.csir.res.in/calls-for-proposals",
        ]
        for url in urls:
            try:
                resp = requests.get(url, timeout=20,
                                    headers={"User-Agent": "Mozilla/5.0"})
                if resp.status_code != 200:
                    continue
                soup = BeautifulSoup(resp.text, "html.parser")
                for link in soup.find_all("a", href=True):
                    title = link.get_text(strip=True)
                    if len(title) < 10:
                        continue
                    if not any(k in title.lower() for k in GRANT_KEYWORDS):
                        continue
                    href = link["href"]
                    if not href.startswith("http"):
                        href = "https://www.csir.res.in" + href
                    parent_text = link.parent.get_text(" ", strip=True) if link.parent else ""
                    date_hit = re.search(r"\b(\d{1,2}[-/.]\d{1,2}[-/.]\d{4})\b", parent_text)
                    deadline = _parse_date(date_hit.group(1)) if date_hit else None
                    grants.append(self.build_grant(
                        title=title, url=href, deadline=deadline,
                        description=parent_text[:300], grant_type="Research Grant",
                        eligibility=["Faculty", "Researcher", "Indian Institution"],
                        disciplines=["Science", "Engineering"], amount="Varies",
                    ))
                if grants:
                    break
            except Exception as e:
                print(f"  [CSIR:{url}] {e}")
        return grants


class ICARScraper(BaseScraper):
    AGENCY_NAME    = "ICAR"
    AGENCY_COUNTRY = "India"
    AGENCY_URL     = "https://icar.gov.in/content/calls-proposals"

    def scrape(self) -> list:
        grants = []
        urls = [
            "https://icar.gov.in/content/calls-proposals",
            "https://icar.gov.in/funding",
            "https://icar.gov.in/",
        ]
        for url in urls:
            try:
                # ICAR has an invalid SSL certificate — suppress warning, use verify=False
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    resp = requests.get(url, timeout=20, verify=False,
                                        headers={"User-Agent": "Mozilla/5.0"})
                if resp.status_code != 200:
                    continue
                soup = BeautifulSoup(resp.text, "html.parser")
                for link in soup.find_all("a", href=True):
                    title = link.get_text(strip=True)
                    if len(title) < 10:
                        continue
                    if not any(k in title.lower() for k in GRANT_KEYWORDS):
                        continue
                    href = link["href"]
                    if not href.startswith("http"):
                        href = "https://icar.gov.in" + href
                    parent_text = link.parent.get_text(" ", strip=True) if link.parent else ""
                    date_hit = re.search(r"\b(\d{1,2}[-/.]\d{1,2}[-/.]\d{4})\b", parent_text)
                    deadline = _parse_date(date_hit.group(1)) if date_hit else None
                    grants.append(self.build_grant(
                        title=title, url=href, deadline=deadline,
                        description=parent_text[:300], grant_type="Research Grant",
                        eligibility=["Faculty", "Researcher", "Indian Institution"],
                        disciplines=["Agriculture", "Animal Science", "Food Science"],
                        amount="Varies",
                    ))
                if grants:
                    break
            except Exception as e:
                print(f"  [ICAR:{url}] {e}")
        return grants



class BIRACScraper(BaseScraper):
    """
    Curated — BIRAC website mixes navigation/news with current calls,
    producing 278 noisy entries when scraped blindly.
    These 10 entries cover all major standing BIRAC schemes.
    BIG opens Jan 1 and Jul 1 every year (confirmed pattern).
    """
    AGENCY_NAME    = "BIRAC"
    AGENCY_COUNTRY = "India"
    AGENCY_URL     = "https://birac.nic.in/cfp.php"

    def scrape(self):
        return [
            self.build_grant(
                title       = "BIRAC Biotechnology Ignition Grant (BIG)",
                url         = "https://birac.nic.in/big.php",
                deadline    = "2026-07-01",
                open_date   = "2026-07-01",
                description = "Flagship early-stage biotech funding. Up to ₹50L for proof-of-concept. Opens TWICE yearly: Jan 1 and Jul 1. Largest early-stage biotech funding programme in India.",
                grant_type  = "Startup Grant",
                eligibility = ["Startup", "Individual Innovator", "Faculty Entrepreneur"],
                disciplines = ["Biotechnology", "MedTech", "AgriTech", "Biopharma"],
                amount      = "Up to ₹50 Lakhs (18 months)",
            ),
            self.build_grant(
                title       = "BIRAC BioNEST (Biotech Incubator Support)",
                url         = "https://birac.nic.in/bionest.php",
                deadline    = None,
                description = "Supports establishment of biotech incubators at academic institutions. Covers infrastructure and startup support. Academic institutions can apply.",
                grant_type  = "Infrastructure Grant",
                eligibility = ["University", "Academic Institution", "R&D Organization"],
                disciplines = ["Biotechnology", "Biopharma", "MedTech"],
                amount      = "Up to ₹10 Crores (phased)",
            ),
            self.build_grant(
                title       = "BIRAC SPARSH (Social Innovation Grant)",
                url         = "https://birac.nic.in/sparsh.php",
                deadline    = None,
                description = "Supports affordable healthcare and agriculture innovations for underserved populations. Open to startups, NGOs, faculty, social enterprises.",
                grant_type  = "Startup Grant",
                eligibility = ["Startup", "Social Enterprise", "Faculty", "NGO"],
                disciplines = ["Healthcare", "Agriculture", "Biotechnology"],
                amount      = "Up to ₹50 Lakhs",
            ),
            self.build_grant(
                title       = "BIRAC SBIRI (Small Business Innovation Research Initiative)",
                url         = "https://birac.nic.in/sbiri.php",
                deadline    = None,
                description = "Industry-academia collaborative grants for late-stage biotech product development. Phase I (₹50L) and Phase II (₹4Cr). Requires industry partner.",
                grant_type  = "Research Grant",
                eligibility = ["Company/Startup with Academic Partner"],
                disciplines = ["Biotechnology", "Biopharma", "MedTech", "Diagnostics"],
                amount      = "Phase I: ₹50L; Phase II: ₹4 Crores",
            ),
            self.build_grant(
                title       = "BIRAC BIPP (Biotechnology Industry Partnership Programme)",
                url         = "https://birac.nic.in/bipp.php",
                deadline    = None,
                description = "Large-scale industry-government partnership for national-need biotech product development.",
                grant_type  = "Research Grant",
                eligibility = ["Company", "Institution with Industry Partner"],
                disciplines = ["Biotechnology", "Biopharma", "Vaccines", "Diagnostics"],
                amount      = "Up to ₹25 Crores",
            ),
            self.build_grant(
                title       = "BIRAC SITARE (Student Innovators and Translational Research)",
                url         = "https://birac.nic.in/sitare.php",
                deadline    = None,
                description = "Seed funding for UG/PG/PhD students with innovative biotech ideas. Mentorship from BIRAC network. Good entry point for student-led innovation.",
                grant_type  = "Startup Grant",
                eligibility = ["UG/PG Student", "PhD Student", "Faculty Mentor required"],
                disciplines = ["Biotechnology", "Life Sciences", "MedTech"],
                amount      = "Up to ₹10 Lakhs",
            ),
            self.build_grant(
                title       = "BIRAC PACE (Academia-Industry Translation Research)",
                url         = "https://birac.nic.in/pace.php",
                deadline    = None,
                description = "Bridges laboratory research and commercial product. Indian institution + industry partner required.",
                grant_type  = "Research Grant",
                eligibility = ["Faculty", "Researcher", "with Industry Partner"],
                disciplines = ["Biotechnology", "Life Sciences", "Translational Research"],
                amount      = "Up to ₹2 Crores",
            ),
            self.build_grant(
                title       = "BIRAC DBT-BIRAC AMR Mission",
                url         = "https://birac.nic.in/cfp.php",
                deadline    = None,
                description = "Dedicated AMR research programme. Novel diagnostics, therapeutics, vaccines against drug-resistant pathogens. Directly relevant to ESKAPE pathogen research.",
                grant_type  = "Research Grant",
                eligibility = ["Faculty", "Researcher", "Startup", "Institution"],
                disciplines = ["AMR", "Infectious Disease", "Drug Discovery", "Diagnostics", "Vaccines"],
                amount      = "Varies by project scope",
            ),
            self.build_grant(
                title       = "BIRAC Bio-Saarthi — Global Mentorship for Biotech Startups",
                url         = "https://birac.nic.in/",
                deadline    = "2026-03-24",
                description = "Global mentorship connecting Indian biotech startups with international mentors. Call open for mentees till March 24, 2026.",
                grant_type  = "Startup Grant",
                eligibility = ["Startup", "Innovator", "Early-stage company"],
                disciplines = ["Biotechnology", "MedTech", "AgriTech"],
                amount      = "Mentorship support",
            ),
            self.build_grant(
                title       = "DBT-BIRAC Bio-AI Joint Call (BioE3 Biomanufacturing)",
                url         = "https://birac.nic.in/cfp.php",
                deadline    = None,
                description = "Joint call for Bio-AI proposals for biomanufacturing hubs under BioE3 Policy. AI + biotechnology convergence. Check birac.nic.in for current deadline.",
                grant_type  = "Research Grant",
                eligibility = ["Faculty", "Startup", "Institution"],
                disciplines = ["AI/ML", "Biotechnology", "Biomanufacturing", "Bioinformatics"],
                amount      = "Varies",
            ),
        ]
