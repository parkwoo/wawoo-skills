---
name: ja-proofread
description: Proofread Japanese text — docs (`*.ja.md`) and skill content — for non-Japanese wording mixed in: simplified-Chinese-only characters, English/loanwords used where a standard Japanese term exists, machine-translation artifacts, punctuation, and terminology drift. Use when finalizing or reviewing Japanese content, or when it may contain Chinese/English leftovers; not for first-pass translation of a whole document (use documentation-localization).
---

# Japanese proofreading (JA review)

## When to use
- Finalizing a Japanese document (`*.ja.md`), a skill, or a bilingual EN/JA pair.
- When the Japanese may contain **non-Japanese wording**: simplified Chinese, or **English words used where a Japanese term belongs**.

## Detect (evidence, not vibes)
1. **Simplified-Chinese-only characters** (not standard Japanese):
   `这 们 图 个 时 过 请 让 说 对 从 无 还 经 现 发 开 么 专 业 务 动 为 应 关 见 长 门 问 间 题 单 双 认 识 语 记 计 论 谢 谁 边 银 网 线`
   ```bash
   grep -nE '这|们|图|个|时|过|请|让|说|对|从|无|还|经|现|发|开|么|专|业|务|动|为|应' <files>
   ```
   `scripts/validate_assets.py` emits a **WARN** when these appear in `*.ja.md` or `.kilo/skills/**`.
2. **Non-Japanese vocabulary in prose** — bare Latin/English words inside Japanese sentences that have a standard Japanese term. Replace in prose (not in code):
   `skill→スキル agent→エージェント workflow→ワークフロー gate→ゲート routing→ルーティング review→レビュー design→デザイン test→テスト spec→仕様 ticket→チケット scope→範囲 deliver→納品 contract→契約 docs→文書 memory→記憶 prompt→プロンプト skill/agent/layer→層/役割`.
   - **Keep English** for: code, identifiers, file paths, commands, MCP/tool names, proper nouns, and anything inside backticks (`skill_get`, `docs/plans/ACTIVE.md`).
3. **MT artifacts**: literal EN word order; "〜することができます" churn; mixed 敬体/常体.
4. **Punctuation**: half-width `,`/`:` inside Japanese; unbalanced `「」` vs `""`.
5. **Terminology drift**: one term, one rendering across the doc set.

## Fix
- Chinese-only → Japanese kanji: `时→時 图→図 发→発 现→現 经→経 过→過 对→対 从→従 说→説 请→請 让→譲 专→専 业→業 务→務 动→動 为→為 应→応 关→関 见→見 长→長 门→門 问→問 间→間 题→題 单→単 认→認 识→識 语→語 记→記 计→計 论→論 谢→謝 谁→誰 边→辺 银→銀 网→網 线→線 无→無 还→還 个→個`.
- English prose → Japanese term (table above); keep backticked identifiers as-is.
- Do **not** translate quoted third-party text, code samples, commands, or names.
- Language policy (`AGENTS.md` §1): code = English; JA records/docs = Japanese; public explanatory docs = EN primary + JA.

## Gate (Gₑ)
- Show a diff and the `grep` result reaching **0** Chinese-only characters.
- List any English words intentionally kept (identifiers) explicitly.
