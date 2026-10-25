# メンテナ向け（git 管理外: `internal/`）

公開 README には載せない。配置: `./scripts/bootstrap-internal.sh`

## スモーク（API キー不要）

```bash
./internal/scripts/e2e/smoke.sh
```

## Docker（L1）

```bash
./internal/scripts/e2e/install-compose-v2.sh
./internal/scripts/e2e/compose.sh run --rm smoke
```

## CLI 実測

| 文書 | 内容 |
|---|---|
| [audit/CLI-E2E-ENV.md](./audit/CLI-E2E-ENV.md) | Kilo CLI / Cursor `agent` / Docker |
| [audit/KILO-E2E.md](./audit/KILO-E2E.md) | `/feature-delivery` + MCP |
| [audit/SKILL-QUALITY-REVIEW.md](./audit/SKILL-QUALITY-REVIEW.md) | skill 品質 |
| [audit/LICENSE-HEADER-AUDIT.md](./audit/LICENSE-HEADER-AUDIT.md) | ライセンス棚卸し |

```bash
python3 internal/scripts/audit_license_headers.py
python3 internal/scripts/audit_skill_quality.py
```
