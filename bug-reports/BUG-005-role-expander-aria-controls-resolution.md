# BUG-005: Role Accomplishments Expander Target Resolution Robustness

## 1. Bug ID & Title
- **ID:** `BUG-005`
- **Title:** Role Accomplishments Expander Assumes Rigid DOM Sibling Structure Ignoring `aria-controls`

## 2. Affected Page & Section
- **Affected Pages:** `docs/index.html`
- **Affected Section:** Experience Timeline Accomplishments Expander & Key Metrics Tray (`.role-expander`, `.role-metrics`).

## 3. Source-Code File & Line Number
- **Pre-Fix Commit:** `ea99e36`
- **Pre-Fix Location:** `docs/assets/site.js`: lines 1074–1082
- **Post-Fix Location:** `docs/assets/site.js`: lines 1074–1084

## 4. Severity
- **Severity:** Low (DOM robustness & accessibility contract)

## 5. Problem Description
On `docs/index.html`, each role entry provides a collapsible key accomplishments tray toggled via `.role-expander`.
Each `.role-expander` button is annotated with `aria-controls="role-metrics-X"`.
In `docs/assets/site.js`, the click event handler resolved the collapsible tray strictly using:
```javascript
var metrics = btn.nextElementSibling;
```
If formatting elements, assistive comments, or layout wrappers are ever inserted between the button and the tray, `nextElementSibling` can resolve to an unexpected element or `null`, breaking the expand/collapse toggle for keyboard and mouse users.

## 6. Reproduction Steps
1. Navigate to `http://127.0.0.1:8000/index.html#experience`.
2. Locate the experience roles timeline.
3. Click "Key accomplishments & metrics" button (`.role-expander`).
4. In code review, note that `btn.nextElementSibling` ignores the explicit contract established by `aria-controls="role-metrics-0"`.

## 7. Expected Behavior
Interactive accordion/expander controls must resolve their target region primarily by the explicit `aria-controls` identifier, falling back gracefully to DOM adjacency (`nextElementSibling`).

## 8. Actual Behavior
The handler strictly traversed `nextElementSibling`, ignoring the `aria-controls` attribute present on the button.

## 9. Root-Cause Analysis
Direct DOM traversal without inspecting the semantic `aria-controls` attribute defined on the trigger button.

## 10. Evidence
- In `docs/index.html`: `<button class="role-expander" aria-controls="role-metrics-0" ...>`
- In `docs/assets/site.js` line 1076: `var metrics = btn.nextElementSibling;`

## 11. Fix Implemented
In `docs/assets/site.js` lines 1076–1078, updated the target resolution logic to prioritize `aria-controls`:
```javascript
var targetId = btn.getAttribute('aria-controls');
var metrics = (targetId && d.getElementById(targetId)) || btn.nextElementSibling;
```

## 12. Files Modified
- `docs/assets/site.js`

## 13. Testing Performed
- Validated JavaScript syntax via `node --check docs/assets/site.js`.
- Automated regression suite executed via `tests/test_a11y_responsive.py` (5/5 suites passed).
- Verified commit `bfcac5f`.

## 14. Verification Status
**Fixed and verified.**
