# Discovery Workshop — Minutes, Decisions & RAID
## PayTrack — Payment Reconciliation & Exception Management

> **Fictional workshop template.** The attendees, dates, decisions and action descriptions below are illustrative examples and do not represent a real client meeting.

## 1. Meeting details
| Field | Detail |
|---|---|
| Meeting ID | PT-MOM-001 |
| Date | 15 October 2026 (sample date) |
| Duration | 60 minutes (illustrative) |
| Purpose | Understand current reconciliation workflow and exception-handling needs |
| Facilitator | Business Analyst |
| Attendees | Product Owner, Operations Lead, Operations Analyst, Engineering, QA — roles only, names to be confirmed |

## 2. Agenda
1. Current reconciliation workflow and pain points.
2. Source systems and important transaction fields.
3. Matching logic and common mismatch types.
4. Exception assignment, escalation and resolution.
5. Audit, permissions, reporting and UAT.
6. Decisions, open questions and next actions.

## 3. Discussion summary
- Participants need a clear way to search for a transaction and compare internal and gateway values.
- Mismatch categories should use agreed business definitions rather than free-text labels alone.
- Exception ownership and aging should be visible.
- Resolution should capture a reason and note; a history of important changes is required.
- Matching rules, role permissions, retention and escalation thresholds require explicit approval before implementation.

## 4. Decision log (illustrative)
| ID | Decision / working agreement | Status | Owner |
|---|---|---|---|
| DEC-01 | Show internal and gateway references together on transaction detail. | Proposed | Product Owner |
| DEC-02 | Require a resolution type and note to close a case. | Proposed | Operations Lead |
| DEC-03 | Preserve material assignment/status changes in an audit timeline. | Proposed | Product + Engineering |
| DEC-04 | Do not initiate refunds or financial adjustments in the initial sample scope. | Proposed | Business Sponsor |
| DEC-05 | Confirm matching criteria and duplicate-event handling after source mapping review. | Open | Product + Engineering |

## 5. Action register
| ID | Action | Owner role | Due date | Status |
|---|---|---|---|---|
| ACT-01 | Provide field-level source-of-truth mapping. | Operations + Engineering | To agree | Open |
| ACT-02 | Confirm match tolerances, currencies and rounding policy. | Finance / Operations | To agree | Open |
| ACT-03 | Draft case categories, resolution types and escalation thresholds. | Operations Lead | To agree | Open |
| ACT-04 | Review role permissions, audit retention and export constraints. | Security / Compliance | To agree | Open |
| ACT-05 | Review draft user stories and acceptance criteria. | Product + QA | To agree | Open |

## 6. RAID log
| ID | Type | Item | Impact | Response / next step | Owner |
|---|---|---|---|---|---|
| RAID-01 | Risk | Delayed or duplicated gateway events may cause inconsistent results. | Incorrect or duplicate case handling. | Define idempotency and late-event behavior. | Engineering |
| RAID-02 | Assumption | Stable transaction identifiers are available for matching. | Matching may be incomplete if false. | Validate sample source extracts. | Data / Engineering |
| RAID-03 | Issue | Authoritative source for each key field is not yet agreed. | Requirements and test outcomes may be ambiguous. | Complete source-of-truth matrix. | Product Owner |
| RAID-04 | Dependency | Role and retention policy needs control-owner review. | Access and audit acceptance cannot be finalized. | Schedule security/compliance review. | Product Owner |
| RAID-05 | Decision | Escalation threshold is open. | Queue prioritization cannot be finalized. | Agree age and severity thresholds. | Operations Lead |

## 7. Next meeting
Proposed focus: review source mapping, confirm business rules, resolve open decisions and approve the first requirement baseline. Date and attendees to be confirmed.

---
**Portfolio note:** Minutes should record what participants actually said and decided. This fictional sample is a format example, not evidence that the workshop occurred.
