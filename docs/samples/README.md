# PayTrack Sample Business Analysis Portfolio Pack

> **SAMPLE ONLY — FICTIONAL PORTFOLIO CASE STUDY.** Product, organizations, user names, dates, transaction IDs, currency amounts, targets and scenarios are illustrative. Do not represent these artifacts as completed client work.

## Scenario
PayTrack is a fictional payment reconciliation and exception-management portal concept. It compares internal payment records with gateway events, helps operations staff investigate unmatched transactions, assigns exception ownership, captures resolution notes and preserves an audit trail.

## Formal sample documents (PDF + editable Word)
- `docs/01_BRD_PayTrack_Sample.pdf` / `.docx` — problem statement, goals, scope, stakeholders, assumptions, business requirements, risks and sign-off template.
- `docs/02_FRD_PayTrack_Sample.pdf` / `.docx` — functional requirements, business rules, validation, data entities, screen behavior, NFRs, error states and open decisions.
- `docs/03_User_Stories_Acceptance_Criteria_Sample.pdf` / `.docx` — prioritised user stories with Given/When/Then criteria and Definition of Ready/Done.
- `docs/04_RTM_Test_Cases_UAT_Plan_Sample.pdf` / `.docx` — requirement traceability, test cases, UAT approach, entry/exit criteria and sign-off template.
- `docs/05_Discovery_Workshop_MoM_Decision_Log_Sample.pdf` / `.docx` — discovery workshop minutes, decision log, action tracker and RAID log.
- `docs/PayTrack_Sample_BA_Documentation_Bundle.pdf` — combined PDF containing all five documents.

## Diagrams and design
- `diagrams/Payment_Reconciliation_Process.svg` + `.mmd` — illustrative business process flow.
- `diagrams/Payment_Conceptual_Architecture.svg` — conceptual component layout.
- `diagrams/Payment_Data_Model_ERD.svg` + `.mmd` — logical data model.
- `diagrams/Payment_API_Sequence.mmd` — editable Mermaid sequence source.
- Editable Figma wireframes (overview dashboard + exception case detail): https://www.figma.com/design/qt1PFmcQNvtaJnLnrWxPKD
- Editable FigJam process, API sequence and ERD diagrams: https://www.figma.com/board/N90uAbHaqe4OkCOUkNfNxX

## Structured files
- `specs/requirements_traceability.csv` — BR → FR → story → test traceability.
- `specs/sample_test_cases.csv` — test scenarios, preconditions, steps, expected outcomes and execution status.
- `specs/sample_user_stories.csv` — structured backlog starter.

## Using the web gallery
Open `index.html` in a browser to view the artifact gallery. To publish it on GitHub Pages, copy the full package contents under a `samples/` directory in the portfolio repository. The gallery links are relative to that directory, with the return link targeting the website home page one level up.

## Important boundaries
- Success measures in the BRD are proposed example targets, not results achieved.
- Test cases have status `Not Run`; no test execution evidence is implied.
- Matching keys, approval policies, data retention, export authorization, load assumptions and integration contracts need stakeholder confirmation.
- Figma frames contain editable native layers; labels and values in the screens are illustrative.


## Site entry point
Open [`index.html`](index.html) locally. For GitHub Pages, publish the complete folder beneath `samples/` so the document, diagram, and CSV links resolve.
