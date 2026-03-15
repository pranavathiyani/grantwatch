"""
Grant Watch ⌛ — ANRF Scraper
Portal moved to anrfonline.in (old anrf.gov.in/en/calls-for-proposals is 404)

2026 Schedule confirmed from official ANRF announcement:
  JC Bose Grant        : 01 Jan – 10 Feb 2026
  NPDF                 : 15 Jan – 17 Feb 2026
  ANRF-ATRI            : 15 Jan – 24 Feb 2026
  ARG Pre-Proposals    : 01 Apr – 08 May 2026
  ARG MATRICS          : 01 Apr – 08 May 2026
  NSC                  : 01 Jul – 31 Jul 2026
  ARG Full Proposals   : 15 Sep – 15 Oct 2026
  IRG (new scheme)     : 01 Oct – 03 Nov 2026
  PM ECRG              : 02 Nov – 02 Dec 2026
  Ramanujan Fellowship : Open throughout 2026
"""

import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

ANRF_PORTAL = "https://www.anrfonline.in/"
ANRF_BASE   = "https://anrfonline.in"


class ANRFScraper(BaseScraper):
    AGENCY_NAME    = "ANRF"
    AGENCY_COUNTRY = "India"
    AGENCY_URL     = ANRF_PORTAL

    def scrape(self) -> list:
        grants = [
            self.build_grant(
                title       = "ANRF Advanced Research Grant (ARG) — Pre-Proposals 2026",
                url         = "https://anrfonline.in/ANRF/arg_anrf",
                deadline    = "2026-05-08",
                open_date   = "2026-04-01",
                description = (
                    "ARG subsumes the Core Research Grant (CRG). Supports frontier research "
                    "in Science & Engineering. Pre-proposal Apr 1–May 8 2026; "
                    "Full proposals Sep 15–Oct 15 2026. No upper budget limit."
                ),
                grant_type  = "Research Grant",
                eligibility = ["Faculty", "Researcher", "Indian Institution"],
                disciplines = ["Science", "Engineering", "Technology"],
                amount      = "No upper limit — project-based",
            ),
            self.build_grant(
                title       = "ANRF MATRICS 2026 (Mathematics Research Grant)",
                url         = "https://anrfonline.in/ANRF/arg_anrf",
                deadline    = "2026-05-08",
                open_date   = "2026-04-01",
                description = (
                    "Mathematical Research Impact Centric Support. For active researchers "
                    "in mathematics. Apr 1 – May 8 2026."
                ),
                grant_type  = "Research Grant",
                eligibility = ["Faculty", "Researcher"],
                disciplines = ["Mathematics", "Statistics", "Theoretical Sciences"],
                amount      = "Up to ₹10 Lakhs (3 years)",
            ),
            self.build_grant(
                title       = "ANRF National Postdoctoral Fellowship (N-PDF) 2026",
                url         = "https://anrfonline.in/ANRF/npdf",
                deadline    = "2026-02-17",
                open_date   = "2026-01-15",
                description = (
                    "2-year postdoctoral fellowship. Indian PhD holders age ≤35. "
                    "Work under mentor at any recognised Indian institution."
                ),
                grant_type  = "Fellowship",
                eligibility = ["PhD Holder (≤35 years)", "Indian Citizen"],
                disciplines = ["Science", "Engineering"],
                amount      = "₹55,000/month + HRA + ₹2L research grant",
            ),
            self.build_grant(
                title       = "ANRF Prime Minister Early Career Research Grant (PM-ECRG) 2026",
                url         = "https://anrfonline.in/ANRF/ecrg_anrf",
                deadline    = "2026-12-02",
                open_date   = "2026-11-02",
                description = (
                    "One-time career grant for early-career faculty. Subsumes erstwhile SRG. "
                    "₹60L + overheads for 3 years. Max 700 grants/year."
                ),
                grant_type  = "Research Grant",
                eligibility = ["Early Career Faculty", "Indian Institution"],
                disciplines = ["Science", "Engineering", "Technology"],
                amount      = "₹60 Lakhs + overheads (3 years)",
            ),
            self.build_grant(
                title       = "ANRF Ramanujan Fellowship 2026",
                url         = "https://anrfonline.in/ANRF/Ramanujan_fellowship",
                deadline    = "2026-12-31",
                open_date   = "2026-01-01",
                description = (
                    "For exceptional Indian scientists returning from abroad. "
                    "Open throughout 2026. Decisions announced twice yearly."
                ),
                grant_type  = "Fellowship",
                eligibility = ["Indian Scientist (Overseas/Diaspora)"],
                disciplines = ["Science", "Engineering"],
                amount      = "₹1,35,000/month + research grant (5 years)",
            ),
            self.build_grant(
                title       = "ANRF JC Bose Grant 2026",
                url         = "https://anrfonline.in/ANRF/jcbose",
                deadline    = "2026-02-10",
                open_date   = "2026-01-01",
                description = "For senior researchers (Professor-level). ₹25L/year × 5 years.",
                grant_type  = "Research Grant",
                eligibility = ["Professor/Senior Researcher", "Indian Institution"],
                disciplines = ["Science", "Engineering"],
                amount      = "₹25 Lakhs/year (5 years)",
            ),
            self.build_grant(
                title       = "ANRF Inclusivity Research Grant (IRG) 2026 — New Scheme",
                url         = "https://anrfonline.in/",
                deadline    = "2026-11-03",
                open_date   = "2026-10-01",
                description = "New ANRF scheme 2026. Promotes research inclusion. Oct 1–Nov 3 2026.",
                grant_type  = "Research Grant",
                eligibility = ["Faculty", "Researcher", "Indian Institution"],
                disciplines = ["Any"],
                amount      = "TBA",
            ),
            self.build_grant(
                title       = "ANRF National Science Chair (NSC) 2026",
                url         = "https://anrfonline.in/",
                deadline    = "2026-07-31",
                open_date   = "2026-07-01",
                description = "Prestigious chair for exceptional senior researchers. Jul 2026.",
                grant_type  = "Fellowship",
                eligibility = ["Senior Researcher", "Professor"],
                disciplines = ["Any"],
                amount      = "TBA",
            ),
            self.build_grant(
                title       = "ANRF-ATRI Scheme 2026",
                url         = "https://anrf.gov.in/",
                deadline    = "2026-02-24",
                open_date   = "2026-01-15",
                description = "Call for Proposals Jan 15–Feb 24 2026 (5 PM). See anrf.gov.in.",
                grant_type  = "Research Grant",
                eligibility = ["Faculty", "Researcher"],
                disciplines = ["Science", "Technology"],
                amount      = "Varies",
            ),
            self.build_grant(
                title       = "ANRF TARE (Teachers Associateship for Research Excellence)",
                url         = "https://anrfonline.in/ANRF/tare",
                deadline    = None,
                description = "College teachers work in nearby IIT/IISc/NIT labs. Up to 3 years.",
                grant_type  = "Fellowship",
                eligibility = ["College Teacher", "Assistant Professor"],
                disciplines = ["Science", "Engineering"],
                amount      = "₹10,000/month + research grant",
            ),
            self.build_grant(
                title       = "ANRF International Travel Support (ITS)",
                url         = "https://anrfonline.in/ANRF/its",
                deadline    = None,
                description = "Travel support to present at international conferences. Rolling.",
                grant_type  = "Travel Grant",
                eligibility = ["Faculty", "Researcher", "PhD Student"],
                disciplines = ["Any"],
                amount      = "Up to ₹2 Lakhs",
            ),
        ]

        # Live scrape anrfonline.in for currently open calls
        try:
            resp = requests.get(ANRF_PORTAL, timeout=20,
                                headers={"User-Agent": "Mozilla/5.0"})
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                for link in soup.find_all("a", href=True):
                    href  = link["href"]
                    title = link.get_text(strip=True)
                    if len(title) < 8:
                        continue
                    if not any(k in title.lower() for k in
                               ["call", "open", "grant", "fellowship", "proposal", "scheme"]):
                        continue
                    if not href.startswith("http"):
                        href = ANRF_BASE + href
                    if any(g["url"] == href for g in grants):
                        continue
                    grants.append(self.build_grant(
                        title=title, url=href, deadline=None,
                        description=f"ANRF open call: {title}",
                        grant_type="Research Grant",
                        eligibility=["Faculty", "Researcher"],
                        disciplines=["Science", "Engineering"],
                        amount="Varies",
                    ))
        except Exception as e:
            print(f"  [ANRF live] {e}")

        return grants
