import os
import re
import glob

DOCS_DIR = os.path.abspath("docs")
html_files = glob.glob(os.path.join(DOCS_DIR, "**/*.html"), recursive=True)

page_ids = {}
for hf in html_files:
    rel = os.path.relpath(hf, DOCS_DIR).replace("\\", "/")
    content = open(hf, encoding="utf-8").read()
    page_ids[rel] = set(re.findall(r'id=["\']([^"\']+)["\']', content))

broken = []
for hf in html_files:
    rel = os.path.relpath(hf, DOCS_DIR).replace("\\", "/")
    page_dir = os.path.dirname(hf)
    content = open(hf, encoding="utf-8").read()
    
    # find all hrefs
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', content)
    for h in hrefs:
        if not h or h.startswith("http") or h.startswith("mailto:") or h.startswith("tel:") or h.startswith("javascript:"):
            continue
        if "#" in h:
            path_part, anchor = h.split("#", 1)
            if not path_part:
                # internal anchor
                if anchor not in page_ids[rel]:
                    broken.append((rel, h, f"Internal anchor #{anchor} missing in {rel}"))
            else:
                clean_path = path_part.split("?")[0]
                target_full = os.path.normpath(os.path.join(page_dir, clean_path))
                target_rel = os.path.relpath(target_full, DOCS_DIR).replace("\\", "/")
                if target_rel in page_ids:
                    if anchor not in page_ids[target_rel]:
                        broken.append((rel, h, f"Target anchor #{anchor} missing in {target_rel}"))
                else:
                    broken.append((rel, h, f"Target page {target_rel} not found"))

print(f"Total broken anchor links: {len(broken)}")
for b in broken:
    print(b)

