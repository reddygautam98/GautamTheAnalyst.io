# Functional Requirements Document (FRD)
## PayTrack — Payment Reconciliation & Exception Management

> **Portfolio demonstration only.** Fictional workflow and sample values. Requirements are illustrative and not a production-ready integration specification.

| Document control | Detail |
|---|---|
| Document ID | PT-FRD-001 |
| Related BRD | PT-BRD-001 |
| Version | 1.0 — sample |
| Status | Draft for review |

## 1. Purpose
Translate the high-level BRD into system behavior that design, engineering, QA and UAT can discuss and validate. Implementation details such as final API contracts, security controls, source mappings and performance thresholds must be agreed with delivery teams.

## 2. Actors and permissions
| Role | View/search | Assign case | Add note | Resolve case | Export |
|---|---:|---:|---:|---:|---:|
| Operations Analyst | Yes | Yes | Yes | Per policy | Per policy |
| Operations Lead | Yes | Yes | Yes | Yes, per policy | Per policy |
| Read-only Reviewer | Yes | No | No | No | Per policy |
| Administrator | Configured access only | Configured access only | Configured access only | Configured access only | Configured access only |

The final permission matrix must be reviewed by the access-control owner. The table is a proposal, not an implemented security guarantee.

## 3. Functional requirements
| ID | Requirement | Expected behavior | Priority |
|---|---|---|---|
| FR-001 | Transaction search | Search supports approved payment ID, gateway reference, merchant reference and date range. | Must |
| FR-002 | Search validation | Invalid date range or unsupported criteria produce a clear message; no silent result. | Must |
| FR-003 | Transaction detail | Detail shows internal and gateway references, amount, currency, status and relevant timestamps where available. | Must |
| FR-004 | Reconciliation status | Status values use an agreed mapping and include a reason for unmatched results. | Must |
| FR-005 | Exception creation | An unmatched or inconsistent result can create an exception with category, source transaction and creation time. | Must |
| FR-006 | Case assignment | Authorized users can assign an owner; the action is reflected in the case history. | Must |
| FR-007 | Case notes | Users can add a timestamped note without overwriting previous notes. | Must |
| FR-008 | Resolve case | Authorized users must choose a resolution type and enter a non-empty resolution note. | Must |
| FR-009 | Audit history | Status, assignment and resolution events record actor, action and timestamp. | Must |
| FR-010 | Queue filters | Users can filter by status, category, owner, date and age where data exists. | Should |
| FR-011 | Operational summary | Summary cards and charts reflect the same filtered dataset as the queue. | Should |
| FR-012 | Export | An authorized user can export the approved columns and active filter context. | Could |

## 4. Core business logic
1. Normalize configured matching fields using an approved mapping.
2. Apply the agreed match criteria to internal and gateway records.
3. Record a matched outcome when all required criteria pass.
4. Record an unmatched outcome with one or more reason codes when a required criterion fails.
5. Avoid duplicate case creation for repeat delivery of the same gateway event by using an agreed idempotency key.
6. Allow a case to be resolved only by an authorized role with a resolution type and explanatory note.
7. Preserve the before/after state in audit history; do not delete original source values when resolving a mismatch.

The final precedence for pending, failed, reversed, duplicate and late events needs business approval.

## 5. Screen and interaction requirements
### 5.1 Reconciliation overview
- Display transaction count, matched count, open exceptions and failed/pending counts for the selected filters.
- Show the filter state and a clear way to reset filters.
- Provide recent transactions with identifiable status labels.
- Each KPI must define its calculation, time window, inclusion/exclusion rules and currency treatment.

### 5.2 Exception detail
- Display a case ID, category, status, owner and creation/update timestamps.
- Show internal and gateway values side by side for relevant fields.
- Highlight discrepancies without relying on color alone.
- Provide assign, add-note and resolve actions according to role permissions.
- Show an append-only audit timeline.

### 5.3 Empty, error and loading states
- Empty results: explain that no records match the current filter and offer a reset action.
- Loading: show a visible progress state without suggesting stale results are current.
- Service error: display a non-sensitive message and a retry or support path where appropriate.
- Unauthorized action: explain that the user lacks permission; do not mutate the case.

## 6. Data requirements (logical)
| Entity | Key fields (sample) | Notes |
|---|---|---|
| Payment transaction | payment ID, merchant reference, amount, currency, status, created time | Source-of-truth mapping to be agreed. |
| Gateway event | event ID, payment ID/reference, event type, received time | Duplicate and late event behavior to be defined. |
| Reconciliation result | result ID, payment ID, outcome, reason code, compared time | Must be traceable to the rule version. |
| Exception case | case ID, payment ID, category, status, owner, resolution | Required fields and lifecycle to be approved. |
| Audit event | audit ID, actor, action, timestamp, before/after reference | Retention and sensitive-data rules require review. |

## 7. Non-functional requirements to confirm
- **Security:** least-privilege access, secure transport, secret management and approved authentication.
- **Privacy:** data minimization, masking, retention and export policies.
- **Auditability:** reliable actor/action/timestamp capture, with a defined retention period.
- **Availability and recovery:** service objectives, retry behavior and operational support are to be agreed.
- **Performance:** target search latency and supported transaction volume must be baselined with stakeholders; no unverified SLA is asserted.
- **Accessibility:** keyboard operation, visible focus, labels for form fields, adequate contrast and status indicators that do not depend on color alone.
- **Observability:** logs and metrics without exposing sensitive payment data.

## 8. Error and validation handling
- Required fields are validated on the client and server.
- Monetary values use defined decimal precision and currency context.
- Duplicate submissions must be handled idempotently where a stable request/event key exists.
- Invalid transitions are rejected and leave the previous state intact.
- Error responses must not reveal secrets or internal implementation details.

## 9. Dependencies and open decisions
- Gateway webhook/event schema and authentication.
- Approved transaction source and field ownership.
- Matching and duplicate-detection rules.
- Currency/rounding policy and time-zone conventions.
- Case lifecycle, reopen/close policy, and escalation thresholds.
- Role model, export rules, audit retention and operational support model.

## 10. Definition of ready for development
A requirement can be considered ready when the owner, trigger, inputs, output, validation, permissions, error states and acceptance criteria are agreed; dependencies are identified; and QA can create positive, negative and boundary tests.

---
**Portfolio note:** This FRD illustrates requirement decomposition and handoff quality. It is not a verified API contract, security review, or production solution design.
