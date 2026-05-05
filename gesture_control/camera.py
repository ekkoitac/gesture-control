from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import numpy as np

try:
    import cv2
except Exception:  # pragma: no cover - import availability varies by environment
    cv2 = None


class FrameSource(Protocol):
    width: int
    height: int

    def read(self) -> np.ndarray | None:
        ...

    def release(self) -> None:
        ...


@dataclass
class OpenCVCameraSource:
    camera_index: int
    width: int
    height: int

    def __post_init__(self) -> None:
        if cv2 is None:
            raise RuntimeError("opencv-python is not available")
        self._capture = cv2.VideoCapture(self.camera_index)
        self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        if not self._capture.isOpened():
            raise RuntimeError(f"failed to open camera index {self.camera_index}")

    def read(self) -> np.ndarray | None:
        ok, frame = self._capture.read()
        if not ok:
            return None
        return frame

    def release(self) -> None:
        self._capture.release()


@dataclass
class SyntheticCameraSource:
    width: int
    height: int

    _frame_id: int = 0

    def read(self) -> np.ndarray:
        self._frame_id += 1
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        if cv2 is not None:
            cv2.putText(
                frame,
                f"Synthetic frame {self._frame_id}",
                (24, 48),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (120, 220, 120),
                2,
            )
        return frame

    def release(self) -> None:
        return None
