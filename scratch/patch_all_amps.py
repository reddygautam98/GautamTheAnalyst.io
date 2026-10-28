with open("docs/build.py", "r", encoding="utf-8") as f:
    c = f.read()

# Phase buttons
c = c.replace('title="Filter to Phase 1: Discovery & MoM"', 'title="Filter to Phase 1: Discovery &amp; MoM"')
c = c.replace('title="Filter to Phase 2: BRD & FRD Specs"', 'title="Filter to Phase 2: BRD &amp; FRD Specs"')
c = c.replace('title="Filter to Phase 3: Stories & BDD"', 'title="Filter to Phase 3: Stories &amp; BDD"')
c = c.replace('title="Filter to Phase 4: RTM & UAT"', 'title="Filter to Phase 4: RTM &amp; UAT"')

# Services link text
c = c.replace('Inspect Discovery MoM & Decisions &rarr;', 'Inspect Discovery MoM &amp; Decisions &rarr;')

# Projects text
c = c.replace('"Workforce turnover & tenure analytics"', '"Workforce turnover &amp; tenure analytics"')
c = c.replace('"Dashboard tracking retention & performance"', '"Dashboard tracking retention &amp; performance"')
c = c.replace('"Executive business KPI & margin modeling"', '"Executive business KPI &amp; margin modeling"')
c = c.replace('"Standardized monthly profit & sales metrics across units"', '"Standardized monthly profit &amp; sales metrics across units"')
c = c.replace('"User retention & monetization event analysis"', '"User retention &amp; monetization event analysis"')
c = c.replace('"Writing & BA Notes"', '"Writing &amp; BA Notes"')
c = c.replace('"Daily Posts & Notes"', '"Daily Posts &amp; Notes"')
c = c.replace('"Reusable BRD, user story & acceptance criteria templates"', '"Reusable BRD, user story &amp; acceptance criteria templates"')

# Index text
c = c.replace('with QA & Engineering.', 'with QA &amp; Engineering.')
c = c.replace('<h3>Process Analysis & Documentation</h3>', '<h3>Process Analysis &amp; Documentation</h3>')
c = c.replace('Fishbone & 5-Why root cause analysis', 'Fishbone &amp; 5-Why root cause analysis')
c = c.replace('<h3>Agile, Testing & Delivery</h3>', '<h3>Agile, Testing &amp; Delivery</h3>')
c = c.replace('<h3>Technical Skills & Tools</h3>', '<h3>Technical Skills &amp; Tools</h3>')
c = c.replace('OpenAPI 3.0 contracts & webhook payload specs', 'OpenAPI 3.0 contracts &amp; webhook payload specs')
c = c.replace('Analysed 100,000+ records & query optimization', 'Analysed 100,000+ records &amp; query optimization')
c = c.replace('Requirements repository & sprint backlog boards', 'Requirements repository &amp; sprint backlog boards')
c = c.replace('Wireframe reviews & API response verification', 'Wireframe reviews &amp; API response verification')
c = c.replace('Slide 2: User story & BDD', 'Slide 2: User story &amp; BDD')

with open("docs/build.py", "w", encoding="utf-8") as f:
    f.write(c)

print("docs/build.py updated with all ampersand entities.")

