# BUG-003: High-Resolution Screenshot Lens Magnifier Center-Point Optical Offset

## 1. Bug ID & Title
- **ID:** `BUG-003`
- **Title:** High-Resolution Screenshot Lens Magnifier Center-Point Optical Offset Discrepancy

## 2. Affected Page & Section
- **Affected Pages:** `docs/projects.html`
- **Affected Section:** PayTrack Featured Case Study & High-Resolution ERD Architecture Diagram (`.feat-img`, `.has-lens`, `.lens-glass`).

## 3. Source-Code File & Line Number
- **Pre-Fix Commit:** `ea99e36`
- **Pre-Fix Location:** `docs/assets/site.js`: lines 1386–1402
- **Post-Fix Location:** `docs/assets/site.js`: lines 1386–1404

## 4. Severity
- **Severity:** Low (UI / Visual precision)

## 5. Problem Description
On `docs/projects.html`, hovering over the high-resolution architecture diagram activates an interactive magnifying lens (`.lens-glass`).
In `docs/assets/site.js`, the lens diameter was hardcoded to `glassW=120, glassH=120`. However, in `docs/assets/style.css` (line 5639), `.lens-glass` is defined with `width: 140px; height: 140px;` and `transform: translate(-50%, -50%)`. Because the center offset calculation subtracted `glassW/2` (60px) instead of the actual half-width (70px), the background image position inside the magnifying glass was offset by 10px along both axes, creating an optical misalignment where the magnified focus did not align with the pointer location.

## 6. Reproduction Steps
1. Navigate to `http://127.0.0.1:8000/projects.html`.
2. Scroll to the PayTrack Case Study high-resolution diagram (`.feat-img`).
3. Hover over fine text or diagram lines with a fine cursor device.
4. Inspect the background image position inside `.lens-glass`: the focal point is displaced 10px from the center of the crosshair.

## 7. Expected Behavior
The focal center of the zoomed background image must exactly correspond to the cursor position `(x, y)` at the center of `.lens-glass`.

## 8. Actual Behavior
A hardcoded `120px` dimension in JavaScript clashed with `140px` defined in CSS, displacing the optical focal center by 10px.

## 9. Root-Cause Analysis
Hardcoded dimensions `var glassW=120, glassH=120;` in `docs/assets/site.js` lines 1386 and 1398, instead of dynamically querying `.offsetWidth` / `.offsetHeight` or aligning with CSS.

## 10. Evidence
- `docs/assets/site.js` line 1386: `var glassW=120,glassH=120,lensRaf=null;`
- `docs/assets/style.css` line 5639: `.lens-glass { width: 140px; height: 140px; ... }`

## 11. Fix Implemented
Updated `docs/assets/site.js` inside the `requestAnimationFrame` loop to dynamically determine the rendered lens dimensions:
```javascript
var glassW = glass.offsetWidth || 140;
var glassH = glass.offsetHeight || 140;
```
ensuring the center offset computation `-(x * z - glassW / 2)` and `-(y * z - glassH / 2)` matches the CSS box model.

## 12. Files Modified
- `docs/assets/site.js`

## 13. Testing Performed
- Validated JavaScript syntax via `node --check docs/assets/site.js`.
- Automated regression suite executed via `tests/test_a11y_responsive.py` (5/5 suites passed).
- Verified commit `1e2cd80`.

## 14. Verification Status
**Fixed and verified.**
