with open("docs/build.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Deterministic tile_id
old_tile = 'tile_id = f"tk-ev-{abs(hash(name)) % 10000}"'
new_tile = 'tile_id = f"tk-ev-{slug}"'
assert old_tile in content, "old_tile not found"
content = content.replace(old_tile, new_tile)

# 2. Add IDs to filter chips
old_chips = '''chips = f'<button class="chip is-active" type="button" data-f="all" aria-pressed="true">All ({len(PROJECTS)})</button>' + "".join(
        f'<button class="chip" type="button" data-f="{k}" aria-pressed="false">{n} ({cat_counts.get(k, 0)})</button>\''''

new_chips = '''chips = f'<button class="chip is-active" id="all" type="button" data-f="all" aria-pressed="true">All ({len(PROJECTS)})</button>' + "".join(
        f'<button class="chip" id="{k}" type="button" data-f="{k}" aria-pressed="false">{n} ({cat_counts.get(k, 0)})</button>\''''

assert old_chips in content, "old_chips not found"
content = content.replace(old_chips, new_chips)

with open("docs/build.py", "w", encoding="utf-8") as f:
    f.write(content)

print("docs/build.py successfully patched.")

