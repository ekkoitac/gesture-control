# ADR-0001: Documentation Structure

## Status

- Accepted

## Context

- The project needs both human-readable docs and agent-readable progressive context.

## Decision

- Use `doc/` as the documentation root.
- Keep human docs as source of truth.
- Keep `AGENTS.md` + `doc/agent/` as progressive agent context.

## Consequences

- Better iteration traceability.
- Lower context load for coding agents.
- Requires disciplined updates after each feature change.

