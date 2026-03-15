"""
Grant Watch ⌛ — Fellowship Scrapers
Covers: ANRF-NPDF, CSIR-SRF/JRF, DBT-JRF, ICMR-JRF, EMBL Fellowship,
        Ramalingaswami Re-entry, Ramanujan Fellowship, DST-INSPIRE Faculty,
        Wellcome Early Career, DBT-India Alliance, Prime Minister Research Fellowship
"""

from datetime import datetime
from .base_scraper import BaseScraper


class ANRFFellowshipScraper(BaseScraper):
    """ANRF / SERB Fellowships — NPDF, National Postdoctoral, Ramanujan"""
    AGENCY_NAME = "ANRF"
    AGENCY_COUNTRY = "India"
    AGENCY_URL = "https://anrf.gov.in/en/calls-for-proposals"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "ANRF National Post Doctoral Fellowship (N-PDF)",
                url         = "https://anrf.gov.in/en/calls-for-proposals",
                deadline    = None,
                description = "Postdoctoral fellowship for Indian researchers. Provides mentor support at premier Indian institutes. Rolling applications.",
                grant_type  = "Fellowship",
                eligibility = ["PhD Holder", "Early Career Researcher"],
                disciplines = ["Science", "Engineering", "Technology"],
                amount      = "₹55,000/month + HRA + research grant",
            ),
            self.build_grant(
                title       = "SERB/ANRF Ramanujan Fellowship",
                url         = "https://anrf.gov.in/en/calls-for-proposals",
                deadline    = None,
                description = "For Indian scientists returning from abroad or working overseas to take up research positions in India. 5-year fellowship.",
                grant_type  = "Fellowship",
                eligibility = ["Indian Scientist (Diaspora/Overseas)", "Faculty"],
                disciplines = ["Science", "Engineering", "Technology"],
                amount      = "₹1,35,000/month + research grant",
            ),
            self.build_grant(
                title       = "ANRF TARE (Teachers Associateship for Research Excellence)",
                url         = "https://anrf.gov.in/en/calls-for-proposals",
                deadline    = None,
                description = "Allows college teachers to work in nearby IITs/IISc labs. Bridges teaching and research, supports ≤3 years.",
                grant_type  = "Fellowship",
                eligibility = ["College Teacher", "Assistant Professor"],
                disciplines = ["Science", "Engineering"],
                amount      = "₹10,000/month + research grant",
            ),
        ]


class CSIRFellowshipScraper(BaseScraper):
    """CSIR JRF, SRF, Research Associateship"""
    AGENCY_NAME = "CSIR"
    AGENCY_COUNTRY = "India"
    AGENCY_URL = "https://csirhrdg.res.in/"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "CSIR Junior Research Fellowship (JRF)",
                url         = "https://csirhrdg.res.in/Home/Index/1/Default/2594/59",
                deadline    = None,
                description = "For NET-qualified candidates to pursue PhD in science. Awarded twice yearly (June & December cycle via CSIR-NET).",
                grant_type  = "Fellowship",
                eligibility = ["CSIR-NET Qualified", "BSc/MSc Graduate"],
                disciplines = ["Life Sciences", "Chemistry", "Physics", "Mathematics", "Engineering"],
                amount      = "₹37,000/month (JRF) → ₹42,000/month (SRF)",
            ),
            self.build_grant(
                title       = "CSIR Senior Research Fellowship (SRF)",
                url         = "https://csirhrdg.res.in/",
                deadline    = None,
                description = "Upgrade from JRF after 2 years with good performance. Also direct SRF (Gates) scheme for experienced researchers.",
                grant_type  = "Fellowship",
                eligibility = ["CSIR JRF Holder", "PhD Student (2+ years)"],
                disciplines = ["Science", "Engineering"],
                amount      = "₹42,000/month + HRA",
            ),
            self.build_grant(
                title       = "CSIR Research Associateship (RA)",
                url         = "https://csirhrdg.res.in/",
                deadline    = None,
                description = "Postdoctoral fellowship at CSIR institutes or universities. For PhD holders within 3 years of degree award.",
                grant_type  = "Fellowship",
                eligibility = ["PhD Holder (≤3 years)"],
                disciplines = ["Science", "Engineering", "Technology"],
                amount      = "₹54,000–58,000/month",
            ),
        ]


class DBTFellowshipScraper(BaseScraper):
    """DBT JRF, Ramalingaswami, Wellcome DBT India Alliance"""
    AGENCY_NAME = "DBT"
    AGENCY_COUNTRY = "India"
    AGENCY_URL = "https://dbtindia.gov.in"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "DBT Junior Research Fellowship (DBT-JRF)",
                url         = "https://dbtindia.gov.in/schemes-programmes/research-development/human-resource-development/dbt-jrf",
                deadline    = None,
                description = "For pursuing PhD in Biotechnology/Life Sciences. Selected via written test (BET). Twice yearly.",
                grant_type  = "Fellowship",
                eligibility = ["MSc/BTech Graduate", "BET Qualified"],
                disciplines = ["Biotechnology", "Life Sciences", "Bioinformatics"],
                amount      = "₹37,000/month (JRF) → ₹42,000/month (SRF)",
            ),
            self.build_grant(
                title       = "DBT Ramalingaswami Re-entry Fellowship",
                url         = "https://dbtindia.gov.in/schemes-programmes/research-development/human-resource-development/ramalingaswami-re-entry-fellowship",
                deadline    = None,
                description = "Prestigious re-entry fellowship for Indian scientists working abroad, to return and build independent labs in India. 5-year tenure.",
                grant_type  = "Fellowship",
                eligibility = ["Indian Scientist (Overseas)", "Early Career Researcher"],
                disciplines = ["Life Sciences", "Biotechnology", "Biomedical"],
                amount      = "₹1,30,000/month + ₹30 Lakhs research grant",
            ),
        ]


class WellcomeFellowshipScraper(BaseScraper):
    """Wellcome DBT India Alliance Fellowships"""
    AGENCY_NAME = "Wellcome DBT India Alliance"
    AGENCY_COUNTRY = "International"
    AGENCY_URL = "https://indiaalliance.org/apply-for-a-grant"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "Wellcome India Alliance — Early Career Fellowship",
                url         = "https://indiaalliance.org/apply-for-a-grant/early-career-fellowships",
                deadline    = None,
                description = "5-year fellowship for researchers who have completed PhD ≤ 5 years ago. Covers salary, research costs, and training. Highly competitive.",
                grant_type  = "Fellowship",
                eligibility = ["Early Career Researcher (PhD ≤5 years)"],
                disciplines = ["Biomedical", "Life Sciences", "Public Health"],
                amount      = "Up to ₹2.4 Crores (5 years)",
            ),
            self.build_grant(
                title       = "Wellcome India Alliance — Intermediate Fellowship",
                url         = "https://indiaalliance.org/apply-for-a-grant/intermediate-fellowship",
                deadline    = None,
                description = "For established Indian researchers seeking independence. 5-year award with salary and substantial research budget.",
                grant_type  = "Fellowship",
                eligibility = ["Faculty", "Researcher (PhD ≤12 years)"],
                disciplines = ["Biomedical", "Life Sciences", "Public Health"],
                amount      = "Up to ₹3.25 Crores (5 years)",
            ),
            self.build_grant(
                title       = "Wellcome India Alliance — Senior Fellowship",
                url         = "https://indiaalliance.org/apply-for-a-grant/senior-fellowships",
                deadline    = None,
                description = "5-year award for researchers with strong independent track record. Covers full research program costs.",
                grant_type  = "Fellowship",
                eligibility = ["Senior Faculty", "Independent Researcher"],
                disciplines = ["Biomedical", "Life Sciences"],
                amount      = "Up to ₹5.5 Crores (5 years)",
            ),
        ]


class EMBLFellowshipScraper(BaseScraper):
    """EMBL Postdoctoral and Predoctoral Fellowships"""
    AGENCY_NAME = "EMBL"
    AGENCY_COUNTRY = "International"
    AGENCY_URL = "https://www.embl.org/about/info/postdoctoral-programme/"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "EMBL Postdoctoral Fellowship (EIPOD)",
                url         = "https://www.embl.org/about/info/postdoctoral-programme/eipod-linc-programme/",
                deadline    = None,
                description = "EMBL Interdisciplinary Postdoctoral (EIPOD) programme at Heidelberg and other sites. Interdisciplinary life science research. Biannual calls.",
                grant_type  = "Fellowship",
                eligibility = ["PhD Holder (≤2 years)", "International Applicant"],
                disciplines = ["Structural Biology", "Computational Biology", "Genomics", "Cell Biology"],
                amount      = "EMBL salary scale + benefits",
            ),
            self.build_grant(
                title       = "EMBL Predoctoral Fellowship (PhD Programme)",
                url         = "https://www.embl.org/about/info/international-phd-programme/",
                deadline    = "2026-11-15",
                description = "Fully funded PhD positions at EMBL sites across Europe. Annual intake. Indian applicants eligible and encouraged.",
                grant_type  = "Fellowship",
                eligibility = ["MSc Graduate", "BTech Graduate (Research experience)"],
                disciplines = ["Computational Biology", "Genomics", "Structural Biology", "Cell Biology"],
                amount      = "Full stipend + benefits",
            ),
        ]


class DSTFellowshipScraper(BaseScraper):
    """DST INSPIRE Faculty, Women Scientist Schemes"""
    AGENCY_NAME = "DST"
    AGENCY_COUNTRY = "India"
    AGENCY_URL = "https://dst.gov.in/scientific-programmes/human-resource-development"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "DST INSPIRE Faculty Award",
                url         = "https://dst.gov.in/scientific-programmes/human-resource-development/inspire/inspire-faculty",
                deadline    = None,
                description = "5-year tenure track fellowship for young Indian scientists under 32 to work in any Indian academic or R&D institution.",
                grant_type  = "Fellowship",
                eligibility = ["Researcher (under 32)", "PhD Holder"],
                disciplines = ["Natural Sciences", "Mathematics", "Engineering"],
                amount      = "₹1,25,000/month + ₹7 Lakhs/year research grant",
            ),
            self.build_grant(
                title       = "DST Women Scientist Scheme-A (WOS-A)",
                url         = "https://dst.gov.in/scientific-programmes/gender-equity/women-scientist-schemes",
                deadline    = None,
                description = "Research grants for women scientists who had a career break. Supports independent research for 3 years.",
                grant_type  = "Fellowship",
                eligibility = ["Women Scientist (career break)", "Faculty"],
                disciplines = ["Science", "Engineering", "Technology", "Medicine"],
                amount      = "₹30,000/month + research grant",
            ),
            self.build_grant(
                title       = "DST KVPY (Kishore Vaigyanik Protsahan Yojana) — Fellowship",
                url         = "https://dst.gov.in/scientific-programmes/human-resource-development/kvpy",
                deadline    = None,
                description = "Scholarship-cum-fellowship for students in BS/BTech pursuing basic sciences, to be encouraged into research careers.",
                grant_type  = "Fellowship",
                eligibility = ["UG Student (Science/Engineering)"],
                disciplines = ["Basic Sciences", "Engineering"],
                amount      = "₹5,000–7,000/month",
            ),
        ]


class ICMRFellowshipScraper(BaseScraper):
    """ICMR JRF, SRF, Research Associateship"""
    AGENCY_NAME = "ICMR"
    AGENCY_COUNTRY = "India"
    AGENCY_URL = "https://icmr.gov.in/fellowship"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "ICMR Junior Research Fellowship (ICMR-JRF)",
                url         = "https://icmr.gov.in/fellowship",
                deadline    = None,
                description = "For pursuing PhD in biomedical and health sciences. Selected via ICMR-JRF exam held annually.",
                grant_type  = "Fellowship",
                eligibility = ["ICMR-JRF Qualified", "MSc/MBBS Graduate"],
                disciplines = ["Medical Research", "Public Health", "Biomedical Sciences"],
                amount      = "₹37,000/month (JRF) → ₹42,000/month (SRF)",
            ),
        ]


class PMRFFellowshipScraper(BaseScraper):
    """Prime Minister's Research Fellowship"""
    AGENCY_NAME = "PMRF (MoE)"
    AGENCY_COUNTRY = "India"
    AGENCY_URL = "https://www.pmrf.in/"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "Prime Minister's Research Fellowship (PMRF)",
                url         = "https://www.pmrf.in/",
                deadline    = None,
                description = "Flagship fellowship for BTech/MSc graduates joining PhD at IITs, IISc, NITs, IISERs. Twice yearly intake (Feb & July).",
                grant_type  = "Fellowship",
                eligibility = ["BTech/MSc Graduate (CGPA ≥ 8.0)", "Direct PhD entrant"],
                disciplines = ["Engineering", "Science", "Technology"],
                amount      = "₹70,000–80,000/month (5 years)",
            )
        ]


class FulbrightFellowshipScraper(BaseScraper):
    """Fulbright-Nehru Fellowships"""
    AGENCY_NAME = "Fulbright-Nehru"
    AGENCY_COUNTRY = "International"
    AGENCY_URL = "https://www.usief.org.in/Fellowships.aspx"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "Fulbright-Nehru Postdoctoral Research Fellowship",
                url         = "https://www.usief.org.in/Fellowships.aspx",
                deadline    = "2026-07-15",
                description = "8–24 months at a US institution. For Indian early career researchers in science, technology, and innovation fields.",
                grant_type  = "Fellowship",
                eligibility = ["Early Career Researcher", "PhD Holder (≤5 years)"],
                disciplines = ["Science", "Technology", "Public Policy", "Any"],
                amount      = "Living allowance + travel + health insurance",
            ),
            self.build_grant(
                title       = "Fulbright-Nehru Doctoral Research Fellowship",
                url         = "https://www.usief.org.in/Fellowships.aspx",
                deadline    = "2026-07-01",
                description = "6–9 months dissertation research in the United States. Priority: AI, energy, space science, defense.",
                grant_type  = "Fellowship",
                eligibility = ["PhD Student (registered in India)"],
                disciplines = ["AI/ML", "Energy", "Space Science", "Defense", "Any"],
                amount      = "Full support (stipend, housing, travel)",
            ),
        ]


class HFSPScraper(BaseScraper):
    """Human Frontier Science Program — Research Grants"""
    AGENCY_NAME = "HFSP"
    AGENCY_COUNTRY = "International"
    AGENCY_URL = "https://www.hfsp.org/funding/hfsp-funding/research-grants"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "HFSP Research Grant — Program Grant",
                url         = "https://www.hfsp.org/funding/hfsp-funding/research-grants",
                deadline    = "2026-03-17",
                description = "High-risk, high-reward basic life science research through international teams. India-based PIs can lead or join. One of the most prestigious international grants for life sciences.",
                grant_type  = "Research Grant",
                eligibility = ["Faculty", "Independent Researcher"],
                disciplines = ["Life Sciences", "Biophysics", "Neuroscience", "Computational Biology"],
                amount      = "Up to USD 450,000/year (3 years)",
            ),
            self.build_grant(
                title       = "HFSP Long-Term Fellowship",
                url         = "https://www.hfsp.org/funding/hfsp-funding/fellowships",
                deadline    = None,
                description = "3-year postdoctoral fellowship in a different country/discipline. Strongly interdisciplinary. Annual call.",
                grant_type  = "Fellowship",
                eligibility = ["PhD Holder (≤3 years)", "International Applicant"],
                disciplines = ["Life Sciences", "Computational Biology", "Biophysics"],
                amount      = "Stipend + research allowance + travel",
            ),
        ]
