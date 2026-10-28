"""Upstream LLM: read the full input and score workflow fitness (no separate API)."""
from __future__ import annotations

from dataclasses import dataclass

from intent_catalog import WORKFLOW_AGENTS, catalog_for_upstream

# workflow + 適合度 score + 学習用 trigger
UPSTREAM_FIELDS = ("workflow", "score", "trigger")

_NO_THINK_RULES = (
    "[intent scoring]Do not use extended thinking or deliberation mode."
    "No chain-of-thought, analysis, preamble, markdown, or code blocks."
    "Do not write prose to the user. Output one JSON line only."
)

_SCORE_RULES = (
    "Read the full input, choose the single most fitting workflow,"
    "and always assign the fitness score(0.0-1.0) for that input."
    "Even if uncertain or ambiguous, still give a score (it may be low). Never omit the score when classifying."
    "trigger is a short phrase extracted from the input (for learning, 2-40 chars)."
)


@dataclass
class UpstreamScoring:
    workflow: str
    score: float
    trigger: str

    @property
    def ok(self) -> bool:
        return (
            self.workflow in WORKFLOW_AGENTS
            and 0.0 <= self.score <= 1.0
            and 2 <= len((self.trigger or "").strip()) <= 40
        )


# 後方互換
UpstreamClassification = UpstreamScoring


def workflow_ids_compact() -> list[str]:
    return sorted(WORKFLOW_AGENTS.keys())


def _catalog_prompt_segment(max_items: int = 15) -> str:
    parts: list[str] = []
    for row in catalog_for_upstream()[:max_items]:
        parts.append(f"{row['id']}:{row['description']}")
    return "|".join(parts)


def upstream_score_prompt(user_text: str, max_input: int = 2000) -> str:
    """Upstream LLM: the prompt for scoring workflow fitness for the input text."""
    text = (user_text or "").strip()
    if len(text) > max_input:
        text = text[: max_input - 1] + "…"
    catalog = _catalog_prompt_segment()
    return (
        f"{_NO_THINK_RULES} {_SCORE_RULES} "
        f'JSON:{{"workflow":"<id>","score":0.0-1.0,"trigger":"2-40字"}} '
        f"candidates(id:when to use)={catalog} "
        f"入力全文:{text}"
    )


def upstream_classify_prompt(user_text: str, max_input: int = 2000) -> str:
    """alias: upstream_score_prompt"""
    return upstream_score_prompt(user_text, max_input=max_input)


def upstream_hint() -> str:
    ids = ",".join(workflow_ids_compact())
    return f"{_NO_THINK_RULES} {_SCORE_RULES} JSON workflow/score/trigger workflow∈{ids}"


def parse_upstream(data: dict) -> UpstreamScoring | None:
    if not isinstance(data, dict):
        return None
    wf = str(data.get("workflow", "")).strip()
    raw_score = data.get("score", data.get("rating", data.get("confidence")))
    try:
        score = float(raw_score if raw_score is not None else 0)
    except (TypeError, ValueError):
        return None
    trigger = str(data.get("trigger", "")).strip()
    c = UpstreamScoring(workflow=wf, score=score, trigger=trigger)
    return c if c.ok else None
