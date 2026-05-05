# Changelog

## 2026-05-05

- Upgraded version TODO governance with status lifecycle, progress board, phase gates, required task evidence, and stricter completion rules.
- Opened `v0.2-cursor-smoothness` to optimize index-finger cursor smoothness and establish the relative cursor-control task split.
- Completed `I0-05` to `I0-07`: cursor movement now requires an intentional index-finger pointing pose, macOS cursor x mapping is flipped to match user-perceived hand direction, user dry-run and OS manual validation passed, and release/known-issue docs now show the v0.1 issue TODO as complete.
- Updated `I0-04` with user OS-mode validation feedback and added follow-up TODOs for index-finger-only cursor movement and cursor direction alignment.
- Recorded `I0-04` OS-input preflight results and marked the task blocked on user-controlled macOS Terminal Accessibility/manual OS-emission validation.
- Completed `I0-03` dry-run manual acceptance after gesture tuning and added `I0-04` to track OS-input/Accessibility validation before release-doc reconciliation.
- Tuned `I0-03` manual validation gestures: wave detection now uses cumulative wrist movement, `thumbs_up` supports the back-of-hand-facing pose, `ok_sign` requires fully straight middle/ring/pinky fingers and suppresses pinch scroll, thumb-index pinch hold suppresses cursor and wave output, and activation now uses back-of-hand shaka activate plus palm-facing thumbs-down deactivate from either hand.
- Completed `I0-02` real webcam hand-tracking validation from macOS Terminal after Camera permission was granted; remaining manual checklist work starts at `I0-03`.
- Completed `I0-01` by rebuilding `.venv` on Python 3.12.13, adding current MediaPipe Tasks `HandLandmarker` support, documenting the local model setup, and recording the remaining webcam permission blocker for `I0-02`.
- Added a new issue-focused TODO at `doc/version/v0.1-prototype/issues-todo.md` to track unresolved compatibility and real-device validation work.
- Completed `T1-01` to `T1-03` with Python runtime scaffold, CLI entrypoint, camera/debug loop, and tracker integration boundary.
- Completed `T2-01` to `T2-05` with activation gating, hotkey safety, cursor mapping, pinch scroll, wave scroll, and config-driven shortcuts.
- Completed `T3-01` to `T3-03` with automated tests, manual acceptance checklist, and full doc sync for the v0.1 prototype.
- Completed `T0-02` and `T0-03` by defining the v0.1 technical baseline and runtime architecture flow/module boundaries.
- Populated the v0.1 prototype product baseline and expanded the active TODO into a gesture-control MVP execution plan.
- Moved the scaffold MVP TODO into `doc/version/examples/` and created `v0.1-prototype` as the first active execution version.
- Added versioned TODO execution docs under `doc/version/`.
- Added focused agent TODO and subagent rules.
- Initialized documentation scaffold based on `spec-strategy.md`.
- Added human-first and agent-first documentation split.
