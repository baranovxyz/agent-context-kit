---
name: resume-from-continuation
description: Resumes a session from a continuation prompt when the user says continue, resume, or pick up where we left off — finds the prompt, verifies it against current repo state, surfaces drift, and confirms the next action with the user.
---

# Resume from continuation prompt

Counterpart to `wrap-up-session`. Closes the loop: a previous
session wrote a continuation prompt; this skill picks it up cleanly
without losing context.

## When to use

User says any of:
- "continue" / "continue session" / "resume"
- "pick up where we left off" / "pick up from the prompt"
- "continue from `<slug>`" / "continue from `CONTINUATION-PROMPT-...`"
- "what were we doing"

## When NOT to use

- Fresh task with no prior context — just do the work.
- User wants a brand-new direction unrelated to past sessions — ask
  what they want before reading old continuation prompts.

## The flow (6 steps)

### 1. Find the continuation prompt

If the user named a specific slug, use that file. Otherwise
**discover by filesystem** — different repos use different
locations:

```bash
# common locations, in priority order: hidden/local first, committed second
ls -t .plans/CONTINUATION-PROMPT-*.md \
      docs/plans/CONTINUATION-PROMPT-*.md \
      docs/harness-plans/CONTINUATION-PROMPT-*.md \
      docs/CONTINUATION-PROMPT-*.md \
      2>/dev/null | head -5

# fallback: anywhere in the tree (exclude archive dirs)
find . -maxdepth 5 -iname 'CONTINUATION-PROMPT-*.md' \
   -not -path './.git/*' -not -path './node_modules/*' \
   -not -path '*-history/*' -not -path '*-archive/*' | head
```

**Filter to heads using frontmatter.** If prompts carry the
frontmatter schema in §1a, only `status: active` candidates are real
heads worth resuming. `status: shipped` means the work is done with
no active follow-up; `status: superseded` means a newer prompt
continues the thread — chase `superseded_by` forward to the head.

```bash
# Filter to active heads
for f in <candidates>; do
  head -12 "$f" | grep -q '^status: active$' && echo "$f"
done
```

If multiple **active** candidates exist (any within ~7 days), **ask
which one** — don't guess. Old prompts go stale fast; the wrong one
wastes the whole session.

If no frontmatter is present (legacy prompts), fall back to mtime +
the "Supersedes:" prose line in the body.

**STOP if** no active continuation prompts exist. Tell the user; ask
what they want to do.

### 1a. Frontmatter schema (when present)

```yaml
---
slug: <kebab-case>             # required — matches filename minus prefix; cross-ref key
status: active | shipped | superseded | abandoned   # required
last_session: YYYY-MM-DD       # required
thread: <kebab-tag>            # optional — groups related prompts
supersedes: <slug>             # optional — prior prompt in this thread
superseded_by: <slug>          # optional — next prompt in this thread; if set, file should live in archive dir
pr: "#NN" or "#NN, #MM"        # optional — shipped PRs
---
```

**Omit optional fields when they don't apply** — do NOT write
`pr: ""` or `superseded_by: ""`. Empty strings are ambiguous (no
value vs deliberately empty); omitting the key makes filters cleaner
(`grep -L '^superseded_by:' file` matches heads).

Reading semantics:
- `status: active` → thread open, this is the head — candidate to resume from.
- `status: shipped` → work done this session, no follow-up planned — thread closed; skip unless user
  explicitly revives.
- `status: superseded` → a newer prompt continues this thread; walk `superseded_by` forward to the
  head before resuming.
- `status: abandoned` → open work was deliberately not picked up; thread closed. Skip unless user
  explicitly revives.
- `supersedes` + `superseded_by` form a linked-list chain. Walk forward to find the current head;
  walk back for context only.
- Absent `superseded_by` (plus `status: active` or `shipped`) = this is the head.

### 2. Read it fully

Read the whole file, not just the "What's next" section. The "Where
we are" and "Open questions" sections often contain the constraint
that changes how next steps should be sequenced.

Note in particular:
- The commit hash the prompt anchored to (in "Pointers")
- Any "agreed-but-not-implemented" decisions
- Live infrastructure references (hosts, branches, worktrees)

**Mutate-style heads are normal.** The `wrap-up-session` skill prefers
editing the active prompt in place across sessions rather than
spawning new files — so seeing the same `slug` mutated multiple times
across the thread is the expected pattern. Use `git log -p <file>`
on the prompt itself to see how the framing evolved if useful for
context.

**The prompt won't restate decisions.** Mutate-style prompts stay
short by promoting decisions / non-obvious naming / gotchas out to
the spec doc, AGENTS.md, or code comments. If you need the *why*
behind a current state, follow the prompt's pointers into those
durable docs rather than expecting the rationale in `Where we are`.

### 3. Verify against current repo state

The prompt is a snapshot — reality has moved on. With mutate-style
heads, the snapshot's anchor is the prompt's `last_session` date
(plus any commit hashes called out in `Pointers`); diff against
those, not just the prior session.

Run in parallel:

```bash
git log --oneline <anchor-commit>..HEAD     # what landed since
git status --short                          # uncommitted drift
git branch -a | grep -v 'origin/HEAD'       # active branches
ls .claude/worktrees/ 2>/dev/null           # active worktrees (if used)
```

For each "next action" in the prompt, check:
- Are its file paths still present?
- Did any commit since the anchor already land it (partially)?
- Is its branch still alive?

Build a short **drift report** (3–5 bullets max) for the user.

**STOP if** drift is severe — multiple "next actions" already done,
infrastructure changed, branch deleted. Surface to user and ask
which thread they actually want.

### 4. Verify external pointers (when stakes are high)

Continuation prompts often name files, flags, or external
infrastructure that may have moved since. **Before recommending
action**, spot-check the load-bearing references:

- Path mentioned: `ls` it.
- Symbol/flag mentioned: `grep` for it.
- Service / host mentioned: quick reachability check.

This costs seconds, prevents wasted sessions.

### 5. Confirm next action with user

The prompt lists 3–5 next actions, prioritized but not strictly
dependent. **Don't pick yourself** — surface the list (with any
drift caveats) and ask which to tackle. The user knows their day's
intent; the prompt was written without that context.

Format the question with concrete options:

```
Continuation prompt "<slug>" lists 4 next actions:
  1. <action 1> — <one-line freshness check>
  2. <action 2> — <one-line freshness check>
  3. <action 3> — <one-line freshness check>
  4. <action 4> — <one-line freshness check>
Which one (or something else)?
```

Use `AskUserQuestion` if the options are mutually exclusive and the
user is at the terminal — otherwise prose works fine.

### 6. Stage the work

Once the action is chosen:
- Set up task tracking (TaskCreate) for the chosen action's substeps
- If the action implies a branch, create it (see `wrap-up-session` for
  conventions)
- Begin the work

For research-style "next actions" (no code), skip the branch — just
start.

## Quick reference

| Step | Always | Skip when |
|---|---|---|
| 1. Find prompt | Yes | — |
| 2. Read fully | Yes | — |
| 3. Verify against repo | Yes | — |
| 4. Verify external pointers | Only if stakes high | Action is pure research / discussion |
| 5. Confirm with user | Yes | — |
| 6. Stage work | Yes | User just wants a status report |

## Common mistakes

- **Skipping the verify step.** Continuation prompts decay. A "next
  action" written 3 days ago may already be in a merged PR. Always
  diff prompt-anchor vs current main.
- **Reading only "What's next".** The "Open questions" and "Where we
  are" sections often shift sequencing — read the whole prompt.
- **Picking the action yourself.** The prompt's priority order is
  the previous session's best guess; the user's intent today may
  differ. Always ask.
- **Treating the prompt as gospel.** If the prompt says to run a
  specific command (`mytool foo --bar`), verify the command and flags
  still exist before suggesting the user run them. Memory of a flag
  isn't the same as the flag.
- **Starting code work before confirming.** If you start
  implementing action #2 and the user wanted action #4, you've
  spent context for nothing.
- **Hardcoding a single location.** Different repos put continuation
  prompts in different places (`.plans/`, `docs/plans/`, custom
  paths). Always discover by filesystem first; only fall back to the
  `.plans/` default when nothing exists.
- **Treating "same slug, same file" as a stale prompt.** Mutate-
  style heads stay at the same path across sessions; `git log -p`
  on the prompt itself shows the history. Don't assume the
  `last_session` date being recent means a stale duplicate exists
  somewhere — it usually means the active head was updated in place
  last session.
- **Looking in the prompt for decision rationale.** Mutate-style
  prompts intentionally promote decisions and gotchas out to the
  spec / AGENTS.md / code comments. If the user asks "why did we
  choose X?", follow the prompt's pointers into the durable docs
  rather than re-reading `Where we are` for an explanation that
  isn't there.
- **Resuming from a `status: superseded` prompt.** Superseded files
  are kept for history (archive dir) — they don't reflect current
  state. Always walk `superseded_by` forward to the chain head before
  reading the "What's next" section.
- **Resuming from a `status: shipped` head without confirming.**
  Shipped = work done, no follow-on prompt written. The next session
  might be a fresh thread or might want to extend the shipped one —
  ask before assuming.
