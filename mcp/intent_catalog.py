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
