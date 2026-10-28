#!/usr/bin/env python3
"""Parse and validate the task table in docs/plans/ACTIVE.md (stdlib only)."""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

VALID_STATUS = frozenset({"todo", "doing", "done", "blocked"})
PLACEHOLDER_IDS = frozenset({"—", "-", "id", ""})


@dataclass
class ActiveTask:
    id: str
    status: str
    body: str
    acceptance: str
    evidence: str


def parse_active(path: Path) -> list[ActiveTask]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    tasks: list[ActiveTask] = []
    in_section = False
    for line in text.splitlines():
        if line.strip() == "## タスク":
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section or not line.startswith("|"):
            continue
        if re.match(r"^\|[\s\-:|]+\|$", line.strip()):
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) < 5:
            continue
        tid, status, body, acceptance, evidence = cols[0], cols[1], cols[2], cols[3], cols[4]
        if tid.lower() in PLACEHOLDER_IDS or status.lower() in PLACEHOLDER_IDS:
            continue
        tasks.append(
            ActiveTask(
                id=tid,
                status=status.lower(),
                body=body,
                acceptance=acceptance,
                evidence=evidence,
            )
        )
    return tasks


def validate_tasks(tasks: list[ActiveTask]) -> list[str]:
    issues: list[str] = []
    doing = 0
    seen: set[str] = set()
    for t in tasks:
        if t.id in seen:
            issues.append(f"duplicate id: {t.id}")
        seen.add(t.id)
        if t.status not in VALID_STATUS:
            issues.append(f"{t.id}: invalid status '{t.status}'")
        if t.status == "doing":
            doing += 1
        if t.status == "done" and not t.evidence.strip():
            issues.append(f"{t.id}: done without evidence")
    if doing > 1:
        issues.append(f"more than one doing ({doing})")
    return issues


def check_file(path: Path) -> int:
    if not path.is_file():
        print(f"MISSING: {path}")
        return 1
    tasks = parse_active(path)
    issues = validate_tasks(tasks)
    if issues:
        print(f"ACTIVE check FAILED: {path}")
        for i in issues:
            print(" -", i)
        return 1
    print(f"ACTIVE OK: {path} tasks={len(tasks)}")
    return 0


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    default = root / "docs" / "plans" / "ACTIVE.md"
    p = argparse.ArgumentParser(description="Validate ACTIVE.md task table (Gₑ helper)")
    p.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=default,
        help=f"ACTIVE.md path (default: {default.relative_to(root)})",
    )
    return check_file(p.parse_args().path)


if __name__ == "__main__":
    sys.exit(main())
