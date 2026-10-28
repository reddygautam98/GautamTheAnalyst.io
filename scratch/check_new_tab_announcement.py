import glob
import os
import re

docs_dir = os.path.abspath("docs")
html_files = sorted(glob.glob(os.path.join(docs_dir, "**/*.html"), recursive=True))

sr_missing = []

for hf in html_files:
    rel = os.path.relpath(hf, docs_dir)
    content = open(hf, encoding="utf-8").read()
    
    # find all <a>...</a> tags with target="_blank"
    # Matches <a ...target="_blank"...>...</a>
    pattern = re.compile(r'<a\s+[^>]*target=["\']_blank["\'][^>]*>(.*?)</a>', re.DOTALL | re.IGNORECASE)
    for m in pattern.finditer(content):
        tag_content = m.group(1)
        full_tag = m.group(0)
        # Check if sr-only or aria-label exists
        if "opens in new tab" not in tag_content.lower() and "opens in new tab" not in full_tag.lower():
            sr_missing.append({"page": rel, "link": full_tag[:120]})

print(f"Total target='_blank' links missing 'opens in new tab': {len(sr_missing)}")
for issue in sr_missing:
    print(issue)

