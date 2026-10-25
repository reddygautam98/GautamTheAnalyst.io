# ui/ux Code & Design Review — GautamTheAnalyst.io

**Scope:** `GautamTheAnalyst.io.zip` (static GitHub Pages site, published from `docs/`). **Review type:** static ui/ux code + design review (no browser rendering).

## 1. Scope, method and limits

**Reviewed in full:** `docs/index.html`, `about.html`, `services.html`, `projects.html`, `resume.html`, `contact.html`, `404.html`, `samples/index.html`, `docs/assets/site.js` (675 lines), `docs/sitemap.xml`, `robots.txt`, `README.txt`, `docs/README.md`.
**Reviewed selectively:** `docs/assets/style.css` (3,661 lines – tokens, header/nav, hero, marquee, cards, tooltips, flip cards, forms, drawer, responsive breakpoints, reduced-motion, print, and every rule referenced by an issue below; not every rule was read). `build.py`/`flows.py` were not reviewed line-by-line because they only generate the HTML that was reviewed directly.
**Not reviewed:** contents of the PDF/DOCX/PNG/SVG/CSV/SQL sample files (only existence, type and image dimensions were checked); the Lenis library internals.
**Checks run:** automated scan of all `href`/`src` for missing local files (none missing), in-page anchors (none broken), duplicate IDs (none), images without `alt`/dimensions (none); WCAG contrast computed from CSS colour values; image dimensions/types via `file`.
**Limits:** external links (GitHub, LinkedIn, HackerRank, Figma/FigJam) could not be tested offline. Items marked **(verify)** are inferred from code and should be confirmed in DevTools/real devices. Line numbers refer to the files as delivered (CRLF).

**Severity key:** **Critical** = content invisible/false or core function broken; **Major** = significant ui/ux, accessibility, performance or content-integrity failure; **Minor** = polish, maintainability or low-impact deviation.

## 2. Summary

| Severity | Count |
|---|---:|
| Critical | 2 |
| Major | 18 |
| Minor | 36 |
| **Total** | **56** |

**By page / area**

| Page / area | Critical | Major | Minor | Total |
|---|---:|---:|---:|---:|
| Global / shared (all pages) | 1 | 4 | 11 | 16 |
| Home page (`docs/index.html`) | 0 | 5 | 9 | 14 |
| About page (`docs/about.html`) | 0 | 1 | 2 | 3 |
| Services page (`docs/services.html`) | 0 | 2 | 2 | 4 |
| Projects page (`docs/projects.html`) | 0 | 1 | 3 | 4 |
| Resume page (`docs/resume.html`) | 0 | 2 | 1 | 3 |
| Contact page (`docs/contact.html`) | 0 | 2 | 3 | 5 |
| BA Samples page (`docs/samples/index.html`) | 1 | 1 | 4 | 6 |
| 404 page (`docs/404.html`) | 0 | 0 | 1 | 1 |

**Top fixes (recommended order):** GL-01 (invisible headings without `color-mix`), SMP-01 (“PASS” results vs “Not Run”), SVC-01 (duplicate `style` attribute), RSM-01 (print drops skills), RSM-03 (no employment dates), CNT-01/CNT-04 (form usability), GL-02/GL-05/GL-06 (keyboard + drawer), IDX-09 (thumbnail crops), IDX-11 (clipped tooltips), GL-03 (animation pause), IDX-14 (inconsistent spec data).

**What already works well (no action):** theme toggle persists and falls back safely; `prefers-reduced-motion` is honoured in CSS and JS; skip link, `aria-current`, `lang`, canonical/OG/JSON-LD, sitemap and robots are present; all images have `alt` and dimensions; external links use `rel="noopener noreferrer"`; the marquee has a pause control.

## 3. Detailed issue list (grouped by page and section)

### Global / shared (all pages)

#### GL-01 — Headings (h2 gradient text)
- **Page / section:** Global / shared › Headings (h2 gradient text)
- **File / line:** docs/assets/style.css:189-197
- **Category:** Cross-browser / color
- **Severity:** **Critical**
- **Problem:** `.sec-head h2, .two h2, .wrap > h2, .form-card h2` set `background: linear-gradient(..., color-mix(in srgb, …))` together with `-webkit-text-fill-color: transparent` and `background-clip: text`. In a browser without `color-mix()` (Chrome < 111, Safari < 16.2, Firefox < 113, older Samsung Internet) the whole `background` declaration is dropped as invalid, but the transparent text fill is not, so every section heading in light theme renders **invisible**. The file uses `color-mix()` 87 times.
- **Suggested fix:** Give the headings a solid fallback (`color: var(--ink); -webkit-text-fill-color: currentColor;`) and apply the gradient + transparent fill only inside `@supports (color: color-mix(in srgb, red, blue)) { … }`. Add a fallback colour before each `color-mix()` border/background/shadow declaration.

#### GL-02 — Skip link / in-page anchors
- **Page / section:** Global / shared › Skip link / in-page anchors
- **File / line:** docs/assets/site.js:99-109; every page `<a class="skip" href="#main">` and `<main id="main">`
- **Category:** Accessibility (keyboard)
- **Severity:** **Major**
- **Problem:** The global anchor handler calls `e.preventDefault()` and scrolls with Lenis/`scrollIntoView`, but never moves focus or updates the URL. After activating “Skip to content” (or the footer “↑ Top” link) keyboard focus stays on the link, so the next Tab returns to the header nav – the skip link has no effect when JS is running. `<main>` has no `tabindex="-1"` so it could not receive focus anyway.
- **Suggested fix:** Add `tabindex="-1"` to `<main id="main">` (and any other anchor target) and, in the handler, call `t.focus({preventScroll:true})` after scrolling, plus `history.pushState(null,'',hash)`. Alternatively skip `preventDefault()` for `.skip` links.

#### GL-03 — Background flow diagrams (`.bgflow` SVGs)
- **Page / section:** Global / shared › Background flow diagrams (`.bgflow` SVGs)
- **File / line:** docs/assets/style.css:236, 2153; docs/assets/site.js:147-157; SVGs at index.html:47, 194, 258, 310, 387 and in every page-head
- **Category:** Animation / performance
- **Severity:** **Major**
- **Problem:** README (v24) claims background animation is paused off-screen via IntersectionObserver. It is not: the observer adds `.is-offscreen` to the `<svg class="bgflow">` element, but `.is-offscreen{animation-play-state:paused}` only affects that element. The running animations live on descendants – `.hero .bgflow .ln` (CSS `stroke-dashoffset`, non-compositor, repaints ~12 dashed paths every frame) and the SMIL `<animateMotion>` packets (2–4 per SVG, unaffected by CSS). Only `.marq-track` is actually paused. Index renders 6 animated SVGs; they all keep running while off-screen.
- **Suggested fix:** In the observer callback call `svg.pauseAnimations()` / `svg.unpauseAnimations()` and add `.is-offscreen .ln, .is-offscreen * {animation-play-state:paused}`. Consider limiting the dash animation to the hero or replacing it with a transform-based animation.

#### GL-04 — Decorative motion (no pause control)
- **Page / section:** Global / shared › Decorative motion (no pause control)
- **File / line:** docs/assets/style.css:297, 1043, 2721, 3464 (ping/pulse loops); SMIL in `.bgflow` SVGs; site.js:249
- **Category:** Animation / accessibility
- **Severity:** **Minor**
- **Problem:** Status dots, reply dot and flow packets animate indefinitely. Only the marquee has a pause button; `prefers-reduced-motion` is honoured (good) but there is no user control for others (WCAG 2.2.2 applies to auto-starting motion > 5 s, even decorative).
- **Suggested fix:** Stop looping pings after ~3 cycles (`animation-iteration-count: 3`) and give `.bgflow` a global pause toggle, or pause all decorative motion when the marquee toggle is pressed.

#### GL-05 — Preview drawer (`#previewDrawer`) – semantics
- **Page / section:** Global / shared › Preview drawer (`#previewDrawer`) – semantics
- **File / line:** docs/assets/site.js:641-673; markup e.g. index.html:399-486
- **Category:** Accessibility
- **Severity:** **Major**
- **Problem:** `role="dialog" aria-modal="true"` is set, but opening the drawer does not move focus into it, does not trap Tab, does not restore focus on close, does not make the page `inert`, and the title `#pdTitle` is always “Document Preview”. The tab strip uses `role="tablist"` but the buttons have no `role="tab"`, `aria-selected`, or `aria-controls`, and the panes have no `role="tabpanel"`. Keyboard users can Tab behind the open modal.
- **Suggested fix:** On open: store `document.activeElement`, focus the close button/dialog, set `inert` on `main`/header/footer, trap focus. On close: restore focus. Implement the full WAI-ARIA tabs pattern (roles, `aria-selected`, roving tabindex, arrow keys) and update `#pdTitle` per tab.

#### GL-06 — Preview drawer – scrolling with Lenis
- **Page / section:** Global / shared › Preview drawer – scrolling with Lenis
- **File / line:** docs/assets/site.js:641-652, 72-75; docs/assets/vendor/lenis.min.js; style.css:113
- **Category:** Functional bug (verify)
- **Severity:** **Major**
- **Problem:** Lenis is initialised without `allowNestedScroll`, and neither `.pd-body` nor any other nested scroller has `data-lenis-prevent`. `openDrawer()` only sets `body.style.overflow='hidden'` and never calls `lenis.stop()`. In Lenis’ default mode wheel events are intercepted and applied to the (locked) window, so mouse-wheel scrolling inside the drawer body is likely dead. (Verify in Chrome/Firefox with a mouse wheel.)
- **Suggested fix:** Add `data-lenis-prevent` to `#pdBody` (and `.tbl-wrap`, `pre` blocks), or init Lenis with `allowNestedScroll:true`; call `lenis.stop()` on open and `lenis.start()` on close.

#### GL-07 — Preview drawer – duplicated markup
- **Page / section:** Global / shared › Preview drawer – duplicated markup
- **File / line:** index.html:399-486, about.html:214-301, contact.html:77-164, services.html, projects.html, resume.html, 404.html:57, samples/index.html:181-268
- **Category:** Content / maintainability
- **Severity:** **Minor**
- **Problem:** The ~90-line drawer is generated into all 8 pages but only `samples/index.html` has `[data-preview]` triggers. On the other 7 pages it is dead, hidden DOM (~4 KB each) that crawlers and screen-reader “headings” lists can still see.
- **Suggested fix:** Emit the drawer only for `samples/index.html` in `build.py`.

#### GL-08 — Dead 3D-hero code (CSS + JS)
- **Page / section:** Global / shared › Dead 3D-hero code (CSS + JS)
- **File / line:** docs/assets/style.css (`.stage`, `.f3d`, `.plane*`, `.scene`, `.traffic*`, `.wf-step`, `.bar-stream`, `.step-arrow-link`, keyframes `sway`/`bob`/`stage-idle-float`, lines ≈300-420, 1892-1894, 2117-2123); docs/assets/site.js:202-216, 449-475, 595-606
- **Category:** 3D effects / maintainability
- **Severity:** **Minor**
- **Problem:** No page contains `.stage`, `[data-scene]`, `.f3d`, `.plane`, `.scene`, `.traffic-*`, `.wf-step`, `.bar-stream` or `.step-arrow-link`. The related CSS (~100 lines incl. infinite `bob`/`sway` keyframes), the data-scene pointer handlers, the traceability `stage` toggle and the hero scroll-linked `--plane-gap` code are unreachable. They add parse cost and make the “3D hero” described in README/comments appear to exist.
- **Suggested fix:** Delete the unused selectors, keyframes and JS blocks (or restore the hero stage if it was intended).

#### GL-09 — Colour tokens / contrast
- **Page / section:** Global / shared › Colour tokens / contrast
- **File / line:** docs/assets/style.css:3-90 (tokens), `.band` sections, `.eyebrow`
- **Category:** Color / accessibility
- **Severity:** **Minor**
- **Problem:** Computed WCAG ratios: dark `--accent #3b82f6` on `--soft #162036` = **4.41:1** (eyebrows, `.source-tag`, `.cat` on `.band` sections, <4.5); dark `.eyebrow b:hover` white on `--accent` = **3.68:1**; light `--danger #dc2626` on `--soft` = 4.41:1; light `--flow` / dark `--flow #475569` (2.3:1) only used decoratively (OK). `--amber` is declared but never used.
- **Suggested fix:** Use `--accent-2`/a lighter accent for small text on `--soft` in dark theme; use `--accent-ink` consistently for text on accent backgrounds; remove unused tokens.

#### GL-10 — Cascade hygiene
- **Page / section:** Global / shared › Cascade hygiene
- **File / line:** docs/assets/style.css – 179 `!important`; duplicate blocks at 126/133 (`p`), 1099 & 3326 (`.chip`), 1970 & 3419 (`@media print`), card transitions at ≈1935 & 2193
- **Category:** Maintainability
- **Severity:** **Minor**
- **Problem:** Later “spec” blocks re-declare earlier components with `!important` (cards, chips, nav buttons, print). Rules fight each other (e.g. `.card` transitions defined twice, hover lift −4 px vs −3 px, `.chip` styled twice) which makes behaviour order-dependent and caused the print and tilt bugs below.
- **Suggested fix:** Merge duplicate component blocks, remove `!important` except for utilities, split CSS per component and minify for production (file is 150 KB unminified).

#### GL-11 — Performance hints (3D tilt, blur, transitions)
- **Page / section:** Global / shared › Performance hints (3D tilt, blur, transitions)
- **File / line:** docs/assets/style.css:256 (will-change), 294 (`.hero::after` blur 90px), 373 & 2615 (blur 28px), 2510 (aurora anim); site.js:183-199
- **Category:** 3D effects / performance
- **Severity:** **Minor**
- **Problem:** Every `[data-tilt]` element (1–2 per page) carries permanent `will-change:transform` (persistent compositor layers); tilt handlers write 4 custom properties per `pointermove` with no `requestAnimationFrame` batching and repaint a `mix-blend-mode:soft-light` radial-gradient overlay; a 580 px element is blurred by 90 px; 7 rules use `transition: all`.
- **Suggested fix:** Apply `will-change` only while `.tilting`; throttle with rAF; drop the blend-mode overlay on large panels; replace `transition: all` with explicit properties.

#### GL-12 — Header / main navigation
- **Page / section:** Global / shared › Header / main navigation
- **File / line:** docs/assets/site.js:28-69; style.css:1855-1866; index.html:39-44
- **Category:** Responsiveness / accessibility
- **Severity:** **Minor**
- **Problem:** (a) Opening the mobile menu does not move focus into the menu. (b) At 821–~880 px the brand, 6 nav items (incl. bordered Resume button) and theme toggle are estimated at ~770 px against a 773 px container – likely to wrap or clip just above the 820 px breakpoint (verify). (c) `aria-label="Menu"` is static (fine) but the ☰ glyph is a text character that depends on font fallback.
- **Suggested fix:** Focus the first nav link on open; raise the breakpoint to ~900 px or reduce padding; replace `&#9776;` with an inline SVG.

#### GL-13 — Footer
- **Page / section:** Global / shared › Footer
- **File / line:** index.html:488 (all pages)
- **Category:** Content
- **Severity:** **Minor**
- **Problem:** Footer text hard-codes “Updated 2026.” while `data-year` is replaced at runtime with the current year, so the two will drift. Footer nav packs 11 links into one wrapping row including “↑ Top”.
- **Suggested fix:** Drop “Updated 2026.” or generate it in `build.py`; split footer into site links vs. social links.

#### GL-14 — Head / loading performance
- **Page / section:** Global / shared › Head / loading performance
- **File / line:** index.html:29-32 (all pages)
- **Category:** Performance
- **Severity:** **Minor**
- **Problem:** Google Fonts stylesheet (3 families, 8 weights/axes) and a 150 KB unminified `style.css?v=32` are render-blocking; `site.js` is 675 unminified lines. A `?v=32` query string is used for cache-busting but the build does not update it automatically.
- **Suggested fix:** Self-host/subset the fonts (`font-display:swap`), preload the 2 used weights, minify CSS/JS, and hash filenames in `build.py`.

#### GL-15 — Responsive overflow / small screens (verify at 320–360 px)
- **Page / section:** Global / shared › Responsive overflow / small screens (verify at 320–360 px)
- **File / line:** docs/assets/style.css:115 (`body{overflow-x:hidden}`), 421-423 (`.slider-tabs{flex-wrap:nowrap}`), 3254-3258 (flip cards), 1870-1890 (`.proof b{font-size:2.2rem}`)
- **Category:** Responsiveness
- **Severity:** **Minor**
- **Problem:** `body{overflow-x:hidden}` masks horizontal overflow instead of fixing it. Likely overflow/clipping candidates at ≤360 px: 4-tab hero slider + arrows in one non-wrapping row; “100K+” at 2.2 rem inside a ~94 px proof tile with `overflow:hidden`; flip cards with fixed `min-height:230px` and absolutely positioned faces; wireframe table (`wf-screen`) with 0.62 rem text.
- **Suggested fix:** Remove `overflow-x:hidden` from body during testing to find the offender(s); allow slider tabs to scroll (`overflow-x:auto`) or wrap; use `clamp()` for proof numerals.

#### GL-16 — Repository / deployment hygiene
- **Page / section:** Global / shared › Repository / deployment hygiene
- **File / line:** `repo root `assets/` (6 files) and docs/ (`build.py`, `flows.py`, `README.md`, `__pycache__/`)`
- **Category:** Maintainability / security
- **Severity:** **Minor**
- **Problem:** `docs/` is the published folder, so `build.py` (120 KB), `flows.py`, `README.md` and `__pycache__/*.pyc` are served publicly. Root `assets/` is not referenced by any page and holds duplicates (`363429418-….jpg` is byte-identical to `docs/assets/projects/Hr-data-analysis.png`) plus raw camera/screenshot files (`IMG_20231209_201205.jpg`, `Screenshot 2024-….jpg`). `.git/` was included in the zip.
- **Suggested fix:** Move build scripts out of `docs/` (e.g. `/tools`), delete unreferenced assets, remove `__pycache__`, and strip personal/camera files from the repo history if not intended to be public.

### Home page (`docs/index.html`)

#### IDX-01 — Hero › “Right now:” rotator
- **Page / section:** Home page › Hero › “Right now:” rotator
- **File / line:** index.html:51; site.js:219-233; style.css:300-305
- **Category:** Animation / accessibility
- **Severity:** **Major**
- **Problem:** All 7 phrases are in the DOM stacked in a grid (`aria-live="off"`), so screen readers read them as one run-on string with no separators. The visible phrase swaps every 3.2 s forever with no pause/stop control (WCAG 2.2.2).
- **Suggested fix:** Expose only the current phrase to AT (`aria-hidden="true"` on others) or render a static comma-separated list; pause on hover/focus and stop after one cycle; add a pause button if kept.

#### IDX-02 — Hero › deliverables slider (code blocks & tables)
- **Page / section:** Home page › Hero › deliverables slider (code blocks & tables)
- **File / line:** index.html:76-80, 139-145, 157-168; style.css:581, 588; slider panels `role="tabpanel"` at 74, 85, 106, 152
- **Category:** Accessibility (keyboard)
- **Severity:** **Major**
- **Problem:** `<pre class="schema-json">` and `<pre class="sql-view">` are `overflow-x:auto` scroll regions that cannot receive keyboard focus, and the `tabpanel`s have no `tabindex="0"`. Keyboard-only users cannot scroll the SQL/JSON when it overflows (WCAG 2.1.1).
- **Suggested fix:** Add `tabindex="0"` and an `aria-label` to each scrollable `<pre>`/`.tbl-wrap`, and `tabindex="0"` on tab panels that have no focusable content.

#### IDX-03 — Hero › slider controls
- **Page / section:** Home page › Hero › slider controls
- **File / line:** index.html:56-70; style.css:423-440; site.js:490-538
- **Category:** Alignment / responsiveness
- **Severity:** **Minor**
- **Problem:** Tabs are 32 px tall (`min-height:32px`) with `white-space:nowrap` in a non-wrapping flex row next to two arrow buttons – below the 44 px touch target used elsewhere and likely to overflow ≤360 px. The wrapper `div.hero-showcase-wrap` (line 56) carries an `aria-label` but no role (ignored) and duplicates the label on line 57.
- **Suggested fix:** Raise tab/arrow targets to ≥40–44 px, allow `overflow-x:auto` on the tab strip, remove the duplicate `aria-label`.

#### IDX-04 — Hero › PayTrack traceability table
- **Page / section:** Home page › Hero › PayTrack traceability table
- **File / line:** index.html:77-79; site.js:447-475; style.css:2162-2170
- **Category:** Accessibility / UX
- **Severity:** **Minor**
- **Problem:** Rows are `tabindex="0"` with `cursor:pointer` but are not buttons: no role, no accessible name for the interaction, and the “linked IDs” highlight is purely visual so AT users get nothing from focusing a row. Mouse click does nothing (only hover/touch).
- **Suggested fix:** Either remove `tabindex` and keep it decorative, or expose the relationship (e.g. `aria-describedby` listing linked IDs / visually-hidden text) and drop `cursor:pointer`.

#### IDX-05 — Hero & wireframe › tiny type
- **Page / section:** Home page › Hero & wireframe › tiny type
- **File / line:** style.css:553, 573, 578 (`.kwd-tag`, `.node-verb`, `.node-detail` = .66 rem ≈ 10.5 px); 1003, 1010-1015 (`.wf-kpi-lbl`, `.wf-th` = .62 rem ≈ 10 px)
- **Category:** Content / readability
- **Severity:** **Minor**
- **Problem:** Mono labels in the slider and PayTrack wireframe are rendered at 10–10.5 px, below common 12 px minimums and unreadable when the UI is shown scaled down on phones.
- **Suggested fix:** Set a 0.75 rem (12 px) floor; use `clamp()` rather than fixed tiny sizes.

#### IDX-06 — Marquee (skills ticker)
- **Page / section:** Home page › Marquee (skills ticker)
- **File / line:** index.html:178-180; site.js:235-246; style.css:598-614
- **Category:** Accessibility
- **Severity:** **Minor**
- **Problem:** The toggle sets both `aria-pressed` and changes `aria-label` (“Pause marquee”/“Play marquee”), so a screen reader announces e.g. “Play marquee, toggle button, pressed” – contradictory. The first `<ul>` is exposed to AT as a 12-item list while the second is hidden.
- **Suggested fix:** Use a constant label (“Pause skills ticker”) with `aria-pressed`, or change only the label and drop `aria-pressed`.

#### IDX-07 — Proof cards
- **Page / section:** Home page › Proof cards
- **File / line:** index.html:186-189; site.js:159-180
- **Category:** Content / design
- **Severity:** **Minor**
- **Problem:** The bars (`--val:92% / 100% / 80% / 85%`) have no scale or meaning (100K+ records = 92%?) yet imply measurement; counters animate from 0 so values are briefly wrong/unannounced, and the same metrics (350+, 100K+, 20+, 2) are repeated in hero line (54), proof, method chips, toolkit tooltips and experience.
- **Suggested fix:** Remove the bars or bind them to a real scale; show final numbers in HTML and animate only visually; de-duplicate repeated metrics.

#### IDX-08 — Selected work › PayTrack wireframe
- **Page / section:** Home page › Selected work › PayTrack wireframe
- **File / line:** index.html:261-297 (badge at 266, rows at 290-292); site.js:611-621
- **Category:** Content / animation
- **Severity:** **Minor**
- **Problem:** The static HTML mock is badged “Live Prototype” (and addressed `ops.paytrack.internal`) which contradicts the site’s own “fictional, no live system” disclaimers; its table rows auto-cycle every 2.4 s forever with no pause; the wrapper has `aria-label` but no role; three gateways are shown (Stripe, Razorpay, Adyen) while the copy says “2 payment gateways”.
- **Suggested fix:** Rename the badge to “Illustrative mock-up”, stop cycling after one loop or on hover/focus, and make the gateway count consistent.

#### IDX-09 — Selected work › project thumbnails
- **Page / section:** Home page › Selected work › project thumbnails
- **File / line:** index.html:303-305; style.css:894-902; assets/projects/Sales-data-analysis.jpg (1024×257), Loan-data-analytics.jpg (1024×411), Sales-Forecasting-Report.jpg (1024×577)
- **Category:** Content / layout
- **Severity:** **Major**
- **Problem:** Thumbnails sit in a `16/10` box with `object-fit:cover`, but the source screenshots are 4:1 (Sales, 1024×257), 2.5:1 (Loan, 1024×411) and ~16:9 (Forecasting, 1024×577) while the markup declares 1200×600. The 4:1 Sales image is cropped to roughly its centre 40 % (left/right parts of the chart are cut off), the 2.5:1 Loan image to ~64 %, and the hover `scale(1.05)` crops further. (The same assets repeat on projects.html.)
- **Suggested fix:** Export purpose-made 16:10 thumbnails (≥1200×750, WebP/AVIF + `srcset`), update `width/height`, and set meaningful `object-position`.

#### IDX-10 — Selected work › card grid
- **Page / section:** Home page › Selected work › card grid
- **File / line:** index.html:302-307
- **Category:** Alignment
- **Severity:** **Minor**
- **Problem:** Stagger delays are `0s / .14s / .28s` (everywhere else `.07s` steps), and at 641–1000 px the `g3→2-col` rule leaves the third card alone on a row.
- **Suggested fix:** Use the shared 0.07 s step; centre or span the orphan card.

#### IDX-11 — Skills & delivery toolkit › tooltips
- **Page / section:** Home page › Skills & delivery toolkit › tooltips
- **File / line:** index.html:312-366; style.css:2413-2430
- **Category:** Content / accessibility
- **Severity:** **Major**
- **Problem:** Each tile carries evidence (e.g. “Prioritized requirements across 4 modules and challenged 3 feature requests lacking business justification”, ~105 chars) shown only via `::after{content:attr(data-tooltip); white-space:nowrap}` on hover/focus-visible. The bubble is ~700 px wide, centred over a tile inside a 2-column card, so it is clipped by `.sec.has-flow{overflow:hidden}` / the viewport; it never appears on touch devices; generated content is not reliably announced; tiles are `tabindex="0"` with no role so keyboard users land on non-interactive stops.
- **Suggested fix:** Allow wrapping (`white-space:normal; width:max-content; max-width:min(320px,80vw)`), clamp position within the card, and expose the text as real DOM (`aria-describedby` + visually-hidden span) or use a button that toggles a popover for touch.

#### IDX-12 — Skills & delivery toolkit › icons
- **Page / section:** Home page › Skills & delivery toolkit › icons
- **File / line:** index.html:367, 373, 382
- **Category:** Content / design
- **Severity:** **Minor**
- **Problem:** “Figma & Postman” uses a circle-slash (prohibited) icon; “REST API Specs” and “Python (Pandas)” both use the same code-brackets icon, so icons do not discriminate.
- **Suggested fix:** Use distinct, meaningful icons (design/pen, API/plug).

#### IDX-13 — Experience timeline
- **Page / section:** Home page › Experience timeline
- **File / line:** index.html:390-393; site.js:626-636
- **Category:** Accessibility / content
- **Severity:** **Minor**
- **Problem:** “View key metrics” buttons lack `aria-controls` and swap `innerHTML` including `▾/▴` text glyphs read aloud. Bullets all follow the template “Accomplished X, as measured by Y, by Z” (9+ times across index/about/resume) at 30–45 words each, which reads robotic.
- **Suggested fix:** Add `aria-controls`/ids, render chevrons as CSS/SVG, and rewrite bullets in a concise result-first form (≤25 words).

#### IDX-14 — Content consistency across home / about / samples
- **Page / section:** Home page › Content consistency across home / about / samples
- **File / line:** index.html:90, 98, 156-168; about.html:106, 125; samples/index.html:207; drawer BRD (index.html:419)
- **Category:** Content
- **Severity:** **Major**
- **Problem:** The same fictional PayTrack spec contradicts itself: SLA is “5 minutes” (story), “4-hour SLA timer” (Gherkin/SQL), “30-minute SLA window” (about.html:125) and “48-hour SLA breach” (samples:207, BRD “up to 48 hours”); `BR-01` is “Single operational view” on home but “API Idempotency & Duplicate Handling” on About; the SQL counts rows >3 h while the comment says 4 h. For a BA portfolio, traceability inconsistencies undermine credibility.
- **Suggested fix:** Define one source of truth (e.g. the sample CSVs) and generate all snippets from it in `build.py`; unify IDs, SLAs and gateway counts.

### About page (`docs/about.html`)

#### ABT-01 — BA Specification Console › colour
- **Page / section:** About page › BA Specification Console › colour
- **File / line:** style.css:2702, 2793, 2842, 2899, 2947, 2995, 3038, 3142, 3153
- **Category:** Color / accessibility
- **Severity:** **Major**
- **Problem:** Hard-coded colours bypass the tokens and fail AA in light theme on the white/`#f1f5f9` console: `#10b981` badge/pill text = **2.32:1**, `#3b82f6` (active tab, `BR-xx` codes, spec keyword, impact labels, footer link) = **3.36:1**, `#0284c7` tag = 3.74:1, `#dc2626` tag 4.41:1; `.cfoot-link:hover #60a5fa` drops to 2.32:1. Text is 10–13 px.
- **Suggested fix:** Replace with `var(--accent-text)`, `var(--ok)`, `var(--danger)` tokens (all ≥4.5:1 on these surfaces) and keep hover states at least as dark.

#### ABT-02 — Console tabs
- **Page / section:** About page › Console tabs
- **File / line:** about.html:90-94; site.js:559-590
- **Category:** Accessibility
- **Severity:** **Minor**
- **Problem:** Inactive tabs have no `tabindex="-1"` in the markup and JS only sets it after the first click, so before interaction all three tabs are tab stops (roving-tabindex violated). Panels are not focusable, and Home/End are not handled.
- **Suggested fix:** Set `tabindex="-1"` on inactive tabs in HTML/at init; add Home/End and `tabindex="0"` on panels.

#### ABT-03 — Career path
- **Page / section:** About page › Career path
- **File / line:** about.html:205-210 vs index.html:389-394
- **Category:** Content
- **Severity:** **Minor**
- **Problem:** Career-path text duplicates the home Experience bullets almost verbatim (and again in resume.html), creating thin/duplicate content across three URLs. “Promoted early” badge and “17 months” rely on an unexplained baseline.
- **Suggested fix:** Make About narrative (why/how) and keep metrics only on Resume; state the normal promotion timeline or drop “early”.

### Services page (`docs/services.html`)

#### SVC-01 — Service cards (category colours)
- **Page / section:** Services page › Service cards (category colours)
- **File / line:** `services.html:49, 61, 73, 85, 97; style.css:3193, 3200, 3237`
- **Category:** Functional bug / HTML validity
- **Severity:** **Major**
- **Problem:** Each card has two `style` attributes: `<div class="card scard rv" style="--d:0.00s" style="--cat-c:var(--c-brd)">`. HTML parsers keep only the first, so `--cat-c` is never set and all five cards fall back to `--accent` – the intended per-category colour system (top border, badge, bullets) is lost, and the page fails validation.
- **Suggested fix:** Merge into one attribute (`style="--d:0s;--cat-c:var(--c-brd)"`) in the `build.py` card template.

#### SVC-02 — “What you receive” flip cards
- **Page / section:** Services page › “What you receive” flip cards
- **File / line:** `services.html:180-212; style.css:3254-3300`
- **Category:** 3D effects / accessibility / responsiveness
- **Severity:** **Major**
- **Problem:** Cards flip only on `:hover`/`:focus-within`; “tap to flip” depends on emulated sticky hover (unreliable on iOS, un-flips when tapping elsewhere). Both faces stay in the accessibility tree and the back-face link is focusable while visually hidden (`backface-visibility` only). Faces are `position:absolute` inside a `min-height:230px` box, so copy longer than the box (narrow screens, 200 % zoom, larger text) overflows/clips. `div tabindex="0"` has no role/name.
- **Suggested fix:** Replace with a real `<button aria-expanded>` toggle (or drop the flip and show both faces), mark the hidden face `aria-hidden`/`inert`, and stack faces in a grid cell so height is content-driven.

#### SVC-03 — Flip cards › content & links
- **Page / section:** Services page › Flip cards › content & links
- **File / line:** `services.html:189, 205, 221 (+ href of card 2, `…index.html#process-flow`)`
- **Category:** Content / links
- **Severity:** **Minor**
- **Problem:** Back faces are labelled “ARTIFACT THUMBNAIL” but show no thumbnail; card 2 names `Payment_API_Sequence.svg` yet “Open artifact” links to `#process-flow` (the reconciliation process) instead of `#rest-api`; card 3 shows `04_RTM_Test_Cases_UAT_Plan.pdf` but the real file is `…_Sample.pdf`.
- **Suggested fix:** Show a real thumbnail image, correct the anchor to `#rest-api`, and use the exact filenames.

#### SVC-04 — Service grid / FAQ
- **Page / section:** Services page › Service grid / FAQ
- **File / line:** `services.html:48-120, 232-235`
- **Category:** Alignment / content
- **Severity:** **Minor**
- **Problem:** Five cards in a 3-column grid leave an empty cell; FAQ answer “My resume shows work alongside…” is awkward third-person phrasing on a first-person site; `summary{list-style:none}` removes the disclosure marker – verify a custom indicator exists in every browser.
- **Suggested fix:** Use 2+3 or 3+2 centred layout; rewrite FAQ in first person; add `summary::-webkit-details-marker{display:none}` plus a visible chevron.

### Projects page (`docs/projects.html`)

#### PRJ-01 — Project filter
- **Page / section:** Projects page › Project filter
- **File / line:** `projects.html:74-79; site.js:251-325; style.css:1098, 3316-3345`
- **Category:** Functional bug (verify) / animation
- **Severity:** **Major**
- **Problem:** (a) The sliding pill is positioned with only `translateX(offsetLeft)` and set once after 50 ms (before webfonts swap); `.filters` is `flex-wrap:wrap`, so on phones where six chips wrap to 2–3 rows the pill sits on row 1 behind the wrong chip. (b) The FLIP routine leaves inline `style.transition` on every card permanently, overriding the stylesheet’s hover/shadow transitions. (c) Chips are `!important`-styled twice (1099 and 3326) with no visible active state other than the pill.
- **Suggested fix:** Position the pill with `offsetTop` as well (or use per-chip active background), recalculate after `document.fonts.ready`, and clear inline `transition/transform` on `transitionend`.

#### PRJ-02 — Project thumbnails (assets)
- **Page / section:** Projects page › Project thumbnails (assets)
- **File / line:** `projects.html:82-90; assets/projects/*`
- **Category:** Content / performance
- **Severity:** **Minor**
- **Problem:** `Hr-data-analysis.png` is actually a JPEG (1998×1096, wrong extension), `ClinChat-style-RAG-app.png` is 2537×1240 PNG (133 KB) displayed ~370 px wide, and all `<img>` use `width="1200" height="600"` regardless of intrinsic size; no `srcset`/WebP. Alt text is the generic “Title • Category” (inside `aria-hidden` links, so effectively unused).
- **Suggested fix:** Re-export with correct extensions/dimensions, serve WebP/AVIF with `srcset`, and set accurate `width/height`.

#### PRJ-03 — Featured case study card (tilt)
- **Page / section:** Projects page › Featured case study card (tilt)
- **File / line:** `projects.html:49; style.css:1922 (`.feature:hover{transform:…}`), ≈2193-2205 (`.feature` transition/box-shadow `!important`)`
- **Category:** 3D effects (verify)
- **Severity:** **Minor**
- **Problem:** `.feature.featured-paytrack` has `data-tilt`, but `.feature:hover{transform:translateY(-4px)}` (same specificity, declared later) overrides the tilt transform and the `!important` shadow/transition list overrides the `.tilting` glow, so the 3D tilt is likely inert on this card.
- **Suggested fix:** Exclude `[data-tilt]` from the generic hover-lift selectors or raise specificity (`[data-tilt].tilting`).

#### PRJ-04 — Featured card › file links
- **Page / section:** Projects page › Featured card › file links
- **File / line:** `projects.html:66-70`
- **Category:** UX / accessibility
- **Severity:** **Minor**
- **Problem:** The ERD image link and the three PDF links open raw `.svg`/`.pdf` files in the same tab, losing site chrome; PDF links show a “PDF” badge but no file size or new-tab hint.
- **Suggested fix:** Open in a new tab with `rel="noopener"` + sr-only “(opens in new tab)”, or route through the samples viewer.

### Resume page (`docs/resume.html`)

#### RSM-01 — Print / Save as PDF (“ATS-friendly”)
- **Page / section:** Resume page › Print / Save as PDF (“ATS-friendly”)
- **File / line:** resume.html:48; style.css:1970-2116 and 3419-3441
- **Category:** Functional bug
- **Severity:** **Major**
- **Problem:** Two `@media print` blocks conflict. The later one hides `.resume-sidebar` and `.proof`, so the printed/saved ATS PDF **omits the entire Skills & Expertise and Tools section** (and the metrics strip) – the part ATS parsers key on. The button also uses an inline `onclick="window.print()"` (blocks a strict CSP).
- **Suggested fix:** Merge print rules into one block, keep `.resume-sidebar` (render as a normal section), and bind the handler in `site.js`.

#### RSM-02 — Skills sidebar (sticky)
- **Page / section:** Resume page › Skills sidebar (sticky)
- **File / line:** style.css:3381 (`.resume-sidebar{position:sticky;top:96px}`), 186 (`.has-flow{overflow:hidden}`); resume.html:58, 70
- **Category:** Functional bug / layout
- **Severity:** **Minor**
- **Problem:** The sidebar is inside `section.has-flow`, whose `overflow:hidden` makes it the sticky container, so the sidebar never sticks while scrolling; at ≤900 px the layout is one column and `sticky` is meaningless.
- **Suggested fix:** Use `overflow:clip` on `.has-flow` (keeps clipping without creating a scroll container) and set `position:static` below 900 px.

#### RSM-03 — Experience (missing content)
- **Page / section:** Resume page › Experience (missing content)
- **File / line:** resume.html:62-64 (also index.html:389-394, about.html:205-210)
- **Category:** Content (missing)
- **Severity:** **Major**
- **Problem:** None of the four roles shows a start/end date or tenure – the `.org` line only has company and city (education does show 2016–2020). A resume page without employment dates is incomplete for recruiters and ATS parsing, and the skill durations in the sidebar (“API & System Integration 3+ yrs”, “BI & Reporting 3+ yrs”) cannot be checked against the timeline. Also: “Metrics come from my resume…” (line 55) is self-referential on the resume page, and “In progress: CBAP (IIBA)” has no target date.
- **Suggested fix:** Add date ranges (e.g. “Mon YYYY – Mon YYYY”) to every role on all three pages, align skill durations with them, remove the self-referential note and add an expected date for CBAP.

### Contact page (`docs/contact.html`)

#### CNT-01 — Enquiry form › field borders
- **Page / section:** Contact page › Enquiry form › field borders
- **File / line:** style.css:3471-3483 (`border:1.5px solid var(--line)`); contact.html:60-70
- **Category:** Color / accessibility
- **Severity:** **Major**
- **Problem:** Input/select/textarea borders use `--line` against the same surface colour: `#e2e8f0` on `#fff` = **1.23:1** (light), `#1e293b` on `#111827` = **1.21:1** (dark). Fields are nearly invisible and fail WCAG 1.4.11 (3:1 for UI component boundaries).
- **Suggested fix:** Use a border of ≥3:1 against the surface (e.g. `#64748b` light / `#64748b`–`#94a3b8` dark) or add a tinted field background.

#### CNT-02 — Enquiry form › validation styling
- **Page / section:** Contact page › Enquiry form › validation styling
- **File / line:** style.css:3498, 3504-3507; contact.html:63, 66-67, 70
- **Category:** Functional bug / color
- **Severity:** **Minor**
- **Problem:** `input:valid` paints a green border on pristine **optional** fields (Company, Reference link) at page load, while empty required fields look neutral. `select:valid ~ label` makes the label of the non-required selects (Engagement type, Target timeline) permanently floated over an empty box. `aria-invalid` is only set on submit and never cleared on input.
- **Suggested fix:** Use `:user-valid`/`:user-invalid` or a `.touched` class; float labels via `:has(option:checked:not([value=""]))`; clear `aria-invalid` on `input`.

#### CNT-03 — Enquiry form › ARIA
- **Page / section:** Contact page › Enquiry form › ARIA
- **File / line:** `contact.html:58, 60-70; site.js:356-403`
- **Category:** Accessibility
- **Severity:** **Minor**
- **Problem:** The error summary is `role="alert" aria-live="polite"` (conflicting) and every `.err` span is also `aria-live="polite"`, so one failed submit is announced by the summary plus up to 4 field messages. Summary does not link to the fields. Error text always says “valid work email” though any address is accepted (label “Work email *” also excludes personal addresses).
- **Suggested fix:** Keep `role="alert"` only on the summary, remove `aria-live` from field errors, link summary items to fields, and relabel to “Email”.

#### CNT-04 — Enquiry form › submit flow
- **Page / section:** Contact page › Enquiry form › submit flow
- **File / line:** site.js:392-424; contact.html:71-72
- **Category:** Functional bug / UX
- **Severity:** **Major**
- **Problem:** Submit builds a `mailto:` URL and immediately reveals “Preparing your email draft…”. With no default mail client (many desktop and webmail users) nothing opens, yet the page implies progress; long messages can exceed mailto URL limits (~2,000 chars in common clients) and are silently truncated. “Copy message” is a silent no-op when `navigator.clipboard`/secure context is unavailable and has no `.catch`; its label change is not announced.
- **Suggested fix:** Offer a fallback (textarea with the composed message + “Open in Gmail” link) and a real form backend (Formspree/Netlify) if possible; add `.catch` and `aria-live` feedback to copy.

#### CNT-05 — Contact details
- **Page / section:** Contact page › Contact details
- **File / line:** `contact.html:49, 64-67`
- **Category:** Content / accessibility
- **Severity:** **Minor**
- **Problem:** “Typically replies within 24 hours” is an unverifiable promise next to a perpetually pulsing dot (style.css:3464); the selects’ first option is empty (`<option value="" disabled selected hidden></option>`) so iOS shows a blank row and the control has no visible placeholder.
- **Suggested fix:** Reword (“I aim to reply within 1–2 working days”), stop the pulse, and give the placeholder option text (“Select…”).

### BA Samples page (`docs/samples/index.html`)

#### SMP-01 — Preview drawer › RTM pane (also in drawers on all pages)
- **Page / section:** BA Samples page › Preview drawer › RTM pane (also in drawers on all pages)
- **File / line:** `samples/index.html:246-250 (same markup index.html:464-469, about.html:279-284, contact.html:142-147 …)`
- **Category:** Content (integrity)
- **Severity:** **Critical**
- **Problem:** The RTM extract shows **“UAT Status: PASS”** for BR-01/02/03, and the BRD/FRD panes say “Status: Approved / Baselined”. The page itself (line 48), projects.html:49 and README state that test cases are **Not Run** and “no executed-test evidence is claimed”. A visitor (or recruiter) opening the preview sees fabricated execution results presented as fact.
- **Suggested fix:** Change to “Not Run” (matching `sample_test_cases.csv`) and “Draft – sample” for document status, or generate the pane from the CSV.

#### SMP-02 — Documentation bundle item
- **Page / section:** BA Samples page › Documentation bundle item
- **File / line:** `samples/index.html:54-61 (`<p>` wrapping `<div class="bundle-fan">`)`
- **Category:** HTML validity / layout
- **Severity:** **Minor**
- **Problem:** A `<div>` inside a `<p>` auto-closes the paragraph; the orphan `</p>` creates an empty paragraph with margin, adding stray space under the fan graphic.
- **Suggested fix:** Close the `<p>` before the `<div>` (or change the wrapper to `<div>`).

#### SMP-03 — Document / diagram / data link lists
- **Page / section:** BA Samples page › Document / diagram / data link lists
- **File / line:** `samples/index.html:64-210`
- **Category:** Accessibility
- **Severity:** **Minor**
- **Problem:** Link names are bare “PDF”, “Word”, “SVG”, “PNG”, “Mermaid”, “CSV”, “SQL” repeated ~25 times, so a screen-reader link list is indistinguishable (WCAG 2.4.4). `target="_blank"` PDF/SVG links lack the “(opens in new tab)” text used elsewhere; `.mmd` files have no MIME handling on GitHub Pages (open as raw text or download unpredictably).
- **Suggested fix:** Add `aria-label="Business Requirements Document, PDF"` (or sr-only text) to each, add new-tab hints, and consider `download` attributes for `.docx/.mmd/.sql`.

#### SMP-04 — Power BI dashboard item
- **Page / section:** BA Samples page › Power BI dashboard item
- **File / line:** `samples/index.html:147-158`
- **Category:** Content
- **Severity:** **Major**
- **Problem:** The row advertises a “Power BI reconciliation & operations dashboard … DAX measures and executive dashboard views” for PayTrack, but its only links go to `projects.html#bi` and the unrelated `Hr-data-analysis` GitHub repo. No such artifact exists, which misrepresents the case-study scope.
- **Suggested fix:** Add the actual PayTrack `.pbix`/screenshots or remove the row / label it “Not included”.

#### SMP-05 — Quick preview button
- **Page / section:** BA Samples page › Quick preview button
- **File / line:** `samples/index.html:64; site.js:642-647`
- **Category:** Content / accessibility
- **Severity:** **Minor**
- **Problem:** The button label includes the 👁 emoji (read aloud as “eye”), and “Quick In-Page Preview” for the *bundle* opens the BRD tab with a 2-paragraph excerpt, not the bundle.
- **Suggested fix:** Remove the emoji (use an SVG with `aria-hidden`), and either preview the actual PDF (`<object>`/PDF.js) or rename to “Preview excerpts”.

#### SMP-06 — 3D page-fan graphic & external links
- **Page / section:** BA Samples page › 3D page-fan graphic & external links
- **File / line:** style.css:3518-3570 (`.bundle-fan` 150 px fixed height, `perspective:700px`); samples/index.html:164, 173 (Figma / FigJam)
- **Category:** 3D effects / links
- **Severity:** **Minor**
- **Problem:** The fan uses five absolutely positioned 110×140 px docs in a fixed 150 px container – verify it does not overlap the heading/text at ≤360 px. The Figma and FigJam URLs could not be tested offline; confirm they are public (“anyone with the link can view”).
- **Suggested fix:** Test at 320–360 px; verify external share permissions.

### 404 page (`docs/404.html`)

#### E-01 — Absolute production URLs
- **Page / section:** 404 page › Absolute production URLs
- **File / line:** 404.html:34-46 (CSS/JS/links all `https://reddygautam98.github.io/GautamTheAnalyst.io/…`)
- **Category:** Maintainability / functional
- **Severity:** **Minor**
- **Problem:** The 404 template hard-codes absolute production URLs for CSS, JS, images and nav links (correct for GitHub Pages’ arbitrary-depth 404, but) local/staging previews load production assets and ignore uncommitted changes; the page also ships the full 90-line preview drawer.
- **Suggested fix:** Emit root-relative URLs (`/GautamTheAnalyst.io/…`) or a `<base>` tag controlled by a build flag, and omit the drawer.
