import re

for filename in ["docs/services.html", "docs/about.html"]:
    content = open(filename, encoding="utf-8").read()
    lines = content.splitlines()
    print(f"=== {filename} ===")
    for idx, line in enumerate(lines):
        # find & not part of entity
        matches = list(re.finditer(r'&(?!(?:[a-zA-Z0-9]+|#[0-9]+|#x[0-9a-fA-F]+);)', line))
        if matches:
            for m in matches:
                start = max(0, m.start() - 20)
                end = min(len(line), m.end() + 20)
                print(f"  Line {idx+1}: ...{line[start:end]}...")

