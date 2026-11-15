# BUG-002: Missing Scroll-Margin on `:target` and `:focus-visible` Elements Obscures Keyboard Focus Under Sticky Header

## 1. Bug ID & Title
- **ID:** `BUG-002`
- **Title:** Missing `scroll-margin-top` on Target & Focused Elements Obscures Content and Focus Rings Under Sticky Header (WCAG 2.2 AA Criterion 2.4.11)

## 2. Affected Page & Section
- **Affected Pages:** All 8 website pages (`docs/index.html`, `docs/about.html`, `docs/services.html`, `docs/projects.html`, `docs/resume.html`, `docs/contact.html`, `docs/404.html`, `docs/samples/index.html`)
- **Affected Section:** Global keyboard navigation, in-page anchor links, and target element focus rings.

## 3. Source-Code File & Line Number
- **Pre-Fix Commit:** `ea99e36`
- **Pre-Fix Location:** `docs/assets/style.css`: lines 223–225
- **Post-Fix Location:** `docs/assets/style.css`: lines 223–226

## 4. Severity
- **Severity:** Medium (WCAG 2.2 AA Criterion 2.4.11 Focus Not Obscured - Minimum)

## 5. Problem Description
Under WCAG 2.2 Criterion 2.4.11 (Focus Not Obscured - Minimum), interactive components and targeted headings must not be obscured by author-created sticky or fixed elements such as `.site-header` (which occupies 68px/56px height plus borders and shadows up to 84px).
In `docs/assets/style.css`, `scroll-padding-top: 84px;` was applied to `html`, but individual targetable elements (`:target`) and keyboard-focused elements (`:focus-visible`) lacked explicit `scroll-margin-top`. In browsers where keyboard focus scrolling occurs independently of root scroll-padding (such as Safari keyboard navigation, mobile WebViews, or non-smooth scroll fallbacks), tabbing to headings, anchors, cards, or deep-linked target elements caused the top of the element and its focus ring to be partially obscured underneath the sticky navigation bar.

## 6. Reproduction Steps
1. Navigate to `http://127.0.0.1:8000/index.html` or `http://127.0.0.1:8000/samples/index.html`.
2. Press `Tab` repeatedly to navigate through interactive elements and section anchors.
3. Observe that when focusing elements positioned immediately below the header boundary in non-smooth or native focus scrolling scenarios, the top edge of the element and its focus indicator can be clipped or obscured by `.site-header`.

## 7. Expected Behavior
All keyboard-focused elements (`:focus-visible`) and fragment targets (`:target`) must maintain at least 84px of clearance from the top of the viewport when scrolled into view, preventing occlusion by the sticky header.

## 8. Actual Behavior
Only `.file-list li` had `scroll-margin-top: 90px;` defined. Global `:target` and `:focus-visible` elements had no `scroll-margin-top` defined.

## 9. Root-Cause Analysis
Omission of global `scroll-margin-top: var(--header-h, 84px)` declarations for `:target` and `:focus-visible:not(html, body)` in `docs/assets/style.css`.

## 10. Evidence
- In `docs/assets/style.css` line 223, `html { scroll-padding-top: 84px; }` was present, but no rule existed for `:target` or `:focus-visible` across the document.
- Only `.file-list li` at line 1919 defined `scroll-margin-top: 90px;`.

## 11. Fix Implemented
Added explicit `scroll-margin-top` rules to `docs/assets/style.css` immediately after `html`:
```css
:target {
  scroll-margin-top: var(--header-h, 84px);
}
:focus-visible:not(html, body) {
  scroll-margin-top: var(--header-h, 84px);
}
```

## 12. Files Modified
- `docs/assets/style.css`

## 13. Testing Performed
- CSS parsing and brace matching verified.
- Automated regression test suite passed via `tests/test_a11y_responsive.py` (5/5 suites passed).
- Verified commit `610bd84`.

## 14. Verification Status
**Fixed and verified.**
