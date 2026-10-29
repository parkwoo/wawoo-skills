---
name: ja-proofread
description: Proofread Japanese text — docs (`*.ja.md`) and skill content — for non-Japanese mixed in (especially simplified Chinese), machine-translation artifacts, punctuation, and terminology drift. Use when finalizing or reviewing Japanese content, or when a JA doc/skill may contain Chinese; not for first-pass translation of a whole document (use documentation-localization).
---

# Japanese proofreading (JA review)

## When to use
- Before finalizing a Japanese document (`*.ja.md`) or a bilingual EN/JA pair.
- When text may contain **simplified Chinese** or other non-Japanese CJK by mistake.
- NOT for translating a whole document from scratch (use `documentation-localization`).

## Detect (evidence, not vibes)
1. **Chinese-only characters** (not used in standard Japanese):
   `这 们 图 个 时 过 请 让 说 对 从 无 还 经 现 发 开 么 专 业 务 动 为 应 关 见 长 门 问 间 题 单 双 认 识 语 记 计 论 谢 谁 边 银 网 线`
   ```bash
   grep -nE '这|们|图|个|时|过|请|让|说|对|从|无|还|经|现|发|开|么|专|业|务|动|为|应' <files>
   ```
   `scripts/validate_assets.py` emits a **WARN** when these appear in `*.ja.md` or `.kilo/skills/**`.
2. **Punctuation**: half-width `,` / `:` inside Japanese runs; unbalanced `「」` vs `""`.
3. **MT artifacts**: literal EN word order; the same term translated differently across docs.
4. **Language policy** (`AGENTS.md` §1): code = English; JA records/docs = Japanese; public explanatory docs = EN primary + JA secondary.

## Fix
- Replace Chinese-only characters with the Japanese form:
  `时→時 图→図 发→発 现→現 经→経 过→過 对→対 从→従 说→説 请→請 让→譲 专→専 业→業 务→務 动→動 为→為 应→応 关→関 见→見 长→長 门→門 问→問 间→間 题→題 单→単 认→認 识→識 语→語 记→記 计→計 论→論 谢→謝 谁→誰 边→辺 银→銀 网→網 线→線 无→無 还→還 个→個`
- Keep code / identifiers / paths in English. Do not translate quoted third-party text or code samples.
- Use one glossary term consistently.

## Gate (Gₑ)
- Show a diff of corrections and the `grep` result reaching **0** remaining Chinese-only characters.
- State anything intentionally left (e.g., a quoted `zh-CN` example) explicitly.
