#!/usr/bin/env python3
"""this project capability MCP server (stdio, stdlib only).

Exposes skills/agents/workflows/memory/evidence as MCP tools so that agents
(Kilo and Cursor) invoke them via tool calls instead of relying on prose.

Transport: newline-delimited JSON-RPC 2.0 over stdio.
Tools:
  capabilities, skill_search, skill_get, workflow_get, agent_get,
  memory_recall, memory_save, evidence_check,
  interpret_intent, route_task, workflow_clear, delegate_subtask
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path


def _env_path(name: str, default: Path) -> Path:
    value = os.environ.get(name, "").strip()
    return Path(value).expanduser() if value else default


def _env_flag(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


# In a global install the real paths can change, so allow an env override.
# WAWOO_SKILLS_ROOT: kit root (base for .kilo/scripts/docs)
# WAWOO_MEMORY_ROOT: alternate path for docs/memory
# WAWOO_MEMORY_READONLY: 1/true disables memory_save (prevents cross-boundary writes)
ROOT = _env_path("WAWOO_SKILLS_ROOT", Path(__file__).resolve().parents[1])
KILO = ROOT / ".kilo"
MEMORY = _env_path("WAWOO_MEMORY_ROOT", ROOT / "docs" / "memory")
MEMORY_READONLY = _env_flag("WAWOO_MEMORY_READONLY")
PROTOCOL = "2024-11-05"
SERVER = {"name": "wawoo-skills-capabilities", "version": "0.4.0"}

sys.path.insert(0, str(Path(__file__).resolve().parent))
from intent_client import socket_path, submit_intent  # noqa: E402
from intent_delegation import build_delegation_payload, format_delegation_text  # noqa: E402
from intent_steer import build_steer_payload  # noqa: E402
from intent_catalog import phase_dicts  # noqa: E402
from intent_interpreter import (  # noqa: E402
    format_needs_scoring_text,
    format_route_task_text,
    interpret_intent_payload,
)
from intent_session import activate_schedule, active_schedule, check_tool_allowed, clear_schedule  # noqa: E402
from memory_ops import recall_memory, save_memory  # noqa: E402


def load_readiness() -> dict[str, str]:
    try:
        data = json.loads((ROOT / "scripts" / "readiness.json").read_text(encoding="utf-8"))
        return {str(k): str(v) for k, v in (data.get("needs_setup") or {}).items()}
    except Exception:
        return {}


NEEDS_SETUP = load_readiness()


def mark(name: str, base: str) -> str:
    if name.lstrip("/") in NEEDS_SETUP:
        return f"{base} [SETUP: {NEEDS_SETUP[name.lstrip('/')]}]"
    return base


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    out: dict[str, str] = {}
    key = None
    buf: list[str] = []
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            if key:
                out[key] = " ".join(buf).strip()
            key, val = m.group(1), m.group(2).strip()
            buf = [] if (val == "" or val[0] in "|>") else [val]
        elif key and line.startswith((" ", "\t")):
            buf.append(line.strip())
    if key:
        out[key] = " ".join(buf).strip()
    return out


def one_line(s: str, n: int = 200) -> str:
    s = re.sub(r"\s+", " ", s or "").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


class Catalog:
    def __init__(self) -> None:
        self.skills: dict[str, Path] = {}
        self.agents: dict[str, Path] = {}
        self.commands: dict[str, Path] = {}
        self.meta: dict[str, dict[str, str]] = {}
        for p in sorted((KILO / "skills").glob("*/SKILL.md")):
            fm = frontmatter(p)
            name = fm.get("name") or p.parent.name
            self.skills[name] = p
            self.meta[name] = fm
        for p in sorted((KILO / "agents").glob("*.md")):
            fm = frontmatter(p)
            self.agents[p.stem] = p
            self.meta[p.stem] = fm
        for p in sorted((KILO / "commands").glob("*.md")):
            if p.stem == "README":
                continue
            self.commands[p.stem] = p
            self.meta[p.stem] = frontmatter(p)

    def rows(self) -> list[dict]:
        rows = []
        for name, p in self.skills.items():
            rows.append({"kind": "skill", "name": name, "description": one_line(self.meta[name].get("description", "")), "path": str(p.relative_to(ROOT))})
        for name, p in self.agents.items():
            rows.append({"kind": "agent", "name": name, "description": one_line(self.meta[name].get("description", "")), "path": str(p.relative_to(ROOT))})
        for name, p in self.commands.items():
            rows.append({"kind": "workflow", "name": "/" + name, "description": one_line(self.meta[name].get("description", "")), "path": str(p.relative_to(ROOT))})
        return rows


CAT = Catalog()


def tool_result(text: str, is_error: bool = False) -> dict:
    return {"content": [{"type": "text", "text": text}], "isError": is_error}


def safe_read(path: Path) -> str:
    rp = path.resolve()
    if not rp.is_relative_to(KILO.resolve()):
        raise ValueError("path outside .kilo")
    return rp.read_text(encoding="utf-8", errors="ignore")


def do_capabilities(args: dict) -> dict:
    ready_only = bool(args.get("ready_only"))
    lines = []
    if MEMORY_READONLY:
        # Cross-boundary-write prevention mode. The agent must not call memory_save (disabled).
        lines.append("! memory_save: disabled (WAWOO_MEMORY_READONLY) — recall-only; do not call memory_save")
    for r in CAT.rows():
        if ready_only and r["name"].lstrip("/") in NEEDS_SETUP:
            continue
        lines.append(mark(r["name"], f"{r['kind']:8} {r['name']:32} {r['description']}"))
    return tool_result("\n".join(lines) if lines else "no capabilities")


def do_skill_search(args: dict) -> dict:
    q = str(args.get("query", "")).lower().strip()
    terms = [t for t in re.split(r"\W+", q) if t]
    scored = []
    for r in CAT.rows():
        hay = (r["name"] + " " + r["description"]).lower()
        score = sum(1 for t in terms if t in hay)
        if not terms or score:
            scored.append((score, r))
    scored.sort(key=lambda x: (-x[0], x[1]["name"]))
    out = [
        mark(r["name"], f"{r['kind']:8} {r['name']:32} {r['description']}  [{r['path']}]")
        for _, r in scored[: int(args.get("limit", 20))]
    ]
    return tool_result("\n".join(out) if out else "no matches")


def do_skill_get(args: dict) -> dict:
    name = str(args.get("name", ""))
    p = CAT.skills.get(name)
    if not p:
        return tool_result(f"unknown skill: {name}", True)
    return tool_result(safe_read(p))


def do_workflow_get(args: dict) -> dict:
    name = str(args.get("name", "")).lstrip("/")
    p = CAT.commands.get(name)
    if not p:
        return tool_result(f"unknown workflow: {name}", True)
    phase_id = str(args.get("phase", "")).strip()
    if phase_id:
        match = next((ph for ph in phase_dicts(name) if ph["id"] == phase_id), None)
        if not match:
            ids = ",".join(ph["id"] for ph in phase_dicts(name))
            return tool_result(f"unknown phase '{phase_id}' for workflow '{name}' (phases: {ids})", True)
        return tool_result(json.dumps(match, ensure_ascii=False, indent=2))
    return tool_result(safe_read(p))


def do_agent_get(args: dict) -> dict:
    name = str(args.get("name", ""))
    p = CAT.agents.get(name)
    if not p:
        return tool_result(f"unknown agent: {name}", True)
    return tool_result(safe_read(p))


def do_memory_recall(args: dict) -> dict:
    q = str(args.get("query", ""))
    top_k = int(args.get("top_k", 5))
    return tool_result(recall_memory(MEMORY, q, top_k))


def do_memory_save(args: dict) -> dict:
    if MEMORY_READONLY:
        return tool_result(
            "memory_save disabled (WAWOO_MEMORY_READONLY): this deployment is recall-only",
            True,
        )
    text = str(args.get("text", "")).strip()
    tags = str(args.get("tags", "")).strip()
    source = str(args.get("source", "")).strip()
    if not text:
        return tool_result("empty text", True)
    try:
        msg = save_memory(MEMORY, text, tags, source)
    except ValueError as exc:
        return tool_result(str(exc), True)
    return tool_result(msg)


def do_evidence_check(args: dict) -> dict:
    scope = str(args.get("scope", "assets"))
    if scope != "assets":
        return tool_result("only scope=assets is supported (no arbitrary commands)", True)
    try:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_assets.py")],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=60,
        )
    except Exception as exc:  # pragma: no cover
        return tool_result(f"failed to run validation: {exc}", True)
    out = (proc.stdout or "") + (proc.stderr or "")
    return tool_result(out.strip() or f"exit={proc.returncode}", proc.returncode != 0)


def do_interpret_intent(args: dict) -> dict:
    """Intent interpretation — structured JSON. With via_receiver=true and WAWOO_INTENT_SOCKET set, routes to the resident receiver."""
    task = str(args.get("text", args.get("task", ""))).strip()
    if not task:
        return tool_result("text or task is required", True)
    via = args.get("via_receiver") is True or str(args.get("via_receiver", "")).lower() in {"1", "true", "yes"}
    if via and socket_path():
        try:
            resp = submit_intent(task, intent_id=str(args.get("id", "")).strip())
            return tool_result(json.dumps(resp, ensure_ascii=False, separators=(",", ":")))
        except Exception as exc:
            return tool_result(f"intent receiver error: {exc}", True)
    learn = args.get("learn") is True or str(args.get("learn", "")).lower() in {"1", "true", "yes"}
    scoring = args.get("scoring") if isinstance(args.get("scoring"), dict) else None
    classification = args.get("classification") if isinstance(args.get("classification"), dict) else None
    if scoring is None and classification is None and args.get("workflow"):
        scoring = {
            "workflow": args.get("workflow"),
            "score": args.get("score"),
            "trigger": args.get("trigger"),
        }
    payload = interpret_intent_payload(
        task,
        intent_id=str(args.get("id", "")).strip(),
        learn=learn,
        classification=classification,
        scoring=scoring,
    )
    if payload.get("ok") and payload.get("schedule") and not payload.get("needs_scoring"):
        activate_schedule(payload["schedule"])
    out = {"local": True, **payload}
    return tool_result(json.dumps(out, ensure_ascii=False, separators=(",", ":")))


def do_workflow_clear(_args: dict) -> dict:
    clear_schedule()
    return tool_result("workflow session cleared (MCP tool gate open)")


def do_delegate_subtask(args: dict) -> dict:
    """L3: return a subagent delegation instruction under the parent workflow session (executed upstream)."""
    parent = active_schedule()
    if not parent:
        return tool_result("no active workflow session: call interpret_intent with a resolved schedule first", True)
    subtask = str(args.get("subtask", args.get("prompt", ""))).strip()
    phase_id = str(args.get("phase", "")).strip()
    suggested_agent = str(args.get("agent", "")).strip()
    if phase_id:
        ph = next((x for x in phase_dicts(str(parent.get("workflow", ""))) if x["id"] == phase_id), None)
        if not ph:
            ids = ",".join(x["id"] for x in phase_dicts(str(parent.get("workflow", ""))))
            return tool_result(f"unknown phase '{phase_id}' for workflow '{parent.get('workflow', '?')}' (phases: {ids})", True)
        criteria = "; ".join(str(c) for c in ph.get("exit_criteria", []))
        subtask = f"[phase:{phase_id}] {ph.get('goal', '')}\nsubtask: {subtask}\nexit_criteria: {criteria}"
        suggested_agent = suggested_agent or str(ph.get("agent", ""))
    try:
        payload = build_delegation_payload(
            parent,
            subtask=subtask,
            label=str(args.get("label", "")).strip(),
            background=bool(args.get("background")),
            suggested_agent=suggested_agent,
            idempotency_key=str(args.get("idempotency_key", "")).strip(),
            model_tier=str(args.get("model_tier", "")).strip(),
        )
    except ValueError as exc:
        return tool_result(str(exc), True)
    return tool_result(format_delegation_text(payload))



def do_steer_task(args: dict) -> dict:
    """Amend a running plan: classify (or apply) an op against the plan context."""
    text = str(args.get("text", "")).strip()
    parent = active_schedule() or {}
    try:
        payload = build_steer_payload(
            text=text,
            root=ROOT,
            active_workflow=str(parent.get("workflow", "")),
            op=str(args.get("op", "")),
            target=str(args.get("target", "")),
        )
    except ValueError as exc:
        return tool_result(str(exc), True)
    return tool_result(json.dumps(payload, ensure_ascii=False, indent=2))

def do_route_task(args: dict) -> dict:
    """task-router-compatible human-readable text (does not fall back to delivery-lite on needs_scoring)."""
    task = str(args.get("task", "")).strip()
    if not task:
        return tool_result("Task is required. Please provide a task description.", True)
    payload = interpret_intent_payload(task)
    if not payload.get("ok"):
        return tool_result(str(payload.get("error", "interpret failed")), True)
    if payload.get("needs_scoring"):
        return tool_result(format_needs_scoring_text(payload))
    from intent_interpreter import IntentSchedule

    schedule = IntentSchedule(**payload["schedule"])
    activate_schedule(payload["schedule"])
    return tool_result(format_route_task_text(schedule))


TOOLS = [
    ("capabilities", "List skills/agents/workflows with one-line descriptions.", {"type": "object", "properties": {"ready_only": {"type": "boolean"}}}),
    ("skill_search", "Search skills/agents/workflows by query.", {"type": "object", "properties": {"query": {"type": "string"}, "limit": {"type": "integer"}}, "required": ["query"]}),
    ("skill_get", "Get the full SKILL.md for a skill name.", {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}),
    ("workflow_get", "Get the full command/workflow by name. Pass phase=<id> to get one phase (goal, agent, skills, mcp_tools_allow, exit_criteria).", {"type": "object", "properties": {"name": {"type": "string"}, "phase": {"type": "string"}}, "required": ["name"]}),
    ("agent_get", "Get an agent definition by name.", {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}),
    ("memory_recall", "Recall relevant memory entries from docs/memory.", {"type": "object", "properties": {"query": {"type": "string"}, "top_k": {"type": "integer"}}, "required": ["query"]}),
    (
        "memory_save",
        "Append durable memory to INDEX + topic file (secrets rejected). tags: kind (decision|constraint|gotcha|fix|open), topic:name, optional source via source field.",
        {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "tags": {"type": "string"},
                "source": {"type": "string"},
            },
            "required": ["text"],
        },
    ),
    ("evidence_check", "Run asset validation (scope=assets).", {"type": "object", "properties": {"scope": {"type": "string", "enum": ["assets"]}}}),
    (
        "interpret_intent",
        "Fast path: explicit/learned. Else needs_scoring: LLM scores input text (workflow+score). Pass scoring JSON.",
        {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "task": {"type": "string"},
                "scoring": {
                    "type": "object",
                    "description": "Upstream LLM: workflow fit score 0-1 for the input text",
                    "properties": {
                        "workflow": {"type": "string"},
                        "score": {"type": "number"},
                        "trigger": {"type": "string"},
                    },
                },
                "classification": {
                    "type": "object",
                    "description": "Deprecated alias of scoring",
                    "properties": {
                        "workflow": {"type": "string"},
                        "score": {"type": "number"},
                        "trigger": {"type": "string"},
                    },
                },
                "workflow": {"type": "string"},
                "score": {"type": "number"},
                "trigger": {"type": "string"},
                "via_receiver": {"type": "boolean"},
                "learn": {"type": "boolean"},
                "id": {"type": "string"},
            },
        },
    ),
    ("route_task", "Classify task and return human-readable routing (task-router compatible).", {"type": "object", "properties": {"task": {"type": "string"}}, "required": ["task"]}),
    (
        "workflow_clear",
        "Clear active workflow session and MCP tool allow-list gate.",
        {"type": "object", "properties": {}},
    ),
    (
        "delegate_subtask",
        "L3: Return structured subagent delegation for the active workflow (upstream runs Task/subagent).",
        {
            "type": "object",
            "properties": {
                "subtask": {"type": "string"},
                "prompt": {"type": "string"},
                "label": {"type": "string"},
                "agent": {"type": "string"},
                "background": {"type": "boolean"},
                "phase": {"type": "string"},
                "idempotency_key": {"type": "string"},
                "model_tier": {"type": "string"},
            },
        },
    ),
    (
        "steer_task",
        "Amend a running plan (add|reorder|reprioritize|scope_change|abort) using the plan as context. Without op, returns needs_classification for the host LLM.",
        {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "op": {"type": "string"},
                "target": {"type": "string"},
            },
            "required": ["text"],
        },
    ),
]

HANDLERS = {
    "capabilities": do_capabilities,
    "skill_search": do_skill_search,
    "skill_get": do_skill_get,
    "workflow_get": do_workflow_get,
    "agent_get": do_agent_get,
    "memory_recall": do_memory_recall,
    "memory_save": do_memory_save,
    "evidence_check": do_evidence_check,
    "interpret_intent": do_interpret_intent,
    "route_task": do_route_task,
    "workflow_clear": do_workflow_clear,
    "delegate_subtask": do_delegate_subtask,
    "steer_task": do_steer_task,
}


def handle(msg: dict) -> dict | None:
    method = msg.get("method")
    mid = msg.get("id")
    if method == "initialize":
        requested = (msg.get("params") or {}).get("protocolVersion")
        supported = {"2024-11-05", "2025-03-26", "2025-06-18"}
        version = requested if requested in supported else PROTOCOL
        return {"jsonrpc": "2.0", "id": mid, "result": {"protocolVersion": version, "capabilities": {"tools": {}}, "serverInfo": SERVER}}
    if method in ("notifications/initialized", "initialized"):
        return None
    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": [{"name": n, "description": d, "inputSchema": s} for n, d, s in TOOLS]}}
    if method == "tools/call":
        params = msg.get("params") or {}
        name = params.get("name")
        args = params.get("arguments") or {}
        fn = HANDLERS.get(name)
        if not fn:
            return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"unknown tool: {name}"}}
        deny = check_tool_allowed(name)
        if deny:
            return {"jsonrpc": "2.0", "id": mid, "result": tool_result(deny, True)}
        try:
            return {"jsonrpc": "2.0", "id": mid, "result": fn(args)}
        except Exception as exc:
            return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32603, "message": str(exc)}}
    return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"unknown method: {method}"}}


def main() -> None:
    for raw in sys.stdin:
        line = raw.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError as exc:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(exc)}}) + "\n")
            sys.stdout.flush()
            continue
        resp = handle(msg)
        if resp is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
