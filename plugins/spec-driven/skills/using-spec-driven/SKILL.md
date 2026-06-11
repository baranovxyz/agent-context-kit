---
name: using-spec-driven
description: Routes spec and ADR authoring through the living-spec plus ADR lifecycle when creating or changing a spec, recording an architecture decision, or updating the documented source of truth under docs/specs or docs/adr.
version: 0.1.0
---

# Using Spec Driven

## Overview

This is the routing gate for spec and ADR authoring — invoked **once a change
is already known to be a spec/ADR matter**. It does not decide *whether*
something is a spec or an ADR; that classification (where any piece of knowledge
belongs across all artifact types) stays with `agent-ready-repo`'s
`using-agent-ready-repo` and its `artifact-decision-matrix`. This skill picks
the right authoring skill and enforces the lifecycle order.

## When to use

- Writing or editing a living spec under `docs/specs/`.
- Recording an architecture decision under `docs/adr/`.
- Changing the documented source of truth for how the system works.
- Superseding an accepted decision.

## When NOT to use

- Deciding where a piece of knowledge belongs across all artifact types (AGENTS.md, rule, skill,
  spec, ADR) → `using-agent-ready-repo`.
- Writing an implementation plan → `docs/plans/`.
- A work-in-progress handoff → a continuation prompt.

## Routing procedure

1. New or changed behavior/architecture → `evolving-a-spec`.
2. A fresh spec with no decision to record → `authoring-living-spec`.
3. Just recording a decision → `writing-adr`.
4. Reversing an accepted decision → `writing-adr` (new ADR) then `evolving-a-spec` (flip the old ADR
   + edit the spec).

## Lifecycle invariant

- The decision (ADR) precedes the documented current-state (spec).
- Never edit a spec's behavior without a governing ADR.
- Never edit an accepted ADR's body — supersede instead.

## Pointers

- `${CLAUDE_PLUGIN_ROOT}/references/spec-and-adr-frontmatter.md`
- `${CLAUDE_PLUGIN_ROOT}/references/change-lifecycle.md`
- `docs/specs/meta/spec-governance.md`
