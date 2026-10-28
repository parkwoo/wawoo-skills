#!/usr/bin/env python3
"""Intent receiver — a resident process. Receives intents over NDJSON and schedules a workflow.

The resident entry for intent scoring (stdio / Unix socket). The decision is made by the upstream LLM; DB writes are async.

起動:
  python3 mcp/intent_receiver.py
  python3 mcp/intent_receiver.py --socket /run/user/1000/wawoo-intent.sock

Protocol (one JSON per line):
  request: {"id":"1","text":"I want to fix a bug","meta":{}}
  応答: {"id":"1","ok":true,"schedule":{...}}
"""
from __future__ import annotations

import argparse
import json
import os
import socket
import sys
import threading
import uuid
from pathlib import Path
from typing import Any

# modules in the same directory
sys.path.insert(0, str(Path(__file__).resolve().parent))
from intent_interpreter import interpret_intent_payload


def _default_socket_path() -> str:
    runtime = os.environ.get("XDG_RUNTIME_DIR", "").strip()
    if runtime:
        return str(Path(runtime) / "wawoo-intent.sock")
    return "/tmp/wawoo-intent.sock"


def _schedule_request(payload: dict[str, Any]) -> dict[str, Any]:
    req_id = str(payload.get("id") or uuid.uuid4())
    text = str(payload.get("text", "")).strip()
    scoring = payload.get("scoring") if isinstance(payload.get("scoring"), dict) else None
    classification = payload.get("classification") if isinstance(payload.get("classification"), dict) else None
    if scoring is None and classification is None and payload.get("workflow"):
        scoring = {
            "workflow": payload.get("workflow"),
            "score": payload.get("score"),
            "trigger": payload.get("trigger"),
        }
    body = interpret_intent_payload(
        text,
        intent_id=req_id,
        classification=classification,
        scoring=scoring,
    )
    return {"id": req_id, **body}


def handle_line(line: str) -> str:
    line = line.strip()
    if not line:
        return json.dumps({"ok": False, "error": "empty line"}, ensure_ascii=False)
    try:
        payload = json.loads(line)
    except json.JSONDecodeError as exc:
        return json.dumps({"ok": False, "error": f"invalid json: {exc}"}, ensure_ascii=False)
    if payload.get("op") == "ping":
        return json.dumps({"ok": True, "op": "ping", "service": "wawoo-intent-receiver"}, ensure_ascii=False)
    try:
        result = _schedule_request(payload)
        return json.dumps(result, ensure_ascii=False, separators=(",", ":"))
    except Exception as exc:  # pragma: no cover
        return json.dumps(
            {"id": payload.get("id"), "ok": False, "error": str(exc)},
            ensure_ascii=False,
        )


def run_stdio() -> None:
    for line in sys.stdin:
        if not line:
            break
        sys.stdout.write(handle_line(line) + "\n")
        sys.stdout.flush()


def _client_handler(conn: socket.socket) -> None:
    with conn:
        file = conn.makefile("rwb")
        for raw in file:
            line = raw.decode("utf-8", errors="replace")
            out = handle_line(line) + "\n"
            file.write(out.encode("utf-8"))
            file.flush()


def run_socket(path: str) -> None:
    sock_path = Path(path)
    if sock_path.exists():
        sock_path.unlink()
    sock_path.parent.mkdir(parents=True, exist_ok=True)
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    # restrict permissions (so other users cannot post even with a loose umask like /tmp)
    old_umask = os.umask(0o177)
    try:
        server.bind(str(sock_path))
    finally:
        os.umask(old_umask)
    try:
        os.chmod(sock_path, 0o600)
    except OSError:
        pass
    server.listen(8)
    sys.stderr.write(f"wawoo intent receiver listening on {sock_path}\n")
    sys.stderr.flush()
    try:
        while True:
            conn, _ = server.accept()
            threading.Thread(target=_client_handler, args=(conn,), daemon=True).start()
    finally:
        server.close()
        if sock_path.exists():
            sock_path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description="wawoo-skills 意図受信器（常駐）")
    parser.add_argument(
        "--socket",
        default=os.environ.get("WAWOO_INTENT_SOCKET", "").strip() or None,
        help="Unix socket path (stdio when omitted)",
    )
    args = parser.parse_args()
    socket_path = args.socket or os.environ.get("WAWOO_INTENT_SOCKET", "").strip()
    if not socket_path:
        run_stdio()
        return 0
    run_socket(socket_path or _default_socket_path())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
