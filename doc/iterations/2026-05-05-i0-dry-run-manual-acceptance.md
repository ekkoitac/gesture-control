# Iteration Record: I0 Dry-Run Manual Acceptance

## Goal

- Record `I0-03` dry-run manual acceptance after gesture tuning.
- Split remaining OS-emission validation into a separate follow-up TODO instead of marking release validation complete.

## Outcome

- Dry-run manual validation passed after tuning activation, wave, pinch, cursor suppression, and shortcut gestures.
- Validated dry-run behaviors:
  - real webcam frame display,
  - hand present/lost transitions,
  - back-of-hand shaka activation,
  - palm-facing thumbs-down deactivation from either hand,
  - inactive suppression,
  - cursor movement when no discrete gesture is active,
  - thumb-index pinch scroll,
  - wave scroll only outside pinch hold,
  - `thumbs_up` shortcut,
  - strict `ok_sign` shortcut,
  - no-hand suppression,
  - pause/exit path in dry-run.

## TODO Changes

- Marked `I0-03` as completed for dry-run manual acceptance.
- Added `I0-04` for OS-input mode and Accessibility permission validation.
- Moved release-doc reconciliation to `I0-05` so release docs wait for OS-mode evidence.

## Open Items

- Grant Accessibility permission to the Terminal-hosted Python runtime.
- Run OS-input validation from macOS Terminal.
- Reconcile known issues and release docs after OS-mode validation.
