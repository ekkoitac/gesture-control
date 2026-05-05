# Architecture Overview

## System Summary

- `gesture-control` is a local, single-process prototype pipeline:
  1. capture webcam frames,
  2. detect hand landmarks,
  3. convert landmark motion into gesture state,
  4. map gesture state into semantic actions,
  5. emit actions through a selectable backend (`dry-run` or `macOS`),
  6. render debug overlays so safety and behavior are visible.

- Safety is first-class: no output should be emitted unless activation is satisfied and runtime state is active.
- Activation strategy (v0.1): back-of-hand shaka activates; palm-facing thumbs down deactivates; pause and exit are always available via hotkeys.

## Core Components

- Input layer:
  - camera source selection and frame capture.
  - runtime hotkey listener for pause/exit.
- Recognition layer:
  - hand landmark tracking.
  - gesture feature extraction (index-pointing cursor intent, pinch distance, wave displacement).
  - control state machine (inactive, active, paused, tracking-lost).
- Control/execution layer:
  - action mapping with smoothing, thresholds, cooldowns, and debounce.
  - backend adapter for OS events (`dry-run` vs `macOS`), including macOS user-perspective cursor coordinate mapping.
  - debug overlay and logging.

## Key Interfaces

- External interfaces:
  - Webcam device frames (OpenCV capture API).
  - OS input APIs through `pynput` for cursor/scroll/keyboard output.
- Internal contracts:
  - `TrackingResult`: normalized landmarks + confidence + hand presence.
  - `GestureSnapshot`: interpreted gesture signals for one frame.
  - `ActionCommand`: backend-ready semantic action (move, scroll, shortcut, no-op).
  - `InputBackend`: interface for action emission with dry-run and macOS implementations.
