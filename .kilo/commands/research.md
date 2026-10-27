---
description: 調査 → 意思決定（research → product-discovery → to-spec/to-tickets）
agent: product-owner
---

# Research（調査）

> **入口**: `/research`（本 command）が入口。手順本体は同名 skill **`research`**（`.kilo/skills/research/SKILL.md`）。skill はモデルが選択するもので、`/` の入口は本 command に固定する。

**L1**: 進捗は `docs/plans/ACTIVE.md` に調査タスク行を載せる（完了は証拠＝`docs/` へのリンク）。**L2** は issue／BACKLOG。

1. `docs/plans/ACTIVE.md` を読み、調査タスクを `todo` で追記（小さな確認だけなら L0 で省略可）。
2. **`research`**：一次情報に当たり、**事実と推測を分離**して調査結果を Markdown に残す（不確実性を捏造しない）。
3. **`research-decision-room`**（必要なら）：選択肢・根拠・リスクを構造化し、意思決定の材料を揃える。
4. **`product-discovery`**：ユーザー成果・受入基準・スコープ・未決事項を確定。
5. 必要に応じて **`to-spec`** / **`to-tickets`** で仕様・チケット化（**`plan-md`** で計画文書化）。
6. ACTIVE を `done` + 証拠。`python3 scripts/plan_active.py` で検証。
7. 報告：**証拠 / 推測 / 未検証**を区別し、意思決定と次アクションを示す。

## 注意
- 事業判断（価格・契約・法務）は**人が決める**。エージェントは選択肢と根拠を提示するに留める。
- 調査結果は `docs/` に残す場合、秘匿情報（個人情報・鍵）を含めない。
