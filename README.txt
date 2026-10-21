GAUTAM THE ANALYST — WEBSITE SOURCE
===================================

CANONICAL PUBLISHED SOURCE
The live GitHub Pages site is published from the `docs/` folder on the `main` branch. All runnable website HTML, shared CSS/JavaScript, project previews, sample-artifact gallery, diagrams, and CSV resources are kept together there.

PUBLISHED PAGES & ASSETS
- `docs/index.html` — client-focused home page with services, selected work, BA Samples, and engagement process.
- `docs/about.html` — professional profile and working principles.
- `docs/services.html` — service scopes and deliverables.
- `docs/projects.html` — nine project examples with project screenshots and repository links.
- `docs/resume.html` — professional experience, skills, education, and certifications.
- `docs/contact.html` — direct contact details and project enquiry form.
- `docs/samples/index.html` — BA sample artifacts gallery (PayTrack case study, documents, diagrams, CSV specs).
- `docs/assets/style.css` — responsive visual system, light/dark themes, and diagram styling.
- `docs/assets/site.js` — persisted theme, mobile navigation, project filters, smooth scroll, and form handler.
- `docs/assets/vendor/lenis.min.js` — bundled smooth-scrolling library.

BA SAMPLE ARTIFACTS
The `docs/samples/` folder contains fictional PayTrack BRD/FRD, user stories, RTM/test/UAT plan, workshop MoM/RAID, SVG/PNG diagrams, Mermaid source files, and CSV templates. PayTrack is illustrative. Sample names/values are fictional and test cases are marked Not Run.

CONTACT FORM
The static enquiry form prepares an email draft addressed to `gautamreddy098@gmail.com`. It does not store enquiries or auto-send; the visitor reviews and sends the draft via their email client.

BUILDING & LOCAL DEVELOPMENT
- Rebuild all pages: from `docs/`, run `python build.py`
- Local preview: run `npx live-server docs` or `python -m http.server 8080 --directory docs`

DEPLOYMENT
GitHub Pages source is configured to publish from `main /docs`. The `docs/.nojekyll` marker is included to ensure static publishing directly without Jekyll conversion.
