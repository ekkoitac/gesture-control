# Version TODO: v0.1-prototype

## Active Focus

- Current phase: `Phase 0: Version And Product Baseline`
- Current task: `T0-01`
- Status: `planned`

## Execution Rules

- Work on one task at a time.
- If the user names a phase or task, that named item is the boundary.
- If no task is named, choose the first unchecked task in the current phase.
- Do not start later phases until current-phase acceptance is met.
- Do not write runtime code during Phase 0.
- Mark tasks done only after implementation, validation, and required documentation updates are complete.
- If a task is too broad, split it into smaller TODOs before implementation.
- Files under `doc/version/examples/` are examples only and must not be selected as active tasks.

## Task Size Tags

- `[S]`: single focused edit, no subagent.
- `[M]`: moderate task, usually no subagent unless investigation can run in parallel.
- `[L]`: complex task, subagent eligible if work can be split safely.
- `[XL]`: must be split into smaller TODOs before implementation unless explicitly approved.

## Phase 0: Version And Product Baseline

### Goal

Turn the documentation scaffold into a concrete v0.1 prototype baseline before implementation starts.

### TODO

- [ ] T0-01 [S] Determine product baseline
  Scope: Fill `doc/product/vision.md` and `doc/product/requirements.md` with the first concrete product goals, users, non-goals, MVP boundaries, and safety expectations.
  Read: `README.md`, `doc/product/vision.md`, `doc/product/requirements.md`, `doc/version/current.md`.
  Acceptance: Product intent is specific enough for an agent to avoid inventing scope for webcam input, mouse control, pinch scrolling, wave scrolling, configurable keyboard shortcuts, activation, and hotkey safety.
  Validation: Re-read both product files and confirm goals, users, non-goals, functional requirements, non-functional requirements, and constraints exist.
  Subagent: no.

- [ ] T0-02 [S] Determine technical baseline
  Scope: Fill `doc/architecture/tech-stack.md` with the first implementation stack, local runtime expectations, platform priorities, and validation commands.
  Read: `doc/architecture/tech-stack.md`, `doc/architecture/overview.md`, `doc/product/requirements.md`.
  Acceptance: Future agents know the runtime, framework/library choices, OS-input backend boundary, and commands to use before coding.
  Validation: Confirm commands are either real repo commands or explicitly marked as not available yet.
  Subagent: no.

- [ ] T0-03 [M] Determine first runtime flow
  Scope: Fill `doc/architecture/overview.md`, `doc/architecture/module-map.md`, and `doc/architecture/runtime-flow.md` with the intended gesture-control flow.
  Read: `doc/architecture/*`, `doc/product/requirements.md`, `doc/version/v0.1-prototype/todo.md`.
  Acceptance: Camera input, hand tracking, gesture state, action mapping, OS input execution, debug feedback, and failure handling responsibilities are clearly separated.
  Validation: Confirm each component has a responsibility and the flow has at least one failure path.
  Subagent: read-only exploration eligible.

## Phase 1: First Runnable Harness

### Goal

Create the first runnable harness only after Phase 0 gives agents enough product and architecture context.

### TODO

- [ ] T1-01 [L] Scaffold first runnable project harness
  Scope: Create the minimal executable structure for the chosen stack and wire one observable gesture-control path.
  Read: `doc/version/current.md`, `doc/version/v0.1-prototype/todo.md`, `doc/architecture/tech-stack.md`, `doc/architecture/runtime-flow.md`.
  Acceptance: The project has a documented local run path and one visible or testable behavior.
  Validation: Run the documented command and record the result in a new iteration file.
  Subagent: eligible if file ownership can be split.

- [ ] T1-02 [M] Add first verification path
  Scope: Add the smallest useful test, smoke check, or manual verification script for the runnable harness.
  Read: `doc/architecture/tech-stack.md`, implementation files created in `T1-01`.
  Acceptance: Future agents can verify the harness without guessing.
  Validation: Run the verification path and record output summary in `doc/iterations/`.
  Subagent: no unless verification can run independently while implementation continues.
