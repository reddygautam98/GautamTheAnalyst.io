with open("docs/build.py", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "Discovery MoM" in line or "retention &" in line or "Process Analysis" in line or "Agile, Testing" in line or "Technical Skills" in line:
        print(f"Line {idx+1}: {line.strip()}")

