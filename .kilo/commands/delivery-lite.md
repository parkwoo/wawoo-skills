---
description: Lightweight delivery — SSOT plan file state machine, minimal ceremony (L0–L1). Default for single-feature requests without full feature-delivery.
agent: implementer
replay: safe
---

# Delivery Lite

**Goal**: analyze the request, track progress in `docs/plans/ACTIVE.md`, and implement through verification. **Do not re-explain the procedure in chat** (AGENTS §3; this workflow is the default).

## Levels

- **L0**: single file, clear fix → implement without updating ACTIVE (only when the user says "L0").
- **L1 (default)**: this workflow. ACTIVE is the SSOT.
- **L2+**: escalate to `/sprint-plan`, an issue tracker, or `/feature-delivery` (when capacity, legal, or production is involved).

## Steps

0. **Get this workflow via MCP**: call `wawoo-skills_workflow_get {name:"delivery-lite"}` and follow the returned steps (treat this file as authoritative only when MCP is unavailable).
1. Read `AGENTS.md` §3 (SSOT) and `docs/plans/ACTIVE.md`. Check `git status` and do not break unrelated changes.
2. **Memory (entry, brief)**: only when the request touches existing constraints, use `memory_recall` or `docs/memory/INDEX.md`.
3. **Plan**: break the request down and add rows to the ACTIVE table (`id`, `todo`, content, done criteria). If complex, create `docs/plans/<id>.md` with `plan-md` and link it from ACTIVE.
4. **Execute**: set the top `todo` to `doing`, one at a time. Use `implement` / `engineering-quality` as needed.
5. **Verify**: relevant tests and lint. For kit changes, run `python3 scripts/validate_assets.py` and `python3 scripts/e2e_flows.py`. After updating ACTIVE, run `python3 scripts/plan_active.py docs/plans/ACTIVE.md` (**Gₑ**: a `done` without evidence fails the CLI).
6. **Complete**: `doing` → `done` with evidence filled in. Set the meta "last updated" to today. Confirm the checks above pass.
7. **Memory (exit)**: save only **new decisions, constraints, or gotchas** with `memory_save` (task-completion logs go only in ACTIVE).
8. **Commit / push / deploy**: only when the user **explicitly asks** (not required per task).

## Output

- Updated `docs/plans/ACTIVE.md` (required)
- A brief summary of changed code and evidence (keep chat short; details live in ACTIVE)

## Gates

- **Gₐ**: stop and get approval for destructive changes, production, external transmission, or contracts.
- **Gₑ**: never claim `done` without evidence.
- **Gₒ**: on failure, record the cause in the ACTIVE row or memory before retrying.
