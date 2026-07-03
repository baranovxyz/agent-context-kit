"""Stdlib-only tests for agent-ready-check. Run: python3 tests/test_budget_checks.py"""
import importlib.util
import importlib.machinery
import json
import subprocess
import sys
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


def levels(issues):
    return {i["level"] for i in issues}


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def lines(n: int) -> str:
    return "".join(f"line {i}\n" for i in range(n))


def prompt(slug="foo", status="active", last_session="2026-06-16", **extra) -> str:
    fields = {"slug": slug, "status": status, "last_session": last_session, **extra}
    body = "\n".join(f"{k}: {v}" for k, v in fields.items() if v is not None)
    return f"---\n{body}\n---\n\n# prompt body\n"


def run_cli(root: Path, *args):
    result = subprocess.run(
        [sys.executable, str(CHECKER), "--root", str(root), *args],
        capture_output=True, text=True,
    )
    parsed = {}
    if "--json" in args and result.stdout.strip():
        parsed = json.loads(result.stdout)
    return result.returncode, parsed, result


# --- retained byte budget / density / broken-ref behavior -------------------

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


# --- shape / exit code / severity -------------------------------------------

def test_clean_repo_is_ok_and_exits_0():
    with tempfile.TemporaryDirectory() as d:
        write(Path(d) / "AGENTS.md", "# A\nshort and lean\n")
        write(Path(d) / "CLAUDE.md", "@AGENTS.md\n")
        code, data, _ = run_cli(Path(d), "--json")
        assert code == 0, data
        assert data["ok"] is True and data["issue_count"] == 0, data


def test_red_issue_exits_1_and_not_ok():
    with tempfile.TemporaryDirectory() as d:
        # AGENTS.md with no sibling CLAUDE.md shim is a red structural fault.
        write(Path(d) / "AGENTS.md", "# A\nshort\n")
        code, data, _ = run_cli(Path(d), "--json")
        assert code == 1 and data["ok"] is False, data
        assert any(i["level"] == "red" for i in data["issues"]), data


def test_unknown_only_name_is_usage_error():
    with tempfile.TemporaryDirectory() as d:
        code, _, result = run_cli(Path(d), "--json", "--only", "no-such-check")
        assert code == 2 and "unknown check" in result.stderr, result.stderr


def test_yellow_only_exits_0():
    with tempfile.TemporaryDirectory() as d:
        write(Path(d) / "AGENTS.md", lines(250))  # T1 yellow band (200-300)
        write(Path(d) / "CLAUDE.md", "@AGENTS.md\n")
        code, data, _ = run_cli(Path(d), "--json")
        assert code == 0 and data["ok"] is True, data
        assert any(i["level"] == "yellow" for i in data["issues"]), data
        assert not any(i["level"] == "red" for i in data["issues"]), data


# --- tiered budgets ---------------------------------------------------------

def test_tier_t1_nested_agents_md_red_over_300():
    mod = load_checker()
    with tempfile.TemporaryDirectory() as d:
        mod.ROOT = Path(d)
        write(Path(d) / "pkg" / "AGENTS.md", lines(301))
        issues = []
        mod.check_budgets(issues)
        assert any("T1 red band" in i["message"] and i["level"] == "red" for i in issues), messages(issues)


def test_tier_t2_skill_yellow_band():
    mod = load_checker()
    with tempfile.TemporaryDirectory() as d:
        mod.ROOT = Path(d)
        write(Path(d) / "skills" / "demo" / "SKILL.md", lines(400))  # T2 300-500
        issues = []
        mod.check_budgets(issues)
        assert any("T2 yellow band" in i["message"] and i["level"] == "yellow" for i in issues), messages(issues)


def test_tier_t4_plan_red_over_band_and_green_under():
    mod = load_checker()
    with tempfile.TemporaryDirectory() as d:
        mod.ROOT = Path(d)
        write(Path(d) / "docs" / "plans" / "big.md", lines(301))   # T4 red (>300)
        write(Path(d) / "docs" / "plans" / "small.md", lines(50))  # T4 green
        issues = []
        mod.check_budgets(issues)
        assert any("big.md" in i["message"] and i["level"] == "red" for i in issues), messages(issues)
        assert not any("small.md" in i["message"] for i in issues), messages(issues)


def test_archive_dir_is_exempt():
    mod = load_checker()
    with tempfile.TemporaryDirectory() as d:
        mod.ROOT = Path(d)
        write(Path(d) / "docs" / "plans" / "archive" / "old.md", lines(999))
        issues = []
        mod.check_budgets(issues)
        assert not issues, messages(issues)


def test_density_applies_to_nested_tiered_file():
    mod = load_checker()
    with tempfile.TemporaryDirectory() as d:
        mod.ROOT = Path(d)
        write(Path(d) / "docs" / "plans" / "p.md", "ok\n" + ("z" * 1600) + "\n")
        issues = []
        mod.check_budgets(issues, max_line_chars=1500)
        assert any("char cap" in i["message"] for i in issues), messages(issues)


# --- config loader (flag > file > default) ----------------------------------

def test_config_loosens_tier_band():
    with tempfile.TemporaryDirectory() as d:
        write(Path(d) / "docs" / "plans" / "big.md", lines(400))  # red under default T4
        write(Path(d) / ".agent-ready-check.json", json.dumps(
            {"tiers": [{"name": "T4", "globs": ["docs/plans/**/*.md"], "green": 1000, "yellow": 2000}]}
        ))
        code, data, _ = run_cli(Path(d), "--json", "--only", "budgets")
        assert code == 0 and not any(i["level"] == "red" for i in data["issues"]), data


def test_cli_flag_overrides_config_file():
    with tempfile.TemporaryDirectory() as d:
        write(Path(d) / "docs" / "plans" / "p.md", "ok\n" + ("z" * 1600) + "\n")
        write(Path(d) / ".agent-ready-check.json", json.dumps({"max_line_chars": 99999}))
        # File loosens the cap: the long line passes.
        _, data_file, _ = run_cli(Path(d), "--json", "--only", "budgets")
        assert not any("char cap" in i["message"] for i in data_file["issues"]), data_file
        # Flag tightens it back: the long line is red again (flag > file).
        _, data_flag, _ = run_cli(Path(d), "--json", "--only", "budgets", "--max-line-chars", "1500")
        assert any("char cap" in i["message"] for i in data_flag["issues"]), data_flag


# --- continuation-prompt lifecycle ------------------------------------------

def test_lifecycle_bad_status_is_red():
    mod = load_checker()
    with tempfile.TemporaryDirectory() as d:
        mod.ROOT = Path(d)
        write(Path(d) / "docs" / "plans" / "p.md", prompt(status="wip"))
        issues = []
        mod.check_continuation_lifecycle(issues)
        assert any("invalid status" in i["message"] and i["level"] == "red" for i in issues), messages(issues)


def test_lifecycle_superseded_without_superseded_by_is_red():
    mod = load_checker()
    with tempfile.TemporaryDirectory() as d:
        mod.ROOT = Path(d)
        write(Path(d) / "docs" / "plans" / "p.md", prompt(status="superseded"))
        issues = []
        mod.check_continuation_lifecycle(issues)
        assert any("dangling chain head" in i["message"] and i["level"] == "red" for i in issues), messages(issues)


def test_lifecycle_closed_outside_archive_is_flagged():
    mod = load_checker()
    with tempfile.TemporaryDirectory() as d:
        mod.ROOT = Path(d)
        write(Path(d) / "docs" / "plans" / "p.md", prompt(status="shipped"))
        issues = []
        mod.check_continuation_lifecycle(issues)
        assert any("lives outside" in i["message"] and i["level"] == "yellow" for i in issues), messages(issues)


def test_lifecycle_closed_inside_archive_is_clean():
    mod = load_checker()
    with tempfile.TemporaryDirectory() as d:
        mod.ROOT = Path(d)
        write(Path(d) / "docs" / "plans" / "archive" / "p.md", prompt(status="shipped"))
        issues = []
        mod.check_continuation_lifecycle(issues)
        assert not issues, messages(issues)


def test_lifecycle_valid_active_is_green():
    mod = load_checker()
    with tempfile.TemporaryDirectory() as d:
        mod.ROOT = Path(d)
        write(Path(d) / "docs" / "plans" / "p.md", prompt(status="active"))
        issues = []
        mod.check_continuation_lifecycle(issues)
        assert not issues, messages(issues)


def test_lifecycle_missing_required_field_is_red():
    mod = load_checker()
    with tempfile.TemporaryDirectory() as d:
        mod.ROOT = Path(d)
        write(Path(d) / "docs" / "plans" / "p.md", prompt(last_session=None))
        issues = []
        mod.check_continuation_lifecycle(issues)
        assert any("missing `last_session`" in i["message"] and i["level"] == "red" for i in issues), messages(issues)


# --- git-age staleness (injectable clock, graceful no-git) ------------------

def test_staleness_flags_old_active_prompt():
    mod = load_checker()
    with tempfile.TemporaryDirectory() as d:
        mod.ROOT = Path(d)
        write(Path(d) / "docs" / "plans" / "p.md", prompt(status="active"))
        fixed_now = 1_000_000_000
        mod._last_commit_epoch = lambda rel: fixed_now - 40 * 86400  # 40 days old
        issues = []
        mod.check_staleness(issues, max_age_days=30, now=fixed_now)
        assert any("stale head" in i["message"] and i["level"] == "yellow" for i in issues), messages(issues)


def test_staleness_passes_fresh_active_prompt():
    mod = load_checker()
    with tempfile.TemporaryDirectory() as d:
        mod.ROOT = Path(d)
        write(Path(d) / "docs" / "plans" / "p.md", prompt(status="active"))
        fixed_now = 1_000_000_000
        mod._last_commit_epoch = lambda rel: fixed_now - 5 * 86400  # 5 days old
        issues = []
        mod.check_staleness(issues, max_age_days=30, now=fixed_now)
        assert not issues, messages(issues)


def test_staleness_skips_gracefully_without_git():
    mod = load_checker()
    with tempfile.TemporaryDirectory() as d:
        mod.ROOT = Path(d)  # not a git repo
        write(Path(d) / "docs" / "plans" / "p.md", prompt(status="active"))
        issues = []
        mod.check_staleness(issues, max_age_days=1, now=1_000_000_000)
        assert not issues, messages(issues)


# --- --changed scoping ------------------------------------------------------

def test_changed_scopes_to_listed_path():
    mod = load_checker()
    with tempfile.TemporaryDirectory() as d:
        mod.ROOT = Path(d)
        a = write(Path(d) / "docs" / "plans" / "a.md", lines(301))
        write(Path(d) / "docs" / "plans" / "b.md", lines(301))
        issues = []
        mod.check_budgets(issues, changed={a})
        assert any("a.md" in i["message"] for i in issues), messages(issues)
        assert not any("b.md" in i["message"] for i in issues), messages(issues)


def test_changed_path_outside_any_glob_is_noop():
    mod = load_checker()
    with tempfile.TemporaryDirectory() as d:
        mod.ROOT = Path(d)
        readme = write(Path(d) / "README.md", lines(999))
        issues = []
        mod.check_budgets(issues, changed={readme})
        assert not issues, messages(issues)


# --- hook + markdownlint template ship --------------------------------------

def test_posttooluse_hook_is_registered():
    hooks = json.loads((CHECKER.parent.parent / "hooks" / "hooks.json").read_text())
    entries = hooks["hooks"].get("PostToolUse", [])
    assert entries, "PostToolUse hook missing"
    command = entries[0]["hooks"][0]
    assert command["type"] == "command", command
    assert "agent-ready-check" in command["command"] and "--changed" in command["command"], command


def test_markdownlint_template_ships_and_is_valid():
    template = CHECKER.parent.parent / ".markdownlint.json"
    assert template.exists(), "markdownlint template missing"
    data = json.loads(template.read_text())
    assert "MD013" in data, data


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("ALL PASS")
