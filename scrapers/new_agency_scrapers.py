"""
Grant Watch ⌛ — UGC, DST, MeitY, SPARC, IMPRINT Scrapers
"""

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .base_scraper import BaseScraper


def _parse_date(text: str):
    for fmt in ("%d-%m-%Y", "%d/%m/%Y", "%B %d, %Y", "%d %B %Y", "%Y-%m-%d", "%d.%m.%Y"):
        try:
            return datetime.strptime(text.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


GRANT_KEYWORDS = ["call", "proposal", "grant", "fellowship", "scheme",
                  "programme", "fund", "award", "project", "opportunity",
                  "application", "research", "innovation", "vacancy"]


# ─────────────────────────────────────────────
# UGC
# ─────────────────────────────────────────────
class UGCScraper(BaseScraper):
    AGENCY_NAME = "UGC"
    AGENCY_COUNTRY = "India"
    AGENCY_URL = "https://frg.ugc.ac.in/"

    def scrape(self) -> list:
        """Seed with known UGC schemes; supplement with live scrape"""
        grants = [
            self.build_grant(
                title       = "UGC Major Research Project (MRP)",
                url         = "https://frg.ugc.ac.in/",
                deadline    = None,
                description = "Major Research Projects in Sciences (up to ₹12L) and Humanities/Social Sciences (up to ₹10L). For permanent faculty at UGC-recognized institutions.",
                grant_type  = "Research Grant",
                eligibility = ["Faculty (Permanent)", "UGC 2(f)/12B Institution"],
                disciplines = ["Science", "Humanities", "Social Sciences", "Engineering", "Any"],
                amount      = "Up to ₹12 Lakhs (Sciences)",
            ),
            self.build_grant(
                title       = "UGC Faculty Recharge Programme (FRP)",
                url         = "https://frg.ugc.ac.in/",
                deadline    = None,
                description = "Post-doctoral fellowship at Indian universities. Addresses shortage of quality faculty. Provides salary + research grant.",
                grant_type  = "Fellowship",
                eligibility = ["PhD Holder", "Postdoc"],
                disciplines = ["Any"],
                amount      = "₹50,000/month + research grant",
            ),
            self.build_grant(
                title       = "UGC Basic Scientific Research (BSR) Fellowship",
                url         = "https://frg.ugc.ac.in/",
                deadline    = None,
                description = "Research fellowships for meritorious students pursuing PhD in basic sciences at universities.",
                grant_type  = "Fellowship",
                eligibility = ["PhD Student", "UGC-recognized University"],
                disciplines = ["Basic Sciences", "Mathematics", "Life Sciences"],
                amount      = "₹25,000–28,000/month",
            ),
        ]

        # Try live scrape for any new calls
        try:
            resp = requests.get("https://ugc.gov.in/ugc_schemes/",
                                timeout=20, headers={"User-Agent": "Mozilla/5.0"})
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                for link in soup.find_all("a", href=True):
                    title = link.get_text(strip=True)
                    if len(title) < 10:
                        continue
                    if not any(k in title.lower() for k in GRANT_KEYWORDS):
                        continue
                    href = link["href"]
                    if not href.startswith("http"):
                        href = "https://ugc.gov.in" + href
                    grants.append(self.build_grant(
                        title       = title,
                        url         = href,
                        deadline    = None,
                        description = f"UGC scheme: {title}",
                        grant_type  = "Research Grant",
                        eligibility = ["Faculty", "UGC Institution"],
                        disciplines = ["Any"],
                        amount      = "Varies",
                    ))
        except Exception as e:
            print(f"  [UGC live] {e}")

        return grants


# ─────────────────────────────────────────────
# DST (separate from ANRF — FIST, PURSE, etc.)
# ─────────────────────────────────────────────
class DSTScraper(BaseScraper):
    AGENCY_NAME = "DST"
    AGENCY_COUNTRY = "India"
    AGENCY_URL = "https://dst.gov.in/call-for-proposals"

    def scrape(self) -> list:
        grants = [
            self.build_grant(
                title       = "DST-FIST (Fund for Improvement of S&T Infrastructure)",
                url         = "https://dst.gov.in/scientific-programmes/scientific-engineering-research/fist",
                deadline    = None,
                description = "Infrastructure grant for upgrading S&T facilities at universities and colleges. Level I (up to ₹80L) and Level II (up to ₹2Cr).",
                grant_type  = "Infrastructure Grant",
                eligibility = ["University", "College", "Department"],
                disciplines = ["Science", "Engineering", "Technology"],
                amount      = "Up to ₹2 Crores",
            ),
            self.build_grant(
                title       = "DST-PURSE (Promotion of University Research and Scientific Excellence)",
                url         = "https://dst.gov.in/scientific-programmes/scientific-engineering-research/purse",
                deadline    = None,
                description = "Grants to universities with good research output to strengthen research infrastructure and programs.",
                grant_type  = "Infrastructure Grant",
                eligibility = ["University with strong research output"],
                disciplines = ["Any"],
                amount      = "Up to ₹5 Crores",
            ),
            self.build_grant(
                title       = "DST Science and Heritage Research Initiative (SHRI)",
                url         = "https://dst.gov.in/call-for-proposals",
                deadline    = None,
                description = "Research integrating modern science with India's ancient heritage — astronomy, mathematics, metallurgy, traditional medicine.",
                grant_type  = "Research Grant",
                eligibility = ["Faculty", "Researcher"],
                disciplines = ["Science", "Heritage Studies", "Traditional Knowledge"],
                amount      = "Varies",
            ),
        ]

        # Live scrape DST calls page
        try:
            resp = requests.get(self.AGENCY_URL, timeout=20,
                                headers={"User-Agent": "Mozilla/5.0"})
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                for link in soup.find_all("a", href=True):
                    title = link.get_text(strip=True)
                    if len(title) < 10 or not any(k in title.lower() for k in GRANT_KEYWORDS):
                        continue
                    href = link["href"]
                    if not href.startswith("http"):
                        href = "https://dst.gov.in" + href
                    parent_text = link.parent.get_text(" ", strip=True) if link.parent else ""
                    date_hit = re.search(r"\b(\d{1,2}[-/.]\d{1,2}[-/.]\d{4})\b", parent_text)
                    deadline = _parse_date(date_hit.group(1)) if date_hit else None
                    grants.append(self.build_grant(
                        title=title, url=href, deadline=deadline,
                        description=parent_text[:300], grant_type="Research Grant",
                        eligibility=["Faculty", "Researcher"],
                        disciplines=["Science", "Engineering"], amount="Varies",
                    ))
        except Exception as e:
            print(f"  [DST live] {e}")

        return grants


# ─────────────────────────────────────────────
# MeitY
# ─────────────────────────────────────────────
class MeitYScraper(BaseScraper):
    AGENCY_NAME = "MeitY"
    AGENCY_COUNTRY = "India"
    AGENCY_URL = "https://www.meity.gov.in/content/financial-grants"

    def scrape(self) -> list:
        grants = [
            self.build_grant(
                title       = "MeitY AI Innovation Programme",
                url         = "https://www.meity.gov.in/content/financial-grants",
                deadline    = None,
                description = "Applied Research Track: ₹2–5Cr for AI projects at academic institutions (70% funded). Focus: healthcare, agriculture, education, smart cities.",
                grant_type  = "Research Grant",
                eligibility = ["Academic Institution", "Startup", "Company (Indian)"],
                disciplines = ["AI/ML", "Computer Science", "Data Science"],
                amount      = "Up to ₹10 Crores",
            ),
            self.build_grant(
                title       = "MeitY Cyber Security Research Grant",
                url         = "https://www.meity.gov.in/content/financial-grants",
                deadline    = None,
                description = "Research proposals in cybersecurity. Submission by email with subject 'Proposal for Research in Cyber Security'.",
                grant_type  = "Research Grant",
                eligibility = ["Faculty", "Researcher", "Institution"],
                disciplines = ["Cybersecurity", "Computer Science", "Networks"],
                amount      = "Varies",
            ),
            self.build_grant(
                title       = "MeitY-NSF Joint Research Programme",
                url         = "https://www.meity.gov.in/content/announcement-1st-joint-call-porposal-under--research-colaboration",
                deadline    = None,
                description = "India-US joint call. Focus: semiconductors, next-gen communications, cybersecurity, green tech, intelligent transport. Indian team funded by MeitY.",
                grant_type  = "Collaborative Grant",
                eligibility = ["Faculty", "Researcher", "Institution"],
                disciplines = ["Semiconductors", "Communications", "Cybersecurity", "Green Tech"],
                amount      = "Varies (INR, MeitY side)",
            ),
        ]

        try:
            resp = requests.get(self.AGENCY_URL, timeout=20,
                                headers={"User-Agent": "Mozilla/5.0"})
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                for link in soup.find_all("a", href=True):
                    title = link.get_text(strip=True)
                    if len(title) < 10 or not any(k in title.lower() for k in GRANT_KEYWORDS):
                        continue
                    href = link["href"]
                    if not href.startswith("http"):
                        href = "https://www.meity.gov.in" + href
                    grants.append(self.build_grant(
                        title=title, url=href, deadline=None,
                        description=f"MeitY funding opportunity: {title}",
                        grant_type="Research Grant",
                        eligibility=["Institution", "Faculty"],
                        disciplines=["IT", "AI/ML", "Electronics"], amount="Varies",
                    ))
        except Exception as e:
            print(f"  [MeitY live] {e}")

        return grants


# ─────────────────────────────────────────────
# SPARC (MoE — India-Foreign Collaboration)
# ─────────────────────────────────────────────
class SPARCScraper(BaseScraper):
    AGENCY_NAME = "SPARC (MoE)"
    AGENCY_COUNTRY = "India"
    AGENCY_URL = "https://sparc.iitkgp.ac.in/"

    def scrape(self) -> list:
        grants = [
            self.build_grant(
                title       = "SPARC — Scheme for Promotion of Academic and Research Collaboration",
                url         = "https://sparc.iitkgp.ac.in/",
                deadline    = None,
                description = "Joint proposals between Indian institutions and top-100 foreign universities. Covers exchange visits, joint workshops, and seed research grants.",
                grant_type  = "Collaborative Grant",
                eligibility = ["Faculty at IIT/NIT/IISER/Central Univ", "Foreign Collaborator (QS top-100)"],
                disciplines = ["Any — interdisciplinary encouraged"],
                amount      = "Up to ₹1.5 Crores (2 years)",
            )
        ]

        try:
            resp = requests.get(self.AGENCY_URL, timeout=20,
                                headers={"User-Agent": "Mozilla/5.0"})
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                for link in soup.find_all("a", href=True):
                    title = link.get_text(strip=True)
                    if len(title) < 10 or not any(k in title.lower() for k in GRANT_KEYWORDS):
                        continue
                    href = link["href"]
                    if not href.startswith("http"):
                        href = "https://sparc.iitkgp.ac.in" + href
                    grants.append(self.build_grant(
                        title=title, url=href, deadline=None,
                        description=f"SPARC call: {title}",
                        grant_type="Collaborative Grant",
                        eligibility=["Faculty", "Institution"],
                        disciplines=["Any"], amount="Varies",
                    ))
        except Exception as e:
            print(f"  [SPARC live] {e}")

        return grants


# ─────────────────────────────────────────────
# IMPRINT (MoE)
# ─────────────────────────────────────────────
class IMPRINTScraper(BaseScraper):
    AGENCY_NAME = "IMPRINT (MoE)"
    AGENCY_COUNTRY = "India"
    AGENCY_URL = "https://imprint.res.in/"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "IMPRINT-2 Research Grant (IIT-led)",
                url         = "https://imprint.res.in/",
                deadline    = None,
                description = "Impacting Research Innovation and Technology. Funds India-centric problems across 10 technology domains. IIT/NIT-led, but any Indian institution can collaborate.",
                grant_type  = "Research Grant",
                eligibility = ["Faculty", "IIT/NIT/IISER/University"],
                disciplines = ["Healthcare", "Energy", "Sustainable Habitat", "Water", "Manufacturing",
                               "IT & Communication", "Defence", "Transport", "Aerospace", "Advanced Materials"],
                amount      = "Up to ₹3 Crores",
            )
        ]
