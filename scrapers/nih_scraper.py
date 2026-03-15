"""
Grant Watch ⌛ — NIH Scraper (Fixed)
NIH moved to single RSS feed. Old per-activity rss_activity.cfm is dead.
New URL: https://grants.nih.gov/grants/guide/newsfeed/fundingopps.xml
From Oct 2025, Grants.gov is official single source for NIH opportunities.
"""

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from .base_scraper import BaseScraper

NIH_RSS_URL = "https://grants.nih.gov/grants/guide/newsfeed/fundingopps.xml"


class NIHScraper(BaseScraper):
    AGENCY_NAME    = "NIH"
    AGENCY_COUNTRY = "International"
    AGENCY_URL     = "https://grants.nih.gov/funding/nih-guide-for-grants-and-contracts"

    def scrape(self) -> list:
        grants = []
        try:
            resp = requests.get(
                NIH_RSS_URL,
                timeout=30,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "xml")

            for item in soup.find_all("item"):
                title    = item.find("title")
                link     = item.find("link")
                desc     = item.find("description")
                pub_date = item.find("pubDate")

                if not title or not link:
                    continue

                title_text = title.get_text(strip=True)
                link_text  = link.get_text(strip=True)
                desc_text  = desc.get_text(strip=True) if desc else ""

                # Determine activity code from title
                grant_type = "Research Grant"
                for code in ["PAR", "RFA", "PA ", "PAS", "R01", "R21", "R03"]:
                    if code in title_text:
                        grant_type = code.strip()
                        break

                # Estimate deadline ~90 days from publication
                deadline = None
                if pub_date:
                    try:
                        pd = datetime.strptime(
                            pub_date.get_text(strip=True)[:25],
                            "%a, %d %b %Y %H:%M:%S"
                        )
                        est = pd + timedelta(days=90)
                        if est > datetime.now():
                            deadline = est.strftime("%Y-%m-%d")
                    except Exception:
                        pass

                grants.append(self.build_grant(
                    title       = title_text,
                    url         = link_text,
                    deadline    = deadline,
                    description = desc_text[:400],
                    grant_type  = grant_type,
                    eligibility = ["Faculty", "Researcher", "Institution"],
                    disciplines = ["Biomedical", "Life Sciences", "Clinical Research"],
                    amount      = "Varies by mechanism",
                ))

        except Exception as e:
            print(f"  [NIH RSS] {e}")

        print(f"  [NIH] {len(grants)} entries from RSS")
        return grants
