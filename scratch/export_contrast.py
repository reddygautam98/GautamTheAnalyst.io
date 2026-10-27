import json

with open("scratch/contrast_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("scratch/contrast_report.txt", "w", encoding="utf-8") as out:
    out.write(f"Total pages/themes with findings: {len(data)}\n")
    for item in data:
        out.write(f"\n=== {item['page']} ({item['theme']}) - {item['failure_count']} items ===\n")
        for s in item['sample_failures']:
            txt = s['text'].replace('\n', ' ').strip()
            out.write(f"  {s['tag']}.{s['cls']} -> '{txt}': CR={s['cr']} (req={s['req']}) fg={s['color']} bg={s['bg']}\n")

print("Report written successfully.")
