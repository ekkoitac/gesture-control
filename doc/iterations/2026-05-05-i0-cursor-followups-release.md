# Iteration Record: I0 Cursor Followups And Release Reconciliation

## Goal

- Complete `I0-05`, `I0-06`, and `I0-07` from the v0.1 issue TODO.
- Reduce false cursor movement by requiring an intentional index-finger pointing pose.
- Align macOS cursor direction with user-perceived hand direction.
- Reconcile release docs and known issues after user dry-run and OS manual validation passed.

## Changes

- Added index-pointing detection in `GestureEngine`.
  - Fully straight index-finger poses produce cursor intent.
  - Slightly bent index-finger poses also produce cursor intent.
  - Relaxed hands and open palms do not produce cursor intent.
- Kept existing cursor suppression precedence in `ActionMapper`.
  - Activation events, pinch hold/scroll, wave scroll, shortcut dispatch, inactive state, paused state, and tracking loss still prevent cursor movement.
- Changed macOS cursor emission to convert camera-normalized coordinates through a user-perspective horizontal flip while keeping y direction direct and bounded.
- Updated release docs, architecture docs, manual acceptance checklist, known issues, changelog, and current version status.

## Validation

- Ran `.venv/bin/python -m pytest -q` -> `20 passed`.
- Ran `.venv/bin/ruff check gesture_control tests` -> all checks passed.
- Ran `.venv/bin/python -m gesture_control --mode dry-run --no-camera --no-window --no-hotkeys --max-frames 5 --log-level INFO` -> completed with `tracker=no-hand` and `max_frames reached`.
- Ran `.venv/bin/python -m gesture_control --mode os --no-camera --no-window --no-hotkeys --max-frames 5 --log-level INFO` -> completed with `tracker=no-hand` and `max_frames reached`.

## Manual Validation Note

- User reported dry-run and OS manual validation passed after the implementation.
- `I0-05` manual validation passed.
- `I0-06` OS-mode cursor-direction validation passed.
- `I0-07` release reconciliation was completed after those manual checks passed.

## TODO Changes

- Marked `I0-05` complete.
- Marked `I0-06` complete.
- Marked `I0-07` complete.
- Set `doc/version/current.md` to completed status for the v0.1 issue TODO.
