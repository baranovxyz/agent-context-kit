---
name: skill-and-agent-designer
description: Designs focused skills and agents when repeated tasks, checklists, prompts, project procedures, user-invoked workflows, specialized review roles, subagents, or skill ideas need the smallest automation artifact.
version: 0.1.0
---

# Skill And Agent Designer

Design the smallest useful automation artifact.

## Decision Procedure

1. Describe the job, not the tool.
2. Check whether the need is durable knowledge, repeatable procedure, autonomous work, explicit entry point, enforced rule, local executable action, or governed external access.
3. Choose one artifact:
   - doc for durable knowledge;
   - skill for repeatable procedure;
   - agent for autonomous worker role;
   - skill with `disable-model-invocation: true` for explicit user-invoked entry point;
   - hook or CI for enforcement;
   - CLI plus skill for known local jobs;
   - MCP for governed live systems;
   - nothing when existing artifacts already cover the job.
4. Avoid broad, generic skills and agents.
5. Add examples and negative triggers in the body, never in frontmatter.

## Skill Design Rules

Create a skill when the process repeats and can be followed by many agents.

Use `${CLAUDE_PLUGIN_ROOT}/references/anthropic-skill-authoring-best-practices.md` for authoring guidance and `${CLAUDE_PLUGIN_ROOT}/references/anthropic-skills-for-enterprise.md` for governance, security review, evaluation, deployment, and lifecycle guidance.

Require:

- one concern;
- single-line third-person `description` that states what the skill does and when to use it;
- concrete trigger phrases and contexts;
- imperative body;
- references for detail;
- examples for complex usage;
- scripts only for deterministic repeated work.
- evaluation examples covering should-trigger, should-not-trigger, and ambiguous cases.
- `disable-model-invocation: true` for workflows with side effects or user-controlled timing.

Reject:

- project encyclopedias;
- vague triggers;
- live data in skill body;
- unsafe scripts;
- duplicated docs.
- unreviewed third-party skills or scripts.

Governance checks:

- assess risk tier for scripts, network access, MCP references, credentials, and broad file access;
- verify scripts in a sandbox before deployment;
- test trigger accuracy and coexistence with existing skills;
- document owner, version, and deprecation criteria for team-shared skills.

## Agent Design Rules

Create an agent when a role needs isolated context or multi-step autonomous work.

Require:

- lowercase kebab-case name;
- single-line plain-text `description` with capability and trigger context;
- trigger examples only in the Markdown body;
- clear responsibilities;
- explicit process;
- output format;
- least-privilege tools;
- newer frontmatter such as `maxTurns`, `effort`, `skills`, `memory`, `background`, or `isolation` only when it has a concrete benefit.

Do not create an agent for a single checklist that a skill can handle.

For plugin-shipped agents, do not use `hooks`, `mcpServers`, or `permissionMode`; Claude Code ignores those fields for plugin agents.

## Description Compatibility Rules

Use only one-line plain-text `description` frontmatter for skills and agents. Do not use `when_to_use`, YAML block scalars, examples, tags, Markdown, code fences, lists, or conversation transcripts in frontmatter. Put longer trigger guidance in the Markdown body.

## Output

Return:

- artifact recommendation;
- rationale;
- file path to create or update;
- trigger text;
- scope boundaries;
- validation steps.

If creating files, validate frontmatter and references after writing.
