with open("website-bug-audit.md", "r", encoding="utf-8") as f:
    text = f.read()

# Update summary count
text = text.replace("Across the audit, **9 distinct defects** were identified", "Across the audit, **11 distinct defects** were identified")
text = text.replace("""Total Defects Identified: 9
  - Critical Severity: 0
  - High Severity:     0
  - Medium Severity:   5
  - Low Severity:      4""", """Total Defects Identified: 11
  - Critical Severity: 0
  - High Severity:     0
  - Medium Severity:   6
  - Low Severity:      5""")

# Add to summary list
old_sum_end = """8. **WCAG Contrast Failure — Specification Console Rule Tags (Low):** In `about.html`, `.rule-tag.tag-auto` (`#0284c7`, 3.74:1) and `.rule-tag.tag-p1` (`#dc2626`, 4.41:1) fell below the 4.5:1 threshold. *Resolved by upgrading to `#0369a1` (4.75:1) and `#b91c1c` (5.70:1).*
9. **Dark Mode Text Contrast on Eyebrows & PSR Labels (Low):** In `style.css`, `--accent: #3b82f6` produced a borderline 4.41:1 contrast against dark soft background containers (`#162036`). *Resolved by mapping `.eyebrow` and `.psr-lbl` to `#60a5fa` in dark mode (> 5.8:1).*"""

new_sum_end = """8. **WCAG Contrast Failure — Specification Console Rule Tags (Low):** In `about.html`, `.rule-tag.tag-auto` (`#0284c7`, 3.74:1) and `.rule-tag.tag-p1` (`#dc2626`, 4.41:1) fell below the 4.5:1 threshold. *Resolved by upgrading to `#0369a1` (4.75:1) and `#b91c1c` (5.70:1).*
9. **Dark Mode Text Contrast on Eyebrows & PSR Labels (Low):** In `style.css`, `--accent: #3b82f6` produced a borderline 4.41:1 contrast against dark soft background containers (`#162036`). *Resolved by mapping `.eyebrow` and `.psr-lbl` to `#60a5fa` in dark mode (> 5.8:1).*
10. **Structural HTML Syntax Defect — Unclosed Header Container Div (Medium):** Across all 8 pages, `<div class="wrap bar">` within `<header class="site-header">` was never closed before `</header>`, violating HTML5 nesting rules and causing parser auto-closing. *Resolved by restoring the missing `</div>` before `</header>` in `docs/build.py`.*
11. **W3C HTML Validation — Bare Ampersands in Text & URL Attributes (Low):** Bare `&` characters in stylesheet font links, email action links, and text labels violated W3C HTML5 entity specifications. *Resolved by escaping all occurrences to `&amp;` across all templates.*"""

text = text.replace(old_sum_end, new_sum_end)

# Add to table
old_table_end = """| **BUG-08** | `about.html`<br>Specification Console | `docs/assets/style.css`<br>lines 3436–3453 | **Low** | Decision table rule tags (`tag-auto`, `tag-p1`) failed contrast (3.74:1 and 4.41:1). | Sky-600 (`#0284c7`) and Red-600 (`#dc2626`) fell below 4.5:1 on soft surfaces. | Upgraded to `#0369a1` (4.75:1) and `#b91c1c` (5.70:1). | **Fixed & Verified** |
| **BUG-09** | Global Across Pages<br>Eyebrows & Labels | `docs/assets/style.css`<br>lines 90, 246, 2743 | **Low** | Eyebrow badges and PSR labels had borderline 4.41:1 contrast on dark band surfaces. | Dark mode `--accent` (`#3b82f6`) on `#162036` container background is under 4.5:1. | Mapped `[data-theme=dark] .eyebrow` and `.psr-lbl` to `#60a5fa` (CR > 5.8:1). | **Fixed & Verified** |"""

new_table_end = """| **BUG-08** | `about.html`<br>Specification Console | `docs/assets/style.css`<br>lines 3436–3453 | **Low** | Decision table rule tags (`tag-auto`, `tag-p1`) failed contrast (3.74:1 and 4.41:1). | Sky-600 (`#0284c7`) and Red-600 (`#dc2626`) fell below 4.5:1 on soft surfaces. | Upgraded to `#0369a1` (4.75:1) and `#b91c1c` (5.70:1). | **Fixed & Verified** |
| **BUG-09** | Global Across Pages<br>Eyebrows & Labels | `docs/assets/style.css`<br>lines 90, 246, 2743 | **Low** | Eyebrow badges and PSR labels had borderline 4.41:1 contrast on dark band surfaces. | Dark mode `--accent` (`#3b82f6`) on `#162036` container background is under 4.5:1. | Mapped `[data-theme=dark] .eyebrow` and `.psr-lbl` to `#60a5fa` (CR > 5.8:1). | **Fixed & Verified** |
| **BUG-10** | Global (All 8 Pages)<br>Site Header | `docs/build.py`<br>line 185 | **Medium** | Unclosed `<div class="wrap bar">` container inside `<header class="site-header">`. | Omission of secondary closing `</div>` tag before `</header>` in template generator. | Restored `</div></div></header>` in `docs/build.py` and regenerated all 8 pages. | **Fixed & Verified** |
| **BUG-11** | Global (All 8 Pages)<br>Attributes & Copy | `docs/build.py`<br>lines 13, 17, 265, 900+ | **Low** | Bare `&` characters in font URLs, mailto links, and titles failed W3C HTML5 entity validation. | Direct inclusion of literal `&` rather than standard character entity reference `&amp;`. | Escaped literal ampersands to standard `&amp;` across all templates. | **Fixed & Verified** |"""

text = text.replace(old_table_end, new_table_end)

with open("website-bug-audit.md", "w", encoding="utf-8") as f:
    f.write(text)

print("website-bug-audit.md updated successfully.")

