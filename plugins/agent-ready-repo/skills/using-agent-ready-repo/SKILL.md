---
name: using-agent-ready-repo
description: Routes repository-memory work through the layered agent-ready model when working with AGENTS.md, CLAUDE.md, monorepos, docs, skills, agents, hooks, CLI/MCP decisions, tool-specific files, plugin manifests, or agent-ready migrations.
version: 0.1.0
---

# Using Agent Ready Repo

Use this skill as the routing gate for repository-memory work.

## Core Model

Apply the layered model before editing:

1. `AGENTS.md` is the first-class portable instruction contract.
2. `docs/` is durable memory.
3. Tool-specific files such as `CLAUDE.md` contain host-specific loading or capability wiring.
4. Skills encode repeatable procedures.
5. CLI, MCP, hooks, and CI expose executable contracts or enforcement.
6. Agents are autonomous workers for complex multi-step work.
7. Plugin commands are legacy flat skills; prefer `skills/*/SKILL.md` for new workflows.

Consult `${CLAUDE_PLUGIN_ROOT}/references/layered-architecture.md` for details.

## Routing Procedure

1. Identify the user's actual intent.
2. Classify the artifact using `${CLAUDE_PLUGIN_ROOT}/references/artifact-decision-matrix.md`.
3. Choose the smallest applicable plugin skill:
   - use `agent-ready-audit` for repo-wide inspection or migration planning;
   - use `agent-ready-migrate` only for an explicitly approved migration plan;
   - use `agent-ready-maintenance` after project changes;
   - use `monorepo-agent-context` for workspace/package-level instruction layering;
   - use `skill-and-agent-designer` for repeated procedures or worker roles;
   - use `tool-specific-wiring` for Claude, Cursor, Copilot, Gemini, hooks, MCP, or host files;
   - use `wrap-up-session` to close out a session (audit, route findings, write continuation prompt,
     commit, PR, merge);
   - use `resume-from-continuation` to start a session from a previous continuation prompt.
4. Do not add content to `AGENTS.md` by default.
5. Prefer moving knowledge to the right layer over duplicating it.

## Red Flags

Stop and classify before editing when seeing:

- a growing `AGENTS.md`;
- copied rules across `CLAUDE.md`, `.cursor/rules`, and `.github/instructions`;
- duplicated root and package-level instruction files in a monorepo;
- requirements living only in chat;
- a repeated checklist;
- a new role that would benefit from isolated context;
- a rule that must always run;
- an MCP or CLI decision framed as protocol preference instead of job-to-be-done.

## Output

For small tasks, state the chosen layer and proceed.

For larger tasks, produce:

- selected skill or agent;
- affected artifacts;
- proposed changes;
- required verification.
