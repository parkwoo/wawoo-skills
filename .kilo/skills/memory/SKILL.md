---
name: memory
description: Persist and recall durable project knowledge (decisions, constraints, gotchas, recurring fixes) across sessions. Use before starting work and after a decision. File-based so it works in both Kilo and Cursor; use Kilo memory tools when available.
---

# Memory（記憶）

## 優先順（取得・保存）

詳細表: `docs/memory/MEMORY-TOOLS.md`

| 操作 | 順位 |
|------|------|
| **取得** | 1. MCP `memory_recall` → 2. `INDEX.md` → 3. `<topic>.md` → 4. Kilo recall（矛盾時はファイルが正） |
| **保存** | 1. MCP `memory_save` → 2. 手動追記（`TEMPLATE.md`）→ 3. Kilo save（ファイルへ同期） |

## 保存場所

- `docs/memory/INDEX.md` — 索引（セクション別一行＋履歴）
- `docs/memory/<topic>.md` — トピック別の詳細（`### MEM-YYYYMMDD-NNN` 形式）
- MCP `memory_save`: **両方に追記**（`tags` で種別と `topic:name`）

### MCP 引数

- `text`（必須）: 本文
- `tags`: `decision|constraint|gotcha|fix|open` と `topic:名前`（例 `decision,topic:kit`）
- `source`: 出典（ファイル・PR・URL）

## いつ使うか

- **作業前**（WARO の W 前）: 想起 — 特に `/feature-delivery`・`/self-review` の入口。
- **ゲート後・納品前**: 新しい決定・制約・落とし穴を保存（PROCESS P4／D7）。
- **再発する失敗**: 原因と回避策（observed failure）。

## 何を保存するか

- 決定（何を・なぜ・代替案・日付）／制約／落とし穴／再発修正／未決事項。
- **保存しない**: 秘密・鍵・個人情報・本文ログ。

## 書き方

- `docs/memory/TEMPLATE.md` の最小フォーマット。
- 簡潔に。**出典**を必ず付ける。
- 変更時は追記（履歴を消さない）。

## 関連

- 引き継ぎ：`handoff`／計画：`plan-md`／改善：`retro`・`pdca-cycle`
- 工程: `docs/PROCESS-PHILOSOPHY.md` §11 P4
