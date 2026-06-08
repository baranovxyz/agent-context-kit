# Web research and presenting tradeoffs

Depth for the `brainstorming` skill. Loaded on demand — keep `SKILL.md` lean.

## Web research (optional, off by default)

### Consent

Offer once, in its own message, before clarifying questions begin:

> "Want me to scan the web for prior art and how others solve this as we go?
> Optional — adds a little latency, and grounds the tradeoffs in real examples."

Wait for the answer. Decline → text-only from your own knowledge. Accept → it
is *available*, not mandatory per round (next section).

A command may preset this: `web` enables it, `no-web` disables it and skips the
offer.

### Availability guard

If the current host exposes no web-search tool (e.g. Codex, an offline worker
CLI), say so once — "No web tool here, so I'll brainstorm from what I know" —
and continue. Never fail or stall because research is unavailable.

### When to search (per round, only if enabled)

Search when a round genuinely benefits from outside evidence:

- Comparing approaches where prior art exists (libraries, patterns, peer tools).
- A claim about "how X is usually done" you'd otherwise assert unverified.

Skip search for conceptual or project-internal questions (naming, scope,
which-of-these-two-for-our-case). One focused search per round — not a deep
multi-source fan-out. If you need exhaustive, fact-checked research, that's the
separate `deep-research` skill, not this.

### Citing

When research shaped an option, name the source inline so the user can judge it
— e.g. "GitHub Spec Kit uses explicit `/specify → /plan` phases ([spec-kit])".
Keep it to the one or two sources that actually moved the decision.

## Presenting tradeoffs

Every approaches round shows **2-3 options**, never a single take:

- One short paragraph or row per option: what it is, its main **pro**, its main **con**.
- End with **your recommendation and why** — lead with it.
- Ground claims in cited prior art when web research is on.
- Where the host supports it, an `AskUserQuestion` option-list is a good way to
  present the choice (one option per approach, recommendation first).

Example shape:

> **A — <name>** Pro: … Con: …
> **B — <name>** Pro: … Con: …
> **Recommendation: B**, because … .

Re-run a round whenever a new design axis surfaces; resolve one axis at a time.
