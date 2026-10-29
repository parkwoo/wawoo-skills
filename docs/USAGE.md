# Usage (Kilo / Cursor / MCP)

> Japanese version: [USAGE.ja.md](https://github.com/parkwoo/wawoo-skills/blob/master/docs/USAGE.ja.md)

## 0. Prerequisites

- **Python 3 (standard library only)** is required (MCP server, maintenance scripts). **No extra packages.**
- `python3` (or `python` on Windows) must be on `PATH`. Check: `python3 --version`.
  - macOS: `xcode-select --install` if missing. Linux: `apt install python3`, etc. Windows: enable "Add python.exe to PATH" at https://www.python.org/downloads/.
- MCP launches with `python3` as the command (`kilo.json`, `.cursor/mcp.json`). If it has another name (`python` / `py`), align `command`.
- Details: README "Prerequisites (runtime)".

## 1. Contents

- Skills: `.kilo/skills/<name>/SKILL.md`
- Agents: `.kilo/agents/<name>.md`
- Workflows: `.kilo/commands/<name>.md`
- MCP: `mcp/server.py`
- Catalog (generated) — **counts live here** (source of truth): `.kilo/CAPABILITIES.md`

## 2. Kilo CLI / Kilo Code (https://kilo.ai · https://kilocode.ai)

1. Open this directory (auto-discovers `.kilo/`; MCP enabled via `kilo.json`).
2. Workflows: `/feature-delivery`, etc.
3. Skills: the model selects a `SKILL.md`, or reference one explicitly.

### Global install (use in all projects, idempotent)

Mirror `.kilo/{skills,agents,commands}` into `~/.config/kilo/` and idempotently register MCP and an applicability note (re-runnable).
```bash
python3 scripts/install_global.py --dry-run    # preview changes
python3 scripts/install_global.py              # apply (default mirror = delete extras)
python3 scripts/install_global.py --no-delete  # keep extras
KILO_GLOBAL_DIR=/path/to/config python3 scripts/install_global.py  # alternate target
```
- MCP registers absolute paths (`/usr/bin/python3` + `WAWOO_SKILLS_ROOT` / `WAWOO_MEMORY_READONLY`). The default is recall-only (`=1`); use `--memory-writable` (`=0`) to enable writes. See `mcp/README.md`.
- It also **generates `ROUTER.md`**, registers it in `instructions` as an **absolute path** idempotently, and sets `default_agent` to `wawoo-auto` (default).
  - Kilo `instructions` **require absolute paths** (a relative `ROUTER.md` is not injected into the runtime context).
  - The default agent `wawoo-auto` enforces "first tool = `workflow_get` / `interpret_intent`", preventing routing gaps when `code` is the default.
  - Control via `--default-agent <name>` / `--no-default-agent` / `--force-default-agent`.
- **Kilo must be restarted to take effect** (agents/commands/instructions are cached at server start; VS Code: Reload Window).
- Steps that assume the kit's repo-relative SSOT are **valid only inside the kit**. Note this in the global `AGENTS.md`.
- `validate_assets`: a skill/command name collision **does not warn if the command documents its entry** (`design-review`, `research` are handled). An undocumented collision is a `WARN` (`documents_entry` in `scripts/validate_assets.py`).

## 2.5 OpenCode (https://opencode.ai)

OpenCode reads `AGENTS.md` and connects MCP servers over stdio. Add the kit as a local MCP server in `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "wawoo-skills": {
      "type": "local",
      "command": ["python3", "/abs/path/to/wawoo-skills/mcp/server.py"],
      "enabled": true,
      "environment": { "WAWOO_SKILLS_ROOT": "/abs/path/to/wawoo-skills" }
    }
  }
}
```
- OpenCode has no native slash / skill execution; use `AGENTS.md` + MCP (`interpret_intent` → `workflow_get` → `skill_get`).
- Verified by the `opencode_stdio_contract` E2E (MCP handshake + `tools/list`).

## 3. Cursor (https://cursor.com)

1. Open this directory (it reads `AGENTS.md` and `.cursor/rules`).
2. Enable `wawoo-skills` in **Settings → MCP** (`.cursor/mcp.json`).
3. Use the tools `capabilities` / `skill_search` / `skill_get`.

**Cursor limitations**:
- Slash commands (`/feature-delivery`, etc.) **do not work**.
- There is **no agent switching** (read `@.kilo/agents/<role>.md` and apply the role).
- There is **no auto-discovery / auto-start of `SKILL.md`**.

**Fallback (no MCP)**:
```
Look at @.kilo/CAPABILITIES.md, pick a candidate, read the needed @.kilo/skills/<name>/SKILL.md, and follow it.
Apply the steps in @.kilo/commands/<name>.md.
```

## 4. MCP (Model Context Protocol: https://modelcontextprotocol.io)

```bash
python3 mcp/server.py        # stdio (the client usually launches it)
python3 scripts/e2e_flows.py   # public smoke (contract/E2E)
```
**Catalog tools**: `capabilities`, `skill_search`, `skill_get`, `workflow_get`, `agent_get`, `memory_recall`, `memory_save`, `evidence_check`.

**Intent routing** (optional but recommended): `interpret_intent` → `workflow_get` → … → `workflow_clear`. Subtasks: `delegate_subtask`.

- Public guide: **[docs/INTENT-ROUTING.md](INTENT-ROUTING.md)** (L0–L3, score JSON, tool gate)
- Implementation / resident receiver: `mcp/README.md`

## 5. Call order

1. Choose the **Workflow** (entry). For ambiguous requests, use MCP **`interpret_intent`** to pick from the 16 workflows ([INTENT-ROUTING.md](INTENT-ROUTING.md)). When you can be explicit, use **`/delivery-lite`** (`docs/plans/ACTIVE.md` is the progress SSOT). Ceremony levels (L0–L3): see `AGENTS.md` §3 (distinct from the route layers `L0–L3` in `INTENT-ROUTING.md`).
2. Select candidates via the **catalog / MCP** (do not read everything).
3. Open only the **Skills** you need.
4. Follow the workflow's **output schema** and **gates** (approval, evidence).
5. Recall `memory` before work; save decisions after (`memory_save` writes INDEX + a topic file; `docs/memory/TEMPLATE.md`).

### Memory

- SSOT: `docs/memory/` (priority order for Kilo / MCP in `MEMORY-TOOLS.md`)
- Recall/save also at the entry and exit of `/feature-delivery`
- CI: `validate_assets.py` detects secret-like strings in memory
- E2E: `python3 scripts/e2e_flows.py` (**L0–L3**, MCP, workflow). `python3 scripts/cli_adapters_mock.py` (**Kilo/Cursor entry mock**)
- Validation CLIs: `plan_active` / `plan_l2_backlog` / `plan_l3_record` / `plan_content`

## 6. Context budget

- Contract ≤500tok / catalog ≤1k / Workflow ≤1.5k / **one skill ≤2–4KB** / memory top-5.
- Progressive disclosure: do not hand everything at once.
- Budget exceptions: read only the entry `SKILL.md`; details live in each skill's `references/` (e.g. `imagegen-frontend-mobile`, `ask-matt`, `wayfinder`, `design-brief`, `writing-for-agents`).

## 7. Skills needing prerequisites (3)

`to-spec`, `to-tickets`, `triage` need an issue tracker. Run `setup-matt-pocock-skills` once.
Listed in `scripts/readiness.json`.

## 8. Maintenance

```bash
python3 scripts/validate_assets.py
python3 scripts/gen_capabilities.py
python3 scripts/e2e_flows.py
```
Versioning: `docs/VERSIONING.md`.
