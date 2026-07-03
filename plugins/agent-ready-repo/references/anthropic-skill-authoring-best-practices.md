# Skill authoring (best practices, adapted for this plugin)

Practical authoring principles drawn from Anthropic's skill
best-practices guidance, condensed to what `agent-ready-repo`
applies when designing or reviewing skills.

For the canonical, frequently-updated source (with examples):
<https://docs.claude.com/en/agents-and-tools/agent-skills/best-practices>

## The context window is a public good

A skill's SKILL.md competes with conversation history, other
skills' metadata, and the system prompt for the same finite
context budget. Only metadata (name + description) is pre-loaded
at startup; the body of SKILL.md loads on demand when the
description matches, and reference files load only when the body
needs them.

This makes two things load-bearing:

1. **The description is the single highest-leverage line** in a
   skill. It decides whether the skill loads at all.
2. **SKILL.md tokens are not free.** Once loaded, every paragraph
   competes with everything else Claude needs to know. Default
   assumption: Claude is already smart — only add context Claude
   doesn't have.

For every paragraph you write, ask:

- Does Claude really need this explained?
- Can I assume Claude knows this from training?
- Does this paragraph justify its token cost?

If the answer is "no" to any, cut.

## Match degrees of freedom to the task

Pick the right specificity level for what you're encoding:

- **High freedom (prose instructions).** Multiple approaches are
  valid; decisions depend on context; heuristics guide. Right for
  judgment work — code review, architectural decisions, routing
  between artifacts.
- **Medium freedom (pseudocode or parameterized scripts).** A
  preferred pattern exists; some variation is acceptable; config
  affects behavior. Right for templated work — generating reports,
  scaffolding files.
- **Low freedom (specific scripts, no parameters).** Exact
  reproducibility matters; one correct way exists. Right for
  deterministic mechanical work — validation, fixed
  transformations.

Picking wrong fails in opposite directions: too much freedom on a
fragile task gives inconsistent results; too little on a creative
task gives brittle skills that can't adapt.

## Description metadata is the most important field

It's the only thing Claude sees at startup. Required structure:

- **One line, plain text.** No multiline YAML scalars, no
  Markdown, no code fences, no lists, no XML-like tags, no
  conversation transcripts, no examples.
- **Capability + trigger context together.** State both what the
  skill does AND when to invoke it. Example: "Audits agent-facing
  repository memory when AGENTS.md, docs, skills, agents, hooks,
  or plugin setup need qualitative evaluation."
- **No `when_to_use` field.** Some hosts don't support it; put
  trigger guidance into the description and the Markdown body
  instead.
- **≤240 characters.** Longer descriptions get truncated or
  parsed incorrectly by some hosts, silently breaking the trigger.

## Naming conventions

- **kebab-case.** `agent-ready-audit`, not `agentReadyAudit` or
  `agent_ready_audit`.
- **Describe the action**, not the noun. `audit-skills` beats
  `skill-auditor`; `wrap-up-session` beats `session-wrapper`.
- **Avoid generic words.** `helper`, `utils`, `general`, `stuff` —
  these don't trigger reliably because they don't distinguish
  cases.
- **Match the actual scope.** Names broader than the skill cause
  coexistence problems with future related skills.

## Progressive disclosure

SKILL.md is a table of contents, not the manual:

```text
SKILL.md          # lean overview, when-to-use, top-level flow
references/*.md   # detailed material loaded only when needed
scripts/*         # bundled executables for deterministic work
```

An agent reading SKILL.md should be able to:

1. Decide whether the skill applies to the current task.
2. Know what to do next at a high level.
3. Find reference files when (and only when) it needs depth.

The agent `Read`s reference files only when the SKILL.md flow
points to that specific detail. This keeps the context cost of a
loaded-but-not-deeply-needed skill close to its SKILL.md size, and
keeps an unloaded skill's cost at just its metadata line.

## SKILL.md structure that works

- **Frontmatter** — name, description, optional `argument-hint`,
  optional `disable-model-invocation: true` for user-only
  workflows, optional version.
- **One-paragraph overview** — what this skill does, in plain
  prose, no fluff.
- **When to use / When NOT to use** — explicit trigger boundaries.
  This is the section Claude consults under load to decide whether
  to keep going with the skill.
- **The flow** — numbered steps with explicit STOP conditions that
  tell the skill to bail and ask the user rather than proceed on
  thin information.
- **Quick reference table** — for skills with conditional steps, a
  compact table beats re-reading the prose flow each time.
- **Common mistakes** — anti-patterns observed in practice, with
  one line of "do this instead". Saves debugging cycles for
  future agents (and humans) hitting the same trap.

## Things that quietly degrade a skill

- **Vague trigger words in the description** — `help`, `useful`,
  `general`, `stuff`, `things`. Claude can't reliably distinguish
  when these apply.
- **Long descriptions** — over the 240-char limit they get
  truncated mid-sentence in some contexts, silently breaking the
  trigger.
- **Embedding project facts in the skill body.** Skills are
  procedures, not knowledge stores. Project facts (API endpoints,
  version numbers, team conventions) belong in `AGENTS.md` or
  `docs/`. If the skill needs to reference them, link rather than
  inline.
- **Bundling live data.** Anything that changes (URLs, version
  numbers, credentials, IPs) goes stale and misleads.
- **Multiple concerns in one skill.** Claude can't decide when to
  invoke it; trigger accuracy splits across both concerns,
  degrading both.
- **Treating SKILL.md like full documentation.** Long, exhaustive
  SKILL.md files burn context that other skills and conversation
  need. Push depth into `references/`.

## Evaluation and iteration

Treat skills like code that needs tests:

- **Build a small eval suite** per skill: 3–5 representative
  queries covering should-trigger, should-not-trigger, and
  ambiguous edge cases.
- **Run on every change.** If trigger accuracy or output quality
  degrades, the change broke something — investigate before
  shipping.
- **Re-evaluate periodically.** Model upgrades and concurrent
  changes to other skills both shift behavior; a skill that
  worked last quarter may misbehave today.
- **Deprecate, don't infinitely patch.** Skills that consistently
  fail evaluations should be retired rather than rewritten in
  place — the workflow may no longer fit the skill model.

## How this plugin applies the model

- `skill-and-agent-designer` enforces "one concern per skill" and
  the description-shape rules when proposing a new skill.
- `agent-ready-check` preflight catches mechanical violations:
  multiline descriptions, `when_to_use` fields, examples or
  Markdown in frontmatter, descriptions over 240 chars, vague
  trigger words. Run it as a pre-commit gate.
- `agent-ready-audit` applies the qualitative checks — trigger
  accuracy, coexistence with the existing skill set, embedded
  project facts, multi-concern bloat — that can't be mechanically
  detected.
- `agent-ready-maintenance` defers to the progressive-disclosure
  pattern when deciding whether new content belongs in a skill,
  its references, a bundled script, or somewhere else entirely.
