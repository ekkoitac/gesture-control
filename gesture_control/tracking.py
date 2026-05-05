from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from gesture_control.contracts import Point3D, TrackingResult

try:
    import cv2
except Exception:  # pragma: no cover
    cv2 = None


LANDMARK_INDEX = {
    "wrist": 0,
    "thumb_mcp": 2,
    "thumb_ip": 3,
    "thumb_tip": 4,
    "index_mcp": 5,
    "index_pip": 6,
    "index_tip": 8,
    "middle_mcp": 9,
    "middle_pip": 10,
    "middle_tip": 12,
    "ring_mcp": 13,
    "ring_pip": 14,
    "ring_tip": 16,
    "pinky_mcp": 17,
    "pinky_pip": 18,
    "pinky_tip": 20,
}


@dataclass
class HandTracker:
    min_detection_confidence: float = 0.5
    min_tracking_confidence: float = 0.5
    max_num_hands: int = 1
    model_asset_path: str | Path | None = None

    def __post_init__(self) -> None:
        self._available = False
        self._init_error: str | None = None
        self._mp: Any | None = None
        self._hands: Any | None = None
        self._backend: str | None = None
        self._timestamp_ms = 0

        if cv2 is None:
            self._init_error = "opencv-python unavailable"
            return

        try:
            import mediapipe as mp  # type: ignore
        except Exception as exc:  # pragma: no cover - depends on local env
            self._init_error = f"mediapipe unavailable: {exc}"
            return

        self._mp = mp
        if hasattr(mp, "solutions") and hasattr(mp.solutions, "hands"):
            self._init_solutions(mp)
            return

        if hasattr(mp, "tasks") and hasattr(mp.tasks, "vision"):
            self._init_tasks(mp)
            return

        self._init_error = "mediapipe hand tracking API unavailable in current Python/runtime"

    def _init_solutions(self, mp: Any) -> None:
        try:
            self._hands = mp.solutions.hands.Hands(
                static_image_mode=False,
                max_num_hands=self.max_num_hands,
                min_detection_confidence=self.min_detection_confidence,
                min_tracking_confidence=self.min_tracking_confidence,
            )
            self._backend = "solutions"
            self._available = True
        except Exception as exc:  # pragma: no cover - depends on local env
            self._init_error = f"mediapipe Hands init failed: {exc}"
            self._hands = None
            self._available = False

    def _init_tasks(self, mp: Any) -> None:
        if self.model_asset_path is None:
            self._init_error = "mediapipe Tasks model path is not configured"
            return

        model_path = Path(self.model_asset_path).expanduser()
        if not model_path.exists():
            self._init_error = f"mediapipe Tasks model missing: {model_path}"
            return

        try:
            options = mp.tasks.vision.HandLandmarkerOptions(
                base_options=mp.tasks.BaseOptions(model_asset_path=str(model_path)),
                running_mode=mp.tasks.vision.RunningMode.VIDEO,
                num_hands=self.max_num_hands,
                min_hand_detection_confidence=self.min_detection_confidence,
                min_hand_presence_confidence=self.min_detection_confidence,
                min_tracking_confidence=self.min_tracking_confidence,
            )
            self._hands = mp.tasks.vision.HandLandmarker.create_from_options(options)
            self._backend = "tasks"
            self._available = True
        except Exception as exc:  # pragma: no cover - depends on local env/model
            self._init_error = f"mediapipe Tasks HandLandmarker init failed: {exc}"
            self._hands = None
            self._available = False

    @property
    def available(self) -> bool:
        return self._available

    @property
    def init_error(self) -> str | None:
        return self._init_error

    def process(self, frame) -> TrackingResult:
        height, width = frame.shape[:2]

        if not self._available:
            return TrackingResult(
                frame_width=width,
                frame_height=height,
                hand_present=False,
                tracker_status="unavailable",
                error_message=self._init_error,
            )

        if self._backend == "tasks":
            return self._process_tasks(frame, width=width, height=height)
        return self._process_solutions(frame, width=width, height=height)

    def _process_solutions(self, frame, *, width: int, height: int) -> TrackingResult:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self._hands.process(rgb)
        if not result.multi_hand_landmarks:
            return TrackingResult(
                frame_width=width,
                frame_height=height,
                hand_present=False,
                tracker_status="no-hand",
            )

        landmarks_raw = result.multi_hand_landmarks[0]
        handedness = None
        confidence = 0.0
        if result.multi_handedness:
            cls = result.multi_handedness[0].classification[0]
            handedness = cls.label
            confidence = float(cls.score)

        landmarks: dict[str, Point3D] = {}
        for name, index in LANDMARK_INDEX.items():
            lm = landmarks_raw.landmark[index]
            landmarks[name] = Point3D(x=float(lm.x), y=float(lm.y), z=float(lm.z))

        return TrackingResult(
            frame_width=width,
            frame_height=height,
            hand_present=True,
            confidence=confidence,
            handedness=handedness,
            landmarks=landmarks,
            tracker_status="ok",
        )

    def _process_tasks(self, frame, *, width: int, height: int) -> TrackingResult:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = self._mp.Image(image_format=self._mp.ImageFormat.SRGB, data=rgb)
        self._timestamp_ms += 33
        result = self._hands.detect_for_video(image, self._timestamp_ms)
        if not result.hand_landmarks:
            return TrackingResult(
                frame_width=width,
                frame_height=height,
                hand_present=False,
                tracker_status="no-hand",
            )

        landmarks_raw = result.hand_landmarks[0]
        handedness = None
        confidence = 0.0
        if result.handedness and result.handedness[0]:
            category = result.handedness[0][0]
            handedness = getattr(category, "category_name", None)
            confidence = float(getattr(category, "score", 0.0))

        landmarks: dict[str, Point3D] = {}
        for name, index in LANDMARK_INDEX.items():
            lm = landmarks_raw[index]
            landmarks[name] = Point3D(x=float(lm.x), y=float(lm.y), z=float(lm.z))

        return TrackingResult(
            frame_width=width,
            frame_height=height,
            hand_present=True,
            confidence=confidence,
            handedness=handedness,
            landmarks=landmarks,
            tracker_status="ok",
        )

    def close(self) -> None:
        if self._hands is not None:
            self._hands.close()
