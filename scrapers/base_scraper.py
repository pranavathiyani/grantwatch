"""
Grant Watch ⌛ — Base Scraper
All agency scrapers inherit from this.
"""

import hashlib
from datetime import datetime
from abc import ABC, abstractmethod


class BaseScraper(ABC):
    AGENCY_NAME = "Unknown"
    AGENCY_COUNTRY = "India"  # or "International"
    AGENCY_URL = ""

    def make_id(self, title: str, agency: str) -> str:
        raw = f"{agency.lower()}-{title.lower()}"
        return hashlib.md5(raw.encode()).hexdigest()[:10]

    def build_grant(
        self,
        title: str,
        url: str,
        deadline: str = None,
        open_date: str = None,
        description: str = "",
        amount: str = "Not specified",
        eligibility: list = None,
        disciplines: list = None,
        grant_type: str = "Grant",
        status: str = "open",
    ) -> dict:
        return {
            "id": self.make_id(title, self.AGENCY_NAME),
            "title": title.strip(),
            "agency": self.AGENCY_NAME,
            "country": self.AGENCY_COUNTRY,
            "grant_type": grant_type,
            "amount": amount,
            "description": description.strip()[:500],
            "url": url,
            "deadline": deadline,
            "open_date": open_date,
            "eligibility": eligibility or ["Faculty", "Researcher"],
            "disciplines": disciplines or ["Any"],
            "status": status,
            "last_updated": datetime.utcnow().strftime("%Y-%m-%d"),
        }

    @abstractmethod
    def scrape(self) -> list:
        pass

    def run(self) -> list:
        print(f"[{self.AGENCY_NAME}] Scraping...")
        try:
            results = self.scrape()
            print(f"[{self.AGENCY_NAME}] Found {len(results)} grants")
            return results
        except Exception as e:
            print(f"[{self.AGENCY_NAME}] ERROR: {e}")
            return []
