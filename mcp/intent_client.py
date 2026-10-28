"""Client for the (resident) intent receiver."""
from __future__ import annotations

import json
import os
import socket
from pathlib import Path
from typing import Any


def socket_path() -> str | None:
    path = os.environ.get("WAWOO_INTENT_SOCKET", "").strip()
    return path or None


def submit_intent(text: str, *, intent_id: str = "", timeout: float = 2.0) -> dict[str, Any]:
    """Send an intent to the resident receiver and get a schedule. Raises instead of returning None when unset."""
    path = socket_path()
    if not path or not Path(path).parent.exists():
        raise FileNotFoundError("WAWOO_INTENT_SOCKET is unset, or the parent directory is missing")
    payload = {"id": intent_id or "", "text": text}
    data = (json.dumps(payload, ensure_ascii=False) + "\n").encode("utf-8")
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        sock.connect(path)
        sock.sendall(data)
        chunks: list[bytes] = []
        while True:
            part = sock.recv(4096)
            if not part:
                break
            chunks.append(part)
            if b"\n" in part:
                break
    line = b"".join(chunks).split(b"\n", 1)[0].decode("utf-8")
    return json.loads(line)
