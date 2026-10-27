#!/usr/bin/env python3
"""memory_ops の単体テスト（stdlib のみ）。"""
from __future__ import annotations

import tempfile
from pathlib import Path

from memory_ops import recall_memory, save_memory, scan_memory_secrets


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        mem = Path(td)
        msg = save_memory(
            mem,
            "MCP は INDEX と topic ファイルの両方に追記する",
            "decision,topic:kit",
            "docs/METHODOLOGY.md",
        )
        assert "MEM-" in msg and "kit.md" in msg, msg

        got = recall_memory(mem, "MCP INDEX", 3)
        assert "INDEX" in got or "MCP" in got, got

        bad = 0
        try:
            save_memory(mem, "password=supersecret", "fix")
        except ValueError:
            bad = 1
        assert bad == 1

        issues = scan_memory_secrets(mem)
        assert not issues, issues

    print("memory_ops unit test: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
