---
description: 自己修正（code-review → code-skeptic → diagnosing-bugs/tdd → 修正 → 検証）
agent: code-reviewer
---

# Self Review（自己修正）

1. `AGENTS.md` を読み、`memory` を想起（既存の決定・制約・落とし穴）。
2. **`code-review`**：変更を固定点から 2 軸（標準/仕様）でレビュー。
3. **批判レビュー**：`.kilo/agents/code-skeptic.md` の観点を適用して、前提・設計・テストの弱さを**批判的に**検証（Kilo では Task で `code-skeptic` に委譲してもよい。**command 実行中に agent を切り替える前提にはしない**）。
4. **`diagnosing-bugs`**：不具合/性能退行があれば原因を特定（推測で直さない）。
5. **`tdd`／`test-engineering`**：修正はテスト先行。回帰を追加。
6. 修正 → **再検証**（テスト・lint・型）。証拠を残す。
7. **`memory`**：再発しうる落とし穴と回避策を保存。

## ゲート
- 「動いた」だけで完了にしない（**未検証を明示**）。
- 破壊的変更・本番・削除は承認必須。
- セキュリティ境界は `security-review` を併用。
