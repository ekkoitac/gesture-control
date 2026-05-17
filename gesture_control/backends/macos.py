from __future__ import annotations

from dataclasses import dataclass

from gesture_control.backends.base import InputBackend
from gesture_control.contracts import ActionCommand, ActionType

try:
    from pynput import keyboard, mouse
except Exception:  # pragma: no cover - depends on runtime environment
    keyboard = None
    mouse = None


def _screen_size_fallback() -> tuple[int, int]:
    try:
        import tkinter as tk

        root = tk.Tk()
        root.withdraw()
        width = int(root.winfo_screenwidth())
        height = int(root.winfo_screenheight())
        root.destroy()
        return width, height
    except Exception:
        return 1920, 1080


def _parse_key(value: str):
    if keyboard is None:
        return value
    normalized = value.lower().strip()
    key_map = {
        "cmd": keyboard.Key.cmd,
        "ctrl": keyboard.Key.ctrl,
        "alt": keyboard.Key.alt,
        "shift": keyboard.Key.shift,
        "enter": keyboard.Key.enter,
        "esc": keyboard.Key.esc,
        "space": keyboard.Key.space,
        "tab": keyboard.Key.tab,
    }
    if normalized in key_map:
        return key_map[normalized]
    if len(normalized) == 1:
        return normalized
    return normalized


def _normalized_to_screen_position(
    position: tuple[float, float],
    *,
    screen_width: int,
    screen_height: int,
) -> tuple[int, int]:
    nx = max(0.0, min(1.0, float(position[0])))
    ny = max(0.0, min(1.0, float(position[1])))
    x = int((1.0 - nx) * (screen_width - 1))
    y = int(ny * (screen_height - 1))
    return x, y


def _clamp_screen_position(
    x: float,
    y: float,
    *,
    screen_width: int,
    screen_height: int,
) -> tuple[int, int]:
    max_x = screen_width - 1
    max_y = screen_height - 1
    return (
        int(max(0, min(max_x, round(x)))),
        int(max(0, min(max_y, round(y)))),
    )


def _relative_normalized_delta_to_screen_position(
    delta: tuple[float, float],
    *,
    current_position: tuple[int, int],
    screen_width: int,
    screen_height: int,
) -> tuple[int, int]:
    dx = -float(delta[0]) * (screen_width - 1)
    dy = float(delta[1]) * (screen_height - 1)
    return _clamp_screen_position(
        current_position[0] + dx,
        current_position[1] + dy,
        screen_width=screen_width,
        screen_height=screen_height,
    )


@dataclass
class MacOSInputBackend(InputBackend):
    screen_width: int = 1920
    screen_height: int = 1080

    def __post_init__(self) -> None:
        if keyboard is None or mouse is None:
            raise RuntimeError("pynput is not available; cannot emit OS input")
        self._mouse = mouse.Controller()
        self._keyboard = keyboard.Controller()
        self.screen_width, self.screen_height = _screen_size_fallback()

    def emit(self, command: ActionCommand) -> None:
        if command.action_type == ActionType.MOVE_CURSOR:
            mode = str(command.payload.get("mode", "absolute"))
            if mode == "relative":
                delta = command.payload.get("delta")
                if not delta:
                    return
                self._mouse.position = _relative_normalized_delta_to_screen_position(
                    delta,
                    current_position=self._mouse.position,
                    screen_width=self.screen_width,
                    screen_height=self.screen_height,
                )
                return

            position = command.payload.get("position")
            if not position:
                return
            self._mouse.position = _normalized_to_screen_position(
                position,
                screen_width=self.screen_width,
                screen_height=self.screen_height,
            )
            return

        if command.action_type == ActionType.SCROLL:
            amount = int(command.payload.get("amount", 0))
            if amount == 0:
                return
            steps = amount // 120
            if steps == 0:
                steps = 1 if amount > 0 else -1
            self._mouse.scroll(0, steps)
            return

        if command.action_type == ActionType.SHORTCUT:
            keys = command.payload.get("keys", [])
            parsed_keys = [_parse_key(value) for value in keys]
            for item in parsed_keys:
                self._keyboard.press(item)
            for item in reversed(parsed_keys):
                self._keyboard.release(item)

    def close(self) -> None:
        return None
