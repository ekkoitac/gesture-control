# Vision

## Product Goal

- `gesture-control` enables local desktop control through visible hand gestures captured by a normal webcam.
- The v0.1 prototype focuses on proving that hand gestures can safely drive basic computer input:
  - Index-finger movement controls the mouse pointer.
  - Pinch movement controls scrolling in the active page or list.
  - Wave gestures trigger mouse wheel-style scrolling.
  - Hand gestures can trigger configurable keyboard shortcuts.
- The first product shape is a debuggable local prototype, not a polished packaged desktop app.

## Target Users

- Primary users:
  - macOS desktop users who want to experiment with gesture-based mouse, scrolling, and shortcut control.
  - Developers testing a local computer-vision input prototype with visible debug feedback.
- Secondary users:
  - Presenters or demo users who need lightweight no-touch control for simple navigation.
  - Users exploring accessibility-adjacent input workflows, without treating the prototype as a medical or assistive-device replacement.

## MVP Boundaries

- Use a normal built-in or USB webcam as the only required input device.
- Prioritize macOS behavior first while keeping platform boundaries clear enough for later Windows or Linux support.
- Keep processing local to the machine.
- Prefer visible debug state over background convenience: camera feed, hand tracking state, activation state, and emitted action should be inspectable.
- Treat pinch scrolling as system scroll events, not literal dragging of application scrollbar thumbs.

## Non-Goals

- No menu bar app, installer, auto-start service, or packaged desktop distribution in v0.1.
- No complete air keyboard or free-form text entry.
- No dependency on depth cameras, gloves, wearable sensors, or phone camera streaming.
- No multi-user gesture tracking.
- No app-specific automation rules beyond generic mouse, scroll, and keyboard shortcut output.
- No guarantee of production-grade accessibility, reliability, or safety for critical workflows.
