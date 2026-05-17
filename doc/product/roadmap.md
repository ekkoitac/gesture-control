# Roadmap

## Current Milestone

- Milestone name: `v0.2-cursor-smoothness`
- Target date: `2026-05-05`
- Success criteria:
  - Index-finger cursor control uses relative normalized deltas instead of absolute screen jumps.
  - Adaptive smoothing, jitter filtering, and max-step clamping have deterministic tests.
  - macOS relative cursor emission preserves user-perspective x direction and screen bounds.
  - Automated tests, ruff, and no-camera dry-run smoke validation pass.

## Next Milestones

- M1: Run manual macOS OS-mode validation for relative cursor feel on a real focused surface.
- M2: Tune gesture thresholds from real-device observations and add calibration profile support.
- M3: Add platform-specific backend adapters for Windows/Linux while preserving dry-run parity.
