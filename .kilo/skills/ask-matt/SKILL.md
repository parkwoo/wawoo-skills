---
name: ask-matt
description: Ask which skill or flow fits your situation. A router over the skills in this repo.
disable-model-invocation: true
---
# Ask Matt (skill router)

Use this to pick a skill/flow inside this repository. Before recommending, **open the target skill's `SKILL.md`** and check it (this summary is orientation only).

## Context budget

- Entry: this `SKILL.md` only (≤4KB guide).
- Detail: read [`references/routing-map.md`](routing-map.md) only when needed.
- Phase boundaries: [`PHASE-BOUNDARIES.md`](../PHASE-BOUNDARIES.md).

## Quick routes (wawoo-skills / Cursor)

| Situation | Entry |
|---|---|
| Ship a feature | `@.kilo/commands/feature-delivery.md` |
| Research → decision | `@.kilo/commands/research.md` |
| Huge and foggy | `wayfinder` → the reference on-ramp |
| No issue tracker configured | `setup-matt-pocock-skills` |

## Automatic route (deterministic · MCP)

To pick a workflow from keywords or an explicit `/workflow`, use MCP **instead of reading this skill** (so the agent can call it reliably).

1. `interpret_intent` (JSON) or `route_task` (human-readable text)
2. If `needs_scoring:true`, **read the full input via `upstream_prompt` and score the workflow fit** (no thinking, one JSON line): `{"workflow":"…","score":0.72,"trigger":"…"}`
3. Pass `scoring` back to the same tool to apply it. **Only when `learn:true`** is a score ≥ 0.85 promoted to the DB asynchronously (learn defaults to off).
4. Use the returned `workflow` with `workflow_get`
5. For ambiguous or composite tasks, use this skill and [`references/routing-map.md`](routing-map.md)

The resident receiver is optional. CLI-only: `scripts/task-router.py` or `scripts/wawoo-route.sh`.
