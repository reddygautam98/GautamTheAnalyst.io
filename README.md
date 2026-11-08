# GautamTheAnalyst.io — Executive Business Analyst Portfolio

[![CI & Accessibility Verification](https://github.com/reddygautam98/GautamTheAnalyst.io/actions/workflows/ci.yml/badge.svg)](https://github.com/reddygautam98/GautamTheAnalyst.io/actions/workflows/ci.yml)
[![WCAG 2.2 AA](https://img.shields.io/badge/accessibility-WCAG%202.2%20AA-059669.svg)](https://www.w3.org/WAI/WCAG22/quickref/)
[![Zero Runtime Dependencies](https://img.shields.io/badge/runtime-zero%20dependencies-3b82f6.svg)](https://developer.mozilla.org/en-US/docs/Web)
[![Python 3.10+](https://img.shields.io/badge/build-Python%203.10+-3776ab.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-amber.svg)](LICENSE)

> **Live Deployment**: [https://reddygautam98.github.io/GautamTheAnalyst.io/](https://reddygautam98.github.io/GautamTheAnalyst.io/)  
> **Executive Portfolio**: Professional Business Analyst portfolio demonstrating end-to-end delivery across requirements elicitation, UML 2.5 architecture, BPMN process workflows, SQL reconciliation, and enterprise traceability.

---

## 1. Architectural Philosophy & Technology Stack

The portfolio is engineered with the **Architectural Executive Precision** philosophy:

- **Pure Vanilla Web Architecture**: Engineered entirely in standard HTML5, modern CSS3 (Custom Properties, `@supports`, CSS Grid, Flexbox, 3D Transforms), and vanilla ES2022 JavaScript. Zero heavy runtime client-side frameworks (no React, Vue, Angular, or bundler overhead).
- **Deterministic Static Site Generation**: Built using Python 3 standard library scripts (`docs/build.py`, `docs/flows.py`). Generates 100% deterministic, idempotent static HTML with SHA-256 asset cache-busting fingerprints.
- **Accessibility & Contrast First (WCAG 2.2 AA)**: Strict contrast compliance across both light and dark themes (4.5:1 for body copy, 3:1 for graphical UI elements and form boundaries). Fully keyboard-navigable with visible focus rings and accessible ARIA attributes.
- **Resilient Motion & Life-Cycle Management**: Interactive canvas elements (`bg-anim.js`, `ascii-wave.js`, `globe.js`, `grid-trail.js`) and 3D card tilts (`card-fx.js`) dynamically respect `prefers-reduced-motion: reduce`, the global `#animToggle` switch, and document visibility changes (`requestAnimationFrame` lifecycle cancellation).
- **Deployment via GitHub Pages**: Published directly from the repository's `/docs` directory with `.nojekyll` bypass, ensuring fast CDN delivery with zero server configuration.

---

## 2. Directory & File Organization

The codebase is structured to separate source compilation, public web delivery, sample artifacts, testing automation, and CI/CD pipelines:

```text
GautamTheAnalyst.io/
├── .github/
│   └── workflows/
│       └── ci.yml                  # GitHub Actions workflow (Build, axe-core a11y, Lighthouse)
├── .editorconfig                   # Cross-editor style consistency (indentation, line endings)
├── .gitattributes                  # Git line-ending normalization (LF) and binary tracking
├── .gitignore                      # Git exclusion rules (cache, venv, logs, OS artifacts)
├── .lighthouserc.json              # Lighthouse CI audit assertions & performance budgets
├── pyproject.toml                  # PEP 621 Python project metadata & pytest configuration
├── requirements.txt                # Automated testing dependencies (playwright, pytest, axe-core)
├── serve.py                        # Zero-dependency local development HTTP server
├── README.md                       # Comprehensive repository documentation & architectural guide
├── README.txt                      # Canonical text reference (packaging metadata fallback)
├── BUG_FIX_REPORT.md               # Complete audit report for historical bugs (BUG-01 to BUG-34)
├── IMPLEMENTATION_REPORT.md        # Technical implementation & UML sequence diagram report
│
├── docs/                           # Canonical GitHub Pages web root
│   ├── .nojekyll                   # Bypasses Jekyll processing for pure static publishing
│   ├── index.html                  # Homepage: Hero showcase, Selected Work, BA Deliverables, Process
│   ├── about.html                  # Professional background, BA operating principles & stakeholders
│   ├── services.html               # Service offerings, deliverable kits & scoping HUD calculator
│   ├── projects.html               # 9 enterprise projects, interactive filter tabs & case studies
│   ├── resume.html                 # Complete chronological career history, skills & print layout
│   ├── contact.html                # Enquiry form, scoping calculator & interactive 3D globe
│   ├── 404.html                    # Custom 404 error page with dynamic ASCII wave canvas
│   ├── robots.txt                  # Search engine crawl directives & sitemap location
│   ├── sitemap.xml                 # Deterministic XML sitemap for SEO discovery
│   ├── build.py                    # Core static generator for HTML pages & cache-busting hashes
│   ├── flows.py                    # SVG generator for UML 2.5 sequence diagrams & BPMN flows
│   ├── README.md                   # Documentation for the docs/ web distribution folder
│   │
│   ├── assets/                     # Shared client-side stylesheets, scripts & static media
│   │   ├── style.css               # Unified responsive design system, theme tokens & 3D styling
│   │   ├── site.js                 # Theme toggling, mobile menu, Lenis smooth scroll & UI state
│   │   ├── card-fx.js              # 3D perspective tilt & specular lighting for interactive cards
│   │   ├── bg-anim.js              # Ambient background canvas particle field animation
│   │   ├── ascii-wave.js           # Interactive ASCII wave canvas effect on 404 error page
│   │   ├── globe.js                # Interactive 3D WebGL/Canvas globe on contact page
│   │   ├── cobe.js                 # Lightweight canvas globe library
│   │   ├── grid-trail.js           # Interactive cursor grid-trail canvas effect on about page
│   │   ├── mark.svg                # Brand monogram & SVG favicon
│   │   ├── og-card.png             # OpenGraph & Twitter social preview banner
│   │   ├── apple-touch-icon.png    # iOS home screen web clip icon
│   │   ├── vendor/
│   │   │   └── lenis.min.js        # Bundled Lenis smooth scroll library (offline, zero-CDN)
│   │   └── projects/               # Enterprise project preview screenshots & architectural diagrams
│   │
│   └── samples/                    # PayTrack Business Analysis Sample Deliverable Pack
│       ├── index.html              # Interactive sample artifact gallery & 4-phase timeline
│       ├── README.md               # Documentation & scenario guide for PayTrack case study
│       ├── docs/                   # Formal BA deliverables (PDF & editable DOCX templates)
│       │   ├── 01_BRD_PayTrack_Sample.pdf
│       │   ├── 02_FRD_PayTrack_Sample.pdf
│       │   ├── 03_User_Stories_Acceptance_Criteria_Sample.pdf
│       │   ├── 04_RTM_Test_Cases_UAT_Plan_Sample.pdf
│       │   ├── 05_Discovery_Workshop_MoM_Decision_Log_Sample.pdf
│       │   ├── BA_Document_Pack_Payment_Reconciliation.pdf
│       │   └── PayTrack_Sample_BA_Documentation_Bundle.pdf
│       ├── diagrams/               # Architecture, BPMN & UML sequence diagrams (SVG, PNG, MMD)
│       │   ├── Payment_API_Sequence.mmd / .svg
│       │   ├── Payment_Conceptual_Architecture.svg / .png
│       │   ├── Payment_Data_Model_ERD.mmd / .svg / .png
│       │   └── Payment_Reconciliation_Process.mmd / .svg / .png
│       └── specs/                  # Structured requirement & data artifacts
│           ├── requirements_traceability.csv
│           ├── sample_test_cases.csv
│           ├── sample_user_stories.csv
│           └── sample_reconciliation_queries.sql
│
└── tests/                          # Automated Quality Assurance & Testing Suite
    ├── __init__.py                 # Python package marker
    └── test_a11y_responsive.py     # 144-point responsive viewport & accessibility test suite
```

---

## 3. Local Development & Workflow

### Prerequisites
- **Python 3.10+** (standard library only; no pip dependencies required for building or running).

### Rebuilding Static Pages
Whenever modifying `docs/build.py`, `docs/flows.py`, or any asset in `docs/assets/`, regenerate all 8 HTML pages:

```bash
# On Windows / macOS / Linux:
python docs/build.py
# Or:
python3 docs/build.py
```

*The generator validates asset existence, calculates SHA-256 query strings, compiles technical SVG sequence diagrams, and produces deterministic HTML outputs.*

### Running the Local Development Server
Start the bundled lightweight development server:

```bash
python serve.py
```
Open **`http://127.0.0.1:8000/`** in your browser. The server serves directly from `docs/` with CORS and cache-invalidation headers enabled.

---

## 4. Quality Assurance & Automated Testing

### Test Suite Execution
The test suite in `tests/test_a11y_responsive.py` executes 5 comprehensive test suites with **144 responsive viewport verification checks**:

```bash
# Standard library unittest execution:
python tests/test_a11y_responsive.py

# Or via pytest (with test dependencies installed):
pytest tests/test_a11y_responsive.py -v
```

### Verified Target Viewports Matrix
Tests validate complete layout integrity, non-zero geometry, and absence of horizontal overflow across all 9 standard industry viewports:

| Viewport Name | Dimensions (CSS px) | Target Device Category | Verification Status |
| :--- | :--- | :--- | :--- |
| **Mobile Small** | 320 × 568 | iPhone SE (1st gen) / Compact Mobile | Verified (0 horizontal overflow) |
| **Mobile Standard** | 375 × 667 | iPhone 8 / SE (2nd/3rd gen) | Verified |
| **Mobile Modern** | 390 × 844 | iPhone 12/13/14/15/16 Pro | Verified |
| **Mobile Large** | 430 × 932 | iPhone 14/15/16 Pro Max | Verified |
| **Tablet Portrait** | 768 × 1024 | iPad Mini / Portrait Tablets | Verified |
| **Tablet Landscape** | 1024 × 768 | iPad Pro / Small Laptops | Verified |
| **Desktop HD** | 1280 × 800 | MacBook Air / Standard Laptops | Verified |
| **Desktop Full HD** | 1440 × 900 | Standard Desktop Monitors | Verified |
| **Desktop Large** | 1920 × 1080 | Full HD External Displays | Verified |

---

## 5. Continuous Integration (CI/CD)

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push and pull request to `main`:
1. **Static Build Verification**: Compiles all HTML files via `python docs/build.py` and verifies zero uncommitted diffs (`git diff --exit-code docs/`).
2. **Automated Testing**: Launches the development server and runs Playwright and axe-core accessibility checks.
3. **Lighthouse CI**: Audits performance, accessibility, best practices, and SEO against strict budgets.

---

## 6. Business Analyst Deliverables & Transparency

All portfolio deliverables are accompanied by authentic, downloadable artifacts:
- **Requirements**: Functional (FRD), Non-Functional (NFR), Business (BRD) specifications.
- **Modeling**: BPMN 2.0 Business Processes, UML 2.5 Sequence Diagrams, Logical Data Models (ERD).
- **Execution**: User Stories with Given/When/Then Acceptance Criteria, Definition of Ready (DoR) / Done (DoD).
- **Verification**: Requirements Traceability Matrix (RTM), SQL reconciliation queries, and UAT test plans.

---

## 7. License

This project is licensed under the MIT License — see the repository files for details.

