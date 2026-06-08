---
name: authoring-living-spec
description: Creates or edits a living spec under docs/specs with current-state-only content, the domain/status/governing_adrs frontmatter, one capability per file, and a verification section.
version: 0.1.0
---

# Authoring Living Spec

## Overview

A living spec is the current-state source of truth for one capability, edited in
place forever. It describes *what* the capability does today and how to verify
it — never *why* (that is an ADR's job).

## When to use

- A capability needs a current-state spec.
- An existing spec must be updated to reflect new behavior.

## When NOT to use

- Recording *why* a decision was made → `writing-adr`.
- Writing an implementation plan or a work-in-progress handoff.

## Steps

1. Pick the path `docs/specs/<domain>/<capability>.md`; create the domain folder if no existing domain fits.
2. Write the frontmatter per `${CLAUDE_PLUGIN_ROOT}/references/spec-and-adr-frontmatter.md` (`name`, `domain`, `status`, `governing_adrs`, `last_updated`).
3. Write the body: current-state WHAT plus a how-to-verify section. One capability per file.

STOP: if you are writing past tense or rationale ("we used to…", "we chose…"),
stop — that belongs in an ADR, not the spec.

## Common mistakes

- A changelog inside the spec — history lives in git + ADRs.
- Multiple capabilities crammed into one file — one capability per file.
- Missing `governing_adrs` — link the decisions that shaped the current state.
- Rationale prose where current-state belongs — move the why to an ADR.

## Pointers

- `${CLAUDE_PLUGIN_ROOT}/references/spec-and-adr-frontmatter.md`
- `${CLAUDE_PLUGIN_ROOT}/references/change-lifecycle.md`
- `docs/specs/meta/spec-governance.md`
