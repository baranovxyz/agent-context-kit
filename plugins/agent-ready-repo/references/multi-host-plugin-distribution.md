# Multi-Host Plugin Distribution

Reference for shipping this plugin (and any future plugin in this marketplace) across Claude Code,
Cursor, and Codex without duplicating body content.

## Manifest Locations

| Host | Marketplace manifest | Per-plugin manifest |
|---|---|---|
| Claude Code | `.claude-plugin/marketplace.json` | `plugins/<name>/.claude-plugin/plugin.json` |
| Cursor | `.cursor-plugin/marketplace.json` | `plugins/<name>/.cursor-plugin/plugin.json` |
| Codex | `.agents/plugins/marketplace.json` (preferred) | `plugins/<name>/.codex-plugin/plugin.json` |

Codex still honors `.claude-plugin/marketplace.json` as a legacy fallback, but
`.agents/plugins/marketplace.json` is the path documented by OpenAI.

## Shared vs Host-Specific

| Component | Shared? | Notes |
|---|---|---|
| `AGENTS.md` | Yes | Natively read by Codex CLI, GitHub Copilot, Cursor, Windsurf, Amp, Devin. Claude reads `CLAUDE.md`, Gemini reads `GEMINI.md`. |
| `skills/*/SKILL.md` | Yes | Same frontmatter and body across hosts. |
| `agents/*.md` | Yes | Frontmatter `name` + `description` is portable. |
| `hooks/hooks.json` | Yes | Schema is shared across hosts. |
| `references/*.md` | Yes | Just markdown. |
| `.{host}-plugin/*.json` | No | One thin wrapper per host. |

## `source` Field Shape Differs By Host

Claude Code and Cursor marketplaces take `source` as a **string**:

```json
{ "name": "agent-ready-repo", "source": "./plugins/agent-ready-repo" }
```

Codex takes `source` as an **object** and supports installation policy:

```json
{
  "name": "agent-ready-repo",
  "source": { "source": "local", "path": "./plugins/agent-ready-repo" },
  "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" }
}
```

Using Cursor/Claude string form in the Codex marketplace will not install.

## Codex Plugin Manifest Adds an `interface` Block

The Codex plugin manifest mirrors the Claude/Cursor fields and adds an optional `interface` block
used by the Codex marketplace picker:

- `displayName`, `shortDescription`, `longDescription`
- `category`, `capabilities[]`
- `defaultPrompt`
- `websiteURL`, `privacyPolicyURL`, `termsOfServiceURL`, `logo`, `screenshots`

Cursor's marketplace picker uses top-level `description`, `keywords`, `category`, and `logo` — no
separate `interface` block.

## Known Codex Bugs to Work Around

- **[openai/codex#17066](https://github.com/openai/codex/issues/17066)** — local `source.path`
  cannot be `"./"`. Every plugin must live in a subdirectory of the marketplace root. We comply
  (`./plugins/agent-ready-repo`).
- **[openai/codex#22105](https://github.com/openai/codex/issues/22105)** — `.mcp.json` examples in
  docs use snake_case `mcp_servers`, but the runtime requires camelCase `mcpServers`. Relevant when
  this plugin adds MCP servers; not relevant today.

## Version-Sync Rule

The six manifests must all share the same version:

```
.claude-plugin/marketplace.json
.cursor-plugin/marketplace.json
.agents/plugins/marketplace.json
plugins/agent-ready-repo/.claude-plugin/plugin.json
plugins/agent-ready-repo/.cursor-plugin/plugin.json
plugins/agent-ready-repo/.codex-plugin/plugin.json
```

`bin/agent-ready-check` warns when these drift via `check_manifest_versions`.

## Reference Implementation

[`mike-north/ai-plugin-marketplace-template`](https://github.com/mike-north/ai-plugin-marketplace-template)
is the canonical multi-host marketplace template (Claude, Cursor, Codex, Kiro, Gemini). Read it when
adding a new host wrapper or introducing a second plugin.
