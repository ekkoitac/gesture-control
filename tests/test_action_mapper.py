from __future__ import annotations

from gesture_control.action_mapper import ActionMapper
from gesture_control.contracts import ActionType, CursorControlMode, GestureSnapshot


def test_inactive_only_keeps_state_events() -> None:
    mapper = ActionMapper(shortcut_map={"thumbs_up": ["cmd", "l"]})
    snapshot = GestureSnapshot(
        active=False,
        paused=False,
        tracking_lost=False,
        activation_event="activated",
    )
    commands = mapper.map_actions(snapshot)
    assert len(commands) == 1
    assert commands[0].action_type == ActionType.STATE


def test_active_maps_cursor_when_no_discrete_gesture() -> None:
    mapper = ActionMapper(shortcut_map={"thumbs_up": ["cmd", "l"]})
    snapshot = GestureSnapshot(
        active=True,
        paused=False,
        tracking_lost=False,
        cursor_position=(0.5, 0.5),
        cursor_delta=(0.03, -0.02),
    )
    commands = mapper.map_actions(snapshot)
    types = [item.action_type for item in commands]
    assert ActionType.MOVE_CURSOR in types


def test_active_maps_relative_cursor_payload_without_absolute_position() -> None:
    mapper = ActionMapper(shortcut_map={})
    snapshot = GestureSnapshot(
        active=True,
        paused=False,
        tracking_lost=False,
        cursor_mode=CursorControlMode.RELATIVE,
        cursor_delta=(0.02, -0.01),
    )
    commands = mapper.map_actions(snapshot)
    move = next(item for item in commands if item.action_type == ActionType.MOVE_CURSOR)
    assert move.payload == {
        "mode": "relative",
        "delta": (0.02, -0.01),
    }


def test_active_without_cursor_intent_maps_no_action() -> None:
    mapper = ActionMapper(shortcut_map={})
    snapshot = GestureSnapshot(
        active=True,
        paused=False,
        tracking_lost=False,
    )
    commands = mapper.map_actions(snapshot)
    assert len(commands) == 1
    assert commands[0].action_type == ActionType.NONE


def test_active_suppresses_cursor_during_discrete_gestures() -> None:
    mapper = ActionMapper(shortcut_map={"thumbs_up": ["cmd", "l"]})
    snapshot = GestureSnapshot(
        active=True,
        paused=False,
        tracking_lost=False,
        cursor_position=(0.5, 0.5),
        cursor_delta=(0.03, -0.02),
        pinch_scroll=180.0,
        wave_scroll=-1,
        shortcut_gesture="thumbs_up",
    )
    commands = mapper.map_actions(snapshot)
    types = [item.action_type for item in commands]
    assert ActionType.MOVE_CURSOR not in types
    assert ActionType.SCROLL in types
    assert ActionType.SHORTCUT in types


def test_active_suppresses_cursor_during_pinch_hold() -> None:
    mapper = ActionMapper(shortcut_map={})
    snapshot = GestureSnapshot(
        active=True,
        paused=False,
        tracking_lost=False,
        cursor_position=(0.5, 0.5),
        cursor_delta=(0.03, -0.02),
        pinch_active=True,
        pinch_scroll=0.0,
    )
    commands = mapper.map_actions(snapshot)
    assert all(item.action_type != ActionType.MOVE_CURSOR for item in commands)
