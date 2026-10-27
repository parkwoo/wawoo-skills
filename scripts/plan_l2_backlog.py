#!/usr/bin/env python3
"""L2 スプリントバックログ（issue 相当）の Markdown 表を検証。stdlib のみ。"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

VALID_STATUS = frozenset({"open", "in_progress", "done", "blocked"})
PLACEHOLDER = frozenset({"—", "-", "issue", ""})


@dataclass
class BacklogItem:
    issue: str
    status: str
    title: str
    evidence: str


def parse_backlog(path: Path) -> list[BacklogItem]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    items: list[BacklogItem] = []
    in_section = False
    for line in text.splitlines():
        if line.strip() in ("## バックログ", "## Backlog"):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section or not line.startswith("|"):
            continue
        if re.match(r"^\|[\s\-:|]+\|$", line.strip()):
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) < 4:
            continue
        iid, status, title, evidence = cols[0], cols[1], cols[2], cols[3]
        if iid.lower() in PLACEHOLDER or status.lower() in PLACEHOLDER:
            continue
        items.append(
            BacklogItem(
                issue=iid,
                status=status.lower(),
                title=title,
                evidence=evidence,
            )
        )
    return items


def validate_backlog(items: list[BacklogItem]) -> list[str]:
    issues: list[str] = []
    in_prog = 0
    seen: set[str] = set()
    for it in items:
        if it.issue in seen:
            issues.append(f"duplicate issue: {it.issue}")
        seen.add(it.issue)
        if it.status not in VALID_STATUS:
            issues.append(f"{it.issue}: invalid status '{it.status}'")
        if it.status == "in_progress":
            in_prog += 1
        if it.status == "done" and not it.evidence.strip():
            issues.append(f"{it.issue}: done without evidence")
    if in_prog > 1:
        issues.append(f"more than one in_progress ({in_prog})")
    return issues


def check_file(path: Path) -> int:
    if not path.is_file():
        print(f"MISSING: {path}")
        return 1
    items = parse_backlog(path)
    issues = validate_backlog(items)
    if issues:
        print(f"L2 backlog check FAILED: {path}")
        for i in issues:
            print(" -", i)
        return 1
    print(f"L2 backlog OK: {path} items={len(items)}")
    return 0


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    default = root / "docs" / "plans" / "BACKLOG.example.md"
    p = argparse.ArgumentParser(description="Validate L2 sprint backlog table")
    p.add_argument("path", nargs="?", type=Path, default=default)
    return check_file(p.parse_args().path)


if __name__ == "__main__":
    sys.exit(main())
