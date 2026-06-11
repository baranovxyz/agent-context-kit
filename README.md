# Agent Context Kit

Tool-neutral repository context and memory tooling for coding agents. This repository is packaged as
a Claude Code marketplace, while the guidance inside `agent-ready-repo` is designed to remain useful
for Claude Code, Cursor, Codex, OpenCode, and other agent hosts.

## Included Plugins

- `agent-ready-repo` - keeps agent-facing repository memory layered, current, and maintainable
  across `AGENTS.md`, docs, skills, agents, hooks, CLI, and MCP surfaces.
- `spec-driven` - authoring and evolution workflow for living specs and ADRs: keeps `docs/specs` the
  source of truth and `docs/adr` the immutable decision log.

## Install

The repo ships parallel marketplace manifests for three hosts. The plugin body (`skills/`,
`agents/`, `hooks/`, `AGENTS.md`) is shared; only the thin `.{host}-plugin/` wrappers differ per
host.

### Claude Code

```shell
/plugin marketplace add <owner>/agent-context-kit
/plugin install agent-ready-repo@agent-context-kit
/plugin install spec-driven@agent-context-kit
```

Reload during an active session with `/reload-plugins`.

### Cursor

After Cursor's marketplace picks up the repo (or via team marketplace setup), install
`agent-ready-repo` and/or `spec-driven`. Cursor reads `.cursor-plugin/marketplace.json` at the repo
root and `plugins/<plugin>/.cursor-plugin/plugin.json` per plugin. See the
[Cursor plugins reference](https://cursor.com/docs/plugins/building) for current install flows.

### Codex (OpenAI)

Codex reads `.agents/plugins/marketplace.json` at the repo root and
`plugins/<plugin>/.codex-plugin/plugin.json`. Add the marketplace via the Codex CLI's plugin
marketplace flow (see [Codex plugin docs](https://developers.openai.com/codex/plugins)) and select
`agent-ready-repo` or `spec-driven` from the picker.

## Local Testing

For Claude Code, from the **parent directory** of your local checkout:

```shell
/plugin marketplace add ./agent-context-kit
/plugin install agent-ready-repo@agent-context-kit
/plugin install spec-driven@agent-context-kit
```

Or from **inside** the checkout:

```shell
/plugin marketplace add .
/plugin install agent-ready-repo@agent-context-kit
/plugin install spec-driven@agent-context-kit
```

For direct plugin development without the marketplace layer (point `--plugin-dir` at the plugin
you're working on):

```bash
claude --plugin-dir ./plugins/agent-ready-repo
claude --plugin-dir ./plugins/spec-driven
```

## Release Notes

Each plugin is versioned independently (currently `agent-ready-repo` `0.5.2`, `spec-driven`
`0.2.0`).

When publishing a release for a plugin, bump its version in the three marketplace entries plus its
three per-plugin manifests so all hosts receive updates:
- `.claude-plugin/marketplace.json`
- `.cursor-plugin/marketplace.json`
- `.agents/plugins/marketplace.json`
- `plugins/<plugin>/.claude-plugin/plugin.json`
- `plugins/<plugin>/.cursor-plugin/plugin.json`
- `plugins/<plugin>/.codex-plugin/plugin.json`

`bin/agent-ready-check` warns when these drift.

For git-backed Claude Code marketplace version resolution, tag releases using Claude Code's plugin
tag convention:

```bash
cd plugins/agent-ready-repo
claude plugin tag --push
```

Use `--dry-run` first when preparing a release.

## Open Source Checklist

Before making the repository public:

- Run `python3 plugins/agent-ready-repo/bin/agent-ready-check --root . --json`.
- Confirm all host manifests list the same plugin names, descriptions, versions, authors, licenses,
  and keywords.
- Search for private paths, credentials, and organization-only references.
- Keep the GitHub Actions check green on the public default branch.
