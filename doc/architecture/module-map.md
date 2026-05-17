# Module Map

## Modules

- `gesture_control/cli.py` + `gesture_control/app.py`
  - Responsibility: process lifecycle, CLI mode selection, loop timing, graceful shutdown.
- `gesture_control/camera.py`
  - Responsibility: OpenCV device init/read/release and camera index configuration.
- `gesture_control/tracking.py`
  - Responsibility: MediaPipe hand detection and normalized landmark output, including current Tasks model loading and legacy Hands fallback.
- `gesture_control/gesture_engine.py`
  - Responsibility: feature extraction, activation gating, relative index-pointing cursor intent, adaptive cursor smoothing/filtering, state transition logic, and debounce/cooldown calculations.
- `gesture_control/action_mapper.py`
  - Responsibility: transform gesture snapshots into semantic actions (cursor move with explicit mode/delta, scroll, wave wheel, shortcuts).
- `gesture_control/backends/*`
  - Responsibility: emit semantic actions via dry-run logging or macOS input APIs, including backend-specific absolute and relative cursor coordinate mapping.
- `gesture_control/debug_overlay.py`
  - Responsibility: render frame overlays for status, landmarks, active/paused state, and last emitted action.
- `gesture_control/config.py` + `config/default.yaml`
  - Responsibility: config schema + parsing + defaults for tracker model path, cursor mode, thresholds, smoothing, cooldowns, and shortcut bindings.
- `tests/*`
  - Responsibility: non-camera deterministic checks for math, state transitions, config parsing, and action mapping.

## Ownership

- Current owner: main coding agent / repo maintainer.
- Future split suggestion:
  - CV pipeline owner: `camera/` + `tracking/`.
  - Controls owner: `gesture/` + `mapping/` + `backend/`.
  - Docs/verification owner: `tests/` + `doc/`.

## Dependency Rules

- Allowed dependencies:
  - `runtime` can depend on all runtime modules.
  - `mapping` can depend on `gesture` data contracts, not vice versa.
  - `backend` depends only on semantic action contracts from `mapping`.
  - `ui_debug` can read tracker + gesture + action state, but must not emit actions.
- Restricted dependencies:
  - `tracking` must not call OS input APIs.
  - `gesture` must not depend on OpenCV display/window APIs.
  - `tests` should default to dry-run behavior and avoid camera/OS side effects.
