# Gautam Reddy Portfolio (v32)

Static site. No external runtime frameworks, no build step needed to deploy.

- Pages: index, about, services, projects, resume (with Print / Save ATS PDF), contact, samples/index, 404
- assets/style.css, assets/site.js, assets/vendor/lenis.min.js (smooth scroll, MIT, bundled so there is no CDN dependency)
- OpenGraph & Twitter preview card (`assets/og-card.png`) & Apple Touch Icon (`assets/apple-touch-icon.png`)
- Light and dark theme (follows OS preferences, persists user choice via localStorage, updates meta theme-color)
- Deploy: upload the contents of this folder to GitHub Pages (keep the folder structure)
- Run locally: `python -m http.server 8000`

## UI/UX & Code Quality Polish (v32)
- **WCAG AA Compliance**: All text contrast exceeds 4.5:1 (including card links and footer meta) and UI components exceed 3:1 (form borders, chips, focus rings).
- **Accessible Navigation & Drawer**: Lenis scroll lock on preview drawer open, focus traps for mobile menu and preview drawer, unique ARIA tabs (`role="tab"`, `role="tabpanel"`).
- **Reduced Motion & Fail-Safe Reveals**: Content renders cleanly without stuck opacity if IntersectionObserver is unsupported or delayed; animated elements honor `prefers-reduced-motion: reduce`.
- **Responsive Layouts**: Flexible 3D card tilt, 2-column flip cards with grid heights that prevent text clipping on smaller viewports, resilient filter pills on project gallery.
- **Deep-linking & Hash Anchors**: Direct URL hash navigation to project filter chips (`#bi`, `#analytics`) scrolls smoothly and sets active state.
- **Form UX**: Clean client-side validation without premature red borders, single polite live region, clipboard copy fallback.
- **Performance & Asset Footprint**: Heavy drawer markup isolated to samples page, eliminating 5KB overhead on standard pages; removed dead 3D scene code.

## Editing
`python build.py` regenerates all 7 HTML pages from `build.py` (copy, links, keywords) and `flows.py` (diagrams).
The keyword lists are `MARQ_ITEMS` and `ROLES_ROT` at the top of `build.py`. `build.py` also writes `sitemap.xml`, `robots.txt` and `404.html`; page titles, descriptions and JSON-LD are set at the bottom of the file.
