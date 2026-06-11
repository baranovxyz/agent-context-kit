---
name: agent-ready-maintenance
description: Maintains agent-facing docs and automation artifacts after feature work, refactors, monorepo structure changes, repeated agent mistakes, or changes to AGENTS.md, CLAUDE.md, docs, skills, agents, hooks, CLI, MCP, or plugin guidance.
version: 0.1.0
---

# Agent Ready Maintenance

Maintain agent-facing artifacts as a natural side effect of project work.

## When To Run

Run after work that changes:

- commands, skills, scripts, package manager, or verification flow;
- project structure or module ownership;
- monorepo package boundaries or workspace ownership;
- architecture or integration boundaries;
- conventions not enforced by tooling;
- feature requirements, specs, plans, or acceptance criteria;
- repeated procedures;
- agent roles, skills, hooks, CLI, or MCP usage.

## Maintenance Procedure

1. Identify what changed.
2. Decide which layer owns the knowledge.
3. Update only the owning layer.
4. Add or adjust links from `AGENTS.md` only when the knowledge is important to discover.
5. Create an ADR for architecture decisions.
6. Update specs/plans for active feature work.
7. Recommend a skill for repeated procedures.
8. Recommend an agent for autonomous multi-step work.
9. Use `monorepo-agent-context` when root and package-level instruction files both need updates.
10. Recommend hook or CI when a rule must always run.
11. Prefer skills over new `commands/` files; command files are legacy flat skills.
12. Run `agent-ready-check --json` when available.

## Update Rules

`AGENTS.md`:

- keep first-class and short;
- add exact commands and non-obvious always-on boundaries;
- link to docs with "when to read" guidance;
- link by plain relative path — never `@`-import a doc (`@` inlines the whole file into every
  session; the only sanctioned import is the `CLAUDE.md` shim's `@AGENTS.md`);
- remove or move long content.

Monorepos:

- keep root `AGENTS.md` for shared workspace truth;
- keep package-level instruction files to local deltas only;
- route Claude Code loading behavior through `CLAUDE.md` wrappers or `claudeMdExcludes` without
  copying shared rules.

`docs/`:

- store durable memory;
- separate spec from plan;
- keep ADRs append-only;
- prefer one topic per file;
- soft cap each `.md` at ~500 lines — when a file would exceed it,
  propose a split or regroup before writing. Aim for cohesive
  sub-files, not arbitrary line breaks. Ask the user before
  splitting a long-standing file (links and skill references may
  point at section anchors).

When capturing new knowledge into docs:

- capture the **idea**, not the verbatim symbol, error string, file
  path, or line number. Names rot, line numbers move, error
  wording changes between tool versions. The lesson — what bit, why
  it bit, how to recognize it next time — is what survives.
- write so the entry stays useful after the surrounding code is
  refactored. A future reader should learn the shape of the trap,
  not chase a dead reference.
- exception: keep one exact pointer (file path, command, or short
  symbol) per entry as a starting handle for the next agent. Bury
  it at the end, not in the lead.

Skills:

- encode process only;
- keep details in references;
- add scripts only for deterministic repetition;
- set `disable-model-invocation: true` for user-only workflows with side effects.

Agents:

- create only for autonomous work that benefits from isolated context;
- use clear one-line descriptions, body trigger examples, and least-privilege tools.

Tool-specific files:

- store host-specific capabilities;
- link to shared docs instead of copying.

## Output

Return:

- changed project facts;
- affected layers;
- edits made or recommended;
- verification performed;
- follow-up recommendations.
