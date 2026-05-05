from __future__ import annotations

import logging
from dataclasses import dataclass, field
from threading import Lock

from gesture_control.config import HotkeyConfig

try:
    from pynput import keyboard
except Exception:  # pragma: no cover
    keyboard = None


LOGGER = logging.getLogger(__name__)


@dataclass
class RuntimeControl:
    _paused: bool = False
    _should_exit: bool = False
    _lock: Lock = field(default_factory=Lock)

    def toggle_pause(self) -> None:
        with self._lock:
            self._paused = not self._paused
            LOGGER.info("pause toggled -> %s", self._paused)

    def request_exit(self) -> None:
        with self._lock:
            self._should_exit = True
            LOGGER.info("exit requested")

    @property
    def paused(self) -> bool:
        with self._lock:
            return self._paused

    @property
    def should_exit(self) -> bool:
        with self._lock:
            return self._should_exit


@dataclass
class HotkeyController:
    config: HotkeyConfig
    enabled: bool = True

    def __post_init__(self) -> None:
        self._listener = None
        self.error_message: str | None = None

    def start(self, control: RuntimeControl) -> None:
        if not self.enabled:
            return
        if keyboard is None:
            self.error_message = "pynput keyboard listener unavailable"
            LOGGER.warning(self.error_message)
            return
        try:
            self._listener = keyboard.GlobalHotKeys(
                {
                    self.config.pause_toggle: control.toggle_pause,
                    self.config.exit: control.request_exit,
                }
            )
            self._listener.start()
        except Exception as exc:  # pragma: no cover - depends on OS permission
            self.error_message = f"failed to start hotkeys: {exc}"
            LOGGER.warning(self.error_message)
            self._listener = None

    def stop(self) -> None:
        if self._listener is not None:
            self._listener.stop()
            self._listener = None
