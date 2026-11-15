# BUG-004: Contact Form Dynamic Scoping HUD Service Prefill Synchronization

## 1. Bug ID & Title
- **ID:** `BUG-004`
- **Title:** Missing `change` Event Dispatch on Service Dropdown URL Query Prefill Leaves Scoping HUD Unsynchronized

## 2. Affected Page & Section
- **Affected Pages:** `docs/contact.html`
- **Affected Section:** Contact Form Service Selection & Scoping Feedback HUD (`#enquiry-service`, `.scoping-hud-pill`).

## 3. Source-Code File & Line Number
- **Pre-Fix Commit:** `ea99e36`
- **Pre-Fix Location:** `docs/assets/site.js`: lines 606–628
- **Post-Fix Location:** `docs/assets/site.js`: lines 606–629

## 4. Severity
- **Severity:** Low (Interactive feedback & state consistency)

## 5. Problem Description
When navigating to `contact.html?service=...` (e.g. from service card links across the portfolio), lines 606–628 in `docs/assets/site.js` match and assign `#enquiry-service`'s value programmatically.
In standard DOM behavior, programmatic `.value` assignment does not fire native `change` or `input` events.
As a result, if the page is loaded or state is restored dynamically, the `.scoping-hud-pill` feedback HUD (showing scope focus, delivery cadence, and NDA alignment) is not immediately synchronized via its change listener, and related field validation states are not notified.

## 6. Reproduction Steps
1. Navigate to `http://127.0.0.1:8000/contact.html?service=brd-frd-specifications`.
2. Inspect the `#enquiry-service` select element: the correct service is selected.
3. Observe that without a synthetic `change` event dispatch, external event subscribers relying on `change` are not triggered during the prefill cycle.

## 7. Expected Behavior
Programmatic prefilling of form controls must dispatch an appropriate `change` event so all bound feedback widgets and validation handlers update their state consistently.

## 8. Actual Behavior
The select `.value` was updated and `.classList.add('has-val')` was called, but no `change` event was dispatched to registered listeners.

## 9. Root-Cause Analysis
Omission of `sField.dispatchEvent(new Event('change', { bubbles: true }))` after matching and setting the prefill value in `docs/assets/site.js`.

## 10. Evidence
- In `docs/assets/site.js` lines 617 and 624: `sField.value = ...` with no subsequent event dispatch.

## 11. Fix Implemented
In `docs/assets/site.js` line 627, added:
```javascript
try {
  sField.dispatchEvent(new Event('change', { bubbles: true }));
} catch (_) {}
```
ensuring that any change listeners, including the dynamic `.scoping-hud-pill` updater and float-label state updaters, receive the prefilled state immediately.

## 12. Files Modified
- `docs/assets/site.js`

## 13. Testing Performed
- Validated JavaScript syntax via `node --check docs/assets/site.js`.
- Automated regression suite executed via `tests/test_a11y_responsive.py` (5/5 suites passed).
- Verified commit `a6e0cf8`.

## 14. Verification Status
**Fixed and verified.**
