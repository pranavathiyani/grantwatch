python3 -c "
import json, urllib.request
with open('data/grants.json') as f:
    grants = json.load(f)

# Just show unique URLs per agency so you can spot-check
from collections import defaultdict
urls = defaultdict(set)
for g in grants:
    urls[g['agency']].add(g['url'])
for agency, us in sorted(urls.items()):
    for u in sorted(us):
        print(f'  {agency:25} {u}')
" | head -60
