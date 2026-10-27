import glob
import re
import os
from bs4 import BeautifulSoup

docs_dir = os.path.abspath("docs")
html_files = glob.glob(os.path.join(docs_dir, "**/*.html"), recursive=True)

broken_assets = []
broken_anchors = []

for hf in html_files:
    rel_page = os.path.relpath(hf, docs_dir)
    with open(hf, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        
    page_dir = os.path.dirname(hf)
    
    # 1. Check all elements with href
    for el in soup.find_all(href=True):
        href = el["href"]
        if not href or href.startswith("http") or href.startswith("mailto:") or href.startswith("tel:") or href.startswith("javascript:"):
            continue
        if href.startswith("#"):
            target_id = href[1:]
            if target_id and not soup.find(id=target_id) and not soup.find(attrs={"name": target_id}):
                broken_anchors.append({"page": rel_page, "anchor": href, "tag": str(el)[:80]})
        else:
            clean_href = href.split("?")[0].split("#")[0]
            target_path = os.path.normpath(os.path.join(page_dir, clean_href))
            if not os.path.exists(target_path):
                broken_assets.append({"page": rel_page, "href": href, "resolved": target_path, "tag": str(el)[:80]})

    # 2. Check all elements with src
    for el in soup.find_all(src=True):
        src = el["src"]
        if not src or src.startswith("http") or src.startswith("data:"):
            continue
        clean_src = src.split("?")[0].split("#")[0]
        target_path = os.path.normpath(os.path.join(page_dir, clean_src))
        if not os.path.exists(target_path):
            broken_assets.append({"page": rel_page, "src": src, "resolved": target_path, "tag": str(el)[:80]})

    # 3. Check data-full attributes (used by lightbox/zoom)
    for el in soup.find_all(attrs={"data-full": True}):
        df = el["data-full"]
        if not df or df.startswith("http") or df.startswith("data:"):
            continue
        clean_df = df.split("?")[0].split("#")[0]
        target_path = os.path.normpath(os.path.join(page_dir, clean_df))
        if not os.path.exists(target_path):
            broken_assets.append({"page": rel_page, "data-full": df, "resolved": target_path, "tag": str(el)[:80]})

print(f"Total broken assets: {len(broken_assets)}")
for b in broken_assets:
    print(" ", b)

print(f"Total broken in-page anchors: {len(broken_anchors)}")
for a in broken_anchors:
    print(" ", a)
