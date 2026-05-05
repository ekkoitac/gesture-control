# Iteration Record: I0 Manual Gesture Tuning

## Goal

- Address manual dry-run findings from `I0-03` before continuing the acceptance checklist.

## Findings

- Lateral wave did not emit `wave scroll` during normal human motion because the previous detector required a large wrist delta between adjacent frames.
- `thumbs_up` could toggle activation back to inactive because shortcut detection and activation detection both used thumb/finger proximity in the same frame.
- `ok_sign` was too strict because its thumb-index distance threshold was narrower than the configured pinch threshold.

## Changes

- Changed wave detection to use cumulative wrist displacement from an anchor point, then reset the anchor after a wave event.
- Evaluated shortcut gestures before activation handling so a recognized shortcut does not also act as a control gesture.
- Changed `ok_sign` detection to use `gesture.pinch_threshold`.
- Suppressed cursor movement output on frames where pinch scroll, wave scroll, or shortcut dispatch fires.
- Relaxed `thumbs_up` detection to support the intended back-of-hand-facing pose.
- Replaced thumb-middle activation toggle with single-purpose control gestures: back-of-hand shaka activates, and palm-facing thumbs down deactivates from either hand.
- Separated `ok_sign` from pinch scroll: thumb-index contact with middle/ring/pinky fully straight upward dispatches `ok_sign` and does not emit pinch scroll.
- Added `pinch_active` so cursor movement is suppressed for the entire thumb-index pinch hold, not only on frames that emit scroll.
- Suppressed wave scroll while thumb-index pinch is held.
- Updated the manual checklist with pose guidance for wave, `thumbs_up`, and `ok_sign`.

## Validation

- Ran `.venv/bin/python -m pytest -q` -> `14 passed`.
- Ran `.venv/bin/ruff check gesture_control tests` -> all checks passed.

## Open Items

- Re-run `I0-03` dry-run manual acceptance from macOS Terminal.
- Validate Accessibility permission before global hotkey and OS-input checks.
