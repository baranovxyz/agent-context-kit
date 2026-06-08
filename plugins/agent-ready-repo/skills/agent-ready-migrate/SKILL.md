---
name: agent-ready-migrate
description: Applies approved agent-ready repository memory migration plans when the user asks to migrate AGENTS.md content, monorepo instructions, docs, skills, agents, or agent-ready setup.
argument-hint: [approved-plan-file-or-summary]
disable-model-invocation: true
version: 0.1.0
---

# Agent Ready Migrate

Apply an approved agent-ready repository migration. Do not infer approval from the existence of an audit or TODO list.

## Input

Approved plan:

```text
$ARGUMENTS
```

If no plan is provided, stop and ask for the approved migration plan.

## Procedure

1. Use `using-agent-ready-repo`, `agent-ready-maintenance`, `tool-specific-wiring`, and `skill-and-agent-designer` as needed.
2. Read the approved plan and relevant existing files before editing.
3. Apply only approved changes:
   - shrink `AGENTS.md` by moving durable details to `docs/`;
   - update `CLAUDE.md` only as Claude Code loading wiring plus Claude-only additions;
   - split monorepo root and package-level instruction files into shared truth plus local deltas;
   - move Claude path-scoped guidance into `.claude/rules/`;
   - replace duplicated host files with thin pointers;
   - create or update docs, specs, plans, ADRs, rules, runbooks, or troubleshooting docs;
   - create focused skills for repeated procedures;
   - create agents only for autonomous worker roles;
   - update hooks, CLI, or MCP guidance when the approved plan calls for it.
4. Prefer skills over new `commands/` files. Use `disable-model-invocation: true` for user-only workflows with side effects.
5. Preserve intent when moving knowledge. Do not silently delete existing project decisions.
6. Run `agent-ready-check` when available. Use `agent-ready-check --json` when the plugin is installed and available on `PATH`; otherwise run `python3 ${CLAUDE_PLUGIN_ROOT}/bin/agent-ready-check --json`.

## Output

Return:

- files changed;
- knowledge moved between layers;
- validation output;
- remaining risks or questions.
