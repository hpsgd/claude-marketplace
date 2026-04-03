---
name: retrospective
description: "Analyse a session transcript for learnings — corrections, reversals, approach changes, and successes. Runs automatically on SessionStart for the previous session. Invoke manually to analyse the current session or review accumulated learnings."
argument-hint: "[session-id, 'current', 'summary', or 'patterns']"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Retrospective

Analyse conversation transcripts to extract learnings. Use `$ARGUMENTS` to control what to analyse:

- **`current`** — analyse the current session's transcript so far
- **`summary`** — review all accumulated learnings and show metrics
- **`patterns`** — detect recurring patterns across sessions (3+ instances)
- **`{session-id}`** — analyse a specific past session

This skill is also triggered automatically by the SessionStart hook, which analyses the most recent completed session.

## Step 1: Locate transcript

```bash
# Find the project's transcript directory
PROJECT_HASH=$(echo "$PWD" | sed 's|^/||; s|/|-|g')
TRANSCRIPT_DIR="$HOME/.claude/projects/-$PROJECT_HASH"
```

For `current`: find the most recently modified `.jsonl` file in `$TRANSCRIPT_DIR`.
For a specific session: look for `$TRANSCRIPT_DIR/{session-id}.jsonl`.
For `summary` or `patterns`: skip to Step 3 or Step 4.

**Output:** Path to the transcript file, or list of available sessions.

## Step 2: Run analysis (mandatory for session analysis)

Run the analysis script:

```bash
python3 scripts/analyse-session.py <transcript.jsonl> \
    --project-dir .claude/learnings \
    --global-dir ~/.claude/learnings \
    --json
```

The script outputs structured JSON with:
- **metrics**: turns, corrections, reversals, successes, correction rate, tokens
- **events**: each correction, reversal, or success with context and timestamps
- **files_modified**: which files were touched and how many times

Read the JSON output and present the results.

**Output:** Metrics summary table and event list.

## Step 3: Classify queued signals (mandatory)

The `UserPromptSubmit` hook captures every user message and classifies obvious cases via regex. Messages that are ambiguous are queued as `"type": "unclassified"` in `.claude/learnings/signals/pending.jsonl`.

Read the pending signals file:

```bash
cat .claude/learnings/signals/pending.jsonl
```

For each `unclassified` signal, read the `prompt_preview` and classify it yourself:
- **correction** (rating 2-4): user is correcting, rejecting, or redirecting your work
- **frustration** (rating 1-3): user is expressing dissatisfaction
- **praise** (rating 8-10): user is expressing approval
- **direction** (rating 5-6): user is giving new instructions (neutral, not correcting)
- **neutral** (rating 5-7): none of the above

Update the signal's `type` and `rating` fields, and set `confidence` to `"claude"`. Write the updated signals back.

This is why the system doesn't need an external AI API — you ARE the AI doing the classification.

### Update the regex patterns (mandatory after classifying)

For each message you classified that the regex missed, **extract a pattern that would catch similar messages in the future** and add it to `.claude/learnings/signals/patterns.json`.

The patterns file has this structure:

```json
{
  "correction": ["\\bfeels (arbitrary|wrong|off)\\b", "\\bunderestimating\\b"],
  "praise": [],
  "approach_change": ["\\bi think (we|you) should\\b"],
  "not_correction": []
}
```

For each unclassified message you classified:
1. Identify the **key phrase** that signals the intent (e.g., "feels arbitrary" → correction)
2. Write a regex pattern that would match it and similar phrasings
3. Test the pattern mentally against a few examples — would it false-positive on normal instructions?
4. If the pattern is safe (low false-positive risk), add it to the appropriate category

Read the existing `patterns.json` (create if missing), append new patterns, and write it back. The `classify-message.py` script loads this file on every run, so new patterns take effect immediately.

**Rules for pattern generation:**
- Patterns must be **general enough** to catch variations but **specific enough** to avoid false positives
- `\bfeels (arbitrary|wrong|off|unnecessary)\b` is good — catches a class of pushback
- `\bfeels\b` alone is too broad — would match "it feels responsive"
- Always use `\b` word boundaries to prevent partial matches
- Test against the original message AND imagine 3 other messages — would they match correctly?

**Output:** Classified signal count by type + number of new patterns added.

## Step 4: Interpret and write learnings (mandatory)

For each event extracted by the script AND each classified signal, interpret it into a learning:

### For corrections (HIGH severity):

Ask: *What did the assistant do wrong, and what should it do differently?*

```markdown
### Learning: [short title]

**Type:** immediate_correction
**What happened:** [assistant did X]
**What was wrong:** [why X was incorrect — the user's actual intent was Y]
**Rule:** [imperative statement — "Always X" or "Never Y"]
**Scope:** [universal — applies to all projects | project-specific — only this codebase]
```

### For reversals (MEDIUM severity):

Ask: *Was this a genuine mistake that was corrected, or normal iterative refinement?*

Files touched 3+ times are flagged, but not all are problems. A file edited 5 times during a planned multi-pass refactor is normal. A file written then immediately rewritten with a different approach is a reversal.

Check `git log` for the file to distinguish iterative refinement from reversals.

### For successes (POSITIVE):

Ask: *What did the assistant do right that should be reinforced?*

Only record successes that are non-obvious — approaches that worked but might not be the default choice. "Wrote code that compiled" is not worth recording. "Used a single bundled PR instead of splitting, and the user confirmed that was the right call" is.

**Output:** Classified learnings with rules and scope.

## Step 5: Check for patterns (mandatory for `patterns` mode)

Read all session analysis files from `.claude/learnings/sessions/` and `~/.claude/learnings/sessions/`.

```bash
# Count learnings by type across all sessions
find .claude/learnings/sessions ~/.claude/learnings/sessions -name '*.json' 2>/dev/null
```

For each learning type, count occurrences across sessions. When the same kind of correction appears 3+ times:

```markdown
### Pattern detected: [name]

**Instances:** [count] across [N] sessions
**First seen:** [date]
**Last seen:** [date]
**Common thread:** [what these corrections have in common]
**Proposed rule:** [imperative statement that would prevent recurrence]
**Target:** [which rule file or agent to update]
**Status:** pending_review
```

Save the pattern to `.claude/learnings/patterns/{pattern-id}.json`.

**Output:** Pattern table with proposed changes.

## Step 6: Propose changes (when patterns reach threshold)

When a pattern has 5+ instances OR the user approves a 3+ instance pattern:

1. Draft the proposed change (new rule, agent modification, or skill update)
2. Show the change to the user with the evidence (which sessions, which corrections)
3. If approved, create a PR branch and apply the change
4. Include metrics in the PR description

```markdown
### Proposed change

**Pattern:** [name] (observed [N] times across [M] sessions)
**Change type:** [new rule | rule update | agent update | skill update]
**Target file:** [path]
**Evidence:** [list of session IDs and correction summaries]

**Proposed content:**
[the actual rule/change to add]
```

**Output:** Proposed change with evidence, ready for user approval.

## Rules

- **The script does extraction, you do interpretation.** The Python script (`analyse-session.py`) handles JSONL parsing and pattern matching. This skill reads the structured output and applies judgment — classifying scope, filtering noise, detecting patterns.
- **Not every reversal is a mistake.** Files touched 3+ times during a planned multi-pass operation are normal iterative refinement. Check the context before flagging.
- **Not every correction is a learning.** "No, use tabs not spaces" in a project with a `.editorconfig` is a config issue, not a learning. Only record corrections that reveal a gap in understanding or process.
- **Universal vs project-specific.** "Don't declare completion without running the audit" is universal. "The config file is at `src/config.ts` not `config/index.ts`" is project-specific. Classify correctly — universal learnings go to `~/.claude/learnings/`, project-specific to `.claude/learnings/`.
- **Patterns are more valuable than incidents.** One correction is an event. Three corrections about the same thing are a pattern. Patterns become rules.
- **Never record user-specific information.** Learnings capture what went wrong and how to fix it, not personal details about the user.
- **The 1-hour rule.** The SessionStart hook analyses the previous session, which gives at least a session-gap delay. This is intentional — it allows delayed corrections (where the user realises later something was wrong) to be captured in the same transcript.

## Output Format

### Session analysis:
```markdown
## Retrospective: [session-id]

### Metrics
| Metric | Value |
|---|---|
| Duration | [N] minutes |
| Turns | [N] user / [N] assistant |
| Corrections | [N] immediate, [N] approach changes, [N] reversals |
| Successes | [N] |
| Correction rate | [N]% |

### Learnings
| # | Type | Severity | Rule | Scope |
|---|---|---|---|---|
| 1 | [type] | [sev] | [rule] | [scope] |

### Patterns
[Any patterns detected from accumulated data]
```

### Summary mode:
```markdown
## Learning Summary

### Totals (across [N] sessions)
| Metric | Value |
|---|---|
| Sessions analysed | [N] |
| Total corrections | [N] |
| Total successes | [N] |
| Active patterns | [N] |
| Pending proposals | [N] |

### Top patterns
| Pattern | Count | Proposed change | Status |
|---|---|---|---|
```

## Related Skills

- `/thinking:learning` — capture individual learnings in the moment. Retrospective analyses transcripts after the fact.
- `/thinking:wisdom` — when patterns crystallise (85%+ confidence), promote them to wisdom frames.
- `/thinking:health-check` — audits the learning system's coverage as part of project health.
