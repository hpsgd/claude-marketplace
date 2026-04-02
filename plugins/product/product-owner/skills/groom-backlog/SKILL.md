---
name: groom-backlog
description: Review and groom a backlog — classify items by readiness, break large items into deliverables, add acceptance criteria, RICE-score, and recommend actions.
argument-hint: "[path to backlog file, or 'current' to scan for issues/todos]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Groom the backlog at $ARGUMENTS.

Follow every step below in order. Do not skip steps.

---

## Step 1: Locate and Ingest the Backlog

If the argument is a file path, read it. If the argument is "current" or a directory:
1. Search for issue trackers: `grep -r "TODO\|FIXME\|HACK\|XXX"` across the codebase
2. Look for backlog files: `*.md` files containing "backlog", "roadmap", "issues", or "tasks"
3. Check for GitHub issues if a `.git` remote is configured: parse `git remote -v`

Collect every backlog item into a working list. Each item needs: title, description (if available), current status, last activity date, any existing priority or labels.

---

## Step 2: Audit and Classify Every Item

Classify each item into exactly one of four categories. Apply these criteria strictly — do not give items the benefit of the doubt.

### Ready
All of the following must be true:
- Has specific, verifiable acceptance criteria (not just a title)
- Is small enough to complete in one sprint (1-2 weeks of focused work)
- Dependencies are identified and either resolved or have a clear path to resolution
- The "why" is clear — you can explain who benefits and how
- No open questions that would block implementation

### Needs Refinement
Any of the following is true:
- Title only, no description or acceptance criteria
- Too large: involves multiple independent deliverables bundled together
- Vague acceptance criteria ("should work well", "needs to be fast")
- Missing information about who the user is or what the success criteria are
- Has unvalidated assumptions baked in

### Stale
Any of the following is true:
- No activity or discussion in 30+ days AND no one has asked for it
- The problem it describes has been solved by other work
- The context has changed enough that the original framing is no longer relevant
- It was a speculative idea that never gained traction
- It references systems, APIs, or designs that no longer exist

### Blocked
All of the following are true:
- The item is otherwise well-defined (would be "Ready" if not blocked)
- There is a specific, identifiable blocker: a dependency on another team, an unanswered question from a stakeholder, a technical prerequisite that is not yet in place
- The blocker is not something the team can resolve unilaterally

**Anti-pattern**: Do not classify vague items as "Blocked." An item that says "Build analytics dashboard" with no further detail is "Needs Refinement," not "Blocked." Blocked means there is a specific external impediment.

---

## Step 3: Refine Items That Need It

For each item classified as "Needs Refinement," perform all applicable refinement actions:

### Break down large items
Apply the INVEST criteria:
- **I**ndependent: Can be delivered without other items
- **N**egotiable: The approach is flexible, the outcome is fixed
- **V**aluable: Delivers user-visible value on its own
- **E**stimable: Small enough to estimate with reasonable confidence
- **S**mall: Completable in one sprint
- **T**estable: Has verifiable acceptance criteria

If an item fails the "Small" or "Independent" test, split it. Each child item must independently deliver value — do not create items like "Build backend for X" and "Build frontend for X." Instead, split by user behaviour: "User can create X" and "User can filter X by date."

### Add acceptance criteria
Write acceptance criteria that pass the ISC Splitting Test:
- **Independent**: Each criterion is verifiable on its own
- **Small**: Each criterion tests one behaviour
- **Complete**: Each criterion specifies boundary conditions

### Identify dependencies
For each item, list:
- What must exist before this can start (prerequisite)
- What other items interact with this (related)
- What external teams or systems are involved (external dependency)

### Estimate size
Use t-shirt sizes based on complexity AND uncertainty:

| Size | Complexity | Uncertainty | Typical duration |
|------|-----------|-------------|-----------------|
| **S** | Well-understood, similar to past work | Low — we have done this before | 1-3 days |
| **M** | Moderate complexity, some new territory | Medium — some unknowns but manageable | 3-5 days |
| **L** | High complexity or significant new territory | High — meaningful unknowns to resolve | 1-2 weeks |
| **XL** | Too large — must be broken down | N/A | N/A — split this item |

Any item sized as XL must be broken down before it can be scheduled. This is not optional.

---

## Step 4: RICE Score Every Ready Item

Calculate a RICE score for every item classified as "Ready" (including items that were refined into "Ready" in Step 3).

### Scoring Guide

**Reach** — How many users/accounts will this affect per quarter?
- Use real numbers from analytics when available
- If estimating, state the assumption explicitly
- Count the number of users who will encounter the relevant workflow, not total users

**Impact** — How much does this improve the affected users' experience?
| Score | Meaning | Example |
|-------|---------|---------|
| 3 | Massive | Eliminates a multi-step manual process entirely |
| 2 | High | Significantly reduces time/effort for a common task |
| 1 | Medium | Noticeable improvement, users would appreciate it |
| 0.5 | Low | Minor convenience, nice-to-have |
| 0.25 | Minimal | Cosmetic or very edge-case improvement |

**Confidence** — How sure are we about the Reach and Impact estimates?
| Score | Meaning | Basis |
|-------|---------|-------|
| 100% | High | Direct user data, support ticket volume, analytics |
| 80% | Medium | User interviews, strong signals, analogous data |
| 50% | Low | Gut feel, untested hypothesis, no data |

**Effort** — Person-weeks across all disciplines (design + eng + QA)
- Include time for design, implementation, code review, QA, and deployment
- Round up to the nearest 0.5 weeks
- If uncertain, use the higher estimate

**Formula**: RICE = (Reach x Impact x Confidence) / Effort

### Interpretation
- Score > 10: Strong candidate for next sprint
- Score 5-10: Good candidate, schedule when capacity allows
- Score 1-5: Moderate value, consider batching with related work
- Score < 1: Question whether this is worth doing at all

---

## Step 5: Dependency Mapping

Create a dependency map showing which items block or are blocked by other items.

Format:
```
[Item A] --depends on--> [Item B]
[Item C] --depends on--> [Item A]
[Item D] (no dependencies — can start immediately)
```

Flag any dependency cycles — these indicate a scoping problem that needs to be resolved before scheduling.

---

## Step 6: Recommend Actions

Produce four lists:

### Schedule Next (prioritised)
Items that are Ready, ordered by RICE score descending. Include the RICE score and size estimate for each.

### Refine Before Scheduling
Items that need more work before they can be scheduled. For each, list the specific questions that need answers or the refinement that is needed.

### Recommend for Closure
Stale items with a one-sentence rationale for closing each. Be direct — "No activity in 90 days and the problem was addressed by [other item]" is sufficient.

### Blocked — Escalation Needed
Items that cannot proceed without external action. For each, state: who needs to act, what they need to do, and what the consequence of delay is.

---

## Output Format

Present the groomed backlog as a structured document:

```markdown
# Backlog Grooming Summary — [Date]

## Overview
- Total items reviewed: N
- Ready to schedule: N
- Needs refinement: N
- Recommended for closure: N
- Blocked: N

## 1. Schedule Next (by RICE priority)

| Priority | Item | RICE | Size | Dependencies | Notes |
|----------|------|------|------|-------------|-------|
| 1 | ... | 15.2 | S | None | ... |
| 2 | ... | 12.0 | M | Item 1 | ... |

## 2. Needs Refinement

| Item | Issue | Action needed |
|------|-------|--------------|
| ... | Missing AC | Write acceptance criteria; clarify scope with [owner] |

## 3. Recommended for Closure

| Item | Reason |
|------|--------|
| ... | Superseded by [other item], no activity since [date] |

## 4. Blocked — Escalation Needed

| Item | Blocker | Who | Impact of delay |
|------|---------|-----|----------------|
| ... | API contract not finalised | Platform team | Delays 3 downstream items |
```

Write the output to a file if the backlog is file-based. Otherwise, present it directly.
