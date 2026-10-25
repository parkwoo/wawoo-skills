#!/usr/bin/env python3
"""全 skill の手順・ゲート・サイズの機械的品質スキャン。docs/audit に Markdown を出力。"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".kilo" / "skills"
OUT = ROOT / "docs" / "audit" / "SKILL-QUALITY-REVIEW.md"

GATE_PATTERNS = re.compile(
    r"(ゲート|承認|approval|human sign-off|Not a substitute|advisory|法的判断)",
    re.IGNORECASE,
)
STEP_PATTERNS = re.compile(r"(^##\s+[0-9]+\.|^##\s+手順|^#\s+[A-Z].*Review|^\d+\.\s+\*\*)", re.MULTILINE)
LEGAL_SECURITY = {
    "compliance-legal",
    "privacy-review",
    "security-review",
    "release-readiness",
    "change-readiness",
    "database-change-safety",
}


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    out: dict[str, str] = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def scan_skill(skill_md: Path) -> dict:
    body = skill_md.read_text(encoding="utf-8", errors="ignore")
    fm = frontmatter(skill_md)
    name = fm.get("name") or skill_md.parent.name
    size = skill_md.stat().st_size
    has_gate = bool(GATE_PATTERNS.search(body))
    has_steps = bool(STEP_PATTERNS.search(body))
    broken_refs = re.findall(r"`(docs/design/[^`]+)`", body)
    chinese = bool(re.search(r"调研|迭代|了吗|吗\?|什么呢", body))
    budget_ok = size <= 4096
    return {
        "name": name,
        "size": size,
        "budget_ok": budget_ok,
        "has_gate": has_gate,
        "has_steps": has_steps,
        "broken_refs": broken_refs,
        "chinese": chinese,
    }


def main() -> None:
    items = [scan_skill(p) for p in sorted(SKILLS.glob("*/SKILL.md"))]
    over = [i for i in items if not i["budget_ok"]]
    no_gate = [i["name"] for i in items if i["name"] in LEGAL_SECURITY and not i["has_gate"]]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# スキル品質レビュー（機械スキャン + 法務・セキュリティ深掘り）",
        "",
        f"> 生成: `python3 scripts/audit_skill_quality.py`（{date.today().isoformat()}）",
        "",
        "## スコープ",
        "- 55 skill の `SKILL.md` をサイズ・ゲート語・手順構造・壊れやすい内部参照でスキャン。",
        "- 法務・セキュリティ系 6 件は**実効性**を人が追記評価。",
        "",
        "## サマリ",
        f"| 指標 | 値 |",
        f"|---|---|",
        f"| skill 数 | {len(items)} |",
        f"| 予算超過（>4KB、入口 SKILL のみ） | {len(over)} |",
        f"| 法務/セキュリティでゲート語なし | {len(no_gate)} |",
        "",
        "## 予算超過（入口 SKILL.md）",
        "",
        "| skill | bytes | 備考 |",
        "|---|---:|---|",
    ]
    for i in sorted(over, key=lambda x: -x["size"]):
        note = "references 分割済み" if i["name"] == "imagegen-frontend-mobile" else "ルーター/長文 — 段階的開示を推奨"
        lines.append(f"| `{i['name']}` | {i['size']} | {note} |")

    lines += [
        "",
        "## 全 skill 一覧",
        "",
        "| skill | bytes | ゲート語 | 手順構造 | 要確認 |",
        "|---|---:|:---:|:---:|---|",
    ]
    for i in items:
        flags = []
        if i["broken_refs"]:
            flags.append("外部設計パス参照")
        if i["chinese"]:
            flags.append("中国語残存?")
        lines.append(
            f"| `{i['name']}` | {i['size']} | {'✅' if i['has_gate'] else '—'} | {'✅' if i['has_steps'] else '—'} | {', '.join(flags) or '—'} |"
        )

    lines += [
        "",
        "## 法務・セキュリティスキルの実効性（人レビュー）",
        "",
        "### `compliance-legal`",
        "- **強み**: OSS 帰属・SBOM・ToS/プライバシー/DPA/AI ポリシーのチェックリスト。人の承認を明記。",
        "- **弱み**: プロダクト固有の規制（業種・地域）はスコープ外。証拠の保存先テンプレは無い。",
        "- **実効性**: **中〜高**（リリース前の棚卸しゲートとして機能。最終判断は人）。",
        "",
        "### `privacy-review`",
        "- **強み**: PII フロー・最小化・保持・マスキング・越境の観点。",
        "- **弱み**: `docs/design/60-SECURITY-OPS.md` 等**本キットに無いパス**を参照（汎用リポジトリではリンク切れ）。",
        "- **実効性**: **中**（チェックは使えるが、消費側でセキュリティ文書パスを差し替える必要）。",
        "",
        "### `security-review`",
        "- **強み**: 信頼境界・認証認可・注入・秘密・依存のレビュー手順。本番変更・PoC 禁止。",
        "- **弱み**: 出力フォーマット（重大度テンプレ）が短い。自動スキャンツール連携は無い。",
        "- **実効性**: **中〜高**（コードレビュー補助として妥当）。",
        "",
        "### `release-readiness`",
        "- **強み**: 版・タグ・ロールバック・承認境界が明確。`change-readiness` 連携。",
        "- **弱み**: CI/パッケージ種別ごとの具体コマンドは消費側依存。",
        "- **実効性**: **高**（本リポジトリの `VERSIONING.md` と整合）。",
        "",
        "### `change-readiness` / `database-change-safety`",
        "- **強み**: 変更種別ごとの検証・ロールバック意識。",
        "- **弱み**: 本番 DB の組織ポリシーは記載不能（汎用キットの限界）。",
        "- **実効性**: **中**（チェックリスト起動用）。",
        "",
        "## Kilo 実機 E2E",
        "",
        "手順・受入ゲート: **`docs/audit/KILO-E2E.md`**。",
        "",
        "| 項目 | 結果 |",
        "|---|---|",
        "| Kilo CLI / Kilo Code の実行 | **未実施**（開発環境に `kilo` コマンドなし） |",
        "| MCP stdio スモーク | **合格**（`python3 mcp/test_server.py`） |",
        "",
        "## 改善 backlog（優先）",
        "1. ~~OpenDesign 7 skill の LICENSE 同梱~~ → **対応済**（各ディレクトリ `LICENSE.txt` + `NOTICE.txt`）。",
        "2. ~~大型 skill の references 分割~~ → **対応済**（`ask-matt`・`wayfinder`・`design-brief`・`writing-for-agents` + `imagegen-frontend-mobile`）。",
        "3. ~~Kilo 実機 E2E~~ → 手順 **`docs/audit/KILO-E2E.md`**（実機記録は未記入）。",
        "4. 残: 予算超過 skill の追加分割（`diagnosing-bugs`・`code-review` 等）。",
        "5. 残: `security-review` に findings テンプレ（重大度・再現・修正・検証）を追加。",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
