cd /mnt/d/grantwatch

# Create required folders
mkdir -p scrapers data .github/workflows .github/ISSUE_TEMPLATE

# Move scraper files into scrapers/
mv __init__.py scrapers/
mv base_scraper.py scrapers/
mv anrf_scraper.py scrapers/
mv additional_agencies_scrapers.py scrapers/
mv additional_fellowship_scrapers.py scrapers/
mv bilateral_scrapers.py scrapers/
mv csir_icar_birac_scraper.py scrapers/
mv dbt_icmr_scraper.py scrapers/
mv embo_conference_startup_scrapers.py scrapers/
mv fellowship_scrapers.py scrapers/
mv icgeb_scraper.py scrapers/
mv international_scrapers.py scrapers/
mv new_agency_scrapers.py scrapers/
mv nih_scraper.py scrapers/
mv par_indiabioscience_scrapers.py scrapers/
mv travel_grant_scrapers.py scrapers/

# Move data file
mv grants.json data/

# Move GitHub Actions workflows
mv monthly_refresh.yml .github/workflows/
mv daily_check.yml .github/workflows/

# Move issue template
mv submit_grant.yml .github/ISSUE_TEMPLATE/
