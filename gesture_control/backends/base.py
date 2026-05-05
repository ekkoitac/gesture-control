from __future__ import annotations

from abc import ABC, abstractmethod

from gesture_control.contracts import ActionCommand


class InputBackend(ABC):
    @abstractmethod
    def emit(self, command: ActionCommand) -> None:
        ...

    @abstractmethod
    def close(self) -> None:
        ...
