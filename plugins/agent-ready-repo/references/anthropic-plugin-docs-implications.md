# Anthropic Plugin Docs Implications

Use this reference when maintaining Agent Ready Repo against current Anthropic skill and plugin guidance.

## What The Current Design Gets Right

- Package shared, reusable agent-readiness procedures as a plugin instead of one-project `.claude/` configuration.
- Keep component directories at the plugin root: `skills/`, `agents/`, `hooks/`, `bin/`, and `references/`.
- Treat `AGENTS.md` as a portable always-on contract and `CLAUDE.md` as Claude Code memory that can import `AGENTS.md`.
- Keep the deterministic checker separate from qualitative evaluation by `agent-ready-auditor`.
- Keep hooks non-editing. Hooks enforce or remind; they must not silently rewrite repository memory.

## Current Docs Updates To Preserve

- Commands and skills now share the same invocation mechanism. Existing files in `commands/` still work, but new plugin workflows should use `skills/<name>/SKILL.md` because skills support resources, invocation controls, and progressive disclosure.
- Plugin `bin/` executables are added to the Bash tool's `PATH` while the plugin is enabled. Executables intended for agents or CI should support structured output, semantic exit codes, and non-interactive use.
- Custom component paths in `plugin.json` replace defaults for `skills`, `commands`, `agents`, `outputStyles`, `themes`, and `monitors`. Do not add custom path fields unless the plugin intentionally moves components away from default directories.
- Plugin subagents support newer fields such as `maxTurns`, `effort`, `skills`, `memory`, `background`, and `isolation: worktree`. Add them only when they change behavior intentionally. Plugin subagents do not support `hooks`, `mcpServers`, or `permissionMode`.
- Prompt hooks must return strict JSON with `{ "ok": true }` or `{ "ok": false, "reason": "..." }`. Stop hooks do not use matchers.

## What Not To Add By Default

- Do not add marketplace scaffolding just because marketplaces exist. Add `.claude-plugin/marketplace.json` only when distributing a catalog.
- Do not add `dependencies` unless this plugin requires another plugin at runtime.
- Do not add LSP servers, monitors, channels, MCP servers, or user configuration without a concrete local readiness job.
- Do not preload skills into agents by default. Preloading injects the full skill content into the agent context; prefer a self-contained agent prompt unless the skill materially improves the worker.
- Do not enable persistent agent memory for repository audits by default. Cross-repository learnings can contaminate evaluation.

## Enterprise Governance Implications

- Treat team-shared skills and plugin dependencies as reviewed software dependencies.
- Keep a lightweight skill registry with owner, purpose, risk tier, version, evaluation notes, and deprecation criteria for shared skills.
- Evaluate trigger accuracy, should-not-trigger cases, coexistence with other skills, tool permissions, script safety, and output quality before deployment.
- Review bundled scripts, network access, MCP references, credential handling, and broad file access as security risk factors.
- For organization rollout, document which settings are managed centrally and which repository artifacts remain local guidance.

## Memory Split

- `AGENTS.md`: short, portable contract for all coding agents.
- `CLAUDE.md`: Claude Code memory file; import `@AGENTS.md` and add Claude-only guidance below it.
- `.claude/rules/`: path-scoped Claude Code guidance that should not load globally.
- `docs/`: durable architecture, specs, plans, ADRs, runbooks, troubleshooting, and codebase maps.
- Skills: repeatable procedures that should load on demand, not every session.
- Hooks, CLI, MCP, and CI: executable contracts or governed live access when text guidance is insufficient.
