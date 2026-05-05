from __future__ import annotations

import logging
from collections import deque
from dataclasses import dataclass, field

from gesture_control.backends.base import InputBackend
from gesture_control.contracts import ActionCommand, ActionType


LOGGER = logging.getLogger(__name__)


@dataclass
class DryRunInputBackend(InputBackend):
    max_history: int = 100
    history: deque[str] = field(default_factory=lambda: deque(maxlen=100))

    def emit(self, command: ActionCommand) -> None:
        if command.action_type == ActionType.NONE:
            return
        self.history.append(command.description)
        LOGGER.info("[dry-run] %s", command.description)

    def close(self) -> None:
        return None

    def last_action(self) -> str:
        if not self.history:
            return "none"
        return self.history[-1]
