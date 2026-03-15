"""
Grant Watch ⌛ — Additional Fellowships & Young Scientist Schemes

Covers:
  ANRF SRG        — Start-up Research Grant (early career, <5 yrs PhD)
  ANRF PM-ECRG    — Prime Minister Early Career Research Grant
  ANRF SIRE       — Short-term International Research Experience
  DBT-RA          — DBT Research Associateship (Postdoc)
  ICMR International Fellowship
  ICMR NISCHA / ANVESHAN — New small/intermediate grant schemes
  Young Scientist schemes — INSA, NASI, IASc
  S.S. Bhatnagar  — highest science award (career recognition)
  Swarnajayanti   — DST flagship fellowship
"""

from .base_scraper import BaseScraper


class ANRFEarlyCareerScraper(BaseScraper):
    AGENCY_NAME    = "ANRF"
    AGENCY_COUNTRY = "India"
    AGENCY_URL     = "https://anrf.gov.in/en/calls-for-proposals"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "ANRF Start-up Research Grant (SRG)",
                url         = "https://anrf.gov.in/en/calls-for-proposals",
                deadline    = None,
                description = (
                    "For faculty who obtained PhD ≤5 years ago and are in first faculty position. "
                    "Supports independent research setup. Rolling applications throughout year. "
                    "Cannot simultaneously hold NPDF or TARE."
                ),
                grant_type  = "Research Grant",
                eligibility = ["Assistant Professor (PhD ≤5 years)", "First faculty position"],
                disciplines = ["Science", "Engineering", "Technology"],
                amount      = "Up to ₹35 Lakhs (3 years)",
            ),
            self.build_grant(
                title       = "ANRF Prime Minister Early Career Research Grant (PM-ECRG)",
                url         = "https://anrf.gov.in/en/calls-for-proposals",
                deadline    = None,
                description = (
                    "New ANRF scheme replacing SERB-ECRA. Supports early career researchers "
                    "at Indian institutions. INSPIRE Faculty, Ramanujan, and Ramalingaswami "
                    "Fellows are explicitly eligible. Budget up to ₹1L/year each for travel and contingency."
                ),
                grant_type  = "Research Grant",
                eligibility = ["Early Career Faculty", "INSPIRE/Ramanujan/Ramalingaswami Fellows"],
                disciplines = ["Science", "Engineering", "Technology"],
                amount      = "Varies (project-based)",
            ),
            self.build_grant(
                title       = "ANRF SIRE — Short-term International Research Experience",
                url         = "https://anrf.gov.in/en/calls-for-proposals",
                deadline    = None,
                description = (
                    "Supports Indian researchers for short-term research visits (1–6 months) "
                    "to overseas labs. For PhD students, postdocs, and early career faculty. "
                    "Rolling applications."
                ),
                grant_type  = "Travel Grant",
                eligibility = ["PhD Student", "Postdoc", "Early Career Faculty"],
                disciplines = ["Science", "Engineering", "Technology"],
                amount      = "Travel + subsistence (as per norms)",
            ),
            self.build_grant(
                title       = "ANRF Swarnajayanti Fellowship",
                url         = "https://anrf.gov.in/en/calls-for-proposals",
                deadline    = None,
                description = (
                    "Prestigious DST/ANRF fellowship for scientists below 45 years with "
                    "exceptional track record. 5-year fellowship with complete academic freedom. "
                    "Annual call; highly competitive (~15 awarded/year)."
                ),
                grant_type  = "Fellowship",
                eligibility = ["Faculty/Researcher (under 45)", "Strong publication record"],
                disciplines = ["Basic Sciences", "Engineering"],
                amount      = "₹25,000/month supplement + ₹5 Lakhs/year research grant",
            ),
        ]


class DBTExtendedFellowshipScraper(BaseScraper):
    AGENCY_NAME    = "DBT"
    AGENCY_COUNTRY = "India"
    AGENCY_URL     = "https://dbtindia.gov.in"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "DBT Research Associateship (DBT-RA)",
                url         = "https://ra.dbtindia.gov.in/",
                deadline    = None,
                description = (
                    "Postdoctoral programme in biotechnology and life sciences. "
                    "PhD holders within 3 years of degree award. Hosted at any recognized "
                    "Indian institution with an established research group."
                ),
                grant_type  = "Fellowship",
                eligibility = ["PhD Holder (≤3 years)", "Biotechnology/Life Sciences"],
                disciplines = ["Biotechnology", "Life Sciences", "Bioinformatics", "Biomedical"],
                amount      = "₹54,000–67,000/month + HRA",
            ),
            self.build_grant(
                title       = "DBT-IYBA — Innovative Young Biotechnologist Award",
                url         = "https://dbtindia.gov.in/schemes-programmes/research-development/human-resource-development/innovative-young-biotechnologist-award",
                deadline    = None,
                description = (
                    "Annual award + research grant for outstanding young researchers in "
                    "biotechnology under 35 years. Provides 3-year research support in addition "
                    "to the award. One of DBT's most competitive early-career recognitions."
                ),
                grant_type  = "Award + Research Grant",
                eligibility = ["Researcher/Faculty (under 35)", "Indian Institution"],
                disciplines = ["Biotechnology", "Life Sciences", "Biomedical"],
                amount      = "₹30 Lakhs research grant (3 years) + award",
            ),
            self.build_grant(
                title       = "DBT-BUILDER Programme",
                url         = "https://dbtindia.gov.in/schemes-programmes/research-development/emerging-technologies/builder",
                deadline    = None,
                description = (
                    "Biotechnology/Life Sciences University-Based Interdisciplinary Life Sciences "
                    "Department and Research (BUILDER). Infrastructure and research support for "
                    "universities to build interdisciplinary life sciences programs."
                ),
                grant_type  = "Infrastructure Grant",
                eligibility = ["University Department", "Institution"],
                disciplines = ["Biotechnology", "Life Sciences", "Interdisciplinary"],
                amount      = "Up to ₹4 Crores",
            ),
        ]


class ICMRExtendedScraper(BaseScraper):
    AGENCY_NAME    = "ICMR"
    AGENCY_COUNTRY = "India"
    AGENCY_URL     = "https://icmr.gov.in"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "ICMR International Fellowship for Indian Biomedical Scientists",
                url         = "https://www.icmr.gov.in/icmr-international-fellowship-programme-for-indian-biomedical-scientists",
                deadline    = None,
                description = (
                    "Supports Indian biomedical scientists to work at advanced research labs abroad "
                    "for 3–6 months. Covers travel, maintenance allowance, and research costs. "
                    "Annual call. Strong career development opportunity for mid-career researchers."
                ),
                grant_type  = "Travel Grant",
                eligibility = ["Faculty/Researcher (Indian)", "PhD in biomedical field"],
                disciplines = ["Biomedical Research", "Public Health", "Clinical Research"],
                amount      = "Travel + monthly allowance (as per ICMR norms)",
            ),
            self.build_grant(
                title       = "ICMR ANVESHAN — Small Research Grant (ICMR SMALL)",
                url         = "https://icmr.gov.in/call-for-applications",
                deadline    = None,
                description = (
                    "ICMR's new small grant scheme (rebranded). Investigator-initiated research "
                    "proposals in biomedical and health sciences. Faster turnaround than ad-hoc grants. "
                    "Follow-on ANVESHAN available for ongoing work."
                ),
                grant_type  = "Research Grant",
                eligibility = ["Faculty", "Medical Researcher", "Institution"],
                disciplines = ["Biomedical Research", "Public Health", "Clinical Research"],
                amount      = "Up to ₹30 Lakhs",
            ),
            self.build_grant(
                title       = "ICMR NISCHA — Intermediate Research Grant",
                url         = "https://icmr.gov.in/call-for-applications",
                deadline    = None,
                description = (
                    "ICMR intermediate-scale grant for established researchers. Mid-tier between "
                    "ANVESHAN (small) and full ad-hoc grants. For health research with clear "
                    "translational potential."
                ),
                grant_type  = "Research Grant",
                eligibility = ["Faculty", "Senior Researcher", "Institution"],
                disciplines = ["Biomedical Research", "Public Health", "Translational Research"],
                amount      = "₹30–70 Lakhs",
            ),
        ]


class YoungScientistAwardScraper(BaseScraper):
    """Young Scientist Awards that come with research grants"""
    AGENCY_NAME    = "Various"
    AGENCY_COUNTRY = "India"
    AGENCY_URL     = "https://dst.gov.in"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "INSA Young Scientist Award",
                url         = "https://insaindia.res.in/award_ys.php",
                deadline    = None,
                description = (
                    "Annual award for Indian scientists under 35 for outstanding contributions. "
                    "Comes with a medal, citation, and research support grant. One of the most "
                    "prestigious young scientist recognitions in India."
                ),
                grant_type  = "Award + Research Grant",
                eligibility = ["Researcher/Faculty (under 35)", "Indian Institution"],
                disciplines = ["Science", "Engineering"],
                amount      = "Medal + research grant",
            ),
            self.build_grant(
                title       = "DST Young Scientist Award (SERC Fast Track / SRG equivalent)",
                url         = "https://anrf.gov.in/en/calls-for-proposals",
                deadline    = None,
                description = (
                    "ANRF/SERB early career support for young scientists. Fast-track funding "
                    "mechanism for scientists within 5 years of PhD. Superseded partially by SRG; "
                    "check ANRF portal for current active scheme name."
                ),
                grant_type  = "Research Grant",
                eligibility = ["Faculty (PhD ≤5 years)"],
                disciplines = ["Science", "Engineering", "Technology"],
                amount      = "Up to ₹35 Lakhs",
            ),
            self.build_grant(
                title       = "NASI Young Scientist Platinum Jubilee Award",
                url         = "https://nasi.nic.in/",
                deadline    = None,
                description = (
                    "National Academy of Sciences India award for scientists under 35. "
                    "Includes cash prize, medal, and visibility for early career researchers."
                ),
                grant_type  = "Award",
                eligibility = ["Scientist (under 35)", "Indian Institution"],
                disciplines = ["Science", "Technology"],
                amount      = "Cash prize + medal",
            ),
            self.build_grant(
                title       = "IASc-INSA-NASI Joint Summer Research Fellowship",
                url         = "https://www.ias.ac.in/fellowship/",
                deadline    = None,
                description = (
                    "Summer research fellowships for final-year BSc/BE/MSc students to work "
                    "with fellows of the three science academies. Good pipeline for future "
                    "PhD students; also useful for faculty seeking collaborative network."
                ),
                grant_type  = "Fellowship",
                eligibility = ["BSc/BE/MSc Final Year Student"],
                disciplines = ["Science", "Engineering"],
                amount      = "₹10,000/month (2 months)",
            ),
        ]
