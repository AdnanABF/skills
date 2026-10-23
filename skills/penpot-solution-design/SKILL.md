---
name: penpot-solution-design
description: Use when designing or reviewing software solution architecture, user journeys, wireframes, UI systems, or clickable prototypes in Penpot through MCP.
---

# Penpot Solution Design

## When to Use

Use for editable visual software blueprints in Penpot: architecture, product/UX design, or both. Connect business requirements to system responsibilities and user-facing behavior. Adapt the depth to the request; a small screen revision does not need a complete architecture exercise.

Non-triggers: implementing application code from an approved design without changing the design; generic architecture discussion with no Penpot deliverable; configuring OpenCode or MCP itself. Use the relevant implementation or configuration guidance for those tasks.

## Required and Optional Companions

- For UI design, read the matching shared frontend skills before applying the Penpot implementation guidance. Product behavior belongs to those skills; Penpot mechanics belong here.
- Admin listing design: `frontend-admin-panels.md`, `frontend-listing-screens.md`, and `frontend-ui-states.md`.
- Admin detail/edit design: `frontend-admin-panels.md`, `frontend-forms.md`, `frontend-ui-states.md`, then `frontend-admin-detail-pages.md`.
- Other UI: load `frontend-forms.md`, `frontend-ui-states.md`, `frontend-auth-entry-ui.md`, or `frontend-interaction-patterns.md` when those behaviors are being designed. Load dynamic-field companions only when metadata-generated UI is in scope.
- Responsive, device-specific, or safe-area design: `frontend-device-layout.md`.
- Existing project app mappings or backend connections: `project-connections.md`.
- Do not load Flutter/Next.js implementation adapters merely because those technologies appear in a diagram. Load them when implementation work is explicitly requested. Likewise, a proposed API box does not by itself activate backend code skills.
- A Penpot mobile prototype alone does not activate `frontend-mobile-app-prototyping.md`; that skill applies to browser-hosted app prototypes with its stated presentation requirements.

## Working Contract

1. Confirm the requested outcome, scope, audience, target file, and priority journey. Use information already provided; ask only for missing decisions that materially affect the design.
2. Separate confirmed facts, proposed decisions, assumptions, and open questions. Never portray an inferred backend, endpoint, permission, or integration as implemented.
3. Keep design work in Penpot. Do not edit application code, deploy, install packages, or change MCP configuration without a separate explicit request.
4. Inspect the connected file before mutations. Preserve unrelated content, library assets, and user work. Ask before deleting or replacing existing work or changing shared assets with wider impact.
5. Establish the architecture and one complete core journey before expanding into many screens. Use review checkpoints for substantial decisions, not for every shape.
6. Prefer the simplest architecture that satisfies the constraints. Do not invent microservices, queues, caches, or infrastructure without a reason.
7. Use native editable text, shapes, and paths; components and tokens where useful. A flattened image is not a substitute for an editable deliverable.
8. Represent security at the system boundary: server-side authorization, tenant boundaries, sensitive data, external integrations, and failure/retry behavior where relevant. Hiding a UI control is not authorization.
9. Label connector directions and meanings. Distinguish synchronous calls, asynchronous jobs/events, and conceptual relationships with a legend when mixed.
10. Verify each completed batch structurally and visually. Do not claim a prototype is a working backend or that untested navigation works.

## Workflow

Follow [the design workflow](references/design-workflow.md) for discovery, architecture, UX, and handoff templates. Create only the pages and artifacts needed for the agreed scope.

1. **Discover:** users, goals, roles, business rules, constraints, current systems, and success criteria.
2. **Inspect:** connected file identity, pages, existing target boards, styles, and reusable assets. If the target is ambiguous, ask before editing.
3. **Outline:** propose page/board structure, architecture level, initial journey, fidelity, and review checkpoints.
4. **Model:** context, applications/modules, conceptual data, and critical sequences at the appropriate depth.
5. **Design:** journey and screen map, wireframes, then visual UI and reusable assets after the structure is settled.
6. **Connect:** prototype the agreed journey and maintain requirement-to-screen-to-system traceability.
7. **Review:** inspect diagram readability, UI states, layout, relevant device sizes, and prototype navigation. Record unresolved decisions.
8. **Handoff:** report changed pages/boards, design links or identifiers when available, decisions, checks performed, and unverified behavior.

## Penpot MCP Execution

Read [the MCP execution reference](references/penpot-mcp.md) before using Penpot tools. Read the server's high-level overview once per conversation before using other Penpot tools; do not repeat it if already loaded. Discover tools and API documentation rather than guessing methods, shape properties, or capabilities.

If the plugin is not attached to a design file, report the blocker and ask the user to connect it. Do not reinstall or reconfigure the already available MCP server as a workaround. Read-only review requests remain read-only even with writable tools available.

## Verification

- Scope and target file are established; unrelated designs are preserved.
- Facts, assumptions, proposals, and unresolved questions are distinguishable.
- Architecture boundaries, connector labels/directions, and data ownership are coherent; permission and failure paths are represented where relevant.
- The priority journey connects relevant screens to system responsibilities without claiming invented contracts exist.
- Edited content is editable, semantically named, and consistent with existing design assets.
- Inspect exports at a useful zoom: no clipped text, unintended overlap, missing labels, unreadable connectors, or accidental overflow.
- UI review covers relevant viewports, contrast, focus/keyboard intent, validation, loading/empty/error states, and recovery. Mark behavior that a static canvas cannot verify as a specification, not a passed runtime test.
- Inspect prototype destinations and triggers; exercise the agreed path in a viewer when available. Distinguish configured interactions from viewer-tested interactions.
- Report checks actually performed and limitations; if export/viewer tools are unavailable, disclose the missing visual/interaction verification.
