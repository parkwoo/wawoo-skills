"""Amend / steer a running plan (OS-7).

The MCP does not run the host loop and does not write the plan files. It
returns a structured **amend** instruction that the host agent applies to
ACTIVE/BACKLOG at a step boundary, using the running plan as context.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

OPS = ("add", "reorder", "reprioritize", "scope_change", "abort")

_ROW = re.compile(
    r"^\|\s*([A-Za-z0-9][A-Za-z0-9._-]*)\s*\|\s*"
    r"(open|in_progress|done|blocked|todo|doing)\s*\|\s*([^|]+)"
)


def _rows(path: Path) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return out
    for line in text.splitlines():
        m = _ROW.match(line.strip())
        if m:
            out.append(
                {"id": m.group(1), "status": m.group(2), "title": m.group(3).strip()}
            )
    return out


def plan_context(root: Path) -> dict[str, Any]:
    """A compact view of the running plan (backlog + active), if present."""
    backlog = _rows(root / "docs" / "plans" / "BACKLOG.md")
    active = _rows(root / "docs" / "plans" / "ACTIVE.md")
    return {"backlog": backlog[:50], "active": active[:50]}


def build_steer_payload(
    *,
    text: str,
    root: Path,
    active_workflow: str = "",
    op: str = "",
    target: str = "",
) -> dict[str, Any]:
    """Build an amend instruction. Without a valid `op`, ask the host to classify."""
    text = (text or "").strip()
    if not text:
        raise ValueError("text is required")
    ctx = plan_context(root)
    base: dict[str, Any] = {
        "kind": "amend",
        "text": text,
        "active_workflow": active_workflow,
        "plan": ctx,
    }
    op = (op or "").strip().lower()
    if op in OPS:
        base.update(
            {
                "op": op,
                "target": (target or "").strip(),
                "needs_classification": False,
                "applied": False,
                "note": (
                    "Apply to ACTIVE/BACKLOG at a step boundary (append for add; "
                    "reorder/reprioritize in place; never overwrite done rows). "
                    "For abort, propagate to owned subagents."
                ),
            }
        )
        return base
    base.update(
        {
            "op": "",
            "needs_classification": True,
            "prompt": (
                "Using the plan context, classify this instruction into one op "
                f"({', '.join(OPS)}) and a target id, then re-call steer_task with op/target. "
                "Do not guess scope beyond the text."
            ),
        }
    )
    return base
