#!/usr/bin/env python3
"""Validate and order the Markdown table of an L2 sprint backlog (issue-like). stdlib only.

検証:
  - valid status; at most one in_progress; done requires evidence
  - dependencies (`depends` column) exist and there are no cycles
  - **row order satisfies dependencies (topological order)** (no dual ordering)

整列:
  - `--apply` reorders rows by dependency (content/evidence unchanged = order only)

列: `issue | status | title | evidence | depends`
  `depends` = comma-separated issue ids (`OS-*`). Decisions (`D3`, etc.) and `—` are ignored.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

VALID_STATUS = frozenset({"open", "in_progress", "done", "blocked"})
PLACEHOLDER = frozenset({"—", "-", "issue", ""})
ID_RE = re.compile(r"^[A-Za-z]+-[0-9A-Za-z]+$")  # 例: OS-1a, MEM-2
SEP_RE = re.compile(r"^\|[\s\-:|]+\|$")


@dataclass
class BacklogItem:
    issue: str
    status: str
    title: str
    evidence: str
    depends: tuple[str, ...] = field(default_factory=tuple)


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _parse_depends(cell: str) -> tuple[str, ...]:
    if cell.strip() in PLACEHOLDER:
        return ()
    out: list[str] = []
    for tok in re.split(r"[,\s、]+", cell.strip()):
        tok = tok.strip("`* ")
        # Count only issue ids (e.g. OS-1a) as dependencies. Decisions (D3 etc.) are ignored.
        if tok and ID_RE.match(tok):
            out.append(tok)
    return tuple(out)


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
        if SEP_RE.match(line.strip()):
            continue
        cols = _cells(line)
        if len(cols) < 4:
            continue
        iid, status, title, evidence = cols[0], cols[1], cols[2], cols[3]
        depends = _parse_depends(cols[4]) if len(cols) > 4 else ()
        if iid.lower() in PLACEHOLDER or status.lower() in PLACEHOLDER:
            continue
        items.append(
            BacklogItem(
                issue=iid,
                status=status.lower(),
                title=title,
                evidence=evidence,
                depends=depends,
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


def _topo_order(ids: list[str], deps: dict[str, list[str]]) -> list[str]:
    """Stable topological order. Tie-break by the original (input) order."""
    order: list[str] = []
    remaining = list(ids)
    while remaining:
        progressed = False
        for iid in list(remaining):
            ready = all(d not in remaining for d in deps.get(iid, []))
            if ready:
                order.append(iid)
                remaining.remove(iid)
                progressed = True
        if not progressed:  # cycle → append the rest in the original order
            order.extend(remaining)
            break
    return order


def analyze(items: list[BacklogItem]) -> tuple[list[str], list[str], list[str]]:
    """Return (hard_issues, expected_order, order_issue).

    hard_issues: unknown deps / cycles (not fixed by reordering)
    order_issue: row order does not match dependency order (fixed by reordering)
    """
    ids = [it.issue for it in items]
    idset = set(ids)
    deps = {it.issue: [d for d in it.depends if d in idset] for it in items}
    hard: list[str] = []
    for it in items:
        for d in it.depends:
            if d not in idset:
                hard.append(f"{it.issue}: unknown dependency '{d}'")
    expected = _topo_order(ids, deps)
    if set(expected) != set(ids):  # a cycle prevents ordering part of the list
        hard.append("dependency cycle detected among: " + " ".join(ids))
    order_issue = ""
    if not hard and expected != ids:
        order_issue = "row order violates dependency order; expected: " + " ".join(expected)
    return hard, expected, order_issue


def check_file(path: Path, apply: bool = False) -> int:
    if not path.is_file():
        print(f"MISSING: {path}")
        return 1
    items = parse_backlog(path)
    hard = validate_backlog(items)
    hard2, expected, order_issue = analyze(items)
    hard += hard2
    if apply:
        if hard:
            print(f"L2 backlog check FAILED: {path}")
            for i in hard:
                print(" -", i)
            return 1
        _reorder_file(path, expected)
        print(f"L2 backlog reordered: {path} items={len(items)}")
        return 0
    issues = hard + ([order_issue] if order_issue else [])
    if issues:
        print(f"L2 backlog check FAILED: {path}")
        for i in issues:
            print(" -", i)
        return 1
    print(f"L2 backlog OK: {path} items={len(items)}")
    return 0


def _reorder_file(path: Path, order: list[str]) -> None:
    """Rewrite the table data rows in `order` (content unchanged)."""
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    idx: list[int] = []
    for i, line in enumerate(lines):
        if not line.startswith("|") or SEP_RE.match(line.strip()):
            continue
        cols = _cells(line)
        if len(cols) < 4 or cols[0].lower() in PLACEHOLDER or cols[1].lower() in PLACEHOLDER:
            continue
        idx.append(i)
    rows = {_cells(lines[i])[0]: lines[i] for i in idx}
    ordered = [rows[o] for o in order if o in rows]
    if len(ordered) != len(idx):
        return
    for pos, i in enumerate(idx):
        lines[i] = ordered[pos]
    path.write_text("".join(lines), encoding="utf-8")


def check_file(path: Path, apply: bool = False) -> int:
    if not path.is_file():
        print(f"MISSING: {path}")
        return 1
    items = parse_backlog(path)
    hard = validate_backlog(items)
    hard2, expected, order_issue = analyze(items)
    hard += hard2
    if apply:
        if hard:
            print(f"L2 backlog check FAILED: {path}")
            for i in hard:
                print(" -", i)
            return 1
        _reorder_file(path, expected)
        print(f"L2 backlog reordered: {path} items={len(items)}")
        return 0
    issues = hard + ([order_issue] if order_issue else [])
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
    p = argparse.ArgumentParser(description="Validate/reorder L2 sprint backlog table")
    p.add_argument("path", nargs="?", type=Path, default=default)
    p.add_argument("--apply", action="store_true", help="reorder rows by dependency")
    a = p.parse_args()
    return check_file(a.path, apply=a.apply)


if __name__ == "__main__":
    sys.exit(main())
