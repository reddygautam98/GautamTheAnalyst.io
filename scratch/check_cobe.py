import re

content = open('docs/assets/cobe.js', 'r', encoding='utf-8').read()
for var in ['ge', 'me', 'ue', 'he']:
    m = re.search(var + r'="([^"]+)"', content)
    if m:
        print(f"{var}: {m.group(1)[:120]}...")
