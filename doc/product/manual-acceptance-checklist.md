# Manual Gesture Acceptance Checklist (v0.1)

## Preconditions

- Use the project Python 3.12 virtual environment with dependencies and `config/models/hand_landmarker.task` installed.
- Grant Camera permission to the Python runtime before webcam validation.
- If validating OS emission, grant Accessibility permission to the Python binary.
- Use `--mode dry-run` first, then switch to `--mode os` only after safety checks pass.
- For OS emission, focus a disposable long page or empty text surface, keep the keyboard reachable, and close unsaved work before activating gestures.

## Run Commands

- Dry-run with webcam:
  - `.venv/bin/python -m gesture_control --mode dry-run`
- Dry-run without webcam (smoke only):
  - `.venv/bin/python -m gesture_control --mode dry-run --no-camera --no-window --max-frames 120`
- OS-input mode:
  - `.venv/bin/python -m gesture_control --mode os`
- OS-input preflight without real emission:
  - `.venv/bin/python -m gesture_control --mode os --no-camera --no-window --no-hotkeys --max-frames 5 --log-level INFO`

## Acceptance Steps

1. Camera startup and frame updates
   - Action: start dry-run webcam command.
   - Expect: debug window opens, frames update continuously, no crash.

2. Activation gesture gate
   - Action: face the back of the hand toward the camera and perform a shaka gesture.
   - Expect: overlay state changes `INACTIVE -> ACTIVE` and logs activation event.
   - Action: with either hand, face the palm toward the camera and perform a thumbs-down gesture.
   - Expect: overlay state changes `ACTIVE -> INACTIVE` and logs deactivation event.

3. Inactive suppression
   - Action: while inactive, move hand and perform pinch/wave gestures.
   - Expect: no cursor/scroll/shortcut actions emitted.

4. Cursor movement
   - Action: in active mode, point with the index finger, move it slowly left/right/up/down, then hold still.
   - Pose: a fully straight or slightly bent index finger counts as pointing; relaxed hands, open palms, and non-pointer gestures should not count.
   - Expect: pointer follows smoothly in the same perceived direction as hand movement, with no aggressive jitter while hand is still.
   - Expect: relaxed hands, open palms, and non-pointer gestures do not emit cursor movement.
   - Expect: cursor movement is suppressed while thumb-index pinch is held and on frames where wave scroll or shortcut dispatch fires.

5. Pinch scrolling
   - Action: keep thumb-index pinched and move hand up/down over a long page.
   - Pose: keep middle/ring/pinky folded or relaxed; `ok_sign` is only recognized when all three are fully straight upward from knuckle to fingertip.
   - Expect: scroll direction matches movement; release pinch stops scrolling.

6. Wave wheel gesture
   - Action: keep the palm visible and move the whole hand/wrist left or right across the frame.
   - Pose: palm should face the camera or be only slightly angled; avoid finger-only waving.
   - Expect: wave is suppressed while thumb-index pinch is held.
   - Expect: wheel-style scroll bursts occur with cooldown; normal small motion does not spam.

7. Shortcut dispatch
   - Action: perform configured `thumbs_up` and `ok_sign` gestures.
   - `thumbs_up` pose: back of hand faces the camera, thumb points upward, and the other four fingers are folded.
   - `ok_sign` pose: palm faces the camera, thumb and index finger form a visible circle, middle/ring/pinky stay fully straight upward from knuckle to fingertip.
   - Expect: `ok_sign` dispatch does not also emit pinch scroll in the same gesture.
   - Expect: mapped shortcuts fire once per cooldown and respect activation gate.

8. Pause hotkey
   - Action: press configured pause toggle hotkey.
   - Expect: overlay state becomes `PAUSED`; no actions emit until resumed.

9. Exit hotkey
   - Action: press configured exit hotkey (or `q` in window).
   - Expect: runtime exits cleanly and releases resources.
   - Emergency stop: if OS emission is active and the hotkey path fails, click the debug window and press `q`; if the window is unreachable, interrupt the Terminal process with `Ctrl+C`.

10. No-hand suppression
    - Action: remove hand from camera in active mode.
    - Expect: overlay shows tracking lost/no-hand and output actions stop until hand returns.
