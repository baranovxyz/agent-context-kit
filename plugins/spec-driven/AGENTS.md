# AGENTS.md

## Project Overview
Spec Driven ships the ideation, authoring, and evolution slices of the spec-governance model: an
ideation on-ramp (`brainstorming`, also the `/brainstorm` command) plus skills that teach agents to
author living specs (`docs/specs/`) and ADRs (`docs/adr/`) and run the ADR→spec change lifecycle.
Brainstorming produces an approved design and hands it to `using-spec-driven`, which routes it into
an ADR and a living spec. The plugin ships parallel manifests for Claude Code, Cursor, and Codex;
the body components (`skills/`, `commands/`, `references/`) are shared across all three hosts. It is
the second plugin in the agent-context-kit marketplace, alongside `agent-ready-repo`. It
operationalizes `docs/specs/meta/spec-governance.md`.

## Docs
Read these when changing plugin behavior:

- `README.md` - user-facing overview, the four skills, the change lifecycle
- `references/spec-and-adr-frontmatter.md` - exact frontmatter shapes for living specs and ADRs
- `references/change-lifecycle.md` - the four-step ADR→spec flow, immutability + supersede rules
- `references/coexistence-eval.md` - router-trigger eval guarding overlap with `agent-ready-repo`
- `docs/specs/meta/spec-governance.md` (repo root) - the source of truth this plugin
  operationalizes; if a reference drifts, the repo spec wins

## Project Structure
```text
.claude-plugin/plugin.json   # Claude Code plugin manifest
.cursor-plugin/plugin.json   # Cursor plugin manifest
.codex-plugin/plugin.json    # Codex plugin manifest (includes interface block)
skills/brainstorming/SKILL.md          # ideation on-ramp → using-spec-driven
skills/brainstorming/references/web-research-and-tradeoffs.md  # web-research + tradeoff depth
skills/using-spec-driven/SKILL.md      # router (shared across hosts)
skills/authoring-living-spec/SKILL.md  # create/edit a living spec
skills/writing-adr/SKILL.md            # write an ADR
skills/evolving-a-spec/SKILL.md        # run the change lifecycle end to end
commands/brainstorm.md                 # /brainstorm entry → brainstorming skill
references/spec-and-adr-frontmatter.md # frontmatter shapes
references/change-lifecycle.md         # the change flow
references/coexistence-eval.md         # router-coexistence eval
```

## Verification
```bash
python3 -m json.tool .claude-plugin/plugin.json >/dev/null
python3 -m json.tool .cursor-plugin/plugin.json >/dev/null
python3 -m json.tool .codex-plugin/plugin.json >/dev/null
# Run agent-ready-check from the marketplace root or repo root so it sees all manifests:
( cd ../.. && python3 plugins/agent-ready-repo/bin/agent-ready-check --json )
# From the repo root, the specdoc helper that powers `pnpm spec:ls` / `pnpm adr:ls`:
pnpm test:specdoc
```

## Conventions
- One concern per skill: `brainstorming` turns an idea into an approved design (ideation only —
  never writes specs/ADRs/code), `using-spec-driven` routes, `authoring-living-spec` writes specs,
  `writing-adr` writes ADRs, `evolving-a-spec` runs the lifecycle. `brainstorming` is strictly
  upstream of `using-spec-driven` and hands off to it.
- Write skill descriptions as one-line plain text, ≤240 chars, stating capability and trigger.
- Never use `when_to_use`, multiline YAML scalars, examples, tags, Markdown, or transcripts in
  frontmatter descriptions; keep longer trigger guidance in the body.
- Keep each `SKILL.md` lean (table-of-contents style); depth goes in `references/`.
- Version lockstep: any change under this plugin bumps the version in all three per-plugin manifests
  and all three marketplace manifests, per the agent-context-kit convention. `agent-ready-check`
  warns when these drift.
- Coexistence boundary with `agent-ready-repo`: this plugin owns *authoring and evolution* of specs
  and ADRs; `agent-ready-repo` owns *classification and placement* across all artifact types.
  `using-spec-driven` triggers on "write/update a spec or ADR" and "record this decision" — it must
  never claim `using-agent-ready-repo`'s generic "where does this knowledge go?" placement trigger.
- Use `${CLAUDE_PLUGIN_ROOT}` for plugin-internal reference paths from skills.
- The change lifecycle is ADR-first: the decision (ADR) precedes the documented current-state
  (spec). Never edit spec behavior without a governing ADR. Never edit an accepted ADR's body —
  supersede instead.

## Boundaries
- Always validate JSON after changing any manifest.
- Always update README and references when changing plugin behavior; if a reference drifts from
  `docs/specs/meta/spec-governance.md`, the repo spec wins.
- Never let `using-spec-driven` claim the generic "where does knowledge go" placement trigger — that
  stays with `using-agent-ready-repo`.
- Run the `references/coexistence-eval.md` query suite before shipping any router-description
  change.
