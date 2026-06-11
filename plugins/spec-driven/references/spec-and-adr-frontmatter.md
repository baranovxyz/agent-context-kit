# Spec and ADR frontmatter

The exact frontmatter shapes for living specs (`docs/specs/<domain>/<capability>.md`)
and ADRs (`docs/adr/NNNN-<kebab-title>.md`).

## Living spec frontmatter

```yaml
---
name: <kebab-case-slug>
domain: <domain folder name>
status: draft | active | deprecated
governing_adrs: [NNNN, ...]
last_updated: YYYY-MM-DD
---
```

- `name` — kebab-case slug, unique within its domain.
- `domain` — the folder the spec lives in (`harness`, `sync`, `routines`, `meta`, …); create a new
  folder when no existing domain fits.
- `status` — `draft` = being written, not yet authoritative; `active` = current source of truth;
  `deprecated` = capability removed or superseded, kept for reference with a pointer to its
  replacement.
- `governing_adrs` — list of ADR ids that shaped the spec's current state.
- `last_updated` — `YYYY-MM-DD`; bump on every content edit.

### Worked example (spec header)

```yaml
---
name: manager-composition
domain: harness
status: active
governing_adrs: [0002, 0007]
last_updated: 2026-05-29
---
```

## ADR frontmatter

```yaml
---
id: "NNNN"
title: <imperative sentence>
status: proposed | accepted | superseded
date: YYYY-MM-DD
affects_specs: [<domain>/<name>, ...]
supersedes: NNNN | null
superseded_by: NNNN | null
---
```

- `id` — four-digit, zero-padded; matches the filename number.
- `title` — imperative sentence stating the decision.
- `status` — `proposed` = drafted, decision not yet settled; `accepted` = settled and immutable;
  `superseded` = reversed by a later ADR.
- `date` — `YYYY-MM-DD` the ADR was written.
- `affects_specs` — list of `<domain>/<name>` specs this decision shapes.
- `supersedes` — ADR id this one overturns, or `null`.
- `superseded_by` — ADR id that overturned this one, or `null`.

### Worked example (ADR header)

```yaml
---
id: "0002"
title: Compose the article manager from a fixed content/compositor/reviewer pipeline
status: accepted
date: 2026-05-29
affects_specs:
  - harness/manager-composition
supersedes: null
superseded_by: null
---
```

These mirror `docs/specs/meta/spec-governance.md`; if they drift, the repo spec wins.
