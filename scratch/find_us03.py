import re

for f in ["docs/build.py", "docs/index.html"]:
    content = open(f, encoding="utf-8").read()
    lines = content.splitlines()
    for idx, l in enumerate(lines):
        if 'US-03' in l and 'id=' in l:
            print(f"{f}:{idx+1}: {l.strip()}")

