#!/usr/bin/env python3
"""Mock the behavior of Kilo CLI / Cursor CLI via MCP (no real TUI or agent login). stdlib only."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KILO_COMMANDS = ROOT / ".kilo" / "commands"


@dataclass
class WorkflowPayload:
    name: str
    body: str
    source: str  # kilo-slash | cursor-at-file


def mcp_workflow_get(name: str) -> str:
    proc = subprocess.Popen(
        [sys.executable, str(ROOT / "mcp" / "server.py")],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=str(ROOT),
    )
    try:
        proc.stdin.write(
            json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": 0,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {},
                        "clientInfo": {"name": "cli-mock", "version": "0"},
                    },
                }
            )
            + "\n"
        )
        proc.stdin.flush()
        proc.stdout.readline()
        proc.stdin.write(
            json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {
                        "name": "workflow_get",
                        "arguments": {"name": name.lstrip("/")},
                    },
                }
            )
            + "\n"
        )
        proc.stdin.flush()
        line = proc.stdout.readline()
        data = json.loads(line)
        if data.get("result", {}).get("isError"):
            raise RuntimeError(data)
        return data["result"]["content"][0]["text"]
    finally:
        try:
            proc.stdin.close()
        except Exception:
            pass
        proc.wait(timeout=30)


class KiloCLIMock:
    """Kilo: `/workflow-name` → the workflow body (equivalent to MCP workflow_get)."""

    native_slash: bool = True

    def resolve_slash(self, slash: str) -> WorkflowPayload:
        name = slash.strip().lstrip("/")
        path = KILO_COMMANDS / f"{name}.md"
        if not path.is_file():
            raise FileNotFoundError(f"unknown slash command: /{name}")
        body = mcp_workflow_get(name)
        return WorkflowPayload(name=name, body=body, source="kilo-slash")


class CursorCLIMock:
    """Cursor: `@.kilo/commands/<name>.md` → the same workflow. Slash is not natively supported."""

    native_slash: bool = False

    def resolve_at_file(self, at_path: str) -> WorkflowPayload:
        # @.kilo/commands/foo.md or .kilo/commands/foo.md
        clean = at_path.strip().lstrip("@")
        p = Path(clean)
        if not p.is_absolute():
            p = ROOT / clean
        if not p.is_file():
            raise FileNotFoundError(at_path)
        if ".kilo/commands" not in str(p).replace("\\", "/"):
            raise ValueError("not a workflow path")
        name = p.stem
        body = mcp_workflow_get(name)
        return WorkflowPayload(name=name, body=body, source="cursor-at-file")

    def try_slash(self, slash: str) -> None:
        if slash.startswith("/"):
            raise NotImplementedError("Cursor has no native slash commands; use @.kilo/commands/...")


# Expect SSOT keywords per deliverable type (contract E2E)
DELIVERABLE_SSOT = {
    "delivery-lite": ("ACTIVE.md", "plan_active"),
    "content-delivery-lite": ("CONTENT.md", "plan_content"),
    "ui-delivery": ("ACTIVE.md",),
    "research": ("ACTIVE.md",),
    "market-plan": ("ACTIVE.md",),
}


def assert_workflow_contract(payload: WorkflowPayload) -> list[str]:
    issues: list[str] = []
    pair = DELIVERABLE_SSOT.get(payload.name)
    if not pair:
        return issues
    for needle in pair:
        if needle not in payload.body:
            issues.append(f"{payload.name}: missing {needle} in workflow body")
    return issues


def run_parity_check(workflow_names: list[str]) -> list[str]:
    """The same workflow body is obtained via Kilo slash and Cursor @file."""
    issues: list[str] = []
    kilo = KiloCLIMock()
    cursor = CursorCLIMock()
    for name in workflow_names:
        k = kilo.resolve_slash(f"/{name}")
        c = cursor.resolve_at_file(f".kilo/commands/{name}.md")
        if k.body != c.body:
            issues.append(f"parity mismatch: {name} (kilo vs cursor)")
        issues.extend(assert_workflow_contract(k))
    return issues


def main() -> int:
    names = [
        "delivery-lite",
        "content-delivery-lite",
        "ui-delivery",
        "research",
        "market-plan",
    ]
    print("== cli_adapters_mock (Kilo / Cursor parity) ==")
    issues = run_parity_check(names)
    cursor = CursorCLIMock()
    try:
        cursor.try_slash("/delivery-lite")
        issues.append("cursor should reject native slash")
    except NotImplementedError:
        print("PASS cursor rejects native slash")
    if issues:
        for i in issues:
            print("FAIL", i)
        return 1
    print(f"PASS parity for {len(names)} workflows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
