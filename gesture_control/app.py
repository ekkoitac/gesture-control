from __future__ import annotations

import logging
import time
from dataclasses import dataclass

from gesture_control.action_mapper import ActionMapper
from gesture_control.backends import DryRunInputBackend, InputBackend, MacOSInputBackend
from gesture_control.camera import OpenCVCameraSource, SyntheticCameraSource
from gesture_control.config import AppConfig
from gesture_control.debug_overlay import draw_overlay
from gesture_control.gesture_engine import GestureEngine
from gesture_control.hotkeys import HotkeyController, RuntimeControl
from gesture_control.tracking import HandTracker

try:
    import cv2
except Exception:  # pragma: no cover
    cv2 = None


LOGGER = logging.getLogger(__name__)


@dataclass
class AppRuntime:
    config: AppConfig
    use_camera: bool = True
    enable_hotkeys: bool = True
    mode_override: str | None = None

    def _select_backend(self, mode: str) -> InputBackend:
        if mode == "os":
            return MacOSInputBackend()
        return DryRunInputBackend()

    def run(self) -> int:
        mode = self.mode_override or self.config.runtime.mode
        if mode not in {"dry-run", "os"}:
            raise ValueError(f"unsupported mode: {mode}")

        source = None
        tracker = None
        backend: InputBackend | None = None
        hotkeys = HotkeyController(self.config.hotkeys, enabled=self.enable_hotkeys)
        control = RuntimeControl()

        try:
            if self.use_camera:
                try:
                    source = OpenCVCameraSource(
                        camera_index=self.config.runtime.camera_index,
                        width=self.config.runtime.camera_width,
                        height=self.config.runtime.camera_height,
                    )
                except Exception as exc:
                    LOGGER.warning("camera unavailable (%s), fallback to synthetic source", exc)
                    source = SyntheticCameraSource(
                        width=self.config.runtime.camera_width,
                        height=self.config.runtime.camera_height,
                    )
            else:
                source = SyntheticCameraSource(
                    width=self.config.runtime.camera_width,
                    height=self.config.runtime.camera_height,
                )

            tracker = HandTracker(model_asset_path=self.config.tracking.model_asset_path)
            backend = self._select_backend(mode)
            mapper = ActionMapper(shortcut_map=self.config.shortcut_map())
            engine = GestureEngine(self.config.gesture)
            hotkeys.start(control)

            frame_budget = self.config.runtime.max_frames
            frame_id = 0
            last_hand_present: bool | None = None
            last_action = "none"
            frame_interval = 1.0 / max(self.config.runtime.max_fps, 1.0)

            while not control.should_exit:
                start = time.monotonic()
                frame = source.read()
                if frame is None:
                    LOGGER.error("frame capture failed")
                    break

                tracking = tracker.process(frame)
                if last_hand_present != tracking.hand_present:
                    last_hand_present = tracking.hand_present
                    LOGGER.info("hand_present=%s tracker=%s", tracking.hand_present, tracking.tracker_status)

                snapshot = engine.update(tracking, paused=control.paused)
                commands = mapper.map_actions(snapshot)
                for command in commands:
                    backend.emit(command)
                    if command.description != "no action":
                        last_action = command.description

                draw_overlay(
                    frame,
                    mode=mode,
                    tracking=tracking,
                    snapshot=snapshot,
                    last_action=last_action,
                )

                if self.config.runtime.show_window and cv2 is not None:
                    cv2.imshow(self.config.runtime.window_name, frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord("q"):
                        control.request_exit()
                    elif key == ord("p"):
                        control.toggle_pause()

                frame_id += 1
                if frame_budget is not None and frame_id >= frame_budget:
                    LOGGER.info("max_frames reached: %s", frame_budget)
                    break

                elapsed = time.monotonic() - start
                sleep_s = frame_interval - elapsed
                if sleep_s > 0:
                    time.sleep(sleep_s)

            return 0
        finally:
            hotkeys.stop()
            if tracker is not None:
                tracker.close()
            if source is not None:
                source.release()
            if backend is not None:
                backend.close()
            if cv2 is not None:
                cv2.destroyAllWindows()
