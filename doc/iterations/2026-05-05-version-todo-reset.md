# Iteration Record: Version TODO Reset

## Goal

- Move the scaffold MVP TODO out of the active execution path and create the first real version TODO for the prototype.

## Changes

- Moved the old MVP TODO to `doc/version/examples/mvp-todo-example.md`.
- Added `doc/version/v0.1-prototype/todo.md` as the active execution contract.
- Updated version, agent, and documentation routing to point at `v0.1-prototype`.
- Updated the documentation strategy to include active version directories and non-active examples.

## Affected Areas

- Repository documentation only.

## Validation

- Confirm `doc/version/current.md` points to `doc/version/v0.1-prototype/todo.md`.
- Confirm agent entry documents no longer point to `doc/version/mvp/todo.md` as the active TODO.
- Confirm `doc/version/examples/mvp-todo-example.md` is labeled as an example.
- Confirm the new active TODO includes phases, task IDs, size tags, scope, acceptance, validation, and subagent fields.

## Open Items

- Execute `T0-01` in `doc/version/v0.1-prototype/todo.md` to populate the product baseline.
