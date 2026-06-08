---
name: evolving-a-spec
description: Runs the change lifecycle when documented behavior changes: write an ADR for the why, edit the living spec to the new current state, bump governing_adrs, and supersede any reversed ADR.
version: 0.1.0
---

# Evolving a Spec

## Overview

The end-to-end change flow that binds an ADR (the why) to a living-spec edit
(the new current state). Use it when both the decision and the documentation
must move together.

## When to use

- Behavior or architecture is changing and both the decision and the current-state doc must move together.

## When NOT to use

- A brand-new spec with no decision to record → `authoring-living-spec`.
- Recording a decision with no spec to edit yet → `writing-adr`.

## Steps

1. Run `writing-adr` to capture the why (`proposed` → `accepted`).
2. Run `authoring-living-spec` to edit the affected spec(s) to the new current state.
3. Add the ADR id to the spec's `governing_adrs`; bump `last_updated`.
4. If reversing an earlier decision, run the supersede flow (new ADR `supersedes`; old ADR → `superseded` + `superseded_by`).
5. Run `pnpm spec:ls` / `pnpm adr:ls` to confirm the new state is listed.

STOP: never edit spec behavior without a governing ADR.

## Quick reference

| Change type | Sub-skills, in order |
|---|---|
| New behavior on an existing capability | `writing-adr` → `authoring-living-spec` (add ADR to `governing_adrs`) |
| Reversal of an accepted decision | `writing-adr` (new, `supersedes`) → flip old ADR → `authoring-living-spec` |
| Deprecation of a capability | `writing-adr` → `authoring-living-spec` (set spec `status: deprecated`, point to replacement) |

## Pointers

- `${CLAUDE_PLUGIN_ROOT}/references/change-lifecycle.md`
- `docs/specs/meta/spec-governance.md`
