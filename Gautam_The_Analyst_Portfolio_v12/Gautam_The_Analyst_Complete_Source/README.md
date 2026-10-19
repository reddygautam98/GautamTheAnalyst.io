# Gautam The Analyst — Complete Website Source

A standalone, responsive Business Analyst portfolio website for **Gautam Reddy**. This package contains the HTML pages, shared CSS and JavaScript, custom analytics logo, project preview artwork, and the full BA sample-artifact collection.

## Main pages

- `index.html` — homepage, services overview, selected projects, BA sample links, recruiter path and client enquiry CTA.
- `about.html` — professional story and working principles.
- `services.html` — services, deliverables and engagement options.
- `projects.html` — nine project examples linked to their repositories; illustrative previews are labelled.
- `resume.html` — experience, Google XYZ-style measurable bullets, skills, education and certifications. Employer date ranges and a resume-download button are omitted.
- `contact.html` — direct contact options and project enquiry form.
- `samples/index.html` — BRD/FRD, user-story, RTM/UAT, workshop, diagram, CSV and wireframe showcase with matching light/dark theme control.

## Shared code and assets

- `styles.css` — responsive layout, page components, light/dark palette, accessible focus states and theme-specific surfaces.
- `assets/js/site.js` — mobile navigation, project filters, contact form validation/email-draft preparation, year update and persistent theme toggle.
- `assets/gautam-analyst-mark.svg` — custom orange analytics logo used on the main pages and BA Samples gallery.
- `assets/project-previews/` — clearly labelled illustrative project visuals.
- `samples/docs/` — fictional PayTrack example documents in PDF and editable Word formats, plus the combined BA documentation bundle.
- `samples/diagrams/` — process, architecture, ERD and API sequence diagrams in SVG/PNG/Mermaid formats.
- `samples/specs/` — CSV samples for requirements traceability, test cases and user stories.

## Run locally

Open `index.html` directly, or run a small local web server from this directory:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000/`.

## Deploy to GitHub Pages

Upload the **contents of this directory** to the publishing folder selected in GitHub Pages. If Pages is configured for `/docs`, copy the contents into `/docs`; if configured for repository root, upload the contents at the root. Preserve all relative paths, particularly `assets/` and `samples/`.

## Contact form

The website is static. The form validates visitor input and creates an email draft addressed to `reddygautam98@gmail.com`. It does not store visitor details or auto-send an email; the visitor must review and send the draft.

## Sample-work integrity

PayTrack is a fictional portfolio case study. Names, values, targets and scenarios are illustrative. Test cases have not been executed and are marked Not Run. Do not represent these sample artifacts as actual client deliverables or production evidence.

## Project links

- Website: https://reddygautam98.github.io/GautamTheAnalyst.io/
- Repository: https://github.com/reddygautam98/GautamTheAnalyst.io
- LinkedIn: https://www.linkedin.com/in/gautam-reddy-analyst
- GitHub profile: https://github.com/reddygautam98


## Futuristic redesign (v2)

- **Design system** (`styles.css`): dark-first "Neo-Terminal Aurora" theme with a matching light theme; glass surfaces, animated gradient borders (`@property`), cursor spotlights, aurora + node-network background, fluid type (Space Grotesk / Inter / JetBrains Mono).
- **Motion**: scroll reveals, count-up metrics, typed role line, hero 3D tilt, tech ticker, cross-document page transitions (`@view-transition`). All disabled under `prefers-reduced-motion`.
- **New sections**: delivery lifecycle explorer with a live traceability demo (home), operating principles + toolkit ticker (about), quick-nav + toolkit ticker (services), project search + live count (projects), timeline + tool chips + quick-nav (resume), enquiry-draft terminal + copy buttons (contact).
- **Command palette**: `Ctrl/⌘ + K` or `/` on any page.
- **Fixes**: the light/dark toggle had two competing click handlers that cancelled each other; now a single handler, dark by default, choice persisted. Broken remote preview images degrade to a placeholder.
- `samples/index.html` now shares the same design system (`samples/gallery.css`).

## 3D & background layer (v3)

- `assets/js/fx3d.js` (no libraries): 3D wireframe globe on the home hero and a different rotating solid (torus, lattice, icosahedron) on each sub-page hero; they react to the pointer and scroll.
- Cards: perspective tilt, holographic glare, HUD corner brackets, depth-popped icons/titles/thumbnails, outlined service numerals.
- Background: depth starfield with parallax and shooting stars, floating glass orbs and CSS 3D cubes, perspective grid floor under every hero, scroll-driven hue shift.
- Home: new "Toolkit in orbit" draggable 3D ring (arrow keys also rotate it).
- Tilt only runs on hover-capable pointers; everything respects `prefers-reduced-motion`; canvases pause off-screen and in hidden tabs.

## 2026 portfolio patterns (v4)

- `assets/js/portfolio.js`: kinetic word-by-word headlines, magnetic primary buttons, scroll-spy section dots (home), scroll-linked giant marquee, process line that fills as you scroll, sticky case-study depth effect, projects grid/list toggle.
- Home: proof bento (resume figures), sticky stacked case studies (4 featured projects, all link to their repositories), scroll-told process.
- About: "At a glance" bento. Services: bento-rhythm service cards. Resume: sticky snapshot beside the timeline. Footer: giant wordmark on every page.
