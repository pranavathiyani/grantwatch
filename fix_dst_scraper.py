#!/usr/bin/env python3
"""
Grant Watch ⌛ — Fix DST scraper permanently
Run: python fix_dst_scraper.py

Removes the live HTML scrape from DSTScraper (the noise source)
and adds remaining useful DST schemes as curated entries.
"""

import re, subprocess
from pathlib import Path

ROOT     = Path(__file__).parent
SCRAPERS = ROOT / "scrapers"

path = SCRAPERS / "new_agency_scrapers.py"
content = path.read_text(encoding='utf-8')

# Find DSTScraper class and replace entirely
old_pattern = re.search(
    r'class DSTScraper\(BaseScraper\):.*?(?=\nclass |\Z)',
    content, re.DOTALL
)

if not old_pattern:
    print("⚠ DSTScraper not found in new_agency_scrapers.py")
    exit(1)

NEW_DST = '''class DSTScraper(BaseScraper):
    """
    Curated — DST website mixes navigation links with actual calls.
    Live scraping pulled entries like "Schemes/Programmes", "Archive
    Call For Proposals" etc. Replaced with curated standing schemes.
    DSTFellowshipScraper (fellowship_scrapers.py) handles INSPIRE/WOS-A/KVPY.
    """
    AGENCY_NAME    = "DST"
    AGENCY_COUNTRY = "India"
    AGENCY_URL     = "https://dst.gov.in/call-for-proposals"

    def scrape(self) -> list:
        return [
            self.build_grant(
                title       = "DST-FIST (Fund for Improvement of S&T Infrastructure)",
                url         = "https://dst.gov.in/scientific-programmes/scientific-engineering-research/fist",
                deadline    = None,
                description = "Infrastructure grant for upgrading S&T facilities at universities and colleges. Level I (up to ₹80L) and Level II (up to ₹2Cr). Rolling applications.",
                grant_type  = "Infrastructure Grant",
                eligibility = ["University", "College", "Department"],
                disciplines = ["Science", "Engineering", "Technology"],
                amount      = "Up to ₹2 Crores",
            ),
            self.build_grant(
                title       = "DST-PURSE (Promotion of University Research and Scientific Excellence)",
                url         = "https://dst.gov.in/scientific-programmes/scientific-engineering-research/purse",
                deadline    = None,
                description = "Grants to universities with strong research output to strengthen research infrastructure. Based on publication metrics.",
                grant_type  = "Infrastructure Grant",
                eligibility = ["University with strong research output"],
                disciplines = ["Any"],
                amount      = "Up to ₹5 Crores",
            ),
            self.build_grant(
                title       = "DST Science and Heritage Research Initiative (SHRI)",
                url         = "https://dst.gov.in/call-for-proposals",
                deadline    = None,
                description = "Integrates modern science with India's ancient heritage — astronomy, mathematics, metallurgy, traditional medicine.",
                grant_type  = "Research Grant",
                eligibility = ["Faculty", "Researcher"],
                disciplines = ["Science", "Heritage Studies", "Traditional Knowledge"],
                amount      = "Varies",
            ),
            self.build_grant(
                title       = "DST India-France Call for Proposals (Applied Mathematics & AI)",
                url         = "https://dst.gov.in/international-cooperation/bilateral/france",
                deadline    = None,
                description = "Joint Indo-French call in Applied Mathematics and Artificial Intelligence. Coordinated by DST (India) and ANR (France). Annual call.",
                grant_type  = "Collaborative Grant",
                eligibility = ["Faculty", "Researcher", "French Co-PI required"],
                disciplines = ["Applied Mathematics", "AI/ML", "Computer Science"],
                amount      = "Varies (DST norms for Indian side)",
            ),
            self.build_grant(
                title       = "India-Netherlands Hydrogen Fellowship Programme",
                url         = "https://dst.gov.in/international-cooperation",
                deadline    = None,
                description = "DST-NWO joint programme for researchers working on hydrogen energy technology. India-Netherlands bilateral.",
                grant_type  = "Fellowship",
                eligibility = ["Researcher", "Faculty", "Dutch Co-PI required"],
                disciplines = ["Energy", "Chemistry", "Chemical Engineering"],
                amount      = "Varies",
            ),
            self.build_grant(
                title       = "India Science and Research Fellowship (ISRF) 2025",
                url         = "https://dst.gov.in/call-for-proposals",
                deadline    = None,
                description = "Supports researchers from neighbouring countries (Bangladesh, Nepal, Sri Lanka etc) to visit Indian labs. DST-funded. Annual call.",
                grant_type  = "Fellowship",
                eligibility = ["Researcher from SAARC/neighbouring country"],
                disciplines = ["Science", "Engineering", "Technology"],
                amount      = "As per DST norms",
            ),
            self.build_grant(
                title       = "DST-NIDHI PRAYAS Grant (Proof of Concept)",
                url         = "https://nidhi.dst.gov.in/prayas",
                deadline    = None,
                description = "Seed funding for proof-of-concept for technology startups. Part of DST's NIDHI (National Initiative for Developing and Harnessing Innovations) programme.",
                grant_type  = "Startup Grant",
                eligibility = ["Startup", "Innovator", "Faculty Entrepreneur"],
                disciplines = ["Technology", "Engineering", "Biotechnology", "Any"],
                amount      = "Up to ₹10 Lakhs",
            ),
            self.build_grant(
                title       = "DST-NIDHI Technology Business Incubator (TBI) Support",
                url         = "https://nidhi.dst.gov.in/tbi",
                deadline    = None,
                description = "Supports setting up and strengthening Technology Business Incubators at academic institutions. Funding + mentorship ecosystem.",
                grant_type  = "Infrastructure Grant",
                eligibility = ["University", "Academic Institution"],
                disciplines = ["Technology", "Entrepreneurship", "Any"],
                amount      = "Up to ₹3.75 Crores",
            ),
            self.build_grant(
                title       = "DST SERB-POWER (Promoting Opportunities for Women in Exploratory Research)",
                url         = "https://serb.gov.in/power",
                deadline    = None,
                description = "Research grants for women scientists at Fellow and Accelerate levels. Addresses gender disparity in STEM. Annual call via ANRF/SERB.",
                grant_type  = "Research Grant",
                eligibility = ["Women Researcher", "Faculty"],
                disciplines = ["Science", "Engineering", "Technology"],
                amount      = "₹35–60 Lakhs (3 years)",
            ),
            self.build_grant(
                title       = "DST Scheduled Caste Sub Plan (SCSP) — Mission Projects",
                url         = "https://dst.gov.in/call-for-proposals",
                deadline    = None,
                description = "S&T interventions for SC communities. Research and technology projects that directly benefit scheduled castes.",
                grant_type  = "Research Grant",
                eligibility = ["Faculty", "Researcher", "NGO"],
                disciplines = ["Science", "Technology", "Social Development"],
                amount      = "Varies",
            ),
        ]

'''

content = content[:old_pattern.start()] + NEW_DST + content[old_pattern.end():]
path.write_text(content, encoding='utf-8')
print(f"✓ DSTScraper replaced in {path.name}")
print(f"  Old: live HTML scrape (noise source)")
print(f"  New: 10 curated DST schemes")

# Git commit + push
print("\n=== Git commit + push ===\n")
for cmd in [
    ["git", "add", f"scrapers/{path.name}"],
    ["git", "commit", "-m", "fix: DSTScraper — remove live HTML scrape, curate 10 standing schemes"],
    ["git", "push"],
]:
    print(f"$ {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode != 0:
        print("⚠ Failed")
        break

print("\n✅ Done — DST scraper now permanent. No noise on next cron run.")
print("   Next bi-weekly refresh: DST will show exactly 10 curated entries")
print("   + 3 from DSTFellowshipScraper (INSPIRE, WOS-A, KVPY) = 13 total DST")
