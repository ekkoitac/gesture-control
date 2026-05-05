# Version TODO: v0.2 Cursor Smoothness

## Version Metadata

- Version: `v0.2-cursor-smoothness`
- Active phase: `Phase 0`
- Active task: `V2-01`
- Status: `planned`
- Last updated: `2026-05-05`
- Validation baseline: `.venv/bin/python -m pytest -q`, `.venv/bin/ruff check gesture_control tests`, dry-run smoke check when runtime behavior changes.

## Progress Board

- Current task: `V2-01`
- Blocked tasks: none
- Next task: `V2-02`
- Completed count: `0/6`
- Validation debt: none

## Execution Rules

- Work on one task at a time.
- If the user names a phase or task, that named item is the boundary.
- If no task is named, choose the first unchecked task in the current phase.
- Do not start later phases until current-phase exit criteria are met.
- Do not mark tasks done before implementation, validation, required docs, and evidence are complete.
- Keep existing activation, pause, tracking-loss, pinch, wave, and shortcut safety behavior unchanged unless the task explicitly says otherwise.
- Do not update architecture behavior docs to describe relative cursor control until the runtime behavior is implemented and validated.
- If a task grows beyond its size tag, mark it `split-required` and split it before continuing.

## Task Size Tags

- `[S]`: single focused edit, no subagent.
- `[M]`: moderate task, main agent by default; subagent only for parallel read-only investigation.
- `[L]`: complex task, subagent eligible only with non-overlapping ownership and a clear deliverable.
- `[XL]`: split into smaller TODOs first unless explicitly approved.

## Phase Gates

### Phase 0: Version Setup

- Goal: Open a focused version for improving index-finger mouse-control smoothness.
- Entry criteria: v0.1 prototype is complete and cursor smoothness is selected as the next active version focus.
- Exit criteria: Active version routing and metadata point to v0.2 without claiming relative cursor control is already implemented.
- Validation required before moving on: Re-read changed docs and confirm no stale active-version reference remains.

### Phase 1: Relative Cursor Control

- Goal: Make index-finger mouse control feel smoother and more responsive by changing cursor movement from absolute screen positioning to relative movement.
- Entry criteria: Phase 0 is done.
- Exit criteria: Relative cursor contract, gesture smoothing/filtering, and macOS emission are implemented with deterministic tests.
- Validation required before moving on: Run `.venv/bin/python -m pytest -q` and record evidence for changed cursor behavior.

### Phase 2: Validation And Docs

- Goal: Verify the cursor feel improvement and keep human/agent docs aligned with runtime behavior.
- Entry criteria: Phase 1 is done or explicitly blocked with documented validation debt.
- Exit criteria: Automated checks, dry-run smoke validation, and docs sync are complete.
- Validation required before completion: Run unit tests, ruff, dry-run smoke validation, and record any remaining manual OS-mode follow-up.

## Task Records

- [ ] V2-01 [S] Create v0.2 active version baseline
  Status: planned
  Progress: 0%
  Owner: main-agent
  Scope: Point version/docs entrypoints to this TODO, bump project version metadata to `0.2.0`, and document that v0.2 focuses on relative cursor smoothness.
  Non-goals: Do not implement relative cursor runtime behavior; do not update architecture behavior docs to claim relative control exists.
  Read: `doc/version/current.md`, `pyproject.toml`, `README.md`, `doc/README.md`, `AGENTS.md`.
  Files likely touched: `doc/version/current.md`, `pyproject.toml`, `README.md`, `doc/README.md`, `AGENTS.md`, `doc/changelog.md`.
  Acceptance: Agents can identify `v0.2-cursor-smoothness` as the active version and first task, while no runtime docs claim relative cursor control is already implemented.
  Validation: Re-read changed docs and confirm no stale active-version reference remains.
  Evidence: pending.
  Risks: Docs could overstate runtime behavior before implementation exists.
  Blockers: none.
  Follow-ups: Start `V2-02` after version baseline is complete.
  Subagent: no.
  Done criteria: Version metadata updated, docs re-read, evidence recorded, task checked, progress board updated.

- [ ] V2-02 [M] Add relative cursor movement contract
  Status: planned
  Progress: 0%
  Owner: main-agent
  Scope: Extend cursor action payloads and config so cursor movement can be emitted as relative normalized delta instead of absolute screen position.
  Non-goals: Do not implement gesture smoothing or macOS relative emission in this task.
  Read: `gesture_control/contracts.py`, `gesture_control/config.py`, `config/default.yaml`, `gesture_control/action_mapper.py`.
  Files likely touched: `gesture_control/contracts.py`, `gesture_control/config.py`, `config/default.yaml`, `gesture_control/action_mapper.py`, related tests.
  Acceptance: Cursor commands carry enough information for the backend to distinguish relative movement from absolute positioning.
  Validation: Add or update deterministic action/config tests and run `.venv/bin/python -m pytest -q`.
  Evidence: pending.
  Risks: Contract changes could break existing absolute cursor behavior if compatibility is not preserved.
  Blockers: none.
  Follow-ups: Use the contract in `V2-03` and `V2-04`.
  Subagent: no.
  Done criteria: Contract implemented, deterministic tests pass, evidence recorded, task checked, progress board updated.

- [ ] V2-03 [M] Implement adaptive smoothing and jitter filtering
  Status: planned
  Progress: 0%
  Owner: main-agent
  Scope: Update `GestureEngine` cursor logic to use relative deltas with adaptive smoothing, jitter floor, max-step clamp, and baseline reset.
  Non-goals: Do not change macOS backend emission; do not alter activation, pinch, wave, shortcut, pause, or tracking-loss priority.
  Read: `gesture_control/gesture_engine.py`, `tests/test_gesture_engine.py`.
  Files likely touched: `gesture_control/gesture_engine.py`, `tests/test_gesture_engine.py`.
  Acceptance: First pointing frame does not jump; tiny still-hand movement is filtered; deliberate slow and fast movement still emits cursor deltas.
  Validation: Add gesture-engine tests for first-frame seed, jitter suppression, larger movement, and reset after pointing loss/no-hand/pause.
  Evidence: pending.
  Risks: Smoothing can create lag or suppress intentional small movement if thresholds are too aggressive.
  Blockers: none.
  Follow-ups: Verify emitted deltas in backend behavior during `V2-04`.
  Subagent: no.
  Done criteria: Gesture logic implemented, tests pass, evidence recorded, task checked, progress board updated.

- [ ] V2-04 [M] Emit relative cursor movement on macOS
  Status: planned
  Progress: 0%
  Owner: main-agent
  Scope: Update `MacOSInputBackend` to apply relative cursor deltas from the current pointer position, with x flipped for user perspective, y direct, and screen bounds preserved.
  Non-goals: Do not retune gesture smoothing; do not change non-cursor OS input behavior.
  Read: `gesture_control/backends/macos.py`, `tests/test_macos_backend.py`.
  Files likely touched: `gesture_control/backends/macos.py`, `tests/test_macos_backend.py`.
  Acceptance: Relative movement moves left/right/up/down in the expected perceived direction and never exits screen bounds.
  Validation: Add backend coordinate tests and run `.venv/bin/python -m pytest -q`.
  Evidence: pending.
  Risks: Direction mapping can regress previously fixed user-perspective x behavior.
  Blockers: none.
  Follow-ups: Run full automated and dry-run validation in `V2-05`.
  Subagent: no.
  Done criteria: Backend emission implemented, tests pass, evidence recorded, task checked, progress board updated.

- [ ] V2-05 [M] Run automated and smoke validation
  Status: planned
  Progress: 0%
  Owner: main-agent
  Scope: Run unit tests, ruff, and dry-run smoke validation after cursor changes.
  Non-goals: Do not implement new cursor behavior in this task unless validation exposes a blocker that must be fixed before completion.
  Read: `doc/agent/todo-execution.md`, `doc/product/manual-acceptance-checklist.md`.
  Files likely touched: validation evidence docs, `doc/iterations/`, active TODO.
  Acceptance: Automated checks pass or any failure is documented as a blocker.
  Validation: Run `.venv/bin/python -m pytest -q`, `.venv/bin/ruff check gesture_control tests`, and `.venv/bin/python -m gesture_control --mode dry-run --no-camera --no-window --no-hotkeys --max-frames 5 --log-level INFO`.
  Evidence: pending.
  Risks: Dry-run may pass while real OS-mode cursor feel still needs manual follow-up.
  Blockers: none.
  Follow-ups: Capture any OS-mode manual validation gap before release docs are finalized.
  Subagent: no.
  Done criteria: Automated and smoke validation evidence recorded, failures tracked as blockers or validation debt, task checked, progress board updated.

- [ ] V2-06 [S] Sync cursor smoothness docs
  Status: planned
  Progress: 0%
  Owner: main-agent
  Scope: Update README, manual acceptance checklist, runtime-flow/module-map docs, changelog, and one iteration record to describe relative cursor control.
  Non-goals: Do not claim manual OS-mode validation passed unless it was actually performed.
  Read: `README.md`, `doc/product/manual-acceptance-checklist.md`, `doc/architecture/runtime-flow.md`, `doc/architecture/module-map.md`, `doc/changelog.md`.
  Files likely touched: `README.md`, `doc/product/manual-acceptance-checklist.md`, `doc/architecture/runtime-flow.md`, `doc/architecture/module-map.md`, `doc/changelog.md`, `doc/iterations/`.
  Acceptance: Docs describe v0.2 cursor behavior, validation steps, and any remaining manual OS-mode follow-up without overstating unverified behavior.
  Validation: Re-read changed docs and confirm completed TODO items include implementation and validation evidence.
  Evidence: pending.
  Risks: Docs may drift from runtime if implementation details change late.
  Blockers: none.
  Follow-ups: Create issue TODO entries for any unresolved cursor-feel gaps.
  Subagent: no.
  Done criteria: Docs synced to verified behavior, evidence recorded, task checked, progress board updated.
