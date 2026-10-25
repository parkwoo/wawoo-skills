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
