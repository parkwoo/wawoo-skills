#!/usr/bin/env python3
"""実機 E2E の dry モード: エージェントが行うべき ACTIVE/CONTENT 更新を決定的に適用。"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def apply_delivery_lite_active(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    row = (
        "| E2E-LIVE-1 | done | delivery-lite 実機 dry | plan_active 通過 | "
        "python3 scripts/plan_active.py（sandbox） |\n"
    )
    text = text.replace("| — | — | （プレースホルダ） | | |", row)
    if row.strip() not in text:
        raise RuntimeError("placeholder row not found; reset sandbox fixture")
    path.write_text(text, encoding="utf-8")


def apply_content_lite(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    row = (
        "| CH-LIVE-1 | done | content-delivery-lite 実機 dry | 稿あり | "
        "docs/plans/evidence/sandbox/draft-ch-live-1.md |\n"
    )
    text = text.replace("| — | — | （プレースホルダ） | | |", row)
    if row.strip() not in text:
        raise RuntimeError("placeholder row not found; reset sandbox fixture")
    path.write_text(text, encoding="utf-8")
    draft = path.parent / "draft-ch-live-1.md"
    draft.write_text("# draft\n\ne2e stub\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--workflow", choices=("delivery-lite", "content-delivery-lite"), required=True)
    p.add_argument("--path", type=Path, required=True)
    args = p.parse_args()
    if not args.path.is_file():
        print(f"MISSING {args.path}", file=sys.stderr)
        return 1
    if args.workflow == "delivery-lite":
        apply_delivery_lite_active(args.path)
    else:
        apply_content_lite(args.path)
    print(f"dryrun applied: {args.workflow} -> {args.path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
