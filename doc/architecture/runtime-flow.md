# Runtime Flow

## Main Flow

1. Input capture
   - Read frame from configured camera index.
   - If frame capture fails, move to failure handling without emitting actions.
2. Hand tracking
   - Load the configured MediaPipe hand model when using the current Tasks tracker.
   - Run landmark detection and derive normalized hand features.
   - Produce `hand_present` and confidence status for overlay + control logic.
3. Gesture interpretation
   - Evaluate activation gestures and pause state.
   - Back-of-hand shaka activates control; palm-facing thumbs down deactivates control.
   - Compute cursor intent only when an index-finger pointing pose is valid; fully straight and slightly bent index poses are accepted, while relaxed hands and open palms are rejected.
   - Compute pinch intent (thumb-index + vertical movement), wave intent (wrist lateral delta), and shortcut gesture intent.
4. Action mapping
   - Apply smoothing/dead zone/bounds to cursor intent.
   - Apply debounce/cooldown to pinch/wave/shortcut intents.
   - Build semantic `ActionCommand` list for this frame.
5. Execution and feedback
   - Send commands to selected backend (`dry-run` logs or `macOS` emitter).
   - In macOS mode, map camera-normalized cursor x through a user-perspective horizontal flip and keep y direction direct.
   - Render debug overlay: active/paused/tracking-lost, gesture metrics, and last action.
6. Loop control
   - Check global pause/exit hotkeys.
   - Continue to next frame until exit signal.

## Failure Paths

- Recognition failure:
  - Conditions: no hand detected, low confidence, missing tracker model, tracker error, or unsupported tracker runtime.
  - Behavior: emit no actions; set visible state to `tracking-lost` or `no-hand`.
- Execution failure:
  - Conditions: backend unavailable, permission denied, or OS emission error.
  - Behavior: stop OS emission for that frame, log explicit error, remain visible in debug overlay.
- Recovery strategy:
  - Hotkey pause always overrides recognition state.
  - Exit hotkey always terminates loop cleanly.
  - On transient tracking loss, resume actions only after hand presence + activation conditions are re-satisfied.
