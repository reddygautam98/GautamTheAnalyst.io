import json

with open("docs/audit_results_live.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Keys:", list(data.keys()))
print("Pages in viewports:", list(data.get("pages", {}).keys()))

overflows = data.get("overflows", [])
print(f"Total overflows recorded: {len(overflows)}")
for o in overflows:
    print(o)

console_errors = data.get("console_errors", [])
print(f"Total console errors recorded: {len(console_errors)}")
for ce in console_errors:
    print(ce)

imgs_no_alt = data.get("images_without_alt", [])
print(f"Images without alt: {len(imgs_no_alt)}")

interactive_no_name = data.get("interactive_without_name", [])
print(f"Interactive without name: {len(interactive_no_name)}")

