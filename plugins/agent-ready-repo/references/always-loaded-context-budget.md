# Always-loaded context budget

`AGENTS.md` and `CLAUDE.md` load into **every** agent session. Every line costs
tokens on every turn, forever — so always-loaded files are the scarce resource,
not the model's intelligence.

## Rules

- **Pointers over copies.** Keep lightweight identifiers (file paths, keywords,
  links) in always-loaded files; load detail on demand. Never duplicate a doc's
  headings or body into `AGENTS.md`.
- **Gotchas, runbooks, and indexes are on-demand.** They belong in `docs/` and
  are grepped when needed — not pasted into `AGENTS.md`.
- **Only every-task rules belong in `AGENTS.md`.** If a rule applies to nearly
  every session, keep it; otherwise make it a referenced doc or a skill.
- **Enforce with a tool, not prose.** Style/length discipline belongs in a
  deterministic check (see `bin/agent-ready-check` byte/line budget), not in a
  paragraph that itself costs tokens every session.
- **Target.** Keep `AGENTS.md` well under the byte budget and every line under
  the per-line cap; `agent-ready-check` flags both.

## Sources

- Anthropic — Effective context engineering for AI agents
- Anthropic — Best practices for Claude Code
- HumanLayer — Writing a good CLAUDE.md
