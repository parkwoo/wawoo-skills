#!/usr/bin/env python3
"""docs/plans/CONTENT.md（長文・書籍・章単位）の目次表を検証。ACTIVE と同型の状態機械。"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

VALID_STATUS = frozenset({"todo", "doing", "done", "blocked"})
PLACEHOLDER_IDS = frozenset({"—", "-", "id", ""})


@dataclass
class ContentUnit:
    id: str
    status: str
    title: str
    acceptance: str
    evidence: str


def parse_content(path: Path) -> list[ContentUnit]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    units: list[ContentUnit] = []
    in_section = False
    for line in text.splitlines():
        if line.strip() in ("## 目次", "## 章・節"):
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
        uid, status, title, acceptance, evidence = cols[0], cols[1], cols[2], cols[3], cols[4]
        if uid.lower() in PLACEHOLDER_IDS or status.lower() in PLACEHOLDER_IDS:
            continue
        units.append(
            ContentUnit(
                id=uid,
                status=status.lower(),
                title=title,
                acceptance=acceptance,
                evidence=evidence,
            )
        )
    return units


def validate_content(units: list[ContentUnit]) -> list[str]:
    issues: list[str] = []
    doing = 0
    seen: set[str] = set()
    for u in units:
        if u.id in seen:
            issues.append(f"duplicate id: {u.id}")
        seen.add(u.id)
        if u.status not in VALID_STATUS:
            issues.append(f"{u.id}: invalid status '{u.status}'")
        if u.status == "doing":
            doing += 1
        if u.status == "done" and not u.evidence.strip():
            issues.append(f"{u.id}: done without evidence")
    if doing > 1:
        issues.append(f"more than one doing ({doing})")
    return issues


def check_file(path: Path) -> int:
    if not path.is_file():
        print(f"MISSING: {path}")
        return 1
    units = parse_content(path)
    issues = validate_content(units)
    if issues:
        print(f"CONTENT check FAILED: {path}")
        for i in issues:
            print(" -", i)
        return 1
    print(f"CONTENT OK: {path} units={len(units)}")
    return 0


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    default = root / "docs" / "plans" / "CONTENT.example.md"
    p = argparse.ArgumentParser(description="Validate CONTENT.md outline table (L1 knowledge)")
    p.add_argument("path", nargs="?", type=Path, default=default)
    return check_file(p.parse_args().path)


if __name__ == "__main__":
    sys.exit(main())
