"""上流 LLM：入力全文を読み workflow 適合度を score 化（別 API なし）。"""
from __future__ import annotations

from dataclasses import dataclass

from intent_catalog import WORKFLOW_AGENTS, catalog_for_upstream

# workflow + 適合度 score + 学習用 trigger
UPSTREAM_FIELDS = ("workflow", "score", "trigger")

_NO_THINK_RULES = (
    "【意図スコアリング】extended thinking/思索/推理モードは使わない。"
    "chain-of-thought・・分析過程・前置き・markdown・コードブロック禁止。"
    "ユーザーへの自然文は書かない。出力はJSON1行のみ。"
)

_SCORE_RULES = (
    "入力全文を読み、最も適する workflow を1つ選び、"
    "その入力に対する適合度を score(0.0-1.0) で必ず付ける。"
    "未確定・曖昧でも score は付与（低くてよい）。分類だけで score を省略しない。"
    "trigger は入力から抽出した短いフレーズ（学習用・2-40字）。"
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
    """上流 LLM：入力文章に対する workflow 適合度スコアリング用プロンプト。"""
    text = (user_text or "").strip()
    if len(text) > max_input:
        text = text[: max_input - 1] + "…"
    catalog = _catalog_prompt_segment()
    return (
        f"{_NO_THINK_RULES} {_SCORE_RULES} "
        f'JSON:{{"workflow":"<id>","score":0.0-1.0,"trigger":"2-40字"}} '
        f"候補(id:いつ使う)={catalog} "
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
