---
name: monorepo-agent-context
description: Designs monorepo agent context when root and package-level AGENTS.md, CLAUDE.md, docs, rules, ownership, or workspace boundaries need layering without duplication.
version: 0.2.0
---

# Monorepo Agent Context

Design instruction layers for repositories with multiple packages, teams, apps, services, or
workspaces.

## Core Rule

Make root `AGENTS.md` the first-class shared contract. Package-level instruction files contain only
local deltas. Host-specific files such as `CLAUDE.md` exist to make a host load the right truth;
they are not independent sources of shared policy.

**Every `AGENTS.md` in the repo MUST have a sibling `CLAUDE.md` shim** containing only `@AGENTS.md`
(with optional Claude-Code-specific lines after the import). This is mandatory, not optional: Claude
Code does not auto-load `AGENTS.md` and will not see package-level guidance otherwise. The validator
(`agent-ready-check`) enforces this — a missing shim is a `WARN`, a shim that fails to reference its
sibling `AGENTS.md` is a `WARN`.

Use this skill instead of the generic maintenance flow when package boundaries matter.

## What Anthropic Guidance Means Here

Claude Code guidance says:

- parent `CLAUDE.md` files load when launching from a nested directory;
- child `CLAUDE.md` files load on demand when Claude reads files in those directories;
- large monorepos can use `claudeMdExcludes` to skip irrelevant team instructions.

Apply that as Claude Code wiring around `AGENTS.md`:

- root `CLAUDE.md` should import or point to root `AGENTS.md`;
- package `CLAUDE.md` should import or point to package `AGENTS.md` only when Claude Code needs
  package-local loading;
- `claudeMdExcludes` should prevent unrelated team context from loading, not hide shared root rules.

## Layering Procedure

1. Identify the monorepo root and package/workspace boundaries.
2. Read root `AGENTS.md`, root `CLAUDE.md`, package instruction files, and relevant docs before
   editing.
3. Classify each instruction as shared root truth, package-local delta, host wiring, durable doc,
   procedure, or enforcement.
4. Move shared rules to root `AGENTS.md` or linked root docs.
5. Keep package-level `AGENTS.md` files focused on package commands, ownership, local constraints,
   package docs, and exceptions to root defaults.
6. Keep `CLAUDE.md` files thin: imports, Claude Code loading behavior, Claude-specific rules, and
   `claudeMdExcludes` guidance only.
7. **Create a `CLAUDE.md` shim next to every `AGENTS.md`.** Minimum content is one line:
   `@AGENTS.md`. Add Claude-Code-specific guidance below the import only when it exists; do not
   duplicate `AGENTS.md` content.
8. Move long package knowledge into package docs and link from the nearest instruction file with
   "when to read" intent.
9. Check for duplicate or conflicting rules across root and package files.
10. Run `agent-ready-check --json` and resolve every `CLAUDE.md shim` warning before finishing.

## Placement Guide

Root `AGENTS.md`:

- workspace package manager and install commands;
- repo-wide verification entry points;
- shared safety boundaries and ownership model;
- links to workspace docs and package map;
- rules that apply to all packages.

Package `AGENTS.md`:

- package-specific commands that differ from root;
- local architecture, ownership, and test boundaries;
- package docs with "when to read" links;
- exceptions to root conventions.

Root or package `CLAUDE.md`:

- `@AGENTS.md` imports or direct pointers for Claude Code;
- Claude Code-only memory, hooks, skills, plugins, permissions, or plan-mode guidance;
- `claudeMdExcludes` notes for unrelated package instructions.

Docs:

- architecture, ADRs, specs, plans, runbooks, troubleshooting, and package maps.

## Anti-Patterns

- Copying root rules into every package.
- `@`-importing docs from `AGENTS.md` or `CLAUDE.md` — every `@` import is always-loaded; reference
  docs by plain path instead (the only sanctioned import is the `CLAUDE.md` shim's `@AGENTS.md`).
- Putting package-specific commands in root `AGENTS.md` when only one package uses them.
- Treating `CLAUDE.md` as the canonical cross-agent file.
- Using `claudeMdExcludes` to compensate for duplicated or bloated instructions instead of fixing
  the layers.
- Creating package instruction files for packages with no meaningful local delta.
- Shipping a package `AGENTS.md` without its `CLAUDE.md` shim — Claude Code launched from that
  subdir will not load the brief.
- Duplicating `AGENTS.md` content inside `CLAUDE.md` instead of importing via `@AGENTS.md`.

## Output

Return:

- root instruction changes;
- package-level instruction changes;
- host-specific wiring changes;
- knowledge moved to docs;
- duplicate or conflicting rules removed;
- verification performed.
