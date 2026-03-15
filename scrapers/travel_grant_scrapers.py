"""
Grant Watch ⌛ — Travel Grant Scrapers
Covers: EMBO Travel Grants, CSIR Travel, DBT Overseas Travel,
        INSA, IYBA, FEBS, Royal Society, SERB-ITS (now ANRF-ITS)
"""

import re
import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper


def _parse_date(text: str):
    from datetime import datetime
    for fmt in ("%d %B %Y", "%B %d, %Y", "%d-%m-%Y", "%d/%m/%Y",
                "%Y-%m-%d", "%d.%m.%Y", "%b %d, %Y"):
        try:
            return datetime.strptime(text.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


# ─────────────────────────────────────────────
# EMBO Travel Grants (Short-Term Fellowships)
# ─────────────────────────────────────────────
class EMBOTravelScraper(BaseScraper):
    AGENCY_NAME = "EMBO"
    AGENCY_COUNTRY = "International"
    AGENCY_URL = "https://www.embo.org/funding-awards/scientific-exchange-grants/"

    def scrape(self) -> list:
        grants = []
        pages = [
            ("EMBO Scientific Exchange Grant",
             "https://www.embo.org/funding-awards/scientific-exchange-grants/",
             "Supports short scientific visits to labs in EMBC member/associate countries. Rolling deadline, decisions within 6 weeks.",
             "Up to €2,500"),
            ("EMBO Short-Term Fellowship",
             "https://www.embo.org/funding-awards/short-term-fellowships/",
             "Up to 3 months at EMBC member country lab. For PhD students and postdocs. Rolling applications.",
             "Stipend + travel"),
        ]
        for title, url, desc, amount in pages:
            grants.append(self.build_grant(
                title       = title,
                url         = url,
                deadline    = None,   # rolling
                description = desc,
                grant_type  = "Travel Grant",
                eligibility = ["PhD Student", "Postdoc", "Researcher"],
                disciplines = ["Life Sciences", "Molecular Biology"],
                amount      = amount,
            ))
        return grants


# ─────────────────────────────────────────────
# ANRF / SERB International Travel Support (ITS)
# ─────────────────────────────────────────────
class ANRFITSScraper(BaseScraper):
    AGENCY_NAME = "ANRF"
    AGENCY_COUNTRY = "India"
    AGENCY_URL = "https://anrf.gov.in/en/calls-for-proposals"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "ANRF International Travel Support (ITS)",
                url         = "https://anrf.gov.in/en/calls-for-proposals",
                deadline    = None,
                description = "Supports Indian researchers to present papers at international conferences abroad. Rolling applications throughout the year.",
                grant_type  = "Travel Grant",
                eligibility = ["Faculty", "Researcher", "PhD Student"],
                disciplines = ["Any"],
                amount      = "Up to ₹2 Lakhs",
            )
        ]


# ─────────────────────────────────────────────
# DBT Overseas Associateship / Travel
# ─────────────────────────────────────────────
class DBTTravelScraper(BaseScraper):
    AGENCY_NAME = "DBT"
    AGENCY_COUNTRY = "India"
    AGENCY_URL = "https://dbtindia.gov.in/schemes-programmes/research-development/human-resource-development"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "DBT Overseas Associateship",
                url         = "https://dbtindia.gov.in/schemes-programmes/research-development/human-resource-development/overseas-associateship",
                deadline    = None,
                description = "Supports Indian scientists with PhDs to work at overseas labs for 6–12 months. Covers travel, subsistence, and research costs.",
                grant_type  = "Travel Grant",
                eligibility = ["Early Career Researcher", "Faculty"],
                disciplines = ["Biotechnology", "Life Sciences", "Bioinformatics"],
                amount      = "As per DBT norms",
            ),
            self.build_grant(
                title       = "DBT-EMBL Short-Term Visit Programme",
                url         = "https://dbtindia.gov.in/",
                deadline    = None,
                description = "Joint DBT-EMBL programme supporting short visits by Indian researchers to EMBL labs in Heidelberg and other sites.",
                grant_type  = "Travel Grant",
                eligibility = ["PhD Student", "Postdoc", "Early Career Researcher"],
                disciplines = ["Computational Biology", "Structural Biology", "Genomics"],
                amount      = "Full travel + accommodation",
            ),
        ]


# ─────────────────────────────────────────────
# CSIR Travel Grant
# ─────────────────────────────────────────────
class CSIRTravelScraper(BaseScraper):
    AGENCY_NAME = "CSIR"
    AGENCY_COUNTRY = "India"
    AGENCY_URL = "https://www.csir.res.in/travel-grant"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "CSIR Travel Grant for International Conferences",
                url         = "https://www.csir.res.in/travel-grant",
                deadline    = None,
                description = "Financial support for scientists/researchers to attend/present at international conferences. Applications reviewed on a rolling basis.",
                grant_type  = "Travel Grant",
                eligibility = ["Faculty", "Researcher", "CSIR Scientist"],
                disciplines = ["Any"],
                amount      = "Up to ₹1.5 Lakhs",
            )
        ]


# ─────────────────────────────────────────────
# INSA (Indian National Science Academy)
# ─────────────────────────────────────────────
class INSAScraper(BaseScraper):
    AGENCY_NAME = "INSA"
    AGENCY_COUNTRY = "India"
    AGENCY_URL = "https://insaindia.res.in/fellowship.php"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "INSA International Bilateral Exchange Programme",
                url         = "https://insaindia.res.in/fellowship.php",
                deadline    = None,
                description = "Exchange visits with foreign academies (Royal Society, NAS, JSPS, CNRS, DFG). For Indian scientists visiting abroad or hosting foreign scientists.",
                grant_type  = "Travel Grant",
                eligibility = ["Faculty", "Senior Researcher"],
                disciplines = ["Science", "Engineering"],
                amount      = "Varies by partner academy",
            ),
            self.build_grant(
                title       = "INSA Senior Scientist Fellowship",
                url         = "https://insaindia.res.in/fellowship.php",
                deadline    = None,
                description = "For INSA Fellows and active scientists post-superannuation to continue research. Provides honorarium and research support.",
                grant_type  = "Fellowship",
                eligibility = ["Senior Scientist", "Superannuated Faculty"],
                disciplines = ["Science", "Engineering"],
                amount      = "₹15,000/month + contingency",
            ),
        ]


# ─────────────────────────────────────────────
# FEBS Travel Grants
# ─────────────────────────────────────────────
class FEBSScraper(BaseScraper):
    AGENCY_NAME = "FEBS"
    AGENCY_COUNTRY = "International"
    AGENCY_URL = "https://www.febs.org/funding/fellowships-and-grants/"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "FEBS Short-Term Fellowship",
                url         = "https://www.febs.org/funding/fellowships-and-grants/short-term-fellowships/",
                deadline    = None,
                description = "Supports short research visits (1–3 months) to a lab in a different country. Open to researchers from FEBS constituent societies.",
                grant_type  = "Travel Grant",
                eligibility = ["PhD Student", "Postdoc", "Early Career Researcher"],
                disciplines = ["Biochemistry", "Molecular Biology", "Life Sciences"],
                amount      = "Up to €3,500",
            ),
            self.build_grant(
                title       = "FEBS Science for Life Laboratory Prize",
                url         = "https://www.febs.org/funding/",
                deadline    = None,
                description = "Annual FEBS prize for outstanding contributions to molecular life sciences. Includes travel to FEBS Congress.",
                grant_type  = "Travel Grant",
                eligibility = ["Researcher", "Early Career"],
                disciplines = ["Molecular Biology", "Life Sciences"],
                amount      = "Prize + travel",
            ),
        ]
