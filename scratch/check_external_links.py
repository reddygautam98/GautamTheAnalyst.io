import glob
import os
from bs4 import BeautifulSoup

docs_dir = os.path.abspath("docs")
html_files = sorted(glob.glob(os.path.join(docs_dir, "**/*.html"), recursive=True))

target_blank_issues = []

for hf in html_files:
    rel = os.path.relpath(hf, docs_dir)
    with open(hf, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        
    for a in soup.find_all("a", target="_blank"):
        rel_attr = a.get("rel")
        if not rel_attr or "noopener" not in rel_attr or "noreferrer" not in rel_attr:
            target_blank_issues.append({"page": rel, "link": str(a)[:80], "issue": "Missing rel='noopener noreferrer'"})
        sr = a.find(class_="sr-only")
        if not sr or "new tab" not in sr.text.lower():
            target_blank_issues.append({"page": rel, "link": str(a)[:80], "issue": "Missing accessible (opens in new tab) indicator"})

print(f"Total target='_blank' issues: {len(target_blank_issues)}")
for issue in target_blank_issues:
    print(issue)
