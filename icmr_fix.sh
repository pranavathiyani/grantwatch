cd /mnt/d/grantwatch

# Fix URLs in the scraper
sed -i 's|icmr.gov.in/call-for-applications|icmr.gov.in/extramural-grants|g' scrapers/dbt_icmr_scraper.py

# Fix in grants.json too (live data)
python3 -c "
import json
with open('data/grants.json') as f:
    grants = json.load(f)
fixed = 0
for g in grants:
    if g.get('url') == 'https://icmr.gov.in/call-for-applications':
        g['url'] = 'https://icmr.gov.in/extramural-grants'
        fixed += 1
with open('data/grants.json', 'w') as f:
    json.dump(grants, f, indent=2, ensure_ascii=False)
print(f'Fixed {fixed} ICMR URLs')
"

git add scrapers/dbt_icmr_scraper.py data/grants.json
git commit -m "fix: ICMR URLs — extramural-grants not call-for-applications (404)"
git push
