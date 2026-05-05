# TODO Execution Rules

## Required Read Order

1. `AGENTS.md`
2. `doc/version/current.md`
3. Active version TODO, currently `doc/version/mvp/todo.md`
4. This file
5. Task-specific docs from `doc/agent/context-index.md`

## Selecting Work

- If the user names a phase or task, use that as the execution boundary.
- If the user does not name a phase or task, select the first unchecked task in the active phase.
- Work on one TODO item only unless the user explicitly asks for a batch.
- If a TODO item is ambiguous, clarify the TODO before implementation.

## Staying Focused

- Do not opportunistically fix nearby issues outside the current TODO.
- Do not start later phases because they look easy.
- Do not mark parent phases complete unless all acceptance criteria are verified.
- If implementation reveals new work, add it as a new TODO instead of silently expanding scope.

## Completion Rules

A TODO item can be checked only when all are true:

- Implementation is complete.
- Validation was run or a clear reason is recorded.
- Required docs were updated.
- Any new risk or follow-up is captured in the TODO, `doc/agent/known-issues.md`, or an iteration record.

## Reporting Back

When finishing a TODO, report:

- Task ID and title.
- Files changed.
- Validation performed.
- TODO status update.
- Remaining next task.

