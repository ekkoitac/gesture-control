# Iteration Record: TODO Governance Upgrade

## Goal

- Upgrade version TODOs from checkbox tracking to a stricter execution contract for progress, reliability, and consistency.

## Changes

- Added canonical lifecycle states: `planned`, `active`, `validating`, `done`, `blocked`, `split-required`, and `deferred`.
- Added required progress board fields for current task, blocked tasks, next task, completed count, and validation debt.
- Added required task fields for status, progress, ownership, scope, non-goals, validation, evidence, risks, blockers, follow-ups, subagent use, and done criteria.
- Migrated `doc/version/v0.2-cursor-smoothness/todo.md` to the new structure while preserving task IDs `V2-01` through `V2-06`.
- Updated agent execution and routing docs so tasks cannot be marked done without validation evidence.

## Affected Areas

- Documentation only.
- No runtime code, dependencies, or automation scripts changed.

## Validation

- Confirm lifecycle/status vocabulary appears in TODO governance docs.
- Confirm the example TODO includes metadata, progress board, phase gates, and full task records.
- Confirm the active v0.2 TODO keeps task IDs `V2-01` through `V2-06`.
- Confirm agent routing treats the active TODO as a task board before task-specific docs.

## Open Items

- Apply the new lifecycle fields during the next implementation task, starting with `V2-01`.
