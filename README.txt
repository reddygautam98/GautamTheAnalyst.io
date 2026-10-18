# Gautam The Analyst Portfolio — Client Enquiry Edition

Client-focused portfolio with service descriptions, project links, a clear working process and structured project inquiry form.

## Client conversion features
- Service cards list practical deliverables for Business Analysis, Data & BI, SQL/Data Quality, Data Engineering, AI/RAG prototypes, and UAT/Delivery support.
- Service CTAs jump to the project inquiry and preselect a relevant service.
- A four-step engagement process describes discovery, scope, checkpoints and handover.
- Direct email, LinkedIn and GitHub options.
- Project inquiry fields cover contact name, work email, company, service, engagement preference, timeline, summary and optional reference URL.
- Metrics shown on the site are from the supplied resume: 4+ years of business analysis experience, 100K+ transaction records analyzed, 350+ test cases supported, and 2 payment gateway integrations.
- Nine projects link to the provided repositories.

## Contact form behavior
GitHub Pages is static. The form validates required fields then opens the visitor's default email application with a pre-filled message to reddygautam98@gmail.com. It does not store or automatically submit form data. A server-side form requires an approved form provider and an updated privacy notice.

## Files
- index.html — homepage with client-benefit section, project previews and BA Samples showcase.
- about.html — professional story and working principles.
- services.html — scoped services, deliverables and engagement process.
- projects.html — nine project cards with consistent screenshot/illustration labels and category filters.
- resume.html — skills, achievements, experience, education and certifications (no resume download button; employer durations omitted).
- contact.html — direct links and project enquiry form.
- samples/index.html — BA document/diagram gallery.
- assets/css/portfolio.css — shared responsive styling, light/dark themes, and restrained diagram backgrounds.
- assets/js/portfolio.js — theme persistence, mobile navigation, accessible project filters, query-based service preselection and mailto enquiry builder.

## Before publishing
Confirm reddygautam98@gmail.com and the LinkedIn URL are your preferred public contact routes. Keep project claims aligned with your repositories and resume. Do not add invented testimonials, prices or client outcomes.

## Project snapshots and preview labels
- Repository screenshots are shown for Sales Data Analysis, HR Data Analysis, Business Insights Report, Sales Forecasting Report, Loan Data Analytics, and ClinChat-style RAG App.
- The Business Insights Report and ClinChat screenshots are embedded in their project READMEs and loaded from GitHub's user-attachment image URLs.
- GameZone Business Intelligence, Excel Dashboard Analysis, and MetaLayer do not currently expose matching screenshots of the running project in their tracked files. Their visual cards use custom SVG diagrams stored in `assets/project-previews/`, clearly labelled as illustrative previews.
- All nine project cards have visual previews, descriptive alt text, lazy loading, and links to open the full-size image or diagram.


## Business Analyst sample artifacts
The live portfolio includes a "BA Samples" navigation link and a sample-artifacts section. The `samples/` folder includes a fictional PayTrack case study with BRD, FRD, user stories, RTM/test/UAT plan, workshop MoM/RAID, CSV templates, SVG diagrams and Mermaid source. An editable Figma design contains reconciliation overview and exception case-detail wireframes.


## Homepage positioning update
The homepage hero now leads with the client problem-to-delivery journey and features direct calls to discuss a project or explore the BA sample artifacts. The BA sample showcase covers BRD/FRD, user stories, RTM/testing/UAT, workshop MoM/RAID, diagrams, and editable Figma wireframes.


## Theme switch
- A light/dark theme control is available in the main navigation and BA Samples gallery.
- Theme choice is persisted in localStorage and shared across pages; when no choice is saved, the browser's color-scheme preference is used.
- The control has keyboard focus styling and aria-pressed state.


## Work-sample diagram backgrounds
- The homepage hero and selected content sections use low-opacity background artwork composed from the real project-preview diagrams and the BA sample diagrams.
- The BA Samples gallery also has a subtle diagram background and now displays an API sequence SVG alongside its Mermaid source.
- Diagram artwork sits behind the content, is reduced on small screens, and uses a dark-theme-adjusted treatment so text remains readable.
- The original SVG/PNG/Mermaid files remain separate and can still be opened or downloaded as sample artifacts.


## Dedicated multi-page site
The homepage navigation links to Home, Services, Projects, BA Samples, About, Resume and Contact. Dedicated pages share the same responsive header, theme toggle, footer and stylesheet. The project page uses one preview per card; screenshots and illustrative visuals are labelled according to their source. Diagram artwork is limited to the hero and BA Samples sections to avoid reducing readability.

## QA notes
- Service links pass a `service` query parameter to contact.html, where the selected service is prefilled.
- Project filters also update `aria-pressed` so their selected state is available to assistive technology.
- The inquiry form opens a prepared email draft; it does not store or auto-send visitor data.
- Test themes, mobile navigation, filters, form validation and email-draft behavior in a browser after publishing.
