"""意図解釈で使う workflow 台帳（循環 import 回避用）。"""

from __future__ import annotations

from dataclasses import dataclass

# MCP server.py が公開するツール名（workflow ごとの許可集合）
MCP_TOOL_NAMES: frozenset[str] = frozenset(
    {
        "capabilities",
        "skill_search",
        "skill_get",
        "workflow_get",
        "agent_get",
        "memory_recall",
        "memory_save",
        "evidence_check",
        "interpret_intent",
        "route_task",
    }
)

_MCP_READ: frozenset[str] = frozenset(
    {
        "capabilities",
        "skill_search",
        "skill_get",
        "workflow_get",
        "agent_get",
        "memory_recall",
        "interpret_intent",
        "route_task",
    }
)

_MCP_FULL: frozenset[str] = MCP_TOOL_NAMES

_MCP_AUDIT: frozenset[str] = frozenset(
    {
        "capabilities",
        "skill_search",
        "skill_get",
        "workflow_get",
        "agent_get",
        "memory_recall",
        "evidence_check",
        "interpret_intent",
        "route_task",
    }
)


@dataclass(frozen=True)
class WorkflowSpec:
    agent: str
    description: str
    mcp_tools: frozenset[str]
    # L3: workflow 起動後の委譲はホスト IDE／エージェント（OpenCode subagent 相当）
    delegation: str = "upstream-subagent"
    # P1: 分解されたフェーズ（phases_for() で後付けされる）
    phases: tuple[Phase, ...] = ()


WORKFLOWS: dict[str, WorkflowSpec] = {
    "delivery-lite": WorkflowSpec(
        "implementer",
        "軽量納品。単機能の実装と ACTIVE.md による進捗管理。明確な小さな変更の既定経路。",
        _MCP_FULL,
    ),
    "content-delivery-lite": WorkflowSpec(
        "docs-specialist",
        "知識・長文納品。書籍・レポート・長文ドキュメントを CONTENT.md で管理する（コード実装向けではない）。",
        _MCP_FULL,
    ),
    "feature-delivery": WorkflowSpec(
        "delivery-lead",
        "機能横断の納品。複数コンポーネント・設計と実装を束ねる本格デリバリー。",
        _MCP_FULL,
    ),
    "ui-delivery": WorkflowSpec(
        "web-designer",
        "UI/UX 実装。画面・コンポーネント・デザイン憲章に沿ったフロント納品。",
        _MCP_FULL,
    ),
    "design-review": WorkflowSpec(
        "web-designer",
        "デザイン・UI のレビュー。実装変更より評価・指摘・改善提案が主目的。",
        _MCP_READ,
    ),
    "research": WorkflowSpec(
        "product-owner",
        "調査と意思決定。技術・市場・仕様の調査から spec/チケット化の判断まで。",
        _MCP_READ,
    ),
    "market-plan": WorkflowSpec(
        "market-researcher",
        "市場・競合・ポジショニングの計画と整理。",
        _MCP_READ,
    ),
    "deck": WorkflowSpec(
        "market-researcher",
        "プレゼン・デック・投資家向け資料の構成と文案。",
        _MCP_READ,
    ),
    "compliance-review": WorkflowSpec(
        "compliance-reviewer",
        "コンプライアンス・ポリシー適合のレビュー（memory への自動追記は制限）。",
        _MCP_AUDIT,
    ),
    "release-review": WorkflowSpec(
        "release-manager",
        "リリース前チェック。変更範囲・リスク・ゲートの確認。",
        _MCP_AUDIT,
    ),
    "incident-response": WorkflowSpec(
        "sre-operator",
        "本番障害・インシデント対応。診断・復旧・記録が主目的。",
        _MCP_FULL,
    ),
    "sprint-plan": WorkflowSpec(
        "project-manager",
        "スプリント計画。バックログ整理・見積・スコープ合意。",
        _MCP_READ,
    ),
    "status-report": WorkflowSpec(
        "project-manager",
        "ステータス報告。進捗・ブロッカー・次アクションの整理。",
        _MCP_READ,
    ),
    "self-review": WorkflowSpec(
        "code-reviewer",
        "自己レビュー。変更の品質・テスト・設計整合の点検。",
        _MCP_AUDIT,
    ),
    "self-improve": WorkflowSpec(
        "delivery-lead",
        "キット・プロセス自身の改善。スキル・手順・テンプレの更新。",
        _MCP_FULL,
    ),
}

# 後方互換
WORKFLOW_AGENTS: dict[str, str] = {wid: spec.agent for wid, spec in WORKFLOWS.items()}


def workflow_spec(workflow_id: str) -> WorkflowSpec | None:
    return WORKFLOWS.get(workflow_id)


def mcp_tools_allow(workflow_id: str) -> list[str]:
    spec = workflow_spec(workflow_id)
    if spec is None:
        return sorted(MCP_TOOL_NAMES)
    return sorted(spec.mcp_tools)


def catalog_for_upstream(max_desc: int = 72) -> list[dict[str, str]]:
    """上流スコア用のコンパクト一覧。"""
    rows: list[dict[str, str]] = []
    for wid in sorted(WORKFLOWS):
        spec = WORKFLOWS[wid]
        desc = spec.description
        if len(desc) > max_desc:
            desc = desc[: max_desc - 1] + "…"
        rows.append({"id": wid, "description": desc})
    return rows


# --- L1 trigger classifier (決定論的・無料) --------------------------------------
# workflow ごとの識別語。長い（具体的な）語ほど高スコア。ROUTER.md の発火語の正本。
TRIGGER_KEYWORDS: dict[str, tuple[str, ...]] = {
    "delivery-lite": ("バグ修正", "小さな修正", "軽微な修正", "改bug", "改 bug", "单个功能", "単機能", "不具合修正", "fix bug", "small fix", "minor change"),
    "content-delivery-lite": ("書籍", "長文", "レポート作成", "原稿", "記事", "书稿", "长文", "book draft", "long-form doc", "manuscript"),
    "feature-delivery": ("新機能", "機能追加", "複数コンポーネント", "設計込み", "跨模块", "新功能", "feature delivery", "end-to-end feature", "new feature"),
    "ui-delivery": ("画面実装", "コンポーネント実装", "スタイル", "フロント実装", "界面", "组件", "样式", "ui implementation", "frontend ui", "responsive layout"),
    "design-review": ("デザインレビュー", "uiレビュー", "デザイン評価", "ui评审", "设计评审", "design critique", "visual audit"),
    "research": ("調査", "技術選定", "技術比較", "調査して", "调研", "技术选型", "investigate", "compare options", "research", "due diligence"),
    "market-plan": ("市場調査", "競合分析", "事業計画", "市场", "竞品", "商业计划", "market research", "competitive analysis", "business plan", "positioning"),
    "deck": ("プレゼン", "提案資料", "スライド", "デッキ", "幻灯片", "提案材料", "slide deck", "investor deck", "pitch deck"),
    "compliance-review": ("ライセンス確認", "法務確認", "プライバシー", "コンプライアンス", "法务", "合规", "隐私", "license compliance", "privacy review", "legal review"),
    "release-review": ("リリース前", "リリース可否", "出荷前", "发布前", "上线前", "release readiness", "pre-release check", "ship check", "production readiness"),
    "incident-response": ("障害", "本番エラー", "インシデント", "サービス停止", "线上事故", "生产报错", "outage", "incident", "production error", "regression in prod"),
    "sprint-plan": ("スプリント計画", "バックログ", "見積", "迭代计划", "排期", "sprint plan", "backlog grooming", "estimation", "capacity plan"),
    "status-report": ("進捗報告", "状況報告", "进度汇报", "status report", "progress report", "status update"),
    "self-review": ("自己レビュー", "変更レビュー", "自我代码审查", "self review", "review my changes", "review since"),
    "self-improve": ("プロセス改善", "キット改善", "振り返り", "レトロ", "流程改进", "kit improvement", "retrospective", "process improvement", "日志分析", "调用状况", "调用排查", "调用情况", "运行排查", "log 分析", "invocation status", "call status"),
}

# 曖昧な一般語（単独では誤ルーティングするのでスコアを下げる）
WEAK_TRIGGERS: dict[str, tuple[str, ...]] = {
    "delivery-lite": ("実装", "修正", "変更", "implement", "fix", "改修"),
    "feature-delivery": ("機能", "feature"),
}


@dataclass(frozen=True)
class TriggerMatch:
    workflow: str
    trigger: str
    score: float


def _trigger_score(keyword: str) -> float:
    return min(0.95, 0.76 + 0.03 * len(keyword))


def classify_by_trigger(text: str, *, threshold: float = 0.85) -> TriggerMatch | None:
    """決定論的トリガで workflow を推定する（L1）。

    最上位スコアが閾値以上、かつ 2 位と十分差があるときだけ採用する。
    長い語に内包される短い語（例: 「市場調査」の中の「調査」）は競合として数えない。
    曖昧なら None を返し、呼び出し側は needs_scoring にフォールバックする。
    """
    raw = (text or "").strip().lower()
    if not raw:
        return None
    cands: list[tuple[float, str, str]] = []
    for wid, words in TRIGGER_KEYWORDS.items():
        for w in words:
            if w.lower() in raw:
                cands.append((_trigger_score(w) + 0.06, wid, w))
    for wid, words in WEAK_TRIGGERS.items():
        for w in words:
            if w.lower() in raw:
                cands.append((_trigger_score(w) - 0.15, wid, w))
    if not cands:
        return None
    cands.sort(reverse=True)
    # 上位語に内包される下位語は「同一対象の詳細」とみなし競合から外す
    kept = [c for c in cands if not any(c[2] in k[2] and k[0] > c[0] for k in cands)]
    if not kept:
        return None
    top = kept[0]
    if top[0] < threshold:
        return None
    if len(kept) > 1 and kept[1][1] != top[1] and (top[0] - kept[1][0]) < 0.05:
        return None  # 競合 → 上流スコアへ
    return TriggerMatch(workflow=top[1], trigger=top[2], score=round(min(top[0], 0.97), 3))


# --- workflow phases (P1: 分解・P2: phase 単位の道具立て) -------------------------


@dataclass(frozen=True)
class Phase:
    id: str
    goal: str
    agent: str
    skills: tuple[str, ...] = ()
    tools: frozenset[str] = _MCP_READ
    exit_criteria: tuple[str, ...] = ()
    parallel_group: str = ""


BASE_PHASES: dict[str, Phase] = {
    "discover": Phase("discover", "Outcome/受入基準/スコープの確定", "product-owner", ("product-discovery",), _MCP_READ, ("outcome と受入基準が明記されている",)),
    "design": Phase("design", "設計・トレードオフの決定", "architect", ("architecture-decision",), _MCP_READ, ("決定・代替案・却下理由が記録されている",)),
    "plan": Phase("plan", "作業分解と計画の文書化", "project-manager", ("plan-md",), _MCP_READ, ("計画が docs に保存され id を持つ",)),
    "implement": Phase("implement", "最小の変更を実装", "implementer", ("engineering-quality",), _MCP_FULL, ("変更は scoped／テスト追加／秘密なし",)),
    "verify": Phase("verify", "テストと証拠の確認", "qa-engineer", ("test-engineering",), _MCP_FULL, ("未収束 FAILED 0／残留コンテナ 0／実行コマンド記録",), "readonly-parallel"),
    "audit": Phase("audit", "読み取り専用の審査", "security-reviewer", ("security-review",), _MCP_READ, ("所見と証跡（重要度付き）",), "readonly-parallel"),
    "research": Phase("research", "一次情報の調査", "product-owner", ("research",), _MCP_READ, ("事実と推測を分離して記録",), "readonly-parallel"),
    "release": Phase("release", "リリース可否の判定", "release-manager", ("release-readiness",), _MCP_AUDIT, ("版/タグ/ロールバック/未検証の明記",)),
    "report": Phase("report", "証拠つきの報告", "delivery-lead", ("change-readiness",), _MCP_AUDIT, ("証拠・未検証・リスク・次アクション",)),
}

# P5: 共通 phase を再利用（重複定義の排除）
WORKFLOW_PHASES: dict[str, tuple[str, ...]] = {
    "delivery-lite": ("plan", "implement", "verify", "report"),
    "content-delivery-lite": ("plan", "implement", "verify", "report"),
    "feature-delivery": ("discover", "design", "implement", "verify", "report"),
    "ui-delivery": ("design", "implement", "verify", "report"),
    "design-review": ("audit", "report"),
    "research": ("research", "report"),
    "market-plan": ("research", "plan", "report"),
    "deck": ("plan", "report"),
    "compliance-review": ("audit", "report"),
    "release-review": ("audit", "release", "report"),
    "incident-response": ("audit", "implement", "verify", "report"),
    "sprint-plan": ("plan", "report"),
    "status-report": ("report",),
    "self-review": ("audit", "verify", "report"),
    "self-improve": ("plan", "implement", "verify", "report"),
}

# 特定 workflow の phase だけ agent/skills を差し替える
PHASE_OVERRIDES: dict[tuple[str, str], dict[str, object]] = {
    ("ui-delivery", "implement"): {"agent": "web-designer", "skills": ("web-experience-design", "frontend-design")},
    ("ui-delivery", "verify"): {"skills": ("web-design-guidelines", "accessibility-audit")},
    ("design-review", "audit"): {"agent": "web-designer", "skills": ("design-review", "web-design-guidelines", "accessibility-audit")},
    ("compliance-review", "audit"): {"agent": "compliance-reviewer", "skills": ("compliance-legal", "privacy-review")},
    ("release-review", "audit"): {"skills": ("compliance-legal", "privacy-review", "security-review")},
    ("incident-response", "audit"): {"agent": "sre-operator", "skills": ("incident-debugging",)},
    ("incident-response", "implement"): {"agent": "sre-operator", "skills": ("incident-debugging", "deployment")},
    ("self-review", "audit"): {"agent": "code-reviewer", "skills": ("code-review", "codebase-design")},
    ("content-delivery-lite", "implement"): {"agent": "docs-specialist", "skills": ("documentation-localization",)},
    ("market-plan", "research"): {"agent": "market-researcher", "skills": ("research", "research-decision-room")},
    ("deck", "plan"): {"agent": "market-researcher", "skills": ("slides",)},
    ("sprint-plan", "plan"): {"agent": "project-manager", "skills": ("wayfinder", "to-tickets")},
    ("status-report", "report"): {"agent": "project-manager", "skills": ("plan-md",)},
}


def phases_for(workflow_id: str) -> tuple[Phase, ...]:
    base = BASE_PHASES
    out: list[Phase] = []
    for pid in WORKFLOW_PHASES.get(workflow_id, ()):
        phase = base.get(pid)
        if phase is None:
            continue
        ov = PHASE_OVERRIDES.get((workflow_id, pid))
        if ov:
            import dataclasses

            phase = dataclasses.replace(phase, **ov)  # type: ignore[arg-type]
        out.append(phase)
    return tuple(out)


def phase_spec(workflow_id: str, phase_id: str) -> Phase | None:
    for p in phases_for(workflow_id):
        if p.id == phase_id:
            return p
    return None


def phase_dicts(workflow_id: str) -> list[dict[str, object]]:
    return [
        {
            "id": p.id,
            "goal": p.goal,
            "agent": p.agent,
            "skills": list(p.skills),
            "mcp_tools_allow": sorted(p.tools),
            "exit_criteria": list(p.exit_criteria),
            "parallel_group": p.parallel_group,
        }
        for p in phases_for(workflow_id)
    ]


def mcp_tools_allow_for_phase(workflow_id: str, phase_id: str) -> list[str]:
    p = phase_spec(workflow_id, phase_id)
    if p is None:
        return mcp_tools_allow(workflow_id)
    return sorted(p.tools)


def implement_allowed(workflow_id: str) -> bool:
    """この workflow に実装 phase があるか（無ければ実装は workflow 切替が必要）。"""
    return any(p.id == "implement" for p in phases_for(workflow_id))


# WorkflowSpec に phases を後付け（frozen のため replace）
import dataclasses as _dc  # noqa: E402

WORKFLOWS = {wid: _dc.replace(spec, phases=phases_for(wid)) for wid, spec in WORKFLOWS.items()}
WORKFLOW_AGENTS = {wid: spec.agent for wid, spec in WORKFLOWS.items()}


