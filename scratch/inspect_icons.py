import glob
import re
from collections import defaultdict

svg_elements = []
for p in glob.glob('docs/**/*.html', recursive=True):
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all <svg tags and their attributes / classes / parents
    svgs = re.finditer(r'(<(?P<parent>[a-zA-Z0-9_-]+)[^>]*>)?\s*(<svg(?P<attrs>[^>]*)>.*?</svg>)', content, re.DOTALL)
    for s in svgs:
        attrs = s.group('attrs')
        parent = s.group(0)[:100]
        svg_elements.append((p, attrs, parent))

print(f"Total SVGs found: {len(svg_elements)}")

# Let's inspect unique SVG contexts
classes_found = set()
for p, attrs, parent in svg_elements:
    cls_match = re.search(r'class=["\']([^"\']+)["\']', attrs)
    if cls_match:
        classes_found.add(cls_match.group(1))
    parent_cls = re.search(r'class=["\']([^"\']+)["\']', parent)
    if parent_cls:
        classes_found.add("PARENT: " + parent_cls.group(1))

print("Unique contexts:")
for c in sorted(classes_found):
    print(" -", c)
