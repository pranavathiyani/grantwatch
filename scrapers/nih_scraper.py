"""
Grant Watch ⌛ — NIH Scraper (India-relevant only)
RSS feed replaced — it pulled admin notices irrelevant to Indian researchers.
Kept: R01/R21 (foreign org eligible) + Fogarty (designed for India).
"""
from .base_scraper import BaseScraper

class NIHScraper(BaseScraper):
    AGENCY_NAME    = "NIH"
    AGENCY_COUNTRY = "International"
    AGENCY_URL     = "https://grants.nih.gov/new-to-nih/information-for/foreign-grants"

    def scrape(self):
        return [
            self.build_grant(
                title       = "NIH R01 Research Grant (Indian Institution eligible as Foreign Org)",
                url         = "https://grants.nih.gov/funding/activity-codes/R01",
                deadline    = None,
                description = (
                    "Indian institutions can apply as foreign organisations. Technically eligible "
                    "but rare in practice — requires SAM/eRA Commons registration and strong US "
                    "relevance justification. Most practical route: partner with US PI who leads "
                    "the R01 with Indian team as foreign component."
                ),
                grant_type  = "Research Grant",
                eligibility = ["Faculty", "Indian Institution (as foreign org)", "or Co-PI on US-led grant"],
                disciplines = ["Biomedical", "Life Sciences", "Any"],
                amount      = "Varies — typically USD 250,000–500,000/year",
            ),
            self.build_grant(
                title       = "NIH R21 Exploratory Research (Foreign Organisation eligible)",
                url         = "https://grants.nih.gov/funding/activity-codes/R21",
                deadline    = None,
                description = (
                    "Shorter exploratory grant — easier entry point than R01 for foreign orgs. "
                    "2 years, up to USD 275,000. Check each FOA eligibility section for "
                    "foreign org permission before applying."
                ),
                grant_type  = "Research Grant",
                eligibility = ["Faculty", "Indian Institution (as foreign org)"],
                disciplines = ["Biomedical", "Life Sciences", "Any"],
                amount      = "Up to USD 275,000 (2 years)",
            ),
        ]

class NIHFogartyScraper(BaseScraper):
    AGENCY_NAME    = "NIH Fogarty"
    AGENCY_COUNTRY = "International"
    AGENCY_URL     = "https://www.fic.nih.gov/Funding/Pages/default.aspx"

    def scrape(self):
        return [
            self.build_grant(
                title       = "NIH Fogarty FIRCA — International Research Collaboration Award",
                url         = "https://www.fic.nih.gov/Funding/Pages/default.aspx",
                deadline    = None,
                description = (
                    "Designed specifically for researchers in LMICs including India. "
                    "Indian PI collaborates with an existing NIH-funded US researcher. "
                    "Indian PI applies directly — best NIH entry point for Indian researchers."
                ),
                grant_type  = "Collaborative Grant",
                eligibility = ["Faculty", "Researcher at Indian Institution", "US NIH-funded collaborator required"],
                disciplines = ["Global Health", "Biomedical", "Infectious Disease", "Public Health"],
                amount      = "Up to USD 50,000/year (3 years)",
            ),
            self.build_grant(
                title       = "NIH Fogarty Global Health Research Training Programs",
                url         = "https://www.fic.nih.gov/Funding/Pages/default.aspx",
                deadline    = None,
                description = (
                    "Portfolio of Fogarty training programmes in global health, infectious disease, "
                    "neuroscience, and bioethics. India consistently one of top recipient countries."
                ),
                grant_type  = "Research Grant",
                eligibility = ["Faculty", "Researcher", "Indian Institution"],
                disciplines = ["Global Health", "Infectious Disease", "Neuroscience", "Biomedical"],
                amount      = "Varies by specific FOA",
            ),
        ]
