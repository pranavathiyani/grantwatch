"""
Grant Watch ⌛ — EMBO Conference/Workshop Grants, EMBL Travel, SERB-POWER, Startup Grants

EMBO Workshop Organizing Grant  — up to €42,500 per workshop (organisers apply)
EMBO Courses/Conference Travel  — for attending EMBL/EMBO events
SERB-POWER                      — women researchers research grant
Startup Grants                  — DST-NIDHI, BIRAC-BIG, SISFS, TIDE 2.0, BIRAC-SPARSH
"""

from .base_scraper import BaseScraper


# ─────────────────────────────────────────────
# EMBO Conference & Workshop Grants
# ─────────────────────────────────────────────
class EMBOConferenceScraper(BaseScraper):
    """
    EMBO funds life science workshops and courses globally.
    Organisers (including India-based faculty) can apply to host EMBO Workshops.
    Participants can apply for travel grants to attend.
    """
    AGENCY_NAME    = "EMBO"
    AGENCY_COUNTRY = "International"
    AGENCY_URL     = "https://www.embo.org/funding/funding-for-conferences-and-training/"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "EMBO Workshop Organizing Grant",
                url         = "https://www.embo.org/funding/funding-for-conferences-and-training/workshops/",
                deadline    = None,   # 2027 workshop applications open ~mid-2026
                description = (
                    "Scientists can apply to organize an EMBO Workshop anywhere in the world, "
                    "including India. Core funding up to €35,000 + €5,500 for participant "
                    "travel grants + €1,000 childcare + €1,000 accessibility = up to €42,500. "
                    "EMBO handles registration, abstract submission, and workshop webpage. "
                    "Highly relevant for faculty hosting life science conferences."
                ),
                grant_type  = "Conference Grant",
                eligibility = ["Faculty", "Senior Researcher", "Any EMBO Member State or beyond"],
                disciplines = ["Life Sciences", "Molecular Biology", "Computational Biology",
                               "Bioinformatics", "Any life science"],
                amount      = "Up to €42,500 per workshop",
            ),
            self.build_grant(
                title       = "EMBO Lecture Course Organizing Grant",
                url         = "https://www.embo.org/funding/funding-for-conferences-and-training/lecture-courses/",
                deadline    = None,
                description = (
                    "EMBO funds practical lecture courses in life sciences. Organisers apply "
                    "to run intensive training courses. Supports curriculum, invited speakers, "
                    "and participant scholarships. Can be hosted in India."
                ),
                grant_type  = "Conference Grant",
                eligibility = ["Faculty", "Senior Researcher"],
                disciplines = ["Life Sciences", "Molecular Biology", "Bioinformatics"],
                amount      = "Up to €30,000 per course",
            ),
            self.build_grant(
                title       = "EMBL Course and Conference Travel Grant",
                url         = "https://www.embl.org/about/info/course-and-conference-office/information-for-participants/financial-assistance/",
                deadline    = None,   # per-event, check each event page
                description = (
                    "EMBL provides travel grants for researchers to attend EMBL/EMBO courses "
                    "and conferences. Covers airfare, accommodation, visa, registration fees. "
                    "Apply during abstract/motivation letter submission for each event. "
                    "Selection based on scientific merit, location, career stage."
                ),
                grant_type  = "Travel Grant",
                eligibility = ["PhD Student", "Postdoc", "Early Career Researcher"],
                disciplines = ["Life Sciences", "Bioinformatics", "Computational Biology"],
                amount      = "Variable cap per event (travel + accommodation + registration)",
            ),
            self.build_grant(
                title       = "EMBO Postdoctoral Fellowship (Spring/Autumn Rounds)",
                url         = "https://www.embo.org/funding/fellowships-grants-and-career-support/postdoctoral-fellowships/",
                deadline    = None,   # Spring 2026: 4th Friday of January; Autumn: ~August
                description = (
                    "Supports excellent postdocs for up to 2 years at labs in EMBC member states. "
                    "International mobility required. Includes salary/stipend, relocation allowance, "
                    "childcare support. From 2026: Spring round deadline = 4th Friday of January."
                ),
                grant_type  = "Fellowship",
                eligibility = ["PhD Holder", "International mobility required"],
                disciplines = ["Life Sciences", "Molecular Biology", "Computational Biology"],
                amount      = "Competitive stipend + relocation + benefits",
            ),
        ]


# ─────────────────────────────────────────────
# SERB-POWER (Women Researchers)
# ─────────────────────────────────────────────
class SERBPOWERScraper(BaseScraper):
    """
    SERB-POWER: Promoting Opportunities for Women in Exploratory Research
    Level I: IITs, IISERs, IISc, NITs, Central Universities, National Labs
    Level II: State Universities, Private Academic Institutions (SASTRA qualifies)
    """
    AGENCY_NAME    = "ANRF"
    AGENCY_COUNTRY = "India"
    AGENCY_URL     = "https://anrf.gov.in/en/calls-for-proposals"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "SERB-POWER Research Grant (Women Researchers)",
                url         = "https://www.indiascienceandtechnology.gov.in/funding-opportunities/research-grants/individual/serb-power-research-grants",
                deadline    = None,
                description = (
                    "Promotes women researchers in science and engineering. Two levels: "
                    "Level I for IITs/IISc/NITs/Central Univ (up to ₹60L, 3yr); "
                    "Level II for State/Private institutions like SASTRA (up to ₹30L, 3yr). "
                    "Regular academic/research position required. All S&E frontier areas."
                ),
                grant_type  = "Research Grant",
                eligibility = ["Women Faculty/Researcher (permanent position)", "Indian Institution"],
                disciplines = ["Science", "Engineering", "Technology", "Any frontier area"],
                amount      = "Up to ₹30 Lakhs (Level II — SASTRA eligible) / ₹60L (Level I)",
            ),
        ]


# ─────────────────────────────────────────────
# Startup Grants
# ─────────────────────────────────────────────
class StartupGrantsScraper(BaseScraper):
    """
    Startup and innovation grants relevant to SASTRA faculty/students
    starting companies or doing translational research.
    Includes DST-NIDHI, BIRAC-BIG, SISFS, TIDE 2.0, BIRAC-SPARSH.
    """
    AGENCY_NAME    = "Various (Startup)"
    AGENCY_COUNTRY = "India"
    AGENCY_URL     = "https://www.indiascienceandtechnology.gov.in/funding-opportunities/startups"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "DST-NIDHI PRAYAS Grant (Proof of Concept)",
                url         = "https://www.indiascienceandtechnology.gov.in/listingpage/startup-grants-nidhi-programme",
                deadline    = None,
                description = (
                    "DST National Initiative for Developing and Harnessing Innovations (NIDHI). "
                    "PRAYAS supports proof-of-concept development for innovators with technology-"
                    "based ideas. Up to ₹10L grant for prototyping at NIDHI-PRAYAS host institutes."
                ),
                grant_type  = "Startup Grant",
                eligibility = ["Student", "Faculty", "Startup", "Innovator"],
                disciplines = ["Technology", "Biotech", "Engineering", "AI/ML", "Any"],
                amount      = "Up to ₹10 Lakhs",
            ),
            self.build_grant(
                title       = "DST-NIDHI Technology Business Incubator (TBI)",
                url         = "https://www.indiascienceandtechnology.gov.in/listingpage/startup-grants-nidhi-programme",
                deadline    = None,
                description = (
                    "Supports academic institutions in establishing technology business incubators. "
                    "SASTRA could apply to host a TBI. Provides seed funding infrastructure, "
                    "mentorship ecosystem, and connects startups to industry."
                ),
                grant_type  = "Startup Grant",
                eligibility = ["University", "Academic Institution", "R&D Organization"],
                disciplines = ["Technology", "Engineering", "Biotech", "IT"],
                amount      = "Up to ₹3.75 Crores (phased)",
            ),
            self.build_grant(
                title       = "BIRAC Biotechnology Ignition Grant (BIG)",
                url         = "https://birac.nic.in/cfp.php",
                deadline    = None,
                description = (
                    "BIRAC's flagship early-stage support for biotech startups. "
                    "Proof-of-concept funding for innovative biotech ideas. "
                    "Open to individuals and companies. One of the most competitive "
                    "biotech startup grants in India."
                ),
                grant_type  = "Startup Grant",
                eligibility = ["Startup", "Individual Innovator", "Faculty Entrepreneur"],
                disciplines = ["Biotechnology", "MedTech", "AgriTech", "Biopharma"],
                amount      = "Up to ₹50 Lakhs",
            ),
            self.build_grant(
                title       = "BIRAC-SPARSH (Social Innovation Grant)",
                url         = "https://birac.nic.in/cfp.php",
                deadline    = None,
                description = (
                    "BIRAC support for affordable and accessible innovations in healthcare "
                    "and agriculture addressing underserved populations. "
                    "Promotes frugal innovation and social entrepreneurship."
                ),
                grant_type  = "Startup Grant",
                eligibility = ["Startup", "Social Enterprise", "Faculty", "NGO"],
                disciplines = ["Healthcare", "Agriculture", "Biotechnology"],
                amount      = "Up to ₹50 Lakhs",
            ),
            self.build_grant(
                title       = "Startup India Seed Fund Scheme (SISFS)",
                url         = "https://seedfund.startupindia.gov.in/",
                deadline    = None,
                description = (
                    "DPIIT scheme with ₹945 Cr outlay. Grants via eligible incubators for "
                    "proof-of-concept, prototype development, product trials, and market entry. "
                    "Up to ₹20L as grant + up to ₹50L as convertible debentures. "
                    "Disbursed through incubators — SASTRA incubation centre applies."
                ),
                grant_type  = "Startup Grant",
                eligibility = ["DPIIT-recognized Startup (≤2 years)", "via eligible Incubator"],
                disciplines = ["Technology", "Engineering", "Biotech", "AI/ML", "Any"],
                amount      = "Up to ₹20 Lakhs (grant) + ₹50 Lakhs (debenture)",
            ),
            self.build_grant(
                title       = "MeitY TIDE 2.0 (Technology Incubation & Development)",
                url         = "https://www.meity.gov.in/content/tide-20",
                deadline    = None,
                description = (
                    "MeitY Technology Incubation and Development of Entrepreneurs scheme. "
                    "Supports IT/AI/IoT/Cybersecurity/FinTech startups through academic "
                    "incubators. Two tracks: Incubator Support (₹3.15Cr) + Startup Grants."
                ),
                grant_type  = "Startup Grant",
                eligibility = ["Startup (IT/AI focused)", "Academic Incubator Host"],
                disciplines = ["AI/ML", "IoT", "Cybersecurity", "FinTech", "IT"],
                amount      = "Up to ₹25 Lakhs per startup",
            ),
            self.build_grant(
                title       = "ANRF PM Early Career Research Grant — Startup Research",
                url         = "https://anrf.gov.in/en/calls-for-proposals",
                deadline    = None,
                description = (
                    "UGC Start-up Research Grant for newly appointed faculty (within 3 years "
                    "of joining). Available at UGC 2(f)/12B institutions. Covers basic sciences, "
                    "medical sciences, engineering. For establishing independent research."
                ),
                grant_type  = "Startup Grant",
                eligibility = ["Newly appointed Faculty (≤3 years)", "UGC-recognized institution"],
                disciplines = ["Basic Sciences", "Medical Sciences", "Engineering"],
                amount      = "Up to ₹10 Lakhs",
            ),
        ]
