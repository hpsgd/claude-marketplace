---
name: learning
description: "Capture, categorise, and recall learnings from work sessions. Use after completing work, when something unexpected happens, or when explicitly asked to remember something."
argument-hint: "[learning to capture, or 'recall' to review recent learnings]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Capture or recall learnings. Use `$ARGUMENTS` to either record a new learning or review existing ones.

## Step 1: Classify the learning (mandatory)

Determine the category:

| Category | What it covers | Example |
|---|---|---|
| **SYSTEM** | Infrastructure, tooling, configuration, environment | "The CI pipeline silently ignores test failures in the linting stage" |
| **METHOD** | Approach, technique, process improvements | "Splitting the PR into schema-first and logic-second reduced review time" |
| **DOMAIN** | Business logic, domain knowledge, project-specific insights | "Refunds must be processed within 14 days per the merchant agreement" |
| **FEEDBACK** | Direct corrections or preferences from the user | "User prefers single bundled PRs for refactors, not multiple small ones" |

**Output:** Category assignment with reasoning.

## Step 2: Write the learning (mandatory)

Save to the project's memory system using this exact format:

```markdown
---
name: [short-descriptive-name]
description: [one-line summary — specific enough for future matching]
type: feedback
---

[What happened — the specific situation that triggered this learning]

**Learning:** [The insight or rule extracted — stated as an imperative]

**Why:** [Why this matters — what goes wrong if ignored]

**How to apply:** [When and where to apply this in future work]

**Severity:** [Critical / Important / Minor]
**Category:** [SYSTEM / METHOD / DOMAIN / FEEDBACK]
```

**Rules for writing learnings:**
- The learning must be stated as a rule, not a narrative. "Always X when Y" not "I noticed that sometimes..."
- The "why" must explain the consequence of ignoring it, not just restate the learning
- "How to apply" must be specific enough that future-you can act on it without remembering the context

**Output:** Learning file written to memory.

## Step 3: Rate severity (mandatory)

| Severity | Criteria | Example |
|---|---|---|
| **Critical** | Caused visible damage, data loss, or significant rework. Must not happen again | "Force-pushed to main and lost 3 commits" |
| **Important** | Wasted significant time or produced wrong output. Should be avoided | "Spent 2 hours debugging a config issue that was documented in CLAUDE.md" |
| **Minor** | Suboptimal but not harmful. Nice to improve | "Could have used a glob pattern instead of manual file listing" |

**Output:** Severity rating with justification.

## Step 4: Failure capture (when applicable)

When something goes notably wrong (user frustration, rework needed, significant mistake), capture additional detail:

```markdown
### Failure Analysis

**What happened:** [specific failure — not a general category]
**Root cause:** [why it happened — the actual reason, not symptoms]
**What was tried:** [approaches attempted before resolution]
**What worked:** [the eventual fix or resolution]
**Prevention rule:** [what check or rule would prevent recurrence]
```

Save as a learning with `Critical` severity. The prevention rule is the most important field — it becomes a future guardrail.

**Output:** Failure analysis with prevention rule.

## Recalling Learnings

When asked to recall, or at the start of work that relates to past learnings:

1. Check the project's memory directory for relevant learnings
2. Filter by category if the task context is clear (e.g., SYSTEM learnings for infrastructure work)
3. Check for patterns — are there multiple learnings about the same topic?
4. Present relevant learnings concisely: **the rule and why**, not the full story

```markdown
### Relevant Learnings

| # | Learning | Category | Severity | Applied to current task? |
|---|---|---|---|---|
| 1 | [rule — imperative form] | [category] | [severity] | [Yes — how / No — why not] |
```

## Pattern Synthesis

When there are 5+ learnings in a category, synthesise patterns:

```markdown
### Pattern: [name]

**Observed in:** [count] learnings over [time period]
**Common root cause:** [what keeps causing this]
**Proposed rule:** [generalised imperative that would prevent recurrence]
**Confidence:** [High / Medium / Low — based on evidence count]
```

When patterns crystallise into high-confidence principles (85%+), promote them to wisdom frames using `/wisdom`.

## Rules

- **Capture immediately.** A learning recorded 5 minutes after the event is accurate. A learning recorded next week is fiction. Capture during or right after the work.
- **Rules, not narratives.** "Always validate schema changes against existing data before migrating" is a learning. "Today we had a problem with the schema" is a diary entry.
- **Severity must be honest.** Downgrading severity to avoid embarrassment defeats the purpose. If it caused rework, it's Important. If it caused data loss, it's Critical.
- **Never duplicate learnings.** Before saving, check if an existing learning covers the same ground. Update the existing one instead of creating a new file.
- **Patterns over incidents.** Five individual learnings about the same issue should be synthesised into one pattern. The pattern is more valuable than the incidents.
- **Privacy-aware recall.** When presenting learnings, share the rule and the why. Don't expose sensitive details from the original context unless asked.

## Output Format

### When capturing:
```markdown
## Learning Captured

**Name:** [short name]
**Category:** [SYSTEM/METHOD/DOMAIN/FEEDBACK]
**Severity:** [Critical/Important/Minor]
**Rule:** [the learning as an imperative]
**Saved to:** [file path]
```

### When recalling:
```markdown
## Relevant Learnings for [context]

| # | Rule | Category | Severity | Applies here? |
|---|---|---|---|---|
| 1 | [learning] | [cat] | [sev] | [yes/no + reason] |

### Patterns detected
[Any patterns from 5+ related learnings]
```

## Related Skills

- `/wisdom` — promote crystallised learnings (85%+ confidence patterns) to wisdom frames for cross-domain synthesis.
- `/health-check` — audit the learning system's coverage and identify blind spots.
