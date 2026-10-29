---
name: ja-proofread
description: Proofread Japanese text — docs (`*.ja.md`) and skill content — for non-Japanese wording that is actually wrong: simplified-Chinese-only characters, half-width punctuation, machine-translation artifacts, and terminology drift. English words/loanwords in Japanese prose are acceptable and are NOT changed. Use when finalizing or reviewing Japanese content; not for first-pass translation (use documentation-localization).
---

# Japanese proofreading (JA review)

## Scope (what is NOT a problem)
- **English words / identifiers in Japanese prose are fine** — e.g. "skill", "workflow", "MCP", `interpret_intent`. In JP technical writing this is common; **do not force katakana**. Keep code, identifiers, file paths, commands, and tool names in English.
- Only fix things that are genuinely **non-Japanese or wrong**.

## When to use
- Finalizing a Japanese document (`*.ja.md`), a skill, or a bilingual EN/JA pair.

## Detect (evidence, not vibes)
1. **Simplified-Chinese-only characters** (not standard Japanese):
   `这 们 图 个 时 过 请 让 说 对 从 无 还 经 现 发 开 么 专 业 务 动 为 应 关 见 长 门 问 间 题 单 双 认 识 语 记 计 论 谢 谁 边 银 网 线`
   ```bash
   grep -nE '这|们|图|个|时|过|请|让|说|对|从|无|还|经|现|发|开|么|专|业|务|动|为|应' <files>
   ```
   `scripts/validate_assets.py` emits a **WARN** when these appear in `*.ja.md` or `.kilo/skills/**`.
2. **Punctuation**: half-width `,` / `:` inside a Japanese run; unbalanced `「」` vs `""`.
3. **MT artifacts**: literal EN word order; "〜することができます" churn; mixed 敬体/常体.
4. **Terminology drift**: one term, one rendering across the doc set (pick the glossary term).

## Fix
- Chinese-only → Japanese kanji: `时→時 图→図 发→発 现→現 経→経 过→過 对→対 从→従 说→説 请→請 让→譲 专→専 业→業 务→務 动→動 为→為 应→応 关→関 见→見 长→長 门→門 问→問 间→間 题→題 单→単 认→認 识→識 语→語 记→記 计→計 论→論 谢→謝 谁→誰 边→辺 银→銀 网→網 线→線 无→無 还→還 个→個`.
- **Leave English words, identifiers, code, paths, and commands as-is.**
- Do not translate quoted third-party text or code samples.
- Language policy (`AGENTS.md` §1): code = English; JA records/docs = Japanese; public explanatory docs = EN primary + JA.

## Gate (Gₑ)
- Show a diff and the `grep` result reaching **0** Chinese-only characters.
- Confirm **no** English/identifier was rewritten.
