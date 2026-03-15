"""
Grant Watch ⌛ — DBT & ICMR Scrapers (Fixed)
Updated URL lists — their main pages restructured
"""

import re
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
                  "programme", "fund", "award", "project", "application"]


class DBTScraper(BaseScraper):
    AGENCY_NAME    = "DBT"
    AGENCY_COUNTRY = "India"
    AGENCY_URL     = "https://dbtindia.gov.in"

    def scrape(self) -> list:
        grants = []
        urls = [
            "https://dbtindia.gov.in/latest-announcement",
            "https://dbtindia.gov.in/whatsnew",
            "https://dbtindia.gov.in/funding-opportunities",
            "https://dbtindia.gov.in/",
        ]
        for url in urls:
            try:
                resp = requests.get(url, timeout=20,
                                    headers={"User-Agent": "Mozilla/5.0"})
                if resp.status_code != 200:
                    continue
                soup = BeautifulSoup(resp.text, "html.parser")
                links = soup.find_all("a", href=True)
                for link in links:
                    title = link.get_text(strip=True)
                    href  = link["href"]
                    if not href.startswith("http"):
                        href = "https://dbtindia.gov.in" + href
                    if not any(k in title.lower() for k in GRANT_KEYWORDS):
                        continue
                    if len(title) < 10:
                        continue
                    parent_text = link.parent.get_text(" ", strip=True) if link.parent else ""
                    date_hit = re.search(r"\b(\d{1,2}[-/.]\d{1,2}[-/.]\d{4})\b", parent_text)
                    deadline = _parse_date(date_hit.group(1)) if date_hit else None
                    grants.append(self.build_grant(
                        title=title, url=href, deadline=deadline,
                        description=parent_text[:300], grant_type="Research Grant",
                        eligibility=["Faculty", "Researcher", "Indian Institution"],
                        disciplines=["Biotechnology", "Life Sciences", "Bioinformatics"],
                        amount="Varies",
                    ))
                if grants:
                    break
            except Exception as e:
                print(f"  [DBT:{url}] {e}")
        return grants


class ICMRScraper(BaseScraper):
    AGENCY_NAME    = "ICMR"
    AGENCY_COUNTRY = "India"
    AGENCY_URL     = "https://icmr.gov.in/call-for-applications"

    def scrape(self) -> list:
        grants = []
        urls = [
            "https://icmr.gov.in/call-for-applications",
            "https://icmr.gov.in/",
        ]
        for url in urls:
            try:
                resp = requests.get(url, timeout=20,
                                    headers={"User-Agent": "Mozilla/5.0"})
                if resp.status_code != 200:
                    continue
                soup = BeautifulSoup(resp.text, "html.parser")
                # Try structured rows first
                rows = (soup.select("table tr") or
                        soup.select(".view-content .views-row") or
                        soup.select("li"))
                for row in rows:
                    link = row.find("a")
                    if not link:
                        continue
                    title = link.get_text(strip=True)
                    href  = link.get("href", "")
                    if href and not href.startswith("http"):
                        href = "https://icmr.gov.in" + href
                    if len(title) < 8:
                        continue
                    text = row.get_text(" ", strip=True)
                    date_hit = re.search(r"\b(\d{1,2}[-/.]\d{1,2}[-/.]\d{4})\b", text)
                    deadline = _parse_date(date_hit.group(1)) if date_hit else None
                    grants.append(self.build_grant(
                        title=title, url=href, deadline=deadline,
                        description=text[:300], grant_type="Research Grant",
                        eligibility=["Faculty", "Medical Researcher", "Institution"],
                        disciplines=["Medical Research", "Public Health", "Clinical Research"],
                        amount="Varies",
                    ))
                if grants:
                    break
                # Fallback: grab any keyword links
                for link in soup.find_all("a", href=True):
                    title = link.get_text(strip=True)
                    if len(title) < 10:
                        continue
                    if not any(k in title.lower() for k in GRANT_KEYWORDS):
                        continue
                    href = link["href"]
                    if not href.startswith("http"):
                        href = "https://icmr.gov.in" + href
                    grants.append(self.build_grant(
                        title=title, url=href, deadline=None,
                        description=f"ICMR funding: {title}",
                        grant_type="Research Grant",
                        eligibility=["Faculty", "Medical Researcher"],
                        disciplines=["Medical Research", "Public Health"],
                        amount="Varies",
                    ))
                if grants:
                    break
            except Exception as e:
                print(f"  [ICMR:{url}] {e}")
        return grants
