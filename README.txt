GAUTAM THE ANALYST — WEBSITE SOURCE
===================================

This repository contains the current custom multi-page portfolio. Legacy HTML5 UP / Massively template files and dependencies have been removed.

MAIN PAGES
- index.html: client-focused home page, services teaser, selected projects, BA Samples and engagement process.
- about.html: professional profile and working principles.
- services.html: client services, deliverables and engagement process.
- projects.html: nine project cards with consistent screenshots/illustrative labels.
- resume.html: professional experience, responsibilities, skills, education and certifications. Resume download and employer-duration ranges are omitted.
- contact.html: direct contact methods and project inquiry form.
- samples/index.html: BA sample artifacts gallery.

SHARED SOURCE
- assets/css/portfolio.css: responsive site styling, light/dark theme styles, project visuals and restrained diagram backgrounds.
- assets/js/portfolio.js: theme persistence, mobile navigation, project filters, service preselection and email draft generation.
- assets/project-previews/: clearly labelled illustrative SVG visuals.
- assets/*.jpg: dashboard images used by project cards.
- samples/docs/: Markdown document sources for the fictional PayTrack BRD, FRD, user stories, RTM/UAT plan and discovery workshop log.
- samples/diagrams/: SVG diagram previews and editable Mermaid source.
- samples/specs/: CSV examples for traceability, test cases and user stories.

THEME
The light/dark toggle is shared across the pages and saves the user's selection in browser localStorage. If no choice has been saved, the initial theme follows the device preference where supported.

CONTACT FORM
The static form validates required fields and prepares a mailto draft addressed to reddygautam98@gmail.com. It does not store or auto-send visitor data; the visitor must review and send the email.

SAMPLE CONTENT
PayTrack is a fictional portfolio case study. Names, references, amounts and scenarios are illustrative. Test cases are marked Not Run. Do not present the artifacts as actual client work, production behavior or executed test evidence.

PUBLISHING
GitHub Pages should publish from the main branch and repository root. Keep relative paths intact. After the commit, allow Pages to rebuild and check the live URL, then test light/dark themes, mobile navigation, project filters and the enquiry form in a real browser.
