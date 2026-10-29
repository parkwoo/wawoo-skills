# AGENTS.md — wawoo-skills agent contract

> Japanese version: [AGENTS.ja.md](AGENTS.ja.md)

This repository is a **generic kit** of **reusable skills / agents / workflows / MCP servers** for AI coding agents. It depends on no specific product.

---

## 1. Working language & basics

**Language policy (three tiers)** (authoritative; details in `.kilo/skills/language-policy/SKILL.md`):

| Target | Language |
|------|------|
| Code (comments, identifiers, strings, commit messages, config keys) | **English** |
| **Engineering documents** (`plans/`, `ACTIVE.md`, `RETRO-*`, `evidence/`, `memory/`) and agent **responses** | **Japanese** (the project working language) |
| **Explanatory documents** (`README.md`, `docs/USAGE.md`, etc.) | **Two versions: English (primary) + Japanese (secondary)** |

- Check the current state before changing (`git status`, related files). **Do not discard existing uncommitted changes.**
- **Evidence-based** (distinguish inference from measurement).
- **Memory**: recall `memory` (`docs/memory/INDEX.md`) before work; save decisions and gotchas.

---

## 2. Layout

```
.kilo/
  skills/<name>/SKILL.md   … skills
  agents/<name>.md         … agents
  commands/<name>.md       … workflows
  CAPABILITIES.md          … generated catalog — counts live here (do not hand-edit)
.cursor/
  rules/*.mdc              … Cursor adapters
  mcp.json                 … MCP config
  cli.json.example         … Cursor CLI example
mcp/server.py              … capability MCP server (stdio)
scripts/{gen_capabilities,validate_assets}.py
docs/                      … USAGE, INTENT-ROUTING, VERSIONING, plans, memory
```

---

## 3. Tasks and progress source of truth (SSOT)

**Do not manage progress in chat.** Agents default to the following (the user should not have to say it each time).

| Purpose | SSOT | When to update |
|------|------|----------------|
| **L1 in-progress tasks (code, UI, research, etc.)** | `docs/plans/ACTIVE.md` | Read before starting. The agent updates only `todo`→`doing`→`done` and the evidence column |
| **L1 long-form / books / reports** | `docs/plans/CONTENT.md` | `/content-delivery-lite`. Validated by `plan_content.py` |
| **Detailed plan** | `docs/plans/<id>.md` (`plan-md`) | When the breakdown is large. Link from the ACTIVE id |
| **L2 multiple tasks / sync** | issue tracker (if configured) or `docs/plans/BACKLOG*.md` | `to-tickets` / `plan_l2_backlog.py`. Do not double-manage with ACTIVE |
| **L3 process improvement** | `docs/plans/RETRO*.md` etc. + `memory` | `/self-improve`. `plan_l3_record.py` |
| **Cross-cutting decisions / constraints** | `docs/memory/` | Not for task completion — only recurring knowledge |
| **Audit (kit assets)** | CI / `validate_assets.py` | Run it instead of saying "I audited" in words |

**Ceremony levels (L0–L3)**: the table above (a different axis from the **route layers** `L0–L3` in `docs/INTENT-ROUTING.md`). When unsure, **L1 + `/delivery-lite`**. Production, legal, and large work go to `/feature-delivery` or L2.

**git commit**: only when the user asks (a task being `done` and a commit are separate).

---

## 4. Invocation protocol (required)

Theory and design decisions: the required contract is in this file; extended design notes (Skill/Agent/Workflow division, WARO) are maintainer-internal (`internal/`, not in public clones).

**Kilo practice (mandatory, rule 0)**: In an environment with the MCP `wawoo-skills` connected, for **non-trivial requests** (code change, research, design, document generation), **make the first tool call `wawoo-skills_workflow_get`** (or `wawoo-skills_interpret_intent` if undecidable). If you started work using the native `skill` tool (e.g. `plan-md`) or memory instead, treat it as a §4 violation and return to `workflow_get` even mid-task. Use native tools only when MCP is unavailable, and report that.

1. **Entry = Workflow**: usually **`/delivery-lite`** (ceremony L1). For large, gate-heavy work, `/feature-delivery`. Kilo uses `/name`; Cursor uses `@.kilo/commands/<name>.md`. When the request is ambiguous, use MCP **`interpret_intent`** → `schedule.workflow` (`docs/INTENT-ROUTING.md`). If `interpret_intent` returns `needs_scoring`, re-call it with `scoring`.
2. **Candidate selection = catalog / MCP**: `.kilo/CAPABILITIES.md` or MCP `capabilities` / `skill_search`. **Do not read everything.** After `interpret_intent`, **do not call tools outside `mcp_tools_allow`** (`workflow_clear` at the end).
3. **Steps = Skill**: open only the skills the workflow names, via `skill_get` / `@.kilo/skills/<name>/SKILL.md`. When phases exist, get goal/agent/skills/`exit_criteria` via `workflow_get {name, phase:<id>}`; for a workflow without `implement` (audit-type), do not proceed to implementation — **declare the switch**.
4. **Output = schema**: follow the workflow's output shape. Do not skip gates (approval, evidence, observed failure).
5. **Memory**: before work, `memory_recall` (or `docs/memory/INDEX.md`); save decisions, constraints, and gotchas with `memory_save` (INDEX + `docs/memory/<topic>.md`). Priority: `docs/memory/MEMORY-TOOLS.md`.
6. **Verify**: `python3 scripts/validate_assets.py` + lint/tests.

### 4.1 Execution hygiene and convergence gates (kit-wide, product-independent)

These apply to **this kit itself** and to any project adopting the kit's conventions (independent of any product).

- **1 session = 1 target / 1 artifact**: do not mix independent projects or multiple artifacts in one session. If they would mix, split by target with `Task` (subagent). **Metric: payload < 600KB, halve cache_read.**
- **Declare workflow deviation**: when switching workflows mid-way, **declare the reason and the new workflow in one line** and separate the artifacts (e.g. do not mix audit and implementation). Record it in `plan-md` / ACTIVE. **Metric: 1 session, 1 artifact.**
- **Failure convergence gate**: a failed test must be either **fixed** or **recorded explicitly as a known failure + tracked** (ticket / ACTIVE row). Do not report completion with an unconverged `FAILED`. **Metric: unconverged FAILED = 0.**
- **Fixed cleanup**: after tests or a run, stop containers/processes and confirm none remain (e.g. `docker compose ... down -v` and `docker ps`). **Metric: leftovers = 0.**
- **Save memory**: record decisions, constraints, and gotchas at completion (in the kit, `memory_save`; otherwise the project's store) — **at least one**. Task-completion logs go only to the SSOT.
- **Token hygiene**: avoid huge `cat` and full loops; read only the needed lines with `grep -n`/`head`/`sed -n`. `/compact` long sessions. **Metric: one step's tool output < 4KB.**
- **Subagent delegation efficiency**: when delegating an audit via `Task`, **inline the key points of the needed skills in the task text** and do not let the child re-fetch the same skill with `skill_get`. A read-only subagent restricts `read` to a line range (≤200 lines) and does not use `background_process` (a one-off command is a single shell call). **Metric: 0 duplicate `skill_get` per delegation chain, p95 read < 4KB.**
- **Delegation ownership & abort**: a delegated subtask is owned by its creating call/phase; foreground aborts with the turn, background outlives it (track + clean up); abort propagates bottom-up; `delegate_subtask` returns an instruction only (the host executes), and the parent verifies the result before continuing.
- **Local verification**: before a PR / publish, run `python3 scripts/validate_assets.py` and (when applicable) `python3 scripts/e2e_flows.py` **locally and keep the results** (a fallback when CI is unavailable).
- **Board as a multiplayer view**: the board is committed state + deltas. A late joiner reads the current view first, then uses `since` cursors for deltas; post only material updates (not routine progress).
- **Replay safety**: each command declares `replay: safe|unsafe`. For `unsafe` steps (irreversible or external effects: deploy/publish/production/delete), pass an `idempotency_key` to `delegate_subtask` (and steering) so a retry after interruption does not duplicate the effect; re-run only `safe` steps automatically.
- **Model tiers**: route mechanical steps to a fast/cheap model and planning/verification to a reasoning model; pass `model_tier: fast|reasoning` to `delegate_subtask` when delegating. Do not spend a reasoning model on mechanical edits.

---

## 5. Context budget (how to hand things to the model)

- Contract ≤500tok / catalog ≤1k / Workflow ≤1.5k / **one skill ≤2–4KB** (exceptions exist) / memory top-5.
- **Budget guide (§4.1)**: one step's tool output **< 4KB**; one session's payload **< 600KB**. If you would exceed it, split the target / `/compact` / switch to `grep -n`/`head`.
- **Progressive disclosure**: do not hand everything at once. Read references only when needed.
- **Budget exceptions** (read only the entry `SKILL.md`; details in `references/`): `imagegen-frontend-mobile`, `ask-matt`, `wayfinder`, `design-brief`, `writing-for-agents`, `teach`.
- Large tool results: **summary + ID**. Do not leave contradictions (one SSOT).
- **Proactive compaction**: compact at a natural boundary before the budget forces it; write a handoff/memory note so the summary is durable, and keep prior history searchable (do not rely on deleting it).

---

## 6. Per tool

- **Kilo**: auto-discovers `.kilo/` (skills/agents/commands) + `kilo.json`. **Native launch available.**
- **Cursor**: `AGENTS.md` + `.cursor/rules` + **MCP** + `@file`. **No native execution of slash command / agent / SKILL.**
- **OpenCode**: `AGENTS.md` + **MCP** (`opencode.json`). **No native execution of slash / SKILL**; use `interpret_intent` → `workflow_get` → `skill_get`.
- Details: `docs/USAGE.md`.

---

## 7. Readiness

- External prerequisites: listed in `scripts/readiness.json` (e.g. issue tracker).
- `to-spec`/`to-tickets`/`triage` need an issue tracker. If unset, keep them off the standard flow. Excludable via MCP `capabilities {ready_only:true}`.
- Details: `scripts/readiness.json`.

---

## 8. Adding and updating skills

- When adding: require `name` / `description` in `.kilo/skills/<name>/SKILL.md`.
- Regenerate the catalog: `python3 scripts/gen_capabilities.py` (**do not hand-edit**).
- Validate: `python3 scripts/validate_assets.py` (name=dir, refs, dup, JSON).
- Do not break agent and command references (`agent:`).

---

## 9. Guardrails

- **Do not commit** secrets (API keys, tokens). `memory_save` rejects secrets.
- Destructive changes, production, external transmission, and publishing **require approval**.
- Licenses: respect the bundled `LICENSES/` and `.kilo/skills/ATTRIBUTION.md`. Do not redistribute **unverified-license third-party assets**.
- Keep evidence (commands, results) and state what is unverified.

---

## 10. Versioning

- **`VERSION`** (repo root) is the single SSOT. **SemVer** (`MAJOR.MINOR.PATCH`).
- On change, update **`CHANGELOG.md`** and bump `VERSION`.
  - Deletions, renames, breaking MCP tool changes = **MAJOR**
  - Adding skills/agents/commands, backward-compatible additions = **MINOR**
  - Typos, wording, internal refactors = **PATCH**
- Tag `v<version>` at release (e.g. `v0.1.0`).
- Details: `docs/VERSIONING.md`.

---

## 11. Change history

| Date | Content |
|---|---|
| 2026-10-25 | First version as a generic kit (extracted and generalized from an existing project) |
| 2026-10-25 | §3 SSOT (ACTIVE, L0–L3), default entry `/delivery-lite` |
| 2026-10-26 | §4 `interpret_intent`, tool gate, `docs/INTENT-ROUTING.md` |
| 2026-10-27 | §4 mandates MCP-first (`workflow_get` / `interpret_intent`). Fixed: Kilo `instructions` require absolute paths (a relative `ROUTER.md` is not injected) |
| 2026-10-27 | Added `## Routing (MCP first)` to all agent definitions (21) |
| 2026-10-27 | New default agent `wawoo-auto` (`default_agent`). `install_global.py` idempotently generates `ROUTER.md`, registers absolute `instructions`, and sets `default_agent` |
| 2026-10-28 | Added §4.1 "execution hygiene and convergence gates" |
| 2026-10-28 | Added an **L1 trigger classifier** to intent routing; decomposed workflows into **phases** |
| 2026-10-28 | Log-analysis improvements (§4.1 subagent delegation efficiency, read-only subagent efficiency, `security-reviewer` read-only bash subset, `memory_save` availability in `capabilities`, `self-improve` triggers, `scripts/kilo_snapshot_gc.sh`) |
| 2026-10-28 | 3-tier language policy (§1); removed static routing triggers → learned + upstream; publication boundary as a skill + check; tests moved to non-public `internal/tests/`; public assets Englishized |
| 2026-10-29 | Reduced the public surface (process/design docs → non-public); source of truth = a private repo that generates the public repo via a publish allowlist. Docs re-synced to code (layout, change history) |
