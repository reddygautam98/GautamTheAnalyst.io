import glob
import re

html_files = sorted(glob.glob("docs/**/*.html", recursive=True))
bad_buttons = []

for h in html_files:
    content = open(h, encoding="utf-8").read()
    # Find all button tags
    buttons = re.findall(r'<button\b([^>]*)>(.*?)</button>', content, re.DOTALL | re.IGNORECASE)
    for attrs, inner in buttons:
        # Check type attribute
        type_match = re.search(r'type=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        btn_type = type_match.group(1) if type_match else "missing"
        
        # Check text or aria-label
        aria_label = re.search(r'aria-label=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        aria_labelledby = re.search(r'aria-labelledby=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        title_attr = re.search(r'title=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        inner_text = re.sub(r'<[^>]+>', '', inner).strip()
        
        has_accessible_name = bool(inner_text or aria_label or aria_labelledby or title_attr)
        if btn_type == "missing" or not has_accessible_name:
            bad_buttons.append((h, attrs[:60], inner[:40], f"type: {btn_type}, accessible name: {has_accessible_name}"))

print(f"Total problematic buttons: {len(bad_buttons)}")
for b in bad_buttons:
    print(b)

