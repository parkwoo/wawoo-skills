# wawoo-skills

AI コーディングエージェント向けの**再利用可能な skills／agents／workflows／MCP サーバ**の汎用キット。

## なぜこのキットか

エージェントに skill や役割（agent）定義を置いても、実際の対話では**散文だけで進め、手順を読まない・選ばない・飛ばす**ことがよく起きます。結果として、同じタスクでも品質がぶれ、レビュー・法務・テストなどの**ゲートが形骸化**し、チームが用意した知識が使われません。

wawoo-skills は、この「**能力はあるのに呼ばれない**」問題に対し、次のように**呼び出しを設計**します。

| 層 | 役割 |
|---|---|
| **契約**（`AGENTS.md`・Cursor rules） | 何を先に読み、何を勝手に省略しないかを固定 |
| **ワークフロー**（`.kilo/commands`） | プロセスの入口。どの skill をどの順で使うかを明示 |
| **カタログ／MCP** | 55 件を一度に渡さず、候補選定→必要分だけ取得（段階的開示） |
| **意図ルーティング** | `interpret_intent` で workflow 選定・学習 trigger・ツール権限ゲート（[docs/INTENT-ROUTING.md](docs/INTENT-ROUTING.md)） |
| **ゲート** | 承認・証拠・失敗観察。推測だけで「完了」にしない |

エージェントの創造性を奪うのではなく、**再現可能な手順とツール呼び出し**のレールを敷くためのキットです。

- 構造（Skill・Agent・ワークフロー）: **[docs/METHODOLOGY.md](docs/METHODOLOGY.md)**
- 工程（納品ライフサイクル・ゲート・学習）: **[docs/PROCESS-PHILOSOPHY.md](docs/PROCESS-PHILOSOPHY.md)**

## 対応環境

- **Kilo CLI / Kilo Code**：`.kilo/` の探索、slash ワークフロー（`/feature-delivery` 等）、`kilo.json` の MCP。
- **Cursor**：`AGENTS.md`・`.cursor/rules`・MCP、および `@.kilo/commands`／`@.kilo/skills` の参照（slash／ネイティブ agent 切替は非対応。手順は同等に適用）。

## 対応ツール（公式）

| ツール | 正式名 | 公式 URL |
|---|---|---|
| Kilo CLI | Kilo（CLI） | https://kilo.ai |
| Kilo Code | Kilo Code（VS Code 拡張） | https://kilocode.ai |
| Cursor | Cursor | https://cursor.com |
| MCP | Model Context Protocol | https://modelcontextprotocol.io |
| AGENTS.md | AGENTS.md | https://agents.md |

## 収録

| 種別 | 件数 | 場所 |
|---|---|---|
| Skills | **55** | `.kilo/skills/<name>/SKILL.md` |
| Agents | **21** | `.kilo/agents/<name>.md` |
| Workflows | **15** | `.kilo/commands/<name>.md`（コード L1: `/delivery-lite`、知識 L1: `/content-delivery-lite`） |
| MCP サーバ | 1 | `mcp/server.py`（stdio・stdlib のみ） |
| Cursor ルール | 3 | `.cursor/rules/*.mdc` |

- カタログ（自動生成）：`.kilo/CAPABILITIES.md`
- Readiness（外部前提）：`scripts/readiness.json`
- 呼び出し・コンテキスト設計：`docs/USAGE.md`
- 意図ルーティング（対外）：`docs/INTENT-ROUTING.md`

## クイックスタート

### Kilo
```bash
# このディレクトリを開く（.kilo/ を自動探索、kilo.json で MCP 有効）
```
- ワークフロー：`/feature-delivery` など
- スキル：`/` やモデルが `SKILL.md` を選択

### Cursor
1. このディレクトリを開く（`AGENTS.md` と `.cursor/rules` を読む）
2. **Settings → MCP** で `wawoo-skills` を有効化（`.cursor/mcp.json`）
3. MCP で `interpret_intent`（入口選定）→ `workflow_get`／`skill_get` 等（[INTENT-ROUTING.md](docs/INTENT-ROUTING.md)）
- **slash command／agent は非対応**。手順は `@.kilo/commands/<name>.md` を開いて適用。
- 詳細：`docs/USAGE.md`

### MCP
```bash
python3 mcp/server.py        # stdio（通常はクライアントが起動）
python3 mcp/test_server.py   # スモークテスト
```

## 保守

```bash
python3 scripts/validate_assets.py   # 資産検証（name=dir・参照・重複・JSON）
python3 scripts/gen_capabilities.py  # カタログ再生成（手編集しない）
python3 mcp/test_server.py           # MCP スモーク
```

## ディレクトリ

```
.kilo/{skills,agents,commands,CAPABILITIES.md}
.cursor/{rules,mcp.json}
mcp/{server.py,intent_*.py,test_*.py,README.md}
scripts/{gen_capabilities.py,validate_assets.py,readiness.json,bootstrap-internal.sh}
docs/{USAGE.md,INTENT-ROUTING.md,VERSIONING.md,PUBLICATION.md,memory,plans,design}
internal.example/   … メンテナ用テンプレ（実体は internal/・git 外）
LICENSES/
AGENTS.md
kilo.json
```

## ライセンスと帰属（かんたん説明）

このリポジトリには、**自分で書いたもの**と、**他の人が公開しているもの**が混ざっています。

| 種類 | ライセンス | 場所 |
|---|---|---|
| このリポジトリで新しく書いた skill／agent／command／MCP | **MIT**（自由に使える。著作権表示を残す） | `LICENSE` |
| Skills For Real Engineers 由来の skill（21 件） | **MIT** | `LICENSES/skills-for-real-engineers-MIT.txt` |
| OpenDesign 由来の skill（10 件） | **Apache-2.0**（著作権表示と NOTICE を残す） | `LICENSES/open-design-Apache-2.0.txt` |
| Kilo Marketplace 由来の agent（6 件） | **Apache-2.0** | `LICENSES/kilo-marketplace-*` |
| その他（Kilo 組み込み skill 等） | 各ファイルの frontmatter／MIT | `.kilo/skills/ATTRIBUTION.md` |

- どのファイルがどこ由来かは `.kilo/skills/ATTRIBUTION.md` に一覧があります。
- **ライセンスが確認できないものは入れていません**（Marketplace の business 3 件と `fal-gen` は除外）。
- 保証はありません（**AS IS**）。使う前に、必要なら各ライセンスを確認してください。

### 収録元（公式）
| 収録元 | 公式 URL |
|---|---|
| Skills For Real Engineers（Matt Pocock） | https://github.com/mattpocock/skills ・ https://skills.sh/mattpocock/skills |
| OpenDesign | https://open-design.ai ・ https://github.com/nexu-io/open-design |
| Kilo Marketplace（Kilo エコシステム） | https://kilo.ai |
| Semantic Versioning | https://semver.org |

## 注意（最初に読む）

- **画像生成は付属していません**：`imagegen-frontend-mobile` は「どんな画像を作るか」の**指示文（プロンプト）だけ**です。実際の生成は OpenAI Images／fal／社内ツール等を別途使います。無い場合は**プロンプトのみ**納品します。
- **3 つの skill は issue tracker が必要**：`to-spec`・`to-tickets`・`triage` は GitHub Issues 等の tracker を前提にしています。初回に `setup-matt-pocock-skills` を実行して設定してください。
- **秘密を書かない**：API キー・トークン・`.env` の中身をコミットしないでください。`memory_save` は秘密を拒否します。
- **Cursor は slash command／agent 非対応**：`AGENTS.md`＋`.cursor/rules`＋MCP＋`@file` で使います（`docs/USAGE.md`）。

## バージョン

- 現在：**0.5.0**（`VERSION`）
- 変更履歴：`CHANGELOG.md`
- 版の付け方・リリース手順：`docs/VERSIONING.md`
