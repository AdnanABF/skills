---
name: visual-explainer
description: Use when the user asks to visually explain something, show what happens, visualize a plan or implementation, compare current versus proposed behavior, or create an interactive HTML explanation. Supports planning and existing implementations; not limited to source-code documentation.
---

# Visual Explainer

Turn a topic into a visual explanation that answers **“What happens, why, and what changes?”**

**Primary rule: show the behavior, not a wall of text.** Diagrams are the explanation; paragraphs are supporting material. Do not produce a report with a few decorative arrows.

## 1. Establish mode and scope

Infer from the request when clear. Ask only when ambiguity would materially change the result.

| Mode | Basis | Required distinctions |
| --- | --- | --- |
| Planning | User requirements, constraints, existing architecture where relevant | Proposed, assumed, undecided; alternatives and failure paths |
| Implementation | Actual source/configuration/contracts | Observed behavior versus inference; frontend versus backend support |
| Current → proposed | Current evidence plus the requested design | Unchanged, changed, added, removed; migration/compatibility effects |

This skill also works without a codebase: product ideas, operational workflows, architecture choices, and conceptual explanations are valid inputs. Never invent implementation evidence for a plan.

- Identify audience, central question, and output location from context.
- Read applicable `AGENTS.md` and project instructions before working in a codebase.
- Honor Plan mode and other write restrictions. If writing HTML is prohibited, discuss the visual structure in the conversation and wait for a mode change. This skill does not authorize writes.
- Summarize intended files and changes before editing.
- Default to a clearly named HTML file in the target project's `docs/` directory when authorized and appropriate. Reuse its conventions and the document for the same feature; otherwise prefer `docs/features/<feature-name>.html`. If no `docs/` exists, state that creating it is part of the requested artifact, subject to active write permissions. Do not modify application code merely to explain it.

### Coordination with a planning agent

- This skill remains reusable for plans, implementation explanations, and current/proposed comparisons. It does not require a custom agent or authorize any write by itself.
- When used by `visual-planner`, the agent owns requirements discovery, project selection, recommendations, and decision tracking. This skill owns visual structure, diagrams, self-contained HTML, accessibility, walkthroughs, and artifact validation.
- Reuse the brief, evidence, decisions, assumptions, and open questions already established in the conversation. Do not repeat answered questions; ask only when new ambiguity changes the explanation.
- Discussion-only planning stays in the conversation. Create or update HTML when requested, not automatically after every reply. Summarize the intended path and changes first.
- Choose the target project's documentation folder, not another project's merely because it is writable. Root documentation is for workspace-wide topics. Ask when ownership is unclear.
- Mark observed facts, proposals, assumptions, undecided choices, and explicitly approved decisions separately. Approval does not mean implemented or authorize application changes.
- Keep agent registration and enforced permissions in the agent definition, not in this skill. Follow the active agent's restrictions even when a suggested browser or shell validation step is unavailable; report the limitation and hand off stronger checks if needed.

## 2. Build a small behavioral model

Before designing the page, determine:

1. **Actors:** who clicks, decides, processes, stores, or receives?
2. **Trigger:** what starts the flow?
3. **Path:** what requests, decisions, and state changes follow?
4. **Outcome:** what does the user see and what persists?
5. **Exceptions:** what changes on failure, cancellation, expiry, or denial?

For implementations, inspect focused source files and contracts rather than relying only on old documentation. Check conditions that hide controls, actual defaults, lifetimes, and async updates. Do not claim a backend capability is exposed in the UI unless the UI actually exposes it.

For plans, show enough detail to support a decision without pretending decisions have already been made. Use short, explicit assumption/open-question labels. Separate recommended and alternative designs.

For comparisons, align matching actors and steps so the differences are visible at a glance.

## 3. Choose visuals to fit the explanation

Use only the visual forms that help; do not force every page into the same sections.

| Question | Useful visual |
| --- | --- |
| What happens after this action? | Click-through stages with highlighted actors and state |
| Who calls whom? | Sequence diagram or swimlanes |
| What changes? | Before → action → after; current/proposed side-by-side |
| What can be accessed? | Boundary box, folder tree, permission gates |
| How does state evolve? | Labeled state machine with transition arrows |
| What happens over time? | Timeline with distinct events and expiry windows |
| Which approach should we choose? | Aligned option diagrams plus compact tradeoff matrix |
| What happens on failure? | Decision branch and visible recovery path |
| How will we roll it out? | Phased rollout with dependencies and rollback point |

### Diagram quality

- Label arrows with the action or data that moves, not just generic “next.”
- Show direction, ordering, and branch outcomes unambiguously.
- Use concrete short examples where they help, but no live tokens, personal data, or secrets.
- Separate metadata/control flow from file/data delivery when relevant.
- Show visible results, not just component names.
- Do not confuse request-time refresh with live updates, signed URL expiry with link expiry, or permission revocation with recalling downloaded bytes.
- Use consistent actor placement and visual vocabulary throughout.
- Use labels/icons as well as color for success, denial, proposed changes, and uncertainty.
- Keep the main canvas dominant: short labels, short captions, minimal prose. Move long rationale, API tables, and source references into collapsed details.

## 4. Create the artifact

Read `templates/visual-explanation.html` relative to this skill directory as a starting point. Adapt the layout and diagrams to the topic; it is not a mandatory page structure.

- Produce self-contained HTML with inline CSS and small vanilla JavaScript where needed.
- No CDN dependencies, external fonts, analytics, or runtime network calls by default. Use HTML/CSS or inline SVG for diagrams.
- Use a clear mode/evidence legend near the top: implemented, proposed, assumed, or undecided. Do not label the entire page implemented when only part is verified.
- Include an interactive walkthrough when useful: step buttons, next/restart, updated actor states, and a short outcome caption. Controls must actually change the visual, not merely a text paragraph.
- Keep core diagrams readable without JavaScript. Add a concise `noscript` note if interactive content has a static fallback.
- Simulations must be labeled. Never call production services or modify user data as part of an explanatory demo.
- Support narrow screens, keyboard navigation, visible focus, `aria-pressed`/`aria-live` where appropriate, reduced motion, and printable static diagrams.
- Do not rely on emoji alone for meaning; all important nodes need text labels.
- Escape source/user content inserted into HTML. Prefer `textContent` over `innerHTML` in interactions.
- Keep sources and dates tied to actual evidence. Use the real review date, not a template date. Do not claim proposed workflows are tested implementations.

### Suggested page shape

1. One-line question/title + mode legend.
2. Main visual answering the central question.
3. Two to four supporting visuals for boundaries, state, failures, or alternatives.
4. Collapsed assumptions, technical references, or unresolved decisions.

For a simple question, fewer sections are better. Avoid expanding scope just to fill a template.

## 5. Validate

Check what is feasible with available tools:

- HTML nesting, unique IDs, internal anchors, relative source links, and JavaScript syntax.
- Walkthrough next/restart, all selectable stages, and any branching interactions.
- If browser tooling is available, inspect desktop and mobile rendering, overflow, focus, and console errors. Review print styling when practical.
- Confirm diagram semantics against the evidence/model: transition order, conditions, scope, timing, and claimed results.
- Confirm no secrets or accidental backend/network actions.

Do not claim browser/rendering validation if only structural or simulated DOM tests ran. Do not call a documentation simulation an end-to-end product test.

## 6. Deliver concisely

Lead with the output file link. Mention the important visual features and what was actually validated. Clearly state remaining assumptions or validation limits only when material.

## Example requests

- “Visually explain our planned offline sync.”
- “Show what happens when a guest opens a shared link.”
- “Compare current storage with the proposed migration.”
- “Make an interactive HTML to understand these architecture options.”
- “More diagrams, less text.” → simplify prose and improve diagrams; do not append more explanation.

## Verification

- Verify that diagrams distinguish observed behavior, proposals, and assumptions.
- Open the generated HTML and check diagram readability, interactions, and responsive layout.
- Confirm that the explanation is self-contained and that implementation claims match inspected evidence.
