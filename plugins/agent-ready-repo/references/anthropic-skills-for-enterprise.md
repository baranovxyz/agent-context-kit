# Skill governance (enterprise principles, adapted for this plugin)

Practical governance principles drawn from Anthropic's enterprise
skills guidance, condensed to what `agent-ready-repo` actually
applies when auditing, designing, or maintaining skills.

For the canonical, frequently-updated source, see Anthropic's
docs: <https://docs.claude.com/en/agents-and-tools/agent-skills/overview>

## Treat every skill as a reviewed dependency

A skill is executable instruction shipped into agents' context. It
has the same blast radius as a library: it can read files, invoke
tools, reference external services, and influence other skills'
behavior through coexistence. Apply the same scrutiny you'd apply
to a third-party package.

## Risk indicators — what to flag during review

Score each indicator before approving a skill from any source
(including internal contributors):

- **Code execution.** Bundled scripts (`*.py`, `*.sh`, `*.js`) run
  with full environment access. Require sandboxed verification of
  behavior; never approve scripts whose effects you haven't
  watched.
- **Instruction manipulation.** Directives telling Claude to
  ignore safety rules, hide actions from the user, or alter
  behavior conditionally are the highest-risk class — they
  bypass the controls the agent runtime depends on.
- **MCP / external tool references.** `ServerName:tool_name`
  syntax extends the skill's reach beyond its own files. Review
  what tools become accessible and to what.
- **Network access.** URLs, API endpoints, `fetch`, `curl`,
  `requests` — primary data exfiltration vector. Verify
  destinations match stated purpose.
- **Hardcoded credentials.** Keys, tokens, passwords anywhere
  in the skill leak into git history and context windows. Always
  fail review.
- **File system scope.** Paths outside the skill directory, broad
  globs, `../` traversal. Medium concern; flag broad scope even if
  the intent is benign.
- **Tool invocations.** Bash commands, file operations, other
  tools the skill tells Claude to call. Consider combined risk —
  file-read + network is more dangerous than either alone.

## Review checklist (apply before approval)

1. **Read every file** in the skill directory — SKILL.md, all
   referenced markdown, all bundled scripts and resources.
2. **Run bundled scripts in a sandbox**; confirm output matches
   the stated purpose. Never approve a script whose behavior
   you've only inferred from its source.
3. **Search for adversarial directives** — "ignore previous
   instructions", "do not tell the user", behavior conditional on
   specific input patterns.
4. **Grep for network calls** (`http`, `requests.get`, `urllib`,
   `curl`, `fetch`).
5. **Verify no hardcoded credentials** anywhere in the skill files.
6. **Catalog every bash command, file operation, and tool** the
   skill tells Claude to invoke. Consider the combined risk
   (e.g., file-read + network is a credible exfiltration path).
7. **Verify external URL destinations** match what the skill
   claims to do.
8. **Look for read-then-exfiltrate patterns** — instructions that
   read sensitive data and then write, send, or encode it for
   transmission, including through Claude's own responses to the
   user.

## Evaluation dimensions (before deployment)

Skills can degrade agent performance if they trigger wrong, conflict
with other skills, or instruct poorly. Require evaluation across
all five dimensions; weakness in any one breaks the skill in
practice:

- **Triggering accuracy.** Fires for the right queries, stays
  inactive for unrelated ones. The most common failure mode is
  over-triggering on broad descriptions.
- **Isolation behavior.** Works correctly on its own — no implicit
  dependencies on other skills being loaded at the same time.
- **Coexistence.** Adding it doesn't degrade other skills. A new
  skill with a broad description can silently steal triggers from
  more specific existing skills.
- **Instruction following.** Claude follows the documented steps
  accurately — doesn't skip validation, uses the libraries
  specified, respects STOP conditions.
- **Output quality.** Produces correct, useful results with no
  formatting errors or missing data.

Build a small eval suite per skill: 3–5 representative queries
covering should-trigger, should-not-trigger, and ambiguous cases.
Run across the models the org uses (Opus/Sonnet/Haiku); skill
effectiveness varies meaningfully by model.

Eval results signal lifecycle decisions:

- Declining trigger accuracy → tighten description or instructions.
- Coexistence conflicts → consolidate overlapping skills or narrow
  descriptions.
- Persistent quality failures → rewrite or deprecate.

## Lifecycle stages

- **Plan.** Identify repetitive, error-prone, or specialized
  workflows. Map to organizational roles. Decide which deserve a
  skill (vs. a runbook, a CLI, or no artifact).
- **Create + review.** Author follows best practices (see
  `anthropic-skill-authoring-best-practices.md`); security review
  per checklist above; evaluation suite required; **separation of
  duties** — authors don't review their own skills.
- **Test.** Evaluate in isolation AND alongside the existing
  active skill set (coexistence). Verify no regressions in other
  skills' triggering or output quality.
- **Deploy.** Upload via the appropriate channel; document in an
  internal registry with purpose, owner, version, dependencies.
- **Monitor.** Track usage and failures. Re-run evals periodically
  — model upgrades and skill-set changes both shift behavior.
- **Iterate or deprecate.** Full eval suite must pass before
  promoting a new version. Deprecate skills that consistently fail
  evals or whose workflow is retired.

## Skill set hygiene

- **Limit active skill count.** Each skill's metadata competes for
  attention in the system prompt. Use eval recall accuracy as the
  stop signal for adding more. API requests cap at 8 skills per
  request.
- **Start specific, consolidate later.** Narrow workflow-specific
  skills first. Merge into role-based bundles only when evals
  confirm equivalent performance to the originals.
- **Consistent naming** across the org so trigger intent is
  visible from the name.
- **Per-skill registry entry**: purpose, owner, current version,
  dependencies (MCP servers, packages, services), last eval date
  and result.

## Versioning and distribution

- **Source control.** Every skill directory in git for history,
  PR review, and rollback.
- **Pin production versions.** Run the full eval suite before
  promoting a new version; treat every update as a new deployment
  requiring fresh security review.
- **Rollback plan.** Keep the previous version available as
  fallback; revert immediately on production eval failure.
- **Integrity verification.** Checksum reviewed skills; verify at
  deploy time; use signed commits for provenance.
- **Cross-surface caveat.** Skills uploaded via the API are not
  available on claude.ai or in Claude Code, and vice versa. Each
  surface is a separate deployment target.

## How this plugin applies the model

- `agent-ready-auditor` agent uses risk indicators and the review
  checklist as evaluation hooks when assessing skills it finds in
  a repo.
- `agent-ready-maintenance` skill defers to lifecycle stages when
  deciding whether to ship a new skill or extend an existing one,
  and to coexistence concerns when sizing new skill scope.
- `skill-and-agent-designer` applies "one concern per skill" and
  the trigger-accuracy lens before recommending a new artifact.
- `agent-ready-check` preflight enforces the mechanical
  description-shape rules (no `when_to_use`, no multiline scalars,
  ≤240 chars). Qualitative review is the human / agent job.
