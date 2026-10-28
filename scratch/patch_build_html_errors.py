with open("docs/build.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Fix unclosed div in header
old_hdr = '</div></header><div class="nav-backdrop" id="navBackdrop" aria-hidden="true"></div>'
new_hdr = '</div></div></header><div class="nav-backdrop" id="navBackdrop" aria-hidden="true"></div>'
assert old_hdr in content, "old_hdr not found"
content = content.replace(old_hdr, new_hdr)

# 2. Fix FONTS URL ampersands
old_fonts = 'FONTS = "https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Sans:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap"'
new_fonts = 'FONTS = "https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;1,400&amp;family=IBM+Plex+Sans:wght@400;500;600;700&amp;family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&amp;display=swap"'
assert old_fonts in content, "old_fonts not found"
content = content.replace(old_fonts, new_fonts)

# 3. Fix openGmailBtn href ampersands
old_gmail = 'href="https://mail.google.com/mail/?view=cm&fs=1&to='
new_gmail = 'href="https://mail.google.com/mail/?view=cm&amp;fs=1&amp;to='
assert old_gmail in content, "old_gmail not found"
content = content.replace(old_gmail, new_gmail)

# 4. Fix MARQ_ITEMS ampersands
content = content.replace('"User Stories & BDD"', '"User Stories &amp; BDD"')
content = content.replace('"Power BI & Excel"', '"Power BI &amp; Excel"')
content = content.replace('"UAT & Defect Triage"', '"UAT &amp; Defect Triage"')

# 5. Fix SERV deliverables ampersands
content = content.replace('"User stories & BDD"', '"User stories &amp; BDD"')
content = content.replace('"Testing & Verification"', '"Testing &amp; Verification"')
content = content.replace('"Advisory & Discovery"', '"Advisory &amp; Discovery"')
content = content.replace('"Custom BA scope & advisory"', '"Custom BA scope &amp; advisory"')
content = content.replace('"Business rules & data dictionaries"', '"Business rules &amp; data dictionaries"')
content = content.replace('"Confluence & Excel documentation"', '"Confluence &amp; Excel documentation"')

# 6. Fix sitem titles in samples
content = content.replace('"Discovery Workshop MoM & Decision Log"', '"Discovery Workshop MoM &amp; Decision Log"')
content = content.replace('"Discovery Workshop MoM & Decisions"', '"Discovery Workshop MoM &amp; Decisions"')
content = content.replace('"BRD & FRD Specifications"', '"BRD &amp; FRD Specifications"')
content = content.replace('"RTM & Test Scenarios"', '"RTM &amp; Test Scenarios"')

# 7. Fix Skills matrix
content = content.replace('("User Stories & BDD"', '("User Stories &amp; BDD"')
content = content.replace('("Scope & Impact"', '("Scope &amp; Impact"')
content = content.replace('("Power BI & DAX"', '("Power BI &amp; DAX"')
content = content.replace('("JIRA & Confluence"', '("JIRA &amp; Confluence"')
content = content.replace('("Figma & Postman"', '("Figma &amp; Postman"')

# 8. Fix contact dropdown option
content = content.replace('<option>Custom BA scope & advisory</option>', '<option>Custom BA scope &amp; advisory</option>')

with open("docs/build.py", "w", encoding="utf-8") as f:
    f.write(content)

print("docs/build.py patched successfully with HTML structural and entity fixes.")

