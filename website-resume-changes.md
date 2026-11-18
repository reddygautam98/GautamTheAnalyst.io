# Website Resume Content Changes Log (`website-resume-changes.md`)

**Repository:** `GautamTheAnalyst.io/`  
**Source Resume:** `Gautam_Reddy_Technical_BA_Resume.tex`  
**Contact Policy Applied:** Previous website email (`gautamreddy098@gmail.com`) and contact setup (no phone number displayed) strictly preserved across all 8 HTML pages, `docs/build.py`, `docs/flows.py`, and `docs/assets/site.js`.

## 1. Summary of Changes Applied

| Category | Previous Website Content | Updated Website Content (from `Gautam_Reddy_Technical_BA_Resume.tex`) | Affected Files / Pages |
| :--- | :--- | :--- | :--- |
| **Email & Contact Number** | `gautamreddy098@gmail.com` (no phone number) | **Unchanged (`gautamreddy098@gmail.com`, no phone number)** — skipped resume email/phone update per instruction | All 8 pages, `docs/build.py`, `docs/flows.py`, `docs/assets/site.js` |
| **Candidate Name & Primary Title** | `Gautam Reddy` — `Business Analyst` | `Gautam Reddy` — `Business Analyst` (`REST API & Payment Gateway Integrations \| Swagger/OpenAPI \| SQL \| SIT/UAT`) | `docs/index.html`, `docs/about.html`, `docs/resume.html`, `docs/build.py` (JSON-LD `Person`) |
| **Professional Summary & Hero Lead** | Generic BA summary mentioning NFRs and STTM | Technical Business Analyst with 4+ years of experience, strongest in payment gateway and REST API integrations. Writes the BRDs, FRDs, SRS documents, Swagger/OpenAPI contract reviews, JSON/XML data mappings and reconciliation rules that Engineering and QA build from, then carries them through SIT, UAT and go-live. Latest project: 2 payment gateway integrations and 350+ test cases with zero critical defects. | `docs/index.html`, `docs/about.html`, `docs/resume.html`, `docs/build.py` |
| **Company Name Spelling (Roles 3 & 4)** | `Infocomm IT Services Pvt Ltd` | `Iinfocomm IT Services Pvt Ltd` | `docs/index.html`, `docs/about.html`, `docs/resume.html`, `docs/build.py`, `docs/flows.py` |
| **Role Date Ranges** | Dates omitted on role headers | Added exact tenure dates: `Oct 2023 to Nov 2024` (Marolix), `Feb 2023 to Mar 2023` (V Moksha), `Apr 2022 to Dec 2022` (Iinfocomm BA), `Nov 2020 to Apr 2022` (Iinfocomm ASE) | `docs/index.html`, `docs/about.html`, `docs/resume.html`, `docs/build.py` |
| **Experience Bullets (`resume.html`)** | 15 older summary bullets | **13 verbatim resume bullets** (7 for Marolix, 1 for V Moksha, 3 for Iinfocomm BA, 2 for Iinfocomm ASE) and updated `#sfCount` to `Showing 13 of 13 bullets` | `docs/resume.html`, `docs/build.py` |
| **Core Competencies & Tools** | 6 older skill meter groups and 8 tool tags | **4 exact resume competency groups** (`Requirements & Documentation`, `API & Integration`, `Data & Reporting`, `Delivery & Testing`) + **13 tool tags** (`JIRA`, `Confluence`, `Azure DevOps`, `Visio`, `Lucidchart`, `Figma`, `Postman`, `SQL`, `Python (Pandas)`, `Power BI`, `Excel`, `Azure`, `AI-assisted documentation`) | `docs/resume.html`, `docs/index.html`, `docs/build.py` |
| **Education & Certifications** | Included `Target completion: 2026/2027` on CBAP | **B.Tech, Mechanical Engineering (Minor: Computer Science)**, Biju Patnaik University of Technology • `2016 to 2020`; **Google Data Analytics Professional Certificate** (Coursera), 2023; CBAP removed per instruction | `docs/resume.html`, `docs/build.py`, `docs/flows.py` |

## 2. File-by-File & Page-by-Page Detailed Diff Breakdown

### 2.1 `docs/resume.html` (Generated via `docs/build.py` `resume()`)

#### Page Header & Meta Tags
- **`<title>`:** Updated to `Resume | Gautam Reddy, Business Analyst`.
- **`<h1>`:** Updated to `Gautam Reddy — Business Analyst`.
- **Lead Paragraph (`.lead`):**
  > Business Analyst with 4+ years of experience, strongest in payment gateway and REST API integrations. Writes the BRDs, FRDs, SRS documents, Swagger/OpenAPI contract reviews, JSON/XML data mappings and reconciliation rules that Engineering and QA build from, then carries them through SIT, UAT and go-live.

#### Proof Strip Cards (`.proof`)
- **Card 1 (`100K+`):** `Marolix • SQL & Azure` — `transaction records validated`
- **Card 2 (`350+`):** `SIT, UAT & Regression` — `test cases cleared (0 critical defects)`
- **Card 3 (`20+`):** `Requirements Elicitation` — `workshops facilitated across 13+ stakeholders`
- **Card 4 (`12+`):** `Marolix • Scope & CRs` — `change requests managed across 2 SAFe releases`
- **Note:** `Metrics from resume and past project delivery records (Nov 2020 – Nov 2024).`

#### Professional Experience (`4` Roles, `13` Verbatim Bullets)
1. **Business Analyst** — *Marolix Technology Solutions Pvt Ltd, Hyderabad • Oct 2023 to Nov 2024*
   - `[api requirements]` Specified **2 payment gateway integrations** in build-ready detail by defining REST API requirements, reviewing Swagger/OpenAPI contracts, JSON/XML payloads, HTTP status codes and error handling, testing endpoints in Postman, and drawing UML workflows and data mappings (Visio, Lucidchart).
   - `[uat]` Cleared **350+ test cases** with zero critical defects by coordinating SIT, UAT and regression testing with QA and Engineering, triaging defects in JIRA, and supporting go-live and user training.
   - `[sql bi]` Surfaced **3 recurring SLA breach patterns** across **100,000+ transaction records** by running SQL validation and reconciliation checks and Python (Pandas) analysis on Azure, then reporting the results in Power BI for process-improvement actions.
   - `[requirements]` Aligned **13+ stakeholders** on scope across **20+ requirements workshops** by documenting each outcome as a BRD, FRD, SRS, use case and set of BDD acceptance criteria, drafted with AI-assisted documentation tools.
   - `[requirements uat]` Kept **12+ change requests** across **2 SAFe releases** under control by assessing each one’s impact on requirements and keeping the RTM current.
   - `[requirements uat]` Held **4 modules** to a clear MoSCoW priority order and pushed back on 3 feature requests with no business justification, working through JIRA and Azure DevOps backlog refinement with the Product Owner and Scrum Master.
   - `[requirements api]` Documented compliance requirements for both payment integrations and kept data dictionaries and field mappings current in Confluence and Excel, so developers built and validated against one source.
2. **Business Analyst** — *V Moksha Technologies Pvt Ltd, Bengaluru • Feb 2023 to Mar 2023*
   - `[sql requirements]` Saved **2 weeks per improvement cycle** by mapping AS-IS and TO-BE processes and running SQL, fishbone and 5-Why root-cause analysis on recurring SLA shortfalls, using Lean and Six Sigma methods to cut error recurrence and rework.
3. **Business Analyst** — *Iinfocomm IT Services Pvt Ltd, Bengaluru • Apr 2022 to Dec 2022*
   - `[requirements]` Delivered **3 concurrent modules** on time by running Three Amigos sessions and turning stakeholder needs into functional requirements and BDD acceptance criteria.
   - `[requirements api]` Covered **4 business units** with documented functional requirements, business rules and control requirements, reviewed API contracts against them, and maintained the RTM and RACI.
   - `[uat]` Reached zero reported post-launch incidents on the delivered modules by coordinating UAT, smoke, sanity and regression testing across **50+ JIRA-tracked test cases**.
4. **Associate Software Engineer → Promoted to BA** — *Iinfocomm IT Services Pvt Ltd, Bengaluru • Nov 2020 to Apr 2022*
   - `[bi requirements]` Earned a move to Business Analyst after 17 months, **six months ahead of the expected timeline**, by taking 3 reporting features from elicitation to stakeholder acceptance and turning input from **15+ Finance and Operations stakeholders** into Power BI requirements and BDD user stories.
   - `[bi requirements]` Won executive approval for a reporting automation business case projecting **3+ hours of weekly manual-effort savings**.

#### Core Competencies & Technical Skills Sidebar (`.resume-side-card`)
- **Requirements & Documentation (`4+ yrs`):** `BRD, FRD, SRS, User Stories, Use Cases, BDD/Gherkin Acceptance Criteria, Business Rules, Gap & Impact Analysis, AS-IS/TO-BE, MoSCoW, RTM, Stakeholder Management`
- **API & Integration (`4+ yrs`):** `REST APIs, Swagger/OpenAPI, JSON, XML, HTTP Methods & Status Codes, API Contract Review, Error Handling, Data Mapping, Postman, BPMN/UML, Sequence & Workflow Diagrams`
- **Data & Reporting (`4+ yrs`):** `SQL (data validation, reconciliation), Python (Pandas), Power BI, Excel, Azure, Root Cause Analysis`
- **Delivery & Testing (`4+ yrs`):** `Agile/Scrum, SAFe, SDLC, SIT/UAT, Regression Testing, Defect Triage, Change Management, Backlog Refinement`
- **Tools (`.side-tags`):** `JIRA`, `Confluence`, `Azure DevOps`, `Visio`, `Lucidchart`, `Figma`, `Postman`, `SQL`, `Python (Pandas)`, `Power BI`, `Excel`, `Azure`, `AI-assisted documentation`

#### Education & Certifications (`dl.facts`)
- **Education:** **B.Tech, Mechanical Engineering (Minor: Computer Science)**, Biju Patnaik University of Technology • 2016 to 2020.
- **Certification:** **Google Data Analytics Professional Certificate** (Coursera), 2023.

### 2.2 `docs/index.html` (Homepage)

- **Hero `<h1>`:** Updated to `Technical Business Analyst in Bengaluru who turns requirements into testable specs.`
- **Hero Lead (`.lead`):** Updated to `Technical Business Analyst with 4+ years of experience, strongest in payment gateway and REST API integrations. Writing the BRDs, FRDs, SRS documents, Swagger/OpenAPI contract reviews, JSON/XML data mappings and reconciliation rules that Engineering and QA build from, then carrying them through SIT, UAT and go-live.`
- **Hero Fact Strip (`.hero-fact-strip`):** Updated 3rd metric to `350+ Test Cases` (`SIT & UAT Coordinated`).
- **Skills Marquee (`MARQ_ITEMS`):** Updated to `Requirements Gathering`, `BRD / FRD / SRS`, `User Stories & BDD`, `Traceability Matrix (RTM)`, `Process Modelling (BPMN / UML)`, `REST API & Payment Gateways`, `Swagger / OpenAPI`, `JSON / XML Data Mapping`, `SQL & Python (Pandas)`, `Power BI, Excel & Azure`, `SIT / UAT & Defect Triage`, `Agile / Scrum & SAFe`.
- **Proof Section (`#proof`):** Updated all 4 proof cards to reflect SQL/Pandas validation on Azure (`100K+`), SIT/UAT/regression test cases cleared in JIRA (`350+`), requirements workshops (`20+` across `13+` stakeholders producing BRDs, FRDs, SRS, use cases, and BDD criteria), and payment gateway integrations (`2` with REST APIs, Swagger/OpenAPI contracts, JSON/XML payloads, and UML flows).
- **Skills & Delivery Toolkit (`#toolkit`):** Updated evidence descriptions inside `BA_WORKFLOW`, `PROCESS_WORKFLOW`, `AGILE_WORKFLOW`, and `TECH_WORKFLOW` to include `SRS`, `Lean and Six Sigma`, `JSON/XML payloads`, `2 SAFe releases`, `JIRA & Azure DevOps backlog refinement`, `SIT, UAT and regression testing`, `Iinfocomm`, `Swagger/OpenAPI contract review`, `Azure`, and `Visio & Lucidchart`.
- **Experience Timeline (`#experience`):** Synchronized all 4 roles, company names (`Iinfocomm IT Services Pvt Ltd`), date ranges (`Oct 2023 to Nov 2024`, `Feb 2023 to Mar 2023`, `Apr 2022 to Dec 2022`, `Nov 2020 to Apr 2022`), bullet points, and collapsible `.role-metrics` trays (`17 mos / Promoted 6 mos early`, `Lean / 6σ`, `2 SAFe releases`).

### 2.3 `docs/about.html` (About Page)

- **3D BA Console Header:** Updated name to `Gautam Reddy` and subtitle to `Business Analyst • REST APIs, Swagger/OpenAPI, SQL & SIT/UAT`.
- **About Lead (`.about-lead`):** Updated to match the Business Analyst summary from the resume.
- **What I Do Grid (`.what-i-do-grid`):**
  - *Elicitation & Scoping:* `Facilitating stakeholder workshops (20+ sessions across 13+ stakeholders), managing backlogs in JIRA and Azure DevOps, and prioritizing scope with MoSCoW.`
  - *Requirements & Specs:* `Writing BRDs, FRDs, SRS documents, use cases, BDD/Gherkin acceptance criteria, Swagger/OpenAPI contract reviews, and JSON/XML data mappings.`
  - *Data & Process Analysis:* `SQL validation and Python (Pandas) reconciliation on 100K+ records on Azure, Power BI reporting, and AS-IS / TO-BE process modelling (Visio, Lucidchart, BPMN/UML).`
  - *Testing & UAT Delivery:* `Requirements Traceability Matrix (RTM), SIT, UAT and regression testing across 350+ test cases, JIRA defect triage, and SAFe release change management.`
- **Career Path & Promotions Timeline (`.roles`):** Updated all 4 role cards with exact tenure dates (`Oct 2023 to Nov 2024`, `Feb 2023 to Mar 2023`, `Apr 2022 to Dec 2022`, `Nov 2020 to Apr 2022`), `Iinfocomm IT Services Pvt Ltd` spelling, `Promoted 6 mos early` badge (`after 17 months`), and resume-aligned narratives.

### 2.4 `docs/flows.py` (Decorative SVG Sequence Diagrams) & Structured Data

- **`docs/flows.py`:**
  - Updated `Infocomm` to `Iinfocomm` across `seq_resume` and `seq_resume_uat`.
  - Updated specification message labels to reference `Swagger/OpenAPI, Data Mapping`, `BRD, FRD, SRS, BPMN/UML, Data Mapping`, and `continuousTraceabilityAndCBAPInProgress()`.
  - Kept `sendEnquiryEmail(gautamreddy098@gmail.com)` in `seq_contact`.
- **JSON-LD Structured Data (`PERSON` in `docs/build.py`):**
  - Updated `name` to `"Gautam Reddy"`, `jobTitle` to `"Technical Business Analyst"`, and `knowsAbout` to the exact resume skill set (without exposing phone or changing email).
  - Removed resume download / save-as-PDF button on `resume.html`.
