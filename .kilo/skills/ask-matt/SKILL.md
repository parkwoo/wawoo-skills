---
name: ask-matt
description: Ask which skill or flow fits your situation. A router over the skills in this repo.
disable-model-invocation: true
---
# Ask Matt（スキルルーター）

このリポジトリ内の skill／フロー選定に使う。推奨前に**該当 skill の `SKILL.md` を開いて**確認する（本要約は orientation のみ）。

## コンテキスト予算

- 入口: 本 `SKILL.md` のみ（≤4KB 目安）。
- 詳細: 必要時だけ [`references/routing-map.md`](routing-map.md)。
- フェーズ境界: [`PHASE-BOUNDARIES.md`](../PHASE-BOUNDARIES.md)。

## クイックルート（wawoo-skills / Cursor）

| 状況 | 入口 |
|---|---|
| 機能を届ける | `@.kilo/commands/feature-delivery.md` |
| 調査→意思決定 | `@.kilo/commands/research.md` |
| 巨大で霧が厚い | `wayfinder` → 参照の on-ramp |
| issue tracker 未設定 | `setup-matt-pocock-skills` |

## 自動ルート（決定的・MCP）

キーワードや `/workflow` 明示から workflow を選ぶときは **本 skill を読む代わりに** MCP を使う（エージェントが確実に呼べる）。

1. `interpret_intent`（JSON）または `route_task`（人間向けテキスト）
2. `needs_scoring:true` なら **`upstream_prompt` で入力全文を読み、workflow 適合度を score 化**（思索オフ・JSON 1 行）: `{"workflow":"…","score":0.72,"trigger":"…"}`
3. 同ツールに `scoring` を渡して適用。**`learn:true` のときだけ** score ≥ 0.85 を DB へ非同期昇格（既定は learn オフ）
4. 返却の `workflow` で `workflow_get`
5. 曖昧・複合タスクは本 skill と [`references/routing-map.md`](routing-map.md)

常駐受信器は任意（`docs/design/INTENT-RECEIVER.md`）。CLI のみなら `scripts/task-router.py` または `scripts/wawoo-route.sh`。
