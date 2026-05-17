# Tech Stack

## Languages and Runtime

- Language: Python 3.12 as the default validation runtime; Python 3.11 remains acceptable if the same dependency set is verified locally.
- Runtime: single local CLI process on macOS first, with dry-run fallback on other platforms.

## Platform Priorities

- Primary target: macOS desktop.
- Secondary target: keep recognition and action mapping platform-neutral so Windows/Linux input backends can be added later.
- Runtime assumptions:
  - A built-in or USB webcam is available.
  - Camera permission is granted to the Python runtime.
  - Accessibility permission is granted when OS input emission is enabled.

## Frameworks and Libraries

- Framework: lightweight module-based Python app (no web service layer).
- Core libraries:
  - `opencv-python`: webcam capture and debug window rendering.
  - `mediapipe`: hand landmark tracking via Tasks `HandLandmarker` on current wheels, with legacy `solutions.hands` support kept as a fallback.
  - `numpy`: gesture math and smoothing utilities.
  - `pynput`: mouse/keyboard output and hotkey listening boundary.
  - `PyYAML`: config-driven gesture thresholds and shortcut mappings.

## Tooling

- Build: none for v0.2; local editable install path only.
- Test: `pytest` for non-camera unit tests and dry-run mapping checks.
- Lint/format: `ruff` (lint + format) for fast local checks.

## Architecture Boundaries

- Recognition boundary: camera + hand tracking code must not emit OS input directly.
- Mapping boundary: gesture interpretation produces semantic actions (move cursor, scroll, shortcut) independent of backend.
- OS backend boundary:
  - `DryRunInputBackend`: logs actions only, no OS emission.
  - `MacOSInputBackend`: emits mouse/scroll/shortcut via `pynput`.

## Validation Commands (Phase 0 Baseline)

- `python3 --version`
  - Status: available now.
- `.venv/bin/pip install -r requirements.txt pytest ruff`
  - Status: available now.
- `mkdir -p config/models && curl -L https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task -o config/models/hand_landmarker.task`
  - Status: available now; required for the current MediaPipe Tasks tracker.
- `.venv/bin/python -m gesture_control --help`
  - Status: available now.
- `.venv/bin/python -m gesture_control --no-camera --no-window --no-hotkeys --max-frames 5 --mode dry-run`
  - Status: available now.
- `.venv/bin/python -m pytest`
  - Status: available now.

## Known Runtime Constraints

- The local machine's system `python3` currently defaults to Python 3.14.3; use the project `.venv` built from `/opt/homebrew/bin/python3.12` for validation.
- If `config/models/hand_landmarker.task` is missing, the tracker degrades gracefully to `unavailable` and emits no OS input.
- Full webcam validation requires macOS camera permission for the Python runtime.
