"""The active workflow and MCP tool permission after interpret_intent (B3).

The gate can optionally be persisted so it survives an MCP-server restart
(resume). Resume is **opt-in**: set `WAWOO_INTENT_RESUME=1`. Only the minimal
gate fields are persisted (never the raw prompt text). Set
`WAWOO_INTENT_SESSION` to override the file path.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

# Tools always callable while gated (re-route, clear session, L3 delegation, steer)
_GATE_EXEMPT: frozenset[str] = frozenset(
    {
        "interpret_intent",
        "route_task",
        "workflow_clear",
        "delegate_subtask",
        "steer_task",
    }
)

# A persisted session older than this is ignored and removed.
_TTL_SECONDS = 12 * 3600

# Only these fields are persisted; never the raw prompt/clean_text/trace.
_PERSIST_KEYS = (
    "workflow",
    "agent",
    "mcp_tools_allow",
    "command_path",
    "delegation_hint",
    "intent_id",
)

_active: dict[str, Any] | None = None
_loaded = False


def _resume_enabled() -> bool:
    return os.environ.get("WAWOO_INTENT_RESUME", "").strip().lower() in ("1", "true", "yes")


def _root() -> Path:
    env = os.environ.get("WAWOO_SKILLS_ROOT", "").strip()
    if env:
        p = Path(env).expanduser()
        if p.is_dir():
            return p
    return Path(__file__).resolve().parents[1]


def _session_path() -> Path:
    env = os.environ.get("WAWOO_INTENT_SESSION", "").strip()
    if env:
        return Path(env).expanduser()
    client = re.sub(r"[^A-Za-z0-9._-]", "_", os.environ.get("WAWOO_INTENT_CLIENT", "").strip())
    name = f"intent_session.{client}.json" if client else "intent_session.json"
    return _root() / "data" / name


def _warn(msg: str) -> None:
    # Best-effort diagnostics; never include session contents.
    print(f"wawoo intent_session: {msg}", file=sys.stderr)


def _load() -> None:
    """Load the persisted session once (lazy), only when resume is enabled."""
    global _active, _loaded
    if _loaded:
        return
    _loaded = True
    if not _resume_enabled():
        return
    path = _session_path()
    try:
        if not path.is_file():
            return
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return
        saved = float(data.get("_saved_at", 0) or 0)
        if saved and (time.time() - saved) > _TTL_SECONDS:
            try:
                path.unlink()
            except OSError:
                pass
            return
        schedule = data.get("schedule")
        if isinstance(schedule, dict) and schedule.get("workflow"):
            _active = schedule
    except Exception as exc:  # corrupt/unreadable session must not crash the server
        _warn(f"ignored unreadable session ({type(exc).__name__})")


def _save() -> None:
    path = _session_path()
    if _active is None:
        try:
            path.unlink()
        except OSError:
            pass
        return
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        minimal = {k: _active[k] for k in _PERSIST_KEYS if k in _active}
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(json.dumps({"schedule": minimal, "_saved_at": time.time()}, ensure_ascii=False), encoding="utf-8")
        os.replace(tmp, path)
    except Exception as exc:  # persistence is best-effort; the in-memory gate still holds
        _warn(f"could not persist session ({type(exc).__name__})")


def active_schedule() -> dict[str, Any] | None:
    _load()
    return _active


def activate_schedule(schedule: dict[str, Any]) -> None:
    global _active
    if not schedule.get("workflow"):
        return
    _active = dict(schedule)
    if _resume_enabled():
        _save()


def clear_schedule() -> None:
    global _active
    _active = None
    _save()


def reset_session(delete: bool = True) -> None:
    """Drop in-memory state. For tests: `delete=False` simulates a restart."""
    global _active, _loaded
    _active = None
    _loaded = False
    if delete:
        try:
            _session_path().unlink()
        except OSError:
            pass


def allowed_tool_names() -> frozenset[str] | None:
    _load()
    if _active is None:
        return None
    raw = _active.get("mcp_tools_allow") or []
    if not isinstance(raw, list):
        return None
    return frozenset(str(x) for x in raw) | _GATE_EXEMPT


def check_tool_allowed(tool_name: str) -> str | None:
    """None if allowed. A user-facing error message if denied."""
    _load()
    allow = allowed_tool_names()
    if allow is None:
        return None
    if tool_name in allow:
        return None
    wf = _active.get("workflow", "?") if _active else "?"
    return (
        f"MCP tool '{tool_name}' is outside the allow-set of workflow '{wf}'."
        f" allowed: {','.join(sorted(allow - _GATE_EXEMPT))}."
        " To re-route use interpret_intent; to release use workflow_clear."
    )
