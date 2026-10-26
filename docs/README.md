# Gautam Reddy Portfolio (v32)

Static site. No external runtime frameworks, no build step needed to deploy.

- Pages: index, about, services, projects, resume (print-friendly with Print / Save PDF), contact, samples/index, 404
- assets/style.css, assets/site.js, assets/vendor/lenis.min.js (Lenis smooth scroll v1.1.18, MIT License, bundled for offline speed without CDN dependencies)
- OpenGraph & Twitter preview card (`assets/og-card.png`) & Apple Touch Icon (`assets/apple-touch-icon.png`)
- Light and dark theme (follows OS preferences, persists user choice via localStorage, updates meta theme-color)
- Deploy: upload the contents of this folder to GitHub Pages (keep the folder structure)
- Run locally: `python -m http.server 8000`

## UI/UX & Code Quality Polish
- **WCAG AA Compliance**: All text contrast exceeds 4.5:1 (including card links and footer meta) and UI components exceed 3:1 (form borders, chips, focus rings).
- **Accessible Navigation & Drawer**: Focus traps for mobile menu, image lightbox, and preview drawer; WAI-ARIA tablist accessibility with roving tabindex.
- **Reduced Motion & Fail-Safe Reveals**: Immediate visibility fallback via noscript; all animations paused under `prefers-reduced-motion: reduce` and synchronized with site animation toggles.
- **Responsive Layouts**: Controlled subtle 3D card tilt, adaptive grid heights preventing text clipping across all mobile viewports, resilient sliding filter pills on project gallery.
- **Deep-linking & Hash Anchors**: Direct URL hash navigation to project filter chips (`#bi`, `#analytics`) scrolls smoothly and sets active state.
- **Form UX**: Clean client-side validation, accessible live error summary with direct field references, truthful draft preparation and clipboard copy fallback.
- **Performance & Asset Footprint**: SVG SMIL animations paused offscreen; SMIL dots eliminated from project mini thumbnails; isolated drawer markup.

## Editing
`python build.py` regenerates all 7 HTML pages from `build.py` (copy, links, keywords) and `flows.py` (diagrams).
The keyword lists are `MARQ_ITEMS` and `ROLES_ROT` at the top of `build.py`. `build.py` also writes `sitemap.xml`, `robots.txt` and `404.html`; page titles, descriptions and JSON-LD are set at the bottom of the file.
