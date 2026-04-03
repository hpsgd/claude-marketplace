---
name: propose-improvement
description: "Propose a change to the marketplace repo based on learned patterns — new rules, updated skills, evolved regex patterns. Creates a branch, applies changes, shows diff for review, and raises a PR on approval. Use when patterns have enough evidence to share upstream."
argument-hint: "[pattern-id, 'all' to review all pending patterns, or describe the change]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Propose Improvement

Stage a change to the marketplace repo based on $ARGUMENTS. This skill handles the full Path 2 workflow: find the repo, create a branch, apply changes, review with the user, and raise a PR.

## Step 1: Locate the marketplace repo

Read the marketplace source path from settings:

```bash
python3 -c "
import json, os
for f in [os.path.expanduser('~/.claude/settings.json'), '.claude/settings.json', '.claude/settings.local.json']:
    try:
        d = json.load(open(f))
        mkts = d.get('extraKnownMarketplaces', {})
        for name, cfg in mkts.items():
            src = cfg.get('source', {})
            path = src.get('path', '')
            if path and os.path.isdir(path):
                print(f'{name}={path}')
    except: pass
"
```

Verify the path is a git repo with the expected structure:

```bash
cd <marketplace-path>
git status
ls plugins/
```

If the marketplace repo is the current working directory (we're already in it), just use `.`.

**Output:** Confirmed marketplace repo path.

## Step 2: Identify what to propose

### From a pattern ID

Read the pattern file from `.claude/learnings/patterns/{pattern-id}.json` or `~/.claude/learnings/patterns/`.

Check:
- `count` >= 3 (minimum for a proposal)
- `status` is `detected` or `pending_review` (not already submitted)
- Evidence is sufficient (multiple sessions, clear common thread)

### From a learned rule

If the user has a local learned rule (`.claude/rules/learned--{topic}.md`) that they want to upstream:
- Read the rule content
- Determine which marketplace plugin it belongs to
- Prepare to move it from a local learned rule to a marketplace rule

### From a direct description

If the user describes the change directly, skip the pattern lookup and proceed to Step 3.

**Output:** The proposed change: what, where, why, and evidence.

## Step 3: Determine the target file

Map the learning to a marketplace file:

| Learning type | Target in marketplace |
|---|---|
| New rule (process/convention) | `plugins/{category}/{agent}/rules/{topic}.md` |
| Skill update (methodology change) | `plugins/{category}/{agent}/skills/{skill}/SKILL.md` |
| Agent update (responsibility change) | `plugins/{category}/{agent}/agents/{agent}.md` |
| Regex pattern evolution | `scripts/classify-message.py` or `scripts/analyse-session.py` |
| Template improvement | `plugins/{category}/{agent}/templates/{template}.md` |
| Cross-cutting rule | `plugins/practices/coding-standards/rules/{topic}.md` |

Read the current version of the target file in the marketplace repo to understand what exists.

**Output:** Target file path + current content summary.

## Step 4: Create branch and apply changes

```bash
cd <marketplace-path>

# Ensure we're on a clean main branch
git fetch origin
git checkout main
git pull --ff-only

# Create the proposal branch
BRANCH="learning/$(echo '{topic}' | tr ' ' '-' | tr '[:upper:]' '[:lower:]')"
git checkout -b "$BRANCH"
```

Apply the change. Depending on type:

### New rule file
Write the complete rule file using `Write`. Follow the existing rule format (YAML frontmatter with `description`, markdown body with imperatives).

### Skill/agent edit
Use `Edit` to modify the specific section. Keep changes minimal — only add what the learning requires.

### Regex pattern update
Read the current seed patterns in the script, add the new patterns to the appropriate list. Use `Edit`.

**Output:** Files modified on the branch.

## Step 5: Show diff for review (mandatory — never skip)

```bash
cd <marketplace-path>
git diff --stat
git diff
```

Present the diff to the user with context:

```markdown
### Proposed change: [title]

**Branch:** `learning/{topic}`
**Pattern:** [pattern-id] — [N] instances across [M] sessions
**Evidence:**
- [session date]: [correction summary]
- [session date]: [correction summary]
- [session date]: [correction summary]

**Files changed:**
[git diff --stat output]

**Diff:**
[git diff output — or summarise if large]

**Local rule:** `.claude/rules/learned--{topic}.md` has been active since [date]

Approve and create PR? (Y/n/edit)
```

If the user says **edit**: let them modify the changes, then re-show the diff.
If the user says **no**: discard the branch (`git checkout main && git branch -D learning/{topic}`).
If the user says **yes**: proceed to Step 6.

**Output:** Diff presented, user decision captured.

## Step 6: Commit, push, and create PR

```bash
cd <marketplace-path>

# Stage and commit
git add <changed-files>
git commit -m "$(cat <<'COMMITEOF'
feat: learned rule — {topic}

Pattern observed {N} times across {M} sessions.
Local rule has been active since {date}.

Evidence:
- {session1}: {summary}
- {session2}: {summary}
- {session3}: {summary}

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
COMMITEOF
)"

# Push
git push -u origin "learning/{topic}"

# Create PR
gh pr create \
  --title "Learning: {topic}" \
  --body "$(cat <<'PREOF'
## Summary

Proposed by the learning system based on observed patterns.

**Pattern:** {description}
**Instances:** {N} across {M} sessions
**First seen:** {date} | **Last seen:** {date}
**Local rule:** Active as `.claude/rules/learned--{topic}.md` since {date}

## Evidence

| Session | Date | Correction |
|---|---|---|
| {id} | {date} | {summary} |

## Change

{what changed and why}

---
🤖 Generated by `/thinking:propose-improvement`
PREOF
)"

# Return to main
git checkout main
```

**Output:** PR URL.

## Step 7: Update tracking

After the PR is created:

1. Update the pattern file (`.claude/learnings/patterns/{pattern-id}.json`):
   ```json
   {
     "status": "pr_submitted",
     "pr_url": "https://github.com/...",
     "pr_submitted_at": "2026-04-03T..."
   }
   ```

2. Add a note to the local learned rule:
   ```markdown
   <!-- Upstream PR: {pr_url} — remove this rule after PR is merged -->
   ```

3. Log the proposal in `.claude/learnings/proposals/`:
   ```json
   {
     "pattern_id": "pat-...",
     "pr_url": "...",
     "branch": "learning/...",
     "files_changed": [...],
     "submitted_at": "...",
     "status": "open"
   }
   ```

**Output:** Tracking updated, PR URL confirmed.

## Rules

- **Never push without user approval.** Step 5 (diff review) is mandatory. The user must see exactly what will be proposed before anything is pushed.
- **One change per PR.** Each pattern or learned rule gets its own branch and PR. Don't bundle unrelated changes.
- **Evidence is mandatory.** Every PR must include the session IDs and correction summaries that justify the change. A rule without evidence is an opinion.
- **Minimal changes.** Only modify what the learning requires. Don't refactor surrounding code or "improve" adjacent content.
- **Clean branch hygiene.** Always branch from a fresh `main`. Delete the branch locally after PR creation. If the PR is rejected, note the reason in the pattern file.
- **Local rule stays until merge.** The `.claude/rules/learned--*.md` file remains active locally until the upstream PR is merged. Don't remove it prematurely — it's the safety net.
- **Return to main.** Always `git checkout main` at the end, regardless of outcome. Never leave the marketplace repo on a feature branch.

## Output Format

```markdown
## Improvement Proposed: [title]

**PR:** [url]
**Branch:** `learning/{topic}`
**Pattern:** {N} instances across {M} sessions
**Files changed:** [count]
**Status:** PR submitted — awaiting review

### Next steps
1. Review the PR on GitHub
2. If merged, run `/thinking:retrospective` to clean up the local learned rule
3. The marketplace update will take effect on next plugin cache refresh
```

## Related Skills

- `/thinking:retrospective` — identifies patterns and proposes changes. This skill executes the proposal.
- `/thinking:learning` — captures individual learnings. Patterns emerge from accumulated learnings.
