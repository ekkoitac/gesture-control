# Known Issues

## Active

- No active runtime defect is known after v0.2 automated and dry-run validation.
- Manual macOS OS-mode cursor-feel validation for relative movement remains a follow-up before claiming live hand-feel quality.

## Resolved

- Cursor movement is gated by an explicit index-finger pointing pose.
  - Fix: `GestureEngine` only produces cursor intent when the index finger is fully straight or slightly bent in a pointing pose and the other fingers are not straight open-palm indicators.
  - Evidence: deterministic gesture tests passed, and user dry-run/OS manual validation passed.
- Cursor direction is mapped for user-facing macOS pointer movement.
  - Fix: macOS cursor emission flips camera-normalized x into user-perspective screen x while preserving y direction and bounds.
  - Evidence: deterministic backend tests passed, OS-mode no-camera preflight initialized successfully, and user OS-mode manual cursor-direction validation passed.
- macOS Accessibility permission no longer blocks OS-input validation.
  - Evidence: user-reported OS-mode validation from macOS Terminal completed with overall acceptable behavior; follow-up cursor refinements were completed in `I0-05` and `I0-06`.
- Camera permission no longer blocks real webcam validation when running from macOS Terminal.
  - Fix: run the prototype from macOS Terminal and grant Camera permission there.
  - Evidence: `.venv/bin/python -m gesture_control --mode dry-run --max-frames 600 --log-level INFO` showed `hand_present=True tracker=ok` and then `hand_present=False tracker=no-hand`.
- Python 3.14-era `mediapipe` compatibility issue no longer blocks the v0.1 tracker path.
  - Fix: project `.venv` was rebuilt on Python 3.12.13, and `HandTracker` now supports current MediaPipe Tasks `HandLandmarker` with a local `hand_landmarker.task` model.
  - Evidence: `.venv/bin/python -m gesture_control --mode dry-run --no-camera --no-window --no-hotkeys --max-frames 5` reported `tracker=no-hand`, not `tracker=unavailable`.
