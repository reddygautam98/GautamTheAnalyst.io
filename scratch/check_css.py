import re

css_path = "docs/assets/style.css"
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# Check unmatched braces
open_braces = css.count("{")
close_braces = css.count("}")
print(f"Open braces: {open_braces}, Close braces: {close_braces}")

# Check for duplicate IDs or invalid rules
# Check for broken url(...) references in css
urls = re.findall(r'url\(([^)]+)\)', css)
print(f"Total url() in CSS: {len(urls)}")
for u in set(urls):
    u_clean = u.strip('"\'').split("?")[0].split("#")[0]
    if u_clean.startswith("data:") or u_clean.startswith("http:") or u_clean.startswith("https:"):
        continue
    # resolve relative to docs/assets/
    import os
    p = os.path.normpath(os.path.join("docs/assets", u_clean))
    exists = os.path.exists(p)
    if not exists:
        print(f"Broken CSS url: {u} -> resolved to {p}")

# Check for vendor prefixes or broken @keyframes
keyframes = re.findall(r'@keyframes\s+([a-zA-Z0-9_-]+)', css)
print(f"Total keyframes: {len(keyframes)}")

