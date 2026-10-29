# Versioning

> Japanese version: [VERSIONING.ja.md](https://github.com/parkwoo/wawoo-skills/blob/master/docs/VERSIONING.ja.md)

## Scheme

- **Semantic Versioning**: `MAJOR.MINOR.PATCH` (e.g. `1.4.2`).
- **`VERSION` is the single SSOT** (repo root).
- Append changes to **`CHANGELOG.md`**.
- Git tag: `v<MAJOR>.<MINOR>.<PATCH>` (e.g. `v0.1.0`).

## What to bump

| Change | Digit |
|---|---|
| **Deleting / renaming** a skill/agent/command, breaking MCP tool I/O or names | **MAJOR** |
| **Adding** a skill/agent/command, backward-compatible feature additions | **MINOR** |
| Typos, wording, internal refactors (compatible) | **PATCH** |

## Release steps

1. Update `VERSION` (e.g. `0.1.0` → `0.2.0`).
2. Prepend `## [0.2.0] - YYYY-MM-DD` to `CHANGELOG.md` (Added/Changed/Fixed/Removed).
3. Verify:
   ```bash
   python3 scripts/validate_assets.py
   python3 scripts/gen_capabilities.py
   python3 scripts/e2e_flows.py
   ```
4. Commit:
   ```bash
   git add -A
   git commit -m "release: v0.2.0"
   ```
5. Tag:
   ```bash
   git tag -a v0.2.0 -m "v0.2.0"
   ```
6. Publish (only after approval):
   ```bash
   git push origin master
   git push origin v0.2.0
   ```

## Cautions

- The catalog `.kilo/CAPABILITIES.md` is a **generated artifact**. Do not hand-edit; regenerate with `gen_capabilities.py`.
- State breaking changes (renames, deletions) **in the CHANGELOG**, and add migration steps if needed.
- Do not add assets with unknown licenses (`ATTRIBUTION.md`).
