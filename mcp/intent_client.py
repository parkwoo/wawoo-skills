"""意図受信器（常駐）へのクライアント。"""
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
    """常駐受信器へ意図を送り、スケジュールを得る。未設定時は None を返す代わりに例外。"""
    path = socket_path()
    if not path or not Path(path).parent.exists():
        raise FileNotFoundError("WAWOO_INTENT_SOCKET が未設定、または親ディレクトリが無い")
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
