import glob
import json
import re

html_files = glob.glob("docs/**/*.html", recursive=True)
for h in sorted(html_files):
    content = open(h, encoding="utf-8").read()
    scripts = re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
    for idx, s in enumerate(scripts):
        try:
            parsed = json.loads(s)
            print(f"[{h} ld-json #{idx+1}] Valid JSON-LD: @context={parsed.get('@context')}")
        except Exception as e:
            print(f"[{h} ld-json #{idx+1}] INVALID: {e}")

