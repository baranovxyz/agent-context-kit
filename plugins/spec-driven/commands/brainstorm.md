---
description: Brainstorm a rough idea into an approved design (strict one-question-at-a-time, explicit tradeoffs, optional web research), then hand off to spec-driven for ADR + spec.
argument-hint: "<idea or feature> [web|no-web]"
---

Invoke the `brainstorming` skill to turn the following idea into an approved
design, then hand the approved design to `using-spec-driven`:

$ARGUMENTS

Web-research preset (off by default):

- If the arguments end with `web`, enable web research and skip the consent offer.
- If they end with `no-web`, disable it and skip the consent offer.
- Otherwise, make the one-time web-research offer as the skill describes.

Follow the skill exactly: explore context first, ask strictly one question at a
time, present 2-3 approaches with explicit tradeoffs, get approval section by
section, and do not write code or invoke an implementation skill before the
design is approved.
