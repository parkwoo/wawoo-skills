#!/usr/bin/env python3
"""this project capability MCP server (stdio, stdlib only).

Exposes skills/agents/workflows/memory/evidence as MCP tools so that agents
(Kilo and Cursor) invoke them via tool calls instead of relying on prose.

Transport: newline-delimited JSON-RPC 2.0 over stdio.
Tools:
  capabilities, skill_search, skill_get, workflow_get, agent_get,
  memory_recall, memory_save, evidence_check
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KILO = ROOT / ".kilo"
MEMORY = ROOT / "docs" / "memory"
PROTOCOL = "2024-11-05"
SERVER = {"name": "wawoo-skills-capabilities", "version": "0.1.0"}

SECRET_PATTERNS = re.compile(
    r"(sk-[A-Za-z0-9]{8,}|AKIA[0-9A-Z]{12,}|ghp_[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|password\s*=|token\s*=)",
    re.IGNORECASE,
)


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
    if not str(rp).startswith(str(KILO.resolve())):
        raise ValueError("path outside .kilo")
    return rp.read_text(encoding="utf-8", errors="ignore")


def do_capabilities(args: dict) -> dict:
    ready_only = bool(args.get("ready_only"))
    lines = []
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
    return tool_result(safe_read(p))


def do_agent_get(args: dict) -> dict:
    name = str(args.get("name", ""))
    p = CAT.agents.get(name)
    if not p:
        return tool_result(f"unknown agent: {name}", True)
    return tool_result(safe_read(p))


def do_memory_recall(args: dict) -> dict:
    q = str(args.get("query", "")).lower()
    terms = [t for t in re.split(r"\W+", q) if t]
    top_k = int(args.get("top_k", 5))
    hits = []
    for p in sorted(MEMORY.glob("*.md")):
        text = p.read_text(encoding="utf-8", errors="ignore")
        low = text.lower()
        score = sum(low.count(t) for t in terms) if terms else 0
        if terms and score == 0:
            continue
        idx = low.find(terms[0]) if terms else 0
        snippet = text[max(0, idx - 120) : idx + 400]
        hits.append((score, str(p.relative_to(ROOT)), snippet))
    hits.sort(key=lambda x: -x[0])
    if not hits:
        return tool_result("no memory matches")
    return tool_result("\n\n".join(f"[{p}]\n{s}" for _, p, s in hits[:top_k]))


def do_memory_save(args: dict) -> dict:
    text = str(args.get("text", "")).strip()
    tags = str(args.get("tags", "")).strip()
    if not text:
        return tool_result("empty text", True)
    if SECRET_PATTERNS.search(text):
        return tool_result("refused: possible secret detected", True)
    MEMORY.mkdir(parents=True, exist_ok=True)
    target = MEMORY / "INDEX.md"
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with target.open("a", encoding="utf-8") as f:
        f.write(f"\n- {stamp} [{tags}] {text}\n")
    return tool_result(f"saved to {target.relative_to(ROOT)}")


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


TOOLS = [
    ("capabilities", "List skills/agents/workflows with one-line descriptions.", {"type": "object", "properties": {"ready_only": {"type": "boolean"}}}),
    ("skill_search", "Search skills/agents/workflows by query.", {"type": "object", "properties": {"query": {"type": "string"}, "limit": {"type": "integer"}}, "required": ["query"]}),
    ("skill_get", "Get the full SKILL.md for a skill name.", {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}),
    ("workflow_get", "Get the full command/workflow by name.", {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}),
    ("agent_get", "Get an agent definition by name.", {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}),
    ("memory_recall", "Recall relevant memory entries from docs/memory.", {"type": "object", "properties": {"query": {"type": "string"}, "top_k": {"type": "integer"}}, "required": ["query"]}),
    ("memory_save", "Append a durable memory entry (secrets rejected).", {"type": "object", "properties": {"text": {"type": "string"}, "tags": {"type": "string"}}, "required": ["text"]}),
    ("evidence_check", "Run asset validation (scope=assets).", {"type": "object", "properties": {"scope": {"type": "string", "enum": ["assets"]}}}),
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
