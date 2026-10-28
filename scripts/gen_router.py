#!/usr/bin/env python3
"""Generate ROUTER.md — 意図→workflow のルーティング表（Kilo の instructions 用）。

`mcp/intent_catalog.py` の WORKFLOWS と `.kilo/commands/*.md` の frontmatter を
唯一の入力とし、エージェントのコンテキストへ毎回載せる短い表を出力する。
出力先は既定でグローバル設定ディレクトリ（$KILO_GLOBAL_DIR または ~/.config/kilo）。

使い方:
  python3 scripts/gen_router.py                     # 既定の出力先へ書く
  python3 scripts/gen_router.py --out /path/ROUTER.md
  python3 scripts/gen_router.py --print             # stdout のみ
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mcp"))

from intent_catalog import TRIGGER_KEYWORDS, WORKFLOW_PHASES, WORKFLOWS  # noqa: E402


def triggers_for(workflow_id: str, limit: int = 3) -> str:
    """発火語の表示（正本は intent_catalog.TRIGGER_KEYWORDS＝L1 分類器と同一）。"""
    words = TRIGGER_KEYWORDS.get(workflow_id) or ()
    return " / ".join(words[:limit]) or "—"


def command_description(stem: str) -> str:
    path = ROOT / ".kilo" / "commands" / f"{stem}.md"
    if not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8", errors="ignore")
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return ""
    for line in m.group(1).splitlines():
        fm = re.match(r"^description:\s*(.*)$", line)
        if fm:
            return fm.group(1).strip()
    return ""


def render() -> str:
    lines: list[str] = [
        "# ROUTER — 意図 → workflow（自動生成・手編集禁止）",
        "",
        "生成: `python3 scripts/gen_router.py`（kit: wawoo-skills）。",
        "",
        "## 手順（エージェント必須）",
        "",
        "**非自明な依頼（コード変更・調査・設計・文書生成）では、ツールを使う前に必ず MCP を呼ぶ。**",
        "ネイティブ `skill` ツールや記憶した手順で代替したら本契約違反。",
        "",
        "1. まず下の表で **workflow を 1 つ**選ぶ（複数該当なら上の行を優先）。",
        "2. **必ず** MCP `wawoo-skills_workflow_get` を呼び、返った手順を読む（`/name` 入力は不要・待たない）。",
        "3. どれか判断できないときだけ先に `wawoo-skills_interpret_intent` を `text` 付きで呼ぶ。"
        "`needs_scoring:true` なら `workflow_catalog` から 1 つ選び、`scoring` を付けて**同じターンで再呼び出し**する。",
        "4. 手順が挙げる skill だけ `wawoo-skills_skill_get` で開く。全部開かない。"
        "MCP が接続不能な場合に限りネイティブ `skill` を使い、その旨を報告する。",
        "",
        "## 表",
        "",
        "| workflow | 推奨 agent | 発火語（例） | 内容 |",
        "|---|---|---|---|",
    ]
    for wid in sorted(WORKFLOWS):
        spec = WORKFLOWS[wid]
        trig = triggers_for(wid)
        desc = command_description(wid) or spec.description
        in_table = desc.replace("|", "/")
        cells = (trig, in_table)
        padded = []
        for cell in cells:
            head = cell[:60]
            padded.append(head + "…" if len(cell) > 60 else head)
        lines.append(f"| `{wid}` | {spec.agent} | {padded[0]} | {padded[1]} |")
    lines += [
        "",
        "## フェーズ（分解・要点）",
        "",
        "`workflow_get {name, phase:<id>}` で phase の goal／agent／skills／`mcp_tools_allow`／`exit_criteria` を取得。",
        "監査系（`design-review`・`compliance-review`・`release-review`・`self-review`）に `implement` は無い → 実装が必要なら**切替を宣言**する。",
        "",
    ]
    grouped: dict[tuple[str, ...], list[str]] = {}
    for wid in sorted(WORKFLOWS):
        ids = WORKFLOW_PHASES.get(wid, ())
        if ids:
            grouped.setdefault(tuple(ids), []).append(wid)
    for seq, wids in sorted(grouped.items(), key=lambda kv: (-len(kv[0]), kv[0])):
        arrow = " → ".join(f"`{i}`" for i in seq)
        lines.append(f"- {arrow}: {', '.join('`'+w+'`' for w in wids)}")
    lines += [
        "",
        "## 運用ゲート（衛生）",
        "",
        "- **1 セッション = 1 対象／1 成果物**。独立した複数対象は Task（subagent）で分割。目標: payload < 600KB。",
        "- **workflow 切替は 1 行で宣言**（理由＋新 workflow）し、成果物を分離する（監査と実装を混在させない）。",
        "- **失敗は収束**: 修正するか、既知失敗として明示＋追跡（チケット／ACTIVE）。未収束 `FAILED` を残さない。",
        "- **後始末**: テスト／起動後に `docker compose ... down -v` 等で停止し、`docker ps` で残留 0 を確認。",
        "- **記憶**: 決定・制約・落とし穴を完了時に最低 1 件記録（キット内は `memory_save`）。",
        "- **トークン衛生**: `grep -n`/`head`/`sed -n` を使い、長セッションは `/compact`。1 step の出力 < 4KB。",
        "- **ローカル検証**: PR／公開前に `validate_assets.py`（＋該当時 `e2e_flows.py`）を実行し結果を残す。",
        "",
        "## 制約",
        "",
        "- **SSOT の読み替え**: kit の `docs/plans/ACTIVE.md` 等が無いプロジェクトでは、"
        "そのプロジェクト既存の計画／タスク管理に読み替える（`docs/plans/` を勝手に作らない）。",
        "- 進捗は各 workflow の SSOT に書く。**memory は決定・制約・落とし穴のみ**（タスク完了ログは書かない）。",
        "- 破壊的変更・本番・外部送信・公開は停止して承認を得る。",
        "- このファイルは自動生成。編集は `scripts/gen_router.py` 側で行う。",
        "",
    ]
    return "\n".join(lines)


def default_out() -> Path:
    env = os.environ.get("KILO_GLOBAL_DIR", "").strip()
    base = Path(env).expanduser() if env else Path.home() / ".config" / "kilo"
    return base / "ROUTER.md"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="出力パス（既定: $KILO_GLOBAL_DIR/ROUTER.md）")
    ap.add_argument("--print", dest="to_stdout", action="store_true", help="stdout に出すだけ")
    args = ap.parse_args()

    text = render()
    if args.to_stdout:
        print(text)
        return 0
    out = Path(args.out).expanduser() if args.out else default_out()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"OK  wrote {out} ({len(text)} bytes, {text.count(chr(10))} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
