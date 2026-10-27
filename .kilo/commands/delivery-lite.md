---
description: Lightweight delivery — SSOT plan file state machine, minimal ceremony (L0–L1). Default for single-feature requests without full feature-delivery.
agent: implementer
---

# Delivery Lite（軽量納品）

**目的**: 依頼を分析し、`docs/plans/ACTIVE.md` で進捗を管理し、実装・検証まで行う。**会話で毎回手順を説明しない**（AGENTS §3・本 workflow がデフォルト）。

## 適用レベル

- **L0**: 単一ファイル・明確な修正 → ACTIVE を更新せず実装のみ可（利用者が「L0」と言った場合）。
- **L1（既定）**: 本 workflow。ACTIVE が SSOT。
- **L2 以上**: `/sprint-plan`・issue tracker・`/feature-delivery` にエスカレート（容量・法務・本番が関わるとき）。

## 手順

0. **MCP で本 workflow を取得**: `wawoo-skills_workflow_get {name:"delivery-lite"}` を呼び、返った手順に従う（MCP が接続不能なときだけ本ファイルを正本とする）。
1. `AGENTS.md` §3（SSOT）と `docs/plans/ACTIVE.md` を読む。`git status` で未関係変更を壊さない。
2. **Memory（入口・短く）**: 依頼が既存の制約に触れるときだけ `memory_recall` または `docs/memory/INDEX.md`。
3. **計画**: 依頼を分解し、ACTIVE の表に `id`・`todo`・内容・完了条件を追記。複雑なら `plan-md` で `docs/plans/<id>.md` を作り ACTIVE にリンク。
4. **実行**: 先頭の `todo` を `doing` にし、1 件ずつ。実装は `implement`／`engineering-quality` を必要分だけ。
5. **検証**: 該当テスト・lint。キット本体を触った場合は `python3 scripts/validate_assets.py` と `python3 scripts/e2e_flows.py`。ACTIVE を更新したら `python3 scripts/plan_active.py docs/plans/ACTIVE.md`（**Gₑ**: 証拠なし `done` は CLI が落とす）。
6. **完了**: `doing` → `done`、証拠を埋める。メタの最終更新日を今日に。上記 check が通ることを確認。
7. **Memory（出口）**: 新しい**決定・制約・落とし穴**だけ `memory_save`（タスク完了の記録は ACTIVE のみ）。
8. **コミット・push・デプロイ**: 利用者が**明示したときのみ**（毎タスク必須ではない）。

## 出力

- 更新された `docs/plans/ACTIVE.md`（必須）
- 変更コードと証拠の要約（チャットは短く。詳細は ACTIVE）

## ゲート

- **Gₐ**: 破壊的変更・本番・外部送信・契約は停止して承認。
- **Gₑ**: `done` に証拠なしの完了宣言は禁止。
- **Gₒ**: 失敗したら原因を ACTIVE の該当行または memory に残しから再試行。
