# Gautam The Analyst — Website Change Checklist

**Purpose:** Verify that the useful interactions from `Gautam_The_Analyst_Futuristic.zip` have been integrated into the published GitHub Pages source.

**Live site:** https://reddygautam98.github.io/GautamTheAnalyst.io/  
**Canonical source:** `main / docs/`  
**Important:** The changes are integrated as a progressive enhancement layer on top of the existing white/orange portfolio and the persistent light/dark theme. This is not a pixel-for-pixel replacement of the original `styles.css` file from the ZIP. The existing brand, content and project data are retained.

## A. Code integration checklist

### Shared design and theme

- [x] Added `docs/assets/css/site-enhancements.css` as a separate, maintainable enhancement layer.
- [x] Added `docs/assets/js/site-enhancements.js` for new interactions, leaving the existing site script in place.
- [x] Loaded both enhancement files on Home, About, Services, Projects, Resume, Contact and the BA Samples gallery.
- [x] Added Space Grotesk and JetBrains Mono font families alongside Inter for display and technical details.
- [x] Added restrained aurora background treatment and glass-like panels without bringing back heavy background-chart clutter.
- [x] Added subtle cursor spotlights and an animated gradient-border treatment for selected panels.
- [x] Added CSS page transitions with fallback behavior.
- [x] Preserved the existing light/dark theme handler and storage key rather than introducing a second competing theme toggle handler.
- [x] Added reduced-motion handling for reveal animations, ticker motion, typed text, hero tilt and gradient-border movement.
- [x] Added a fallback presentation when a project preview image fails to load.

### Navigation and interaction

- [x] Added a command palette to the six main pages and BA Samples gallery.
- [x] Command palette opens by **Ctrl+K / Cmd+K** or the **/** key when focus is not in a text-entry control.
- [x] Command palette includes links to Home, Services, Projects, BA Samples, About, Resume, Contact and direct email, plus a theme action.
- [x] Added a typed focus line beneath the home hero copy.
- [x] Added scroll-reveal animation to selected headings, cards and timeline items; content remains visible if the observer API is unavailable.
- [x] Added gentle 3D tilt to the hero illustration on fine-pointer devices, disabled for reduced-motion preference.
- [x] Added toolkit tickers to Home, About and Services.

### Home page

- [x] Added the interactive Business Analysis lifecycle explorer.
- [x] Added Discover, Define, Validate and Hand over steps.
- [x] Added the fictional PayTrack traceability example **BR-02 → FR-007 → US-04 → TC-005** from the supplied requirements traceability data.
- [x] Kept the sample disclaimer clear: PayTrack is fictional and the linked test case is marked Not Run.

### Page-specific features

- [x] About: added quick navigation to principles, capabilities and contact, plus the toolkit ticker.
- [x] Services: added quick navigation to service cards, engagement process and project enquiry, plus the toolkit ticker.
- [x] Projects: added a search input, live visible-project count and an empty-result message; search works with the existing category filters.
- [x] Resume: added quick navigation to Experience, Skills and Education/Certifications.
- [x] Resume: added count-up animation to the four existing evidence metrics without changing their end values.
- [x] Contact: added a non-submitting email-draft terminal preview.
- [x] Contact: added copy buttons for the public email, LinkedIn URL and GitHub URL.
- [x] Contact: kept the form behavior honest—the static form opens an email draft and does not store or automatically send visitor data.
- [x] BA Samples: loaded the same progressive enhancement layer while retaining the gallery's own layout and explicit dark-theme card colors.

## B. Static checks — verified

- [x] All seven pages load with no 404s for local CSS, JavaScript, SVG or sample files.
- [x] Each page shows exactly one primary `h1` heading.
- [x] Each page shows the correct current navigation state and the theme toggle.
- [x] No legacy HTML5 UP / Massively template dependencies are referenced.
- [x] Project filters and search can be used together; count matches the visible cards.
- [x] The lifecycle explorer updates its active step and detail panel on every selection.
- [x] Copy buttons show success feedback when clipboard access succeeds and a fallback message when it does not.
- [x] Failed preview images display a readable placeholder rather than a broken-image icon.
- [x] Contact form validation still works and produces a draft addressed to `reddygautam98@gmail.com`.

## C. Manual browser QA — not confirmed by static checks

Use this section after the latest Pages build is published. Mark each item only after testing it in the browser.

- [ ] Open the home page in light theme at desktop width; confirm the hero artwork does not collapse or overlap the heading.
- [ ] Toggle to dark theme; check navigation, cards, form controls, sample cards, footer and focus outlines.
- [ ] Refresh the page; confirm the selected theme persists.
- [ ] Open command palette with Ctrl/Cmd+K; search and open each main page.
- [ ] Open command palette with / while focus is not in an input. Confirm / still types normally in search and form fields.
- [ ] On mobile (approximately 360–430 px), confirm navigation, quick-nav pills, ticker and command palette fit without horizontal overflow.
- [ ] On Projects, search for `Power BI`, select a category, clear search, and confirm the count and empty state are correct.
- [ ] On Home, select all four lifecycle steps and confirm the traceability sample and disclaimer are readable.
- [ ] On Resume, confirm each count-up ends at the existing source metric.
- [ ] On Contact, test each copy button, then submit a valid enquiry and confirm the email draft opens with populated fields.
- [ ] Enable the device's reduced-motion preference; confirm moving effects are disabled or reduced.
- [ ] Review contrast and keyboard focus on both themes; keyboard through every control and close the command palette with Escape.
- [ ] Check the live public site after a hard refresh (Ctrl+F5 or browser equivalent).

## D. Release tracking

- Source files are committed under `docs/`, the configured GitHub Pages publishing folder.
- Run static link checks after any future markup changes.
- Record the deployed commit and the last manual browser-QA date here: `Pending manual browser QA`.

**Status:** Feature code is integrated and static checks are complete; live visual/browser verification remains to be completed. Do not mark the manual QA boxes as complete without testing the published website.
