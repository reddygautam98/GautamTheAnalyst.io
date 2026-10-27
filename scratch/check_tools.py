import glob
import re

for p in sorted(glob.glob('docs/**/*.html', recursive=True)):
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # Toolkit
    tiles = re.findall(r'<div class="tk-tile"[^>]*>.*?<span class="tk-name">([^<]+)</span>', c, re.DOTALL)
    if tiles:
        print(f"=== {p} Toolkit items ({len(tiles)}):")
        print("   ", ", ".join(tiles))
    
    # Check any specific icon classes
    tk_icos = re.findall(r'class="tk-ico([^"]*)"', c)
    if tk_icos:
        print("    tk-ico variants:", set(tk_icos))

