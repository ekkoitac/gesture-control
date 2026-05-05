# gesture-control

Local webcam-based gesture control prototype (v0.1).

## Features

- Webcam frame capture with debug overlay.
- Hand-tracking integration boundary with graceful fallback when unavailable.
- Activation gate before control output:
  - back-of-hand shaka activates,
  - palm-facing thumbs down deactivates.
- Gesture actions:
  - index-finger pointing-pose cursor control,
  - thumb-index pinch scrolling,
  - lateral wave wheel scrolling,
  - configurable gesture-to-shortcut mapping.
- Global pause/exit hotkeys and dry-run mode.

## Setup

1. Create a virtual environment:
   - `/opt/homebrew/bin/python3.12 -m venv .venv`
2. Install dependencies:
   - `.venv/bin/pip install -r requirements.txt pytest ruff`
3. Download the MediaPipe Tasks hand model:
   - `mkdir -p config/models`
   - `curl -L https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task -o config/models/hand_landmarker.task`

## Run

- Show CLI help:
  - `.venv/bin/python -m gesture_control --help`
- Dry-run without webcam (smoke path):
  - `.venv/bin/python -m gesture_control --mode dry-run --no-camera --no-window --no-hotkeys --max-frames 120`
- Dry-run with webcam debug window:
  - `.venv/bin/python -m gesture_control --mode dry-run`
- OS-input mode (requires macOS Accessibility permission):
  - `.venv/bin/python -m gesture_control --mode os`

Hotkeys (from `config/default.yaml`):

- Pause/resume: `<ctrl>+<alt>+p`
- Exit: `<ctrl>+<alt>+q`

## Tests

- `.venv/bin/python -m pytest`
- `.venv/bin/ruff check gesture_control tests`

## Docs

- Prototype completion TODO: `/doc/version/v0.1-prototype/todo.md`
- Active issue TODO: `/doc/version/v0.1-prototype/issues-todo.md`
- Architecture: `/doc/architecture/`
- Manual acceptance: `/doc/product/manual-acceptance-checklist.md`

## Validation Notes

- Python 3.12 is the default validation runtime for v0.1.
- Real webcam validation requires macOS camera permission for the Python runtime.
- OS-input mode requires macOS Accessibility permission for the Python runtime.
- Dry-run and OS manual validation passed on the current macOS device after the index-pointing cursor gate and user-perspective cursor direction mapping changes.
