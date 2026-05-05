# TODO Execution Rules

## Required Read Order

1. `AGENTS.md`
2. `doc/version/current.md`
3. Active version TODO, currently `doc/version/v0.2-cursor-smoothness/todo.md`
4. This file
5. Task-specific docs from `doc/agent/context-index.md`

## Selecting Work

- If the user names a phase or task, use that as the execution boundary.
- If the user does not name a phase or task, select the first unchecked task in the active phase.
- Work on one TODO item only unless the user explicitly asks for a batch.
- If a TODO item is ambiguous, clarify or update the TODO before implementation.
- Do not start the next TODO until the active task reaches `done`, `blocked`, or `deferred`.

## Task State Management

Before editing code or docs for a task, the agent should be able to identify:

- Current task ID and title.
- Current status.
- Progress percentage.
- Owner.
- Scope and non-goals.
- Required reads.
- Expected files likely touched.
- Acceptance criteria.
- Validation commands or manual checks.
- Known risks, blockers, and follow-ups.
- Subagent eligibility.
- Done criteria.

If these fields are missing, update the TODO structure first.

## Lifecycle Rules

- Move a task to `active` when implementation starts.
- Move a task to `validating` when implementation is complete but checks are still running or manual validation is pending.
- Move a task to `done` only after implementation, validation, documentation, and evidence are complete.
- Move a task to `blocked` when progress needs a decision, dependency, permission, environment, or user action.
- Move a task to `split-required` when the task is too broad or touches overlapping subsystems.
- Move a task to `deferred` only with a reason and next review condition.

## Staying Focused

- Do not opportunistically fix nearby issues outside the current TODO.
- Do not start later phases because they look easy.
- Do not mark parent phases complete unless all phase exit criteria are verified.
- If implementation reveals new work, add it under `Follow-ups` or as a new TODO item.
- If validation debt appears, record it in the active TODO progress board.

## Completion Rules

A TODO item can be checked only when all are true:

- `Status: done`.
- `Progress: 100%`.
- Implementation is complete.
- Validation was run and summarized, or the task is not marked done.
- Required docs were updated.
- Evidence includes command results, manual validation notes, or a direct reason why a check is not applicable.
- Any risk or follow-up is captured in the task, `doc/agent/known-issues.md`, or an iteration record.

If validation cannot run, keep the task unchecked and use `Status: blocked` or `Status: validating`.

## Progress Board Updates

When task state changes, update the active version TODO progress board:

- Current task.
- Blocked tasks.
- Next task.
- Completed count.
- Validation debt.

Do not hide validation debt in prose-only notes.

## Reporting Back

When finishing a TODO turn, report:

- Task ID and title.
- Final status.
- Files changed.
- Validation performed.
- Evidence summary.
- TODO status update.
- Remaining next task.
