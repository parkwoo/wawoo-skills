---
name: memory
description: Persist and recall durable project knowledge (decisions, constraints, gotchas, recurring fixes) across sessions. Use before starting work and after a decision. File-based so it works in both Kilo and Cursor; use Kilo memory tools when available.
---

# Memory（記憶）

## 優先順（取得）
1. MCP `memory_recall`（あれば）
2. `docs/memory/` を直接読む
3. Kilo memory ツール（任意）

## 保存場所
- **ファイル**：`docs/memory/`
  - `docs/memory/INDEX.md`（一覧）
  - `docs/memory/<topic>.md`（決定・制約・落とし穴・再発する修正）
- Kilo の memory ツール（`kilo_memory_save`／`kilo_memory_recall`）が使える場合は併用。無い環境（Cursor）は**ファイルのみ**。

## いつ使うか
- **作業前**：`memory` を想起（既存の決定・制約・落とし穴を確認）。
- **再発する失敗**：原因と回避策を保存（observed failure）。

## 何を保存するか
- 決定（何を・なぜ・代替案・日付）／制約／落とし穴／再発修正／未決事項。
- **保存しない**：秘密・鍵・個人情報・本文ログ。

## 書き方
- 簡潔に。**出典**（ファイル/PR/設計書）をリンク。
- 変更時は追記（履歴を消さない）。

## 関連
- 引き継ぎ：`handoff`／計画：`plan-md`／改善：`retro`・`pdca-cycle`
