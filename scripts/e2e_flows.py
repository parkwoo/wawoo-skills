#!/usr/bin/env python3
"""キット E2E（契約・ACTIVE 状態機械・MCP・workflow）。API キー不要。stdlib のみ。"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KILO = ROOT / ".kilo"
MEMORY_OPS = ROOT / "mcp" / "memory_ops.py"

sys.path.insert(0, str(ROOT / "scripts"))
from plan_active import ActiveTask, parse_active, validate_tasks  # noqa: E402
from plan_l2_backlog import BacklogItem, parse_backlog, validate_backlog  # noqa: E402
from plan_l3_record import validate_l3_record  # noqa: E402


def load_memory_ops():
    spec = importlib.util.spec_from_file_location("memory_ops", MEMORY_OPS)
    if not spec or not spec.loader:
        raise RuntimeError("memory_ops not found")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fm(path: Path) -> dict[str, str]:
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


def rpc(proc, payload: dict) -> dict:
    proc.stdin.write(json.dumps(payload) + "\n")
    proc.stdin.flush()
    line = proc.stdout.readline()
    if not line:
        raise RuntimeError("MCP: no response")
    return json.loads(line)


def mcp_call(name: str, arguments: dict) -> dict:
    proc = subprocess.Popen(
        [sys.executable, str(ROOT / "mcp" / "server.py")],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=str(ROOT),
    )
    try:
        rpc(proc, {"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "e2e", "version": "0"}}})
        return rpc(
            proc,
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {"name": name, "arguments": arguments},
            },
        )
    finally:
        try:
            proc.stdin.close()
        except Exception:
            pass
        proc.wait(timeout=30)


class Runner:
    def __init__(self) -> None:
        self.passed = 0
        self.failed = 0

    def run(self, name: str, fn) -> None:
        try:
            fn()
            self.passed += 1
            print(f"PASS {name}")
        except AssertionError as exc:
            self.failed += 1
            print(f"FAIL {name}: {exc}")
        except Exception as exc:
            self.failed += 1
            print(f"ERROR {name}: {exc}")


def test_repo_active_template(r: Runner) -> None:
    def _():
        path = ROOT / "docs" / "plans" / "ACTIVE.md"
        assert path.is_file()
        tasks = parse_active(path)
        assert validate_tasks(tasks) == []
        text = path.read_text(encoding="utf-8")
        assert "delivery-lite" in text
        assert "/delivery-lite" in text

    r.run("repo_active_template", _)


def test_active_state_machine_rules(r: Runner) -> None:
    def _():
        issues = validate_tasks(
            [
                ActiveTask("T1", "doing", "a", "ok", ""),
                ActiveTask("T2", "doing", "b", "ok", ""),
            ]
        )
        assert any("more than one doing" in i for i in issues)

        issues = validate_tasks(
            [ActiveTask("T1", "done", "a", "ok", "")]
        )
        assert any("done without evidence" in i for i in issues)

        issues = validate_tasks(
            [ActiveTask("T1", "done", "a", "ok", "python3 scripts/validate_assets.py")]
        )
        assert issues == []

        issues = validate_tasks([ActiveTask("T1", "wut", "a", "ok", "")])
        assert any("invalid status" in i for i in issues)

    r.run("active_state_machine_rules", _)


def test_active_happy_path_file(r: Runner) -> None:
    def _():
        sample = """# ACTIVE

## タスク

| id | status | 内容 | 完了条件 | 証拠 |
|----|--------|------|----------|------|
| T1 | todo | x | y | |
| T2 | doing | z | ok | |
"""
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "ACTIVE.md"
            p.write_text(sample, encoding="utf-8")
            tasks = parse_active(p)
            assert len(tasks) == 2
            assert validate_tasks(tasks) == []

    r.run("active_happy_path_file", _)


def test_contract_agents_ssot(r: Runner) -> None:
    def _():
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        assert "タスクと進捗の正本（SSOT）" in text
        assert "docs/plans/ACTIVE.md" in text
        assert "delivery-lite" in text
        assert "L0" in text or "L0–L3" in text

    r.run("contract_agents_ssot", _)


def test_contract_methodology_levels(r: Runner) -> None:
    def _():
        text = (ROOT / "docs" / "METHODOLOGY.md").read_text(encoding="utf-8")
        assert "L0" in text and "L3" in text
        assert "delivery-lite" in text
        assert "ACTIVE.md" in text

    r.run("contract_methodology_levels", _)


def test_workflow_delivery_lite(r: Runner) -> None:
    def _():
        p = KILO / "commands" / "delivery-lite.md"
        assert p.is_file()
        meta = fm(p)
        assert meta.get("agent") == "implementer"
        body = p.read_text(encoding="utf-8")
        for needle in (
            "docs/plans/ACTIVE.md",
            "memory_save",
            "plan_active",
            "Gₑ",
            "明示したときのみ",
        ):
            assert needle in body, f"missing {needle}"

    r.run("workflow_delivery_lite", _)


def test_workflow_feature_delivery_escalation(r: Runner) -> None:
    def _():
        body = (KILO / "commands" / "feature-delivery.md").read_text(encoding="utf-8")
        assert "delivery-lite" in body

    r.run("workflow_feature_delivery_escalation", _)


def test_all_commands_have_agent(r: Runner) -> None:
    def _():
        agents = {f.stem for f in (KILO / "agents").glob("*.md")}
        for f in (KILO / "commands").glob("*.md"):
            if f.stem == "README":
                continue
            meta = fm(f)
            assert meta.get("description"), f"{f.name} missing description"
            a = meta.get("agent")
            assert a and a in agents, f"{f.name} agent={a}"

    r.run("all_commands_have_agent", _)


def test_mcp_workflow_get_delivery_lite(r: Runner) -> None:
    def _():
        res = mcp_call("workflow_get", {"name": "delivery-lite"})
        assert not res["result"].get("isError"), res
        text = res["result"]["content"][0]["text"]
        assert "ACTIVE" in text

    r.run("mcp_workflow_get_delivery_lite", _)


def test_mcp_memory_roundtrip_isolated(r: Runner) -> None:
    def _():
        mem = load_memory_ops()
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            msg = mem.save_memory(
                d,
                "E2E テスト用の制約",
                "constraint,topic:e2e",
                "scripts/e2e_flows.py",
            )
            assert "MEM-" in msg
            assert (d / "e2e.md").is_file()
            got = mem.recall_memory(d, "E2E 制約", 3)
            assert "制約" in got or "E2E" in got
            try:
                mem.save_memory(d, "ghp_abcdefghijklmnopqrstuvwxyz123456", "fix")
                raise AssertionError("secret should be rejected")
            except ValueError:
                pass

    r.run("mcp_memory_roundtrip_isolated", _)


def test_mcp_evidence_check(r: Runner) -> None:
    def _():
        res = mcp_call("evidence_check", {"scope": "assets"})
        assert not res["result"].get("isError"), res
        text = res["result"]["content"][0]["text"]
        assert "OK:" in text or "skills=" in text

    r.run("mcp_evidence_check", _)


def test_plan_active_cli(r: Runner) -> None:
    def _():
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "plan_active.py")],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr

    r.run("plan_active_cli", _)


def test_active_blocked_and_duplicate(r: Runner) -> None:
    def _():
        issues = validate_tasks([ActiveTask("T1", "blocked", "wait", "ok", "")])
        assert issues == []

        issues = validate_tasks(
            [
                ActiveTask("T1", "todo", "a", "ok", ""),
                ActiveTask("T1", "done", "b", "ok", "evidence"),
            ]
        )
        assert any("duplicate id" in i for i in issues)

    r.run("active_blocked_and_duplicate", _)


def test_mcp_memory_recall_repo(r: Runner) -> None:
    def _():
        res = mcp_call("memory_recall", {"query": "ACTIVE SSOT delivery", "top_k": 3})
        text = res["result"]["content"][0]["text"]
        assert text != "no memory matches", text
        assert "ACTIVE" in text or "delivery" in text.lower() or "SSOT" in text

    r.run("mcp_memory_recall_repo", _)


def test_workflow_status_report_active(r: Runner) -> None:
    def _():
        body = (KILO / "commands" / "status-report.md").read_text(encoding="utf-8")
        assert "ACTIVE.md" in body
        assert "L1" in body

    r.run("workflow_status_report_active", _)


def test_delivery_lite_level_l0_documented(r: Runner) -> None:
    def _():
        body = (KILO / "commands" / "delivery-lite.md").read_text(encoding="utf-8")
        assert "**L0**" in body
        assert "ACTIVE を更新せず" in body or "更新せず" in body

    r.run("delivery_lite_level_l0_documented", _)


def test_l0_simulated_flow(r: Runner) -> None:
    """L0: ACTIVE を増やさず、プレースホルダのみで検証が通る（計画ファイル不要）。"""

    def _():
        path = ROOT / "docs" / "plans" / "ACTIVE.md"
        tasks = parse_active(path)
        assert validate_tasks(tasks) == []
        assert len(tasks) == 0
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        assert "L0" in agents
        meth = (ROOT / "docs" / "METHODOLOGY.md").read_text(encoding="utf-8")
        assert "git diff" in meth or "L0" in meth
        with tempfile.TemporaryDirectory() as td:
            work = Path(td) / "patch.txt"
            work.write_text("l0 evidence\n", encoding="utf-8")
            assert work.read_text().strip() == "l0 evidence"

    r.run("l0_simulated_flow", _)


def test_l2_backlog_state_rules(r: Runner) -> None:
    def _():
        issues = validate_backlog(
            [
                BacklogItem("I1", "in_progress", "a", ""),
                BacklogItem("I2", "in_progress", "b", ""),
            ]
        )
        assert any("in_progress" in i for i in issues)
        issues = validate_backlog([BacklogItem("I1", "done", "a", "")])
        assert any("done without evidence" in i for i in issues)

    r.run("l2_backlog_state_rules", _)


def test_l2_simulated_flow(r: Runner) -> None:
    """L2: バックログ open → in_progress → done（証拠付き）。"""

    def _():
        template = (ROOT / "docs" / "plans" / "BACKLOG.example.md").read_text(encoding="utf-8")
        row_open = "| E2E-42 | open | backlog item | |\n"
        row_ip = "| E2E-42 | in_progress | backlog item | |\n"
        row_done = "| E2E-42 | done | backlog item | issue #42 merged |\n"
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "BACKLOG.md"
            base = template.replace(
                "| — | — | （スプリント計画時に追加） | |",
                row_open,
            )
            p.write_text(base, encoding="utf-8")
            assert validate_backlog(parse_backlog(p)) == []

            text = p.read_text(encoding="utf-8").replace(row_open, row_ip)
            p.write_text(text, encoding="utf-8")
            assert validate_backlog(parse_backlog(p)) == []

            text = p.read_text(encoding="utf-8").replace(row_ip, row_done)
            p.write_text(text, encoding="utf-8")
            assert validate_backlog(parse_backlog(p)) == []

        body = (KILO / "commands" / "sprint-plan.md").read_text(encoding="utf-8")
        assert "L2" in body and "plan_l2_backlog" in body
        assert "to-tickets" in body

        ready = json.loads((ROOT / "scripts" / "readiness.json").read_text(encoding="utf-8"))
        res = mcp_call("capabilities", {"ready_only": True})
        text = res["result"]["content"][0]["text"]
        for skill in (ready.get("needs_setup") or {}):
            assert f"skill    {skill}" not in text, f"L2 readiness: {skill} must be hidden when ready_only"

    r.run("l2_simulated_flow", _)


def test_l3_simulated_flow(r: Runner) -> None:
    """L3: PDCA 記録ファイル + memory（学び）。ACTIVE に done を書かない。"""

    def _():
        sample = (ROOT / "docs" / "plans" / "RETRO.example.md").read_text(encoding="utf-8")
        assert validate_l3_record(sample) == []

        mem = load_memory_ops()
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            retro = Path(td) / "RETRO.md"
            retro.write_text(sample, encoding="utf-8")
            assert validate_l3_record(retro.read_text(encoding="utf-8")) == []

            msg = mem.save_memory(
                d,
                "L3 E2E: retro で手順を 1 行更新する",
                "fix,topic:process",
                "scripts/e2e_flows.py",
            )
            assert "MEM-" in msg
            got = mem.recall_memory(d, "L3 retro", 2)
            assert "retro" in got.lower() or "手順" in got

        body = (KILO / "commands" / "self-improve.md").read_text(encoding="utf-8")
        for needle in ("retro", "pdca-cycle", "memory"):
            assert needle in body, needle

        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "plan_l3_record.py")],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr

    r.run("l3_simulated_flow", _)


def test_ceremony_levels_matrix(r: Runner) -> None:
    """METHODOLOGY §5 の L0–L3 が workflow・SSOT と対応している。"""

    def _():
        text = (ROOT / "docs" / "METHODOLOGY.md").read_text(encoding="utf-8")
        assert "**L0**" in text and "**L3**" in text
        assert "/delivery-lite" in text
        assert "/sprint-plan" in text
        assert "/self-improve" in text
        assert "ACTIVE.md" in text
        assert "issue tracker" in text

    r.run("ceremony_levels_matrix", _)


def test_l1_simulated_flow(r: Runner) -> None:
    """L1: タスク追加 → doing → done（証拠付き）の一連操作をファイルで再現。"""

    def _():
        template = (ROOT / "docs" / "plans" / "ACTIVE.md").read_text(encoding="utf-8")
        row_todo = "| E2E-1 | todo | e2e flow | validate passes | |\n"
        row_doing = "| E2E-1 | doing | e2e flow | validate passes | |\n"
        row_done = "| E2E-1 | done | e2e flow | validate passes | python3 scripts/e2e_flows.py |\n"
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "ACTIVE.md"
            base = template.replace(
                "| — | — | （新規依頼時にエージェントが行を追加） | | |",
                row_todo,
            )
            p.write_text(base, encoding="utf-8")
            assert validate_tasks(parse_active(p)) == []

            text = p.read_text(encoding="utf-8")
            text = text.replace(row_todo, row_doing)
            p.write_text(text, encoding="utf-8")
            assert validate_tasks(parse_active(p)) == []

            text = p.read_text(encoding="utf-8")
            text = text.replace(row_doing, row_done)
            p.write_text(text, encoding="utf-8")
            assert validate_tasks(parse_active(p)) == []

    r.run("l1_simulated_flow", _)


def test_content_delivery_lite_contract(r: Runner) -> None:
    def _():
        p = KILO / "commands" / "content-delivery-lite.md"
        body = p.read_text(encoding="utf-8")
        assert "CONTENT.md" in body and "plan_content" in body
        res = mcp_call("workflow_get", {"name": "content-delivery-lite"})
        assert "CONTENT" in res["result"]["content"][0]["text"]

    r.run("content_delivery_lite_contract", _)


def test_deliverable_workflows_active_hooks(r: Runner) -> None:
    def _():
        for name in ("ui-delivery", "research", "market-plan"):
            body = (KILO / "commands" / f"{name}.md").read_text(encoding="utf-8")
            assert "ACTIVE.md" in body, name

    r.run("deliverable_workflows_active_hooks", _)


def test_content_simulated_flow(r: Runner) -> None:
    def _():
        sys.path.insert(0, str(ROOT / "scripts"))
        from plan_content import parse_content, validate_content

        template = (ROOT / "docs/plans/CONTENT.example.md").read_text(encoding="utf-8")
        row = "| CH-1 | todo | intro | draft ok | |\n"
        base = template.replace("| — | — | （目次確定後に追加） | | |", row)
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "CONTENT.md"
            p.write_text(base, encoding="utf-8")
            assert validate_content(parse_content(p)) == []
            done = "| CH-1 | done | intro | draft ok | docs/chapters/01.md |\n"
            p.write_text(base.replace(row, done), encoding="utf-8")
            assert validate_content(parse_content(p)) == []

    r.run("content_simulated_flow", _)


def test_agent_active_sandbox_dry(r: Runner) -> None:
    """実機 E2E の dry: sandbox ACTIVE/CONTENT 更新 → plan_*（login 不要）。"""

    def _():
        script = ROOT / "internal.example/scripts/e2e/agent-active-live.sh"
        if not script.is_file():
            raise AssertionError("missing internal.example agent-active-live.sh")
        for wf in ("delivery-lite", "content-delivery-lite"):
            proc = subprocess.run(
                ["bash", str(script), wf],
                cwd=str(ROOT),
                env={**dict(os.environ), "MODE": "dry"},
                capture_output=True,
                text=True,
                timeout=60,
            )
            assert proc.returncode == 0, (wf, proc.stdout, proc.stderr)

    r.run("agent_active_sandbox_dry", _)


def test_cli_adapters_mock_subprocess(r: Runner) -> None:
    def _():
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "cli_adapters_mock.py")],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=120,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr

    r.run("cli_adapters_mock_subprocess", _)


def main() -> int:
    r = Runner()
    tests = [
        test_repo_active_template,
        test_active_state_machine_rules,
        test_active_happy_path_file,
        test_contract_agents_ssot,
        test_contract_methodology_levels,
        test_workflow_delivery_lite,
        test_workflow_feature_delivery_escalation,
        test_all_commands_have_agent,
        test_mcp_workflow_get_delivery_lite,
        test_mcp_memory_roundtrip_isolated,
        test_mcp_evidence_check,
        test_plan_active_cli,
        test_active_blocked_and_duplicate,
        test_mcp_memory_recall_repo,
        test_workflow_status_report_active,
        test_delivery_lite_level_l0_documented,
        test_l0_simulated_flow,
        test_l1_simulated_flow,
        test_l2_backlog_state_rules,
        test_l2_simulated_flow,
        test_l3_simulated_flow,
        test_ceremony_levels_matrix,
        test_content_delivery_lite_contract,
        test_deliverable_workflows_active_hooks,
        test_content_simulated_flow,
        test_agent_active_sandbox_dry,
        test_cli_adapters_mock_subprocess,
    ]
    print("== e2e_flows ==")
    for t in tests:
        t(r)
    print(f"== summary: passed={r.passed} failed={r.failed} ==")
    return 1 if r.failed else 0


if __name__ == "__main__":
    sys.exit(main())
