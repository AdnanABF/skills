---
name: project-local-feature-branches
description: Use when creating local-only feature branches, preserving uncommitted work during branch changes, or isolating new feature commits from an open PR in a single working folder.
---

# Local Feature Branches

## When to Use

- A user wants local feature branches without publishing them to GitHub.
- New feature work must remain separate from an existing PR branch.
- A single-folder workflow is preferred over separate worktrees.

Do not use this skill for deploying, promoting release branches, changing CI, or
merging remote PRs. Those operations need their own authorization and applicable
deployment skills. Merely creating a local branch does not authorize a commit,
push, merge, stash, reset, or remote configuration change.

## Preserve Work When Creating a Branch

1. Identify each actual Git repository; nested apps may have independent histories.
2. Confirm that other editing sessions are paused before changing the active branch
   in their working folder. Single-folder branches are not parallel file isolation.
3. Inspect the current branch, HEAD, staged/unstaged changes, untracked files and
   whether the proposed feature branch already exists. Do not overwrite a branch.
4. Record the status, index diff and content hashes of changed/untracked files.
5. When branching from the current HEAD, use `git switch -c feature/<name>`.
   Existing tracked modifications and untracked files remain in place; no stash,
   copying or commit is normally needed. Do not use forced switching.
6. Verify that HEAD and the original branch ref are unchanged and all local changes
   retain their content and staging state. Report the active branch per repository.

Uncommitted changes live in the working folder, not permanently in a branch.
Creating a feature branch positions future commits there but does not yet save
those changes as feature commits. Before subsequently switching to another branch,
commit the feature work locally or, with authorization, stash it including untracked
files. Otherwise compatible uncommitted changes may follow the next branch switch.

## Keep an Open PR Separate

- Keep unrelated feature commits off the branch that backs the current PR.
- Commit feature work on local-only feature branches; publish none unless requested.
- For a PR fix, first preserve unfinished feature work, then switch to the PR branch
  or create a fresh fix branch from it. Do not merge unrelated feature work into an
  open PR just to deliver a fix.
- After an authorized PR-fix commit, bring that fix into the feature branch when
  requested. A new feature branch already includes all commits present at creation.
- After the PR merges, inspect the updated target and merge method before preparing
  the next PR. A normal merge retains original commits; squash and rebase merges
  create different commit identities. Do not blindly merge or reset branches in a
  way that reintroduces previous work or discards local commits.
- Resolve conflicts deliberately; never discard user edits to obtain a clean tree.
- Git branches isolate source history, not databases, running processes, ports or
  deployment state. Do not run migrations as part of routine branch verification.

## Verification

- Every intended repository is on its named local feature branch.
- Creating the branch leaves the source branch ref and HEAD commit unchanged.
- Modified/untracked file hashes and index state match the pre-switch inventory.
- Existing PR fixes remain ancestors of the feature branch when branching from them.
- No remote branch was created, no push occurred, and no commit was made unless
  separately authorized. State clearly that carried changes are still uncommitted.
