GAUTAM THE ANALYST — WEBSITE SOURCE
===================================

CANONICAL PUBLISHED SOURCE
The live GitHub Pages site is published from the `docs/` folder on the `main` branch. All runnable website HTML, shared CSS/JavaScript, project previews, sample-artifact gallery, diagrams and CSV resources are kept together there. Root-level duplicate HTML/CSS/JavaScript and the original HTML5 UP/Massively template dependencies have been removed to avoid competing copies of the site.

PUBLISHED PAGES
- `docs/index.html` — client-focused home page with services, selected work, BA Samples and engagement process.
- `docs/about.html` — professional profile and working principles.
- `docs/services.html` — service scopes and deliverables.
- `docs/projects.html` — nine project examples with accurately labelled screenshots/illustrations.
- `docs/resume.html` — professional experience, skills, education and certifications; no resume-download button or employer-duration ranges.
- `docs/contact.html` — direct contact details and project enquiry form.
- `docs/samples/index.html` — BA sample artifacts gallery.
- `docs/assets/css/portfolio.css` — responsive visual system, light/dark theme and restrained diagram backgrounds.
- `docs/assets/js/portfolio.js` — persisted theme, mobile navigation, project filters, service preselection and mailto enquiry draft behavior.

ROOT-LEVEL IMAGE FILES
The root `assets/*.jpg` files are retained as stable public image sources for project screenshots; they are not old website code. The deployed site has the assets it needs under `docs/assets/`.

BA SAMPLE ARTIFACTS
The `docs/samples/` folder contains fictional PayTrack BRD/FRD, user stories, RTM/test/UAT plan, workshop MoM/RAID, SVG diagrams, Mermaid source files, and CSV templates. PayTrack is illustrative. Sample names/values are fictional and test cases are marked Not Run.

CONTACT FORM
The static enquiry form prepares an email addressed to `reddygautam98@gmail.com`. It does not store enquiries or auto-send; the visitor must review and send the email draft.

DEPLOYMENT
GitHub Pages source is `main /docs`. The `.nojekyll` marker is included to publish this static HTML/CSS/JavaScript site without relying on legacy template conversion. After publishing, test the live URL, light/dark toggle, mobile navigation, project filters and enquiry flow in a real browser.
