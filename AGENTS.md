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
  agents/<name>.md         … エージェント（22）
  commands/<name>.md       … ワークフロー（15）
  CAPABILITIES.md          … 自動生成カタログ（手編集しない）
.cursor/
  rules/*.mdc              … Cursor 用アダプタ
  mcp.json                 … MCP 設定
mcp/server.py              … 能力 MCP サーバ（stdio）
scripts/{gen_capabilities,validate_assets}.py
docs/                      … 設計・運用手順・記憶
```

---

## 3. タスクと進捗の正本（SSOT）

**チャットで進捗を管理しない。** エージェントは次をデフォルトとする（利用者が毎回言わなくてよい）。

| 用途 | 正本 | 更新タイミング |
|------|------|----------------|
| **L1 進行中タスク（コード・UI・調査等）** | `docs/plans/ACTIVE.md` | 着手前に読む。`todo`→`doing`→`done` と証拠列のみエージェントが更新 |
| **L1 長文・書籍・レポート** | `docs/plans/CONTENT.md` | `/content-delivery-lite`。`plan_content.py` で検証 |
| **詳細計画** | `docs/plans/<id>.md`（`plan-md`） | 分解が大きいとき。ACTIVE の id とリンク |
| **L2 複数タスク・同期** | issue tracker（設定時）または `docs/plans/BACKLOG*.md` | `to-tickets`／`plan_l2_backlog.py`。ACTIVE と二重管理しない |
| **L3 プロセス改善** | `docs/plans/RETRO*.md` 等 + `memory` | `/self-improve`。`plan_l3_record.py` |
| **横断の決定・制約** | `docs/memory/` | タスク完了ではなく、再発する知識のみ |
| **監査（キット資産）** | CI／`validate_assets.py` | エージェントが口頭で「監査した」と言う代わりに実行 |

**儀式レベル（L0–L3）**: `docs/METHODOLOGY.md` §5。迷ったら **L1＋`/delivery-lite`**。本番・法務・大規模は `/feature-delivery` または L2 へ。

**git commit**: 利用者が依頼したときのみ（タスク `done` と commit は別）。

---

## 4. 呼び出しプロトコル（必須）

理論・設計判断: `docs/METHODOLOGY.md`（Skill／Agent／ワークフローの分担と WARO）。

**Kilo 実運用（強制・0 番）**: MCP `wawoo-skills` が接続されている環境では、コード変更・調査・設計・文書生成などの**非自明な依頼では、最初のツール呼び出しを `wawoo-skills_workflow_get`（判断不能なら `wawoo-skills_interpret_intent`）にする**。ネイティブ `skill` ツール（`plan-md` 等）や記憶で代替して作業を始めたら §4 違反として扱い、途中でも `workflow_get` に戻る。接続不能な場合のみネイティブを使い、その旨を報告する。

1. **入口＝Workflow**：通常は **`/delivery-lite`**（儀式 L1）。大規模・ゲート多めは `/feature-delivery`。Kilo は `/name`、Cursor は `@.kilo/commands/<name>.md`。依頼が曖昧なときは MCP **`interpret_intent`** → `schedule.workflow`（`docs/INTENT-ROUTING.md`）。`interpret_intent` が `needs_scoring` を返したら `scoring` を付けて再呼び出しする。
2. **候補選定＝カタログ／MCP**：`.kilo/CAPABILITIES.md` または MCP `capabilities`／`skill_search`。**全部読まない**。`interpret_intent` 後は **`mcp_tools_allow` 外のツールを呼ばない**（終了時 `workflow_clear`）。
3. **手順＝Skill**：Workflow が挙げた skill を**必要分だけ** `skill_get`／`@.kilo/skills/<name>/SKILL.md` で開く。phase があるときは `workflow_get {name, phase:<id>}` で goal／agent／skills／`exit_criteria` を取得し、`implement` を持たない workflow（監査系）では実装に進まず**切替を宣言**する。
4. **出力＝スキーマ**：Workflow の出力形に従う。ゲート（承認・証拠・失敗観察）を飛ばさない。
5. **記憶**：作業前に `memory_recall`（または `docs/memory/INDEX.md`）、決定・制約・落とし穴は `memory_save`（INDEX＋`docs/memory/<topic>.md`）。優先順は `docs/memory/MEMORY-TOOLS.md`。
6. **検証**：`python3 scripts/validate_assets.py` ＋ lint/テスト。

### 4.1 実行衛生・収束ゲート（キット共通・プロジェクト非依存）

対象は**この kit 自体**と、kit の規約を採用する各プロジェクト（特定プロダクトには依存しない）。

- **1 セッション = 1 対象／1 成果物**：独立した複数プロジェクトや複数成果物を 1 セッションに混在させない。混在しそうなら `Task`（subagent）で対象ごとに分割委譲する。**指標: payload < 600KB、cache_read を半減**。
- **Workflow 逸脱の明示**：途中で workflow を切り替えるときは、**切替理由と新 workflow を 1 行で宣言**し、成果物を分離する（例: 監査と実装を混在させない）。`plan-md`／ACTIVE に記録。**指標: 1 セッション 1 成果物**。
- **失敗の収束ゲート**：テスト失敗は「**修正する**」か「**既知の失敗として明示＋追跡**（チケット／ACTIVE 行）」のいずれかを必須。未収束の `FAILED` を残したまま完了報告しない。**指標: 未収束 FAILED = 0**。
- **クリーンアップ固定**：テスト・起動の後にコンテナ／プロセスを停止し、残留を確認する（例: `docker compose ... down -v` と `docker ps`）。**指標: 残留 0**。
- **記憶の保存**：決定・制約・落とし穴は完了時に記録する（キット内は `memory_save`、他プロジェクトはその既定の記録先へ）**最低 1 件**。タスク完了ログは SSOT 側のみ。
- **トークン衛生**：巨大 `cat`・全件ループを避け、`grep -n`/`head`/`sed -n` で必要行だけ読む。長セッションは `/compact`。**指標: 1 step のツール出力 < 4KB**。
- **サブエージェント委譲の効率**：`Task` で監査等を委譲するときは、必要な skill の要点を**タスク文に内联**し、子に同じ skill を `skill_get` で**再取得させない**。read-only subagent は `read` を行範囲に絞り（≤200 行）、`background_process` を使わない（短命令は shell 1 回）。**指標: 1 委譲チェーンの `skill_get` 重複 0、p95 read < 4KB**。
- **ローカル検証の担保**：PR／公開の前に `python3 scripts/validate_assets.py` と（該当時）`python3 scripts/e2e_flows.py` を**ローカルで実行し結果を残す**（CI が停止・課金等で使えない場合の代替）。

---

## 5. コンテキスト予算（モデルへの渡し方）

- 契約 ≤500tok／カタログ ≤1k／Workflow ≤1.5k／**Skill 1 個 ≤2〜4KB**（例外あり）／Memory top-5。
- **予算の目安（§4.1）**：1 step のツール出力 **< 4KB**、1 セッションの payload **< 600KB**。超えそうなら対象分割・`/compact`・`grep -n`/`head` へ切替。
- **段階的開示**：全部を一度に渡さない。Reference は必要時のみ。
- **予算例外**（入口 `SKILL.md` のみ先読み、詳細は `references/`）：`imagegen-frontend-mobile`・`ask-matt`・`wayfinder`・`design-brief`・`writing-for-agents`。
- 大きいツール結果は**要約＋ID**。矛盾を置かない（SSOT 1 つ）。

---

## 6. ツール別

- **Kilo**：`.kilo/` を自動探索（skills/agents/commands）＋ `kilo.json`。**ネイティブ起動可**。
- **Cursor**：`AGENTS.md`＋`.cursor/rules`＋**MCP**＋`@file`。**slash command／agent／SKILL のネイティブ実行は無い**。
- 詳細：`docs/USAGE.md`。

---

## 7. 実行可能性（Readiness）

- 外部前提：`scripts/readiness.json` に記載（例：issue tracker）。
- `to-spec`/`to-tickets`/`triage` は issue tracker 設定が必要。未設定は標準フローに載せない。MCP `capabilities {ready_only:true}` で除外可能。
- 詳細：`scripts/readiness.json`。

---

## 8. スキルの追加・更新

- 追加時：`.kilo/skills/<name>/SKILL.md` に `name`／`description` を必須。
- カタログ再生成：`python3 scripts/gen_capabilities.py`（**手編集禁止**）。
- 検証：`python3 scripts/validate_assets.py`（name=dir・参照・重複・JSON）。
- エージェントとコマンドの参照（`agent:`）を壊さない。

---

## 9. ガードレール

- 秘密（API キー・トークン）を**コミットしない**。`memory_save` は秘密を拒否。
- 破壊的変更・本番・外部送信・公開は**承認必須**。
- ライセンス：同梱の `LICENSES/` と `.kilo/skills/ATTRIBUTION.md` を尊重。**ライセンス未確認の第三者資産**を再配布しない。
- 証拠（コマンド・結果）を残し、未検証を明示する。

---

## 10. バージョン管理

- **`VERSION`**（リポジトリ直下）が唯一の正本。**SemVer**（`MAJOR.MINOR.PATCH`）。
- 変更時は **`CHANGELOG.md`** を更新し、`VERSION` を上げる。
  - 削除・改名・MCP ツールの破壊的変更 = **MAJOR**
  - skill/agent/command の追加・後方互換の追加 = **MINOR**
  - 誤字・文言・内部リファクタ = **PATCH**
- リリース時は `v<version>` タグを付ける（例 `v0.1.0`）。
- 詳細：`docs/VERSIONING.md`。

---

## 11. 更新履歴

| 日付 | 内容 |
|---|---|
| 2026-10-25 | 汎用キットとして初版（既存プロジェクトから抽出・一般化） |
| 2026-10-25 | §3 SSOT（ACTIVE・L0–L3）、既定入口 `/delivery-lite` |
| 2026-10-26 | §4 `interpret_intent`・ツールゲート・`docs/INTENT-ROUTING.md` |
| 2026-10-27 | §4 に MCP 先呼びを強制（`workflow_get`／`interpret_intent`）。Kilo の `instructions` は絶対パス必須（相対 `ROUTER.md` は注入されない）と判明し修正 |
| 2026-10-27 | 全 agent 定義（21）に `## Routing (MCP first)` を追加（subagent でネイティブ `skill` が先行する事象への対応） |
| 2026-10-27 | 既定 agent `wawoo-router` を新設（`default_agent` 既定）。`install_global.py` が `ROUTER.md` 生成・`instructions` 絶対パス登録・`default_agent` 設定を冪等に実施 |
| 2026-10-28 | §4.1「実行衛生・収束ゲート」を追加（セッション分割・workflow 逸脱の明示・失敗の収束・後始末・記憶・トークン衛生・ローカル検証） |
| 2026-10-28 | 意図ルーティングに **L1 トリガ分類器**を追加（ROUTER 発火語と同一正本・曖昧時は `needs_scoring`）。workflow を **phases** に分解し、`workflow_get {phase}`／`delegate_subtask {phase}` と監査系の `implement` 不在で逸脱を構造的に防止 |
| 2026-10-28 | kilo ログ分析（run `c956c7f2`）に基づく改善: §4.1 にサブエージェント委譲の効率（skill 重複排除・read-only read 規律）、read-only subagent へ実行効率節、`security-reviewer` に read-only bash サブセット、`memory_save` 可否を `capabilities` で明示、`self-improve` トリガ語追加、`scripts/kilo_snapshot_gc.sh` |
