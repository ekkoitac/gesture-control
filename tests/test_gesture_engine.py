from __future__ import annotations

from math import hypot

import pytest

from gesture_control.config import GestureConfig
from gesture_control.contracts import CursorControlMode, Point3D, TrackingResult
from gesture_control.gesture_engine import GestureEngine


def _tracking_result(
    *,
    hand_present: bool = True,
    thumb_tip: tuple[float, float] = (0.3, 0.6),
    middle_tip: tuple[float, float] = (0.45, 0.6),
    index_tip: tuple[float, float] = (0.4, 0.5),
    wrist: tuple[float, float] = (0.45, 0.8),
    handedness: str | None = None,
    overrides: dict[str, tuple[float, float]] | None = None,
) -> TrackingResult:
    landmarks = {
        "wrist": Point3D(*wrist),
        "thumb_mcp": Point3D(0.3, 0.7),
        "thumb_ip": Point3D(0.31, 0.65),
        "thumb_tip": Point3D(*thumb_tip),
        "index_mcp": Point3D(0.4, 0.66),
        "index_pip": Point3D(0.4, 0.56),
        "index_tip": Point3D(*index_tip),
        "middle_mcp": Point3D(0.45, 0.66),
        "middle_pip": Point3D(0.45, 0.58),
        "middle_tip": Point3D(*middle_tip),
        "ring_mcp": Point3D(0.49, 0.70),
        "ring_pip": Point3D(0.49, 0.62),
        "ring_tip": Point3D(0.49, 0.67),
        "pinky_mcp": Point3D(0.53, 0.72),
        "pinky_pip": Point3D(0.53, 0.64),
        "pinky_tip": Point3D(0.53, 0.68),
    }
    if overrides:
        landmarks.update({name: Point3D(*point) for name, point in overrides.items()})
    return TrackingResult(
        frame_width=1280,
        frame_height=720,
        hand_present=hand_present,
        confidence=0.95 if hand_present else 0.0,
        handedness=handedness,
        landmarks=landmarks if hand_present else {},
        tracker_status="ok" if hand_present else "no-hand",
    )


def _shaka_tracking() -> TrackingResult:
    return _tracking_result(
        overrides={
            "thumb_mcp": (0.42, 0.55),
            "thumb_ip": (0.35, 0.55),
            "thumb_tip": (0.30, 0.55),
            "index_pip": (0.46, 0.52),
            "index_tip": (0.46, 0.54),
            "middle_pip": (0.49, 0.52),
            "middle_tip": (0.49, 0.54),
            "ring_pip": (0.52, 0.52),
            "ring_tip": (0.52, 0.54),
            "pinky_pip": (0.56, 0.56),
            "pinky_tip": (0.56, 0.48),
        }
    )


def _thumbs_down_tracking(handedness: str | None = None) -> TrackingResult:
    return _tracking_result(
        handedness=handedness,
        overrides={
            "thumb_mcp": (0.42, 0.54),
            "thumb_ip": (0.42, 0.60),
            "thumb_tip": (0.42, 0.66),
            "index_pip": (0.46, 0.50),
            "index_tip": (0.46, 0.52),
            "middle_pip": (0.49, 0.50),
            "middle_tip": (0.49, 0.52),
            "ring_pip": (0.52, 0.50),
            "ring_tip": (0.52, 0.52),
            "pinky_pip": (0.55, 0.50),
            "pinky_tip": (0.55, 0.52),
        },
    )


def test_activation_gestures_and_tracking_loss() -> None:
    engine = GestureEngine(GestureConfig())

    # Activate by back-of-hand shaka.
    snap1 = engine.update(_shaka_tracking(), paused=False)
    assert snap1.activation_event == "activated"
    assert snap1.active is True

    # Holding the same control gesture should not repeat activation.
    snap2 = engine.update(_shaka_tracking(), paused=False)
    assert snap2.activation_event is None
    assert snap2.active is True

    # Deactivate by palm-facing thumbs down from either hand.
    snap3 = engine.update(_thumbs_down_tracking(handedness="Left"), paused=False)
    assert snap3.activation_event == "deactivated"
    assert snap3.active is False

    # Lose hand tracking: active output suppressed.
    snap4 = engine.update(_tracking_result(hand_present=False), paused=False)
    assert snap4.active is False
    assert snap4.tracking_lost is True


def test_pinch_scroll_and_wave_with_cooldown() -> None:
    cfg = GestureConfig(
        pinch_cooldown_frames=2,
        wave_cooldown_frames=2,
    )
    engine = GestureEngine(cfg)

    engine.update(_shaka_tracking(), paused=False)
    # Release activation gesture and seed pinch baseline.
    engine.update(_tracking_result(thumb_tip=(0.3, 0.6), middle_tip=(0.5, 0.6)), paused=False)
    seed = engine.update(
        _tracking_result(thumb_tip=(0.39, 0.5), index_tip=(0.4, 0.5), middle_tip=(0.5, 0.6)),
        paused=False,
    )
    assert seed.pinch_active is True
    assert seed.pinch_scroll == 0.0

    # Move index while pinched; should emit scroll once.
    scroll = engine.update(
        _tracking_result(thumb_tip=(0.39, 0.52), index_tip=(0.4, 0.56), middle_tip=(0.5, 0.6)),
        paused=False,
    )
    assert scroll.pinch_active is True
    assert scroll.pinch_scroll != 0.0

    # Immediate frame should be blocked by cooldown.
    blocked = engine.update(
        _tracking_result(thumb_tip=(0.39, 0.55), index_tip=(0.4, 0.61), middle_tip=(0.5, 0.6)),
        paused=False,
    )
    assert blocked.pinch_scroll == 0.0

    engine.update(
        _tracking_result(thumb_tip=(0.30, 0.55), index_tip=(0.45, 0.55), middle_tip=(0.5, 0.6)),
        paused=False,
    )

    # Wave trigger.
    wave = engine.update(
        _tracking_result(
            thumb_tip=(0.30, 0.55),
            index_tip=(0.45, 0.55),
            middle_tip=(0.5, 0.6),
            wrist=(0.62, 0.8),
        ),
        paused=False,
    )
    assert wave.wave_scroll in {-1, 1}


def test_wave_uses_cumulative_lateral_motion() -> None:
    cfg = GestureConfig(wave_threshold=0.085, wave_cooldown_frames=2)
    engine = GestureEngine(cfg)

    engine.update(_shaka_tracking(), paused=False)
    engine.update(_tracking_result(thumb_tip=(0.3, 0.6), middle_tip=(0.5, 0.6)), paused=False)

    small_step = engine.update(
        _tracking_result(thumb_tip=(0.3, 0.6), middle_tip=(0.5, 0.6), wrist=(0.50, 0.8)),
        paused=False,
    )
    assert small_step.wave_scroll == 0

    cumulative_step = engine.update(
        _tracking_result(thumb_tip=(0.3, 0.6), middle_tip=(0.5, 0.6), wrist=(0.54, 0.8)),
        paused=False,
    )
    assert cumulative_step.wave_scroll == 1


def test_thumbs_up_shortcut_does_not_toggle_activation() -> None:
    engine = GestureEngine(GestureConfig())

    engine.update(_shaka_tracking(), paused=False)
    engine.update(_tracking_result(thumb_tip=(0.3, 0.6), middle_tip=(0.5, 0.6)), paused=False)

    snap = engine.update(
        _tracking_result(
            overrides={
                "thumb_mcp": (0.44, 0.48),
                "thumb_ip": (0.44, 0.45),
                "thumb_tip": (0.44, 0.42),
                "index_pip": (0.48, 0.52),
                "index_tip": (0.48, 0.54),
                "middle_pip": (0.45, 0.52),
                "middle_tip": (0.45, 0.54),
                "ring_pip": (0.52, 0.52),
                "ring_tip": (0.52, 0.54),
                "pinky_pip": (0.56, 0.52),
                "pinky_tip": (0.56, 0.54),
            }
        ),
        paused=False,
    )

    assert snap.active is True
    assert snap.activation_event is None
    assert snap.shortcut_gesture == "thumbs_up"


def test_ok_sign_uses_pinch_threshold_for_shortcut_detection() -> None:
    engine = GestureEngine(GestureConfig())

    engine.update(_shaka_tracking(), paused=False)
    engine.update(_tracking_result(thumb_tip=(0.3, 0.6), middle_tip=(0.5, 0.6)), paused=False)

    snap = engine.update(
        _tracking_result(
            overrides={
                "thumb_tip": (0.44, 0.50),
                "index_tip": (0.49, 0.50),
                "middle_pip": (0.45, 0.58),
                "middle_tip": (0.45, 0.50),
                "ring_pip": (0.49, 0.62),
                "ring_tip": (0.49, 0.54),
                "pinky_pip": (0.53, 0.64),
                "pinky_tip": (0.53, 0.56),
            }
        ),
        paused=False,
    )

    assert snap.shortcut_gesture == "ok_sign"


def test_ok_sign_does_not_emit_pinch_scroll() -> None:
    engine = GestureEngine(GestureConfig())

    engine.update(_shaka_tracking(), paused=False)
    engine.update(_tracking_result(thumb_tip=(0.3, 0.6), middle_tip=(0.5, 0.6)), paused=False)

    seed = engine.update(
        _tracking_result(
            overrides={
                "thumb_tip": (0.44, 0.50),
                "index_tip": (0.49, 0.50),
                "middle_pip": (0.45, 0.58),
                "middle_tip": (0.45, 0.50),
                "ring_pip": (0.49, 0.62),
                "ring_tip": (0.49, 0.54),
                "pinky_pip": (0.53, 0.64),
                "pinky_tip": (0.53, 0.56),
            }
        ),
        paused=False,
    )
    assert seed.shortcut_gesture == "ok_sign"
    assert seed.pinch_scroll == 0.0

    moved = engine.update(
        _tracking_result(
            overrides={
                "thumb_tip": (0.44, 0.56),
                "index_tip": (0.49, 0.56),
                "middle_pip": (0.45, 0.64),
                "middle_tip": (0.45, 0.56),
                "ring_pip": (0.49, 0.68),
                "ring_tip": (0.49, 0.60),
                "pinky_pip": (0.53, 0.70),
                "pinky_tip": (0.53, 0.62),
            }
        ),
        paused=False,
    )
    assert moved.shortcut_gesture is None
    assert moved.pinch_scroll == 0.0


def test_relaxed_pinch_is_not_ok_sign() -> None:
    engine = GestureEngine(GestureConfig())

    engine.update(_shaka_tracking(), paused=False)
    engine.update(_tracking_result(thumb_tip=(0.3, 0.6), middle_tip=(0.5, 0.6)), paused=False)

    seed = engine.update(
        _tracking_result(
            overrides={
                "thumb_tip": (0.44, 0.50),
                "index_tip": (0.49, 0.50),
                "middle_pip": (0.45, 0.58),
                "middle_tip": (0.45, 0.56),
                "ring_pip": (0.49, 0.62),
                "ring_tip": (0.49, 0.60),
                "pinky_pip": (0.53, 0.64),
                "pinky_tip": (0.53, 0.62),
            }
        ),
        paused=False,
    )
    assert seed.shortcut_gesture is None
    assert seed.pinch_scroll == 0.0

    scrolled = engine.update(
        _tracking_result(
            overrides={
                "thumb_tip": (0.44, 0.57),
                "index_tip": (0.49, 0.57),
                "middle_pip": (0.45, 0.65),
                "middle_tip": (0.45, 0.63),
                "ring_pip": (0.49, 0.69),
                "ring_tip": (0.49, 0.67),
                "pinky_pip": (0.53, 0.71),
                "pinky_tip": (0.53, 0.69),
            }
        ),
        paused=False,
    )
    assert scrolled.shortcut_gesture is None
    assert scrolled.pinch_scroll != 0.0


def test_relative_cursor_first_pointing_frame_seeds_without_jump() -> None:
    engine = GestureEngine(GestureConfig())

    engine.update(_shaka_tracking(), paused=False)
    first = engine.update(_tracking_result(index_tip=(0.40, 0.50)), paused=False)

    assert first.active is True
    assert first.cursor_mode == CursorControlMode.RELATIVE
    assert first.cursor_position == (0.40, 0.50)
    assert first.cursor_delta == (0.0, 0.0)


def test_relative_cursor_filters_jitter_and_emits_slow_and_fast_delta() -> None:
    engine = GestureEngine(
        GestureConfig(
            cursor_smoothing=0.50,
            cursor_fast_smoothing=1.0,
            cursor_dead_zone=0.001,
            cursor_jitter_floor=0.005,
            cursor_max_step=0.040,
        )
    )

    engine.update(_shaka_tracking(), paused=False)
    engine.update(_tracking_result(index_tip=(0.40, 0.50)), paused=False)

    jitter = engine.update(_tracking_result(index_tip=(0.402, 0.501)), paused=False)
    assert jitter.cursor_delta == (0.0, 0.0)

    slow = engine.update(_tracking_result(index_tip=(0.412, 0.501)), paused=False)
    assert slow.cursor_delta is not None
    assert hypot(*slow.cursor_delta) > 0.0

    fast = engine.update(_tracking_result(index_tip=(0.512, 0.501)), paused=False)
    assert fast.cursor_delta is not None
    assert 0.0 < hypot(*fast.cursor_delta) <= 0.040


def test_relative_cursor_baseline_resets_after_pointing_loss_no_hand_and_pause() -> None:
    engine = GestureEngine(
        GestureConfig(
            cursor_smoothing=1.0,
            cursor_fast_smoothing=1.0,
            cursor_dead_zone=0.001,
            cursor_jitter_floor=0.001,
            cursor_max_step=0.10,
        )
    )

    engine.update(_shaka_tracking(), paused=False)
    engine.update(_tracking_result(index_tip=(0.40, 0.50)), paused=False)
    moved = engine.update(_tracking_result(index_tip=(0.46, 0.50)), paused=False)
    assert moved.cursor_delta is not None
    assert moved.cursor_delta[0] == pytest.approx(0.06)
    assert moved.cursor_delta[1] == 0.0

    not_pointing = engine.update(
        _tracking_result(
            index_tip=(0.70, 0.50),
            overrides={
                "middle_pip": (0.45, 0.58),
                "middle_tip": (0.45, 0.48),
            },
        ),
        paused=False,
    )
    assert not_pointing.cursor_delta is None

    reseeded = engine.update(_tracking_result(index_tip=(0.70, 0.50)), paused=False)
    assert reseeded.cursor_delta == (0.0, 0.0)

    engine.update(_tracking_result(hand_present=False), paused=False)
    after_no_hand = engine.update(_tracking_result(index_tip=(0.20, 0.50)), paused=False)
    assert after_no_hand.cursor_delta == (0.0, 0.0)

    paused = engine.update(_tracking_result(index_tip=(0.30, 0.50)), paused=True)
    assert paused.paused is True
    assert paused.cursor_delta is None

    after_pause = engine.update(_tracking_result(index_tip=(0.90, 0.50)), paused=False)
    assert after_pause.cursor_delta == (0.0, 0.0)


def test_pinch_hold_suppresses_wave_scroll() -> None:
    engine = GestureEngine(GestureConfig(wave_threshold=0.085))

    engine.update(_shaka_tracking(), paused=False)
    engine.update(_tracking_result(thumb_tip=(0.3, 0.6), middle_tip=(0.5, 0.6)), paused=False)

    seed = engine.update(
        _tracking_result(
            thumb_tip=(0.39, 0.50),
            index_tip=(0.40, 0.50),
            middle_tip=(0.50, 0.60),
            wrist=(0.45, 0.80),
        ),
        paused=False,
    )
    assert seed.pinch_active is True

    moved = engine.update(
        _tracking_result(
            thumb_tip=(0.39, 0.51),
            index_tip=(0.40, 0.51),
            middle_tip=(0.50, 0.60),
            wrist=(0.62, 0.80),
        ),
        paused=False,
    )
    assert moved.pinch_active is True
    assert moved.wave_scroll == 0


def test_cursor_requires_index_pointing_pose() -> None:
    engine = GestureEngine(GestureConfig())

    engine.update(_shaka_tracking(), paused=False)
    relaxed = engine.update(
        _tracking_result(
            overrides={
                "index_pip": (0.40, 0.56),
                "index_tip": (0.40, 0.60),
            }
        ),
        paused=False,
    )
    assert relaxed.active is True
    assert relaxed.metrics["index_pointing"] == 0.0
    assert relaxed.cursor_position is None
    assert relaxed.cursor_delta is None

    pointed = engine.update(_tracking_result(index_tip=(0.40, 0.50)), paused=False)
    assert pointed.metrics["index_pointing"] == 1.0
    assert pointed.cursor_position == (0.40, 0.50)
    assert pointed.cursor_delta == (0.0, 0.0)

    moved = engine.update(_tracking_result(index_tip=(0.46, 0.50)), paused=False)
    assert moved.metrics["index_pointing"] == 1.0
    assert moved.cursor_position is not None
    assert moved.cursor_delta is not None
    assert moved.cursor_delta[0] > 0.0


def test_slightly_bent_index_counts_as_pointing() -> None:
    engine = GestureEngine(GestureConfig())

    engine.update(_shaka_tracking(), paused=False)
    snap = engine.update(
        _tracking_result(
            overrides={
                "index_mcp": (0.40, 0.66),
                "index_pip": (0.40, 0.52),
                "index_tip": (0.41, 0.53),
            }
        ),
        paused=False,
    )

    assert snap.metrics["index_pointing"] == 1.0
    assert snap.cursor_position is not None


def test_open_palm_does_not_count_as_index_pointing() -> None:
    engine = GestureEngine(GestureConfig())

    engine.update(_shaka_tracking(), paused=False)
    snap = engine.update(
        _tracking_result(
            index_tip=(0.40, 0.50),
            overrides={
                "middle_mcp": (0.45, 0.66),
                "middle_pip": (0.45, 0.58),
                "middle_tip": (0.45, 0.50),
                "ring_mcp": (0.49, 0.70),
                "ring_pip": (0.49, 0.62),
                "ring_tip": (0.49, 0.54),
                "pinky_mcp": (0.53, 0.72),
                "pinky_pip": (0.53, 0.64),
                "pinky_tip": (0.53, 0.56),
            },
        ),
        paused=False,
    )

    assert snap.metrics["index_pointing"] == 0.0
    assert snap.cursor_position is None
