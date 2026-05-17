from __future__ import annotations

from dataclasses import dataclass

from gesture_control.contracts import ActionCommand, ActionType, CursorControlMode, GestureSnapshot


def _cursor_mode_value(mode: CursorControlMode | str) -> str:
    if isinstance(mode, CursorControlMode):
        return mode.value
    return str(mode)


@dataclass
class ActionMapper:
    shortcut_map: dict[str, list[str]]

    def map_actions(self, snapshot: GestureSnapshot) -> list[ActionCommand]:
        commands: list[ActionCommand] = []

        if snapshot.activation_event:
            commands.append(
                ActionCommand(
                    action_type=ActionType.STATE,
                    payload={"event": snapshot.activation_event},
                    description=f"activation {snapshot.activation_event}",
                )
            )

        if not snapshot.active or snapshot.paused or snapshot.tracking_lost:
            return commands

        suppress_cursor = (
            snapshot.activation_event is not None
            or snapshot.pinch_active
            or snapshot.pinch_scroll != 0.0
            or snapshot.wave_scroll != 0
            or snapshot.shortcut_gesture is not None
        )

        cursor_mode = _cursor_mode_value(snapshot.cursor_mode)
        has_cursor_target = snapshot.cursor_delta and (
            cursor_mode == CursorControlMode.RELATIVE.value or snapshot.cursor_position is not None
        )
        if not suppress_cursor and has_cursor_target:
            dx, dy = snapshot.cursor_delta
            if dx != 0.0 or dy != 0.0:
                payload = {
                    "mode": cursor_mode,
                    "delta": snapshot.cursor_delta,
                }
                if snapshot.cursor_position is not None:
                    payload["position"] = snapshot.cursor_position

                commands.append(
                    ActionCommand(
                        action_type=ActionType.MOVE_CURSOR,
                        payload=payload,
                        description=(
                            f"cursor {cursor_mode} "
                            f"delta({snapshot.cursor_delta[0]:.3f}, {snapshot.cursor_delta[1]:.3f})"
                        ),
                    )
                )

        if snapshot.pinch_scroll != 0.0:
            amount = int(snapshot.pinch_scroll)
            if amount != 0:
                commands.append(
                    ActionCommand(
                        action_type=ActionType.SCROLL,
                        payload={"amount": amount, "source": "pinch"},
                        description=f"pinch scroll {amount}",
                    )
                )

        if snapshot.wave_scroll != 0:
            amount = 120 * snapshot.wave_scroll
            commands.append(
                ActionCommand(
                    action_type=ActionType.SCROLL,
                    payload={"amount": amount, "source": "wave"},
                    description=f"wave scroll {amount}",
                )
            )

        if snapshot.shortcut_gesture:
            keys = self.shortcut_map.get(snapshot.shortcut_gesture)
            if keys:
                commands.append(
                    ActionCommand(
                        action_type=ActionType.SHORTCUT,
                        payload={
                            "gesture": snapshot.shortcut_gesture,
                            "keys": keys,
                        },
                        description=f"shortcut {snapshot.shortcut_gesture} -> {'+'.join(keys)}",
                    )
                )

        if not commands:
            commands.append(
                ActionCommand(
                    action_type=ActionType.NONE,
                    payload={},
                    description="no action",
                )
            )

        return commands
