#!/usr/bin/env python3
"""Smoke test for the capability MCP server (stdio JSON-RPC). Stdlib only."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "mcp" / "server.py"


def rpc(proc, payload: dict) -> dict:
    proc.stdin.write(json.dumps(payload) + "\n")
    proc.stdin.flush()
    line = proc.stdout.readline()
    if not line:
        raise RuntimeError("no response")
    return json.loads(line)


def main() -> int:
    proc = subprocess.Popen(
        [sys.executable, str(SERVER)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=str(ROOT),
    )
    try:
        init = rpc(proc, {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "0"}}})
        assert init["result"]["serverInfo"]["name"] == "wawoo-skills-capabilities", init

        tools = rpc(proc, {"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        names = {t["name"] for t in tools["result"]["tools"]}
        for required in ("capabilities", "skill_search", "skill_get", "workflow_get", "agent_get", "memory_recall", "memory_save", "evidence_check"):
            assert required in names, (required, names)

        cap = rpc(proc, {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "capabilities", "arguments": {}}})
        text = cap["result"]["content"][0]["text"]
        assert "code-review" in text and "/feature-delivery" in text, text[:200]

        got = rpc(proc, {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "skill_get", "arguments": {"name": "code-review"}}})
        assert not got["result"].get("isError"), got
        assert "code-review" in got["result"]["content"][0]["text"].lower()

        wf = rpc(proc, {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "workflow_get", "arguments": {"name": "feature-delivery"}}})
        assert not wf["result"].get("isError"), wf

        ev = rpc(proc, {"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"name": "evidence_check", "arguments": {"scope": "assets"}}})
        assert not ev["result"].get("isError"), ev

        bad = rpc(proc, {"jsonrpc": "2.0", "id": 7, "method": "tools/call", "params": {"name": "skill_get", "arguments": {"name": "../etc/passwd"}}})
        assert bad["result"].get("isError") is True, bad

        print("MCP server smoke test: OK")
        return 0
    finally:
        try:
            proc.stdin.close()
        except Exception:
            pass
        proc.wait(timeout=5)


if __name__ == "__main__":
    sys.exit(main())
