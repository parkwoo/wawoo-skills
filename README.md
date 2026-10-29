# wawoo-skills

**Your agent has the skills. It just doesn't use them.**

> **Invocation by design.** A generic kit of reusable **skills / agents / workflows / MCP servers** for AI coding agents — so the same request takes the same steps, every time.

> Japanese version: [README.ja.md](README.ja.md)

## Why this kit

Even with skill and role (agent) definitions available, agents often **proceed in prose only — not reading, choosing, or following the steps**. Quality then varies for the same task, gates (review, legal, tests) become hollow, and the knowledge a team prepared goes unused.

wawoo-skills addresses this "**the capability exists but is never invoked**" problem by **designing the invocation**:

| Layer | Role |
|---|---|
| **Contract** (`AGENTS.md`, Cursor rules) | Fix what to read first and what may not be skipped |
| **Workflows** (`.kilo/commands`) | Process entry points. State which skills to use, in what order |
| **Catalog / MCP** | Never pass every skill at once; select candidates → fetch only what you need (progressive disclosure) |
| **Intent routing** | Select the workflow with `interpret_intent`, learn triggers, gate tool permissions ([docs/INTENT-ROUTING.md](docs/INTENT-ROUTING.md)) |
| **Gates** | Approval, evidence, observed failure. Never call it "done" on inference alone |

It lays **rails of reproducible steps and tool calls** — it does not take away the agent's creativity.

## Capabilities

- **Intent routing** — `interpret_intent` selects the workflow (explicit `/name` → **learned** SQLite → **upstream** LLM score; no static keyword table) and **gates which MCP tools** each workflow may call.
- **Phases & gates** — every workflow decomposes into **phases** (`goal`, `agent`, `skills`, `mcp_tools_allow`, `exit_criteria`); **audit workflows are read-only** (no `implement`).
- **Dynamic steering** — `steer_task` amends a running plan (add / reorder / reprioritize / scope_change / abort) at a step boundary.
- **Delegation** — `delegate_subtask` carves off parallel, read-only subtasks and can target a **model tier** (`fast` or `reasoning`).
- **Gates** — approval (Gₐ), evidence (Gₑ), observed failure (Gₒ): never "done" on inference alone.
- **Progressive disclosure** — catalog → candidates → open only the skills you need (bounded context).
- **Memory** — `memory_recall` / `memory_save` (secrets rejected).

## What changes (2 minutes)

**Before — no routing.** You say "fix this bug". The agent improvises, skips the gates, and the next identical request takes a different path.

**After — routed.** The request enters `/self-review`; the agent opens `test-engineering`, reaches the evidence gate (Gₑ) with a reproduction, and the next identical request follows the same chain.

## Who this is for

| This is for you if… | This is **not** for you if… |
|---|---|
| You use Kilo / Cursor and have skills + agents, but they are **never invoked** | You only want one-off code generation |
| You want the same request to take the same steps every time | You value free improvisation over process |
| Your team needs review / legal / test **gates** you can actually run | You don't need gates or evidence |
| You want team knowledge **used by the agent**, not parked in a wiki | — |

## Supported environments

- **Kilo CLI / Kilo Code**: discovery of `.kilo/`, slash workflows (`/feature-delivery`, etc.), MCP via `kilo.json`.
- **Cursor**: `AGENTS.md`, `.cursor/rules`, MCP, and references via `@.kilo/commands` / `@.kilo/skills` (no slash or native agent switching; the same steps apply).
- **OpenCode**: `AGENTS.md` + MCP via `opencode.json` (no native slash/skill execution; use `interpret_intent` → `workflow_get` → `skill_get`).

### Prerequisites (runtime)

The kit's **MCP server and maintenance scripts run on Python 3 (standard library only)**. No extra packages are needed, but a **`python3` on `PATH` (or `python` on Windows) is required**.

| OS | Extra step |
|---|---|
| macOS | Usually none (otherwise `xcode-select --install`, or https://www.python.org/downloads/) |
| Linux | Usually none (otherwise `apt install python3`, etc.) |
| Windows | Install from https://www.python.org/downloads/ and enable **"Add python.exe to PATH"** (Microsoft Store version works too) |

- Check: `python3 --version` (Windows: `python --version`) returns `3.x` → OK.
- MCP launches with `python3` as the command (`kilo.json`, `.cursor/mcp.json`). If `python3` has another name, set each config's `command` to the real binary (`python` / `py`, etc.; a global install registers an **absolute path** via `install_global.py`).
- No extra dependencies, network, or `.env` are needed (`stdio` only).

## Supported tools (official)

| Tool | Official name | Official URL |
|---|---|---|
| Kilo CLI | Kilo (CLI) | https://kilo.ai |
| Kilo Code | Kilo Code (VS Code extension) | https://kilocode.ai |
| Cursor | Cursor | https://cursor.com |
| OpenCode | OpenCode | https://opencode.ai |
| MCP | Model Context Protocol | https://modelcontextprotocol.io |
| AGENTS.md | AGENTS.md | https://agents.md |

## Contents

| Kind | Location |
|---|---|
| Skills | `.kilo/skills/<name>/SKILL.md` |
| Agents | `.kilo/agents/<name>.md` |
| Workflows | `.kilo/commands/<name>.md` (code L1: `/delivery-lite`, knowledge L1: `/content-delivery-lite`) |
| MCP server | `mcp/server.py` (stdio, stdlib only) |
| Cursor rules | `.cursor/rules/*.mdc` |

- Catalog (generated) — **counts live here** (source of truth): `.kilo/CAPABILITIES.md`
- Readiness (external prerequisites): `scripts/readiness.json`
- Invocation & context design: `docs/USAGE.md`
- Intent routing (public): `docs/INTENT-ROUTING.md`

## Quick start

### Kilo
```bash
# Open this directory (it discovers .kilo/; MCP is enabled by kilo.json)
```
- Workflows: `/feature-delivery`, etc.
- Skills: `/` or the model selects a `SKILL.md`

**First 10 minutes** (a small win up front):
1. Send one sentence to `interpret_intent` and read the workflow it returns.
2. Run `/delivery-lite` once — `docs/plans/ACTIVE.md` advances one row.
3. `python3 scripts/validate_assets.py` → `OK: skills=… agents=… commands=…` means you're set.

### Cursor
1. Open this directory (it reads `AGENTS.md` and `.cursor/rules`)
2. Enable `wawoo-skills` in **Settings → MCP** (`.cursor/mcp.json`)
3. Use MCP `interpret_intent` (entry selection) → `workflow_get` / `skill_get`, etc. ([INTENT-ROUTING.md](docs/INTENT-ROUTING.md))
- **No slash command / agent support.** Open `@.kilo/commands/<name>.md` and apply the steps.
- Details: `docs/USAGE.md`

### MCP
```bash
python3 mcp/server.py        # stdio (the client usually launches it)
python3 scripts/e2e_flows.py   # public smoke (contract/E2E)
```

## Maintenance

```bash
python3 scripts/validate_assets.py   # asset validation (name=dir, refs, dup, JSON)
python3 scripts/gen_capabilities.py  # regenerate the catalog (do not hand-edit)
python3 scripts/e2e_flows.py           # MCP contract smoke
```

## Directory

```
.kilo/{skills,agents,commands,CAPABILITIES.md}
.cursor/{rules,mcp.json}
mcp/{server.py,intent_*.py,README.md}
scripts/{gen_capabilities.py,validate_assets.py,readiness.json,…}
docs/{USAGE.md,INTENT-ROUTING.md,VERSIONING.md,memory,plans}
LICENSES/
AGENTS.md
kilo.json
```

## License and attribution (plain explanation)

This repository mixes **what we wrote** with **what others published**.

| Kind | License | Location |
|---|---|---|
| Skills / agents / commands / MCP newly written here | **MIT** (free to use; keep the copyright notice) | `LICENSE` |
| Skills derived from Skills For Real Engineers (25) | **MIT** | `LICENSES/skills-for-real-engineers-MIT.txt` |
| Skills derived from OpenDesign (10) | **Apache-2.0** (keep the copyright notice and NOTICE) | `LICENSES/open-design-Apache-2.0.txt` |
| Agents derived from Kilo Marketplace (6) | **Apache-2.0** | `LICENSES/kilo-marketplace-*` |
| Others (Kilo built-in skills, etc.) | Per-file frontmatter / MIT | `.kilo/skills/ATTRIBUTION.md` |

- `.kilo/skills/ATTRIBUTION.md` lists which file comes from where.
- **We exclude anything whose license is unverified** (the 3 Marketplace "business" items are excluded). `fal-gen` is a skill **we wrote ourselves** (MIT) — see `.kilo/skills/ATTRIBUTION.md`.
- No warranty (**AS IS**). Verify each license as needed before use.

### Sources (official)

| Source | Official URL |
|---|---|
| Skills For Real Engineers (Matt Pocock) | https://github.com/mattpocock/skills · https://skills.sh/mattpocock/skills |
| OpenDesign | https://open-design.ai · https://github.com/nexu-io/open-design |
| Kilo Marketplace (Kilo ecosystem) | https://kilo.ai |
| Semantic Versioning | https://semver.org |

## Cautions (read first)

- **Image generation is not bundled**: `imagegen-frontend-mobile` provides **prompts only** (what to generate). Actual generation uses OpenAI Images / fal / an internal tool separately. If none is available, deliver **prompts only**.
- **3 skills need an issue tracker**: `to-spec`, `to-tickets`, `triage` assume a tracker such as GitHub Issues. Run `setup-matt-pocock-skills` once to configure it.
- **Never write secrets**: do not commit API keys, tokens, or `.env` contents. `memory_save` rejects secrets.
- **Cursor has no slash command / agent support**: use `AGENTS.md` + `.cursor/rules` + MCP + `@file` (`docs/USAGE.md`).

## Version

- Current: **0.6.0** (`VERSION`)
- Change history: `CHANGELOG.md` (**a Japanese project record**, per the language policy in `AGENTS.md` §1)
- Versioning and release steps: `docs/VERSIONING.md`
