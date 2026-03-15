cd /mnt/d/grantwatch
python3 -c "
with open('scrapers/anrf_scraper.py') as f:
    content = f.read()

# Remove the live scrape block
cut = content.find('        # Live scrape anrfonline.in')
if cut != -1:
    content = content[:cut] + '        return grants\n'
else:
    print('marker not found — check file manually')

with open('scrapers/anrf_scraper.py', 'w') as f:
    f.write(content)
print('done')
"
