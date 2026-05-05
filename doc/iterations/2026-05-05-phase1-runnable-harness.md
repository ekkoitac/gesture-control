# Iteration Record: Phase 1 Runnable Harness

## Goal

- Complete `T1-01`, `T1-02`, and `T1-03` by creating the first runnable prototype harness with debug output.

## Changes

- Added Python project scaffold and dependencies:
  - `pyproject.toml`, `requirements.txt`, `.gitignore`.
- Added runtime and config entrypoints:
  - `gesture_control/__main__.py`, `gesture_control/cli.py`, `gesture_control/app.py`, `gesture_control/config.py`.
- Added camera and tracker runtime modules:
  - `gesture_control/camera.py`, `gesture_control/tracking.py`, `config/default.yaml`.
- Added debug overlay and data contracts:
  - `gesture_control/contracts.py`, `gesture_control/debug_overlay.py`.

## Affected Areas

- Runtime code and setup docs.

## Validation

- Ran `.venv/bin/python -m gesture_control --no-camera --no-window --no-hotkeys --max-frames 5 --mode dry-run`.
  - Result: exit code `0`, loop runs and exits by frame budget.
- Confirmed CLI path and config loading are callable.
- Confirmed debug state text path exists for paused/active/tracking status.

## Open Items

- Live hand landmark rendering could not be fully validated on local Python 3.14 due MediaPipe runtime limitation; tracked in `doc/agent/known-issues.md`.
