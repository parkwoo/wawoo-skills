#!/usr/bin/env python3
"""タスクルーター CLI — 意図解釈器の薄いラッパ。"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mcp"))

from intent_interpreter import format_route_task_text, interpret_intent  # noqa: E402


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: task-router.py '<task description>' [--json]")
        sys.exit(1)
    task_text = sys.argv[1]
    as_json = "--json" in sys.argv[2:]
    schedule = interpret_intent(task_text)
    if as_json:
        print(json.dumps(schedule.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(format_route_task_text(schedule))


if __name__ == "__main__":
    main()
