# Versioned TODOs

## Purpose

Version TODOs are execution contracts. They define what an agent should work on, in what order, and when a task can be marked complete.

Use version TODOs to keep agent attention narrow:

- One active version.
- One active phase.
- One active task.
- No later-phase work unless the current boundary is complete.

## Directory Convention

```text
doc/version/
  README.md
  current.md
  examples/
    mvp-todo-example.md
  v0.1-prototype/
    todo.md
    issues-todo.md
```

- `doc/version/current.md` points to the active version and active TODO.
- `doc/version/<version>/todo.md` is the task contract for that version.
- `doc/version/<version>/issues-todo.md` is optional and used to track post-completion unresolved issues or validation gaps.
- `doc/version/examples/` contains format examples only; files there must not be selected as active TODOs.
- `doc/iterations/` remains the historical record of completed work.

## Status Vocabulary

- `planned`: task is not started.
- `active`: task is the current focus.
- `blocked`: task cannot proceed without a decision or dependency.
- `validating`: implementation is done, verification is still running.
- `done`: implementation, validation, and documentation updates are complete.

## Task Size Tags

- `[S]`: single focused edit, no subagent.
- `[M]`: moderate task, usually no subagent unless investigation can run in parallel.
- `[L]`: complex task, subagent eligible if work can be split safely.
- `[XL]`: must be split into smaller TODOs before implementation unless the user explicitly approves a larger execution plan.

## Focus Rules

- If the user names a phase or task, that named item is the boundary.
- If no phase or task is named, choose the first unchecked task in the current active phase.
- Do not execute multiple TODO items in one turn unless the user explicitly asks for a batch.
- Do not mark a task done before validation.
- If a task grows beyond its size tag, update the TODO before continuing.

## Maintenance Rules

- Update the active TODO after each implementation.
- Add an iteration record under `doc/iterations/` for completed feature work.
- Keep `doc/changelog.md` human-readable and result-focused.
- Update architecture docs only when runtime behavior, module boundaries, or interfaces change.
