"""Workflow ledger used by intent interpretation (to avoid circular imports)."""

from __future__ import annotations

from dataclasses import dataclass

# Tool names exposed by MCP server.py (the allow-set per workflow)
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
    # L3: post-start delegation is done by the host IDE/agent (equivalent to an OpenCode subagent)
    delegation: str = "upstream-subagent"
    # P1: decomposed phases (attached later by phases_for())
    phases: tuple[Phase, ...] = ()


WORKFLOWS: dict[str, WorkflowSpec] = {
    "delivery-lite": WorkflowSpec(
        "implementer",
        "Lightweight delivery. Single-feature implementation and progress tracking via ACTIVE.md. Default path for clear, small changes.",
        _MCP_FULL,
    ),
    "content-delivery-lite": WorkflowSpec(
        "docs-specialist",
        "Knowledge / long-form delivery. Manage books, reports, and long documents with CONTENT.md (not for code implementation).",
        _MCP_FULL,
    ),
    "feature-delivery": WorkflowSpec(
        "delivery-lead",
        "Cross-cutting feature delivery. Full delivery that bundles design and implementation across multiple components.",
        _MCP_FULL,
    ),
    "ui-delivery": WorkflowSpec(
        "web-designer",
        "UI/UX implementation. Frontend delivery of screens and components per the design charter.",
        _MCP_FULL,
    ),
    "design-review": WorkflowSpec(
        "web-designer",
        "Design/UI review. The main goal is evaluation, findings, and improvement suggestions rather than implementation changes.",
        _MCP_READ,
    ),
    "research": WorkflowSpec(
        "product-owner",
        "Research and decisions. From research on technology, market, and specs to the spec/ticket decision.",
        _MCP_READ,
    ),
    "market-plan": WorkflowSpec(
        "market-researcher",
        "Market, competitive, and positioning planning and synthesis.",
        _MCP_READ,
    ),
    "deck": WorkflowSpec(
        "market-researcher",
        "Structure and copy for presentations, decks, and investor materials.",
        _MCP_READ,
    ),
    "compliance-review": WorkflowSpec(
        "compliance-reviewer",
        "Compliance / policy-fit review (automatic writes to memory are restricted).",
        _MCP_AUDIT,
    ),
    "release-review": WorkflowSpec(
        "release-manager",
        "Pre-release check. Confirm change scope, risks, and gates.",
        _MCP_AUDIT,
    ),
    "incident-response": WorkflowSpec(
        "sre-operator",
        "Production incident response. Diagnosis, recovery, and recording are the main goals.",
        _MCP_FULL,
    ),
    "sprint-plan": WorkflowSpec(
        "project-manager",
        "Sprint planning. Backlog grooming, estimation, and scope agreement.",
        _MCP_READ,
    ),
    "status-report": WorkflowSpec(
        "project-manager",
        "Status report. Organize progress, blockers, and next actions.",
        _MCP_READ,
    ),
    "self-review": WorkflowSpec(
        "code-reviewer",
        "Self-review. Check change quality, tests, and design consistency.",
        _MCP_AUDIT,
    ),
    "self-improve": WorkflowSpec(
        "delivery-lead",
        "Improve the kit and process themselves. Update skills, procedures, and templates.",
        _MCP_FULL,
    ),
    "writing": WorkflowSpec(
        "docs-specialist",
        "Creative/article writing (explore → beats → shape): blog, essay, fiction, scripts. Pairs with content-delivery-lite.",
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
    """A compact list for upstream scoring."""
    rows: list[dict[str, str]] = []
    for wid in sorted(WORKFLOWS):
        spec = WORKFLOWS[wid]
        desc = spec.description
        if len(desc) > max_desc:
            desc = desc[: max_desc - 1] + "…"
        rows.append({"id": wid, "description": desc})
    return rows


# --- workflow phases (P1: decomposition, P2: per-phase tooling) -------------------


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
    "discover": Phase("discover", "Fix the outcome, acceptance criteria, and scope", "product-owner", ("product-discovery",), _MCP_READ, ("outcome and acceptance criteria are stated",)),
    "design": Phase("design", "Decide design and tradeoffs", "architect", ("architecture-decision",), _MCP_READ, ("decision, alternatives, and rejection reasons are recorded",)),
    "plan": Phase("plan", "Break down the work and document the plan", "project-manager", ("plan-md",), _MCP_READ, ("the plan is saved in docs and has an id",)),
    "implement": Phase("implement", "Implement the smallest change", "implementer", ("engineering-quality",), _MCP_FULL, ("change is scoped / tests added / no secrets",)),
    "verify": Phase("verify", "Check tests and evidence", "qa-engineer", ("test-engineering",), _MCP_FULL, ("0 unconverged FAILED / 0 leftover containers / commands recorded",), "readonly-parallel"),
    "audit": Phase("audit", "Read-only review", "security-reviewer", ("security-review",), _MCP_READ, ("findings and evidence (with severity)",), "readonly-parallel"),
    "research": Phase("research", "Research primary sources", "product-owner", ("research",), _MCP_READ, ("fact and inference recorded separately",), "readonly-parallel"),
    "release": Phase("release", "Decide release readiness", "release-manager", ("release-readiness",), _MCP_AUDIT, ("version/tag/rollback/unverified stated",)),
    "report": Phase("report", "Report with evidence", "delivery-lead", ("change-readiness",), _MCP_AUDIT, ("evidence, unverified, risk, next actions",)),
}

# P5: reuse common phases (avoid duplicate definitions)
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
    "writing": ("plan", "implement", "verify", "report"),
}

# Override agent/skills only for a specific workflow's phase
PHASE_OVERRIDES: dict[tuple[str, str], dict[str, object]] = {
    ("ui-delivery", "implement"): {"agent": "web-designer", "skills": ("web-experience-design", "frontend-design")},
    ("writing", "implement"): {"agent": "docs-specialist", "skills": ("writing-fragments", "writing-beats", "writing-shape")},
    ("writing", "verify"): {"skills": ("research",)},
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
    """Whether this workflow has an implement phase (if not, implementation requires a workflow switch)."""
    return any(p.id == "implement" for p in phases_for(workflow_id))


# Attach phases to WorkflowSpec (replace, since it is frozen)
import dataclasses as _dc  # noqa: E402

WORKFLOWS = {wid: _dc.replace(spec, phases=phases_for(wid)) for wid, spec in WORKFLOWS.items()}
WORKFLOW_AGENTS = {wid: spec.agent for wid, spec in WORKFLOWS.items()}


