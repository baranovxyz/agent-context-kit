---
name: brainstorming
description: Turns a rough idea into an approved design through strict one-question-at-a-time dialogue with explicit tradeoffs and optional web research, then hands it to using-spec-driven for ADR and spec authoring.
version: 0.2.0
---

# Brainstorming Ideas Into Designs

## Overview

Turn an idea into an approved design through collaborative dialogue, then hand
off to spec authoring. This is the *ideation on-ramp* to spec-driven: it
produces the design that `using-spec-driven` turns into an ADR (the why) and a
living spec (the current-state what). It does not write code, plans, specs, or
ADRs itself — its single output is an approved design.

## When to use

- A new feature, capability, or behavior change is being designed.
- A request is vague, broad, or has unstated constraints worth teasing out.
- You are about to implement something non-trivial with no agreed design.

## When NOT to use

- The change is a spec/ADR edit with the design already settled → `using-spec-driven`.
- A pure factual or how-does-this-work question → just answer it.
- Deep multi-source factual research is the goal → the `deep-research` skill.

## The gate (soft but firm)

Present a design and get the user's approval before writing code, scaffolding,
or invoking an implementation skill. Scale the design to complexity — a few
sentences for a small change, more for a nuanced one. A genuinely trivial
change gets a one-line design and a quick confirm, not a ceremony. The point is
a shared, approved design before build — not bureaucracy.

## Optional: web research (off by default)

Offer web research **once, in its own message**, before asking questions:

> "Want me to scan the web for prior art and how others solve this as we go?
> Optional — adds a little latency, and grounds the tradeoffs in real examples."

If accepted, fold cited prior art into the approaches. If declined, brainstorm from your own
knowledge. If the host has no web tool, say so once and continue without it. Full procedure (when to
search per round, citation format, availability guard):
`${CLAUDE_PLUGIN_ROOT}/skills/brainstorming/references/web-research-and-tradeoffs.md`.

## Process

Work these in order:

1. **Explore project context** — files, docs, recent commits. Skip questions the context already
   answers.
2. **Offer web research** — the consent message above, on its own. Wait for the answer.
3. **Ask clarifying questions — strictly one per message.** Exactly one question per turn; never
   bundle. Multiple-choice when it lowers the user's effort; open-ended when it does not. Invite the
   user to dump as much context as they like. Keep going until you genuinely understand purpose,
   constraints, and success criteria — do not stop early because it "seems simple."
4. **Propose 2-3 approaches with explicit tradeoffs** — each with pros/cons and your recommendation
   (and cited prior art if web research is on). One round per open design axis; iterate as new axes
   surface.
5. **Present the design in sections** scaled to complexity; get approval after each section. Cover
   the parts that matter: shape, components, data flow, failure modes, how it's verified.
6. **Hand off** — on full approval, invoke `using-spec-driven` to route the design into an ADR (the
   decision) and a living spec (the current state). That router is the only skill this one hands to.

## Key principles

- **One question at a time** — never bundle questions into one message.
- **Tradeoffs always explicit** — every approaches round shows 2-3 options with pros/cons and a
  recommendation, never a single take.
- **YAGNI** — cut features that don't serve the stated goal.
- **Approval-gated** — present, get sign-off, then move on; don't build ahead of the design.
- **Terminal is `using-spec-driven`** — never invoke an implementation skill from here.

## Pointers

- `${CLAUDE_PLUGIN_ROOT}/skills/brainstorming/references/web-research-and-tradeoffs.md` —
  web-research procedure + how to present tradeoffs.
- `${CLAUDE_PLUGIN_ROOT}/skills/using-spec-driven/SKILL.md` — the handoff target (routes to ADR +
  spec).
