cd /mnt/d/grantwatch
python3 -c "
import json
with open('data/grants.json') as f:
    grants = json.load(f)

before = len(grants)

# Remove NIH RSS-pulled entries that are not India-relevant
# Keep: Fogarty, our 2 seeded R01/R21 entries
# Remove: anything with 'NOT-' (notices), vague titles, training-only
keep_nih = []
remove_nih = []

for g in grants:
    if g['agency'] not in ('NIH', 'NIH Fogarty'):
        keep_nih.append(g)
        continue
    title = g['title']
    # Remove administrative notices and non-applicable types
    if any(x in title for x in ['NOT-', 'Notice', 'Policy', 'Training', 'NRSA',
                                  'Fellowship Program Announcement', 'Loan Repayment',
                                  'Supplement', 'Revision', 'Resubmission']):
        remove_nih.append(title)
        continue
    keep_nih.append(g)

print(f'Before: {before}')
print(f'Removed {before - len(keep_nih)} NIH noise entries:')
for t in remove_nih:
    print(f'  - {t[:80]}')

with open('data/grants.json', 'w') as f:
    json.dump(keep_nih, f, indent=2, ensure_ascii=False)
print(f'After: {len(keep_nih)}')
"
