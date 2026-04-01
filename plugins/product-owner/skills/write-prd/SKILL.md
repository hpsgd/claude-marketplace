---
name: write-prd
description: Write a Product Requirements Document from rough notes or a feature idea. Produces a structured PRD with problem statement, user stories, acceptance criteria, and scope.
argument-hint: "[feature idea or rough notes]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Write a PRD for $ARGUMENTS.

## PRD Structure

### 1. Problem Statement
- What problem are we solving?
- Who has this problem?
- How do they solve it today?
- Why is the current solution inadequate?

### 2. Target User
- Who specifically is this for? (not "everyone")
- What's their context when they encounter the problem?
- What's their technical sophistication?

### 3. Success Metrics
- How will we know this succeeded?
- Leading indicators (can measure immediately)
- Lagging indicators (measure over time)
- What does failure look like?

### 4. User Stories
For each story:
```
As a [user type], I want [action] so that [outcome].

Acceptance criteria:
- [ ] [Verifiable criterion 1]
- [ ] [Verifiable criterion 2]
```

Apply the ISC Splitting Test to every acceptance criterion — each must be independently verifiable.

### 5. Scope
- **In scope**: What's included in this release
- **Out of scope**: What's deliberately deferred (and why)
- **Anti-requirements**: What we're explicitly NOT doing

### 6. Edge Cases and Open Questions
- What happens in unusual scenarios?
- What decisions still need to be made?
- What assumptions are we making that might be wrong?

### 7. Technical Notes (optional)
- Any known technical constraints
- Dependencies on other systems or teams
- Suggested approach (if the author has one) — clearly marked as suggestion, not requirement

## Output

Write the PRD to a file. Suggest a filename based on the feature: `docs/prd-[feature-name].md`
