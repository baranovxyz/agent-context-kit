# Coexistence eval: spec-driven vs agent-ready-repo

A small should-trigger / should-not-trigger suite for confirming that `using-spec-driven` and
`agent-ready-repo`'s `using-agent-ready-repo` do not collide on router triggers. `spec-driven` owns
*authoring and evolution* of specs and ADRs; `agent-ready-repo` owns *classification and placement*
of knowledge across all artifact types. The guard: `using-spec-driven` must fire on spec/ADR
authoring asks and stay silent on generic placement asks.

| Query | Should route to | Must NOT trigger |
|---|---|---|
| "Write a spec for the manager-composition feature" | using-spec-driven → authoring-living-spec | using-agent-ready-repo |
| "Record why we chose the curated catalog" | using-spec-driven → writing-adr | — |
| "We changed how the daemon dispatches; update the docs" | using-spec-driven → evolving-a-spec | — |
| "Where should this new convention live — AGENTS.md or docs?" | using-agent-ready-repo | using-spec-driven |
| "Audit our AGENTS.md for drift" | using-agent-ready-repo (agent-ready-audit) | using-spec-driven |

## How to run the eval

Read each query and confirm, from the routed skill's frontmatter `description` alone, that it is the
one a router would pick — then check that the listed "Must NOT trigger" skill stays silent. The
first three rows exercise the spec-driven authoring paths (author a fresh spec, record a decision,
run the full change lifecycle). The last two rows are the coexistence guard: they are generic
placement / audit asks that belong to `agent-ready-repo` and must **not** pull `using-spec-driven`.
If a description change makes either guard row fire `using-spec-driven`, tighten the description
back to the spec/ADR authoring trigger before shipping.
