cd /mnt/d/grantwatch
python3 -c "
import json
from collections import Counter
with open('data/grants.json') as f:
    grants = json.load(f)
counts = Counter(g['agency'] for g in grants)
for a, c in sorted(counts.items(), key=lambda x: -x[1]):
    print(f'  {c:3d}  {a}')
"
