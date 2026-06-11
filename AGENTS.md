# AGENTS.md

## Project Overview
Agent Context Kit is a Claude Code plugin marketplace repository for tool-neutral coding-agent
context and memory guidance.

## Structure
```text
.claude-plugin/marketplace.json   # Claude Code marketplace manifest
.cursor-plugin/marketplace.json   # Cursor marketplace manifest
.agents/plugins/marketplace.json  # Codex marketplace manifest (preferred path)
plugins/agent-ready-repo/         # Agent Ready Repo plugin
  .claude-plugin/plugin.json      # Claude Code plugin manifest
  .cursor-plugin/plugin.json      # Cursor plugin manifest
  .codex-plugin/plugin.json       # Codex plugin manifest (with interface block)
  AGENTS.md                       # Plugin-specific development guidance
  README.md                       # User-facing component overview
  skills/*/SKILL.md               # Model-invoked procedures
  agents/*.md                     # Autonomous worker roles
  hooks/hooks.json                # Non-editing drift reminder
  bin/agent-ready-check           # Preflight checker (--json)
  references/*.md                 # Reference material
```

## Key Files
- `README.md` - installation and release notes.
- `plugins/agent-ready-repo/AGENTS.md` - plugin-specific development guidance.
- `plugins/agent-ready-repo/.claude-plugin/plugin.json` - plugin manifest.

## Verification
```bash
python3 plugins/agent-ready-repo/bin/agent-ready-check --json
python3 -m py_compile plugins/agent-ready-repo/bin/agent-ready-check
```

## Conventions
- Keep repository-level guidance short; put plugin-specific rules in
  `plugins/agent-ready-repo/AGENTS.md`.
- Treat `AGENTS.md` as first-class shared instruction truth; use host-specific files such as
  `CLAUDE.md` only as loading or capability wiring.
- Keep skill and agent frontmatter descriptions as one-line plain text with capability and trigger
  context.
- Do not use `when_to_use`, multiline YAML scalars, tags, Markdown, or examples in frontmatter
  descriptions.
- When changing anything under `plugins/agent-ready-repo/`, bump the version in every marketplace
  and plugin manifest so all hosts receive updates. Files to update:
  `.claude-plugin/marketplace.json`, `.cursor-plugin/marketplace.json`,
  `.agents/plugins/marketplace.json`, and the three per-plugin manifests under
  `plugins/agent-ready-repo/.{claude,cursor,codex}-plugin/plugin.json`. `agent-ready-check` warns
  when these drift.
- Keep marketplace plugin metadata (description, version, keywords) aligned across all three
  marketplace manifests and their corresponding plugin manifests.
- The body components (`skills/`, `agents/`, `hooks/hooks.json`, `AGENTS.md`) are shared across all
  hosts; only the thin `.{host}-plugin/` wrappers differ.
- Claude and Cursor marketplaces take `source` as a string (`"./plugins/..."`); Codex takes an
  object (`{ "source": "local", "path": "./plugins/..." }`) and the path cannot be `"./"` (Codex bug
  #17066). See `plugins/agent-ready-repo/references/multi-host-plugin-distribution.md`.
- Do not add marketplace dependencies or new plugins unless there is a concrete runtime need.
