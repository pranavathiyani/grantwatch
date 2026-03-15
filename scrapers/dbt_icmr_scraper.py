"""
Grant Watch ⌛ — DBT & ICMR Curated Scrapers
HTML scraping replaced — their sites mix navigation/old calls with current ones.
Each agency now returns 7-8 verified, described standing schemes.
"""
from .base_scraper import BaseScraper

class DBTScraper(BaseScraper):
    AGENCY_NAME    = "DBT"
    AGENCY_COUNTRY = "India"
    AGENCY_URL     = "https://dbtindia.gov.in"

    def scrape(self):
        return [
            self.build_grant(
                title       = "DBT Junior Research Fellowship (DBT-JRF)",
                url         = "https://dbtindia.gov.in/dbt-junior-research-fellowship-jrf-programme",
                deadline    = None,
                description = "PhD fellowship in Biotechnology/Life Sciences via BET exam. Twice yearly. One of India's most sought-after biotech fellowships.",
                grant_type  = "Fellowship",
                eligibility = ["MSc/BTech Graduate", "BET Qualified"],
                disciplines = ["Biotechnology", "Life Sciences", "Bioinformatics"],
                amount      = "₹37,000/month (JRF) → ₹42,000/month (SRF)",
            ),
            self.build_grant(
                title       = "DBT Research Associateship (DBT-RA)",
                url         = "https://ra.dbtindia.gov.in/",
                deadline    = None,
                description = "Postdoctoral programme for PhD holders within 3 years of degree. Hosted at any recognised Indian institution.",
                grant_type  = "Fellowship",
                eligibility = ["PhD Holder (≤3 years)"],
                disciplines = ["Biotechnology", "Life Sciences", "Bioinformatics"],
                amount      = "₹54,000–67,000/month + HRA",
            ),
            self.build_grant(
                title       = "DBT Ramalingaswami Re-entry Fellowship",
                url         = "https://dbtindia.gov.in/ramalingaswami-re-entry-fellowshiprrf-programme",
                deadline    = None,
                description = "Prestigious 5-year re-entry fellowship for Indian scientists working abroad. ₹1.3L/month + ₹30L research grant. Annual call.",
                grant_type  = "Fellowship",
                eligibility = ["Indian Scientist (Overseas)", "Early Career Researcher"],
                disciplines = ["Life Sciences", "Biotechnology", "Biomedical"],
                amount      = "₹1,30,000/month + ₹30 Lakhs research grant (5 years)",
            ),
            self.build_grant(
                title       = "DBT BioCARe (Biotechnology Career Advancement for Women)",
                url         = "https://dbtindia.gov.in/schemes-programmes/research-development/human-resource-development/biocare",
                deadline    = None,
                description = "Women scientist re-entry scheme. Salary + research costs for 3 years in biotechnology research.",
                grant_type  = "Fellowship",
                eligibility = ["Women Scientist (career break)", "Faculty"],
                disciplines = ["Biotechnology", "Life Sciences"],
                amount      = "Up to ₹55 Lakhs (3 years)",
            ),
            self.build_grant(
                title       = "DBT-IYBA — Innovative Young Biotechnologist Award",
                url         = "https://dbtindia.gov.in/schemes-programmes/research-development/human-resource-development/innovative-young-biotechnologist-award",
                deadline    = None,
                description = "Annual award + 3-year research grant for outstanding biotech researchers under 35. Highly competitive early-career recognition.",
                grant_type  = "Award",
                eligibility = ["Researcher/Faculty (under 35)", "Indian Institution"],
                disciplines = ["Biotechnology", "Life Sciences", "Biomedical"],
                amount      = "₹30 Lakhs research grant + award",
            ),
            self.build_grant(
                title       = "DBT Overseas Associateship",
                url         = "https://dbtindia.gov.in/schemes-programmes/research-development/human-resource-development/overseas-associateship",
                deadline    = None,
                description = "6–12 months at overseas labs for Indian scientists. Covers travel, subsistence, and research costs.",
                grant_type  = "Travel Grant",
                eligibility = ["Early Career Researcher", "Faculty", "PhD Holder"],
                disciplines = ["Biotechnology", "Life Sciences", "Bioinformatics"],
                amount      = "As per DBT norms",
            ),
            self.build_grant(
                title       = "DBT BUILDER Programme",
                url         = "https://dbtindia.gov.in/schemes-programmes/research-development/emerging-technologies/builder",
                deadline    = None,
                description = "Infrastructure and research support for universities to build interdisciplinary life science departments.",
                grant_type  = "Infrastructure Grant",
                eligibility = ["University Department", "Institution"],
                disciplines = ["Biotechnology", "Life Sciences", "Interdisciplinary"],
                amount      = "Up to ₹4 Crores",
            ),
            self.build_grant(
                title       = "DBT-EMBL Short-Term Visit Programme",
                url         = "https://dbtindia.gov.in/",
                deadline    = None,
                description = "Short visits by Indian researchers to EMBL labs in Heidelberg. Covers travel and accommodation.",
                grant_type  = "Travel Grant",
                eligibility = ["PhD Student", "Postdoc", "Early Career Researcher"],
                disciplines = ["Computational Biology", "Structural Biology", "Genomics"],
                amount      = "Full travel + accommodation",
            ),
        ]


class ICMRScraper(BaseScraper):
    AGENCY_NAME    = "ICMR"
    AGENCY_COUNTRY = "India"
    AGENCY_URL     = "https://icmr.gov.in/call-for-applications"

    def scrape(self):
        return [
            self.build_grant(
                title       = "ICMR Ad-hoc Research Projects (Extramural)",
                url         = "https://icmr.gov.in/call-for-applications",
                deadline    = None,
                description = "Main ICMR extramural research funding for biomedical and health research. Open to medical colleges, universities, and research institutions.",
                grant_type  = "Research Grant",
                eligibility = ["Faculty", "Medical Researcher", "Institution"],
                disciplines = ["Medical Research", "Public Health", "Epidemiology", "Clinical Research"],
                amount      = "Varies by project scope (₹10–50L typical)",
            ),
            self.build_grant(
                title       = "ICMR ANVESHAN — Small Research Grant",
                url         = "https://icmr.gov.in/call-for-applications",
                deadline    = None,
                description = "New ICMR small grant scheme. Faster turnaround than ad-hoc. Up to ₹30L. Follow-on ANVESHAN also available.",
                grant_type  = "Research Grant",
                eligibility = ["Faculty", "Medical Researcher", "Institution"],
                disciplines = ["Biomedical Research", "Public Health", "Clinical Research"],
                amount      = "Up to ₹30 Lakhs",
            ),
            self.build_grant(
                title       = "ICMR NISCHA — Intermediate Research Grant",
                url         = "https://icmr.gov.in/call-for-applications",
                deadline    = None,
                description = "Mid-tier ICMR grant (₹30–70L) for established researchers with translational potential. Between ANVESHAN and full ad-hoc.",
                grant_type  = "Research Grant",
                eligibility = ["Senior Researcher", "Faculty", "Institution"],
                disciplines = ["Biomedical Research", "Translational Research", "Public Health"],
                amount      = "₹30–70 Lakhs",
            ),
            self.build_grant(
                title       = "ICMR Junior Research Fellowship (ICMR-JRF)",
                url         = "https://icmr.gov.in/fellowships",
                deadline    = None,
                description = "Annual PhD fellowship in biomedical and health sciences. Selected via ICMR-JRF exam.",
                grant_type  = "Fellowship",
                eligibility = ["ICMR-JRF Qualified", "MSc/MBBS Graduate"],
                disciplines = ["Medical Research", "Public Health", "Biomedical Sciences"],
                amount      = "₹37,000/month → ₹42,000/month (SRF upgrade)",
            ),
            self.build_grant(
                title       = "ICMR International Fellowship for Indian Biomedical Scientists",
                url         = "https://icmr.gov.in/icmr-international-fellowship-programme-for-indian-biomedical-scientists",
                deadline    = None,
                description = "3–6 month research visits to advanced labs abroad. Covers travel and monthly allowance. Annual call.",
                grant_type  = "Travel Grant",
                eligibility = ["Faculty", "Researcher", "PhD in biomedical field"],
                disciplines = ["Biomedical Research", "Public Health", "Clinical Research"],
                amount      = "Travel + monthly allowance (ICMR norms)",
            ),
            self.build_grant(
                title       = "Indo-Swiss Joint Research Programme (ISJRP) — ICMR/DBT/SNSF 2026",
                url         = "https://icmr.gov.in/international-fellowships",
                deadline    = "2026-05-05",
                description = "Joint call: ICMR + DBT (India) + Swiss NSF. Indian PI funded by ICMR/DBT; Swiss PI by SNSF. Deadline May 5, 2026.",
                grant_type  = "Collaborative Grant",
                eligibility = ["Faculty (Indian PI)", "Swiss Co-PI required"],
                disciplines = ["Biomedical Research", "Life Sciences", "Biotechnology"],
                amount      = "Varies (ICMR/DBT norms for Indian side)",
            ),
            self.build_grant(
                title       = "ICMR Start-Up Grant for Induction into Biomedical Research",
                url         = "https://icmr.gov.in/call-for-applications",
                deadline    = None,
                description = "Seed grant for newly appointed faculty entering biomedical/health research. Helps establish research programme at a new institution.",
                grant_type  = "Research Grant",
                eligibility = ["Newly appointed Faculty", "MD/PhD"],
                disciplines = ["Biomedical Research", "Health Sciences"],
                amount      = "Up to ₹20 Lakhs (2 years)",
            ),
            self.build_grant(
                title       = "ICMR DHR Human Resource Development Fellowships",
                url         = "https://icmr.gov.in/fellowships",
                deadline    = None,
                description = "DHR HRD scheme covering research fellowships, short-term studentships, and postdoctoral fellowships in health research. Annual call.",
                grant_type  = "Fellowship",
                eligibility = ["MBBS/MD", "MSc", "PhD Student", "Postdoc"],
                disciplines = ["Medical Research", "Health Research", "Public Health"],
                amount      = "Varies by fellowship category",
            ),
        ]
