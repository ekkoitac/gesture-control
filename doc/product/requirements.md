# Requirements

## Functional Requirements

- FR-001: The prototype must read live frames from a normal built-in or USB webcam.
- FR-002: The prototype must detect at least one visible hand and expose a visible debug state for hand present, no hand, active, paused, and emitted action.
- FR-003: The prototype must support an activation gesture or activation state before emitting mouse, scroll, or keyboard events.
- FR-004: The prototype must provide a global pause or exit hotkey so the user can stop control even if camera tracking is wrong.
- FR-005: In active mode, index-finger movement must map to mouse pointer movement with smoothing and bounded output.
- FR-006: In active mode, thumb-index pinch with vertical movement must emit system scroll events for the focused page, list, or scrollable surface.
- FR-007: In active mode, deliberate lateral wave movement must emit mouse wheel-style scroll actions.
- FR-008: The prototype must support configurable gesture-to-keyboard-shortcut mappings without code changes.
- FR-009: Losing hand tracking must stop output events until a valid hand and activation state are restored.
- FR-010: The prototype must support a dry-run or debug mode where recognized gestures and mapped actions are visible without sending OS input events.

## Non-Functional Requirements

- NFR-001: Local processing is required; camera frames should not be uploaded to a remote service for MVP behavior.
- NFR-002: macOS is the first supported runtime target, with implementation boundaries that keep later Windows or Linux input backends possible.
- NFR-003: The control loop should favor stability over aggressiveness; smoothing, dead zones, thresholds, and cooldowns should reduce false triggers.
- NFR-004: Safety state must be visible enough for a user to understand whether the system is inactive, active, paused, or tracking-lost.
- NFR-005: MVP implementation should remain small enough for one developer or coding agent to inspect and modify without a separate service layer.
- NFR-006: Runtime failures such as missing camera, permission denial, no hand detected, or unsupported input backend should fail visibly instead of silently emitting input.

## Constraints

- Technical:
  - Use ordinary webcam input for v0.1; do not require depth cameras or wearable devices.
  - Keep OS input emission behind a backend boundary so macOS can be implemented first without hard-coding all future platforms into gesture recognition.
  - Phase 0 is documentation-only; runtime code starts in Phase 1.
- Product:
  - v0.1 is a debuggable prototype, not a menu bar app or polished end-user product.
  - Pinch controls scrolling through system scroll events; literal scrollbar-thumb dragging is out of scope for MVP.
  - Keyboard support means configurable shortcuts, not full text input.
- Timeline:
  - Finish product, technical, and runtime-flow baselines before writing the first runnable harness.
  - Ship the first runnable harness before implementing real OS input actions.
