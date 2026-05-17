from __future__ import annotations

from dataclasses import dataclass
from math import hypot

from gesture_control.config import GestureConfig
from gesture_control.contracts import CursorControlMode, GestureSnapshot, Point3D, TrackingResult


def _distance(a: Point3D, b: Point3D) -> float:
    return hypot(a.x - b.x, a.y - b.y)


@dataclass
class GestureEngine:
    config: GestureConfig

    def __post_init__(self) -> None:
        self._active_latched = False
        self._control_gesture_latched: str | None = None
        self._pinch_contact = False
        self._prev_cursor_raw: tuple[float, float] | None = None
        self._smoothed_cursor_position: tuple[float, float] | None = None
        self._smoothed_cursor_delta: tuple[float, float] = (0.0, 0.0)
        self._prev_pinch_index_y: float | None = None
        self._wave_anchor_x: float | None = None
        self._pinch_cooldown = 0
        self._wave_cooldown = 0
        self._shortcut_cooldown = 0

    def _consume_cooldowns(self) -> None:
        if self._pinch_cooldown > 0:
            self._pinch_cooldown -= 1
        if self._wave_cooldown > 0:
            self._wave_cooldown -= 1
        if self._shortcut_cooldown > 0:
            self._shortcut_cooldown -= 1

    def _finger_folded(self, tip: Point3D, pip: Point3D) -> bool:
        return tip.y >= pip.y - self.config.control_fold_tolerance

    def _finger_extended(self, tip: Point3D, pip: Point3D) -> bool:
        return tip.y < pip.y - self.config.control_extend_threshold

    def _finger_straight_up(self, tip: Point3D, pip: Point3D, mcp: Point3D) -> bool:
        return (
            tip.y < pip.y - self.config.control_extend_threshold
            and pip.y < mcp.y - self.config.control_extend_threshold
        )

    def _detect_index_pointing_pose(self, tracking: TrackingResult) -> bool:
        index_mcp = tracking.get_landmark("index_mcp")
        index_pip = tracking.get_landmark("index_pip")
        index_tip = tracking.get_landmark("index_tip")
        middle_mcp = tracking.get_landmark("middle_mcp")
        middle_pip = tracking.get_landmark("middle_pip")
        middle_tip = tracking.get_landmark("middle_tip")
        ring_mcp = tracking.get_landmark("ring_mcp")
        ring_pip = tracking.get_landmark("ring_pip")
        ring_tip = tracking.get_landmark("ring_tip")
        pinky_mcp = tracking.get_landmark("pinky_mcp")
        pinky_pip = tracking.get_landmark("pinky_pip")
        pinky_tip = tracking.get_landmark("pinky_tip")

        if not all(
            [
                index_mcp,
                index_pip,
                index_tip,
                middle_mcp,
                middle_pip,
                middle_tip,
                ring_mcp,
                ring_pip,
                ring_tip,
                pinky_mcp,
                pinky_pip,
                pinky_tip,
            ]
        ):
            return False

        index_reach = index_mcp.y - index_tip.y
        index_points_up = (
            index_tip.y <= index_pip.y + self.config.control_fold_tolerance
            and index_pip.y < index_mcp.y - self.config.control_fold_tolerance
            and index_reach >= self.config.control_thumb_threshold
        )
        if not index_points_up:
            return False

        non_index_straight = any(
            self._finger_straight_up(tip, pip, mcp)
            for tip, pip, mcp in [
                (middle_tip, middle_pip, middle_mcp),
                (ring_tip, ring_pip, ring_mcp),
                (pinky_tip, pinky_pip, pinky_mcp),
            ]
        )
        return not non_index_straight

    def _detect_activation_gesture(self, tracking: TrackingResult) -> str | None:
        thumb_tip = tracking.get_landmark("thumb_tip")
        thumb_ip = tracking.get_landmark("thumb_ip")
        thumb_mcp = tracking.get_landmark("thumb_mcp")
        index_pip = tracking.get_landmark("index_pip")
        index_tip = tracking.get_landmark("index_tip")
        middle_pip = tracking.get_landmark("middle_pip")
        middle_tip = tracking.get_landmark("middle_tip")
        ring_pip = tracking.get_landmark("ring_pip")
        ring_tip = tracking.get_landmark("ring_tip")
        pinky_pip = tracking.get_landmark("pinky_pip")
        pinky_tip = tracking.get_landmark("pinky_tip")

        if not all(
            [
                thumb_tip,
                thumb_ip,
                thumb_mcp,
                index_pip,
                index_tip,
                middle_pip,
                middle_tip,
                ring_pip,
                ring_tip,
                pinky_pip,
                pinky_tip,
            ]
        ):
            return None

        folded_core = sum(
            self._finger_folded(tip, pip)
            for tip, pip in [
                (index_tip, index_pip),
                (middle_tip, middle_pip),
                (ring_tip, ring_pip),
            ]
        )
        thumb_extended = _distance(thumb_tip, thumb_mcp) >= self.config.control_thumb_threshold
        pinky_extended = self._finger_extended(pinky_tip, pinky_pip)

        if thumb_extended and pinky_extended and folded_core >= 2:
            return "activate"

        folded_fingers = folded_core + int(self._finger_folded(pinky_tip, pinky_pip))
        thumb_points_down = (
            thumb_tip.y > thumb_ip.y - self.config.control_fold_tolerance
            and thumb_tip.y > thumb_mcp.y + self.config.control_extend_threshold
        )
        if thumb_points_down and folded_fingers >= 3:
            return "deactivate"

        return None

    def _apply_activation_gesture(self, control_gesture: str | None) -> str | None:
        if control_gesture is None:
            self._control_gesture_latched = None
            return None
        if control_gesture == self._control_gesture_latched:
            return None

        self._control_gesture_latched = control_gesture
        if control_gesture == "activate" and not self._active_latched:
            self._active_latched = True
            return "activated"
        if control_gesture == "deactivate" and self._active_latched:
            self._active_latched = False
            return "deactivated"
        return None

    def _detect_shortcut_gesture(self, tracking: TrackingResult) -> str | None:
        thumb_tip = tracking.get_landmark("thumb_tip")
        thumb_ip = tracking.get_landmark("thumb_ip")
        thumb_mcp = tracking.get_landmark("thumb_mcp")
        index_tip = tracking.get_landmark("index_tip")
        index_pip = tracking.get_landmark("index_pip")
        middle_mcp = tracking.get_landmark("middle_mcp")
        middle_tip = tracking.get_landmark("middle_tip")
        middle_pip = tracking.get_landmark("middle_pip")
        ring_mcp = tracking.get_landmark("ring_mcp")
        ring_tip = tracking.get_landmark("ring_tip")
        ring_pip = tracking.get_landmark("ring_pip")
        pinky_mcp = tracking.get_landmark("pinky_mcp")
        pinky_tip = tracking.get_landmark("pinky_tip")
        pinky_pip = tracking.get_landmark("pinky_pip")

        if not all(
            [
                thumb_tip,
                thumb_ip,
                thumb_mcp,
                index_tip,
                index_pip,
                middle_mcp,
                middle_tip,
                middle_pip,
                ring_mcp,
                ring_tip,
                ring_pip,
                pinky_mcp,
                pinky_tip,
                pinky_pip,
            ]
        ):
            return None

        # Thumbs up: support both side-facing and back-of-hand-facing poses.
        folded_fingers = sum(
            tip.y >= pip.y - 0.015
            for tip, pip in [
                (index_tip, index_pip),
                (middle_tip, middle_pip),
                (ring_tip, ring_pip),
                (pinky_tip, pinky_pip),
            ]
        )
        thumb_points_up = (
            thumb_tip.y < thumb_ip.y + self.config.control_fold_tolerance
            and thumb_tip.y < thumb_mcp.y - 0.025
            and thumb_tip.y < min(index_pip.y, middle_pip.y, ring_pip.y, pinky_pip.y) - 0.015
        )
        if thumb_points_up and folded_fingers >= 3:
            return "thumbs_up"

        # OK sign: thumb-index contact and three fingers straight upward.
        thumb_index_distance = _distance(thumb_tip, index_tip)
        if (
            thumb_index_distance < self.config.pinch_threshold
            and self._finger_straight_up(middle_tip, middle_pip, middle_mcp)
            and self._finger_straight_up(ring_tip, ring_pip, ring_mcp)
            and self._finger_straight_up(pinky_tip, pinky_pip, pinky_mcp)
        ):
            return "ok_sign"

        return None

    def _cursor_mode(self) -> CursorControlMode:
        return CursorControlMode(self.config.cursor_mode)

    def _reset_cursor_state(self) -> None:
        self._prev_cursor_raw = None
        self._smoothed_cursor_position = None
        self._smoothed_cursor_delta = (0.0, 0.0)

    def _reset_motion_state(self) -> None:
        self._pinch_contact = False
        self._reset_cursor_state()
        self._prev_pinch_index_y = None
        self._wave_anchor_x = None

    def _clamp_cursor_delta(self, delta: tuple[float, float]) -> tuple[float, float]:
        max_step = max(0.0, self.config.cursor_max_step)
        if max_step == 0.0:
            return (0.0, 0.0)

        norm = hypot(delta[0], delta[1])
        if norm <= max_step or norm == 0.0:
            return delta

        scale = max_step / norm
        return (delta[0] * scale, delta[1] * scale)

    def _relative_cursor_delta(self, raw_delta: tuple[float, float]) -> tuple[float, float]:
        raw_norm = hypot(raw_delta[0], raw_delta[1])
        if raw_norm < max(0.0, self.config.cursor_jitter_floor):
            self._smoothed_cursor_delta = (0.0, 0.0)
            return (0.0, 0.0)

        target_delta = self._clamp_cursor_delta(raw_delta)
        target_norm = hypot(target_delta[0], target_delta[1])
        max_step = max(self.config.cursor_max_step, target_norm, 1e-9)
        speed_scale = min(1.0, target_norm / max_step)
        slow_alpha = min(max(self.config.cursor_smoothing, 0.0), 1.0)
        fast_alpha = min(max(self.config.cursor_fast_smoothing, slow_alpha), 1.0)
        alpha = slow_alpha + (fast_alpha - slow_alpha) * speed_scale

        previous = self._smoothed_cursor_delta
        filtered = (
            alpha * target_delta[0] + (1.0 - alpha) * previous[0],
            alpha * target_delta[1] + (1.0 - alpha) * previous[1],
        )
        self._smoothed_cursor_delta = filtered

        if hypot(filtered[0], filtered[1]) < max(0.0, self.config.cursor_dead_zone):
            return (0.0, 0.0)
        return filtered

    def update(self, tracking: TrackingResult, paused: bool) -> GestureSnapshot:
        self._consume_cooldowns()

        if not tracking.hand_present:
            self._control_gesture_latched = None
            self._reset_motion_state()
            return GestureSnapshot(
                active=False,
                paused=paused,
                tracking_lost=True,
                metrics={"confidence": tracking.confidence},
            )

        index_tip = tracking.get_landmark("index_tip")
        wrist = tracking.get_landmark("wrist")

        control_gesture = self._detect_activation_gesture(tracking)
        activation_event = self._apply_activation_gesture(control_gesture)
        detected_gesture = None
        if control_gesture is None:
            detected_gesture = self._detect_shortcut_gesture(tracking)

        active = self._active_latched and not paused
        metrics: dict[str, float] = {"confidence": tracking.confidence}
        index_pointing = self._detect_index_pointing_pose(tracking)
        metrics["index_pointing"] = 1.0 if index_pointing else 0.0

        cursor_mode = self._cursor_mode()
        cursor_position: tuple[float, float] | None = None
        cursor_delta: tuple[float, float] | None = None
        if active and index_tip and index_pointing:
            raw_cursor = (index_tip.x, index_tip.y)
            if cursor_mode == CursorControlMode.RELATIVE:
                cursor_position = raw_cursor
                if self._prev_cursor_raw is None:
                    cursor_delta = (0.0, 0.0)
                    self._smoothed_cursor_delta = (0.0, 0.0)
                else:
                    raw_delta = (
                        raw_cursor[0] - self._prev_cursor_raw[0],
                        raw_cursor[1] - self._prev_cursor_raw[1],
                    )
                    cursor_delta = self._relative_cursor_delta(raw_delta)
                    metrics["cursor_delta_raw_norm"] = hypot(raw_delta[0], raw_delta[1])
                self._prev_cursor_raw = raw_cursor
                self._smoothed_cursor_position = None
            else:
                if self._smoothed_cursor_position is None:
                    smoothed = raw_cursor
                    cursor_delta = (0.0, 0.0)
                else:
                    alpha = self.config.cursor_smoothing
                    smoothed = (
                        alpha * raw_cursor[0] + (1.0 - alpha) * self._smoothed_cursor_position[0],
                        alpha * raw_cursor[1] + (1.0 - alpha) * self._smoothed_cursor_position[1],
                    )
                    cursor_delta = (
                        smoothed[0] - self._smoothed_cursor_position[0],
                        smoothed[1] - self._smoothed_cursor_position[1],
                    )

                self._prev_cursor_raw = raw_cursor
                self._smoothed_cursor_position = smoothed
                cursor_position = smoothed
                if (
                    cursor_delta is not None
                    and hypot(cursor_delta[0], cursor_delta[1]) < self.config.cursor_dead_zone
                ):
                    cursor_delta = (0.0, 0.0)

            if cursor_delta is not None:
                metrics["cursor_delta_norm"] = hypot(cursor_delta[0], cursor_delta[1])
        else:
            self._reset_cursor_state()

        pinch_scroll = 0.0
        pinch_active = False
        thumb_tip = tracking.get_landmark("thumb_tip")
        if thumb_tip and index_tip:
            pinch_distance = _distance(thumb_tip, index_tip)
            metrics["pinch_distance"] = pinch_distance
            if self._pinch_contact:
                pinch_contact = pinch_distance < self.config.pinch_release_threshold
            else:
                pinch_contact = pinch_distance < self.config.pinch_threshold
            self._pinch_contact = pinch_contact

            is_ok_shortcut = detected_gesture == "ok_sign"
            pinch_active = active and pinch_contact and not is_ok_shortcut
            if pinch_active:
                if self._prev_pinch_index_y is not None:
                    delta_y = index_tip.y - self._prev_pinch_index_y
                    metrics["pinch_delta_y"] = delta_y
                    if (
                        abs(delta_y) >= self.config.pinch_min_delta
                        and self._pinch_cooldown == 0
                    ):
                        pinch_scroll = -delta_y * self.config.pinch_scroll_gain
                        self._pinch_cooldown = self.config.pinch_cooldown_frames
                self._prev_pinch_index_y = index_tip.y
            else:
                self._prev_pinch_index_y = None

        wave_scroll = 0
        if wrist:
            if self._wave_anchor_x is None or not active:
                self._wave_anchor_x = wrist.x
            wave_delta = wrist.x - self._wave_anchor_x
            metrics["wave_delta_x"] = wave_delta
            if (
                active
                and not pinch_active
                and self._wave_cooldown == 0
                and abs(wave_delta) >= self.config.wave_threshold
            ):
                wave_scroll = 1 if wave_delta > 0 else -1
                self._wave_cooldown = self.config.wave_cooldown_frames
                self._wave_anchor_x = wrist.x

        shortcut_gesture = None
        if active and detected_gesture and self._shortcut_cooldown == 0:
            shortcut_gesture = detected_gesture
            self._shortcut_cooldown = self.config.shortcut_cooldown_frames

        return GestureSnapshot(
            active=active,
            paused=paused,
            tracking_lost=False,
            cursor_mode=cursor_mode,
            cursor_position=cursor_position,
            cursor_delta=cursor_delta,
            pinch_active=pinch_active,
            pinch_scroll=pinch_scroll,
            wave_scroll=wave_scroll,
            shortcut_gesture=shortcut_gesture,
            activation_event=activation_event,
            metrics=metrics,
        )
