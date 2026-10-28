#!/usr/bin/env python3
"""Validate .kilo assets (skills/agents/commands). Stdlib only.

Checks:
- every skill dir has SKILL.md with name+description; name matches dir
- every agent has description+mode
- every command's `agent:` exists
- duplicate names across skills/agents/commands
- readiness.json entries exist as skills
- key JSON config files parse
Exit code 1 if issues found.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KILO = ROOT / ".kilo"
MEMORY = ROOT / "docs" / "memory"


def fm(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    out: dict[str, str] = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def documents_entry(command_path: Path, name: str) -> bool:
    """Whether the command documents "entry is the command / procedure is the same-named skill" (an intentional name collision)."""
    text = command_path.read_text(encoding="utf-8", errors="ignore")
    return "**入口**" in text and name in text


# Internal dev materials that must never be tracked in the public tree.
INTERNAL_PUBLIC_PATTERNS = (
    r"^internal/",
    r"^data/.*\.(db|sqlite)$",
    r"^docs/plans/ACTIVE\.md$",
    r"^docs/plans/CONTENT\.md$",
    r"^docs/plans/RETRO-.*\.md$",
    r"^docs/plans/self-improve-.*\.md$",
    r"^docs/plans/E2E-.*\.md$",
    r"^docs/design/.*-AUDIT\.md$",
    r"^docs/blog/",
    r"^docs/memory/(?!(TEMPLATE|MEMORY-TOOLS|INDEX\.example)(\.ja)?\.md$).+\.md$",
)



# Context-budget check (AGENTS §5): entry SKILL.md should be 2-4KB.
SKILL_BUDGET_BYTES = 4096
SKILL_BUDGET_EXCEPTIONS = frozenset(
    {"imagegen-frontend-mobile", "ask-matt", "wayfinder", "design-brief", "writing-for-agents", "teach"}
)



def command_replay_issues() -> list[str]:
    """Every command must declare `replay: safe|unsafe` (replay-safety classification)."""
    out: list[str] = []
    for entry in sorted((ROOT / ".kilo" / "commands").glob("*.md")):
        if entry.name == "README.md":
            continue
        meta = fm(entry)
        if not meta.get("agent"):  # not a workflow command; skip auxiliary markdown
            continue
        val = (meta.get("replay") or "").strip()
        if val not in ("safe", "unsafe"):
            out.append(f"command {entry.stem}: missing or invalid replay (expected safe|unsafe)")
    return out

def skill_budget_warnings() -> list[str]:
    """One summary warning for skills whose entry SKILL.md exceeds the 4KB budget."""
    over: list[str] = []
    for entry in sorted((ROOT / ".kilo" / "skills").glob("*/SKILL.md")):
        name = entry.parent.name
        if name in SKILL_BUDGET_EXCEPTIONS:
            continue
        try:
            size = entry.stat().st_size
        except OSError:
            continue
        if size > SKILL_BUDGET_BYTES:
            over.append(f"{name} ({size / 1024:.1f}KB)")
    if not over:
        return []
    return [f"{len(over)} skills over 4KB budget (see AGENTS §5): " + ", ".join(over)]

def public_boundary_violations() -> list[str]:
    """Boundary check for the source -> publish model.

    This repo is the private source of truth and tracks `internal/` by design; the
    public repo is generated from `.publish-allowlist`. The boundary to enforce is
    therefore that the allowlist never names an internal-only path.
    """
    al = ROOT / ".publish-allowlist"
    if not al.exists():
        return []
    bad: list[str] = []
    for raw in al.read_text(encoding="utf-8").splitlines():
        entry = raw.strip()
        if not entry or entry.startswith("#"):
            continue
        if entry == ".publish-allowlist" or any(
            re.match(p, entry) for p in INTERNAL_PUBLIC_PATTERNS
        ):
            bad.append(entry)
    return bad


def main() -> int:
    issues: list[str] = []

    # JSON configs
    for rel in ("kilo.json", ".cursor/mcp.json", "scripts/readiness.json"):
        p = ROOT / rel
        if p.exists():
            try:
                json.loads(p.read_text(encoding="utf-8"))
            except Exception as exc:
                issues.append(f"invalid JSON: {rel} ({exc})")

    skill_names: dict[str, str] = {}
    for d in sorted((KILO / "skills").glob("*/")):
        f = d / "SKILL.md"
        if not f.exists():
            issues.append(f"skill missing SKILL.md: {d.name}")
            continue
        meta = fm(f)
        name = meta.get("name") or d.name
        if not meta.get("name"):
            issues.append(f"skill missing name: {d.name}")
        elif name != d.name:
            issues.append(f"skill name!=dir: {name} vs {d.name}")
        if not meta.get("description"):
            issues.append(f"skill missing description: {d.name}")
        if name in skill_names:
            issues.append(f"duplicate skill name: {name} ({d.name} vs {skill_names[name]})")
        skill_names[name] = d.name

    agent_names: set[str] = set()
    for f in sorted((KILO / "agents").glob("*.md")):
        meta = fm(f)
        if not meta.get("description"):
            issues.append(f"agent missing description: {f.name}")
        if not meta.get("mode"):
            issues.append(f"agent missing mode: {f.name}")
        agent_names.add(f.stem)

    command_names: set[str] = set()
    for f in sorted((KILO / "commands").glob("*.md")):
        if f.stem == "README":
            continue
        command_names.add(f.stem)
        meta = fm(f)
        if not meta.get("description"):
            issues.append(f"command missing description: {f.name}")
        a = meta.get("agent")
        if a and a not in agent_names:
            issues.append(f"command {f.stem} -> missing agent {a}")

    # cross-kind duplicates: skill/agent share model-selectable namespace (error);
    # command is slash-namespaced, so collisions with commands are warnings —
    # But if the command documents "entry is the command / procedure is the same-named skill", treat it as intentional and do not warn.
    warnings: list[str] = []
    for n in sorted(set(skill_names) & agent_names):
        issues.append(f"name used as both skill and agent: {n}")
    for n in sorted(set(skill_names) & command_names):
        cmd = KILO / "commands" / f"{n}.md"
        if cmd.exists() and documents_entry(cmd, n):
            continue
        warnings.append(f"name used as both skill and command (slash vs model): {n}")
    for n in sorted(agent_names & command_names):
        warnings.append(f"name used as both agent and command (slash vs model): {n}")

    # readiness references
    rp = ROOT / "scripts" / "readiness.json"
    if rp.exists():
        try:
            data = json.loads(rp.read_text(encoding="utf-8"))
            for n in (data.get("needs_setup") or {}):
                if n not in skill_names:
                    issues.append(f"readiness references unknown skill: {n}")
        except Exception:
            pass

    # memory: secret patterns (same rules as MCP memory_save)
    if MEMORY.is_dir():
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "memory_ops", ROOT / "mcp" / "memory_ops.py"
        )
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            for line in mod.scan_memory_secrets(MEMORY):
                issues.append(line)

    for b in public_boundary_violations():
        issues.append(f"publish allowlist must not include internal path: {b}")

    issues.extend(command_replay_issues())
    warnings.extend(skill_budget_warnings())

    for w in warnings:
        print("WARN:", w)
    if issues:
        print("ISSUES:")
        for i in issues:
            print(" -", i)
        return 1
    print(f"OK: skills={len(skill_names)} agents={len(agent_names)} commands={len(command_names)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
