from __future__ import annotations

from pathlib import Path

from gesture_control.config import DEFAULT_CONFIG_PATH, PROJECT_ROOT, load_config


def test_load_default_config() -> None:
    config = load_config(DEFAULT_CONFIG_PATH)
    assert config.runtime.mode == "dry-run"
    assert config.runtime.camera_index == 0
    assert config.tracking.model_asset_path is not None
    assert config.tracking.model_asset_path.name == "hand_landmarker.task"
    assert config.gesture.control_thumb_threshold > 0
    assert config.gesture.cursor_mode == "relative"
    assert config.gesture.cursor_fast_smoothing > config.gesture.cursor_smoothing
    assert config.gesture.cursor_jitter_floor > 0
    assert config.gesture.cursor_max_step > 0
    assert config.shortcut_map()["thumbs_up"] == ["cmd", "l"]


def test_load_custom_config(tmp_path: Path) -> None:
    config_file = tmp_path / "custom.yaml"
    config_file.write_text(
        """
runtime:
  mode: os
  camera_index: 2
  max_frames: 10
gesture:
  cursor_mode: absolute
  cursor_smoothing: 0.5
  cursor_fast_smoothing: 0.8
  cursor_jitter_floor: 0.01
  cursor_max_step: 0.04
tracking:
  model_asset_path: local-model.task
shortcuts:
  - gesture: thumbs_up
    keys: ["ctrl", "k"]
""".strip(),
        encoding="utf-8",
    )

    config = load_config(config_file)
    assert config.runtime.mode == "os"
    assert config.runtime.camera_index == 2
    assert config.runtime.max_frames == 10
    assert config.tracking.model_asset_path == PROJECT_ROOT / "local-model.task"
    assert config.gesture.cursor_mode == "absolute"
    assert config.gesture.cursor_smoothing == 0.5
    assert config.gesture.cursor_fast_smoothing == 0.8
    assert config.gesture.cursor_jitter_floor == 0.01
    assert config.gesture.cursor_max_step == 0.04
    assert config.shortcut_map()["thumbs_up"] == ["ctrl", "k"]
