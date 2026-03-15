cd /mnt/d/grantwatch
python3 -c "
import json
with open('data/grants.json') as f:
    grants = json.load(f)

fixes = {
    'https://anrf.gov.in/en/calls-for-proposals': 'https://anrfonline.in/',
    'https://dbtindia.gov.in/schemes-programmes/research-development/human-resource-development/dbt-jrf': 'https://dbtindia.gov.in/dbt-junior-research-fellowship-jrf-programme',
}

fixed = 0
for g in grants:
    if g.get('url') in fixes:
        print(f'  Fixed: {g[\"title\"][:60]}')
        g['url'] = fixes[g['url']]
        fixed += 1

with open('data/grants.json', 'w') as f:
    json.dump(grants, f, indent=2, ensure_ascii=False)
print(f'Total fixed: {fixed}')
"

# Also fix in the scraper
sed -i 's|anrf.gov.in/en/calls-for-proposals|anrfonline.in/|g' scrapers/anrf_scraper.py

git add .
git commit -m "fix: remove dead ANRF old URL, fix DBT-JRF URL"
git push
