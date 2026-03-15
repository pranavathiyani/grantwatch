cd /mnt/d/grantwatch
python3 -c "
import json
with open('data/grants.json') as f:
    grants = json.load(f)

print('=== DST entries ===')
for g in grants:
    if 'DST' in g['agency']:
        print(f'  [{g[\"agency\"]:22}] {g[\"title\"][:70]}')

print()
print('=== DST (Bilateral) entries ===')
for g in grants:
    if g['agency'] == 'DST (Bilateral)':
        print(f'  url: {g[\"url\"][:60]}')
        print(f'  title: {g[\"title\"][:70]}')
        print()
"
