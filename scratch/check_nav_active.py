import glob
import os
import re

html_files = glob.glob("docs/**/*.html", recursive=True)
for h in sorted(html_files):
    rel = os.path.relpath(h, "docs")
    content = open(h, encoding="utf-8").read()
    # find nav link with aria-current="page"
    nav_match = re.search(r'<nav[^>]*id="nav"[^>]*>(.*?)</nav>', content, re.DOTALL)
    if nav_match:
        cur_links = re.findall(r'<a\s+[^>]*aria-current="page"[^>]*>(.*?)</a>', nav_match.group(1))
        print(f"[{rel}] Active nav link: {cur_links}")
    else:
        print(f"[{rel}] No #nav found")

