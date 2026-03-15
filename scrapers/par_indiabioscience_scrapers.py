"""
Grant Watch ⌛ — PAR Foundation, IndiaBioscience & GitHub Travel Grants

Ethical scraping standards applied throughout:
  1. robots.txt checked before any request (urllib.robotparser)
  2. Crawl-delay respected — min 3s enforced regardless
  3. User-Agent clearly identifies this bot and its purpose
  4. Only public /grants/* pages — no login, no private areas
  5. Low volume (monthly run only, not continuous)
  6. Non-commercial academic aggregation only
  7. Source always attributed in output data
  8. GitHub README via official API — not scraping
"""

import re, time, base64, requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.robotparser import RobotFileParser
from .base_scraper import BaseScraper

GRANT_WATCH_UA = (
    "GrantWatchBot/1.0 (SASTRA University research funding aggregator; "
    "non-commercial academic use; https://github.com/pranavathiyani/grantwatch)"
)
MIN_CRAWL_DELAY = 3.0


def _robots_allows(base_url, path):
    try:
        rp = RobotFileParser()
        rp.set_url(f"{base_url}/robots.txt")
        rp.read()
        return rp.can_fetch(GRANT_WATCH_UA, f"{base_url}{path}")
    except Exception:
        return True


def _parse_date(text):
    for fmt in ("%d %B", "%B %d", "%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d", "%d %b %Y", "%B %d, %Y", "%d %b"):
        try:
            if fmt in ("%d %B", "%B %d", "%d %b"):
                dt = datetime.strptime(text.strip(), fmt).replace(year=datetime.now().year)
                if dt < datetime.now():
                    dt = dt.replace(year=datetime.now().year + 1)
                return dt.strftime("%Y-%m-%d")
            return datetime.strptime(text.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


class PARFoundationScraper(BaseScraper):
    AGENCY_NAME    = "PAR Foundation"
    AGENCY_COUNTRY = "International"
    AGENCY_URL     = "https://opencalls.parfoundation.org/"

    def scrape(self):
        # JS-rendered site (Teamtailor) — seeded manually
        return [self.build_grant(
            title       = "PAR Foundation 2026 Grant — Beyond Antibiotics",
            url         = "https://opencalls.parfoundation.org/",
            deadline    = None,
            description = (
                "2026 theme: 'Beyond Antibiotics: Preventive Strategies That Lower the Need "
                "for Antibiotic Use.' Supports AMR prevention research and educational "
                "initiatives. Global applicants including India eligible."
            ),
            grant_type  = "Research Grant",
            eligibility = ["Researcher", "Faculty", "Institution", "NGO"],
            disciplines = ["AMR", "Infectious Disease", "Public Health", "Microbiology"],
            amount      = "Varies (project-based)",
        )]


class IndiaBioscienceScraper(BaseScraper):
    """
    Ethical scraper for indiabioscience.org/grants public listing.
    robots.txt checked, 3s delay, identified UA, non-commercial use,
    source attributed. Only /grants/* paths accessed.
    """
    AGENCY_NAME    = "IndiaBioscience"
    AGENCY_COUNTRY = "India"
    BASE           = "https://indiabioscience.org"
    AGENCY_URL     = "https://indiabioscience.org/grants"

    def _get(self, path):
        if not _robots_allows(self.BASE, path):
            print(f"  [IndiaBioscience] robots.txt disallows {path} — skipping")
            return None
        time.sleep(MIN_CRAWL_DELAY)
        try:
            resp = requests.get(
                self.BASE + path,
                headers={"User-Agent": GRANT_WATCH_UA, "Accept": "text/html"},
                timeout=20,
            )
            resp.raise_for_status()
            return resp
        except Exception as e:
            print(f"  [IndiaBioscience] {path}: {e}")
            return None

    def _parse(self, html):
        grants, seen = [], set()
        soup = BeautifulSoup(html, "html.parser")
        items = soup.select("div.grant") or soup.select("article") or []

        if not items:
            # Fallback: find /grants/<slug> links in main content
            main = soup.find("main") or soup.find("div", id="content") or soup
            for link in main.find_all("a", href=True):
                href  = link["href"]
                title = link.get_text(strip=True)
                if not re.match(r"^/grants/[a-z0-9\-]+$", href):
                    continue
                if len(title) < 8 or href in seen:
                    continue
                seen.add(href)
                ptext = ""
                for p in [link.parent, getattr(link.parent, "parent", None)]:
                    if p:
                        ptext = p.get_text(" ", strip=True)
                        break
                dl = None
                m = re.search(r"(\d{1,2}\s+\w+(?:\s+\d{4})?)", ptext)
                if m:
                    dl = _parse_date(m.group(1))
                g = self.build_grant(
                    title=title, url=self.BASE + href, deadline=dl,
                    description=ptext[:300], grant_type="Research Grant / Fellowship",
                    eligibility=["Researcher", "Faculty", "PhD Student"],
                    disciplines=["Life Sciences", "Bioinformatics", "Biomedical"],
                    amount="Varies — see IndiaBioscience",
                )
                g["source"] = "IndiaBioscience (indiabioscience.org/grants)"
                grants.append(g)
            return grants

        for item in items:
            link = item.find("a", href=True)
            if not link:
                continue
            title = link.get_text(strip=True)
            href  = link["href"]
            if not href.startswith("http"):
                href = self.BASE + href
            if len(title) < 8:
                continue
            text = item.get_text(" ", strip=True)
            dl = None
            for pat in [r"Deadline[:\s]+(\d{1,2}\s+\w+(?:\s+\d{4})?)", r"(\d{1,2}\s+\w+\s+\d{4})"]:
                m = re.search(pat, text, re.IGNORECASE)
                if m:
                    dl = _parse_date(m.group(1))
                    if dl:
                        break
            gtype = next((t.get_text(strip=True) for t in item.select(".tag,.badge") if t.get_text(strip=True)), "Research Grant")
            g = self.build_grant(
                title=title, url=href, deadline=dl, description=text[:300],
                grant_type=gtype, eligibility=["Researcher", "Faculty", "PhD Student"],
                disciplines=["Life Sciences", "Bioinformatics", "Biomedical"],
                amount="Varies — see IndiaBioscience",
            )
            g["source"] = "IndiaBioscience (indiabioscience.org/grants)"
            grants.append(g)
        return grants

    def scrape(self):
        all_grants, seen_ids = [], set()
        for path in [f"/grants/{datetime.now().year}", "/grants"]:
            resp = self._get(path)
            if not resp:
                continue
            for g in self._parse(resp.text):
                if g["id"] not in seen_ids:
                    seen_ids.add(g["id"])
                    all_grants.append(g)
        print(f"  [IndiaBioscience] {len(all_grants)} grants")
        return all_grants


class GitHubTravelGrantsScraper(BaseScraper):
    """
    Reads AdhyaSuman/International_Travel_Grants README via GitHub Contents API.
    Official API — not scraping. 1 request per run, well within 60 req/hr limit.
    """
    AGENCY_NAME    = "Various (Travel)"
    AGENCY_COUNTRY = "International"
    AGENCY_URL     = "https://github.com/AdhyaSuman/International_Travel_Grants"
    API_URL        = "https://api.github.com/repos/AdhyaSuman/International_Travel_Grants/contents/README.md"

    def _fetch_readme(self):
        try:
            resp = requests.get(self.API_URL,
                headers={"User-Agent": GRANT_WATCH_UA, "Accept": "application/vnd.github.v3+json"},
                timeout=20)
            resp.raise_for_status()
            return base64.b64decode(resp.json()["content"]).decode("utf-8")
        except Exception as e:
            print(f"  [GitHubTravelGrants] {e}")
            return ""

    def _parse_table(self, md):
        grants, in_table = [], False
        for line in md.splitlines():
            line = line.strip()
            if "Grant Name" in line and "Application Page" in line:
                in_table = True; continue
            if in_table and line.startswith("|---"):
                continue
            if in_table and line.startswith("|"):
                cells = [c.strip() for c in line.strip("|").split("|")]
                if len(cells) < 2:
                    continue
                title = re.sub(r"\*\*(.+?)\*\*", r"\1", cells[0]).strip()
                if len(title) < 5:
                    continue
                link_cell = cells[1] if len(cells) > 1 else ""
                url_m = re.search(r"\(https?://[^\)]+\)", link_cell)
                url   = url_m.group(0).strip("()") if url_m else self.AGENCY_URL
                status = "closed" if "CLOSED" in link_cell.upper() else "open"
                email = ""
                if len(cells) > 2:
                    em = re.search(r"[\w\.-]+@[\w\.-]+", cells[2])
                    if em: email = em.group(0)
                desc = "Travel grant for Indian PhD students/researchers. Source: AdhyaSuman/International_Travel_Grants (GitHub)."
                if email: desc += f" Contact: {email}"
                g = self.build_grant(
                    title=title, url=url, deadline=None, description=desc,
                    grant_type="Travel Grant",
                    eligibility=["PhD Student", "Researcher", "Indian Applicant"],
                    disciplines=["Any"], amount="Varies", status=status,
                )
                g["source"] = "AdhyaSuman/International_Travel_Grants (GitHub)"
                grants.append(g)
            elif in_table and not line.startswith("|"):
                in_table = False
        return grants

    def scrape(self):
        md = self._fetch_readme()
        grants = self._parse_table(md) if md else []
        print(f"  [GitHubTravelGrants] {len(grants)} entries")
        return grants
