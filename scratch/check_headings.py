import glob
import re

html_files = sorted(glob.glob("docs/**/*.html", recursive=True))
for h in html_files:
    content = open(h, encoding="utf-8").read()
    h_tags = re.findall(r'<h([1-6])[^>]*>(.*?)</h\1>', content, re.DOTALL | re.IGNORECASE)
    print(f"=== {h} ({len(h_tags)} headings) ===")
    prev_level = 0
    for level, text in h_tags:
        lvl = int(level)
        clean_text = re.sub(r'<[^>]+>', '', text).strip()[:40]
        jump = (lvl - prev_level > 1) and (prev_level != 0)
        flag = " [HEADING SKIP WARNING]" if jump else ""
        print(f"  h{lvl}: {clean_text}{flag}")
        prev_level = lvl

