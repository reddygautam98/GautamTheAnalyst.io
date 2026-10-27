import glob, re
from collections import defaultdict

classes_by_file = defaultdict(set)
for f in glob.glob('docs/**/*.html', recursive=True):
    content = open(f, encoding='utf-8').read()
    for m in re.finditer(r'class=["\']([^"\']+)["\']', content):
        for c in m.group(1).split():
            if any(k in c.lower() for k in ['card', 'tile', 'box', 'role', 'kit', 'step', 'proof', 'stat', 'feat', 'item', 'panel', 'preview', 'rbody', 'form', 'contact', 'hero', 'grid', 'peek', 'what']):
                classes_by_file[f].add(c)

for f, clss in sorted(classes_by_file.items()):
    print('==', f)
    for c in sorted(clss):
        print('  ', c)
