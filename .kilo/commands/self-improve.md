---
description: 自己改善（retro → pdca-cycle → self-review → plan-md）
agent: project-manager
---

# Self Improve（自己改善）

1. `AGENTS.md` を読み、`memory` を想起（過去の決定・失敗・回避策）。
2. **`retro`**：この反復の**事実**（何をした・何が起きた・期待との差）を振り返る。
3. **`pdca-cycle`**：Plan → Do → Check → Act で**改善アクション**を決める（測定可能に）。
4. 必要なら**自己修正の手順を展開**（`code-review`→（`.kilo/agents/code-skeptic.md` の観点）→`tdd`）で技術的負債を解消。
5. 必要なら **`.kilo/agents/code-simplifier.md` の観点**で複雑さを下げる（挙動を変えない。Task 委譲可）。
6. **`plan-md`**：改善計画を Markdown に保存（**担当・期限・指標**）。
7. **`memory`**：学び・再発防止を保存。次回の `retro` で効果を確認。

## ゲート
- 改善は**証拠**（メトリクス・失敗ログ）に基づく。推測で「改善した」と言わない。
- 事業判断・契約・法務は人が決める。
- 破壊的変更・本番・削除は承認必須。
