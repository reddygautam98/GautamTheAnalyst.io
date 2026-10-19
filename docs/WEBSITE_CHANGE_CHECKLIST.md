# Gautam The Analyst — Website Change Checklist

**Purpose:** Verify the integrated Futuristic v2/v3 interactions and the 2026 portfolio patterns from Gautam_The_Analyst_Portfolio_2026.zip in the GitHub Pages source.

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


## Futuristic 3D integration — 2026-10-19

### Added to the live source (static integration checks)
- [x] Added a self-contained 3D canvas effects layer at `docs/assets/js/fx3d.js` without loading an external 3D library.
- [x] Added a theme-aware starfield, ambient orbs, CSS 3D cubes, shooting-star accents and scroll-responsive hue shift.
- [x] Added wireframe geometric visuals to the homepage hero and subtle geometric visuals to interior-page headings.
- [x] Added a draggable, keyboard-operable toolkit ring to the homepage.
- [x] Added perspective tilt and pointer-following highlights to cards on fine-pointer devices.
- [x] Added responsive rules and reduced-motion / print fallbacks.
- [x] Wired the shared enhancement loader to load the 3D layer on all seven site pages including BA Samples.
- [x] Preserved existing portfolio content and sample-artifact disclaimers; did not publish a phone number from the supplied ZIP.

### Manual browser checks still required
- [ ] Confirm 3D geometry does not obscure text or cards on desktop.
- [ ] Confirm the toolkit ring drags correctly and rotates with the left/right arrow keys.
- [ ] Test on mobile at 360–430 px widths, including touch-drag and horizontal overflow.
- [ ] Verify light/dark theme rendering, keyboard focus and reduced-motion behavior in a real browser.
- [ ] Check CPU/battery impact and confirm animations pause when the tab is hidden.


## 2026 portfolio patterns (v4) — integrated in source

### Static implementation checks
- [x] Added the home-page proof bento for 100,000+ analyzed records, 350+ coordinated test cases, 2 gateway integrations and 20+ workshops; text aligns with the existing resume evidence.
- [x] Replaced the home-page three-card preview with four sticky case studies (Sales Data Analysis, HR Data Analysis, Sales Forecasting Report and MetaLayer), each linked to its repository; all nine projects remain available on Projects.
- [x] Added the process-line / scroll-told handoff treatment to Home and Services.
- [x] Added the About-page “At a glance” bento with role, focus, method, domain and profile links.
- [x] Added the six-card bento rhythm to Services.
- [x] Added a grid/list layout switch to the Projects page without replacing existing category filtering or text search.
- [x] Added the sticky resume snapshot beside the experience timeline using existing evidence and skills.
- [x] Added the large GAUTAM · THE ANALYST footer wordmark across the pages and a scroll-linked headline marquee on Home.
- [x] Added word-by-word heading entrances, magnetic primary CTAs and home-page scroll-spy dots.
- [x] Changed new-visit theme default to dark while respecting an existing saved light/dark choice.
- [x] Preserved all current verified career metrics, project links and the fictional PayTrack sample disclaimer.
- [x] Kept the phone number from the uploaded package off the public contact page.

### Static checks after v4 integration
- [x] Enhancement JavaScript parses without syntax errors.
- [x] Enhancement CSS braces are balanced and responsive / reduced-motion fallbacks remain present.
- [x] All seven pages contain one primary h1 and no duplicate IDs.
- [x] All seven pages include dark-first theme metadata and load the enhancement layer.

### Manual browser QA — still required
- [ ] Confirm case-study sticky stacking/depth, transitions and project screenshots on desktop.
- [ ] Use the Projects Grid/List switch and confirm it works together with category filters, search and result counts.
- [ ] Confirm the homepage marquee tracks scrolling and the section-dot navigation follows the visible section.
- [ ] Check About bento and Services card rhythm at desktop, tablet and mobile breakpoints.
- [ ] Verify the Resume snapshot sticks beside the timeline on desktop and moves above it on mobile.
- [ ] Confirm kinetic words and magnetic buttons are subtle, usable and fully visible with keyboard focus.
- [ ] Verify dark-first, saved light/dark preference, and the system's reduced-motion setting in a real browser.
- [ ] Check performance, tab-visibility behavior, and layout at 360–430 px widths.

**Release status:** v4 code changes are integrated in this branch and static checks passed. Merge/deployment and hands-on browser QA must be confirmed separately.

 
## Open items from the 2026-10-19 v6 review — code integration status

### Resolved in the published source (static checks)
- [x] Standardized the main-site navigation label to **Capabilities** and updated the command-palette entry to match.
- [x] Changed all six service-card calls to action to **Ask about this capability**.
- [x] Removed the remaining **freelance** wording from the Contact page metadata/body; the enquiry options focus on discovery, deliverables, support and feasibility.
- [x] Added the Resume page's direct download link and committed `docs/assets/Gautam_Reddy_Business_Analyst_Resume.pdf`.
- [x] Added the **Payments Extras** section inside the BA Samples page, with links to `iso20022_pain001_to_pacs008_mapping.csv` and `payment_rails_learning_notes.md`.
- [x] Confirmed About, Capabilities and Contact have distinct page-specific structures: About bento tiles, Capabilities cards/process, Contact split direct-contact/enquiry layout.
- [x] Added a floating quick-action dock for Resume / Email / JD fit check; on Resume it links directly to the PDF.
- [x] Made the dock safe-area aware and centred on mobile, hide Email on narrow screens, and constrained the JD checker to the available viewport.
- [x] Added a paste-and-compare job-description keyword checker. Its result explicitly says it is a keyword comparison, not an ATS score.
- [x] Tightened small-screen hero-card styles and reduced the 3D canvas intensity to reduce overlap risk on narrow screens.
- [x] Prepared a separate LinkedIn/Naukri profile-copy kit; it is draft content for manual publishing, not a change to the external accounts.

### Manual checks still open
- [ ] Visually inspect Home hero card and the quick-action dock at 360px, 390px, 430px and desktop widths; the local headless screenshot attempt did not complete, so this is not marked as visually verified.
- [ ] On a phone, tap Resume and JD fit check, confirm labels are legible, and verify the dock does not cover form buttons or footer links.
- [ ] Paste a sample JD, verify both keyword groups render, close with Escape, and confirm inputs retain normal keyboard behavior.
- [ ] Click the Resume PDF link on the published site and confirm the browser downloads/opens the PDF.
- [ ] Test theme toggle, reduced-motion preference, keyboard focus and scrolling on the published site.
- [ ] Publish the prepared LinkedIn and Naukri text into the respective profile accounts; this cannot be done through the static website repository.

**Status for this review:** Code changes and static checks are complete; real-device visual QA and external-profile publishing remain outstanding.
