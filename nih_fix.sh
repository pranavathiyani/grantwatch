cat > /mnt/d/grantwatch/scrapers/nih_scraper.py << 'EOF'
"""
Grant Watch ⌛ — NIH Scraper (India-relevant only)

What Indian researchers at Indian institutions can actually apply for:

KEEP:
  NIH Fogarty (FIC)    — explicitly designed for India/global collaboration
  R01/R21 as foreign PI — possible but rare; include with honest description
  Specific PAR/RFA      — only those explicitly allowing foreign orgs

REMOVED:
  General RSS feed (fundingopps.xml) — pulls admin notices, policy changes,
  fellowship/training grants not open to Indians — pure noise

Reality check: Direct NIH grants to Indian institutions are technically
possible (R01/R21) but extremely rare due to foreign org compliance burden.
Most Indian researchers access NIH via Fogarty or as Co-PI on US-led grants.
"""

from .base_scraper import BaseScraper


class NIHScraper(BaseScraper):
    AGENCY_NAME    = "NIH"
    AGENCY_COUNTRY = "International"
    AGENCY_URL     = "https://grants.nih.gov/funding/nih-guide-for-grants-and-contracts"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "NIH R01 Research Project Grant (Foreign Organisation eligible)",
                url         = "https://grants.nih.gov/funding/activity-codes/R01",
                deadline    = None,
                description = (
                    "Indian institutions can apply as foreign organisations for R01 grants. "
                    "Technically eligible but rare in practice — requires institutional "
                    "registration (SAM, eRA Commons), strong US relevance justification, "
                    "and state department clearance. Best route: partner with a US PI "
                    "who leads the application."
                ),
                grant_type  = "Research Grant",
                eligibility = ["Faculty", "Indian Institution (as foreign org)"],
                disciplines = ["Biomedical", "Life Sciences", "Any"],
                amount      = "Varies (direct + indirect costs)",
            ),
            self.build_grant(
                title       = "NIH R21 Exploratory/Developmental Research (Foreign eligible)",
                url         = "https://grants.nih.gov/funding/activity-codes/R21",
                deadline    = None,
                description = (
                    "Shorter exploratory grant — easier entry point than R01 for foreign orgs. "
                    "2 years, up to USD 275,000. Indian PI can lead or be Co-PI. "
                    "Check each PAR/RFA's eligibility section for foreign org restriction."
                ),
                grant_type  = "Research Grant",
                eligibility = ["Faculty", "Indian Institution (as foreign org)"],
                disciplines = ["Biomedical", "Life Sciences", "Any"],
                amount      = "Up to USD 275,000 (2 years)",
            ),
        ]


class NIHFogartyScraper(BaseScraper):
    """
    NIH Fogarty International Center — explicitly designed for global health
    and India-US research collaboration. This is the most relevant NIH
    mechanism for Indian researchers.
    """
    AGENCY_NAME    = "NIH Fogarty"
    AGENCY_COUNTRY = "International"
    AGENCY_URL     = "https://www.fic.nih.gov/Funding/Pages/default.aspx"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "NIH Fogarty International Research Collaboration Award (FIRCA)",
                url         = "https://www.fic.nih.gov/Funding/Pages/default.aspx",
                deadline    = None,
                description = (
                    "Supports Indian researchers to collaborate with NIH-funded US PIs. "
                    "Indian PI applies directly — no need for separate US application. "
                    "Specifically designed for researchers in LMICs including India."
                ),
                grant_type  = "Collaborative Grant",
                eligibility = ["Faculty", "Researcher at Indian Institution"],
                disciplines = ["Global Health", "Biomedical", "Infectious Disease",
                               "Public Health"],
                amount      = "Up to USD 50,000/year (3 years)",
            ),
            self.build_grant(
                title       = "NIH Fogarty Global Brain and Nervous System Disorders Program",
                url         = "https://www.fic.nih.gov/Funding/Pages/default.aspx",
                deadline    = None,
                description = (
                    "Fogarty program for neuroscience research in LMICs. India-eligible. "
                    "Supports capacity building and collaborative research in brain disorders."
                ),
                grant_type  = "Research Grant",
                eligibility = ["Faculty", "Researcher", "Indian Institution"],
                disciplines = ["Neuroscience", "Global Health", "Clinical Research"],
                amount      = "Varies by specific FOA",
            ),
        ]
EOF
echo "✓ nih_scraper.py replaced"
