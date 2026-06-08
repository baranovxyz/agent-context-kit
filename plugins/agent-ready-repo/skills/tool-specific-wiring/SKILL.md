---
name: tool-specific-wiring
description: Aligns host-specific instruction files and capability configs when working with CLAUDE.md, Cursor rules, Copilot instructions, GEMINI.md, hooks, MCP configs, LSP configs, plugin manifests, or marketplace entries.
version: 0.1.0
---

# Tool Specific Wiring

Keep host-specific files thin and purposeful.

## Core Rule

Shared project truth belongs in first-class `AGENTS.md` or `docs/`. Tool-specific files contain only host-specific loading, capability configuration, and routing.

## Common Placements

`CLAUDE.md`:

- import or point to `AGENTS.md` because Claude Code reads `CLAUDE.md`, not `AGENTS.md`;
- add only Claude Code memory, plugin, hook, skill, policy, or monorepo loading guidance;
- do not copy shared rules.

`.claude/rules/`:

- store Claude Code path-scoped guidance;
- use frontmatter paths when guidance should load only for matching files;
- do not use rules for repeatable procedures that belong in skills.

`.cursor/rules/`:

- define globs, rule mode, and Cursor-specific behavior;
- link to `docs/rules/` for portable policy;
- avoid duplicating `AGENTS.md`.

`.github/instructions/`:

- define Copilot-specific review and path behavior;
- link to shared docs for durable rules.

`GEMINI.md`:

- provide Gemini-specific wrapper or extension;
- link to `AGENTS.md` for shared facts.

Hooks and CI:

- enforce rules that must always run;
- keep hooks deterministic, fast, and safe;
- avoid hidden file edits;
- make prompt hooks return strict JSON in the documented schema.

MCP configs:

- expose governed live systems;
- document setup and usage;
- include skills for when and how to use tools.

Plugin manifests:

- rely on default component paths unless custom paths are intentional;
- add `dependencies` only for runtime plugin dependencies;
- add marketplace metadata only when distributing through a marketplace;
- keep `bin/` tools non-interactive and provide `--json` when agents may call them.

## Wiring Procedure

1. Identify the host and its unique capability.
2. Move portable content to `AGENTS.md` or `docs/`.
3. Keep only host-specific routing or behavior in the host file.
4. Add links with "when to read" intent.
5. Verify referenced files exist.
6. For Claude Code monorepos, use parent/child `CLAUDE.md` loading and `claudeMdExcludes` as wiring around `AGENTS.md`, not as a second source of truth.
7. Run `agent-ready-check` when available.

## Output

Return:

- host-specific files touched;
- shared truth moved or linked;
- duplicated content removed;
- remaining host-specific behavior;
- verification results.
