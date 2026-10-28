content = open("docs/index.html", encoding="utf-8").read()
import re
matches = [m.start() for m in re.finditer(r'\bid=["\']US-03["\']', content)]
print("Found id='US-03' at indices:", matches)
for idx in matches:
    print(content[idx-50:idx+80])

