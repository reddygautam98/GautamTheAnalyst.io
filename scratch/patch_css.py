with open("docs/assets/style.css", "r", encoding="utf-8") as f:
    css = f.read()

# 1. Fix wf-kpi-val colors in light mode (WCAG AA >= 4.5:1)
old_kpi = """.wf-kpi-card.warn .wf-kpi-val{color:#d97706}
.wf-kpi-card.ok .wf-kpi-val{color:#059669}"""
new_kpi = """.wf-kpi-card.warn .wf-kpi-val{color:#b45309}
.wf-kpi-card.ok .wf-kpi-val{color:#047857}"""
assert old_kpi in css, "old_kpi not found"
css = css.replace(old_kpi, new_kpi)

# 2. Fix .req color in light & dark mode
old_req = ".req{color:#ef4444;font-weight:700}"
new_req = ".req{color:#dc2626;font-weight:700}\n[data-theme=dark] .req{color:#f87171}"
assert old_req in css, "old_req not found"
css = css.replace(old_req, new_req)

# 3. Fix rule-tag colors
old_rules = """.rule-tag.tag-auto {
  background: rgba(14, 165, 233, 0.12);
  color: #0284c7;
  border: 1px solid rgba(14, 165, 233, 0.28);
}
[data-theme=dark] .rule-tag.tag-auto {
  color: #38bdf8;
  border-color: rgba(14, 165, 233, 0.35);
}
.rule-tag.tag-p1 {
  background: rgba(239, 68, 68, 0.12);
  color: #dc2626;
  border: 1px solid rgba(239, 68, 68, 0.28);
}"""

new_rules = """.rule-tag.tag-auto {
  background: rgba(14, 165, 233, 0.12);
  color: #0369a1;
  border: 1px solid rgba(14, 165, 233, 0.28);
}
[data-theme=dark] .rule-tag.tag-auto {
  color: #38bdf8;
  border-color: rgba(14, 165, 233, 0.35);
}
.rule-tag.tag-p1 {
  background: rgba(239, 68, 68, 0.12);
  color: #b91c1c;
  border: 1px solid rgba(239, 68, 68, 0.28);
}"""
assert old_rules in css, "old_rules not found"
css = css.replace(old_rules, new_rules)

# 4. Fix dark theme step-num & rank-up-badge & eyebrow/psr-lbl contrast
dark_contrast_rules = """
/* Dark Theme WCAG AA Contrast Adjustments */
[data-theme=dark] .step-num {
  color: #0b0f19 !important;
  font-weight: 800;
}
[data-theme=dark] .rank-up-badge {
  color: #0b0f19 !important;
  font-weight: 800;
}
[data-theme=dark] .eyebrow {
  color: #60a5fa;
}
[data-theme=dark] .psr-lbl {
  color: #60a5fa;
}
"""

# Append to end of style.css
css = css + "\n" + dark_contrast_rules

with open("docs/assets/style.css", "w", encoding="utf-8") as f:
    f.write(css)

print("docs/assets/style.css successfully patched.")

