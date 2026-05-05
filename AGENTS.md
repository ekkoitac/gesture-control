# AGENTS

## Project Snapshot

- Project: `gesture-control`
- Stage: v0.1 prototype issue TODO completed
- Source-of-truth strategy: `spec-strategy.md`

## Progressive Read Order

1. `AGENTS.md`
2. `doc/version/current.md`
3. Active version TODO, currently `doc/version/v0.1-prototype/issues-todo.md`
4. `doc/agent/todo-execution.md`
5. `doc/agent/context-index.md`
6. Task-specific docs in `doc/product/` and `doc/architecture/`
7. `doc/iterations/` for change history

## Working Rules

- Keep human docs as the authoritative source of project facts.
- Keep agent docs as short routing/index context.
- Work on one active TODO item at a time unless the user explicitly asks for a batch.
- Use `doc/agent/subagent-rules.md` before considering subagents.
- After each feature iteration, update:
  - `doc/changelog.md`
  - one file under `doc/iterations/`
  - active version TODO status
  - any changed architecture docs
  - agent context docs if execution constraints changed

## Validation Baseline

- Confirm docs are updated in the same change as feature implementation.
- Do not leave behavior changes undocumented.
- Do not mark TODO items done before validation.
