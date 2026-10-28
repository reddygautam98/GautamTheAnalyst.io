import re

content = open("docs/samples/index.html", encoding="utf-8").read()
ids = set(re.findall(r'id=["\']([^"\']+)["\']', content))

targets = ['brd', 'user-stories', 'rtm', 'process-flow', 'rest-api', 'uat', 'sql', 'power-bi', 'discovery']
for t in targets:
    print(f"{t}: {'FOUND' if t in ids else 'MISSING'}")

