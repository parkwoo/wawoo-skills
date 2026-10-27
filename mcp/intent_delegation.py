"""L3: workflow 起動後の subagent 委譲ヒント（上流エージェント / Task 向け）。"""
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
) -> dict[str, Any]:
    """OpenCode subagent 相当の構造化指示（実行は上流エージェントが Task 等で行う）。"""
    subtask = (subtask or "").strip()
    if not subtask:
        raise ValueError("subtask is required")
    wf = str(parent_schedule.get("workflow", "")).strip()
    agent = suggested_agent.strip() or str(parent_schedule.get("agent", "")).strip()
    hint = str(parent_schedule.get("delegation_hint", "upstream-subagent")).strip()
    return {
        "route_layer": "L3",
        "delegation": hint,
        "parent_workflow": wf,
        "parent_agent": agent,
        "subtask": subtask,
        "label": (label or subtask[:40]).strip(),
        "background": background,
        "instruction": (
            f"親 workflow /{wf} の実行中。次のサブタスクを隔離セッション（subagent）で実行し、"
            f"結果だけ親に返す。サブタスク: {subtask}"
        ),
        "command_path": parent_schedule.get("command_path", ""),
    }


def format_delegation_text(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)
