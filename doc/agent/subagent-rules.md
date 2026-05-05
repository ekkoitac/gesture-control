# Subagent Rules

## Default

The main agent owns the task. Subagents are optional helpers, not a replacement for focus or final responsibility.

## When Subagents Are Allowed

Use a subagent only when all are true:

- The TODO item is `[L]` or `[XL]`.
- The subtask is bounded and can be described independently.
- The subtask is not the immediate blocker for the main agent's next step.
- The subtask has a disjoint read/write scope.
- The main agent can continue useful non-overlapping work.

## Good Uses

- Read-only exploration of a specific code area.
- Focused verification while implementation continues.
- Isolated implementation with clear file/module ownership.
- Risk review for a large change before final integration.

## Do Not Use Subagents For

- `[S]` tasks.
- Simple single-file edits.
- Ambiguous product decisions.
- Immediate blocking work.
- Overlapping write scopes.
- Broad "look through everything" requests.

## Delegation Contract

When delegating implementation, specify:

- Task ID.
- Exact scope.
- Owned files or modules.
- Files the subagent must not edit.
- Required validation.
- Required final summary, including changed paths.

The main agent must review, integrate, validate, and update the TODO after subagent work returns.

