#!/usr/bin/env python3
"""B3 MCP ゲート・L3 delegate の単体テスト。"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "mcp" / "server.py"
sys.path.insert(0, str(ROOT / "mcp"))

from intent_delegation import build_delegation_payload  # noqa: E402
from intent_session import activate_schedule, check_tool_allowed, clear_schedule  # noqa: E402


def rpc(proc, payload: dict) -> dict:
    proc.stdin.write(json.dumps(payload) + "\n")
    proc.stdin.flush()
    line = proc.stdout.readline()
    return json.loads(line)


def test_session_gate_unit() -> None:
    clear_schedule()
    activate_schedule(
        {
            "workflow": "compliance-review",
            "mcp_tools_allow": [
                "capabilities",
                "skill_search",
                "skill_get",
                "workflow_get",
                "agent_get",
                "memory_recall",
                "evidence_check",
                "interpret_intent",
                "route_task",
            ],
        }
    )
    assert check_tool_allowed("memory_save") is not None
    assert check_tool_allowed("skill_get") is None
    assert check_tool_allowed("workflow_clear") is None
    clear_schedule()
    assert check_tool_allowed("memory_save") is None  # ゲート解除後は全許可


def test_delegation_payload() -> None:
    p = build_delegation_payload(
        {"workflow": "research", "agent": "product-owner", "delegation_hint": "upstream-subagent"},
        subtask="競合3社を調べる",
        label="競合調査",
    )
    assert p["route_layer"] == "L3"
    assert p["parent_workflow"] == "research"


def test_mcp_gate_stdio() -> None:
    env = dict(os.environ)
    with tempfile.TemporaryDirectory() as td:
        # テストが実リポジトリの docs/memory を汚さないよう隔離する
        env["WAWOO_MEMORY_ROOT"] = td
        env["WAWOO_INTENT_LEARN_DB"] = str(Path(td) / "learned.db")
        proc = subprocess.Popen(
            [sys.executable, str(SERVER)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(ROOT),
            env=env,
        )
        _run_gate_scenario(proc)


def _run_gate_scenario(proc) -> None:
    try:
        rpc(proc, {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "t", "version": "0"}}})
        rpc(proc, {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "interpret_intent", "arguments": {"text": "/compliance-review ポリシー確認"}}})
        blocked = rpc(
            proc,
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {"name": "memory_save", "arguments": {"text": "test", "tags": "decision"}},
            },
        )
        assert blocked["result"].get("isError") is True
        assert "許可集合外" in blocked["result"]["content"][0]["text"]
        deleg = rpc(
            proc,
            {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {"name": "delegate_subtask", "arguments": {"subtask": "条項Aを要約"}},
            },
        )
        assert not deleg["result"].get("isError")
        assert "L3" in deleg["result"]["content"][0]["text"]
        rpc(proc, {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "workflow_clear", "arguments": {}}})
        ok = rpc(
            proc,
            {
                "jsonrpc": "2.0",
                "id": 6,
                "method": "tools/call",
                "params": {"name": "memory_save", "arguments": {"text": "after clear", "tags": "open"}},
            },
        )
        assert not ok["result"].get("isError")
    finally:
        proc.stdin.close()
        proc.wait(timeout=10)


def main() -> int:
    test_session_gate_unit()
    test_delegation_payload()
    test_mcp_gate_stdio()
    print("intent_session tests: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
