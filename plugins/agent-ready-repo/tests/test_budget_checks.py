"""Stdlib-only tests for agent-ready-check budget checks. Run: python3 tests/test_budget_checks.py"""
import importlib.util
import importlib.machinery
import tempfile
from pathlib import Path

CHECKER = Path(__file__).resolve().parent.parent / "bin" / "agent-ready-check"


def load_checker():
    loader = importlib.machinery.SourceFileLoader("agent_ready_check", str(CHECKER))
    spec = importlib.util.spec_from_loader("agent_ready_check", loader)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def messages(issues):
    return " | ".join(i["message"] for i in issues)


def test_byte_budget_trips_when_over():
    mod = load_checker()
    with tempfile.TemporaryDirectory() as d:
        mod.ROOT = Path(d)
        (Path(d) / "AGENTS.md").write_text("# A\n" + ("x " * 20000), encoding="utf-8")
        issues = []
        mod.check_agents_md(issues, max_bytes=24000, max_line_chars=1500)
        assert any("bytes; budget" in m for m in [i["message"] for i in issues]), messages(issues)


def test_byte_budget_passes_when_under():
    mod = load_checker()
    with tempfile.TemporaryDirectory() as d:
        mod.ROOT = Path(d)
        (Path(d) / "AGENTS.md").write_text("# A\nshort and lean\n", encoding="utf-8")
        issues = []
        mod.check_agents_md(issues, max_bytes=24000, max_line_chars=1500)
        assert not any("bytes; budget" in i["message"] for i in issues), messages(issues)


def test_long_line_trips():
    mod = load_checker()
    with tempfile.TemporaryDirectory() as d:
        mod.ROOT = Path(d)
        (Path(d) / "AGENTS.md").write_text("# A\n" + ("z" * 1600) + "\n", encoding="utf-8")
        issues = []
        mod.check_agents_md(issues, max_bytes=999999, max_line_chars=1500)
        assert any("char cap" in i["message"] for i in issues), messages(issues)


def test_long_line_inside_code_fence_is_ignored():
    mod = load_checker()
    with tempfile.TemporaryDirectory() as d:
        mod.ROOT = Path(d)
        body = "# A\n```\n" + ("z" * 1600) + "\n```\n"
        (Path(d) / "AGENTS.md").write_text(body, encoding="utf-8")
        issues = []
        mod.check_agents_md(issues, max_bytes=999999, max_line_chars=1500)
        assert not any("char cap" in i["message"] for i in issues), messages(issues)


def test_angle_bracket_placeholder_refs_are_not_flagged():
    mod = load_checker()
    with tempfile.TemporaryDirectory() as d:
        mod.ROOT = Path(d)
        (Path(d) / "AGENTS.md").write_text(
            "# A\nSee `docs/peer-sources/<name>.md` and "
            "`docs/harness-plans/CONTINUATION-PROMPT-<slug>.md`.\n",
            encoding="utf-8",
        )
        issues = []
        mod.check_agents_md(issues)
        assert not any("references missing file" in i["message"] for i in issues), messages(issues)


def test_bare_filename_without_path_is_not_flagged():
    mod = load_checker()
    with tempfile.TemporaryDirectory() as d:
        mod.ROOT = Path(d)
        (Path(d) / "AGENTS.md").write_text(
            "# A\nThe `2026-05-17-hosted-controller.md` note covers the direction.\n",
            encoding="utf-8",
        )
        issues = []
        mod.check_agents_md(issues)
        assert not any("references missing file" in i["message"] for i in issues), messages(issues)


def test_real_missing_path_reference_is_still_flagged():
    mod = load_checker()
    with tempfile.TemporaryDirectory() as d:
        mod.ROOT = Path(d)
        (Path(d) / "AGENTS.md").write_text(
            "# A\nSee `docs/does-not-exist.md` for details.\n", encoding="utf-8"
        )
        issues = []
        mod.check_agents_md(issues)
        assert any("references missing file" in i["message"] for i in issues), messages(issues)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("ALL PASS")
