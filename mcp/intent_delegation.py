"""L3: a subagent delegation hint after the workflow starts (for the upstream agent / Task)."""
from __future__ import annotations

import json
from typing import Any


def build_delegation_payload(
    parent_schedule: dict[str, Any],
    *,
    subtask: str,
    label: str = "",
    background: bool = False,
    suggested_agent: str = "",
    idempotency_key: str = "",
    model_tier: str = "",
) -> dict[str, Any]:
    """Structured instruction equivalent to an OpenCode subagent (the upstream agent runs it via Task, etc.)."""
    subtask = (subtask or "").strip()
    if not subtask:
        raise ValueError("subtask is required")
    wf = str(parent_schedule.get("workflow", "")).strip()
    agent = suggested_agent.strip() or str(parent_schedule.get("agent", "")).strip()
    hint = str(parent_schedule.get("delegation_hint", "upstream-subagent")).strip()
    payload = {
        "route_layer": "L3",
        "delegation": hint,
        "parent_workflow": wf,
        "parent_agent": agent,
        "subtask": subtask,
        "label": (label or subtask[:40]).strip(),
        "background": background,
        "instruction": (
            f"While the parent workflow /{wf} is running, run the following subtask in an isolated session (subagent) and"
            f"return only the result to the parent. Subtask: {subtask}"
        ),
        "command_path": parent_schedule.get("command_path", ""),
    }
    key = idempotency_key.strip()
    if key:
        payload["idempotency_key"] = key
    tier = model_tier.strip().lower()
    if tier in ("fast", "reasoning"):
        payload["model_tier"] = tier
    return payload


def format_delegation_text(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)
