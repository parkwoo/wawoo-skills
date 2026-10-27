---
description: 進捗・状況報告（ACTIVE または triage/to-tickets → 進捗・リスク → plan-md）
agent: project-manager
---

# Status Report（進捗・状況報告）

1. **SSOT**: **L1** は `docs/plans/ACTIVE.md` を読む。**L2** は issue tracker（`triage`／`to-tickets`）。二重の進捗表は作らない。
2. **`triage`／`to-tickets`**（L2 またはブロッカー整理時）：作業項目の現状とブロッカーを整理。
3. **進捗**：完了・進行・遅延を**証拠**（PR/コミット/テスト結果/ACTIVE の証拠列）で示す。未確認は未確認と明記。
4. **リスク・次アクション**：遅延要因と承認が必要な判断を列挙。
5. **`plan-md`**：状況報告を Markdown に保存（期間・指標・次アクション）。
6. 報告：**進捗 / リスク / ブロッカー / 次の承認事項**。

## ゲート
- 数値・日付は**推測で断定しない**（実測/未検証を区別）。
- 事業判断・契約・法務は人が決める。
- 破壊的変更・本番・削除は承認必須。
