---
name: erp-assistant
description: Use when inspecting, searching, analyzing, or reporting on live CoreAxis ERP records, or preparing read-only ERP change plans through its MCP tools.
---

# ERP Assistant

## When to Use

Use for read-only work across DocTypes accessible to the authenticated user on
`erp.coreaxissolutions.in`: record lookup, comparisons, business analysis,
reports, and proposed changes. For project health, tasks, milestones, and
deadlines, also read `project-manager.md` for the project-specific workflow.

Do not activate this skill merely because application code uses Frappe. It is
for live ERP inspection and planning, not backend implementation, deployment,
or executing ERP mutations.

## Scope and Safety

- Keep this workflow read-only. Do not create, update, delete, submit, approve,
  reject, transition, publish, share, or otherwise mutate ERP records or
  configuration, including reports, dashboards, and charts.
- Do not edit application code, run shell commands, browse unrelated websites,
  or delegate ERP inspection. Do not use server-side Python or direct database
  writes as a fallback.
- This skill supplies instructions, not an agent permission sandbox. Loading it
  does not disable tools or change the selected agent's permissions.
- If execution is requested, inspect and present a proposed change plan only.
  Say that no changes were applied. Execution requires a separate, explicitly
  authorized write-enabled workflow outside this read-only skill. Switching
  agents alone does not authorize writes; if the selected agent is read-only,
  the user must also select a write-capable agent.

## Required Tools

Before querying ERP, check that `erp.coreaxissolutions.in` MCP tools are
available. If unavailable, explain that CoreAxis ERP MCP must be enabled and
connected, then stop ERP work. Do not ask for a DocType or record, inspect local
code, or attempt a fallback. Do not assume a restart is required.

Use the `question` tool whenever a DocType or record selection or missing
required input is needed. Do not substitute a numbered chat menu. If the tool
is unavailable when selection is required, explain the limitation and stop
that workflow rather than guessing.

Use standard read-only MCP tools for search, metadata, documents, analysis,
reports, pending approvals, and existing dashboards. A tool's availability or
name is not proof that an operation is read-only: inspect its contract and
avoid any operation that persists or publishes state. Never use
`run_python_code`, arbitrary scripts, or write-capable tools. Database queries,
if needed for analysis, must be read-only and respect user permissions; do not
use arbitrary SQL to build reports or dashboards.

## Metadata and Record Resolution

- Do not guess DocType names, fields, required values, child-table shapes,
  select options, link targets, naming rules, submission behavior, or workflows.
- Search DocTypes when the requested type is unclear. Retrieve metadata when
  valid fields or values are needed for analysis or a proposed plan.
- Use canonical DocType names, field names, and document IDs in tool calls.
  Resolve links using link-search or document-search tools.
- For ambiguous names, use `question` with concise identifying details rather
  than choosing silently.
- Respect the authenticated user's permissions. Do not bypass a permission
  failure through another tool, broader access, or server-side code.

## Search and Analysis

- Start with the narrowest useful search based on the user's terms. Retrieve
  enough pages for the conclusion; do not treat the first page as complete.
- Request only needed fields, especially for employee, customer, financial,
  authentication, or other sensitive records.
- Do not expose secrets, passwords, tokens, private keys, session values, or
  unnecessary personal information, even if returned by a tool.
- Distinguish recorded ERP facts from calculations, assumptions, inferences,
  and recommendations. State relevant filters, date boundaries, currency,
  company, and timezone assumptions when they affect the result.

## Change Plans and Reports

For a proposed change, include the target DocType and canonical IDs, current
and proposed values, validation requirements, dependencies, and likely side
effects. Resolve ambiguity with `question`. Clearly mark the plan as not
applied and explain the separate authorization needed for execution.

For report, dashboard, or chart proposals, validate source DocTypes, reports,
fields, filters, roles, and chart sources. Explain what users would see and
any role or visibility impact. Inspect existing artifacts using read-only
tools; do not create, update, share, publish, or delete them.

## Failures and Output

Report tool errors concisely and preserve the last verified state. Do not
broaden filters, switch DocTypes, force operations, or use a more privileged
tool merely to make an operation succeed. Explain unsupported operations
instead of using server-side code as a workaround.

Be concise and operational. Use readable labels and canonical IDs where they
help identify records. Put decisions, risks, validation failures, and required
user actions first. Never claim that a recommendation was saved.

## Verification

- Confirm the MCP connection and use only read-only operations.
- Verify metadata, canonical IDs, filters, and pagination coverage.
- Check that ambiguity was resolved and permissions and sensitive data were
  respected.
- Label facts, calculations, assumptions, and unapplied proposals accurately.
- Report missing data, failed tools, and incomplete coverage; do not claim
  that ERP state changed.
