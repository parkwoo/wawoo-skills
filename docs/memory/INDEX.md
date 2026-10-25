# Memory Index

このリポジトリの**永続知識**（決定・制約・落とし穴・再発修正）。`memory` スキルが参照する。
- 追記式（履歴を消さない）。**秘密・個人情報・本文ログは書かない**。
- 各項目は出典（ファイル/PR/URL）へリンク。

## 決定
- 本リポジトリは **skills／agents／workflows／MCP の汎用キット**。特定プロダクトに依存しない。
- プロセスは **workflows（commands）が所有**し、skills-main の思考法を埋め込む（`SKILLS-MAIN-ALIGNMENT.md`）。
- 公開のため **NOASSERTION／ライセンス不明の資産を除外**（`SKILLS-READINESS.md`）。

## 制約・落とし穴
- **Cursor は slash command／agent／SKILL をネイティブ実行しない**（`AGENTS.md`＋rules＋MCP＋`@file`）。
- `to-spec`/`to-tickets`/`triage` は **issue tracker 設定**が必要。
- `imagegen-frontend-mobile` は**プロンプト指針**（画像生成ツールは同梱しない）。
- `.cursor/mcp.json` は**絶対パス**（環境差で調整）。

## 再発しうる修正
- スキル追加時は `name`／`description` を必ず付け、`name=dir` を守る。
- 参照（command→agent）を壊さない。`validate_assets.py` を通す。
- 秘密をコミットしない。`memory_save` は秘密を拒否。

## 未決
- 計測（workflow 成功率・トークン・再試行）。
- 大規模 skill（`imagegen-frontend-mobile`）の要約モード。
- `design-review`／`research` の skill/command 同名（望むなら改名）。

## 履歴
- 2026-10-25 初版（汎用キット）。
