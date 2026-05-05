# Task Routing

## Before Every Task

- Read `doc/version/current.md`.
- Read the active version TODO.
- Read `doc/agent/todo-execution.md`.
- Select one TODO item only.
- Confirm the task has `Status`, `Progress`, `Acceptance`, `Validation`, `Evidence`, `Risks`, `Blockers`, `Follow-ups`, and `Done criteria` before implementation.

## Feature Changes

- Read: active TODO, `doc/product/requirements.md`, `doc/architecture/*`
- Update: active TODO task fields, progress board, `doc/changelog.md`, one file in `doc/iterations/`, related architecture docs

## Bug Fixes

- Read: active TODO, `doc/architecture/runtime-flow.md`, relevant iteration docs
- Update: active TODO task fields, progress board, `doc/changelog.md`, one file in `doc/iterations/`

## Refactors

- Read: active TODO, `doc/architecture/module-map.md`, `doc/decisions/*`
- Update: active TODO task fields, progress board, related architecture docs and changelog

## Complex Tasks

- Read `doc/agent/subagent-rules.md` before delegating.
- Use subagents only for `[L]` or `[XL]` TODOs with separable, non-blocking work.
- Mark a task `split-required` when it is too broad or touches overlapping subsystems.

## Validation Debt

- Record failed, skipped, or blocked validation in the active TODO progress board.
- Do not hide validation debt only in final chat output.
- Do not check off a task unless `Status: done`, `Progress: 100%`, and `Evidence` are all updated.
