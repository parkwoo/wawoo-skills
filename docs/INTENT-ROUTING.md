# Intent routing (workflow selection)

> Japanese version: [INTENT-ROUTING.ja.md](INTENT-ROUTING.ja.md)

Choose which of the **16 workflows** (`.kilo/commands/<id>.md`) to run a request through, and allow only the MCP tools you need. **No separate LLM API is required** — the Cursor / Kilo conversation model returns a short JSON score.

This kit is a **standalone generic repository**. It is a separate project from any internal LLM API (e.g. co.taro.bz); the API side references this MCP via `WAWOO_SKILLS_ROOT` only when needed.

- Implementation details: `mcp/README.md`
- MCP tool list: [../mcp/README.md](../mcp/README.md)

---

## 1. When to use

| Use | Can skip |
|------|----------------|
| The request's workflow is ambiguous | You already specify `/delivery-lite` or `/research` up front |
| You want a team to learn the same phrasings | Opening `@.kilo/commands/...` in prose already works |

**Ceremony levels L0–L3** (`AGENTS.md` §3) are separate from this **route layer**. Here, L0 / L1 / L2 / L3 (delegation) mean:

| Layer | Meaning | Example |
|----|------|-----|
| **L0** | User-explicit (slash / command) | `/research 調査して` |
| **L1** | Learned trigger (SQLite) | A phrase learned earlier with a high score |
| **L2** | An upstream LLM assigns workflow fitness | `needs_scoring` → one JSON line |
| **L3** | Subagent delegation during a workflow | `delegate_subtask` (executed by the IDE Task, etc.) |

> **Note:** the `L0–L3` here are **route layers** (how a request is routed). They are a different axis from the **ceremony levels** `L0–L3` in `AGENTS.md` §3 (how much process a task carries). Same letters, different meanings.

---

## 2. Recommended flow (MCP)

```text
interpret_intent(text)
  → schedule (workflow, agent, mcp_tools_allow, command_path)
  → workflow_get(name)
  → skill_get … / memory_recall …
  → (parallel subtasks) delegate_subtask(subtask)
  → workflow_clear()
```

1. **`interpret_intent`** — pass the input. If `needs_scoring: true`, follow the prompt to return one JSON line **with no thinking mode**, and pass `scoring` back to `interpret_intent`.
2. **After `schedule` is fixed** — MCP tools **not allowed** for that workflow are rejected (e.g. `compliance-review` cannot use `memory_save`).
3. **`workflow_get`** — read the command with the same id as `schedule.workflow`.
4. **`delegate_subtask`** — when carving off large work. Execute the returned JSON in a **Cursor Task / Kilo subagent** (MCP creates no child session).
5. **`workflow_clear`** — release the gate. Call it before switching workflows too.

If you only want human-readable text, use **`route_task`** (on `needs_scoring` it shows `NEEDS SCORING` instead of misrouting).

**Amend / steer**: `steer_task {text}` returns an `amend` instruction using the running plan as context. Without `op`, it returns `needs_classification` (the host LLM picks add/reorder/reprioritize/scope_change/abort and re-calls with `op`/`target`). It never writes the plan files itself; the host applies at a step boundary.


---

## 3. `interpret_intent` response (summary)

**Routed**

```json
{
  "ok": true,
  "route_layer": "L0",
  "schedule": {
    "workflow": "research",
    "workflow_slash": "/research",
    "agent": "product-owner",
    "route_layer": "L0",
    "command_path": ".kilo/commands/research.md",
    "workflow_description": "Research and decisions…",
    "mcp_tools_allow": ["capabilities", "skill_get", "…"],
    "delegation_hint": "upstream-subagent"
  }
}
```

**Awaiting score (L2)**

```json
{
  "ok": true,
  "needs_scoring": true,
  "route_layer": "L2",
  "upstream_prompt": "…candidates(id:when)=delivery-lite:…|…",
  "no_thinking": true,
  "workflow_catalog": [{"id": "delivery-lite", "description": "…"}]
}
```

**Upstream JSON contract** (one line, fields only)

```json
{"workflow":"deck","score":0.88,"trigger":"investor deck"}
```

- `learn: true` only on **re-apply** (register a high score to SQLite asynchronously; default `false`).
- `workflow` is one of the 16 ids. Off-ledger values are not learned or adopted.

---

## 3.1 Resolution layers (deterministic → learned → upstream)

`interpret_intent` resolves in the order **L0 slash → L1 learned → L2 upstream score (LLM)**.

- **L0 slash**: `/workflow ...` is adopted immediately as explicit (`route_layer: "L0"`).
- **L1 learned**: adopt a high-confidence substring match from `data/intent_learned.db` (SQLite) (`source: "learned"`). The hand-maintained multilingual **static trigger table is removed** (`TRIGGER_KEYWORDS` / `WEAK_TRIGGERS` are gone).
- **seed**: an empty learned DB is bootstrapped with **catalog (workflow id) seeds**. The legacy vocabulary is migrated into the local learned DB (**not distributed**).
- **L2 upstream score**: if nothing matches, return `needs_scoring: true`; the host LLM adds `workflow`+`score` and re-calls (`source: "upstream"`).
- **Language-independent**: drop vocabulary maintenance and rely on **learned (grows with use) + upstream (LLM)** (multilingual).

## 3.2 Phases (workflow decomposition)

Each workflow is decomposed into **phases**, available via `schedule.phases` and `workflow_get {name, phase:<id>}`.

```json
{"id":"audit","goal":"read-only review","agent":"security-reviewer",
 "skills":["security-review"],"mcp_tools_allow":["skill_get","memory_recall","…"],
 "exit_criteria":["findings and evidence (with severity)"],"parallel_group":"readonly-parallel"}
```

- **P2: per-phase tooling** — `audit` / `research` / `verify` are `readonly-parallel` (parallelizable, read-oriented). Only implementation workflows carry `implement`.
- **Audit workflows have no `implement`** — for `design-review`, `compliance-review`, `release-review`, `self-review`, `schedule.gate` is non-empty; if implementation is needed, **declare a workflow switch**.
- **P3: parallel delegation** — pass independent targets to a subagent via `delegate_subtask {subtask, phase}` with the phase's `exit_criteria` (MCP creates no child session).
- **P4: done criteria** — do not close a phase until `exit_criteria` is met (e.g. `verify` = "0 unconverged FAILED / 0 leftover containers").

---

## 4. Resident receiver (optional)

Instead of launching MCP each time, keep it resident over a socket:

```bash
export WAWOO_INTENT_SOCKET=/tmp/wawoo-intent.sock
python3 mcp/intent_receiver.py --socket "$WAWOO_INTENT_SOCKET"
```

Add `via_receiver: true` to `interpret_intent`. If it is **not running, it errors** (no fallback to local interpretation).

---

## 5. Environment variables

| Variable | Description |
|------|------|
| `WAWOO_SKILLS_ROOT` | Kit root (same as MCP) |
| `WAWOO_INTENT_LEARN_DB` | Learned DB path (default `data/intent_learned.db`) |
| `WAWOO_INTENT_SOCKET` | Unix socket of the resident receiver |
| `WAWOO_INTENT_SESSION` | Persisted session file (minimal gate fields; default `<root>/data/intent_session.json`) |
| `WAWOO_INTENT_RESUME` | `1`/`true` enables resume of the persisted gate after restart (default off; writes only when enabled) |
| `WAWOO_INTENT_CLIENT` | Per-client session file suffix (`intent_session.<client>.json`) to avoid cross-client bleed |

---

## 6. Tests

```bash
python3 scripts/e2e_flows.py   # public E2E (interpret/route, tool gate, L3 included)
# unit tests (test_intent*, test_server) live in internal/tests/ (non-public, maintainers only)
```

---

## 7. Difference from OpenCode / Kilo subagents

| | OpenCode/Kilo | wawoo-skills |
|--|----------------|--------------|
| workflow selection | user mainly selects the agent | L0–L2 + learned triggers |
| parallel subagents | the runtime creates child sessions | **L3 is an instruction JSON only** (the IDE executes) |
| tool restriction | agent permission | **`mcp_tools_allow` gate** |

For skills with heavy parallelism/exploration (e.g. `implement-spec`), the **upstream agent** that receives the L3 JSON is expected to launch Tasks in parallel.

**Delegation ownership**: a subtask is owned by its creating call/phase; abort propagates bottom-up; foreground aborts with the turn, background is tracked and cleaned up. `delegate_subtask` returns an instruction only (the host executes).


---

## 8. Change history

| Date | Content |
|------|------|
| 2026-10-26 | First public guide (L0–L3, MCP gate, delegate) |
| 2026-10-28 | Removed the static trigger table; resolution order = slash → learned (seeded) → upstream. Added `NAME.ja.md` Japanese version |
