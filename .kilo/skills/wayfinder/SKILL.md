---
name: wayfinder
description: Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on your issue tracker, and resolve them one at a time until the way to the destination is clear.
disable-model-invocation: true
---
# Wayfinder（巨大仕事の意思決定マップ）

一度のセッションに収まらない仕事を、issue tracker 上の**決定チケットの地図**として進める。各チケットは**成果物ではなく決定**を残す。

## コンテキスト予算

- 入口: 本 `SKILL.md` のみ。
- 全文手順: 必要時だけ [`references/wayfinding-guide.md`](wayfinding-guide.md)。
- tracker 未設定: `setup-matt-pocock-skills`。

## ゲート

- **Plan, don't do**（既定）: 地図は決定まで。実装は地図の外で `to-spec` / main flow に合流。
- 1 セッションで解決するチケットは**1 つ**（research 除く）。
- チケットは**名前**で参照（番号だけにしない）。
