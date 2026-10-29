---
name: erp-assistant
description: Use when inspecting, searching, analyzing, reporting on, or making explicitly requested changes to live CoreAxis ERP records through MCP, subject to the active agent's permissions.
---

# ERP Assistant

## When to Use

Use for work across DocTypes accessible to the authenticated user on
`erp.coreaxissolutions.in`: record lookup, comparisons, business analysis,
reports, proposed changes, and authorized execution. For project health, tasks, milestones, and
deadlines, also read `project-manager.md` for the project-specific workflow.

Do not activate this skill merely because application code uses Frappe. It is
for live ERP operations, not backend implementation or deployment.

## Scope and Safety

- Follow the active agent's permissions. In Plan or any read-only agent, only
  inspect and propose changes; never mutate ERP state, even through a remote tool.
- In Build or another write-capable agent, execute explicitly requested changes
  through supported MCP tools within the user's authorized scope. Analysis-only
  requests remain read-only. A mode switch alone is not a request to change ERP.
- Do not edit application code, run shell commands, browse unrelated websites,
  or delegate ERP inspection. Do not use server-side Python or direct database
  writes as a fallback.
- This skill supplies instructions, not an agent permission sandbox. Loading it
  does not disable tools or change the selected agent's permissions.
- A clear creation or update request supplies authorization for that scoped
  operation in a write-capable agent. Do not demand a special confirmation phrase,
  an exit from this skill, or repeated authorization solely because Plan was used
  earlier. If the active agent is read-only, present an unapplied plan and explain
  that execution requires switching to a write-capable agent.
- Confirm destructive or otherwise high-impact actions with their exact targets
  and material consequences before execution. Resolve missing required inputs or
  ambiguous scope; do not treat skill loading or tool availability as authorization.

## Required Tools

Before querying ERP, check that `erp.coreaxissolutions.in` MCP tools are
available. If unavailable, explain that CoreAxis ERP MCP must be enabled and
connected, then stop ERP work. Do not ask for a DocType or record, inspect local
code, or attempt a fallback. Do not assume a restart is required.

Use the `question` tool whenever a DocType or record selection or missing
required input is needed. Do not substitute a numbered chat menu. If the tool
is unavailable when selection is required, explain the limitation and stop
that workflow rather than guessing.

Use standard MCP tools for search, metadata, documents, analysis, reports,
pending approvals, and dashboards. Inspect each tool's contract for side effects;
only use mutation tools when both agent permissions and the user's request allow
the operation. Never use `run_python_code`, arbitrary scripts, or direct database
writes as an alternative to supported ERP operations. Database queries,
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
effects. Resolve ambiguity with `question`. Clearly mark unapplied plans as such;
do not imply that a proposal or suggested default has been authorized or saved.

For report, dashboard, or chart proposals, validate source DocTypes, reports,
fields, filters, roles, and chart sources. Explain what users would see and
any role or visibility impact. Inspection and proposals remain read-only;
creating, updating, sharing, publishing, or deleting artifacts follows the same
agent-permission and user-authorization rules as other ERP writes.

## Executing Authorized Changes

1. Confirm that the active agent permits writes and the request identifies the
   intended operation and scope. Validate metadata, required fields, canonical
   targets, linked records, allowed values, and relevant workflow transitions.
2. Read current records before updating them. Change only requested fields and
   check for material changes since a prior plan; clarify conflicts rather than
   overwriting unrelated work. For creation, check for existing matching records.
3. Use documented MCP mutation tools and normal ERP validation. If the tool does
   not support the operation, explain the limitation without a code/SQL fallback.
4. For batches, resolve scope and dependencies first, track results per item,
   and stop dependent operations when a prerequisite fails. Do not assume a batch
   is atomic or silently roll back successful items through further mutations.
5. After a timeout or uncertain response, inspect ERP state before retrying.
   Do not blindly repeat creates, submissions, or other non-idempotent actions.
6. Read back affected records or inspect equivalent authoritative results to
   verify persisted values. Report canonical IDs, verified changes, failures,
   skipped items, and uncertain results separately. Never claim full success
   from a request being sent alone.

## Failures and Output

Report tool errors concisely and preserve the last verified state. Do not
broaden filters, switch DocTypes, force operations, or use a more privileged
tool merely to make an operation succeed. Explain unsupported operations
instead of using server-side code as a workaround.

Be concise and operational. Use readable labels and canonical IDs where they
help identify records. Put decisions, risks, validation failures, and required
user actions first. Never claim that a recommendation was saved unless execution
and the persisted result were verified.

## Verification

- Confirm the MCP connection, active agent permissions, and authorized scope.
- In Plan or analysis-only work, confirm that no mutations were performed.
- Verify metadata, canonical IDs, filters, and pagination coverage.
- Check that ambiguity was resolved and permissions and sensitive data were
  respected.
- Label facts, calculations, assumptions, and unapplied proposals accurately.
- For writes, verify persisted results, duplicate prevention, and partial failures.
- Report missing data, failed tools, and incomplete coverage; claim ERP changes
  only when supported by verified results.
