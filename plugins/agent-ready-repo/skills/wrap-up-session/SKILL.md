---
name: wrap-up-session
description: Closes out a coding session when the user says wrap up, ship it, finalize, or commit and PR — audits findings, promotes durable knowledge to spec / AGENTS / code, mutates the active continuation prompt in place (or writes a new one only when the spec direction changed), branches, commits, opens a PR, and merges.
---

# Wrap up a coding session

Procedural checklist for closing out a session. Detects the repo's
agent-doc convention, captures knowledge that exists only in this
chat into the right doc, writes a continuation prompt, then ships
via PR.

## When to use

User says any of:
- "wrap up" / "wrap this up" / "let's ship it"
- "finalize" / "end of session" / "we're done"
- "PR and merge" / "commit and PR" / "open a PR"
- "update the docs and ship"

## When NOT to use

- Mid-session, when work isn't actually done
- The user wants to commit but explicitly NOT open a PR (just commit)
- Repo has no agent-facing docs at all — then skip the doc steps,
  run the rest

## The flow

Run sequentially. Each step has a STOP condition — if it triggers,
report back instead of proceeding.

### 1. Detect the repo's agent-doc layout

Before touching anything, find where agent docs live. Discover by
filesystem, don't assume:

```bash
ls AGENTS.md AGENT.md CLAUDE.md GEMINI.md AGENTS.override.md 2>/dev/null
find . -maxdepth 4 -name AGENTS.md -not -path './node_modules/*' -not -path './.git/*'
ls docs/ specs/ 2>/dev/null
find . -maxdepth 5 -iname 'CONTINUATION-PROMPT-*.md' -not -path './.git/*' | head
```

Pick the nearest `AGENTS.md` for files you're touching; treat
`CLAUDE.md` / `GEMINI.md` as host-specific wrappers around it. For
the layered model (which artifact owns which knowledge), use the
agent-ready-repo plugin if installed — see step 3.

For continuation prompts, **mirror whatever location already exists
in the repo** (find them via the `find` above). If nothing exists,
default to `.plans/CONTINUATION-PROMPT-<slug>.md` — a hidden,
gitignorable location, since continuation prompts are per-developer
working notes that most teams don't want in the committed tree.
Confirm with the user before creating new top-level folders.

If `.plans/` is the chosen default and the repo doesn't already
ignore it, suggest adding `.plans/` to `.gitignore` so prompts stay
local by default. Teams that *do* want continuation prompts
committed can opt in by not ignoring the directory, or by using
`docs/plans/` instead.

Record the chosen paths and use them for the rest of the flow.

### 2. Audit the session

List, grounded in `git status` + `git diff` (don't trust memory):
- **What landed** — files created / modified, infra provisioned, decisions made
- **What broke + how it was fixed** — each hard-won lesson is a gotcha candidate
- **What was discovered** that isn't already in docs
- **What was discussed but isn't in code or git** — rationale, rejected
  alternatives, environment quirks, undocumented external behavior,
  root causes that the fix alone won't reveal

**STOP if** there's nothing meaningfully done — confirm with user before continuing.

### 3. Capture hard-to-get knowledge into agent docs

The point: a future agent reading the repo cold cannot reconstruct
what we learned from this chat. Save the durable bits, routing each
piece to the right layer.

**Filter first** — save only if all three are true:
- Non-obvious (would trip the next agent)
- Cost real time, or would have if not warned
- Won't be obvious from reading the code / git log later

**Routing — delegate to agent-ready-repo.** That plugin owns the
layered model (AGENTS.md = contract, docs/ = durable memory,
CLAUDE.md / GEMINI.md = host wiring, skills = procedures, hooks/CI =
enforcement) and the artifact decision matrix. Don't duplicate it
here.

- If `agent-ready-repo:agent-ready-maintenance` is available, invoke
  it with the audit findings — it decides which layer owns what and
  updates accordingly.
- If only `agent-ready-repo:using-agent-ready-repo` is available,
  invoke it as the router; it picks the right sub-skill.
- If neither is available, fall back to a one-line classification:
  exact command / boundary / 2-5 hard-won conventions → `AGENTS.md`;
  long-form rationale, ADRs, runbooks, research → `docs/`; host
  quirks → `CLAUDE.md` / `GEMINI.md`; repeated procedure → a skill.
  Then confirm with the user before writing.

### 4. Update other docs touched this session

For each doc whose subject area was touched, update it. The
agent-ready-repo maintenance skill (step 3) usually covers this;
this step is a sweep for anything it missed (architecture, CLI,
service/harness behavior, research notes).

**Skip** if nothing changed that's visible to a future reader.

### 5. Update the continuation prompt

**The default is mutate, not new.** A continuation prompt is a thin
state file — "where we are, what's next, pointers." It's not a place
to re-explain decisions or rebuild the spec. Decisions and durable
reasoning belong in the spec doc, AGENTS.md, or code comments
(promoted in step 3). The prompt should stay short enough to read
on one screen.

This step has four possible outcomes; pick one:

| Outcome | When |
|---|---|
| **(M) Mutate the active prompt in place** | Default. There is an `status: active` prompt for this thread and the spec direction is unchanged. |
| **(N) New prompt, supersede prior** | The spec direction changed, OR you split one thread into two, OR no prior prompt exists for this thread. |
| **(A) Archive — thread done** | All `What's next` items shipped or were abandoned. |
| **(S) Skip — no prompt needed** | Trivial session with no concrete next-session action. |

#### 5a. Diff prior "What's next" against the repo

Whether mutating or writing fresh, first reconcile. Find the active
head for this thread:

```bash
# Find the active head for this thread (or all active heads if no thread set)
grep -l '^status: active$' docs/<plans-dir>/CONTINUATION-PROMPT-*.md \
  .plans/CONTINUATION-PROMPT-*.md 2>/dev/null

# Check what shipped since its last_session
prior=<chosen-path>
since=$(grep "^last_session:" "$prior" | sed 's/last_session: //')
git log --since="$since" --oneline
gh pr list --state merged --search "merged:>=$since" --limit 20
```

Walk the prior's `What's next` list:
- **shipped** → remove this line in the mutate path; in the new-file
  path, just don't carry it forward.
- **still open** → keep (mutate) or carry forward (new).
- **abandoned** → drop; note in commit message or `Where we are` if
  relevant context for future-you.

If **all** items shipped or were abandoned → outcome **(A)**: edit
the prior's `status` to `shipped` (all done) or `abandoned`
(deliberately not picked up), `git mv` it to the archive dir, skip
to step 6.

#### 5b. Routing decisions — what goes WHERE

Anything that's a *decision*, *spec amendment*, or *gotcha* belongs
outside the prompt. Use step 3 to promote first; the prompt then
just points at the durable home.

| Knowledge type | Goes in |
|---|---|
| Why we chose X over Y (option a vs b) | Spec doc (or ADR) — amend in place, link from prompt if load-bearing for next session |
| Non-obvious naming or shape decisions | Code comment + spec note. The prompt should NOT restate it. |
| Behavior gotchas a future agent will hit | AGENTS.md gotcha index entry; trouble-doc body |
| Host/tool quirks | CLAUDE.md / GEMINI.md |
| Current branch/commit/file state | The prompt — this IS the prompt's job |
| Concrete next actions with file paths | The prompt |
| Open questions blocking next session | The prompt |

Rule of thumb: **if it would still be true two threads from now**,
it belongs in spec/AGENTS/code. If it's "where we left off
yesterday," it belongs in the prompt.

#### 5c. Outcome (M) — mutate the active prompt in place

Default path. Edit the existing file:

1. Bump `last_session: YYYY-MM-DD` to today.
2. Optionally append PR numbers to `pr:` (or add the field).
3. **Trim**: drop shipped items from `What's next`. Drop resolved
   `Open questions`. Drop `Where we are` paragraphs that no longer
   describe current state.
4. **Replace**: rewrite `Where we are` to one short paragraph of the
   current state.
5. **Add**: only what changed materially. New next-actions, new open
   questions, new pointers.

After mutation, the file should still fit on one screen (~60 lines of
body, less is better). If it doesn't, you're restating things that
belong in spec/AGENTS — promote them and link.

The `supersedes` / `superseded_by` chain stays untouched in mutate
mode. No `git mv`. The file is the same head.

#### 5d. Outcome (N) — new prompt, supersede prior

Use only when:
- The spec direction itself changed (the prior prompt's framing is
  no longer accurate), OR
- One thread legitimately splits into two distinct followups, OR
- No prior prompt exists for this thread at all.

NOT a reason to write new: "I made some interesting decisions and
want to document them." That's a spec/AGENTS update, not a new prompt.

Create the file at the location from step 1, named
`CONTINUATION-PROMPT-<slug>.md`:

```yaml
---
slug: <matches-filename-minus-prefix>
status: active
last_session: YYYY-MM-DD
thread: <kebab-tag>          # optional — groups related prompts
supersedes: <prev-slug>      # required when a prior prompt exists in this thread
pr: "#NN, #MM"               # optional — PRs this session shipped
---
```

**Omit optional fields when they don't apply** — do NOT write
`pr: ""` or `superseded_by: ""`. `superseded_by` is set later by the
*next* session when this prompt gets superseded. Full schema and
reading semantics in `resume-from-continuation` §1a.

Body — short:
- **Where we are** (one paragraph)
- **What's next** (3–5 actions with file paths / commands)
- **Open questions** (decisions deferred — small, blocking ones only)
- **Pointers** (files, commits, runnable verification)

Then back-link the predecessor: edit its frontmatter to
`status: superseded` + `superseded_by: <new-slug>` and
`git mv` it to the archive dir (e.g. `docs/harness-history/plans/`).
No README index update — frontmatter is the index.

Self-contained: the next agent must be able to pick up cold with no
prior conversation. But "self-contained" doesn't mean "rebuilds the
spec" — it means "links to the spec at the right anchor."

#### 5e. Outcome (S) — skip

If neither a mutate nor a new makes sense (rare — only when the
session was trivial AND there's no active head for the thread):
tell the user "no continuation prompt needed; nothing concrete to
hand off."

A missing prompt is fine; a stale prompt costs the next agent's
context window.

**Skip the whole step** if the user explicitly says "no continuation
needed", or if step 1 detected no continuation-prompt location.

### 6. Branch off main

```bash
git checkout -b <type>/<brief-description>
```

`<type>` = feat | fix | docs | chore | refactor | test (or whatever
the repo's conventional-commit scopes are — grep recent `git log` if
unsure). Branch description matches the work.

**STOP if** working tree was dirty before this session and there's
unrelated stuff staged — ask user how to split.

### 7. Commit (conventional commits, possibly multiple)

Run in parallel: `git status`, `git diff`, `git log -5` to mirror the
repo's commit style. Then split logically:
- Doc updates → one `docs: ...` commit
- New gotchas → fold into the docs commit or split
- Continuation prompt → its own `docs: ...` commit or folded

Commit message body via heredoc (preserves formatting).

**Do NOT** mention Claude, Anthropic, any LLM, "AI", "Generated with",
or `Co-Authored-By: Claude` in commit messages. The commit should
read as the user's own work. See common mistakes.

**Never** use `git add -A` or `.`; stage by explicit path. Verify
nothing sensitive is in scope (`.env`, keys, local config files).

### 8. Push + open PR

```bash
git push -u origin <branch>
gh pr create --title "..." --body "$(cat <<'EOF'
## Summary
<1–3 bullets>

## Test plan
- [ ] <runnable verification>
EOF
)"
```

Title under 70 chars. Body explains the why, not the what (diff shows
the what).

**Do NOT** add Claude / LLM / "Generated with" footers to the PR body
either. Same rule as commits.

**STOP if** the user asked you not to push, or there's no remote.

### 9. Merge + pull main

Only auto-merge if CI is green (or the repo's CI is `workflow_dispatch`
only — then ask user first).

**Default to merge-commit** (`gh pr merge <num> --merge --delete-branch`)
— preserves every commit in `main`'s history, which is the user's
stated preference. Check `gh api repos/{owner}/{repo} --jq
'{squash:.allow_squash_merge,merge:.allow_merge_commit,rebase:.allow_rebase_merge}'`
if unsure what the repo allows; fall back to `--rebase` for linear
history, or `--squash` only if `--merge` is disabled at the repo
level.

```bash
gh pr merge <num> --merge  --delete-branch     # default — keeps all commits
gh pr merge <num> --rebase --delete-branch     # linear, also keeps all commits
git checkout main
git pull origin main
```

**STOP if** PR has unresolved review comments, CI is red, or there are
merge conflicts. Report and wait.

## Quick reference

| Step | Always | Skip when |
|---|---|---|
| 1. Detect conventions | Yes | — |
| 2. Audit | Yes | — |
| 3. Capture knowledge → agent docs | If anything non-obvious surfaced | Nothing chat-only worth saving |
| 4. Other docs | If touched area | Nothing user-visible changed |
| 5. Continuation prompt | Default = **mutate** active head; new only when spec changed | User says no, no location detected, or thread is fully shipped |
| 6. Branch | Yes | Already on a feature branch |
| 7. Commit | Yes | Nothing staged |
| 8. Push + PR | Yes | User says hold |
| 9. Merge + pull | Yes | CI red / conflicts / review pending |

## Common mistakes

- **Mentioning LLMs / Claude / "AI" / "Generated with" in commits or
  PR bodies.** Forbidden. No `Co-Authored-By: Claude`, no robot emoji
  footer, no "with help from an AI assistant". The commit and PR are
  the user's work.
- **Committing on main.** Most repos forbid it. Branch first.
- **Padding the gotchas section.** A gotcha that's "interesting" but
  doesn't cost time gets deleted in review. Cut.
- **Saving chat-only knowledge as ephemeral notes instead of into
  agent docs.** If it took the session to learn it and the next agent
  would need it, write it down where they'll find it.
- **Continuation prompt that needs the prior conversation.** Test by
  re-reading it cold — would a fresh agent know what to do? If no,
  rewrite.
- **`git add -A`.** Stages local-only files, secrets, scratch. Always
  stage by explicit path.
- **PR title > 70 chars.** Commitlint will fail; rebase needed.
- **Skipping the repo's pre-commit verification** (lint, test, type-check).
  Grep the agent file for the canonical command and run it.
- **Hardcoding doc paths.** Always detect in step 1 — don't assume
  `AGENTS.md` exists or that docs live in `docs/`. The repo may use a
  tool-specific file (`CLAUDE.md`/`GEMINI.md`), nested per-package
  `AGENTS.md`, or no docs tree at all.
- **Inventing a layout that isn't real.** Stick to documented
  conventions (AGENTS.md open standard, CLAUDE.md, GEMINI.md). Don't
  fabricate sibling directories like `agent/` or `.agent/` — they
  aren't part of any standard.
- **Duplicating the layered model inline.** Routing (which knowledge
  goes to AGENTS.md vs docs/ vs host file vs skill) belongs in
  `agent-ready-repo`. Invoke its skills in step 3 instead of
  rewriting the decision matrix here.
- **Defaulting to squash.** Squash collapses meaningful commit boundaries.
  Prefer `--merge` (or `--rebase`); only squash if the repo disables both.
- **Committing a continuation prompt the team didn't ask for.** The
  default location `.plans/` is gitignorable on purpose. If the repo
  doesn't ignore it and there's no team convention saying continuation
  prompts get committed, ask before staging the file.
- **Writing a new prompt when the spec direction is unchanged.** The
  default for an active thread is mutate, not new. New files
  proliferate stale heads and bury the chain in archives. New only
  when the spec amendment is large enough that the prior prompt's
  framing is wrong, or you genuinely split one thread into two.
- **Restating decisions in the prompt instead of promoting them.** If
  this session resolved an option-a-vs-b question, picked a non-
  obvious name, or learned a gotcha, that lives in the spec
  doc / AGENTS.md / code comment — not in `Where we are`. The prompt
  links to it at most. Continuation prompts that re-explain decisions
  duplicate spec content and rot quickly.
- **Prompts that grow past one screen.** ~60 lines of body is the
  soft ceiling. Past that, you're restating durable content; promote
  it out and trim. A 200-line prompt is a documentation smell.
- **Carrying forward `What's next` items that already shipped.** Step
  5a reconciles against git log — actually do it. Skipping the diff
  is how stale prompts accumulate.
- **Leaving a finished thread `status: active`.** If everything in
  `What's next` shipped, flip to `shipped` and archive. The repo's
  active-prompt set should reflect real open threads, not historical
  ones.
