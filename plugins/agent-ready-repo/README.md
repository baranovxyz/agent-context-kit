# Agent Ready Repo

Agent Ready Repo is a Claude Code plugin for maintaining the repository memory layer that coding agents rely on. Its packaged components run in Claude Code, while its layering model is intentionally portable to Cursor, Codex, OpenCode, and other coding-agent hosts.

It uses a five-layer model:

1. `AGENTS.md` is the first-class portable instruction contract.
2. `docs/` is durable memory for architecture, specs, plans, ADRs, rules, runbooks, troubleshooting, and codebase maps.
3. Tool-specific files such as `CLAUDE.md` contain host-specific loading or capability wiring, not duplicated shared truth.
4. Skills encode repeatable procedures.
5. CLI, MCP, hooks, and CI expose executable contracts and enforcement.

## Component Model

This plugin follows the BMAD-style separation:

- **Agents are workers.** They audit, write, migrate, and design artifacts.
- **Skills are procedures.** They decide how to audit, maintain, design, or wire project memory.
- **Docs are artifacts.** They hold project knowledge and are read on demand.
- **Commands are legacy flat skills.** New user-invoked workflows live in `skills/` with invocation controls.
- **Hooks are nudges.** They surface likely drift without editing files automatically.

## Included Skills

- `using-agent-ready-repo` - checks which plugin skill applies before touching repository memory.
- `agent-ready-audit` - audits `AGENTS.md`, docs, tool-specific files, skills, agents, hooks, CLI, and MCP surfaces.
- `agent-ready-migrate` - applies an approved migration plan; user-invoked only.
- `agent-ready-maintenance` - updates agent-facing artifacts after code, command, structure, or process changes.
- `monorepo-agent-context` - designs root and package-level agent context without duplicating shared rules.
- `skill-and-agent-designer` - decides whether repeated work needs a skill, agent, command, hook, CLI, MCP, doc, or no new artifact.
- `tool-specific-wiring` - keeps shared truth out of host-specific files.
- `wrap-up-session` - closes out a session: audits findings, routes them via `agent-ready-maintenance`, writes a continuation prompt, branches, commits, opens a PR, merges.
- `resume-from-continuation` - starts a session by reading the most recent continuation prompt, verifying it against current repo state, and confirming the next action with the user.

## Included Agents

- `agent-ready-auditor` - read-only drift and layer audit.
- `docs-maintainer` - writes and updates `AGENTS.md` and `docs/`.
- `skill-architect` - creates and improves focused skills.
- `agent-architect` - creates subagents with clear triggers and least-privilege tools.

## User-Invoked Entry Points

Claude Code now treats command files as legacy flat skills. This plugin keeps entry points in `skills/`:

- `/agent-ready-repo:agent-ready-audit` - run a read-only agent evaluation and produce a migration plan.
- `/agent-ready-repo:agent-ready-migrate` - apply an approved migration plan. This skill uses `disable-model-invocation: true` so Claude does not apply migrations just because an audit exists.

## Agent Evaluation

The real product is the `agent-ready-auditor` agent. It evaluates whether repository memory helps future agents work correctly:

- whether `AGENTS.md` is a useful always-on contract;
- whether durable knowledge is discoverable in `docs/`;
- whether monorepo package instructions are local deltas rather than duplicated root truth;
- whether tool-specific files contain only host-specific wiring;
- whether skills are focused, discoverable, governed, and safe;
- whether agents have clear worker roles;
- whether hooks, CLI, MCP, and CI are used where text instructions are not enough.

The audit result should be a judgment with evidence, not a checklist score.

## Preflight Checker

Run the checker from a project root:

```bash
agent-ready-check
```

For machine-readable output:

```bash
agent-ready-check --json
```

For local testing before the plugin is installed, call it directly:

```bash
python3 plugins/agent-ready-repo/bin/agent-ready-check
```

It checks common mechanical issues: long `AGENTS.md`, missing `CLAUDE.md` shortcut, unresolved placeholders, weak descriptions, incompatible description frontmatter, and broken references in `AGENTS.md`.

Exit code `0` means no common issues were found. Exit code `1` means the checker found warnings to inspect. JSON output has `ok`, `issue_count`, and `issues`.

The checker is not the evaluation. Use it as preflight evidence for the agent audit.

## When The Plugin Edits Files

The plugin should edit files only when the user asks to apply an audit or when an active task clearly changed documented project truth.

Examples:

- A command changed: update `AGENTS.md` commands or a runbook.
- A new architecture decision was made: add an ADR.
- A repeated checklist emerged: propose a skill.
- A new autonomous role is needed: propose an agent.
- A rule must always run: propose hook or CI, not another markdown reminder.

## When It Only Recommends

The plugin should recommend instead of editing when:

- the right layer is ambiguous;
- the change affects team policy;
- a hook, MCP server, CLI, or security boundary is involved;
- deleting or moving existing knowledge could lose intent;
- a new skill or agent would broaden scope beyond the current task.

## Core Rule

Agents are workers. Skills are procedures. Docs are artifacts. `AGENTS.md` is the first-class portable instruction contract.

Skill and agent descriptions are one-line plain-text metadata that states what the artifact does and when to use it. Do not use `when_to_use`, examples, tags, Markdown, code fences, lists, transcripts, or multiline YAML scalars in frontmatter; keep longer trigger guidance in the Markdown body.

Enterprise skill guidance also applies: review every skill as a dependency, evaluate trigger accuracy before deployment, monitor drift, and deprecate skills that keep failing.

Plugin docs guidance also applies: keep default component directories unless there is a concrete reason to replace them. Do not add plugin dependencies, MCP servers, LSP servers, monitors, channels, or user configuration without a runtime need. Marketplace metadata belongs in the distribution repository's root `.claude-plugin/marketplace.json`, not inside the plugin package.

Claude memory guidance applies as host wiring: Claude Code loads `CLAUDE.md`, so `CLAUDE.md` should import or point to `AGENTS.md` plus Claude Code-only additions. Other coding-agent hosts should read `AGENTS.md` or thin host wrappers around the same truth. For monorepos, root `AGENTS.md` owns shared rules and package-level instruction files contain only local deltas.

## References

- `references/layered-architecture.md`
- `references/artifact-decision-matrix.md`
- `references/research-notes.md`
- `references/plugin-architecture-notes.md`
- `references/anthropic-plugin-docs-implications.md`
- `references/anthropic-skill-authoring-best-practices.md`
- `references/anthropic-skills-for-enterprise.md`

## Local Testing

1. Install or load the plugin from `plugins/agent-ready-repo`.
2. Confirm the skills appear under the `agent-ready-repo` namespace.
3. Run `/agent-ready-repo:agent-ready-audit` in a test repository and verify the agent returns qualitative findings.
4. Run `agent-ready-check --json` from a project root after installation, or `python3 ${CLAUDE_PLUGIN_ROOT}/bin/agent-ready-check --json` during local testing.
5. Inspect loaded hooks with the host hook UI or debug mode. The Stop hook should only block when documentation maintenance was explicitly requested and skipped.
