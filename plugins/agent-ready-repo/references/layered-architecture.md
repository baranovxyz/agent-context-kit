# Layered Architecture

Use this reference when deciding where repository knowledge belongs.

## Layer 1: Always-On Contract

`AGENTS.md` is the first-class portable instruction file for coding agents. Claude Code reads `CLAUDE.md`, so use `CLAUDE.md` as host-specific wiring that imports or points to `AGENTS.md`.

Keep:

- exact install, test, lint, typecheck, and build commands;
- package manager and non-obvious version constraints;
- safety boundaries;
- 2-5 conventions that are expensive to infer;
- semantic links into `docs/` with "when to read" guidance.

Avoid:

- PRDs;
- long architecture;
- runbooks;
- API reference;
- workflow checklists;
- linter-enforced style;
- generated `/init` boilerplate.

Target 50-150 lines. Audit above 200 lines.

In monorepos, root `AGENTS.md` owns shared workspace truth. Package-level instruction files should contain local deltas only: package commands, ownership, package-specific constraints, and links to package docs. Do not copy root rules into every package.

## Layer 2: Durable Docs

`docs/` is durable memory:

- `docs/architecture.md`;
- `docs/specs/`;
- `docs/plans/`;
- `docs/adr/`;
- `docs/rules/`;
- `docs/runbooks/`;
- `docs/troubleshooting.md`;
- `docs/codebase-map.md`.

Specs and plans are active docs. Specs define what must become true. Plans define how to change files and verify results.

## Layer 3: Tool-Specific Wiring

Host files contain host-specific capabilities:

- `CLAUDE.md`: import or point to `AGENTS.md`, plus Claude Code memory, hooks, skills, plugins, policy, or monorepo loading settings.
- `.claude/rules`: Claude Code path-scoped guidance that loads only when relevant files enter context.
- `.cursor/rules`: globs, rule mode, Cursor-specific routing.
- `.github/instructions`: Copilot-specific review and path rules.
- `GEMINI.md`: Gemini-specific wrapper or extension.

Shared truth belongs in `AGENTS.md` or `docs/`, not copied into every host file.

For Claude Code monorepos, parent and child `CLAUDE.md` files are loading mechanics. Use them to expose root and package-level `AGENTS.md` truth to Claude Code, and use `claudeMdExcludes` to avoid unrelated team instructions.

## Layer 4: Skills

Skills are procedures. A skill says how to perform a class of task.

Good skills:

- have one concern;
- use a strong one-line plain-text `description` with capability and trigger context;
- keep `SKILL.md` lean;
- move details into `references/`;
- include scripts only for deterministic repeated work;
- are reviewed like code.
- use `disable-model-invocation: true` for user-only workflows with side effects.
- keep trigger examples and longer guidance in the Markdown body, not frontmatter.

Bad skills:

- are project encyclopedias;
- have vague trigger descriptions;
- use `when_to_use`, multiline descriptions, examples, tags, Markdown, code fences, lists, or transcripts in frontmatter;
- include live data as if it were stable;
- ship unsafe scripts;
- duplicate docs.

## Layer 5: Executable Contracts

Use CLI plus skill for known local jobs:

- same interface for humans, agents, and CI;
- structured `--json`;
- semantic exit codes;
- no prompts in non-TTY;
- idempotency and `--dry-run`;
- receipts after mutations.

Plugin `bin/` executables are available on `PATH` while the plugin is enabled. Prefer a stable command name, `--json`, and non-interactive behavior for tools agents may call.

Use MCP for governed live systems:

- OAuth or scoped credentials;
- tenant isolation;
- audit trail;
- dynamic discovery;
- multiple clients without shell access.

Use hooks or CI when a rule must always run.
