# Memory Index

このリポジトリの**永続知識**（決定・制約・落とし穴・再発修正）の索引。`memory` スキルが参照する。

- 形式: `docs/memory/TEMPLATE.md`
- ツール優先順: `docs/memory/MEMORY-TOOLS.md`
- 追記式（履歴を消さない）。
- **秘密・個人情報・本文ログは書かない**。

## 決定
- （例）このリポジトリは skills／agents／workflows／MCP の汎用キット。
- （例）プロセスは workflows（commands）が所有し、Skill は参照知。
- `MEM-20261025-001` 記憶の正本は `docs/memory/` の Markdown（Kilo 内蔵メモリは補助）。
- `MEM-20261025-002` タスク進捗の正本は `docs/plans/ACTIVE.md`（memory に完了ログは書かない）。

## 制約・落とし穴
- （例）Cursor は slash command／agent／SKILL をネイティブ実行しない。
- （例）一部スキルは issue tracker 設定が必要（`scripts/readiness.json`）。

## 再発しうる修正
- （例）Skill 追加時は `name`／`description` を付け、`name=dir` を守る。
- （例）`validate_assets.py` を通す（`docs/memory/` の秘密パターンも検査）。

## 未決
- （記入）
- `MEM-20261026-001` after clear
- `MEM-20261026-002` after clear
- `MEM-20261026-003` after clear
## 履歴
- 2026-10-25 テンプレート作成。
- 2026-10-25 memory P0–P2 強化（MCP↔skill 一致・テンプレ・検証・工程配線）。
- 2026-10-26 追記 `MEM-20261026-001`（未決）。
- 2026-10-26 追記 `MEM-20261026-002`（未決）。
- 2026-10-26 追記 `MEM-20261026-003`（未決）。
