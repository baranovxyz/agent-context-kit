# Change lifecycle

How documented behavior changes: a decision (ADR) precedes the documented
current-state (spec). The spec's git diff is the behavioral delta; the ADR is
the durable rationale.

## The four steps

1. **Write an ADR** (`status: proposed`) capturing the why, the options, and the decision.
2. **Accept it** (`status: accepted`) once the decision is settled.
3. **Edit the affected living spec(s)** to the new current state. Add the ADR id to `governing_adrs`; bump `last_updated`.
4. **Reversal (when overturning an earlier decision):** the new ADR sets `supersedes: <old>`; flip the old ADR to `status: superseded` + `superseded_by: <new>`.

## Immutability rule

Once an ADR is `status: accepted`, its Context / Decision / Options considered /
Consequences are **frozen**. The only permitted later edit to an accepted ADR is
flipping `status` to `superseded` and setting `superseded_by`. To change the
substance of a decision, write a new ADR and supersede — never rewrite an
accepted body.

## Numbering rule

Number a new ADR `max(existing) + 1`, zero-padded to four digits
(`0001`, `0002`, …). Numbers are never reused, even for abandoned or superseded
ADRs.

## No changelog inside specs

A living spec describes current state only. No "we used to…", no past tense
about decisions, no changelog section. History lives in git (the diff) and in
the ADRs (the why). If you catch yourself writing history into a spec, it
belongs in an ADR.

## Trivial-edit carve-out

Wording fixes, typo corrections, and clarifications to a spec need **no ADR**.
An ADR is required only when the change alters *what the system does* or *how it
is structured*.

These mirror `docs/specs/meta/spec-governance.md`; if they drift, the repo spec wins.
