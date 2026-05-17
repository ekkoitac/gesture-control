# Version TODO: v0.2 Cursor Smoothness

## Version Metadata

- Version: `v0.2-cursor-smoothness`
- Active phase: `Completed`
- Active task: `None`
- Status: `done`
- Last updated: `2026-05-05`
- Validation baseline: `.venv/bin/python -m pytest -q`, `.venv/bin/ruff check gesture_control tests`, dry-run smoke check when runtime behavior changes.

## Progress Board

- Current task: `None`
- Blocked tasks: none
- Next task: `Manual macOS OS-mode cursor-feel validation`
- Completed count: `6/6`
- Validation debt: Manual OS-mode cursor-feel validation remains a follow-up; required automated checks and no-camera dry-run smoke validation passed.

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
- Validation result: Completed. Active version routing and metadata point to v0.2; runtime docs were only updated after implementation and validation.

### Phase 1: Relative Cursor Control

- Goal: Make index-finger mouse control feel smoother and more responsive by changing cursor movement from absolute screen positioning to relative movement.
- Entry criteria: Phase 0 is done.
- Exit criteria: Relative cursor contract, gesture smoothing/filtering, and macOS emission are implemented with deterministic tests.
- Validation result: Completed. Deterministic contract, gesture-engine, config, action-mapper, and macOS backend tests passed.

### Phase 2: Validation And Docs

- Goal: Verify the cursor feel improvement and keep human/agent docs aligned with runtime behavior.
- Entry criteria: Phase 1 is done or explicitly blocked with documented validation debt.
- Exit criteria: Automated checks, dry-run smoke validation, and docs sync are complete.
- Validation result: Completed for automated checks and dry-run smoke. Manual macOS OS-mode cursor-feel validation remains a documented follow-up.

## Task Records

- [x] V2-01 [S] Create v0.2 active version baseline
  Status: done
  Progress: 100%
  Owner: main-agent
  Scope: Point version/docs entrypoints to this TODO, bump project version metadata to `0.2.0`, and document that v0.2 focuses on relative cursor smoothness.
  Non-goals: Do not implement relative cursor runtime behavior; do not update architecture behavior docs to claim relative control exists before implementation.
  Read: `doc/version/current.md`, `pyproject.toml`, `README.md`, `doc/README.md`, `AGENTS.md`.
  Files touched: `doc/version/current.md`, `pyproject.toml`, `README.md`, `doc/README.md`, `AGENTS.md`, `doc/changelog.md`.
  Acceptance: Agents can identify `v0.2-cursor-smoothness` as the active version while no runtime docs claimed relative cursor control before implementation existed.
  Validation: Re-read changed docs and confirm stale v0.1 package/status references were removed from active entrypoints.
  Evidence: `pyproject.toml` is `0.2.0`; `AGENTS.md`, `doc/README.md`, and `doc/version/current.md` point at v0.2 completion; final doc scan found no stale package-version or planned-stage active-entry text.
  Risks: Runtime docs could overstate behavior before implementation exists; mitigated by updating behavior docs only after V2-02 to V2-05 validation.
  Blockers: none.
  Follow-ups: none.
  Subagent: no.
  Done criteria: Version metadata updated, docs re-read, evidence recorded, task checked, progress board updated.

- [x] V2-02 [M] Add relative cursor movement contract
  Status: done
  Progress: 100%
  Owner: main-agent
  Scope: Extend cursor action payloads and config so cursor movement can be emitted as relative normalized delta instead of absolute screen position.
  Non-goals: Do not implement gesture smoothing or macOS relative emission in this task.
  Read: `gesture_control/contracts.py`, `gesture_control/config.py`, `config/default.yaml`, `gesture_control/action_mapper.py`.
  Files touched: `gesture_control/contracts.py`, `gesture_control/config.py`, `config/default.yaml`, `gesture_control/action_mapper.py`, `tests/test_action_mapper.py`, `tests/test_config.py`.
  Acceptance: Cursor commands carry enough information for the backend to distinguish relative movement from absolute positioning.
  Validation: Deterministic action/config tests pass in `.venv/bin/python -m pytest -q`.
  Evidence: Added `CursorControlMode`, `GestureConfig.cursor_mode`, relative cursor config defaults, and action payload `mode`/`delta`; `.venv/bin/python -m pytest -q` passed with `26 passed`.
  Risks: Contract changes could break existing absolute cursor behavior; mitigated by keeping `absolute` mode and backend fallback when payload mode is missing.
  Blockers: none.
  Follow-ups: none.
  Subagent: no.
  Done criteria: Contract implemented, deterministic tests pass, evidence recorded, task checked, progress board updated.

- [x] V2-03 [M] Implement adaptive smoothing and jitter filtering
  Status: done
  Progress: 100%
  Owner: main-agent
  Scope: Update `GestureEngine` cursor logic to use relative deltas with adaptive smoothing, jitter floor, max-step clamp, and baseline reset.
  Non-goals: Do not change macOS backend emission; do not alter activation, pinch, wave, shortcut, pause, or tracking-loss priority.
  Read: `gesture_control/gesture_engine.py`, `tests/test_gesture_engine.py`.
  Files touched: `gesture_control/gesture_engine.py`, `tests/test_gesture_engine.py`.
  Acceptance: First pointing frame does not jump; tiny still-hand movement is filtered; deliberate slow and fast movement still emits cursor deltas.
  Validation: Gesture-engine tests cover first-frame seed, jitter suppression, larger movement, max-step clamp, and reset after pointing loss/no-hand/pause.
  Evidence: Added relative cursor baseline state, adaptive alpha, jitter floor, max-step clamp, and reset paths; `.venv/bin/python -m pytest -q` passed with `26 passed`.
  Risks: Smoothing can create lag or suppress intentional small movement if thresholds are too aggressive; config values are explicit and documented for real-device tuning.
  Blockers: none.
  Follow-ups: Tune cursor thresholds after manual OS-mode feel validation if needed.
  Subagent: no.
  Done criteria: Gesture logic implemented, tests pass, evidence recorded, task checked, progress board updated.

- [x] V2-04 [M] Emit relative cursor movement on macOS
  Status: done
  Progress: 100%
  Owner: main-agent
  Scope: Update `MacOSInputBackend` to apply relative cursor deltas from the current pointer position, with x flipped for user perspective, y direct, and screen bounds preserved.
  Non-goals: Do not retune gesture smoothing; do not change non-cursor OS input behavior.
  Read: `gesture_control/backends/macos.py`, `tests/test_macos_backend.py`.
  Files touched: `gesture_control/backends/macos.py`, `tests/test_macos_backend.py`.
  Acceptance: Relative movement moves left/right/up/down in the expected perceived direction and never exits screen bounds.
  Validation: Backend coordinate tests pass in `.venv/bin/python -m pytest -q`.
  Evidence: Added relative normalized-delta mapping from current pointer position with x flip, direct y, and bounds clamp; `.venv/bin/python -m pytest -q` passed with `26 passed`.
  Risks: Direction mapping can regress previously fixed user-perspective x behavior; deterministic tests cover absolute and relative x flip behavior.
  Blockers: none.
  Follow-ups: Manual OS-mode feel validation on macOS remains pending.
  Subagent: no.
  Done criteria: Backend emission implemented, tests pass, evidence recorded, task checked, progress board updated.

- [x] V2-05 [M] Run automated and smoke validation
  Status: done
  Progress: 100%
  Owner: main-agent
  Scope: Run unit tests, ruff, and dry-run smoke validation after cursor changes.
  Non-goals: Do not implement new cursor behavior in this task unless validation exposes a blocker that must be fixed before completion.
  Read: `doc/agent/todo-execution.md`, `doc/product/manual-acceptance-checklist.md`.
  Files touched: `doc/iterations/2026-05-05-v0.2-cursor-smoothness-implementation.md`, `doc/version/v0.2-cursor-smoothness/todo.md`.
  Acceptance: Automated checks pass or any failure is documented as a blocker.
  Validation: Run `.venv/bin/python -m pytest -q`, `.venv/bin/ruff check gesture_control tests`, and `.venv/bin/python -m gesture_control --mode dry-run --no-camera --no-window --no-hotkeys --max-frames 5 --log-level INFO`.
  Evidence: `.venv/bin/python -m pytest -q` -> `26 passed`; `.venv/bin/ruff check gesture_control tests` -> `All checks passed!`; dry-run smoke initialized, logged `hand_present=False tracker=no-hand`, and exited with `max_frames reached: 5`.
  Risks: Dry-run can pass while real OS-mode cursor feel still needs manual follow-up.
  Blockers: none.
  Follow-ups: Run manual macOS OS-mode cursor-feel validation before claiming live hand-feel quality.
  Subagent: no.
  Done criteria: Automated and smoke validation evidence recorded, failures tracked as blockers or validation debt, task checked, progress board updated.

- [x] V2-06 [S] Sync cursor smoothness docs
  Status: done
  Progress: 100%
  Owner: main-agent
  Scope: Update README, manual acceptance checklist, runtime-flow/module-map docs, changelog, and one iteration record to describe relative cursor control.
  Non-goals: Do not claim manual OS-mode validation passed unless it was actually performed.
  Read: `README.md`, `doc/product/manual-acceptance-checklist.md`, `doc/architecture/runtime-flow.md`, `doc/architecture/module-map.md`, `doc/changelog.md`.
  Files touched: `README.md`, `doc/README.md`, `doc/product/roadmap.md`, `doc/product/requirements.md`, `doc/product/manual-acceptance-checklist.md`, `doc/architecture/overview.md`, `doc/architecture/runtime-flow.md`, `doc/architecture/module-map.md`, `doc/architecture/tech-stack.md`, `doc/agent/known-issues.md`, `doc/changelog.md`, `doc/iterations/2026-05-05-v0.2-cursor-smoothness-implementation.md`, `doc/version/current.md`, `doc/version/v0.2-cursor-smoothness/todo.md`.
  Acceptance: Docs describe v0.2 cursor behavior, validation steps, and any remaining manual OS-mode follow-up without overstating unverified behavior.
  Validation: Re-read changed docs and confirm completed TODO items include implementation and validation evidence.
  Evidence: README/manual/architecture docs describe relative cursor control and explicitly state manual OS-mode cursor-feel validation remains pending; this TODO records evidence for all six tasks and has `Completed count: 6/6`.
  Risks: Docs may drift from runtime if implementation details change late; mitigated by syncing docs after validation and recording exact commands.
  Blockers: none.
  Follow-ups: Run real macOS OS-mode cursor-feel validation and tune cursor config if needed.
  Subagent: no.
  Done criteria: Docs synced to verified behavior, evidence recorded, task checked, progress board updated.
