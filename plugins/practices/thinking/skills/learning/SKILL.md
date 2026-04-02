---
name: learning
description: Capture, categorise, and recall learnings from work sessions. Use after completing work, when something unexpected happens, or when explicitly asked to remember something.
argument-hint: "[learning to capture, or 'recall' to review recent learnings]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Capture or recall learnings. Use `$ARGUMENTS` to either record a new learning or review existing ones.

## Capturing a Learning

When something noteworthy happens — a correction, a surprising outcome, a pattern discovered, a mistake made — capture it structured:

### 1. Classify the learning

- **SYSTEM**: Infrastructure, tooling, configuration, environment issues. Things about how the system works.
- **METHOD**: Approach, technique, process improvements. Things about how to do the work.
- **DOMAIN**: Business logic, domain knowledge, project-specific insights. Things about what the work is about.
- **FEEDBACK**: Direct corrections or preferences from the user. Things about how the user wants to work.

### 2. Write the learning

Save to the project's memory system. Each learning should include:

```markdown
---
name: [short descriptive name]
description: [one-line summary for index matching]
type: feedback
---

[What happened — the specific situation]

**Learning:** [The insight or rule extracted from it]

**Why:** [Why this matters — what goes wrong if ignored]

**How to apply:** [When and where to apply this in future]
```

### 3. Rate severity

- **Critical**: Caused visible damage, data loss, or significant rework. Must not happen again.
- **Important**: Wasted time or produced wrong output. Should be avoided.
- **Minor**: Suboptimal but not harmful. Nice to improve.

## Failure Capture

When something goes notably wrong (the user is frustrated, work needs to be redone, or a significant mistake was made):

1. **What happened**: The specific failure, not a general category
2. **Root cause**: Why it happened — the actual reason, not symptoms
3. **What was tried**: What approaches were attempted
4. **What worked**: The eventual fix or resolution
5. **Prevention**: What rule or check would prevent recurrence

Save as a learning with type `feedback` and critical severity.

## Recalling Learnings

When asked to recall, or at the start of work that relates to past learnings:

1. Check the project's memory directory for relevant learnings
2. Check for patterns — are there multiple learnings about the same topic?
3. Present relevant learnings concisely — the rule and why, not the full story

## Pattern Synthesis

When there are 5+ learnings in a category, look for patterns:

- **Recurring frustrations**: What keeps going wrong? What's the common root cause?
- **Recurring successes**: What approach keeps working? Can it be generalised?
- **Contradictions**: Are there learnings that conflict? Which is more recent / better evidenced?

Present patterns as potential rules to add to the project's configuration.

When patterns crystallise into high-confidence principles, use the `/wisdom` skill to record them as wisdom frames for cross-domain synthesis.
