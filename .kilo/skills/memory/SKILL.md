---
name: memory
description: Persist and recall durable project knowledge (decisions, constraints, gotchas, recurring fixes) across sessions. Use before starting work and after a decision. File-based so it works in both Kilo and Cursor; use Kilo memory tools when available.
---

# Memory

## Order (recall / save)

Full table: `docs/memory/MEMORY-TOOLS.md`

| Operation | Order |
|-----------|-------|
| **Recall** | 1. MCP `memory_recall` → 2. `INDEX.md` → 3. `<topic>.md` → 4. Kilo recall (on conflict, the file wins) |
| **Save** | 1. MCP `memory_save` → 2. manual append (`TEMPLATE.md`) → 3. Kilo save (syncs to file) |

## Where it lives

- `docs/memory/INDEX.md` — index (one line per section + history)
- `docs/memory/<topic>.md` — per-topic detail (`### MEM-YYYYMMDD-NNN`)
- MCP `memory_save`: appends to **both** (`tags` carries the kind and `topic:name`)

### MCP arguments

- `text` (required): the body
- `tags`: `decision|constraint|gotcha|fix|open` and `topic:name` (e.g. `decision,topic:kit`)
- `source`: provenance (file, PR, URL)

## When to use

- **Before work** (the W of WARO): recall — especially at the entry of `/feature-delivery` and `/self-review`.
- **After a gate, before delivery**: save a new decision, constraint, or gotcha (PROCESS P4 / D7).
- **Recurring failures**: cause and avoidance (observed failure).

## What to save

- Decisions (what, why, alternatives, date), constraints, gotchas, recurring fixes, open questions.
- **Do not save**: secrets, keys, personal data, raw logs.

## How to write

- Use the minimal format in `docs/memory/TEMPLATE.md`.
- Be concise. Always include **provenance**.
- Append on change (never delete history).

## Related

- Handoff: `handoff` / planning: `plan-md` / improvement: `retro`, `pdca-cycle`
- Process: keep decisions/gotchas in `memory` (see `docs/memory/MEMORY-TOOLS.md`)
