"""Intent interpretation — L0 explicit/command → L1 learned → L2 upstream score; DB writes are async."""
from __future__ import annotations

import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal

from intent_catalog import (
    WORKFLOW_AGENTS,
    catalog_for_upstream,
    implement_allowed,
    mcp_tools_allow,
    phase_dicts,
    workflow_spec,
)
from intent_commands import match_slash_route
from intent_learn_queue import enqueue_hit, enqueue_promote, flush, reset_learn_queue
from intent_learned_store import IntentLearnedStore, default_db_path
from intent_seed import seed_learned_store
from intent_upstream import (
    UpstreamScoring,
    parse_upstream,
    upstream_score_prompt,
    workflow_ids_compact,
)

UpstreamClassification = UpstreamScoring

Confidence = Literal["high", "medium", "low"]
Source = Literal["explicit", "learned", "upstream", "pending", "fallback"]
RouteLayer = Literal["L0", "L1", "L2"]

_store: IntentLearnedStore | None = None
_LEARN_MIN_SCORE = 0.85


def reset_intent_store() -> None:
    global _store
    _store = None
    reset_learn_queue()


def _get_store() -> IntentLearnedStore:
    global _store
    if _store is None:
        root = Path(os.environ.get("WAWOO_SKILLS_ROOT", "")).expanduser() if os.environ.get("WAWOO_SKILLS_ROOT") else None
        _store = IntentLearnedStore(default_db_path(root if root and root.exists() else Path(__file__).resolve().parents[1]))
        seed_learned_store(_store)
    return _store


def _skills_root() -> Path:
    env = os.environ.get("WAWOO_SKILLS_ROOT", "").strip()
    if env:
        p = Path(env).expanduser()
        if p.exists():
            return p
    return Path(__file__).resolve().parents[1]


def _score_to_confidence(score: float) -> Confidence:
    if score >= 0.85:
        return "high"
    if score >= 0.6:
        return "medium"
    return "low"


@dataclass
class IntentSchedule:
    intent_id: str
    task_type: str
    workflow: str
    workflow_slash: str
    agent: str
    confidence: Confidence
    prompt: str
    clean_text: str
    source: Source = "fallback"
    route_layer: RouteLayer = "L2"
    route_subsource: str = ""
    score: float | None = None
    explicit_override: bool = False
    message: str = ""
    trace: list[str] = field(default_factory=list)
    learn_queued: bool = False
    workflow_description: str = ""
    command_path: str = ""
    mcp_tools_allow: list[str] = field(default_factory=list)
    delegation_hint: str = ""
    phases: list[dict[str, Any]] = field(default_factory=list)
    gate: str = ""
    implement_allowed: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _enrich_workflow_meta(schedule: IntentSchedule) -> IntentSchedule:
    spec = workflow_spec(schedule.workflow)
    if spec:
        schedule.workflow_description = spec.description
        schedule.mcp_tools_allow = mcp_tools_allow(schedule.workflow)
        schedule.delegation_hint = spec.delegation
    else:
        schedule.mcp_tools_allow = mcp_tools_allow(schedule.workflow)
    schedule.phases = phase_dicts(schedule.workflow)
    schedule.implement_allowed = implement_allowed(schedule.workflow)
    if schedule.phases and not schedule.implement_allowed:
        schedule.gate = "This workflow is read-only phases only. If implementation is needed, declare the reason and a new workflow (e.g. feature-delivery) and switch."
    return schedule


def _schedule_from_workflow(
    raw: str,
    workflow: str,
    *,
    intent_id: str,
    task_type: str,
    confidence: Confidence,
    source: Source,
    route_layer: RouteLayer,
    route_subsource: str = "",
    score: float | None,
    trace: list[str],
    explicit: bool = False,
    message: str = "",
    learn_queued: bool = False,
    command_path: str = "",
) -> IntentSchedule:
    agent = WORKFLOW_AGENTS.get(workflow, "implementer")
    sched = IntentSchedule(
        intent_id=intent_id,
        task_type=task_type,
        workflow=workflow,
        workflow_slash=f"/{workflow}",
        agent=agent,
        confidence=confidence,
        prompt=f"/{workflow} {raw}".strip(),
        clean_text=raw,
        source=source,
        route_layer=route_layer,
        route_subsource=route_subsource,
        score=score,
        explicit_override=explicit,
        message=message,
        trace=trace,
        learn_queued=learn_queued,
        command_path=command_path,
    )
    return _enrich_workflow_meta(sched)


def apply_upstream_scoring(
    text: str,
    scoring: UpstreamScoring,
    *,
    intent_id: str = "",
    learn: bool = True,
) -> IntentSchedule:
    """Apply the upstream LLM scoring result (SQLite promotion goes to the queue). """
    raw = (text or "").strip()
    trace = [f"L2:upstream:{scoring.workflow}:{scoring.score:.2f}"]
    learn_queued = False
    if learn and scoring.score >= _LEARN_MIN_SCORE:
        trace.append("learn:queued")
        enqueue_promote(
            _get_store(),
            trigger=scoring.trigger,
            workflow=scoring.workflow,
            confidence=scoring.score,
        )
        learn_queued = True
    return _schedule_from_workflow(
        raw,
        scoring.workflow,
        intent_id=intent_id or "upstream",
        task_type="scored",
        confidence=_score_to_confidence(scoring.score),
        source="upstream",
        route_layer="L2",
        route_subsource="upstream_score",
        score=scoring.score,
        trace=trace,
        learn_queued=learn_queued,
    )


apply_upstream_classification = apply_upstream_scoring


def interpret_intent_payload(
    text: str,
    *,
    intent_id: str = "",
    learn: bool = False,
    classification: dict[str, Any] | None = None,
    scoring: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """For MCP: a compact dict. If scoring/classification is present, apply the upstream score."""
    raw = (text or "").strip()
    upstream_json = scoring if scoring is not None else classification
    if upstream_json:
        parsed = parse_upstream(upstream_json)
        if not parsed:
            return {"ok": False, "error": "invalid scoring json (need workflow, score, trigger)"}
        sched = apply_upstream_scoring(raw, parsed, intent_id=intent_id, learn=learn)
        return {"ok": True, "needs_upstream": False, "needs_scoring": False, "route_layer": "L2", "schedule": sched.to_dict()}

    if not raw:
        sched = IntentSchedule(
            intent_id="empty",
            task_type="unknown",
            workflow="delivery-lite",
            workflow_slash="/delivery-lite",
            agent=WORKFLOW_AGENTS["delivery-lite"],
            confidence="low",
            prompt="/delivery-lite",
            clean_text="",
            source="fallback",
            route_layer="L2",
            message="empty",
            trace=["empty_input"],
        )
        sched = _enrich_workflow_meta(sched)
        return {"ok": True, "needs_upstream": False, "schedule": sched.to_dict()}

    slash = match_slash_route(raw, _skills_root())
    if slash:
        sched = _schedule_from_workflow(
            slash.clean_text,
            slash.workflow,
            intent_id=intent_id or "explicit",
            task_type="explicit",
            confidence="high",
            source="explicit",
            route_layer="L0",
            route_subsource=slash.route_subsource,
            score=1.0,
            trace=[f"L0:{slash.route_subsource}:/{slash.command_stem}"],
            explicit=True,
            command_path=slash.command_path,
        )
        return {"ok": True, "needs_upstream": False, "needs_scoring": False, "route_layer": "L0", "schedule": sched.to_dict()}

    store = _get_store()
    learned_route = store.find_match(raw)
    if learned_route:
        enqueue_hit(store, learned_route.route_id)
        sched = _schedule_from_workflow(
            raw,
            learned_route.workflow,
            intent_id=intent_id or f"learned-{learned_route.route_id}",
            task_type="learned",
            confidence=_score_to_confidence(learned_route.confidence),
            source="learned",
            route_layer="L1",
            route_subsource="learned_trigger",
            score=learned_route.confidence,
            trace=[f"L1:learned:{learned_route.trigger}"],
        )
        return {"ok": True, "needs_upstream": False, "needs_scoring": False, "route_layer": "L1", "schedule": sched.to_dict()}

    prompt = upstream_score_prompt(raw)
    return {
        "ok": True,
        "needs_upstream": True,
        "needs_scoring": True,
        "route_layer": "L2",
        "text": raw,
        "upstream_prompt": prompt,
        "no_thinking": True,
        "workflows": workflow_ids_compact(),
        "workflow_catalog": catalog_for_upstream(),
        "score_schema": {"workflow": "id", "score": "0.0-1.0 fit to input", "trigger": "2-40 chars from input"},
        "delegation_note": "L3 (subagent delegation) happens after the workflow starts, in the host agent's execution phase (interpret goes as far as L2).",
    }


def interpret_intent(
    text: str,
    *,
    intent_id: str = "",
    learn: bool = False,
    classification: dict[str, Any] | None = None,
    scoring: dict[str, Any] | None = None,
) -> IntentSchedule:
    """CLI compatibility: when you only want the schedule."""
    payload = interpret_intent_payload(
        text, intent_id=intent_id, learn=learn, classification=classification, scoring=scoring
    )
    if payload.get("needs_upstream"):
        return _schedule_from_workflow(
            text.strip(),
            "delivery-lite",
            intent_id=intent_id or "pending",
            task_type="pending",
            confidence="low",
            source="pending",
            route_layer="L2",
            route_subsource="needs_scoring",
            score=None,
            trace=["L2:needs_scoring"],
            message=payload.get("upstream_prompt", payload.get("hint", "")),
        )
    if not payload.get("ok"):
        raise ValueError(payload.get("error", "interpret failed"))
    d = payload["schedule"]
    return IntentSchedule(**d)


def format_needs_scoring_text(payload: dict[str, Any]) -> str:
    lines = [
        "NEEDS SCORING (L2)",
        "=" * 50,
        "No L1 learned route matched. Have the upstream LLM read the full input and assign a workflow fitness score.",
        "Do not use thinking mode; return one JSON line. Then pass scoring to interpret_intent.",
        "learn=true only on re-applying an upstream decision (optional).",
        "L3 delegation happens after the workflow starts (host agent / Task).",
        "=" * 50,
        "",
        payload.get("upstream_prompt", ""),
    ]
    return "\n".join(lines)


def format_route_task_text(schedule: IntentSchedule) -> str:
    lines = [
        "TASK CLASSIFICATION",
        "=" * 50,
        f"Route: {schedule.route_layer}" + (f" ({schedule.route_subsource})" if schedule.route_subsource else ""),
        f"Type: {schedule.task_type.upper()}",
        f"Workflow: {schedule.workflow_slash}",
        f"Agent: {schedule.agent}",
        f"Source: {schedule.source}",
        f"Confidence: {schedule.confidence.upper()}",
    ]
    if schedule.workflow_description:
        lines.append(f"Description: {schedule.workflow_description}")
    if schedule.command_path:
        lines.append(f"Command: {schedule.command_path}")
    if schedule.mcp_tools_allow:
        lines.append(f"MCP allow: {','.join(schedule.mcp_tools_allow)}")
    if schedule.delegation_hint:
        lines.append(f"Delegation (L3): {schedule.delegation_hint}")
    if schedule.score is not None:
        lines.append(f"Score: {schedule.score:.2f}")
    if schedule.learn_queued:
        lines.append("Learn: queued (async)")
    lines.extend(["=" * 50, "", "PROMPT:", schedule.prompt])
    return "\n".join(lines)


def flush_learn_writes() -> None:
    """For tests."""
    flush(_get_store())
