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
   - For relative cursor mode, seed the first pointing frame as a movement baseline, filter tiny jitter, adapt smoothing for slow versus fast hand motion, clamp oversized normalized steps, and reset the baseline after pointing loss, no-hand, or pause.
   - Compute pinch intent (thumb-index + vertical movement), wave intent (wrist lateral delta), and shortcut gesture intent.
4. Action mapping
   - Build cursor commands with explicit `mode` (`relative` or `absolute`) and normalized `delta`.
   - Apply debounce/cooldown to pinch/wave/shortcut intents.
   - Build semantic `ActionCommand` list for this frame.
5. Execution and feedback
   - Send commands to selected backend (`dry-run` logs or `macOS` emitter).
   - In macOS relative mode, apply normalized cursor deltas from the current pointer position, flip x for user perspective, keep y direction direct, and clamp the result to screen bounds.
   - Absolute cursor mapping remains available for compatibility and still maps camera-normalized x through the user-perspective horizontal flip.
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
