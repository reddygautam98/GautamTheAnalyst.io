import re

content = open("docs/build.py", encoding="utf-8").read()
lines = content.splitlines()
print("Searching build.py for raw '&' in HTML strings:")
for idx, line in enumerate(lines):
    # Check for & not part of &amp; &rarr; etc
    matches = list(re.finditer(r'&(?!(?:[a-zA-Z0-9]+|#[0-9]+|#x[0-9a-fA-F]+);)', line))
    if matches and ('<' in line or 'f\'' in line or 'f"' in line or 'FONTS' in line or 'MARQ' in line):
        print(f"  Line {idx+1}: {line.strip()[:100]}")

