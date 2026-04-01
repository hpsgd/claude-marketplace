---
name: groom-backlog
description: Review and groom a backlog — break large items into smaller deliverables, add missing acceptance criteria, remove stale items, and prioritise.
argument-hint: "[path to backlog file, or 'current' to scan for issues/todos]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Groom the backlog at $ARGUMENTS.

## Process

### 1. Audit current state

Read the backlog and classify each item:

- **Ready**: Has clear acceptance criteria, is small enough to deliver in one sprint, dependencies identified
- **Needs refinement**: Too vague, too large, missing acceptance criteria, or unclear priority
- **Stale**: No activity in 30+ days, no longer relevant, or superseded by other work
- **Blocked**: Has unresolved dependencies or open questions

### 2. Refine items that need it

For each item that needs refinement:
- Break large items into smaller, independently deliverable pieces
- Add acceptance criteria (applying the ISC Splitting Test)
- Identify dependencies and blockers
- Estimate relative size (S/M/L) based on complexity and uncertainty

### 3. Prioritise

Apply RICE scoring:
- **Reach**: How many users/sessions does this affect?
- **Impact**: How much does it improve the experience? (3 = massive, 2 = high, 1 = medium, 0.5 = low, 0.25 = minimal)
- **Confidence**: How sure are we about reach and impact? (100% = high, 80% = medium, 50% = low)
- **Effort**: Person-weeks of work

RICE score = (Reach × Impact × Confidence) / Effort

### 4. Recommend actions

- Items to schedule next (highest priority, ready)
- Items to refine before scheduling
- Items to close (stale or no longer relevant)
- Questions that need answers before items can proceed

## Output

Present as a groomed backlog summary:
1. **Ready to schedule** (prioritised list with RICE scores)
2. **Needs refinement** (with specific questions to answer)
3. **Recommended for closure** (with reasoning)
4. **Blocked** (with what's needed to unblock)
