import glob
import os
import re

html_files = glob.glob("docs/**/*.html", recursive=True)
for h in html_files:
    content = open(h, encoding="utf-8").read()
    has_skip = 'href="#main"' in content
    has_main_id = 'id="main"' in content
    print(os.path.basename(h), f"Skip link: {has_skip}, #main ID: {has_main_id}")

