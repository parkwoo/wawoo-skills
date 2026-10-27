---
description: スプリント計画 L2（wayfinder → to-tickets → 優先度/見積/容量 → plan-md）
agent: project-manager
---

# Sprint Plan（スプリント計画）

**L2**: 進捗 SSOT は **issue tracker**（未設定時は `docs/plans/BACKLOG.example.md` 形式のローカル写し＋`plan_l2_backlog.py` 検証）。**`ACTIVE.md` を第二の進捗表にしない。**

1. **Readiness**: `to-tickets`／`triage` が使えるか `scripts/readiness.json` を確認。未設定なら issue 作成は止め、ローカルバックログ手順に切り替える。
2. **`wayfinder`**：大きな作業を**意思決定チケット**の地図にする（スコープ/依存/未決）。
3. **`to-tickets`**（可能なとき）：tracer-bullet チケットへ分解（blocking 関係を明示）。
4. **優先度・見積・容量**：優先順位、見積（**推測と根拠を区別**）、チーム容量、スコープ調整。
5. **`plan-md`**：スプリント計画を Markdown に保存（対象・非対象・リスク・受入）。
6. バックログ表を更新し `python3 scripts/plan_l2_backlog.py <path>` が通ること（Gₑ）。
7. 報告：計画・前提・リスク・**承認が必要な判断**。

## ゲート
- スコープ/納期の**事業判断は人が決める**。
- 破壊的変更・本番・外部送信は承認必須。
