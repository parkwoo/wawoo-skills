# wawoo-skills Capability MCP Server

> Japanese version: [README.ja.md](README.ja.md)

Provides skills / agents / workflows / memory / evidence and **intent routing** as MCP tools. A server so the agent does not proceed in prose only but **fixes the entry and permissions through tool calls** (shared by Kilo / Cursor).

- Implementation: `mcp/server.py` (**stdlib only**)
- Transport: **stdio / JSON-RPC 2.0** (newline-delimited)
- Public guide (intent routing): **[docs/INTENT-ROUTING.md](../docs/INTENT-ROUTING.md)**

## Tools

### Catalog & procedures

| Tool | Input | Output |
|------|------|------|
| `capabilities` | `ready_only?` | One-line list of skills / agents / workflows |
| `skill_search` | `query`, `limit?` | Candidates (name / desc / path) |
| `skill_get` | `name` | Full `SKILL.md` |
| `workflow_get` | `name` | Full `.kilo/commands/<name>.md` |
| `agent_get` | `name` | Agent definition |
| `memory_recall` | `query`, `top_k?` | Chunked recall from `docs/memory/` |
| `memory_save` | `text`, `tags?`, `source?` | Append to INDEX + topic (**rejects secrets**) |
| `evidence_check` | `scope: assets` | `validate_assets.py` result |

### Intent routing (L0–L2)

| Tool | Input | Output |
|------|------|------|
| `interpret_intent` | `text`, `scoring?`, `learn?`, `via_receiver?` | JSON (`schedule` or `needs_scoring`) |
| `route_task` | `task` | Human-readable text (`NEEDS SCORING` when awaiting a score) |

Once a `schedule` is fixed, the **MCP tool gate** activates and tools outside `mcp_tools_allow` are rejected (`interpret_intent` / `route_task` / `workflow_clear` / `delegate_subtask` / `steer_task` are always allowed).

### Session & delegation (L3)

| Tool | Input | Output |
|------|------|------|
| `workflow_clear` | — | Release the gate |
| `delegate_subtask` | `subtask`, `label?`, `background?`, `agent?`, `idempotency_key?`, `model_tier?` | L3 delegation JSON (**creates no child session**; the IDE Task / subagent runs it) |
| `steer_task` | `text`, `op?`, `target?` | Amend the running plan (`add`/`reorder`/`reprioritize`/`scope_change`/`abort`). Without `op`, returns `needs_classification` for the host LLM |

### Delegation ownership & abort (L3)

- **Ownership**: a delegated subtask is owned by the call/phase that created it. A **foreground** delegation belongs to the current turn and aborts with it; a **background** delegation (`background: true`) outlives the turn and must be tracked (e.g. board/ACTIVE) and cleaned up.
- **Abort propagation**: aborting the parent aborts its children **bottom-up** (children first). On abort, do not retry side effects unless classified safe; mark partial results **aborted**, not done.
- **Execution**: `delegate_subtask` returns an instruction JSON only; MCP creates no child session. The host (IDE Task) executes it, and the parent **verifies the result** before continuing.
- **Cleanup**: after background work, confirm no orphan processes and record status in ACTIVE/board.

## Recommended flow

1. Decide the workflow with `interpret_intent` (if needed, return a JSON score at L2 and re-call).
2. `workflow_get` → only the `skill_get` you need.
3. Split subtasks → `delegate_subtask` → run in parallel upstream.
4. Finish → `workflow_clear`.

Details: [docs/INTENT-ROUTING.md](../docs/INTENT-ROUTING.md).

## Configuration

**Kilo (project)**

```json
{"mcp":{"wawoo-skills":{"type":"local","command":["python3","mcp/server.py"],"enabled":true}}}
```

**Kilo (global)** — absolute paths recommended

```json
{"mcp":{"wawoo-skills":{
  "type":"local",
  "command":["/usr/bin/python3","/abs/path/wawoo-skills/mcp/server.py"],
  "environment":{"WAWOO_SKILLS_ROOT":"/abs/path/wawoo-skills","WAWOO_MEMORY_READONLY":"1"},
  "enabled":true}}}
```

**Cursor** — `.cursor/mcp.json`

```json
{"mcpServers":{"wawoo-skills":{"command":"python3","args":["/abs/path/wawoo-skills/mcp/server.py"],"env":{"WAWOO_SKILLS_ROOT":"/abs/path/wawoo-skills"}}}}
```

## Environment variables

| Variable | Default | Purpose |
|------|------|------|
| `WAWOO_SKILLS_ROOT` | `server.py`'s grandparent | Base for `.kilo` / `scripts` / `docs` |
| `WAWOO_MEMORY_ROOT` | `<root>/docs/memory` | Target of the memory tools |
| `WAWOO_MEMORY_READONLY` | disabled | `1` rejects `memory_save` (recall-only). `install_global.py --memory-writable` registers `0` to allow writes |
| `WAWOO_INTENT_LEARN_DB` | `data/intent_learned.db` | Learned trigger DB |
| `WAWOO_INTENT_SOCKET` | empty | Resident `intent_receiver.py` (optional) |
| `WAWOO_INTENT_SESSION` | `<root>/data/intent_session.json` | Persisted session file (minimal gate fields; no prompt text) |
| `WAWOO_INTENT_RESUME` | off | `1`/`true` enables resume of the persisted gate after restart (the session file is written only when enabled) |
| `WAWOO_INTENT_CLIENT` | empty | Client name for a per-client file (`intent_session.<client>.json`); avoids cross-client gate bleed |

## Run & test

```bash
python3 mcp/server.py
python3 scripts/e2e_flows.py   # public MCP contract/E2E (unit tests are in internal/tests, non-public)
```

## Security

- `skill_get` / `workflow_get` / `agent_get` are **limited to `.kilo`**.
- `memory_save` is append-only, rejects secret patterns, and can be disabled via `WAWOO_MEMORY_READONLY` (`install_global.py` defaults to `1` = recall-only; `--memory-writable` sets `0`).
- `evidence_check` is `scope=assets` only (no arbitrary shell).
- The workflow gate limits tool damage on a misroute (e.g. an audit workflow cannot `memory_save`).

## Module layout (intent)

| File | Role |
|----------|------|
| `intent_catalog.py` | Workflow ledger, descriptions, `mcp_tools_allow` |
| `intent_commands.py` | L0 slash and command paths |
| `intent_interpreter.py` | L0–L2 orchestration |
| `intent_upstream.py` | Upstream JSON prompt |
| `intent_learned_store.py` / `intent_learn_queue.py` | L1 learning (async writes) |
| `intent_session.py` | B3 MCP gate |
| `intent_delegation.py` | L3 payload |
| `intent_receiver.py` / `intent_client.py` | Resident NDJSON (optional) |
