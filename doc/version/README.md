# Versioned TODOs

## Purpose

Version TODOs are execution contracts. They define what an agent should work on, how progress is tracked, what evidence is required, and when a task can move forward.

Use version TODOs to keep agent attention narrow:

- One active version.
- One active phase.
- One active task.
- No later-phase work unless the current boundary is complete, blocked, or deferred.
- No `done` state without implementation, validation, documentation updates, and evidence.

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
  v0.2-cursor-smoothness/
    todo.md
```

- `doc/version/current.md` points to the active version and active TODO.
- `doc/version/<version>/todo.md` is the live execution board for that version.
- `doc/version/<version>/issues-todo.md` is optional and used to track post-completion unresolved issues or validation gaps.
- `doc/version/examples/` contains format examples only; files there must not be selected as active TODOs.
- `doc/iterations/` remains the historical evidence record for completed work.

## Canonical Lifecycle

- `planned`: task is defined but not started.
- `active`: task is the current focus and should be the only implementation target.
- `validating`: implementation is complete, but checks or manual validation are still incomplete.
- `done`: implementation, validation, required docs, and evidence summary are complete.
- `blocked`: work cannot proceed without a decision, dependency, permission, environment, or user action.
- `split-required`: task is too broad or touches overlapping subsystems and must be split before implementation.
- `deferred`: task is intentionally postponed, with a reason and next review condition.

Allowed normal flow:

```text
planned -> active -> validating -> done
```

Allowed exception flow:

```text
planned|active|validating -> blocked|split-required|deferred
```

## Task Size Tags

- `[S]`: single focused edit, no subagent.
- `[M]`: moderate task, main agent by default; subagent only for parallel read-only investigation.
- `[L]`: complex task, subagent eligible only with non-overlapping ownership and a clear deliverable.
- `[XL]`: split into smaller TODOs first unless the user explicitly approves a larger execution plan.

## Required Version TODO Sections

Each `doc/version/<version>/todo.md` must contain:

- `Version Metadata`: version, active phase, active task, status, last updated, validation baseline.
- `Progress Board`: current task, blocked tasks, next task, completed count, validation debt.
- `Execution Rules`: one task at a time, no scope expansion, no done state without evidence.
- `Phase Gates`: phase goal, entry criteria, exit criteria, validation required before moving on.
- `Task Records`: each task uses the same required fields.

## Required Task Fields

Each task record must include:

- `Status`
- `Progress`
- `Owner`
- `Scope`
- `Non-goals`
- `Read`
- `Files likely touched`
- `Acceptance`
- `Validation`
- `Evidence`
- `Risks`
- `Blockers`
- `Follow-ups`
- `Subagent`
- `Done criteria`

## Reliability Rules

- `done` requires implementation, validation command/result, documentation update, and evidence summary.
- `blocked` requires blocker reason, owner or decision needed, and next review condition.
- `validating` means implementation is complete but checks or manual validation are not complete.
- `split-required` is mandatory when a task grows beyond `[XL]` or touches overlapping subsystems.
- Validation debt must be recorded in the progress board instead of hidden in prose.
- If validation cannot run, the task cannot be marked `done`; it becomes `blocked` or `validating` with a documented reason.

## Focus Rules

- If the user names a phase or task, that named item is the boundary.
- If no phase or task is named, choose the first unchecked task in the current active phase.
- Do not execute multiple TODO items in one turn unless the user explicitly asks for a batch.
- Do not start the next TODO until the active task reaches `done`, `blocked`, or `deferred`.
- If implementation reveals new work, add it as a follow-up instead of silently expanding scope.

## Maintenance Rules

- Update the active TODO after each implementation.
- Update the progress board whenever task status, validation debt, or blockers change.
- Add an iteration record under `doc/iterations/` for completed feature work or TODO governance changes.
- Keep `doc/changelog.md` human-readable and result-focused.
- Update architecture docs only when runtime behavior, module boundaries, or interfaces change.
