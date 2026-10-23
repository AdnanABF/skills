# Solution Design Workflow and Templates

## 1. Brief

Capture a short brief, preferably on an existing suitable page:

- Problem and measurable outcome.
- Actors, roles, and primary tasks.
- In-scope modules and explicit exclusions.
- Platforms, target devices, accessibility needs, and brand constraints.
- Existing systems and confirmed integrations.
- Constraints: security, privacy, tenancy, connectivity, scale, timeline.
- Confirmed requirements, proposed decisions, assumptions, open questions.

Use stable identifiers only where they help traceability, for example `REQ-01`, `JRN-01`, `SCR-01`, and `MOD-01`. Do not add process overhead to a small design change.

## 2. Suggested File Structure

Adapt to the existing file rather than recreating it. Do not create empty placeholder pages for artifacts outside the scope.

| Page | Possible content |
| --- | --- |
| 01 — Brief & Decisions | Goals, requirements, assumptions, decision log |
| 02 — Solution Overview | Context diagram and module responsibilities |
| 03 — Architecture & Data | Application/container boundaries, data ownership, conceptual entity model, sequences |
| 04 — Roles & Journeys | Role matrix, swimlanes, alternate and failure paths |
| 05 — Screen Map & Wireframes | Navigation, priority journey, low-fidelity boards |
| 06 — UI System | Colors, typography, spacing, components, states |
| 07 — Screens & Prototype | Visual screens and linked journeys |
| 08 — Handoff | Traceability, decisions, open issues, verification notes |

## 3. Architecture Deliverables

Choose appropriate views, not every possible diagram:

- **Context:** people, the system under design, external systems, and trust boundaries.
- **Application/container:** clients, backend, storage, integration adapters, and jobs when justified. Label module boundaries differently from independently deployed services.
- **Conceptual data:** entities, cardinality, ownership, lifecycle, and sensitive-data boundaries. Do not present this as a migrated database schema.
- **Critical sequence:** actors, calls, persistence, external work, observable status, failure/retry, and authorization points.

For request flows involving long-running or external work, default to persisting local state before background execution unless synchronous behavior is explicitly required. Show enqueue/commit ordering and status/retry responsibilities where relevant. Avoid unexplained infrastructure.

Use a small consistent visual vocabulary. Label relationships with meaning such as “submits application,” “reads enrollment,” or “publishes status,” not just unlabeled arrows. Distinguish existing and proposed elements without relying on color alone.

## 4. Journey and UI Deliverables

Start with one end-to-end journey, including its entry and successful outcome:

1. Role and prerequisites.
2. Entry point and navigation.
3. Key decisions and inputs.
4. Validation, permission denial, cancellation, and recoverable errors.
5. Pending/background state if work continues after submission.
6. Completion, feedback, and next step.

Review wireframes before a large high-fidelity expansion. Reuse existing components and tokens first. If none exist, propose a restrained visual direction and identify it as provisional rather than claiming brand approval.

For the agreed screens, specify relevant loading, empty, error, disabled, saving, and success states. Use realistic but non-sensitive content. Document keyboard order, visible focus, accessible labels, and responsive behavior; a drawing does not prove runtime accessibility.

Prototype the meaningful actions, including back/cancel and failure recovery where supported. Clearly annotate unsupported or simulated behavior rather than adding misleading clickable controls.

## 5. Traceability and Handoff

Example mapping (illustrative, not an existing API contract):

| Requirement | Journey | Screen/action | System responsibility | Entity | Status |
| --- | --- | --- | --- | --- | --- |
| REQ-01: submit a request | JRN-01 | SCR-03 / Submit | MOD-02 validates, authorizes, persists, schedules processing | Request | Proposed |

Summarize the pages/boards changed, verified journeys, assumptions needing approval, architectural tradeoffs, and implementation gaps. Include available Penpot links or IDs without fabricating URLs. Treat prototype navigation, backend implementation, and deployed behavior as separate verification levels.
