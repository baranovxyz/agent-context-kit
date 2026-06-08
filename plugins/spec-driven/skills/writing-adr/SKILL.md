---
name: writing-adr
description: Writes an architecture decision record under docs/adr with context, options, decision, and consequences, four-digit numbering, and the immutability plus supersede rules for accepted ADRs.
version: 0.1.0
---

# Writing ADR

## Overview

An ADR records *why* a decision was made: its context, the options considered,
the choice, and the consequences. Once `status: accepted` its body is immutable.

## When to use

- A material behavior or architecture decision is being made.
- An earlier accepted decision is being reversed.

## When NOT to use

- Describing current state → `authoring-living-spec`.
- A trivial wording fix to a spec (no decision) → no ADR needed.

## Steps

1. Number the ADR `max(existing) + 1`, zero-padded to four digits.
2. Name the file `NNNN-<kebab-title>.md`.
3. Write the frontmatter per `${CLAUDE_PLUGIN_ROOT}/references/spec-and-adr-frontmatter.md`; set `affects_specs` to the `<domain>/<name>` specs this shapes.
4. Write the body sections in order: **Context** → **Decision** → **Options considered** → **Consequences**.

STOP: do not edit an already-accepted ADR's body — write a new one and supersede.

## Supersede flow

- The new ADR sets `supersedes: <old>`.
- Flip the old ADR to `status: superseded` + `superseded_by: <new>` — this is the only permitted edit to an accepted ADR.

## Common mistakes

- Reusing a number — numbers are never reused.
- Editing an accepted ADR's body — supersede instead.
- Omitting the Options considered section.
- Deciding without naming the consequences.

## Pointers

- `${CLAUDE_PLUGIN_ROOT}/references/spec-and-adr-frontmatter.md`
- `${CLAUDE_PLUGIN_ROOT}/references/change-lifecycle.md`
- `docs/specs/meta/spec-governance.md`
