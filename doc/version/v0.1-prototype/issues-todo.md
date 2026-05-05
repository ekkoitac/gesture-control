# Version TODO: v0.1-prototype Issues

## Active Focus

- Current phase: `Completed`
- Current task: `None`
- Status: `done`

## Execution Rules

- Work on one task at a time.
- If the user names a phase or task, that named item is the boundary.
- If no task is named, choose the first unchecked task in the current phase.
- Mark tasks done only after implementation, validation, and required documentation updates are complete.
- Keep this file focused on unresolved issues and validation gaps from the completed prototype.

## Task Size Tags

- `[S]`: single focused edit, no subagent.
- `[M]`: moderate task, usually no subagent unless investigation can run in parallel.
- `[L]`: complex task, subagent eligible if work can be split safely.

## Phase I0: Compatibility And Real-Device Validation

### Goal

Close the known runtime compatibility gap and finish real-device/manual validation that was blocked in Python 3.14.

### TODO

- [x] I0-01 [S] Establish compatible Python runtime baseline (3.11/3.12)
  Scope: Add concrete local setup and verification steps for Python 3.11/3.12 runtime and make it the default recommended validation environment.
  Read: `doc/agent/known-issues.md`, `doc/architecture/tech-stack.md`, `README.md`.
  Acceptance: A new contributor can create a compatible environment and run `gesture_control` without relying on Python 3.14 behavior.
  Validation: Run `python --version` in the new env and run `.venv/bin/python -m gesture_control --help`.
  Result: Completed on Python 3.12.13. Current MediaPipe wheel required Tasks `HandLandmarker` support plus local `config/models/hand_landmarker.task`; smoke path now reports `tracker=no-hand` instead of `tracker=unavailable`.
  Subagent: no.

- [x] I0-02 [M] Validate hand-tracking path on real webcam
  Scope: Run webcam path in compatible runtime and verify hand present/lost transitions and visible landmarks.
  Read: `doc/product/manual-acceptance-checklist.md`, `doc/architecture/runtime-flow.md`, `doc/iterations/2026-05-05-phase1-runnable-harness.md`.
  Acceptance: Tracker status is no longer `unavailable`; hand presence transitions are observed and documented.
  Validation: Run `.venv/bin/python -m gesture_control --mode dry-run` with webcam and record results in a new iteration file.
  Result: Completed from macOS Terminal after granting Camera permission. Webcam opened, real frames rendered, and logs showed `hand_present=False tracker=no-hand`, `hand_present=True tracker=ok`, then `hand_present=False tracker=no-hand`.
  Subagent: no.

- [x] I0-03 [M] Complete dry-run manual acceptance checklist
  Scope: Execute dry-run checklist items for activation, cursor, pinch scroll, wave scroll, shortcut dispatch, pause, exit, and no-hand suppression on real device.
  Read: `doc/product/manual-acceptance-checklist.md`, `doc/product/requirements.md`.
  Acceptance: Every dry-run checklist item has pass/fail evidence and any failures are tracked as follow-up issues.
  Validation: Add one iteration record with step-by-step outcomes and environment details.
  Progress: Manual dry-run surfaced wave, shortcut, cursor-overlap, activation-pose, and OK-vs-pinch ambiguity issues; wave now uses cumulative wrist displacement, `thumbs_up` supports the back-of-hand-facing pose, `ok_sign` requires fully straight middle/ring/pinky fingers, OK suppresses pinch scroll, thumb-index pinch hold suppresses cursor and wave output, and activation now uses back-of-hand shaka activate plus palm-facing thumbs-down deactivate from either hand.
  Result: Completed by user dry-run validation after gesture tuning. Dry-run validation covered camera frames, hand present/lost, shaka activation, palm-facing thumbs-down deactivation, inactive suppression, cursor movement, pinch scroll, wave scroll, shortcut dispatch, pause/exit path, and no-hand suppression.
  Subagent: no.

- [x] I0-04 [M] Validate OS-input mode and Accessibility permission
  Scope: Grant Accessibility permission to the Terminal-hosted Python runtime, then validate OS-emitting cursor, scroll, shortcut, pause, exit, and emergency stop behavior on the real device.
  Read: `doc/product/manual-acceptance-checklist.md`, `doc/agent/known-issues.md`, `doc/architecture/runtime-flow.md`.
  Acceptance: OS mode emits only under activation, cursor/scroll/shortcut actions affect the focused OS surface, pause/exit remain reliable, and any permission/runtime failure is documented as a follow-up issue.
  Validation: Run `.venv/bin/python -m gesture_control --mode os --log-level INFO` from macOS Terminal after Accessibility permission is granted, then record step-by-step pass/fail evidence in `doc/iterations/`.
  Progress: Codex-hosted preflight passed with OS backend initialization, synthetic no-hand suppression, hotkey listener startup, unit tests, and lint. This does not satisfy the Terminal-hosted Accessibility/manual OS-emission requirement.
  Result: Completed by user OS-mode validation from macOS Terminal. Overall OS-input behavior is acceptable; cursor-control refinements found during validation were tracked and completed as `I0-05` and `I0-06`.
  Subagent: no.

- [x] I0-05 [M] Gate cursor movement on index-finger pointing pose
  Scope: Change cursor movement so it is emitted only when the user is intentionally pointing with the index finger. A fully straight index finger and a slightly bent index finger should both count as a valid pointing pose.
  Read: `gesture_control/gesture_engine.py`, `gesture_control/action_mapper.py`, `doc/product/manual-acceptance-checklist.md`, `doc/architecture/runtime-flow.md`.
  Acceptance: In active mode, relaxed hands or non-pointer gestures do not move the cursor; fully straight or slightly bent index-finger pointing does move the cursor; pinch, wave, shortcut, no-hand, inactive, and paused suppression still win over cursor movement.
  Validation: Add deterministic gesture-engine/action-mapper tests for index-pointing gating, then run `.venv/bin/python -m pytest -q`, `.venv/bin/ruff check gesture_control tests`, and a manual dry-run or OS cursor check.
  Result: Completed. Implementation, automated validation, and user manual validation passed. `GestureEngine` now only produces cursor intent when the index-pointing pose is valid, including fully straight and slightly bent index poses; relaxed and open-palm non-pointer poses produce no cursor intent. Existing ActionMapper suppression still blocks cursor movement during activation events, pinch hold/scroll, wave scroll, shortcut dispatch, inactive, paused, and tracking-lost states.
  Subagent: no.

- [x] I0-06 [M] Align cursor direction with hand movement
  Scope: Fix the cursor mapping so the pointer moves in the same perceived direction as the hand movement instead of feeling mirrored.
  Read: `gesture_control/gesture_engine.py`, `gesture_control/action_mapper.py`, `gesture_control/backends/macos.py`, `doc/product/manual-acceptance-checklist.md`.
  Acceptance: After activation, moving the hand left moves the pointer left, moving right moves right, moving up moves up, and moving down moves down on the focused OS surface, while existing smoothing/dead-zone behavior remains intact.
  Validation: Add or update deterministic mapping tests where possible, then run `.venv/bin/python -m pytest -q`, `.venv/bin/ruff check gesture_control tests`, and a manual OS-mode cursor-direction check.
  Result: Completed. Implementation, deterministic validation, and user OS-mode manual cursor-direction validation passed. macOS cursor emission now maps camera-normalized x through a user-perspective horizontal flip while keeping y direction direct.
  Subagent: no.

- [x] I0-07 [S] Reconcile known-issues and release docs
  Scope: After I0-01 ~ I0-06, update `known-issues`, README limitation notes, and version status based on observed results.
  Read: `doc/agent/known-issues.md`, `README.md`, `doc/version/current.md`.
  Acceptance: Docs reflect current truth (resolved vs unresolved) with no stale workaround guidance.
  Validation: Re-read changed docs and ensure each unresolved issue maps to an explicit TODO or known-issue entry.
  Result: Completed after user dry-run and OS manual validation passed for `I0-05` and `I0-06`; release docs and known issues now reflect no active v0.1 prototype issue TODOs.
  Subagent: no.
