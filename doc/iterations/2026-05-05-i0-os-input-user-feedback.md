# Iteration Record: I0 OS-Input User Feedback

## Goal

- Record user feedback from the `I0-04` OS-input validation run.
- Update TODO status only; do not implement cursor behavior changes in this iteration.

## User Feedback

- OS-input mode was tested from macOS Terminal and was overall acceptable.
- Two cursor-control refinements remain:
  - cursor movement should only occur when the user is intentionally pointing with the index finger,
  - fully straight and slightly bent index-finger poses should both count as valid pointing,
  - cursor movement direction currently feels mirrored and should match hand movement direction.

## TODO Changes

- Marked `I0-04` complete based on user-reported OS-mode validation.
- Added `I0-05` for index-finger-only cursor movement gating.
- Added `I0-06` for cursor direction alignment.
- Moved release/known-issues reconciliation to `I0-07` so release docs wait for the new cursor follow-ups.

## Validation

- Documentation-only update; no code changes and no automated tests run for this iteration.
