from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ActionType(str, Enum):
    MOVE_CURSOR = "move_cursor"
    SCROLL = "scroll"
    SHORTCUT = "shortcut"
    STATE = "state"
    NONE = "none"


@dataclass(frozen=True)
class Point3D:
    x: float
    y: float
    z: float = 0.0


@dataclass
class TrackingResult:
    frame_width: int
    frame_height: int
    hand_present: bool
    confidence: float = 0.0
    handedness: str | None = None
    landmarks: dict[str, Point3D] = field(default_factory=dict)
    tracker_status: str = "ok"
    error_message: str | None = None

    def get_landmark(self, name: str) -> Point3D | None:
        return self.landmarks.get(name)


@dataclass
class GestureSnapshot:
    active: bool
    paused: bool
    tracking_lost: bool
    cursor_position: tuple[float, float] | None = None
    cursor_delta: tuple[float, float] | None = None
    pinch_active: bool = False
    pinch_scroll: float = 0.0
    wave_scroll: int = 0
    shortcut_gesture: str | None = None
    activation_event: str | None = None
    metrics: dict[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class ActionCommand:
    action_type: ActionType
    payload: dict[str, Any]
    description: str
