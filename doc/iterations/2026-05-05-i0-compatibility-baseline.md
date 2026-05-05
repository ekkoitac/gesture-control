# Iteration Record: I0 Compatibility Baseline

## Goal

- Complete `I0-01` by establishing a compatible Python runtime and unblocking the tracker from the old `solutions.hands` assumption.
- Complete `I0-02` webcam validation once Camera permission is available from macOS Terminal.

## Changes

- Installed Homebrew Python 3.12 and rebuilt project `.venv` with Python 3.12.13.
- Backed up the previous Python 3.14 virtual environment as `.venv-py314-backup-20260505-142033`.
- Downloaded MediaPipe Tasks hand model to `config/models/hand_landmarker.task`.
- Tightened the MediaPipe dependency to `mediapipe>=0.10.35,<0.11`, matching the verified Tasks API path.
- Added tracker model-path configuration under `tracking.model_asset_path`.
- Updated `HandTracker` to support:
  - legacy `mediapipe.solutions.hands` when available,
  - current `mediapipe.tasks.vision.HandLandmarker` when using the configured `.task` model.
- Synced README, tech stack, module map, runtime flow, known issues, and active version routing docs.

## Validation

- Ran `.venv/bin/python --version` -> `Python 3.12.13`.
- Ran `.venv/bin/pip check` -> no broken requirements found.
- Ran `.venv/bin/python -m gesture_control --help` -> command completed and printed CLI usage.
- Ran `.venv/bin/python -m pytest -q` -> `6 passed`.
- Ran `.venv/bin/ruff check gesture_control tests` -> all checks passed.
- Ran `.venv/bin/python -m gesture_control --mode dry-run --no-camera --no-window --no-hotkeys --max-frames 120 --log-level INFO` -> completed with `tracker=no-hand`, confirming the tracker is no longer `unavailable`.
- Ran `.venv/bin/python -m gesture_control --mode dry-run --max-frames 600 --log-level INFO` from macOS Terminal after Camera permission was granted.
- Real webcam validation result: logs showed `hand_present=False tracker=no-hand`, then `hand_present=True tracker=ok`, then `hand_present=False tracker=no-hand`.
- Observation: debug window opened with real camera frames and was exited cleanly.

## Permission Notes

- Codex-hosted terminal did not appear in macOS Camera settings, so webcam validation was performed from macOS Terminal.
- Real webcam dry-run emitted a `pynput.keyboard.GlobalHotKeys` trust warning; Accessibility permission is still required before validating global pause/exit hotkeys and OS-input mode.

## Open Items

- Run the full manual checklist for `I0-03` from macOS Terminal.
- Grant Accessibility permission to Terminal before validating global hotkeys and OS-input mode.
- Reconcile release docs and close `I0-04` only after `I0-02` and `I0-03` have real-device evidence.
