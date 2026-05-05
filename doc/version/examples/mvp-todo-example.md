# Example Version TODO: mvp

This file is a canonical format example only. Do not use it as an active execution contract.

## Version Metadata

- Version: `mvp`
- Active phase: `Phase 0`
- Active task: `T0-01`
- Status: `planned`
- Last updated: `YYYY-MM-DD`
- Validation baseline: `not established`

## Progress Board

- Current task: `T0-01`
- Blocked tasks: none
- Next task: `T0-02`
- Completed count: `0/5`
- Validation debt: none

## Execution Rules

- Work on one task at a time.
- If the user names a phase or task, that named item is the boundary.
- If no task is named, choose the first unchecked task in the current phase.
- Do not start later phases until current-phase exit criteria are met.
- Do not mark tasks done before implementation, validation, required docs, and evidence are complete.
- If a task is too broad, mark it `split-required` and split it into smaller TODOs before implementation.

## Task Size Tags

- `[S]`: single focused edit, no subagent.
- `[M]`: moderate task, main agent by default; subagent only for parallel read-only investigation.
- `[L]`: complex task, subagent eligible only with non-overlapping ownership and a clear deliverable.
- `[XL]`: split into smaller TODOs first unless the user explicitly approves a larger execution plan.

## Phase Gates

### Phase 0: Documentation And Project Baseline

- Goal: Turn the initialized documentation scaffold into a concrete project baseline before implementation starts.
- Entry criteria: Documentation scaffold exists.
- Exit criteria: Product baseline, technical baseline, and runtime flow are specific enough for implementation.
- Validation required before moving on: Re-read changed docs and confirm no required task evidence is missing.

### Phase 1: First Runnable Harness

- Goal: Create the first runnable harness only after Phase 0 gives agents enough product and architecture context.
- Entry criteria: Phase 0 exit criteria are complete.
- Exit criteria: Project has a documented local run path and one visible/testable behavior.
- Validation required before moving on: Run the documented command and record evidence in `doc/iterations/`.

## Task Records

- [ ] T0-01 [S] Populate product baseline
  Status: planned
  Progress: 0%
  Owner: main-agent
  Scope: Fill product docs with concrete goals, users, non-goals, MVP boundaries, and safety expectations.
  Non-goals: Do not choose runtime stack or implement code.
  Read: `README.md`, `doc/product/vision.md`, `doc/product/requirements.md`.
  Files likely touched: `doc/product/vision.md`, `doc/product/requirements.md`.
  Acceptance: Product intent is specific enough for an agent to avoid inventing scope.
  Validation: Re-read changed product docs and confirm goals, users, non-goals, and MVP boundaries exist.
  Evidence: pending.
  Risks: Product scope may still be too broad.
  Blockers: none.
  Follow-ups: none.
  Subagent: no.
  Done criteria: Product docs updated, validation evidence recorded, task checked, progress board updated.

- [ ] T0-02 [S] Choose initial technical baseline
  Status: planned
  Progress: 0%
  Owner: main-agent
  Scope: Fill tech-stack docs with runtime, framework/library choices, local commands, and validation expectations.
  Non-goals: Do not implement the runnable harness.
  Read: `doc/architecture/tech-stack.md`, `doc/architecture/overview.md`.
  Files likely touched: `doc/architecture/tech-stack.md`.
  Acceptance: Future agents know the runtime, framework, and commands before coding.
  Validation: Confirm commands are either real repo commands or explicitly marked as not available yet.
  Evidence: pending.
  Risks: Commands may become stale after scaffold work starts.
  Blockers: none.
  Follow-ups: Refresh commands after the first runnable harness exists.
  Subagent: no.
  Done criteria: Tech baseline documented, validation evidence recorded, task checked, progress board updated.

- [ ] T1-01 [L] Scaffold first runnable project harness
  Status: planned
  Progress: 0%
  Owner: main-agent
  Scope: Create minimal executable structure and wire one observable behavior.
  Non-goals: Do not add unrelated product features or broad refactors.
  Read: `doc/version/current.md`, active TODO, `doc/architecture/tech-stack.md`, `doc/architecture/runtime-flow.md`.
  Files likely touched: implementation entrypoint, package config, README, tests.
  Acceptance: The project has a documented local run path and one visible/testable behavior.
  Validation: Run documented command and record result in a new iteration file.
  Evidence: pending.
  Risks: Task may need to split if implementation touches unrelated subsystems.
  Blockers: none.
  Follow-ups: Add the first verification path.
  Subagent: eligible only for isolated file ownership or parallel read-only verification.
  Done criteria: Harness runs, validation evidence recorded, docs synced, task checked, progress board updated.
