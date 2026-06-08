---
name: agent-ready-audit
description: Evaluates agent-facing repository memory when auditing AGENTS.md, CLAUDE.md, monorepo context, docs, skills, agents, hooks, CLI, MCP, plugin setup, or migration needs, and produces evidence-backed plans without editing.
version: 0.1.0
---

# Agent Ready Audit

Evaluate repository memory and produce a migration plan. Do not edit files until the user approves an apply step.

The evaluation is agent judgment with evidence. Do not reduce it to guardrails, checkboxes, or line-count rules.

## Scope

Inspect relevant artifacts when present:

- `AGENTS.md`;
- `CLAUDE.md`;
- package-level or workspace-level instruction files in monorepos;
- `.cursor/rules/`;
- `.claude/rules/`;
- `.github/copilot-instructions.md`;
- `.github/instructions/`;
- `GEMINI.md`;
- `docs/`;
- `.claude/skills/`, `.agents/skills/`, plugin `skills/`;
- `.claude/agents/`, plugin `agents/`;
- hooks, CI, MCP, CLI configuration;
- plugin manifests, dependencies, marketplace entries, `bin/`, monitors, channels, LSP, and settings when present.

## Classification

Classify each notable instruction or artifact as:

- always-on;
- docs;
- spec;
- plan;
- tool-specific;
- procedure;
- executable contract;
- enforcement;
- delete.

Use `${CLAUDE_PLUGIN_ROOT}/references/artifact-decision-matrix.md` for placement rules.

## Evaluation Procedure

1. Read the top-level instruction files first.
2. Judge whether `AGENTS.md` gives future agents the right portable always-on context without becoming a manual.
3. Judge whether `docs/` makes durable knowledge discoverable at the moment an agent needs it.
4. Judge whether monorepo package-level instructions are local deltas rather than duplicated root truth.
5. Judge whether tool-specific files add host capabilities without duplicating shared truth.
6. Judge whether skills are focused, discoverable, safe, evaluated, and governed.
7. Judge whether agents are real worker roles with clear boundaries and enough context isolation.
8. Judge whether command files are legacy flat skills that should move into `skills/`.
9. Judge whether hooks/CI enforce rules that text cannot reliably enforce and return structured hook output where required.
10. Judge whether CLI/MCP surfaces match the job-to-be-done and trust boundary.
11. Judge whether `CLAUDE.md` exists only as Claude Code wiring that imports or points to `AGENTS.md` plus Claude-specific deltas.
12. Use `agent-ready-check` only as preflight evidence, not as the evaluation result.
13. Produce findings before suggesting rewrites.

## Finding Categories

Use severity:

- **High:** misleading instructions, duplicated conflicting truth, unsafe tool access, lost requirements, broken verification.
- **Medium:** bloated `AGENTS.md`, duplicated monorepo package instructions, dead docs, vague skills, missing ADR/spec/plan, poor host wiring.
- **Low:** naming, organization, missing examples, style drift.

## Output

Return:

- summary of repository memory health;
- findings by severity;
- evidence from files;
- instruction classification table;
- recommended moves;
- proposed files to create or update;
- confidence and residual risks;
- explicit "apply plan?" question.

Do not silently delete knowledge. Move it to a better layer or ask.
