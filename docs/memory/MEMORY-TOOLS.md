# Memory tool priority (Kilo / Cursor / MCP)

**Conflict-resolution rules** for when several memory mechanisms are available at once. Detailed steps: `.kilo/skills/memory/SKILL.md`.

## Recall

| Priority | Means | Condition |
|------|------|----------|
| 1 | MCP `memory_recall` | With Cursor / MCP connected. Returns `docs/memory/` in chunks |
| 2 | Read `docs/memory/INDEX.md` | Without MCP, lightweight check |
| 3 | `docs/memory/<topic>.md` | When the topic is known |
| 4 | Kilo `kilo_memory_recall` | When Kilo native is enabled. **On conflict with files, the files win**, and update the Kilo side |

## Save

| Priority | Means | Condition |
|------|------|----------|
| 1 | MCP `memory_save` | Structured append to INDEX + a topic file (recommended) |
| 2 | Manually append `INDEX` / `<topic>.md` | Template: `TEMPLATE.md` |
| 3 | Kilo `kilo_memory_save` | Auxiliary. **Always** mirror the same content into `docs/memory/` (or export) |

## SSOT

In this kit, the **Markdown under `docs/memory/`** is the SSOT. Kilo's built-in memory is only a session aid.

## Ties to the process

- **D7 / P4** (feeding back the retro): keep new constraints, gotchas, and decisions in `memory`.
