"""
Grant Watch ⌛ — Scraper Registry
All scrapers registered here. Categories clearly marked.
Run: python run_scrapers.py
"""

from .nih_scraper                     import NIHScraper
from .anrf_scraper                    import ANRFScraper
from .dbt_icmr_scraper                import DBTScraper, ICMRScraper
from .csir_icar_birac_scraper         import CSIRScraper, ICARScraper, BIRACScraper
from .international_scrapers          import WellcomeScraper, EMBOScraper, GatesScraper
from .travel_grant_scrapers           import (
    EMBOTravelScraper, DBTTravelScraper,
    CSIRTravelScraper, INSAScraper, FEBSScraper,
)
from .fellowship_scrapers             import (
    ANRFFellowshipScraper, CSIRFellowshipScraper, DBTFellowshipScraper,
    WellcomeFellowshipScraper, EMBLFellowshipScraper, DSTFellowshipScraper,
    ICMRFellowshipScraper, PMRFFellowshipScraper, FulbrightFellowshipScraper,
    HFSPScraper,
)
from .new_agency_scrapers             import UGCScraper, DSTScraper, MeitYScraper, SPARCScraper, IMPRINTScraper
from .par_indiabioscience_scrapers    import PARFoundationScraper, IndiaBioscienceScraper, GitHubTravelGrantsScraper
from .bilateral_scrapers              import BilateralGrantsScraper
from .additional_fellowship_scrapers  import (
    ANRFEarlyCareerScraper, DBTExtendedFellowshipScraper,
    ICMRExtendedScraper, YoungScientistAwardScraper,
)
from .icgeb_scraper                   import ICGEBScraper
from .embo_conference_startup_scrapers import (
    EMBOConferenceScraper, SERBPOWERScraper, StartupGrantsScraper,
)

ALL_SCRAPERS = [
    # ── Indian Research Grants ──────────────────────────────────────────
    ANRFScraper,
    DSTScraper,
    UGCScraper,
    DBTScraper,
    ICMRScraper,
    CSIRScraper,
    ICARScraper,
    BIRACScraper,
    MeitYScraper,
    SPARCScraper,
    IMPRINTScraper,
    SERBPOWERScraper,           # Women researchers — Level I/II (SASTRA = Level II)

    # ── Indian Fellowships ─────────────────────────────────────────────
    ANRFFellowshipScraper,      # N-PDF, Ramanujan, TARE
    ANRFEarlyCareerScraper,     # SRG, PM-ECRG, SIRE, Swarnajayanti
    CSIRFellowshipScraper,      # JRF, SRF, RA
    DBTFellowshipScraper,       # DBT-JRF, Ramalingaswami
    DBTExtendedFellowshipScraper, # DBT-RA, IYBA, BUILDER
    DSTFellowshipScraper,       # INSPIRE Faculty, WOS-A, KVPY
    ICMRFellowshipScraper,      # ICMR-JRF
    ICMRExtendedScraper,        # International Fellowship, ANVESHAN, NISCHA
    PMRFFellowshipScraper,      # Prime Minister Research Fellowship
    YoungScientistAwardScraper, # INSA, NASI, IASc awards

    # ── Indian Travel Grants ───────────────────────────────────────────
    DBTTravelScraper,
    CSIRTravelScraper,
    INSAScraper,

    # ── Indian Startup Grants ──────────────────────────────────────────
    StartupGrantsScraper,       # DST-NIDHI, BIRAC-BIG, SISFS, TIDE 2.0

    # ── Bilateral / Collaborative (Indian PI required) ──────────────────
    BilateralGrantsScraper,     # CEFIPRA, IGSTC, DST-JSPS, ISJRP, Newton-Bhabha, IUSSTF, Indo-Israel, Indo-Korea, Indo-Australia

    # ── International Research Grants (India-eligible) ─────────────────
    NIHScraper,                 # PA, PAR, RFA via RSS
    GatesScraper,
    HFSPScraper,
    PARFoundationScraper,       # AMR — 2026 call live
    ICGEBScraper,               # CRP Apr 30 2026, SMART Mar 31 2026 — India member state

    # ── International Fellowships ──────────────────────────────────────
    WellcomeScraper,
    WellcomeFellowshipScraper,  # Early/Intermediate/Senior
    EMBOScraper,
    EMBLFellowshipScraper,      # EIPOD, PhD Programme
    FulbrightFellowshipScraper, # Postdoc Jul 15 2026, Doctoral Jul 1 2026

    # ── International Conference & Workshop Grants ─────────────────────
    EMBOConferenceScraper,      # Workshop organizing (up to €42,500), EMBL travel, EMBO PostDoc

    # ── International Travel Grants ───────────────────────────────────
    EMBOTravelScraper,
    FEBSScraper,
    GitHubTravelGrantsScraper,  # AdhyaSuman/International_Travel_Grants via GitHub API

    # ── Supplementary Aggregators ──────────────────────────────────────
    IndiaBioscienceScraper,     # indiabioscience.org/grants — ethical scrape
]
from .additional_agencies_scrapers import (
    AICTEScraper, HumboldtScraper, NovoNordiskScraper,
    RoyalSocietyScraper, DAADScraper,
)

# Append to ALL_SCRAPERS
ALL_SCRAPERS += [
    AICTEScraper,       # AICTE-RPS — SASTRA directly eligible, lower competition
    HumboldtScraper,    # Georg Forster + Postdoc + Experienced + Award — all rolling
    NovoNordiskScraper, # NNF Challenge + Data Science — underused by Indian researchers
    RoyalSocietyScraper,# Newton International + International Exchanges
    DAADScraper,        # DAAD research stays, PPP, WISE
]
