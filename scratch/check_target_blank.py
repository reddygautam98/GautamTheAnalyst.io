import glob
import os
import re

docs_dir = os.path.abspath("docs")
html_files = sorted(glob.glob(os.path.join(docs_dir, "**/*.html"), recursive=True))

target_blank_issues = []

for hf in html_files:
    rel = os.path.relpath(hf, docs_dir)
    content = open(hf, encoding="utf-8").read()
    
    # find all <a ...> tags
    a_tags = re.findall(r'<a\s+[^>]*target=["\']_blank["\'][^>]*>', content, re.IGNORECASE)
    for tag in a_tags:
        rel_match = re.search(r'rel=["\']([^"\']+)["\']', tag, re.IGNORECASE)
        if not rel_match or "noopener" not in rel_match.group(1) or "noreferrer" not in rel_match.group(1):
            target_blank_issues.append({"page": rel, "tag": tag, "issue": "Missing rel='noopener noreferrer'"})

print(f"Total target='_blank' issues: {len(target_blank_issues)}")
for issue in target_blank_issues:
    print(issue)

