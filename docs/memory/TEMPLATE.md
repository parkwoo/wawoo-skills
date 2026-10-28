# Memory entry template

The minimal format for `memory_save` (MCP) or a manual append. **Append only** (never delete history).

## Structure of one entry (in a topic file)

```markdown
### MEM-YYYYMMDD-NNN

- **Date**: YYYY-MM-DD
- **Kind**: decision | constraint/gotcha | recurring fix | open
- **Body**: what was decided / what to watch for (1–3 sentences)
- **Source**: link to a file, PR, or design doc
- **Alternatives rejected** (optional): options not adopted and why
```

## Reflecting into INDEX.md

- Append `- \`MEM-...\` one-line summary` to the relevant `##` section.
- Add a dated line under `## History`.

## MCP `memory_save` tags

| Form | Meaning |
|------|------|
| `decision` / `constraint` / `gotcha` / `fix` / `open` | kind (INDEX section) |
| `topic:kit` | append detail to `docs/memory/kit.md` |
| `決定,topic:cursor` | a Japanese kind is also allowed |

The `source` argument carries provenance.

## Topic file frontmatter (optional)

```yaml
---
tags: cursor, constraint
---
```

`memory_recall` reads it during recall.

## Do not write

Secrets, keys, personal data, or full long logs (summary + source only).
