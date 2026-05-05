# AGENTS

## Project Snapshot

- Project: `gesture-control`
- Stage: documentation scaffold
- Source-of-truth strategy: `spec-strategy.md`

## Progressive Read Order

1. `AGENTS.md`
2. `doc/agent/context-index.md`
3. Task-specific docs in `doc/product/` and `doc/architecture/`
4. `doc/iterations/` for change history

## Working Rules

- Keep human docs as the authoritative source of project facts.
- Keep agent docs as short routing/index context.
- After each feature iteration, update:
  - `doc/changelog.md`
  - one file under `doc/iterations/`
  - any changed architecture docs
  - agent context docs if execution constraints changed

## Validation Baseline

- Confirm docs are updated in the same change as feature implementation.
- Do not leave behavior changes undocumented.
