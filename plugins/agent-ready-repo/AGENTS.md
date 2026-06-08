# AGENTS.md

## Project Overview
Agent Ready Repo keeps repository memory layered across first-class `AGENTS.md`, `docs/`, host-specific files, skills, agents, hooks, CLI, and MCP surfaces. The plugin ships parallel manifests for Claude Code, Cursor, and Codex; the body components (`skills/`, `agents/`, `hooks/`) are shared across all three hosts.

## Docs
Read these when changing plugin behavior:

- `README.md` - user-facing overview, components, local testing
- `references/layered-architecture.md` - layer definitions and placement rules
- `references/artifact-decision-matrix.md` - where new knowledge belongs
- `references/plugin-architecture-notes.md` - Superpowers, BMAD, Claude, Cursor plugin patterns
- `references/research-notes.md` - evidence and caveats behind the model
- `references/anthropic-plugin-docs-implications.md` - current Claude Code plugin and memory implications
- `references/anthropic-skill-authoring-best-practices.md` - official guidance for skill metadata, descriptions, structure, and progressive disclosure
- `references/anthropic-skills-for-enterprise.md` - official guidance for skill governance, security review, evaluation, deployment, and lifecycle management
- `references/multi-host-plugin-distribution.md` - manifest shapes for Claude/Cursor/Codex, version-sync rules, and known Codex bugs to work around
- `references/always-loaded-context-budget.md` - why always-loaded files are the scarce resource and how the byte/line budget check enforces it

## Project Structure
```text
.claude-plugin/plugin.json  # Claude Code plugin manifest
.cursor-plugin/plugin.json  # Cursor plugin manifest
.codex-plugin/plugin.json   # Codex plugin manifest (includes interface block)
skills/*/SKILL.md           # model-invoked procedures (shared across hosts)
agents/*.md                 # autonomous worker roles (shared across hosts)
commands/*.md               # legacy flat skills; prefer skills/*/SKILL.md for new workflows
hooks/hooks.json            # non-editing drift reminder (shared across hosts)
bin/agent-ready-check       # deterministic preflight checker with --json, not the evaluator
references/*.md             # plugin reference material
```

## Verification
```bash
python3 -m json.tool .claude-plugin/plugin.json >/dev/null
python3 -m json.tool .cursor-plugin/plugin.json >/dev/null
python3 -m json.tool .codex-plugin/plugin.json >/dev/null
python3 -m json.tool hooks/hooks.json >/dev/null
python3 -m py_compile bin/agent-ready-check
# Run agent-ready-check from repo root so it sees all marketplace manifests:
( cd ../.. && python3 plugins/agent-ready-repo/bin/agent-ready-check --json )
```

## Conventions
- Keep skills focused on procedures, not durable project facts.
- Treat `AGENTS.md` as the portable source of shared instruction truth; `CLAUDE.md` is Claude Code loading and capability wiring.
- Use `monorepo-agent-context` when root and package-level instruction files interact.
- Write skill and agent descriptions as one-line plain text with both capability and trigger context.
- Never use `when_to_use`, multiline YAML scalars, examples, tags, Markdown, or transcripts in frontmatter descriptions.
- Treat skills as governed dependencies: review, evaluate, deploy, monitor, and deprecate them deliberately.
- Keep agents as worker roles with least-privilege tools; put trigger examples in the Markdown body when needed.
- Prefer skills over new command files; use `disable-model-invocation: true` for user-only side-effect workflows.
- Keep hooks safe, non-editing, easy to disable, and explicit about prompt-hook JSON output.
- Treat `agent-ready-check` output as preflight evidence; the `agent-ready-auditor` agent performs the real evaluation.
- Use `${CLAUDE_PLUGIN_ROOT}` for plugin-internal references from skills, commands, and hooks.
- Do not add plugin dependencies, marketplace entries, MCP servers, LSP servers, monitors, channels, or settings unless this plugin has a concrete runtime need for them.
- Use `CLAUDE.md` only because Claude Code loads it; keep shared truth in `AGENTS.md` and use `@AGENTS.md` imports or pointers to avoid duplication.

## Boundaries
- Always validate JSON and Python syntax after changing manifest, hooks, or `bin/`.
- Always update README and references when changing plugin behavior.
- Never duplicate shared project truth into host-specific files.
- Never make the Stop hook auto-edit files.
