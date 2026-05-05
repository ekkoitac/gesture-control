# Iteration Record: I0 OS-Input Preflight

## Goal

- Continue `I0-04` without performing uncontrolled OS input from the Codex-hosted shell.
- Verify the OS backend can initialize in the compatible Python runtime before user-controlled Terminal validation.

## Commands Run

- `.venv/bin/python --version`
  - Result: `Python 3.12.13`.
- `.venv/bin/python -m gesture_control --help`
  - Result: CLI help rendered successfully.
- `.venv/bin/python -m gesture_control --mode os --no-camera --no-window --no-hotkeys --max-frames 5 --log-level INFO`
  - Result: exited by frame budget; logged `hand_present=False tracker=no-hand`.
- `.venv/bin/python -m gesture_control --mode os --no-camera --no-window --max-frames 5 --log-level INFO`
  - Result: exited by frame budget; logged `hand_present=False tracker=no-hand`.
- `.venv/bin/python -m pytest -q`
  - Result: `14 passed`.
- `.venv/bin/ruff check gesture_control tests`
  - Result: all checks passed.

## Outcome

- OS backend construction works in the current Python 3.12.13 environment.
- Synthetic no-hand mode suppresses emitted actions and exits cleanly by `--max-frames`.
- Hotkey listener startup did not crash in the Codex-hosted preflight.

## Not Validated

- This was not a macOS Terminal-hosted Accessibility permission validation.
- No real cursor, scroll, or shortcut output was emitted to a focused OS surface.
- Pause, exit, and emergency stop were not manually validated while OS emission was active.

## TODO Status

- `I0-04` remains unchecked.
- Active status is now `blocked` until a user-controlled Terminal run grants Accessibility permission and performs the OS-mode manual checklist.
