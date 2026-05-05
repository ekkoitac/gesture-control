# Iteration Record: Phase 2 Gesture Control MVP

## Goal

- Complete `T2-01` to `T2-05` by mapping tracked gesture state into gated mouse/scroll/shortcut actions.

## Changes

- Added gesture state engine with activation toggle, safety gates, and cooldowns:
  - `gesture_control/gesture_engine.py`.
- Added semantic action mapping:
  - `gesture_control/action_mapper.py`.
- Added hotkey control and input backend boundaries:
  - `gesture_control/hotkeys.py`, `gesture_control/backends/base.py`, `gesture_control/backends/dry_run.py`, `gesture_control/backends/macos.py`.
- Connected runtime loop to gesture/action path and debug overlay:
  - `gesture_control/app.py`.
- Added default thresholds and shortcut mappings:
  - `config/default.yaml`.

## Affected Areas

- Gesture interpretation and output execution runtime.

## Validation

- Ran `.venv/bin/python -m gesture_control --no-camera --no-window --no-hotkeys --max-frames 5 --mode dry-run`.
  - Result: gated no-hand flow works without emitting OS input actions.
- Ran `.venv/bin/python -m pytest`.
  - Result: gesture math/state and action mapping tests pass.

## Open Items

- Manual webcam interaction checks (cursor/pinch/wave/shortcut on real hand input) should be executed in Python 3.11/3.12 where MediaPipe Hands is available.
