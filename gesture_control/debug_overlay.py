from __future__ import annotations

from typing import Iterable

from gesture_control.contracts import GestureSnapshot, TrackingResult

try:
    import cv2
except Exception:  # pragma: no cover
    cv2 = None


def _status_color(snapshot: GestureSnapshot) -> tuple[int, int, int]:
    if snapshot.paused:
        return (0, 215, 255)  # yellow
    if snapshot.tracking_lost:
        return (0, 80, 255)  # red-ish
    if snapshot.active:
        return (80, 220, 80)  # green
    return (190, 190, 190)


def _status_text(snapshot: GestureSnapshot) -> str:
    if snapshot.paused:
        return "PAUSED"
    if snapshot.tracking_lost:
        return "TRACKING_LOST"
    if snapshot.active:
        return "ACTIVE"
    return "INACTIVE"


def _iter_overlay_lines(
    mode: str,
    tracking: TrackingResult,
    snapshot: GestureSnapshot,
    last_action: str,
) -> Iterable[str]:
    yield f"mode: {mode}"
    yield f"state: {_status_text(snapshot)}"
    yield f"tracker: {tracking.tracker_status} conf={tracking.confidence:.2f}"
    if snapshot.activation_event:
        yield f"activation: {snapshot.activation_event}"
    yield f"action: {last_action}"

    if "pinch_distance" in snapshot.metrics:
        yield f"pinch_distance: {snapshot.metrics['pinch_distance']:.4f}"
    if "wave_delta_x" in snapshot.metrics:
        yield f"wave_delta_x: {snapshot.metrics['wave_delta_x']:.4f}"
    if "cursor_delta_norm" in snapshot.metrics:
        yield f"cursor_delta_norm: {snapshot.metrics['cursor_delta_norm']:.4f}"
    if tracking.error_message:
        yield f"tracker_error: {tracking.error_message}"


def draw_overlay(
    frame,
    *,
    mode: str,
    tracking: TrackingResult,
    snapshot: GestureSnapshot,
    last_action: str,
) -> None:
    if cv2 is None:
        return

    height, width = frame.shape[:2]
    color = _status_color(snapshot)

    for index, text in enumerate(_iter_overlay_lines(mode, tracking, snapshot, last_action)):
        y = 28 + index * 24
        cv2.putText(
            frame,
            text,
            (14, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color if index <= 1 else (220, 220, 220),
            2,
        )

    for point in tracking.landmarks.values():
        x = int(point.x * width)
        y = int(point.y * height)
        cv2.circle(frame, (x, y), 4, (255, 120, 120), -1)
