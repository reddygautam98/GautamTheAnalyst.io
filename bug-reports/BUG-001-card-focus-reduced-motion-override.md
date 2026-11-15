# BUG-001: Card Focus Dimming & Section Blur Ignores Reduced Motion Preference

## 1. Bug ID & Title
- **ID:** `BUG-001`
- **Title:** Card Focus Dimming & Section Blur Ignores User Reduced Motion Preference & Animation Pause State

## 2. Affected Page & Section
- **Affected Pages:** All 8 website pages (`docs/index.html`, `docs/about.html`, `docs/services.html`, `docs/projects.html`, `docs/resume.html`, `docs/contact.html`, `docs/404.html`, `docs/samples/index.html`)
- **Affected Section:** All interactive card elements (`.card`, `.scard`, `.pcard`, `.step-card`, `.what-card`, `.peek-card`, `.principle-card`, etc.) and root `<main>` sections.

## 3. Source-Code File & Line Number
- **Pre-Fix Commit:** `ea99e36`
- **Pre-Fix Location:**
  - `docs/assets/card-fx.js`: line 135
  - `docs/assets/style.css`: lines 6241–6252
- **Post-Fix Location:**
  - `docs/assets/card-fx.js`: line 135
  - `docs/assets/style.css`: lines 6241–6274

## 4. Severity
- **Severity:** Medium (WCAG 2.2 AA / Motion-reduction compliance)

## 5. Problem Description
Clicking or tapping an interactive card triggers `body.has-card-focused-mode`, which applies a site-wide background section blur (`filter: blur(3.5px) saturate(0.8);`) and card scaling (`transform: translateY(-4px) scale(1.015);`). In `docs/assets/card-fx.js`, the click event listener checked `isPaused()` but failed to check `isReduced()`. Users with `prefers-reduced-motion: reduce` who tapped or clicked a card still experienced disorienting blur transitions and depth transformations. In addition, `docs/assets/style.css` lacked explicit overrides for `body.has-card-focused-mode main > section` under `@media (prefers-reduced-motion: reduce)` and `html.is-anim-paused`, leaving blurred backgrounds active even if the user enabled the `#animToggle` motion-pause control.

## 6. Reproduction Steps
1. Enable `prefers-reduced-motion: reduce` in operating system / browser preferences, or toggle `#animToggle` to paused.
2. Navigate to `http://127.0.0.1:8000/index.html` or `http://127.0.0.1:8000/about.html`.
3. Click or tap any interactive card (e.g. `.step-card`, `.what-card`, `.principle-card`).
4. Observe that `body.has-card-focused-mode` is activated and surrounding sections become blurred with `filter: blur(3.5px)`.

## 7. Expected Behavior
When `prefers-reduced-motion: reduce` or `html.is-anim-paused` is active, clicking or tapping a card must not activate disorienting background blur transitions or transform scaling.

## 8. Actual Behavior
The click handler in `card-fx.js` did not check `isReduced()`, and the stylesheet lacked reduced-motion and paused-animation neutralization rules for `body.has-card-focused-mode`.

## 9. Root-Cause Analysis
`docs/assets/card-fx.js` only checked `if (isPaused()) return;` inside the card `click` event listener. Furthermore, `docs/assets/style.css` applied `body.has-card-focused-mode main > section:not(.has-card-focused)` unconditionally without `@media (prefers-reduced-motion: reduce)` or `html.is-anim-paused` resets.

## 10. Evidence
- Code inspection of `docs/assets/card-fx.js` line 135: `if (isPaused()) return;` omitted `isReduced()`.
- Code inspection of `docs/assets/style.css` lines 6242–6248: absence of `@media (prefers-reduced-motion: reduce)` block resetting `filter: none !important; opacity: 1 !important;`.

## 11. Fix Implemented
1. Updated `docs/assets/card-fx.js` line 135 to guard against both paused and reduced-motion states:
   ```javascript
   if (isPaused() || isReduced()) return;
   ```
2. Added reduced motion and animation-pause reset blocks in `docs/assets/style.css`:
   ```css
   @media (prefers-reduced-motion: reduce) {
     body.has-card-focused-mode main > section,
     body.has-card-focused-mode .site-footer {
       filter: none !important;
       opacity: 1 !important;
       pointer-events: auto !important;
       transition: none !important;
     }
     .is-focused-card {
       transform: none !important;
     }
   }
   html.is-anim-paused body.has-card-focused-mode main > section,
   html.is-anim-paused body.has-card-focused-mode .site-footer {
     filter: none !important;
     opacity: 1 !important;
     pointer-events: auto !important;
     transition: none !important;
   }
   html.is-anim-paused .is-focused-card {
     transform: none !important;
   }
   ```

## 12. Files Modified
- `docs/assets/card-fx.js`
- `docs/assets/style.css`

## 13. Testing Performed
- JavaScript syntax verification via `node --check docs/assets/card-fx.js`.
- CSS brace structure validation.
- Automated regression suite executed via `tests/test_a11y_responsive.py` (5/5 suites passed).
- Verified commit `383d499`.

## 14. Verification Status
**Fixed and verified.**
