import glob
import re

for h in ["docs/services.html", "docs/samples/index.html", "docs/projects.html", "docs/index.html"]:
    content = open(h, encoding="utf-8").read()
    lines = content.splitlines()
    for idx, line in enumerate(lines):
        matches = list(re.finditer(r'&(?!(?:[a-zA-Z0-9]+|#[0-9]+|#x[0-9a-fA-F]+);)', line))
        if matches:
            for m in matches:
                start = max(0, m.start() - 25)
                end = min(len(line), m.end() + 25)
                print(f"[{h}:{idx+1}] ...{line[start:end]}...")

