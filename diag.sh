cd /mnt/d/grantwatch
python3 -c "
import json
from collections import Counter

with open('data/grants.json') as f:
    grants = json.load(f)

print(f'Total: {len(grants)}')
print()

# Show all agencies and counts
agency_counts = Counter(g['agency'] for g in grants)
print('=== ALL AGENCIES ===')
for agency, count in sorted(agency_counts.items()):
    print(f'  {count:3d}  {agency}')

print()
print('=== VARIOUS* ENTRIES ===')
for g in grants:
    if g['agency'].startswith('Various') or g['agency'] == 'Various':
        print(f'  [{g[\"agency\"]}] {g[\"grant_type\"]:20} | {g[\"title\"][:70]}')

print()
print('=== DUPLICATE TITLES (same title, different IDs) ===')
from collections import defaultdict
by_title = defaultdict(list)
for g in grants:
    by_title[g['title'].lower().strip()].append(g['agency'])
for title, agencies in by_title.items():
    if len(agencies) > 1:
        print(f'  {agencies} | {title[:70]}')
"
