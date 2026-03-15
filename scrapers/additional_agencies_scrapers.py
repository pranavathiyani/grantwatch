"""
Grant Watch ⌛ — AICTE, Humboldt, Novo Nordisk, Royal Society, DAAD

AICTE-RPS  : Research Promotion Scheme — AICTE-approved institutions only
             SASTRA is AICTE-approved → lower competition than DST/DBT
Humboldt   : Georg Forster (developing countries), Research Fellowship,
             Experienced Researcher Fellowship — all India-eligible
Novo Nordisk: Open Life Science calls, Data Science Challenge,
              some India-specific — underused by Indian researchers
Royal Society: Newton International, International Exchanges (seed £12k)
DAAD       : Indo-German exchange, PPP, WISE scholarship for women
"""

from .base_scraper import BaseScraper


# ─────────────────────────────────────────────
# AICTE Research Promotion Scheme
# ─────────────────────────────────────────────
class AICTEScraper(BaseScraper):
    """
    AICTE-RPS is specifically for AICTE-approved institutions.
    SASTRA (Deemed University) is AICTE-approved → this is directly eligible
    and less competitive than DST/DBT because many researchers don't realise it.
    """
    AGENCY_NAME    = "AICTE"
    AGENCY_COUNTRY = "India"
    AGENCY_URL     = "https://www.aicte-india.org/bureaus/research"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "AICTE Research Promotion Scheme (RPS)",
                url         = "https://www.aicte-india.org/bureaus/research/research-promotion-scheme",
                deadline    = None,
                description = (
                    "Promotes research culture in AICTE-approved institutions. Two tracks: "
                    "Basic/Applied Research (₹20L, 2yr) and Development Research (₹30L, 3yr). "
                    "Less competitive than DST/DBT — underutilised by faculty at deemed universities. "
                    "SASTRA is directly eligible. Submit via AICTE web portal."
                ),
                grant_type  = "Research Grant",
                eligibility = ["Faculty at AICTE-approved Institution", "Regular position"],
                disciplines = ["Engineering", "Technology", "Applied Sciences",
                               "Computer Science", "Biotechnology", "Any AICTE discipline"],
                amount      = "Up to ₹30 Lakhs (Development Research track)",
            ),
            self.build_grant(
                title       = "AICTE Margdarshan — Faculty Development Grant",
                url         = "https://www.aicte-india.org",
                deadline    = None,
                description = (
                    "AICTE faculty development and capacity building grants. Covers short-term "
                    "courses, workshops, and training programmes at premier institutions. "
                    "Also includes Quality Improvement Programme (QIP) support."
                ),
                grant_type  = "Faculty Development Grant",
                eligibility = ["Faculty at AICTE-approved Institution"],
                disciplines = ["Engineering", "Technology", "Management"],
                amount      = "Varies by programme",
            ),
            self.build_grant(
                title       = "AICTE-INAE (Indian National Academy of Engineering) Research Grant",
                url         = "https://www.aicte-india.org",
                deadline    = None,
                description = (
                    "Joint AICTE-INAE scheme for frontier engineering research. "
                    "Includes Young Engineer Award track with research support. "
                    "For engineering disciplines at AICTE institutions."
                ),
                grant_type  = "Research Grant",
                eligibility = ["Faculty", "Young Engineer (under 32)", "AICTE Institution"],
                disciplines = ["Engineering", "Technology", "Computer Science"],
                amount      = "Varies",
            ),
        ]


# ─────────────────────────────────────────────
# Alexander von Humboldt Foundation
# ─────────────────────────────────────────────
class HumboldtScraper(BaseScraper):
    """
    AvH explicitly targets researchers from developing countries.
    Georg Forster Fellowship is India-specific in practice.
    Rolling deadlines — apply anytime.
    """
    AGENCY_NAME    = "Alexander von Humboldt Foundation"
    AGENCY_COUNTRY = "International"
    AGENCY_URL     = "https://www.humboldt-foundation.de/en/apply"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "Georg Forster Research Fellowship (AvH) — India-eligible",
                url         = "https://www.humboldt-foundation.de/en/apply/sponsorship-programmes/georg-forster-research-fellowship",
                deadline    = None,   # rolling — apply anytime
                description = (
                    "For researchers from developing/transition countries (incl. India) to "
                    "conduct research in Germany for 6–24 months. All disciplines. Highly "
                    "prestigious. Rolling deadline — no fixed call. Strong publication record needed. "
                    "Covers salary, travel, family allowance."
                ),
                grant_type  = "Fellowship",
                eligibility = ["PhD Holder", "Indian Researcher", "Strong publication record"],
                disciplines = ["Any — all disciplines eligible"],
                amount      = "€2,670–3,170/month + travel + family allowance",
            ),
            self.build_grant(
                title       = "Humboldt Research Fellowship for Postdoctoral Researchers",
                url         = "https://www.humboldt-foundation.de/en/apply/sponsorship-programmes/humboldt-research-fellowship",
                deadline    = None,
                description = (
                    "6–24 months at a German university/research institution. "
                    "Open to Indian researchers with PhD ≤4 years. Any discipline. "
                    "Rolling deadline — apply anytime. One of the most prestigious "
                    "postdoc fellowships worldwide."
                ),
                grant_type  = "Fellowship",
                eligibility = ["Postdoc (PhD ≤4 years)", "Indian Researcher"],
                disciplines = ["Any"],
                amount      = "€2,670/month + travel + health insurance",
            ),
            self.build_grant(
                title       = "Humboldt Research Fellowship for Experienced Researchers",
                url         = "https://www.humboldt-foundation.de/en/apply/sponsorship-programmes/humboldt-research-fellowship",
                deadline    = None,
                description = (
                    "For senior researchers (>4 years post-PhD) to work in Germany for "
                    "6–18 months. All disciplines. Highly prestigious. Can be split visits. "
                    "India has one of the highest success rates globally."
                ),
                grant_type  = "Fellowship",
                eligibility = ["Senior Researcher (PhD >4 years)", "Indian Researcher"],
                disciplines = ["Any"],
                amount      = "€3,170/month + travel + family allowance",
            ),
            self.build_grant(
                title       = "Humboldt Research Award",
                url         = "https://www.humboldt-foundation.de/en/apply/sponsorship-programmes/humboldt-research-award",
                deadline    = None,
                description = (
                    "Prestigious award for internationally recognised researchers in any discipline. "
                    "Nominated by German academics — cannot self-apply. Carries €60,000 prize "
                    "and extended research stay in Germany."
                ),
                grant_type  = "Award",
                eligibility = ["Senior Researcher (nominated by German colleague)"],
                disciplines = ["Any"],
                amount      = "€60,000 + extended Germany visit",
            ),
        ]


# ─────────────────────────────────────────────
# Novo Nordisk Foundation
# ─────────────────────────────────────────────
class NovoNordiskScraper(BaseScraper):
    """
    NNF is underused by Indian researchers. Life sciences + data science.
    Some calls explicitly open globally including India.
    """
    AGENCY_NAME    = "Novo Nordisk Foundation"
    AGENCY_COUNTRY = "International"
    AGENCY_URL     = "https://novonordiskfonden.dk/en/grants/"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "Novo Nordisk Foundation Challenge Programme — Open Call",
                url         = "https://novonordiskfonden.dk/en/grants/",
                deadline    = None,
                description = (
                    "NNF Challenge Programmes tackle specific global health/life science problems. "
                    "Some calls explicitly open to international (including Indian) collaborators. "
                    "Focus areas: infectious disease, antimicrobial resistance, metabolic disease, "
                    "data science for health. Check current open calls."
                ),
                grant_type  = "Research Grant",
                eligibility = ["Faculty", "Researcher", "International Applicant"],
                disciplines = ["Life Sciences", "AMR", "Data Science", "Metabolic Disease",
                               "Infectious Disease", "Bioinformatics"],
                amount      = "Varies by call (up to DKK millions)",
            ),
            self.build_grant(
                title       = "NNF Data Science Research Infrastructure Grant",
                url         = "https://novonordiskfonden.dk/en/grants/",
                deadline    = None,
                description = (
                    "Supports computational biology, bioinformatics, and data science "
                    "research infrastructure. Increasingly open to global collaborations. "
                    "India-based researchers with Danish collaborators are eligible."
                ),
                grant_type  = "Research Grant",
                eligibility = ["Researcher", "Faculty", "with Danish collaborator"],
                disciplines = ["Data Science", "Computational Biology", "Bioinformatics", "AI/ML"],
                amount      = "Varies",
            ),
        ]


# ─────────────────────────────────────────────
# Royal Society (UK)
# ─────────────────────────────────────────────
class RoyalSocietyScraper(BaseScraper):
    """
    RS Newton International Fellowships and International Exchanges
    are India-eligible and underutilised.
    """
    AGENCY_NAME    = "Royal Society"
    AGENCY_COUNTRY = "International"
    AGENCY_URL     = "https://royalsociety.org/grants-schemes-awards/"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "Royal Society Newton International Fellowship",
                url         = "https://royalsociety.org/grants-schemes-awards/grants/newton-international/",
                deadline    = None,   # annual call, typically ~Feb
                description = (
                    "2-year fellowship for early career non-UK researchers to work at UK "
                    "institutions. All disciplines. India-eligible. Strong career development — "
                    "alumni network is highly connected. Annual call."
                ),
                grant_type  = "Fellowship",
                eligibility = ["Early Career Researcher (PhD ≤7 years)", "Non-UK national", "Indian Researcher"],
                disciplines = ["Any — all disciplines"],
                amount      = "£33,000/year salary + £14,500 research expenses (2 years)",
            ),
            self.build_grant(
                title       = "Royal Society International Exchanges — Cost Share",
                url         = "https://royalsociety.org/grants-schemes-awards/grants/international-exchanges/",
                deadline    = None,
                description = (
                    "Seed funding for new collaborations between UK and international researchers. "
                    "India participates in the Cost Share scheme (funded by both RS and Indian agency). "
                    "Covers short visits and workshops up to £12,000. Rolling deadline."
                ),
                grant_type  = "Collaborative Grant",
                eligibility = ["Faculty", "Researcher", "with UK collaborator"],
                disciplines = ["Any — STEM focus"],
                amount      = "Up to £12,000",
            ),
        ]


# ─────────────────────────────────────────────
# DAAD — German Academic Exchange Service
# ─────────────────────────────────────────────
class DAADScraper(BaseScraper):
    """
    DAAD has India-specific programmes. DST-DAAD PPP is a major bilateral channel.
    WISE scholarship for women researchers is especially notable.
    """
    AGENCY_NAME    = "DAAD"
    AGENCY_COUNTRY = "International"
    AGENCY_URL     = "https://www.daad.in/en/"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "DAAD Research Stays for University Academics (India)",
                url         = "https://www.daad.in/en/find-funding/scholarship-database/",
                deadline    = None,
                description = (
                    "Short research stays (1–3 months) at German universities for Indian faculty. "
                    "Covers travel and accommodation. No age limit. "
                    "Also includes bilateral exchange for PhD students."
                ),
                grant_type  = "Travel Grant",
                eligibility = ["Faculty", "Senior Researcher", "Indian Institution"],
                disciplines = ["Any"],
                amount      = "Monthly allowance + travel (as per DAAD norms)",
            ),
            self.build_grant(
                title       = "DST-DAAD Personnel Exchange Programme (PPP) — Indo-German",
                url         = "https://www.daad.in/en/find-funding/scholarship-database/",
                deadline    = None,
                description = (
                    "Bilateral MoU between DAAD and DST. Supports researcher exchanges for "
                    "joint research projects. Indian PI applies to DST; German PI to DAAD. "
                    "Covers travel + per diem for both teams. Well-established channel."
                ),
                grant_type  = "Collaborative Grant",
                eligibility = ["Faculty (Indian PI)", "German Co-PI required"],
                disciplines = ["Science", "Engineering", "Technology", "Any STEM"],
                amount      = "Travel + per diem (DST norms for Indian side)",
            ),
            self.build_grant(
                title       = "DAAD WISE Scholarship (Women in STEM)",
                url         = "https://www.daad.in/en/find-funding/scholarship-database/wise/",
                deadline    = None,
                description = (
                    "For women engineering/science students from India for summer internships "
                    "at top German universities. Highly competitive, well-regarded. "
                    "Also increases visibility for follow-on collaborations."
                ),
                grant_type  = "Fellowship",
                eligibility = ["Women Engineering/Science Student (penultimate year)", "Indian"],
                disciplines = ["Engineering", "Natural Sciences", "Computer Science"],
                amount      = "€650/month + travel support",
            ),
        ]
