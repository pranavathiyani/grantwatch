"""
Grant Watch ⌛ — International Grants Scrapers
Covers: DBT-Wellcome India Alliance, EMBO, Gates Grand Challenges,
        NIH Fogarty (India-eligible), Newton-Bhabha (UK-India)
"""

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .base_scraper import BaseScraper


def _parse_date(text: str):
    for fmt in ("%d %B %Y", "%B %d, %Y", "%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(text.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


# ─────────────────────────────────────────────
# Wellcome DBT India Alliance
# ─────────────────────────────────────────────
class WellcomeScraper(BaseScraper):
    AGENCY_NAME = "Wellcome DBT India Alliance"
    AGENCY_COUNTRY = "International"
    AGENCY_URL = "https://indiaalliance.org/apply-for-a-grant/current-calls"

    def scrape(self) -> list:
        grants = []
        try:
            resp = requests.get(self.AGENCY_URL, timeout=30,
                                headers={"User-Agent": "Mozilla/5.0"})
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")

            for block in soup.select(".grant-item, .call-item, article, .card"):
                link = block.find("a")
                if not link:
                    continue
                title = link.get_text(strip=True)
                href  = link.get("href", "")
                if not href.startswith("http"):
                    href = "https://indiaalliance.org" + href
                text = block.get_text(" ", strip=True)
                date_hit = re.search(
                    r"\b(\d{1,2}\s+\w+\s+\d{4}|\d{1,2}/\d{1,2}/\d{4})\b", text
                )
                deadline = _parse_date(date_hit.group(1)) if date_hit else None
                if len(title) < 8:
                    continue
                grants.append(self.build_grant(
                    title       = title,
                    url         = href,
                    deadline    = deadline,
                    description = text[:300],
                    grant_type  = "Fellowship / Grant",
                    eligibility = ["Early Career Researcher", "Faculty", "Indian Researcher"],
                    disciplines = ["Biomedical", "Life Sciences", "Public Health"],
                    amount      = "Varies by scheme",
                ))
        except Exception as e:
            print(f"  [Wellcome] {e}")
        return grants


# ─────────────────────────────────────────────
# EMBO (Travel / Installation / Scientific)
# ─────────────────────────────────────────────
class EMBOScraper(BaseScraper):
    AGENCY_NAME = "EMBO"
    AGENCY_COUNTRY = "International"
    AGENCY_URL = "https://www.embo.org/funding-awards/"

    def scrape(self) -> list:
        grants = []
        try:
            resp = requests.get(self.AGENCY_URL, timeout=30,
                                headers={"User-Agent": "Mozilla/5.0"})
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            for link in soup.select("a[href]"):
                title = link.get_text(strip=True)
                href  = link["href"]
                keywords = ["grant", "fellowship", "award", "fund", "travel", "installation"]
                if not any(k in title.lower() for k in keywords):
                    continue
                if len(title) < 10:
                    continue
                if not href.startswith("http"):
                    href = "https://www.embo.org" + href
                grants.append(self.build_grant(
                    title       = title,
                    url         = href,
                    deadline    = None,  # EMBO rolling deadlines, check page
                    description = f"EMBO funding opportunity: {title}",
                    grant_type  = "Fellowship / Award",
                    eligibility = ["Researcher", "Postdoc", "Faculty"],
                    disciplines = ["Life Sciences", "Molecular Biology"],
                    amount      = "Varies",
                ))
        except Exception as e:
            print(f"  [EMBO] {e}")
        return grants


# ─────────────────────────────────────────────
# Gates Foundation Grand Challenges
# ─────────────────────────────────────────────
class GatesScraper(BaseScraper):
    AGENCY_NAME = "Gates Foundation"
    AGENCY_COUNTRY = "International"
    AGENCY_URL = "https://gcgh.grandchallenges.org/challenges"

    def scrape(self) -> list:
        grants = []
        try:
            resp = requests.get(self.AGENCY_URL, timeout=30,
                                headers={"User-Agent": "Mozilla/5.0"})
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            for card in soup.select(".challenge-card, article, .views-row"):
                link = card.find("a")
                if not link:
                    continue
                title = link.get_text(strip=True)
                href  = link.get("href", "")
                if not href.startswith("http"):
                    href = "https://gcgh.grandchallenges.org" + href
                text = card.get_text(" ", strip=True)
                date_hit = re.search(r"\b(\w+\s+\d{1,2},\s+\d{4})\b", text)
                deadline = _parse_date(date_hit.group(1)) if date_hit else None
                if len(title) < 8:
                    continue
                grants.append(self.build_grant(
                    title       = title,
                    url         = href,
                    deadline    = deadline,
                    description = text[:300],
                    grant_type  = "Grand Challenge",
                    eligibility = ["Researcher", "Institution", "NGO", "Company"],
                    disciplines = ["Global Health", "Agriculture", "Poverty", "Vaccines"],
                    amount      = "Up to $100,000 (exploratory)",
                ))
        except Exception as e:
            print(f"  [Gates] {e}")
        return grants


# ─────────────────────────────────────────────
# NIH Fogarty International (India-eligible)
# ─────────────────────────────────────────────
class FogartyScraper(BaseScraper):
    AGENCY_NAME = "NIH Fogarty"
    AGENCY_COUNTRY = "International"
    AGENCY_URL = "https://www.fic.nih.gov/Funding/Pages/default.aspx"

    def scrape(self) -> list:
        grants = []
        try:
            resp = requests.get(self.AGENCY_URL, timeout=30,
                                headers={"User-Agent": "Mozilla/5.0"})
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            for link in soup.find_all("a", href=True):
                title = link.get_text(strip=True)
                href  = link["href"]
                if not any(k in title.lower() for k in ["grant", "fund", "fellowship", "training", "research"]):
                    continue
                if len(title) < 10:
                    continue
                if not href.startswith("http"):
                    href = "https://www.fic.nih.gov" + href
                grants.append(self.build_grant(
                    title       = title,
                    url         = href,
                    deadline    = None,
                    description = f"NIH Fogarty International: {title}",
                    grant_type  = "International Research Grant",
                    eligibility = ["Faculty", "Researcher", "Institution"],
                    disciplines = ["Global Health", "Biomedical", "Infectious Disease"],
                    amount      = "Varies",
                ))
        except Exception as e:
            print(f"  [Fogarty] {e}")
        return grants
