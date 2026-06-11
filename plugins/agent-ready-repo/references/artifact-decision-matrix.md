# Artifact Decision Matrix

When new agent-facing knowledge appears, classify it before editing files.

| Need | Artifact |
|---|---|
| Needed in every session by coding agents | `AGENTS.md` |
| Needed only to make Claude Code load shared truth | thin `CLAUDE.md` wrapper around `AGENTS.md` |
| Needed only inside one monorepo package | package-level instruction delta plus package docs |
| Long, durable, rarely needed | `docs/` |
| Requirements, scope, non-goals, acceptance criteria | `docs/specs/` |
| File-level implementation order and verification | `docs/plans/` |
| Architecture decision and consequences | `docs/adr/` |
| Portable coding convention | `docs/rules/` and link from `AGENTS.md` |
| Host-specific behavior | `CLAUDE.md`, `.cursor/rules`, `.github/instructions`, `GEMINI.md` |
| Claude Code path-scoped guidance | `.claude/rules/` |
| Repeatable procedure | skill |
| Autonomous worker role | agent |
| Explicit user-invoked workflow | skill with `disable-model-invocation: true` |
| Known local operation | CLI plus skill |
| Governed external access | MCP |
| Rule must always run | hook or CI |
| Obvious from one file read | no new artifact |

## Classification Questions

Ask these before writing:

1. Is this needed in every session?
2. Is this stable project memory or a repeatable procedure?
3. Is this specific to one agent host?
4. Does this need enforcement rather than advice?
5. Does this involve live data, user credentials, or tenant boundaries?
6. Would a senior engineer infer this cheaply from code?
7. Did this emerge from a repeated agent mistake?

## Migration Rules

- Move, do not silently delete, existing knowledge.
- Replace duplicated vendor copies with thin pointers.
- Keep active specs and plans out of `AGENTS.md`.
- In monorepos, keep shared truth at the root and local deltas in package-level instruction files.
- Create skills only when a process repeats.
- Prefer skills over new `commands/` files; command files are legacy flat skills.
- Create agents only when autonomous multi-step work benefits from isolated context.
- Create hooks only when the rule must run automatically.
- Add plugin dependencies, marketplace metadata, MCP servers, monitors, channels, and LSP servers
  only for concrete runtime needs.
