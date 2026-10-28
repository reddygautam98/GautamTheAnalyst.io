import xml.etree.ElementTree as ET
from html.parser import HTMLParser

for f in ["docs/services.html", "docs/about.html", "docs/index.html"]:
    with open(f, encoding="utf-8") as fp:
        html = fp.read()
    
    # Check for duplicate IDs
    import re
    ids = re.findall(r'id=["\']([^"\']+)["\']', html)
    id_dups = [i for i in ids if ids.count(i) > 1]
    if id_dups:
        print(f"[{f}] Duplicate IDs:", set(id_dups))
        
    # Check for aria-controls targets
    controls = re.findall(r'aria-controls=["\']([^"\']+)["\']', html)
    missing_controls = [c for c in controls if c not in ids]
    if missing_controls:
        print(f"[{f}] Missing aria-controls targets:", set(missing_controls))
        
    # Check for aria-describedby targets
    descby = re.findall(r'aria-describedby=["\']([^"\']+)["\']', html)
    missing_descby = [d for d in descby if d not in ids]
    if missing_descby:
        print(f"[{f}] Missing aria-describedby targets:", set(missing_descby))
        
    # Check for aria-labelledby targets
    lblby = re.findall(r'aria-labelledby=["\']([^"\']+)["\']', html)
    missing_lblby = [l for l in lblby if l not in ids]
    if missing_lblby:
        print(f"[{f}] Missing aria-labelledby targets:", set(missing_lblby))

print("ARIA target validation completed.")

