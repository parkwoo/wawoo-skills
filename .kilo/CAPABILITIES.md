# CAPABILITIES（自動生成）

> `python3 scripts/gen_capabilities.py` で再生成。手で編集しない。
> まず本カタログで候補を選び、必要なものだけ `SKILL.md` を開く（段階的開示）。
> `⚠️` は外部セットアップが必要（`scripts/readiness.json`）。標準フローでは使わない。

## Skills（55）

| name | ready | 説明 | path |
|---|---|---|---|
| `accessibility-audit` | ✅ | Audit and improve web accessibility for semantic structure, keyboard operation, forms, focus, contrast, motion, assistive technol… | `.kilo/skills/accessibility-audit/SKILL.md` |
| `api-contract-design` | ✅ | Design or review HTTP, RPC, event, or internal API contracts for clear inputs, outputs, errors, authentication, compatibility, an… | `.kilo/skills/api-contract-design/SKILL.md` |
| `architecture-decision` | ✅ | Evaluate software architecture choices, dependencies, interfaces, constraints, and tradeoffs, then produce a concise decision rec… | `.kilo/skills/architecture-decision/SKILL.md` |
| `ask-matt` | ✅ | Ask which skill or flow fits your situation. A router over the skills in this repo. | `.kilo/skills/ask-matt/SKILL.md` |
| `brand-guidelines` | ✅ | Apply Anthropic's official brand colors and typography to artifacts for consistent visual identity and professional design standa… | `.kilo/skills/brand-guidelines/SKILL.md` |
| `change-readiness` | ✅ | Perform an evidence-based pre-handoff review of a non-trivial software change before requesting human or external audit. Use afte… | `.kilo/skills/change-readiness/SKILL.md` |
| `changelog` | ✅ | Generate and maintain user-facing changelog/release notes from git history (Conventional Commits) and keep version/tags consisten… | `.kilo/skills/changelog/SKILL.md` |
| `code-review` | ✅ | "Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this… | `.kilo/skills/code-review/SKILL.md` |
| `codebase-design` | ✅ | Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening o… | `.kilo/skills/codebase-design/SKILL.md` |
| `compliance-legal` | ✅ | Review OSS license obligations (MIT/Apache-2.0 attribution, NOTICE), SBOM, and product/service legal checklists (terms, privacy, … | `.kilo/skills/compliance-legal/SKILL.md` |
| `database-change-safety` | ✅ | Plan, implement, and review schema changes, data migrations, backfills, and cleanup with integrity, availability, observability, … | `.kilo/skills/database-change-safety/SKILL.md` |
| `dependency-upgrade` | ✅ | Safely evaluate, apply, and verify software dependency, runtime, container-image, or toolchain upgrades with compatibility, secur… | `.kilo/skills/dependency-upgrade/SKILL.md` |
| `deployment` | ✅ | Plan, execute, and verify a deployment or release (Docker Compose, image tagging, environment, migrations, health checks, rollbac… | `.kilo/skills/deployment/SKILL.md` |
| `design-brief` | ✅ | Parse a structured design brief written in I-Lang protocol format into a concrete design spec. Eliminates ambiguity from vague re… | `.kilo/skills/design-brief/SKILL.md` |
| `design-md` | ✅ | Create and manage DESIGN.md files. Useful for capturing design direction, tokens, and visual rules in a single source of truth. | `.kilo/skills/design-md/SKILL.md` |
| `design-review` | ✅ | Designer Who Codes: visual audit then fixes with atomic commits and before/after screenshots. Useful for tightening shipped UI be… | `.kilo/skills/design-review/SKILL.md` |
| `diagnosing-bugs` | ✅ | Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something br… | `.kilo/skills/diagnosing-bugs/SKILL.md` |
| `documentation-localization` | ✅ | Write, review, and synchronize technical documentation and localized content for factual accuracy, usable instructions, links, me… | `.kilo/skills/documentation-localization/SKILL.md` |
| `domain-modeling` | ✅ | Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a GLOSSARY.md, or record… | `.kilo/skills/domain-modeling/SKILL.md` |
| `engineering-quality` | ✅ | Plan and implement software changes with explicit scope, evidence-based verification, safe migrations, and rollback readiness. Us… | `.kilo/skills/engineering-quality/SKILL.md` |
| `frontend-design` | ✅ | Create distinctive, production-grade frontend interfaces with strong visual direction, polished typography, considered layout, an… | `.kilo/skills/frontend-design/SKILL.md` |
| `grill-with-docs` | ✅ | A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go. | `.kilo/skills/grill-with-docs/SKILL.md` |
| `grilling` | ✅ | Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any '… | `.kilo/skills/grilling/SKILL.md` |
| `handoff` | ✅ | Compact the current conversation into a handoff document for another agent to pick up. | `.kilo/skills/handoff/SKILL.md` |
| `imagegen-frontend-mobile` | ✅ | モバイルアプリ向けの高品質画像コンセプト用スキル。iOS/Android 向け画面・フローのプロンプトとビジュアル指針を提供する（コードは書かない）。詳細な英語プロンプト集は references に分離。 | `.kilo/skills/imagegen-frontend-mobile/SKILL.md` |
| `implement` | ✅ | "Implement a piece of work based on a spec or set of tickets." | `.kilo/skills/implement/SKILL.md` |
| `implement-spec` | ✅ | "Implement the result of /to-spec and /to-tickets in code." | `.kilo/skills/implement-spec/SKILL.md` |
| `incident-debugging` | ✅ | Diagnose a software incident or high-impact defect through reproduction, evidence collection, fault isolation, mitigation, verifi… | `.kilo/skills/incident-debugging/SKILL.md` |
| `marketing-psychology` | ✅ | Apply psychological principles and behavioral science to copy and design. Useful for tightening hooks, framing, and pricing prese… | `.kilo/skills/marketing-psychology/SKILL.md` |
| `memory` | ✅ | Persist and recall durable project knowledge (decisions, constraints, gotchas, recurring fixes) across sessions. Use before start… | `.kilo/skills/memory/SKILL.md` |
| `pdca-cycle` | ✅ | Run a lightweight Plan-Do-Check-Act cycle for product, engineering, quality, or process improvements. Use when a request needs me… | `.kilo/skills/pdca-cycle/SKILL.md` |
| `performance-audit` | ✅ | Measure and improve application or web performance using representative workloads, bottleneck evidence, and regression safeguards… | `.kilo/skills/performance-audit/SKILL.md` |
| `plan-md` | ✅ | 計画に関わる成果物（修正計画・実装計画・設計方針・レビュー対応など）を必ず Markdown ファイルとして保存する。計画を作る・計画を立てる・fix/implementation/design plan を作るタスクで使う。 | `.kilo/skills/plan-md/SKILL.md` |
| `pr` | ✅ | "Use when writing a PR body." | `.kilo/skills/pr/SKILL.md` |
| `privacy-review` | ✅ | Review personal data (PII) flows, minimization, retention, masking, logging, and cross-border handling for a feature or service. … | `.kilo/skills/privacy-review/SKILL.md` |
| `product-discovery` | ✅ | Turn an ambiguous product or feature request into a scoped problem statement, user outcome, acceptance criteria, priorities, risk… | `.kilo/skills/product-discovery/SKILL.md` |
| `prototype` | ✅ | Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic f… | `.kilo/skills/prototype/SKILL.md` |
| `reference-design-contract` | ✅ | Turn vague taste, screenshots, URLs, product notes, or "make it feel like this" references into a grounded DESIGN.md plus an impl… | `.kilo/skills/reference-design-contract/SKILL.md` |
| `release-readiness` | ✅ | Prepare and review a software release for versioning, legal files, changelog accuracy, tags, release notes, deployment checks, an… | `.kilo/skills/release-readiness/SKILL.md` |
| `research` | ✅ | Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the u… | `.kilo/skills/research/SKILL.md` |
| `research-decision-room` | ✅ | Turn messy user research notes, interviews, support tickets, surveys, and product context into an evidence-backed decision room: … | `.kilo/skills/research-decision-room/SKILL.md` |
| `retro` | ✅ | "Conduct a retrospective on a coding session." | `.kilo/skills/retro/SKILL.md` |
| `screenshots-marketing` | ✅ | Produce marketing screenshots (landing hero, App Store, changelog visuals). Use Playwright when available; otherwise produce a ca… | `.kilo/skills/screenshots-marketing/SKILL.md` |
| `security-review` | ✅ | Perform a read-first security review of application code, configuration, dependencies, and delivery changes. Use for requested se… | `.kilo/skills/security-review/SKILL.md` |
| `setup-matt-pocock-skills` | ✅ | "Configure this repo for the engineering skills: set up its issue tracker, triage label vocabulary, and domain doc layout. Run on… | `.kilo/skills/setup-matt-pocock-skills/SKILL.md` |
| `slides` | ✅ | Create slide decks as Markdown/HTML by default (no external dependencies); optionally export .pptx with PptxGenJS if installed. U… | `.kilo/skills/slides/SKILL.md` |
| `tdd` | ✅ | Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or want… | `.kilo/skills/tdd/SKILL.md` |
| `test-engineering` | ✅ | Design, implement, diagnose, and review software tests with evidence-focused coverage across unit, integration, and end-to-end la… | `.kilo/skills/test-engineering/SKILL.md` |
| `to-spec` | ⚠️ issue tracker (setup-matt-pocock-skills) | "Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you'… | `.kilo/skills/to-spec/SKILL.md` |
| `to-tickets` | ⚠️ issue tracker (setup-matt-pocock-skills) | Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published… | `.kilo/skills/to-tickets/SKILL.md` |
| `triage` | ⚠️ issue tracker (setup-matt-pocock-skills) | Move issues and external PRs through a state machine of triage roles, categorise, verify, grill if needed, and write agent-ready … | `.kilo/skills/triage/SKILL.md` |
| `wayfinder` | ✅ | Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on your issue tracker, and r… | `.kilo/skills/wayfinder/SKILL.md` |
| `web-design-guidelines` | ✅ | Review UI code for Web Interface Guidelines compliance by the Vercel engineering team. Covers layout, typography, color, motion, … | `.kilo/skills/web-design-guidelines/SKILL.md` |
| `web-experience-design` | ✅ | Design, implement, audit, and hand off web interfaces with evidence for user tasks, visual hierarchy, responsive behavior, access… | `.kilo/skills/web-experience-design/SKILL.md` |
| `writing-for-agents` | ✅ | Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md. | `.kilo/skills/writing-for-agents/SKILL.md` |

## Agents（22）

| name | 説明 | path |
|---|---|---|
| `accessibility-reviewer` | Performs read-only accessibility review of user flows, semantic structure, keyboard operation, and responsive UI. | `.kilo/agents/accessibility-reviewer.md` |
| `architect` | Evaluates architecture alternatives, interfaces, dependencies, migration risk, and decision records. | `.kilo/agents/architect.md` |
| `Code Reviewer` | Senior software engineer conducting thorough code reviews | `.kilo/agents/code-reviewer.md` |
| `Code Simplifier` | For simplifying/refactoring features of codebase | `.kilo/agents/code-simplifier.md` |
| `Code Skeptic` | For when you need your code criticized like nobody's business | `.kilo/agents/code-skeptic.md` |
| `compliance-reviewer` | Legal, compliance, and privacy review gate for a change or release. Collects evidence and checklists; final legal judgment requir… | `.kilo/agents/compliance-reviewer.md` |
| `Data` | Run notebook-first data analysis by appending and executing cells for each request. | `.kilo/agents/data.md` |
| `delivery-lead` | Coordinates evidence-based delivery from scope through review without bypassing approvals. | `.kilo/agents/delivery-lead.md` |
| `docs-localization-reviewer` | Maintains factual technical documentation and equivalent localized content. | `.kilo/agents/docs-localization-reviewer.md` |
| `Documentation Specialist` | Focus on writing documentation, markdown files, and other text-based files | `.kilo/agents/docs-specialist.md` |
| `Frontend Specialist` | Frontend developer expert in React, TypeScript, and modern CSS | `.kilo/agents/frontend-specialist.md` |
| `implementer` | Implements scoped software changes with project conventions, focused tests, and evidence-based reporting. | `.kilo/agents/implementer.md` |
| `market-researcher` | Market, competitor, and customer research for product/service market plans. Produces evidence-backed findings and decision memos;… | `.kilo/agents/market-researcher.md` |
| `performance-reviewer` | Reviews performance bottlenecks, measurement design, budgets, and regression safeguards. | `.kilo/agents/performance-reviewer.md` |
| `product-owner` | Clarifies user outcomes, priorities, scope, and acceptance criteria without inventing business decisions. | `.kilo/agents/product-owner.md` |
| `project-manager` | Agile project and progress management for this project — sprint planning, status reporting, risk tracking, and delivery coordinat… | `.kilo/agents/project-manager.md` |
| `qa-engineer` | Designs test strategy, reproduces defects, evaluates verification evidence, and identifies coverage gaps. | `.kilo/agents/qa-engineer.md` |
| `release-manager` | Prepares releases with version, legal, artifact, compatibility, rollback, and remote-verification checks. | `.kilo/agents/release-manager.md` |
| `security-reviewer` | Performs read-only security review of code, configuration, dependencies, and delivery changes. | `.kilo/agents/security-reviewer.md` |
| `sre-operator` | Performs cautious read-first operations analysis for logs, monitoring, incidents, and cloud environments. | `.kilo/agents/sre-operator.md` |
| `wawoo-router` | Default entry agent. Routes non-trivial requests to a wawoo workflow via MCP before any other tool, then executes that workflow. … | `.kilo/agents/wawoo-router.md` |
| `web-designer` | Designs and implements accessible responsive web interfaces, then audits rendered behavior before handoff. | `.kilo/agents/web-designer.md` |

## Workflows（15）

| name | 説明 | path |
|---|---|---|
| `/compliance-review` | 法務・プライバシー・セキュリティのゲート（compliance-legal → privacy-review → security-review → release-readiness） | `.kilo/commands/compliance-review.md` |
| `/content-delivery-lite` | L1 knowledge delivery — books, long docs, reports via CONTENT.md state machine (not code implement). | `.kilo/commands/content-delivery-lite.md` |
| `/deck` | 提案・計画デッキ（Markdown/HTML 既定・pptx は任意）。標準の開発フローには含めない。 | `.kilo/commands/deck.md` |
| `/delivery-lite` | Lightweight delivery — SSOT plan file state machine, minimal ceremony (L0–L1). Default for single-feature requests without full f… | `.kilo/commands/delivery-lite.md` |
| `/design-review` | UI の設計レビュー（design-review → web-design-guidelines → accessibility-audit） | `.kilo/commands/design-review.md` |
| `/feature-delivery` | Deliver a feature through discovery, design, implementation, testing, review, and approval gates. | `.kilo/commands/feature-delivery.md` |
| `/incident-response` | Investigate and safely resolve an incident or urgent regression with evidence and follow-up. | `.kilo/commands/incident-response.md` |
| `/market-plan` | 市場調査 → 戦略 → 計画（research → research-decision-room → product-discovery → marketing-psychology → plan-md）。提案デッキは任意（`slides` は Markdo… | `.kilo/commands/market-plan.md` |
| `/release-review` | Prepare a release-review package with legal/compliance, privacy, version, security, test, artifact, remote, and rollback evidence… | `.kilo/commands/release-review.md` |
| `/research` | 調査 → 意思決定（research → product-discovery → to-spec/to-tickets） | `.kilo/commands/research.md` |
| `/self-improve` | 自己改善（retro → pdca-cycle → self-review → plan-md） | `.kilo/commands/self-improve.md` |
| `/self-review` | 自己修正（code-review → code-skeptic → diagnosing-bugs/tdd → 修正 → 検証） | `.kilo/commands/self-review.md` |
| `/sprint-plan` | スプリント計画 L2（wayfinder → to-tickets → 優先度/見積/容量 → plan-md） | `.kilo/commands/sprint-plan.md` |
| `/status-report` | 進捗・状況報告（ACTIVE または triage/to-tickets → 進捗・リスク → plan-md） | `.kilo/commands/status-report.md` |
| `/ui-delivery` | Design, implement, and audit a web UI change across responsive and accessibility states. | `.kilo/commands/ui-delivery.md` |

## 呼び出し規約
1. Workflow（入口）を選ぶ。2. その本文の skill を**必要分だけ**開く。3. 出力スキーマとゲートに従う。
詳細：`docs/USAGE.md`。
