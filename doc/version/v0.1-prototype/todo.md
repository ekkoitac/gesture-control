# Version TODO: v0.1-prototype

## Active Focus

- Current phase: `Completed`
- Current task: `None`
- Status: `done`

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

Turn the documentation scaffold into a concrete v0.1 prototype baseline before runtime implementation starts.

### TODO

- [x] T0-01 [S] Determine product baseline
  Scope: Fill `doc/product/vision.md` and `doc/product/requirements.md` with the first concrete product goals, users, non-goals, MVP boundaries, and safety expectations.
  Read: `README.md`, `doc/product/vision.md`, `doc/product/requirements.md`, `doc/version/current.md`.
  Acceptance: Product intent is specific enough for an agent to avoid inventing scope for webcam input, mouse control, pinch scrolling, wave scrolling, configurable keyboard shortcuts, activation, and hotkey safety.
  Validation: Re-read both product files and confirm goals, users, non-goals, functional requirements, non-functional requirements, and constraints exist.
  Subagent: no.

- [x] T0-02 [S] Determine technical baseline
  Scope: Fill `doc/architecture/tech-stack.md` with the first implementation stack, local runtime expectations, platform priorities, and validation commands.
  Read: `doc/architecture/tech-stack.md`, `doc/architecture/overview.md`, `doc/product/requirements.md`.
  Acceptance: Future agents know the runtime, framework/library choices, OS-input backend boundary, and commands to use before coding.
  Validation: Confirm commands are either real repo commands or explicitly marked as not available yet.
  Subagent: no.

- [x] T0-03 [M] Determine first runtime flow
  Scope: Fill `doc/architecture/overview.md`, `doc/architecture/module-map.md`, and `doc/architecture/runtime-flow.md` with the intended gesture-control flow.
  Read: `doc/architecture/*`, `doc/product/requirements.md`, `doc/version/v0.1-prototype/todo.md`.
  Acceptance: Camera input, hand tracking, gesture state, action mapping, OS input execution, debug feedback, and failure handling responsibilities are clearly separated.
  Validation: Confirm each component has a responsibility and the flow has at least one failure path.
  Subagent: read-only exploration eligible.

## Phase 1: First Runnable Harness

### Goal

Create a debuggable Python prototype harness with camera input and observable hand-tracking output.

### TODO

- [x] T1-01 [L] Scaffold Python prototype harness
  Scope: Create the minimal executable structure, dependency files, configuration loading, and documented local run command for the v0.1 prototype.
  Read: `doc/version/current.md`, `doc/version/v0.1-prototype/todo.md`, `doc/architecture/tech-stack.md`, `doc/architecture/runtime-flow.md`.
  Acceptance: The project has a documented local run path and a CLI entrypoint that can start in debug or dry-run mode.
  Validation: Run the documented command and record the result in a new iteration file.
  Subagent: eligible if file ownership can be split.

- [x] T1-02 [M] Add webcam debug window
  Scope: Add normal webcam capture, frame display, camera selection configuration, and visible paused or active state in the debug window.
  Read: `doc/architecture/tech-stack.md`, `doc/architecture/runtime-flow.md`, implementation files created in `T1-01`.
  Acceptance: A user can launch the prototype and see live camera frames without emitting OS input events.
  Validation: Run the debug command locally and record whether the camera opens, frames update, and exit works.
  Subagent: no.

- [x] T1-03 [M] Add hand landmark dry-run
  Scope: Add hand tracking output with visible landmarks, confidence/status overlay, and logs for recognized hand presence without controlling the OS.
  Read: `doc/architecture/runtime-flow.md`, implementation files created in `T1-01` and `T1-02`.
  Acceptance: The debug window shows hand landmarks when a hand is visible and clearly reports no-hand state when tracking is lost.
  Validation: Run the dry-run path and record hand-present and hand-lost observations.
  Subagent: no.

## Phase 2: Gesture Control MVP

### Goal

Turn tracked hand input into gated mouse, scrolling, and configurable keyboard actions with safe defaults.

### TODO

- [x] T2-01 [M] Add activation gesture and hotkey safety
  Scope: Add activation gating, global pause or exit hotkeys, no-hand output suppression, and visible active/paused state.
  Read: `doc/product/requirements.md`, `doc/architecture/runtime-flow.md`, `doc/version/v0.1-prototype/todo.md`.
  Acceptance: No mouse, scroll, or keyboard events are emitted unless activation is satisfied; pause/exit works regardless of camera state.
  Validation: Run a manual safety check covering inactive hand, active hand, hotkey pause, hotkey exit, and tracking loss.
  Subagent: no.

- [x] T2-02 [M] Add index-finger cursor control
  Scope: Map index fingertip movement to cursor movement with smoothing, dead zone, screen bounds, and dry-run visualization.
  Read: `doc/product/requirements.md`, `doc/architecture/runtime-flow.md`, implementation files from Phase 1.
  Acceptance: In active mode, the cursor follows the index finger smoothly enough for basic pointing while staying stable when the hand is still.
  Validation: Run a manual cursor check covering center movement, screen-edge behavior, still-hand jitter, and inactive mode.
  Subagent: no.

- [x] T2-03 [M] Add pinch scrolling
  Scope: Detect thumb-index pinch and map vertical pinch movement to system scroll events instead of literal scrollbar dragging.
  Read: `doc/product/requirements.md`, `doc/architecture/runtime-flow.md`, cursor and action-mapping code.
  Acceptance: In active mode, pinch-up and pinch-down gestures scroll the focused page or list, with debounce and no runaway scroll after release.
  Validation: Run a manual scroll check in a long page or list and record direction, sensitivity, release behavior, and inactive behavior.
  Subagent: no.

- [x] T2-04 [M] Add wave wheel gesture
  Scope: Detect lateral wave movement and map it to mouse wheel scroll bursts with thresholding, cooldown, and direction rules.
  Read: `doc/product/requirements.md`, `doc/architecture/runtime-flow.md`, gesture state code.
  Acceptance: Deliberate wave gestures trigger wheel scrolling, while normal cursor movement does not repeatedly trigger wheel events.
  Validation: Run a manual wave check covering left/right movement, cooldown, false positives, and inactive behavior.
  Subagent: no.

- [x] T2-05 [M] Add configurable keyboard shortcuts
  Scope: Add config-driven gesture-to-shortcut mappings for a small set of stable actions, with dry-run logging before OS emission.
  Read: `doc/product/requirements.md`, `doc/architecture/tech-stack.md`, `doc/architecture/runtime-flow.md`.
  Acceptance: Users can change shortcut bindings without code edits, and shortcuts only fire under activation and debounce rules.
  Validation: Run config parsing checks and a manual shortcut check for at least two configured shortcuts.
  Subagent: no.

## Phase 3: Verification And Handoff

### Goal

Make the MVP behavior repeatable to verify and clear enough for the next implementation pass to continue safely.

### TODO

- [x] T3-01 [M] Add automated verification path
  Scope: Add the smallest useful automated tests or smoke checks for gesture math, state transitions, config parsing, and action mapping in dry-run mode.
  Read: `doc/architecture/tech-stack.md`, implementation files created in `T1-01`.
  Acceptance: Future agents can verify core non-camera behavior without guessing or emitting OS input events.
  Validation: Run the documented verification command and record output summary in `doc/iterations/`.
  Subagent: no unless verification can run independently while implementation continues.

- [x] T3-02 [S] Add manual gesture acceptance checklist
  Scope: Document the manual checks for camera startup, activation, cursor movement, pinch scrolling, wave scrolling, shortcut dispatch, pause, exit, and no-hand suppression.
  Read: `doc/product/requirements.md`, `doc/architecture/runtime-flow.md`, latest implementation iteration records.
  Acceptance: A new agent or user can validate the MVP behavior without inventing test scenarios.
  Validation: Re-read the checklist and confirm every MVP gesture and safety path has an acceptance step.
  Subagent: no.

- [x] T3-03 [S] Sync release-ready docs
  Scope: Update README, architecture docs, changelog, iteration records, and active TODO status to match the verified prototype.
  Read: `AGENTS.md`, `doc/version/current.md`, `doc/version/v0.1-prototype/todo.md`, `doc/agent/todo-execution.md`.
  Acceptance: Documentation reflects real commands, implemented behavior, known limits, and the next active task.
  Validation: Run documented checks, re-read changed docs, and confirm no completed TODO lacks validation evidence.
  Subagent: no.
