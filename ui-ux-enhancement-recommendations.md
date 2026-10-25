# ui/ux Enhancement Recommendations — GautamTheAnalyst.io

**Reviewer role:** Senior ui/ux developer
**Source reviewed:** `31971f2e-GautamTheAnalyst.io.zip` (static GitHub Pages site, published from `docs/`)
**Method:** Rendered every page at 1440 px (desktop) and 390 px (mobile), then read `docs/assets/style.css`, `docs/assets/site.js` and the generated HTML. No testing on real devices and no external-link checks.
**Design preferences supplied:** none beyond what the code states (blueprint look, light/dark theme, "professional, not flashy"). Anything I could not confirm is marked `[PLACEHOLDER]`.

---

## 0. What the site already does well (keep)

- **Palette and tokens.** Blue-slate blueprint palette (`--accent:#2563eb`, `--ink:#0f172a`, `--bg:#f8fafc`), full dark theme, semantic status tokens (approved / review / draft / not-run).
- **Type system.** Serif headings (`Source Serif 4`), sans body (`IBM Plex Sans`), mono labels (`IBM Plex Mono`). It reads as "analyst + engineer", which suits the positioning.
- **Motion discipline.** Motion tokens, `prefers-reduced-motion` handling, an animation pause button and a marquee pause control.
- **Content honesty.** Fictional PayTrack material is labelled "Illustrative / Fictional sample" throughout. Keep this.
- **Original ideas worth leaning into:** the interactive traceability widget in the hero, the BR→FR→US→TC mapping, and the method timeline.

## 1. Cross-cutting recommendations (all pages)

### 1.1 Colour and accessibility
| Observation | Recommendation |
|---|---|
| Card top-borders rotate through blue, indigo, teal, green and amber for decoration. | Give **one meaning per colour** (e.g. blue = requirements, indigo = specs, green = testing, amber = risk/SLA) and reuse it across cards, timeline dots and sample tags. Tokens `--c-brd`, `--c-frd`, `--c-story`, `--c-test`, `--c-sql`, `--c-api` already exist; apply them consistently. |
| Gradient text on headings and the hero highlight. | Keep gradient on the single hero keyword only. Use solid `--ink` for other `h2`s. |
| Stat numbers are green regardless of meaning. | Use green only for "achieved / pass" values; use `--ink` for neutral counts. |
| Dark mode is well structured (3-surface hierarchy). | Add a visible auto / light / dark choice so OS-dark visitors know they are following the system. |

### 1.2 Typography
- Load only the weights actually used. The Google Fonts link requests `Source Serif 4` at weight 600 only; confirm any regular-weight serif text falling back to Georgia is intentional. The "Who I am" heading on About renders in sans, unlike other headings.
- Use a fluid scale with `clamp()` for `h1 / h2 / h3 / lead` (see the mobile hero in 2.2).
- Reserve mono for IDs and data (BR-01, TC-001, SQL). It currently also appears on eyebrows, facts, chips and KPI labels, which dilutes its "spec artifact" meaning.

### 1.3 Animation and transitions
- Current inventory: scroll reveals (`.rv`), count-up stats, marquee, ping/pulse dots, animated flow lines in section backgrounds, icon hover tilt, and a view-transition fade between pages.
- **Rationalise into three tiers:**
  1. *Structural* (page-load stagger, reveal on scroll): 250–450 ms, ease-out, once only.
  2. *Interactive feedback* (hover, focus, tab change): 120–200 ms.
  3. *Ambient* (marquee, flowing lines, pulses): at most one loop visible per viewport, all covered by the existing pause toggle.
- Persist the animation-pause choice in `localStorage` (wrapped in try/catch) so it survives page changes.
- Apply `will-change: transform` only during active hover/tilt.

### 1.4 3D effects
- Present: pointer-driven card tilt (`data-tilt`, `--tilt-max:4deg`), the perspective-tilted hero "stage" with layered planes, and 3D pop on small icons (rotateX/rotateY of 12–20° with scale 1.18–1.35).
- **Keep 3D for the hero stage and the featured case study only.** Replace the small-icon rotation with a 2 px lift plus a colour or outline change; the current effect is playful against an otherwise serious layout.
- Lower `--tilt-max` to 2–3 deg and add a soft highlight that follows the pointer.
- Confirm tilt is fully disabled on touch and under reduced motion (a `hover:none` rule exists; check it covers `.stage` and all `data-tilt` children).

### 1.5 Layout, spacing and responsiveness
- `--w:1160px` content width is sensible. Standardise section rhythm on `--space-section`.
- Add a spacing scale as tokens (4 / 8 / 12 / 16 / 24 / 32 / 48 / 64); several components use ad-hoc gaps (the contact form is the clearest case, section 7).
- Test at 320, 390, 768, 1024, 1440 and 1920 px.

### 1.6 Overall polish
- Use one section pattern everywhere: eyebrow (number + label) → title → one-line intro → content → single link. The home page does this; inner pages are less consistent.
- Add a thin scroll-progress bar under the header on long pages (resume, samples).
- Use one `:focus-visible` style site-wide (2 px outline, 2 px offset, accent colour) and check it in dark mode.

---

## 2. Home page — `docs/index.html`

### 2.1 Header / navigation
- **Observed:** logo mark + name, five text links, a highlighted "Resume" button, animation toggle and theme toggle.
- **Enhance:**
  - Shrink the sticky header slightly (68 px → about 56 px) after scrolling, with a hairline border appearing.
  - The two icon buttons have no visible text. Add tooltips on hover/focus and text labels inside the mobile menu.
  - Add scroll-spy highlighting for in-page sections on the home page.

### 2.2 Hero
- **Observed (desktop):** strong two-column hero. Large serif H1 with one coloured keyword ("testable specs."), availability pill, role/location/focus fact box, two CTAs, and a tabbed artifact preview (Traceability / User story / REST API / SQL logic).
- **Observed (mobile, 390 px):** the lead paragraph is very large and long; the preview tab labels truncate ("Trac...", "User...", "RES...", "SQL l..."); the traceability table clips on the right so the Tests column is cut off.
- **Enhance:**
  1. **Mobile type:** cap `.hero .lead` with `clamp(1rem, 3.8vw, 1.15rem)` and shorten the copy. The same facts (role, location, years, test count) appear in the lead, the fact box and the proof line; keep each fact in one place.
  2. **Mobile preview:** make the tabs a horizontally scrollable pill row with `scroll-snap`, and let the table scroll inside its own container with a fade-edge hint. Below about 480 px, a card-per-requirement layout is an alternative.
  3. **Hierarchy:** merge "Specializing in", the fact box and the proof line into one compact row of three facts. Keep one primary CTA ("View BA samples") and one secondary ("View resume").
  4. **Animation:** stagger H1 → lead → CTAs → preview on load (about 80 ms steps). Add a one-time row-highlight sweep in the traceability table (BR → FR → US → TC) that then stays interactive. It demonstrates traceability without extra decoration.
  5. **3D:** keep the stage tilt; give it a soft shadow that shifts opposite to the tilt.
  6. **Imagery:** add a small portrait or monogram near the availability pill `[PLACEHOLDER: photo or approved avatar — not provided]`.

### 2.3 Skills marquee
- **Observed:** scrolling keyword pills with a pause button; the first pill is cut off at the left edge.
- **Enhance:** add edge-fade masks (`mask-image: linear-gradient(90deg, transparent, #000 8%, #000 92%, transparent)`), slow it down, and pause on hover/focus. Consider hiding it on mobile; the same skills appear again in the Skills section.

### 2.4 Proof (01)
- **Observed:** four stat cards (100K+, 350+, 20+, 2) with coloured top borders, mono labels and short descriptions; a footnote says the figures come from past delivery records.
- **Enhance:**
  - Run the count-up once, when the cards are about 60% visible.
  - Use sentence-case labels; the all-caps mono labels wrap awkwardly on mobile ("MAROLIX • SQL ANALYSIS" breaks over three lines).
  - Put the source (employer / project) on each card instead of in a footnote only.
  - Add sparklines or icons only if real data exists `[PLACEHOLDER: no time-series data provided]`.

### 2.5 Method (02) — "How a requirement travels"
- **Observed:** four phase cards (Discover / Define / Validate / Hand over) with a glowing dot and a metric per phase.
- **Enhance:**
  - Turn it into a connected horizontal stepper whose connector line draws on scroll (SVG `stroke-dashoffset`) and lights each phase on hover/focus.
  - Link each phase to the matching sample document.
  - On mobile, switch to a vertical timeline, matching the experience timeline.

### 2.6 Selected work (03)
- **Observed:** large featured PayTrack case study with an illustrative mock-up, a Problem / Role / Result box, a fictional-sample callout, then three project cards with screenshots, "What I did / Tools / Outcome" blocks and tags.
- **Enhance:**
  - Present Problem → Role → Result as three stacked rows with hairline dividers instead of one tinted box with mono headings.
  - Use a fixed 16:10 frame for thumbnails (`object-fit: cover; object-position: top`); the dashboard screenshots have different aspect ratios and crop unevenly. Add a click-to-enlarge lightbox with captions.
  - Replace multi-axis hover tilt with a 2–4 px lift and an arrow nudge on "View repository ↗".
  - Add a one-line "business question answered" per project `[PLACEHOLDER: wording to be supplied for each project]`.
  - Give "View all 9 projects →" the same style as other secondary buttons.

### 2.7 Skills and delivery toolkit (04)
- **Observed:** four large cards (Business Analysis, Process Analysis, Agile/Testing, Technical Tools), each with a blue mono "lifecycle" subtitle and a 3×2 icon-tile grid.
- **Enhance:**
  - The all-caps mono subtitles wrap to two lines; make them a normal-case `--muted` caption.
  - Remove the 3D pop from tiles and use a simple state change.
  - Equalise card heights; the bottom row ends unevenly.
  - Show proficiency only if supplied `[PLACEHOLDER: proficiency levels not provided]`.

### 2.8 Experience (05)
- **Observed:** timeline with coloured dots and a vertical connector, role cards with bullets, a "Key accomplishments & metrics" disclosure and a metrics strip.
- **Enhance:**
  - Draw the vertical connector progressively with scroll.
  - Limit each role to three bullets on the home page; keep the full list on the resume page.
  - Make the disclosure a standard text button with a rotating chevron (it is currently tiny mono blue text).
  - Reuse the Proof section's metric-chip style so the same number always looks the same.

### 2.9 Closing call-to-action
- **Observed:** dark gradient panel with an aurora effect, headline and two buttons.
- **Enhance:** the headline sits in a narrow column and leaves empty space; widen the text block to roughly 60%, reduce the gradient to two stops, and keep the grid-line decoration at low opacity.

### 2.10 Footer
- **Observed:** copyright, timezone, fictional-sample note, underlined link row.
- **Enhance:** add a small sitemap row (Projects, Samples, Services, About, Resume, Contact) and a "last updated" date from the build. Increase link spacing on mobile.

---

## 3. About — `docs/about.html`

- **Page header:** the breadcrumb + H1 + lead pattern works. Shorten the H1 on mobile.
- **"Who I am":**
  - Make the heading serif like other section headings.
  - The large logo tile between the heading and paragraph has no clear purpose; replace it with a portrait `[PLACEHOLDER: photo]` or remove it.
  - "What I do" is a good 2×2 grid; add small icons and the colour coding from 1.1.
- **Right-hand spec card** (decision table with BR-01 to BR-03):
  - Strong concept. Fix the title bar ("spec // requirements-spec.yml (illustrative sample)" wraps to three lines).
  - Reveal rules one by one on scroll and allow click-to-expand for the full rule text.
- **Working principles:** give each card an icon, a one-sentence principle and a link to the sample that proves it, so claims have evidence.

## 4. Services — `docs/services.html`

- **Observed:** five category cards with "Ideal when", "Outcome", a deliverables list (some items linked, some plain) and an "Enquire about this →" button. The 3 + 2 grid leaves an empty cell.
- **Enhance:**
  - Fill the empty cell with a "Not sure what you need?" card, or centre the last two cards.
  - Link all deliverables or style unlinked ones as "no sample yet".
  - The italic text reads "Ideal when: Ideal when …"; remove the duplicate words.
  - Reduce label styles per card (italic + bold + mono tag is too many).
  - On mobile, collapse deliverables to three items with "Show all".
  - Pricing or engagement models are not in the source; do not add figures `[PLACEHOLDER: pricing / engagement model, if desired]`.

## 5. Projects — `docs/projects.html`

- **Observed:** featured PayTrack block with a data-model diagram and three PDF rows; filter chips (All, Analytics, Business intelligence, Data engineering, AI prototype, Writing); nine project cards.
- **Enhance:**
  - Show the data-model diagram larger with a zoom/lightbox; its labels are unreadable at the current size.
  - Filter chips: add counts per filter, animate grid changes with a short fade/FLIP instead of an instant jump, and make the "9 projects" count a live region.
  - Make each whole card a single focusable link target rather than several small links.
  - Add per-project Problem / Approach / Outcome in a drawer or modal `[PLACEHOLDER: content to be supplied per project]`.
  - Keep the filter bar sticky while scrolling the gallery.

## 6. Resume — `docs/resume.html`

- **Header actions:** four buttons. Make Print / Save PDF the only filled button and the others outline or text.
- **KPI cards:** they repeat the home page's Proof cards. Give them a different job or remove them.
- **Experience and filter:**
  - Keep the "Filter bullets by focus" idea; show the active filter as a chip, add "Clear filters", and highlight matching bullets rather than hiding the rest abruptly.
  - Put dates in a left column on desktop at a larger size (they are currently small mono blue text).
- **Skills sidebar:** the sticky sidebar with years per skill is good. Add proficiency bars only if values are supplied `[PLACEHOLDER: proficiency data]`.
- **Print:** an `@media print` block exists; verify that the skills sidebar and all roles appear in the printed/PDF output.
- **Education and certifications:** `[PLACEHOLDER: not reviewed in detail]`.

## 7. Contact — `docs/contact.html`

- **Observed:** the form's vertical spacing is uneven (the gap between the name/email row and "Company" is much larger than between other rows), select labels sit tiny inside tall fields, the copy-message textarea clips its last line ("Best regards"), and "Reach me directly" sits tight under the card.
- **Enhance:**
  - Use CSS grid `gap` on a strict 16 px (field) / 24 px (group) rhythm.
  - Use persistent visible labels above fields; make selects the same height as inputs.
  - Give the fallback textarea an auto height or sensible `min-height`.
  - On desktop, use two columns: a "Reach me directly" panel (email, LinkedIn, timezone, response time) on the left and the form on the right, so the quickest option is above the fold.
  - After "Prepare email draft", show an inline confirmation and reveal the fallback only when needed.
  - Keep the "stores nothing" note next to the button.

## 8. BA Samples — `docs/samples/index.html`

- **Observed (layout bug):** the four-step flow ("01 Discovery & MoM → 02 BRD & FRD Specs → …") and the List/Grid toggle render as unstyled stacked text. The HTML uses `.pt-step` and `.pt-name`, while `style.css` only defines `.pt-phase` and `.pt-num`. Fix this first; it is the most visible polish gap.
- **Enhance:**
  - Style the flow as a horizontal stepper with connectors, an active state, and click-to-filter on the document list.
  - Make the layout toggle a segmented control with icons and `aria-pressed`; remember the choice.
  - Add a legend for status badges (Signed off / Approved / In review).
  - Add file size and page counts per document `[PLACEHOLDER: only the bundle size (246 KB) appears in the source]`.
  - Reduce the hover rotation on the stacked-pages bundle illustration and align its download button vertically.
  - Add a diagram gallery with a lightbox and a link to the `.mmd` sources.
  - Keep "Not Run" in a neutral grey chip, never green.

## 9. 404 — `docs/404.html`

- Add quick links (Home, Projects, BA samples, Contact). One small animated detail at most, such as a broken flow line that reconnects.

---

## 10. Suggested priority order

| # | Change | Pages | Effort |
|---|---|---|---|
| 1 | Fix Samples stepper/toggle class mismatch | samples | S |
| 2 | Mobile hero: lead size, tab overflow, table scroll | home | M |
| 3 | Contact form spacing, labels, two-column layout | contact | M |
| 4 | Limit 3D/hover tilt to hero + featured case study | all | S |
| 5 | Consistent colour semantics and heading style | all | M |
| 6 | Thumbnail framing + lightbox | home, projects | M |
| 7 | Method stepper with drawn connector | home | M |
| 8 | Persist animation pause; one ambient loop per viewport | all | S |
| 9 | Resume layout (dates column, filter chip) | resume | M |
| 10 | Services grid fill + copy clean-up | services | S |

## 11. Not confirmed / needs owner input

- Real-device behaviour (iOS Safari, Android Chrome) `[PLACEHOLDER: not tested]`
- Lighthouse / performance figures `[PLACEHOLDER: not measured]`
- Personal photo, per-project "business question" lines, proficiency levels, pricing `[PLACEHOLDER: owner input needed]`
- Contents of the sample PDF/DOCX files `[PLACEHOLDER: not reviewed]`

---

## 12. Lightswind UI — most suitable components (added)

**Source checked:** https://lightswind.com/components (Lightswind UI), plus the `scroll-timeline` and `count-up` component pages.

### 12.1 What Lightswind is, and the fit problem
- A copy-and-paste **React** component library. The component pages I checked list **TypeScript, Tailwind CSS and Framer Motion**, tested on Next.js 15 / React 19, with imports like `@/components/lightswind/scroll-timeline`.
- Categories listed on the page: 3D Elements (27), Components (50), Background (39), Text (10), Button (12), plus AI Components, Cursors, UI Elements, Form Controls, Layout, Navigation, Utilities and Pro Components (names not listed on the page).
- **Your site is static HTML + CSS + JS** (`docs/`, generated by `build.py`, no framework). Lightswind components cannot be dropped in as they are. Two routes:

| Route | What it means | Recommendation |
|---|---|---|
| **A. Borrow the patterns** | Re-create the chosen effects in your existing `style.css` / `site.js` (CSS + IntersectionObserver; no React). Keeps GitHub Pages, no build step, fast. | **Recommended.** Most picks below are small effects. |
| **B. Adopt the library** | Move the site to React/Next.js + Tailwind + Framer Motion and use components directly. | Only if you already plan to migrate. Larger effort and bundle size. |

- **Install command:** not shown on the pages I could read (a "CLI" tab exists). `[PLACEHOLDER: confirm at lightswind.com/components/installation]`
- **License:** not stated on the component pages; a GitHub repo is linked. `[PLACEHOLDER: confirm the licence before copying code, especially for "Pro Components"]`

### 12.2 Selection rule
Because the brief is *professional, not overly flashy*, I chose components that **explain content** (timeline, counters, reveal, zoom) and excluded ones that are only decoration. Each pick maps to a section in this document.

### 12.3 Recommended components, by section

| Site section (this doc) | Lightswind component | Category | Use it for | Notes / restraint |
|---|---|---|---|---|
| Home › Experience (2.8), Resume (6) | **Scroll Timeline** | Components | Progressive reveal of roles with a drawing progress line. Props include `animationOrder`, `cardAlignment`, `revealAnimation`, `connectorStyle`, `progressIndicator`. | Use `revealAnimation="fade"`, `animationOrder="staggered"`, `progressIndicator` on. Leave `perspective` off. Matches the "draw the connector on scroll" idea in 2.8. |
| Home › Method (2.5) | **Scroll Timeline** (horizontal adaptation) or **Scroll Cards** | Components | Four-phase stepper where each phase lights up on scroll. | Keep four phases; link each to a sample doc. |
| Home › Proof (2.4), Resume KPIs | **Count Up** | Components | Stat counters (`value`, `suffix`, `duration`, `separator`, `triggerOnView`, `easing`). | Use `triggerOnView`, `easing="easeOut"`, `animationStyle="gentle"`, `colorScheme="default"`. Avoid `bounce` / `energetic`. Your `site.js` already has `countUp()`; mainly adopt the `triggerOnView` and easing options. |
| Hero (2.2), page headers | **Dot Grid Background** / **Grid Dot Backgrounds** (or **Beam Grid Background** at very low opacity) | Background | Subtle blueprint-style texture behind the hero. | Your hero already uses a grid; replace extra flow lines with one dot grid. Skip WebGL/shader backgrounds (Aurora Shader, Cosmic Singularity, etc.). |
| Hero keyword (2.2) | **Shiny Text** | Text | One-time light sweep on "testable specs." only. | Single use. Disable under reduced motion. |
| Section intros (all pages) | **Scroll Reveal** | Text | Line-by-line fade of section lead paragraphs. | Short paragraphs only; one reveal per section. |
| Home › Selected work (2.6), Projects (5) | **Lens** | Components | Magnifier on dashboard screenshots so small charts can be read without leaving the page. | Strongest fit for an analyst: it lets viewers inspect dashboards. Pair with the lightbox in 2.6. |
| Project cards (2.6, 5) | **Magic Card** / **Interactive Card** | Components | Soft pointer-following spotlight on cards instead of rotateX/rotateY tilt. | Replaces the multi-axis tilt called out in 1.4. Use a very low-opacity spotlight. |
| Featured case study (2.6, 5) | **3D Perspective Card** | 3D Elements | Gentle tilt on the featured PayTrack mock-up only. | The only 3D element I would keep (see 1.4). Max 2–3 deg. |
| Project images loading | **Skeleton loaders** | UI Elements | Placeholder while screenshots load. | Exact component names `[PLACEHOLDER: category names not listed on the page]`. |
| Primary CTAs, closing CTA (2.9) | **Border Beam** | Button | Thin animated border on the closing CTA panel or the single primary button. | One per page. Skip Confetti, Glitch, Stardust, Holo and Liquid Glass buttons. |
| Contact (7) | **Animated Copy Button** | Components | Email copy action with a clear confirmation state. | Replaces the plain "Copy" text link. |
| Contact (7) | **Form Controls** (accessible inputs, selects) | Form Controls | Consistent field heights, labels and focus states. | `[PLACEHOLDER: specific component names not listed on the page]` |
| Header / navigation (2.1) | **Navigation** (floating navbar) or **Top Sticky Bar** | Navigation / Components | Shrinking sticky header with a blurred background. | Avoid Sparkle Navbar and Morphing Navigation. |
| Theme toggle (1.1) | **Utilities › theme toggle** | Utilities | Auto / light / dark control. | `[PLACEHOLDER: component name not listed]` |
| Home › Hero artifact tab "SQL logic" (2.2), Samples (8) | **Terminal Card** / **Code Hover Cards** | Components | Present SQL or API snippets (e.g. the reconciliation query) with a readable code frame. | Use real content from `sample_reconciliation_queries.sql`; do not invent queries. |
| Home › Skills (2.7) | **Sliding Logo Marquee** | Components | Tool logos strip (Jira, Confluence, Postman, Power BI, etc.) in place of text pills. | `[PLACEHOLDER: logo files not provided; check each vendor's brand-usage rules]` |
| Services (4), Samples (8) | **Stack List** / **Scroll List** | Components | Document lists that reveal and stack on scroll. | Keep for the samples document list only if the stepper fix (8) is done first. |
| Cursor (optional) | — | Cursors | Not recommended. | Custom particle cursors compete with content. |

### 12.4 Components to avoid for this portfolio
- 3D carousels and sliders, 3D Model Viewer, Plasma Globe, Hanging Id Card, Ascii Wave, Sparkle Navbar.
- Shader/WebGL backgrounds (Aurora Shader, Quantum Field, Cosmic Singularity, Cyber Hive, etc.) and Text Particle Animation.
- Confetti, Glitch and Stardust buttons.
- Reason: they add motion and weight but no information, and they work against the "calm, evidence-led" positioning.

### 12.5 Implementation notes (Route A, static site)
- Scroll Timeline / Scroll Reveal / Count Up → `IntersectionObserver` + CSS `transition`/`@keyframes` + one scroll-progress variable (`--p`) driving a `stroke-dashoffset` or `scaleY` line.
- Lens → small `pointermove` handler that positions a circular `clip-path` over a 2× scaled copy of the image; disable on touch.
- Magic Card spotlight → `background: radial-gradient(circle at var(--mx) var(--my), rgba(37,99,235,.10), transparent 40%)`, updating `--mx/--my` from `pointermove`.
- Shiny Text → CSS `background-clip:text` sweep, run once, wrapped in `@media (prefers-reduced-motion: no-preference)`.
- Keep every effect behind the existing animation toggle and `prefers-reduced-motion`.
- If you choose Route B, keep the same restraint: use `triggerOnView`, avoid the bouncy `animationStyle` presets, and test bundle size.

### 12.6 Suggested rollout (adds to section 10)
| # | Change | Pages | Effort |
|---|---|---|---|
| L1 | Scroll Timeline pattern for Experience | home, resume | M |
| L2 | Lens on project screenshots | home, projects | M |
| L3 | Magic Card spotlight replacing tilt | home, projects | S |
| L4 | Count Up `triggerOnView` + easing | home, resume | S |
| L5 | Animated Copy Button + form controls | contact | S |
| L6 | Border Beam on closing CTA only | home | S |
| L7 | Terminal Card for SQL/API snippets | home, samples | M |
