with open("docs/build.py", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace('"Interactive HR dashboard tracking retention & performance"', '"Interactive HR dashboard tracking retention &amp; performance"')
c = c.replace('1: ("Discovery MoM & Decisions", "samples/index.html#discovery")', '1: ("Discovery Workshop MoM &amp; Decisions", "samples/index.html#discovery")')
c = c.replace('("Process Analysis & Documentation",', '("Process Analysis &amp; Documentation",')
c = c.replace('("Agile, Testing & Delivery",', '("Agile, Testing &amp; Delivery",')
c = c.replace('("Technical Skills & Tools",', '("Technical Skills &amp; Tools",')

with open("docs/build.py", "w", encoding="utf-8") as f:
    f.write(c)

print("docs/build.py final ampersands patched.")

