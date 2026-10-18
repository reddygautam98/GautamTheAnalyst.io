# User Stories & Acceptance Criteria
## PayTrack — Payment Reconciliation & Exception Management

> Fictional portfolio example. Given/When/Then statements are proposed acceptance criteria for discussion, not evidence of executed tests.

## Epic EP-01 — Find and review transactions

### US-001 — Search for a payment
**As an** Operations Analyst, **I want** to search using a payment or gateway reference, **so that** I can find the record I need to investigate.

**Acceptance criteria**
- **Given** a valid known reference, **when** I submit the search, **then** the matching record is displayed with its current status.
- **Given** no record matches, **when** the search completes, **then** an explicit empty state appears and no stale row is presented as a match.
- **Given** an invalid date range, **when** I submit the filters, **then** a validation message explains how to correct it.

### US-002 — Compare internal and gateway values
**As an** Operations Analyst, **I want** to see comparable internal and gateway fields together, **so that** I can identify a mismatch without switching between tools.

**Acceptance criteria**
- **Given** both records exist, **when** I open transaction detail, **then** the internal reference, gateway reference, amount, currency and statuses are shown where available.
- **Given** a required field differs, **when** the reconciliation result is shown, **then** the difference and its reason code are visible.
- **Given** a source value is missing, **when** the detail loads, **then** the field is marked unavailable rather than silently replaced with a default.

## Epic EP-02 — Manage exceptions

### US-003 — Assign an exception
**As an** Operations Lead, **I want** to assign an exception to an owner, **so that** responsibility for the next action is clear.

**Acceptance criteria**
- **Given** I have assignment permission and the case is open, **when** I select an active owner and confirm, **then** the case shows the new owner.
- **Given** assignment succeeds, **then** the actor, time and previous/new owner are present in the audit history.
- **Given** the selected owner is unavailable or the update fails, **then** the case remains unchanged and a clear error is shown.

### US-004 — Record a resolution
**As an** Operations Analyst with resolution permission, **I want** to record a resolution type and note, **so that** the case can be closed with an explanation.

**Acceptance criteria**
- **Given** the resolution type or note is missing, **when** I submit, **then** required-field validation is shown and the case remains open.
- **Given** valid resolution details and permission, **when** I confirm, **then** the case status changes and the audit history records the action.
- **Given** I lack resolution permission, **when** I try to resolve, **then** the action is blocked and no state change occurs.

## Epic EP-03 — Preserve traceability

### US-005 — Review audit history
**As a** Read-only Reviewer, **I want** to inspect material changes to a case, **so that** I can understand who changed what and when.

**Acceptance criteria**
- **Given** a case has been assigned and updated, **when** I open its audit history, **then** events are displayed in chronological order.
- **Given** a status or owner changes, **then** an event includes actor, action and timestamp.
- **Given** no events exist, **then** the interface displays an empty history state rather than an error.

## Prioritization (sample)
| Story | Priority | Dependency |
|---|---|---|
| US-001 Search | Must | Searchable source fields |
| US-002 Compare values | Must | Source mapping and match rules |
| US-003 Assign case | Must | Role model and case lifecycle |
| US-004 Record resolution | Must | Approved resolution categories |
| US-005 Audit history | Must | Audit event schema and retention |

## Review checklist
- Actor and business value are clear.
- Acceptance criteria include expected and negative behavior.
- Permission and failure cases are considered.
- Dependencies and unresolved policy choices are recorded.
- QA can derive test cases without guessing the outcome.

---
**Portfolio note:** Story IDs, roles and behavior are illustrative and should be refined with real product and engineering stakeholders.
