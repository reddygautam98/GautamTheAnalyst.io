import glob
import os
from collections import Counter
from bs4 import BeautifulSoup

docs_dir = os.path.abspath("docs")
html_files = sorted(glob.glob(os.path.join(docs_dir, "**/*.html"), recursive=True))

for hf in html_files:
    rel = os.path.relpath(hf, docs_dir)
    with open(hf, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    
    ids = [el["id"] for el in soup.find_all(id=True)]
    counts = Counter(ids)
    dupes = {i: c for i, c in counts.items() if c > 1}
    if dupes:
        print(f"[{rel}] Duplicate IDs found:")
        for i, c in dupes.items():
            print(f"  #{i} appears {c} times")
    else:
        print(f"[{rel}] All {len(ids)} IDs are unique.")
