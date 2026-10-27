"""interpret_intent 後のアクティブ workflow と MCP ツール許可（B3）。"""
from __future__ import annotations

from typing import Any

# ゲート中も常に呼べるツール（再ルート・セッション解除・L3 委譲）
_GATE_EXEMPT: frozenset[str] = frozenset(
    {
        "interpret_intent",
        "route_task",
        "workflow_clear",
        "delegate_subtask",
    }
)

_active: dict[str, Any] | None = None


def active_schedule() -> dict[str, Any] | None:
    return _active


def activate_schedule(schedule: dict[str, Any]) -> None:
    global _active
    if not schedule.get("workflow"):
        return
    _active = dict(schedule)


def clear_schedule() -> None:
    global _active
    _active = None


def allowed_tool_names() -> frozenset[str] | None:
    if _active is None:
        return None
    raw = _active.get("mcp_tools_allow") or []
    if not isinstance(raw, list):
        return None
    return frozenset(str(x) for x in raw) | _GATE_EXEMPT


def check_tool_allowed(tool_name: str) -> str | None:
    """許可なら None。拒否ならユーザー向けエラーメッセージ。"""
    allow = allowed_tool_names()
    if allow is None:
        return None
    if tool_name in allow:
        return None
    wf = _active.get("workflow", "?") if _active else "?"
    return (
        f"MCP ツール '{tool_name}' は workflow '{wf}' の許可集合外です。"
        f"許可: {','.join(sorted(allow - _GATE_EXEMPT))}。"
        "再ルートする場合は interpret_intent、解除は workflow_clear。"
    )
