# Gautam Reddy Portfolio (v24)

Static site. No frameworks, no build step needed to deploy.

- Pages: index, about, services, projects, resume (with Print / Save ATS PDF), contact, samples/index
- assets/style.css, assets/site.js, assets/vendor/lenis.min.js (smooth scroll, MIT, bundled so there is no CDN dependency)
- OpenGraph & Twitter preview card (`assets/og-card.png`) & Apple Touch Icon (`assets/apple-touch-icon.png`)
- Light and dark theme (follows the system setting, remembers the choice via SVG toggle)
- Deploy: upload the contents of this folder to GitHub Pages (keep the folder structure)
- Run locally: `python -m http.server 8000`

## What v24 adds
- Senior UI/UX audit polish & WCAG AA contrast compliance (>4.5:1 text contrast).
- De-noised animation budget: steady resting state with responsive 3D micro-interactions on hover.
- Background BPMN animated flow on hero, static on inner sections with off-screen pause via IntersectionObserver.
- Single-row keyword marquee with pause/play toggle button and WCAG 2.2.2 compliance.
- ATS-friendly Print / Save as PDF button on Resume page with print stylesheet avoiding timeline page breaks.
- Full Open Graph, Twitter Summary Large Image, Canonical, and Theme Color meta tags.
- Streamlined 4-phase delivery stepper replacing traffic-light widgets.
- Clean card elevations without sibling blur or click-to-focus traps.

## Editing
`python build.py` regenerates all 7 HTML pages from `build.py` (copy, links, keywords) and `flows.py` (diagrams).
The recruiter keyword lists are `MARQ_ITEMS`, `META_KW` and `ROLES_ROT` at the top of `build.py`.
