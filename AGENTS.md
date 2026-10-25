# AGENTS.md — wawoo-skills エージェント契約

このリポジトリは、AI コーディングエージェント向けの**再利用可能な skills／agents／workflows／MCP サーバ**を集めた**汎用キット**です。特定プロダクトには依存しません。

---

## 1. 作業言語・基本

- 応答・計画・文書は**日本語**（コード・パス・コマンド・識別子・引用は原文のまま）。
- 変更前に**現状を確認**（`git status`・関連ファイル）。既存の未コミット変更を**勝手に破棄しない**。
- **証拠に基づく**（推測と実測を区別する）。
- **記憶**：作業前に `memory`（`docs/memory/INDEX.md`）を想起し、決定・落とし穴を保存する。

---

## 2. 構成

```
.kilo/
  skills/<name>/SKILL.md   … スキル（55）
  agents/<name>.md         … エージェント（21）
  commands/<name>.md       … ワークフロー（13）
  CAPABILITIES.md          … 自動生成カタログ（手編集しない）
.cursor/
  rules/*.mdc              … Cursor 用アダプタ
  mcp.json                 … MCP 設定
mcp/server.py              … 能力 MCP サーバ（stdio）
scripts/{gen_capabilities,validate_assets}.py
docs/                      … 設計・運用手順・記憶
```

---

## 3. 呼び出しプロトコル（必須）

1. **入口＝Workflow**：Kilo は `/name`、Cursor は `@.kilo/commands/<name>.md`。
2. **候補選定＝カタログ／MCP**：`.kilo/CAPABILITIES.md` または MCP `capabilities`／`skill_search`。**全部読まない**。
3. **手順＝Skill**：Workflow が挙げた skill を**必要分だけ** `skill_get`／`@.kilo/skills/<name>/SKILL.md` で開く。
4. **出力＝スキーマ**：Workflow の出力形に従う。ゲート（承認・証拠・失敗観察）を飛ばさない。
5. **記憶**：作業前に `memory_recall`（または `docs/memory/`）、決定後に保存。
6. **検証**：`python3 scripts/validate_assets.py` ＋ lint/テスト。

---

## 4. コンテキスト予算（モデルへの渡し方）

- 契約 ≤500tok／カタログ ≤1k／Workflow ≤1.5k／**Skill 1 個 ≤2〜4KB**（例外あり）／Memory top-5。
- **段階的開示**：全部を一度に渡さない。Reference は必要時のみ。
- **予算例外**（入口 `SKILL.md` のみ先読み、詳細は `references/`）：`imagegen-frontend-mobile`・`ask-matt`・`wayfinder`・`design-brief`・`writing-for-agents`（一覧は `docs/audit/SKILL-QUALITY-REVIEW.md`）。
- 大きいツール結果は**要約＋ID**。矛盾を置かない（SSOT 1 つ）。

---

## 5. ツール別

- **Kilo**：`.kilo/` を自動探索（skills/agents/commands）＋ `kilo.json`。**ネイティブ起動可**。
- **Cursor**：`AGENTS.md`＋`.cursor/rules`＋**MCP**＋`@file`。**slash command／agent／SKILL のネイティブ実行は無い**。
- 詳細：`docs/USAGE.md`。

---

## 6. 実行可能性（Readiness）

- 外部前提：`scripts/readiness.json` に記載（例：issue tracker）。
- `to-spec`/`to-tickets`/`triage` は issue tracker 設定が必要。未設定は標準フローに載せない。MCP `capabilities {ready_only:true}` で除外可能。
- 詳細：`scripts/readiness.json`。

---

## 7. スキルの追加・更新

- 追加時：`.kilo/skills/<name>/SKILL.md` に `name`／`description` を必須。
- カタログ再生成：`python3 scripts/gen_capabilities.py`（**手編集禁止**）。
- 検証：`python3 scripts/validate_assets.py`（name=dir・参照・重複・JSON）。
- エージェントとコマンドの参照（`agent:`）を壊さない。

---

## 8. ガードレール

- 秘密（API キー・トークン）を**コミットしない**。`memory_save` は秘密を拒否。
- 破壊的変更・本番・外部送信・公開は**承認必須**。
- ライセンス：同梱の `LICENSES/` と `.kilo/skills/ATTRIBUTION.md` を尊重。**ライセンス未確認の第三者資産**を再配布しない。
- 証拠（コマンド・結果）を残し、未検証を明示する。

---

## 9. バージョン管理

- **`VERSION`**（リポジトリ直下）が唯一の正本。**SemVer**（`MAJOR.MINOR.PATCH`）。
- 変更時は **`CHANGELOG.md`** を更新し、`VERSION` を上げる。
  - 削除・改名・MCP ツールの破壊的変更 = **MAJOR**
  - skill/agent/command の追加・後方互換の追加 = **MINOR**
  - 誤字・文言・内部リファクタ = **PATCH**
- リリース時は `v<version>` タグを付ける（例 `v0.1.0`）。
- 詳細：`docs/VERSIONING.md`。

---

## 10. 更新履歴

| 日付 | 内容 |
|---|---|
| 2026-10-25 | 汎用キットとして初版（既存プロジェクトから抽出・一般化） |
