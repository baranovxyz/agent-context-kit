# Plugin Architecture Notes

## Superpowers Pattern

Use skills as process gates:

- check whether a skill applies before acting;
- brainstorm before designing;
- plan before executing;
- verify before claiming completion.

For this plugin, that means audit before migration, classify before editing, and validate after writing.

Monorepos get their own process gate: use `monorepo-agent-context` before changing root and package-level instruction files together. Package boundaries change what should load always, what should load locally, and what belongs in host-specific wiring.

## BMAD Pattern

Map roles to agents and workflows to skills.

Correct:

- `docs-maintainer` as an agent;
- `agent-ready-maintenance` as a skill.

Incorrect:

- treating a role such as "architect" as a skill;
- putting workflow steps inside an agent that should be reusable by multiple workers.

## Claude Code Plugin Shape

Use:

```text
.claude-plugin/plugin.json
skills/*/SKILL.md
agents/*.md
commands/*.md
hooks/hooks.json
bin/*
references/*
```

Keep component directories at plugin root. Do not put them inside `.claude-plugin/`.

Do not add custom `skills`, `commands`, or `agents` paths to `plugin.json` unless moving away from default directories intentionally. Current Claude Code docs say these custom paths replace defaults, so an unnecessary path field can hide standard components.

`commands/` is now a legacy flat-skill location. Existing command files still work, but new workflows should be modeled as `skills/<name>/SKILL.md` so they can use supporting files and invocation controls.

`bin/` executables are available on the Bash tool `PATH` while the plugin is enabled. Any executable intended for agents, humans, or CI should offer structured output such as `--json` and stable exit codes.

Plugin subagents can use newer frontmatter fields such as `maxTurns`, `effort`, `skills`, `memory`, `background`, and `isolation: worktree`, but add them only for a specific behavior change. Avoid persistent `memory` for cross-repository evaluators, and do not use `hooks`, `mcpServers`, or `permissionMode` in plugin-shipped agents because Claude Code ignores those fields for plugin agents.

## Description Metadata Compatibility

Use one-line plain-text `description` metadata for every skill and agent. The description must include both capability and trigger context because some hosts do not support Claude-specific fields such as `when_to_use`.

Do not put examples, XML-like tags, Markdown, code fences, lists, conversation transcripts, YAML block scalars, or `when_to_use` in frontmatter. Put longer trigger guidance in the Markdown body so tools that parse only simple YAML strings stay compatible.

## Cursor Cross-Host Shape

Cursor uses `.cursor-plugin/plugin.json` and adds `rules/`. A future Cursor package should keep portable rules in `docs/rules/` and use Cursor rules for globs and routing.

`AGENTS.md` remains the first-class shared instruction contract across hosts. `CLAUDE.md` exists because Claude Code loads it; Cursor, Codex, OpenCode, and other hosts should use `AGENTS.md` directly or thin host-specific wrappers around it.

## Mega-Plugin Caution

Large plugin inventories are useful as ecosystem maps, but this plugin should not ship every possible skill or agent. It should ship a small core that recommends new artifacts when evidence appears.

Do not add marketplace scaffolding, dependencies, LSP servers, monitors, channels, or MCP servers unless Agent Ready Repo has a concrete local readiness job that needs them.
