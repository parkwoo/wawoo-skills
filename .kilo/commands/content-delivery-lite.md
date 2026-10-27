---
description: L1 knowledge delivery — books, long docs, reports via CONTENT.md state machine (not code implement).
agent: docs-specialist
---

# Content Delivery Lite（知識・長文納品）

**目的**: 調査レポート・事業計画書・書籍章など**コード以外**の納品を `docs/plans/CONTENT.md` で管理する。`/delivery-lite` の知識向け変種。

## 適用

- **L1（既定）**: 本 workflow + `CONTENT.md`
- **L0**: 単節・メモ → SSOT 更新省略可（利用者が「L0」）
- **戦略・市場**: 大きい場合は `/market-plan` または `/research` を入口にし、成果を `plan-md` + CONTENT 行でリンク
- **L2/L3**: `/sprint-plan`・`/self-improve`（工程のみ）

## 手順

1. `AGENTS.md` §3 と `docs/plans/CONTENT.md`（無ければ `CONTENT.example.md` をコピー）を読む。
2. **Memory（入口）**: 制約に触れるときだけ `memory_recall` または `docs/memory/INDEX.md`。
3. **目次**: 章・節を CONTENT 表に `todo` で追記。構成は `plan-md` で `docs/plans/<id>-outline.md` にも可。
4. **執筆**: `doing` を 1 件にし、`writing-for-agents`／`documentation-localization` を必要分だけ。
5. **検証**: `python3 scripts/plan_content.py docs/plans/CONTENT.md`。キット変更時は `python3 scripts/e2e_flows.py`。
6. **完了**: `done` + 証拠（稿のパス、字数、レビュー日）。memory は**決定・文体ルール**のみ。
7. **コミット**: 利用者が明示したときのみ。

## 出力

- 更新された `CONTENT.md` と原稿ファイル
- チャットは要約のみ

## ゲート

- **Gₐ**: 公開・契約・第三者素材の権利は承認。
- **Gₑ**: 証拠なし `done` 禁止（`plan_content.py`）。
- **Gₒ**: 事実と推測を分離（調査系は `/research` と同様）。
