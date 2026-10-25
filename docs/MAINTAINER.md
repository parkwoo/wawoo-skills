# メンテナ向け（公開 README には載せない）

リポジトリ公開用の入口は [README.md](../README.md)。ここは**開発・監査・実測**用。

## スモーク（API キー不要）

```bash
./scripts/e2e/smoke.sh
# または
python3 scripts/validate_assets.py && python3 mcp/test_server.py
```

## Docker（L1）

```bash
./scripts/e2e/install-compose-v2.sh   # `docker compose` プラグイン
./scripts/e2e/compose.sh run --rm smoke
```

## CLI 実測

| 文書 | 内容 |
|---|---|
| [audit/CLI-E2E-ENV.md](./audit/CLI-E2E-ENV.md) | Kilo CLI / Cursor `agent` / Docker |
| [audit/KILO-E2E.md](./audit/KILO-E2E.md) | `/feature-delivery` + MCP 手順 |
| [audit/SKILL-QUALITY-REVIEW.md](./audit/SKILL-QUALITY-REVIEW.md) | skill 品質スキャン |
| [audit/LICENSE-HEADER-AUDIT.md](./audit/LICENSE-HEADER-AUDIT.md) | ライセンス棚卸し |

監査の再生成:

```bash
python3 scripts/audit_license_headers.py
python3 scripts/audit_skill_quality.py
```
