import json

with open("scratch/contrast_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total pages/themes with findings: {len(data)}")
for item in data:
    print(f"\n=== {item['page']} ({item['theme']}) - {item['failure_count']} items ===")
    for s in item['sample_failures'][:5]:
        txt = s['text'].replace('\n', ' ').strip()
        print(f"  {s['tag']}.{s['cls']} -> '{txt}': CR={s['cr']} (req={s['req']}) fg={s['color']} bg={s['bg']}")
