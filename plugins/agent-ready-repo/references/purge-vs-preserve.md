# Purge vs preserve

When a fact in agent-read context stops being true, deciding whether to **keep it as history** or
**delete it outright** is a context-engineering decision, not a code-style one. Agents read the
current context window; they do not read git history. The Clean-Code instinct — "delete it, the
diff holds the why" — does not transfer, and it misfires in both directions.

Classify the knowledge first, then apply the matching rule.

## Two kinds of knowledge, opposite treatment

**Durable knowledge — preserve (move, don't delete).**
The *why*: decisions, rejected alternatives, lessons, root causes, dated events. It survives the
code and topology it describes. Move it to the layer that keeps it discoverable — `docs/`, an ADR,
a spec, a history/archive dir — never leave it only in a commit message. This is the existing
"move, do not silently delete" rule in `artifact-decision-matrix.md`.

**Stale current-state assertions — purge (delete from live context).**
A present-tense claim about how things *are right now*: a live host, the current topology, "X runs
on Y", "service A is the deploy origin", "monitor host Z". When it stops being true, delete it from
**every** source of truth an agent reads. Specifically:

- **Do not rewrite it as "X used to run on Y."** A stale positive turned past-tense is still
  context poison — an agent may still act on it, and at best it burns attention and tokens on a
  dead fact.
- **Do not scatter the tombstone.** Repeating "X was retired / decommissioned" across many files is
  context confusion and rot; the signal-to-noise of the live context drops with every copy.
- **Keep at most one negative guardrail**, only in the durable memory layer (a single memory
  entry), and only when there is a real risk an agent re-adds the stale fact. One guardrail, one
  place — not a sprinkling.

## Why agents are not humans here

A human reads code with `git blame` and `git log` within reach; for them the diff genuinely *is* a
memory store. An agent reads only what is loaded into its context — the current docs, the current
`AGENTS.md`, the current spec. So:

- for durable *why*, "the diff holds it" fails — the agent never looks there, so the knowledge must
  be **moved into a doc**;
- for stale *current-state*, "leave it for history" fails — it stays in the live context the agent
  *does* read, so it **poisons** that context and must be **removed**.

Both halves follow from one fact: agents act on present context, not on history.

## Recognizing a stale live-positive

Flag for purge when a fact is **a present-tense assertion of current state that is no longer true**:
a host that is up, a service that is the deploy target, a topology that is "how it works." Leave
alone facts already framed as history: a dated event ("on 2026-05-24 we migrated…"), an ADR, a
changelog entry — those are durable *why*, so preserve them.

The test: *would an agent act on this as if it were true today?* If yes and it is not, purge.

## Sources

- Anthropic — Effective context engineering for AI agents
- Breunig — How Contexts Fail (poisoning, distraction, confusion, clash) / How to Fix Your Context
- Chroma — Context Rot
