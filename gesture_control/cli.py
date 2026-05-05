from __future__ import annotations

import argparse
import logging
from pathlib import Path

from gesture_control.app import AppRuntime
from gesture_control.config import DEFAULT_CONFIG_PATH, AppConfig, load_config


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Gesture control prototype runtime")
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help="Path to YAML config",
    )
    parser.add_argument(
        "--mode",
        choices=["dry-run", "os"],
        default=None,
        help="Input backend mode",
    )
    parser.add_argument("--camera-index", type=int, default=None, help="OpenCV camera index")
    parser.add_argument("--max-frames", type=int, default=None, help="Exit after N frames")
    parser.add_argument("--no-window", action="store_true", help="Run without OpenCV window")
    parser.add_argument("--no-camera", action="store_true", help="Use synthetic frames")
    parser.add_argument("--no-hotkeys", action="store_true", help="Disable global hotkeys")
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level",
    )
    return parser


def _apply_overrides(config: AppConfig, args: argparse.Namespace) -> AppConfig:
    if args.mode:
        config.runtime.mode = args.mode
    if args.camera_index is not None:
        config.runtime.camera_index = args.camera_index
    if args.max_frames is not None:
        config.runtime.max_frames = max(args.max_frames, 1)
    if args.no_window:
        config.runtime.show_window = False
    return config


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    config = load_config(args.config)
    config = _apply_overrides(config, args)

    runtime = AppRuntime(
        config=config,
        use_camera=not args.no_camera,
        enable_hotkeys=not args.no_hotkeys,
        mode_override=args.mode,
    )
    return runtime.run()
