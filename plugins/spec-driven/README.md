# Spec Driven

Spec Driven is a coding-agent plugin for the authoring and evolution workflow behind living specs and ADRs. It keeps `docs/specs/` the current-state source of truth and `docs/adr/` the immutable, numbered decision log, and it teaches agents to run the change lifecycle (ADR then spec edit) whenever documented behavior changes.

Two artifact types with different lifecycles:

- **Living spec** describes *what* a capability does today and how to verify it — one capability per file, grouped by domain, edited in place forever, no changelog.
- **ADR** records *why* a decision was made — context, options, choice, consequences — immutable once accepted, numbered and append-only.

A living spec is the source of truth; ADRs are the immutable trail of why it reads the way it does.

## Included Skills

- `brainstorming` - ideation on-ramp: turns a rough idea into an approved design through strict one-question-at-a-time dialogue with explicit tradeoffs and optional web research, then hands the design to `using-spec-driven`. Also exposed as the `/brainstorm` command.
- `using-spec-driven` - router: given a change already known to be a spec/ADR matter, picks the right authoring skill and enforces the lifecycle order.
- `authoring-living-spec` - creates or edits a living spec under `docs/specs/`: structure, frontmatter, current-state-only discipline, one capability per file.
- `writing-adr` - writes an ADR under `docs/adr/`: the four body sections, four-digit numbering, immutability and supersede rules.
- `evolving-a-spec` - runs the change lifecycle end to end: ADR → spec edit → `governing_adrs` bump, including reversals.

## The Change Lifecycle

- **Write an ADR** (`status: proposed`) capturing the why, the options, and the decision; number it `max(existing) + 1`.
- **Accept it** (`status: accepted`) once the decision is settled — its body is then immutable.
- **Edit the affected living spec(s)** to the new current state; add the ADR id to `governing_adrs` and bump `last_updated`.
- **Supersede on reversal**: a later ADR sets `supersedes: <old>`, and the old ADR flips to `status: superseded` + `superseded_by: <new>`.

Trivial wording fixes to a spec need no ADR — only changes to *what the system does* or *how it is structured*.

## Coexistence with Agent Ready Repo

This plugin owns the *authoring and evolution* of specs and ADRs. Its sibling `agent-ready-repo` owns *classification and placement* of knowledge across all artifact types (AGENTS.md, rules, skills, docs, ADRs). The generic "where should this knowledge live?" question routes to `using-agent-ready-repo`; once a change is known to be a spec/ADR matter, `using-spec-driven` takes over. See `references/coexistence-eval.md`.

## Install

Spec Driven is published in the agent-context-kit marketplace alongside `agent-ready-repo`. Install or load it from `plugins/spec-driven` and confirm the skills appear under the `spec-driven` namespace.

## Source of Truth

The repo's canonical governance document is `docs/specs/meta/spec-governance.md`. This plugin operationalizes that model; if a plugin reference drifts from it, the repo spec wins.
