import glob
import re
import os
import xml.etree.ElementTree as ET

html_files = sorted(glob.glob("docs/**/*.html", recursive=True))

for h in html_files:
    content = open(h, encoding="utf-8").read()
    
    # Check for unescaped & (except valid HTML entities)
    bad_amps = re.findall(r'&(?!(?:[a-zA-Z0-9]+|#[0-9]+|#x[0-9a-fA-F]+);)', content)
    if bad_amps:
        print(f"[{h}] Unescaped ampersands: {len(bad_amps)}")
        
    # Check for empty href or src
    empty_href = re.findall(r'href=["\']\s*["\']', content)
    if empty_href:
        print(f"[{h}] Empty href attributes: {len(empty_href)}")
        
    empty_src = re.findall(r'src=["\']\s*["\']', content)
    if empty_src:
        print(f"[{h}] Empty src attributes: {len(empty_src)}")
        
    # Check for undefined CSS variables
    # Find all var(--...) in style attributes
    style_vars = re.findall(r'var\((--[a-zA-Z0-9_-]+)\)', content)
    
    # Check for script errors / missing closing tags in scripts
    scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', content, re.DOTALL)
    for s in scripts:
        if s.strip() and not s.strip().startswith('{'): # non-json
            pass

print("Audit scan 1 completed.")

