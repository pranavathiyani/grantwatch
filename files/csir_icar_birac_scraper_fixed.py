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
    AGENCY_NAME    = "BIRAC"
    AGENCY_COUNTRY = "India"
    AGENCY_URL     = "https://birac.nic.in/cfp.php"

    def scrape(self) -> list:
        grants = []
        try:
            resp = requests.get(self.AGENCY_URL, timeout=20,
                                headers={"User-Agent": "Mozilla/5.0"})
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            for row in soup.select("table tr"):
                link = row.find("a")
                if not link:
                    continue
                title = link.get_text(strip=True)
                href  = link.get("href", "")
                if href and not href.startswith("http"):
                    href = "https://birac.nic.in/" + href.lstrip("/")
                row_text = row.get_text(" ", strip=True)
                date_hit = re.search(r"\b(\d{1,2}[-/.]\d{1,2}[-/.]\d{4})\b", row_text)
                deadline = _parse_date(date_hit.group(1)) if date_hit else None
                if len(title) < 6:
                    continue
                grants.append(self.build_grant(
                    title=title, url=href, deadline=deadline,
                    description=row_text[:300], grant_type="Innovation Grant",
                    eligibility=["Startup", "Faculty", "Researcher", "Industry"],
                    disciplines=["Biotechnology", "Biopharma", "MedTech", "AgriTech"],
                    amount="Varies",
                ))
        except Exception as e:
            print(f"  [BIRAC] {e}")
        return grants
