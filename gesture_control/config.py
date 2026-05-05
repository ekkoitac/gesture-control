from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "default.yaml"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HAND_LANDMARKER_MODEL_PATH = PROJECT_ROOT / "config" / "models" / "hand_landmarker.task"


@dataclass
class RuntimeConfig:
    mode: str = "dry-run"
    camera_index: int = 0
    camera_width: int = 1280
    camera_height: int = 720
    show_window: bool = True
    window_name: str = "Gesture Control Debug"
    max_fps: float = 30.0
    max_frames: int | None = None


@dataclass
class TrackingConfig:
    model_asset_path: Path | None = DEFAULT_HAND_LANDMARKER_MODEL_PATH


@dataclass
class HotkeyConfig:
    pause_toggle: str = "<ctrl>+<alt>+p"
    exit: str = "<ctrl>+<alt>+q"


@dataclass
class GestureConfig:
    control_fold_tolerance: float = 0.015
    control_extend_threshold: float = 0.04
    control_thumb_threshold: float = 0.075
    cursor_smoothing: float = 0.35
    cursor_dead_zone: float = 0.012
    pinch_threshold: float = 0.055
    pinch_release_threshold: float = 0.07
    pinch_scroll_gain: float = 1800.0
    pinch_min_delta: float = 0.006
    pinch_cooldown_frames: int = 3
    wave_threshold: float = 0.085
    wave_cooldown_frames: int = 8
    shortcut_cooldown_frames: int = 15


@dataclass
class ShortcutBinding:
    gesture: str
    keys: list[str]


@dataclass
class AppConfig:
    runtime: RuntimeConfig = field(default_factory=RuntimeConfig)
    tracking: TrackingConfig = field(default_factory=TrackingConfig)
    hotkeys: HotkeyConfig = field(default_factory=HotkeyConfig)
    gesture: GestureConfig = field(default_factory=GestureConfig)
    shortcuts: list[ShortcutBinding] = field(default_factory=list)

    def shortcut_map(self) -> dict[str, list[str]]:
        return {item.gesture: list(item.keys) for item in self.shortcuts}


def _as_dict(data: Any) -> dict[str, Any]:
    if isinstance(data, dict):
        return data
    return {}


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        parsed = yaml.safe_load(file)
    if parsed is None:
        return {}
    if not isinstance(parsed, dict):
        raise ValueError(f"config root must be a mapping: {path}")
    return parsed


def _runtime_from_dict(data: dict[str, Any]) -> RuntimeConfig:
    return RuntimeConfig(
        mode=str(data.get("mode", "dry-run")),
        camera_index=int(data.get("camera_index", 0)),
        camera_width=int(data.get("camera_width", 1280)),
        camera_height=int(data.get("camera_height", 720)),
        show_window=bool(data.get("show_window", True)),
        window_name=str(data.get("window_name", "Gesture Control Debug")),
        max_fps=float(data.get("max_fps", 30.0)),
        max_frames=None if data.get("max_frames") is None else int(data.get("max_frames")),
    )


def _tracking_from_dict(data: dict[str, Any]) -> TrackingConfig:
    raw_path = data.get("model_asset_path")
    if raw_path is None:
        return TrackingConfig()
    value = str(raw_path).strip()
    if not value:
        return TrackingConfig(model_asset_path=None)
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return TrackingConfig(model_asset_path=path)


def _hotkeys_from_dict(data: dict[str, Any]) -> HotkeyConfig:
    return HotkeyConfig(
        pause_toggle=str(data.get("pause_toggle", "<ctrl>+<alt>+p")),
        exit=str(data.get("exit", "<ctrl>+<alt>+q")),
    )


def _gesture_from_dict(data: dict[str, Any]) -> GestureConfig:
    return GestureConfig(
        control_fold_tolerance=float(data.get("control_fold_tolerance", 0.015)),
        control_extend_threshold=float(data.get("control_extend_threshold", 0.04)),
        control_thumb_threshold=float(data.get("control_thumb_threshold", 0.075)),
        cursor_smoothing=float(data.get("cursor_smoothing", 0.35)),
        cursor_dead_zone=float(data.get("cursor_dead_zone", 0.012)),
        pinch_threshold=float(data.get("pinch_threshold", 0.055)),
        pinch_release_threshold=float(data.get("pinch_release_threshold", 0.07)),
        pinch_scroll_gain=float(data.get("pinch_scroll_gain", 1800.0)),
        pinch_min_delta=float(data.get("pinch_min_delta", 0.006)),
        pinch_cooldown_frames=int(data.get("pinch_cooldown_frames", 3)),
        wave_threshold=float(data.get("wave_threshold", 0.085)),
        wave_cooldown_frames=int(data.get("wave_cooldown_frames", 8)),
        shortcut_cooldown_frames=int(data.get("shortcut_cooldown_frames", 15)),
    )


def _shortcuts_from_list(data: Any) -> list[ShortcutBinding]:
    if not isinstance(data, list):
        return []
    items: list[ShortcutBinding] = []
    for index, raw in enumerate(data):
        if not isinstance(raw, dict):
            raise ValueError(f"shortcut[{index}] must be a mapping")
        gesture = str(raw.get("gesture", "")).strip()
        keys = raw.get("keys", [])
        if not gesture:
            raise ValueError(f"shortcut[{index}] gesture is required")
        if not isinstance(keys, list) or not all(isinstance(item, str) for item in keys):
            raise ValueError(f"shortcut[{index}] keys must be a list[str]")
        items.append(ShortcutBinding(gesture=gesture, keys=list(keys)))
    return items


def load_config(path: str | Path | None = None) -> AppConfig:
    config_path = DEFAULT_CONFIG_PATH if path is None else Path(path).expanduser().resolve()
    raw = _load_yaml(config_path)
    return AppConfig(
        runtime=_runtime_from_dict(_as_dict(raw.get("runtime"))),
        tracking=_tracking_from_dict(_as_dict(raw.get("tracking"))),
        hotkeys=_hotkeys_from_dict(_as_dict(raw.get("hotkeys"))),
        gesture=_gesture_from_dict(_as_dict(raw.get("gesture"))),
        shortcuts=_shortcuts_from_list(raw.get("shortcuts", [])),
    )
