# Research Notes

Use these notes as background, not as claims to repeat without checking source context.

## AGENTS.md Evidence

The useful synthesis is cautious:

- human-curated `AGENTS.md` can reduce runtime and output tokens in some coding-agent settings;
- generated or bloated context files can increase steps, reduce task success, and raise cost;
- therefore the goal is not "more context", but selected context with clear addresses.

## Skills Evidence

SkillsBench supports focused skills:

- curated skills improved average pass rate in the benchmark;
- some tasks worsened;
- 2-3 focused skill modules outperformed broader collections;
- self-generated or exhaustive skills were weaker.

Design implication: do not create a mega-plugin of generic skills. Recommend new skills only when a repeated procedure is observed.

## Security Evidence

Public skills are dependencies:

- review skill text;
- pin versions where possible;
- scan bundled scripts;
- avoid remote execution and credential handling in skills;
- prefer trusted publishers.

Anthropic's enterprise guidance extends this into a lifecycle:

- assess risk before deployment;
- review scripts, MCP references, network access, credentials, and file access scope;
- evaluate trigger accuracy, isolation behavior, coexistence, instruction following, and output quality;
- monitor usage and failures after deployment;
- deprecate stale or persistently failing skills.

## Plugin Architecture Evidence

Superpowers shows process-as-skills. BMAD shows roles-as-agents and workflows-as-skills. Cursor and Claude plugin docs show the same broad component mix, but host semantics differ.

Design implication: keep portable truth in repo docs, and keep host-specific packaging thin.

## Current Anthropic Docs Evidence

The May 2026 Claude Code docs change several maintenance details:

- `commands/` still works, but commands and skills are now the same mechanism; use `skills/` for new workflows because it supports resources, invocation controls, and progressive disclosure.
- Plugin default component paths are enough for this plugin. Custom path fields in `plugin.json` replace defaults for skills, commands, and agents.
- `bin/` is on `PATH` when a plugin is enabled, so deterministic tools should be agent-friendly: `--json`, stable exit codes, no prompts in non-TTY contexts.
- Prompt hooks return strict `{ "ok": true|false, "reason": "..." }` JSON. Stop hooks do not need matchers.
- Plugin subagents support newer fields, but the safe default is to add only fields with clear value. Persistent memory and worktree isolation are not default choices for repository-memory auditors.
- Plugin dependencies and marketplace metadata are distribution features, not readiness features. Add them only when the plugin has runtime dependencies or is being published through a marketplace.
