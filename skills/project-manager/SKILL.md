---
name: project-manager
description: Use when analyzing live CoreAxis ERP project health, tasks, deadlines, milestones, dependencies, blockers, or risks, preparing status briefs, or executing explicitly requested project changes subject to the active agent's permissions.
---

# Project Manager

## When to Use

Use for CoreAxis ERP project planning, decision-oriented reports, and authorized
project and task changes.
Read `erp-assistant.md` first: its MCP checks, interactive selection, metadata,
privacy, permissions, agent-mode restrictions, and execution rules apply here.

Do not use this skill for generic application implementation planning. Loading
it is not authorization to create or modify Projects, Tasks, or ERP configuration.
Skills provide instructions, not agent-level tool permission enforcement.

## Project Resolution

Resolve the project before querying its tasks.

1. Inspect metadata before relying on field names or valid values. Fetch
   accessible Projects with enough identifying and analytical fields when
   available: `name`, `project_name`, `status`, `is_active`, `priority`,
   `percent_complete`, `percent_complete_method`, `expected_start_date`,
   `expected_end_date`, `actual_start_date`, `actual_end_date`, `actual_time`,
   and `modified`. Request only fields needed for the user's analysis.
2. For normal analysis, prefer `is_active = Yes` and status other than
   `Cancelled`. Do not silently exclude inactive or cancelled projects when
   explicitly requested.
3. Match supplied references case-insensitively against both `Project.name`
   and `Project.project_name`. Use a unique exact match without confirmation.
4. If missing or ambiguous, use `question` with header `Project`, question
   `Which CoreAxis project should I use?`, and `multiple: false`. Show up to
   five matches, with `Show next 5` and `Show previous 5` when needed.
5. Report `<project_name> (<Project.name>)`. All Task project filters must use
   `{"project": "<Project.name>"}`, never just the display name.

## Task Resolution

Retrieve enough pages to avoid incomplete first-page analysis. Depending on
the request, use these fields when available:

- `name`, `subject`, `project`, `status`, `priority`, `progress`
- `is_group`, `is_milestone`, `parent_task`
- `exp_start_date`, `exp_end_date`, `expected_time`
- `act_start_date`, `act_end_date`, `actual_time`
- `depends_on_tasks`, `description`, `completed_on`, `modified`

Match references against both `Task.name` and `Task.subject`. For missing or
ambiguous references, use `question` with readable subjects and IDs. Use
canonical IDs internally and subjects first in responses, adding IDs for
lookup or disambiguation. Avoid reproducing long descriptions unnecessarily.

## Change Planning and Execution

For proposed changes to projects, tasks, milestones, dependencies, deadlines,
priority, status, progress, ownership, or workflow:

1. Retrieve metadata for field requirements and valid values.
2. Fetch existing targets and relevant dependencies.
3. Validate proposed links, dates, dependencies, and allowed values.
4. Present DocType, canonical ID, current and proposed values, dependencies,
   risks, and material side effects.
5. In Plan or for a proposal-only request, state that nothing was applied. In
   Build or another write-capable agent, execute explicit change requests using
   the ERP Assistant execution rules; no separate workflow or exit phrase is
   required. A mode switch alone does not authorize unrequested changes.

For new Task proposals, resolve the canonical Project ID. If omitted, propose
the current date as the deadline and `High` as priority, clearly labeling both
as unsaved suggestions, not confirmed delivery commitments or authorized values.
For execution, use user-specified values or verified site defaults; if an optional
deadline is omitted, leave it unset rather than inventing a commitment. Ask only
when required information or a material ambiguity remains. Validate the site's
milestone field and value before setting a Task as a milestone. Validate dependency
links for cycles and preserve parent/child creation order. Check for duplicate
tasks within the resolved project before creation or retries. Never bypass agent
restrictions or permissions with Python, database writes, or indirect changes.

## Project Analysis

Use today's date in the ERP site's timezone. If unavailable, use the session
date and state that assumption once. Validate site status semantics; normally
`Open`, `Working`, `Pending Review`, and `Overdue` are incomplete, and only
`Completed` counts as completed. Avoid double-counting group/summary tasks as
executable work.

Classify incomplete executable tasks where applicable:

| Category | Criteria |
|----------|----------|
| Critical | Overdue milestones, overdue Urgent/High tasks, or overdue tasks blocking incomplete work |
| Due today | Expected end date is today |
| In progress | Status is Working |
| Awaiting review | Status is Pending Review |
| Upcoming risk | Incomplete milestone or Urgent/High task due within the next three calendar days |
| Blocked | At least one declared dependency is incomplete |
| Unscheduled | No expected end date |
| Recently completed | Completed today or in the previous seven calendar days, with a completion date |

Rank recommended actions: overdue milestones; overdue Urgent/High tasks;
tasks due today; Pending Review tasks due today or overdue; tasks blocking
incomplete work; upcoming milestones and Urgent/High work; then incomplete
tasks without deadlines. Within each category, rank milestones first, then
`Urgent > High > Medium > Low > unset`, earliest deadline, and lowest progress.
Recommend resolving prerequisites rather than starting blocked work.

Calculate when data permits:

- Task counts and percentages by status, completed versus incomplete executable
  work, and overdue/due-today/blocked/unscheduled/pending-review counts.
- Milestone completion and overdue milestones; average incomplete-work progress.
- Expected versus actual hours and material variance; elapsed project time
  versus reported completion.
- Recent completion momentum and stale Working tasks, labeling staleness as an
  inference rather than proof of inactivity.

Highlight missing deadlines, priorities, estimates, inconsistent status and
progress, completed tasks without completion dates, deadlines outside the
project timeline, and absent or contradictory project dates.

Separate `ERP fact`, `Calculated`, `Inference`, and `Recommendation`. Proposed
actions and deadlines are not saved ERP values.

## Brief Output

For project briefs, daily summaries, status reports, or requests for what
needs attention, use:

```markdown
# Project Manager Brief: <project_name> (<Project.name>)
Date: <date and timezone/assumption>

## Executive Summary
## Project Health
## Must Address Now
## Milestones, Blockers, And Review Queue
## Deadline Gaps
## Progress And Insights
## Recommended Actions
## Data Quality And Assumptions
```

Include status, priority, timeline, completion, schedule health, and workload
metrics in Project Health. For ranked tasks include subject, ID where useful,
status, priority, deadline, progress, and reason. Include momentum, hours
variance, inconsistencies, and trends in Progress And Insights. Note empty
sections briefly; keep the highest-risk work first and actions short and ordered.

## Verification

- Confirm MCP access, active agent permissions, authorized scope, and the resolved
  canonical Project and Task IDs.
- Verify pagination, metadata, status semantics, timezone, and date boundaries.
- Check dependency evidence and calculations, noting missing fields or records.
- Distinguish facts, calculations, inferences, and unapplied recommendations.
- In Plan or report-only work, confirm no ERP records were changed. For authorized
  execution, verify saved values and report created/updated IDs and partial failures.
- Confirm no local application code was changed by this ERP workflow.
