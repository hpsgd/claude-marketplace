---
name: write-adr
description: Write an Architecture Decision Record. Captures the context, options considered, decision made, and consequences for a significant technical decision.
argument-hint: "[technical decision to document]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Write an ADR for $ARGUMENTS.

## ADR Structure

```markdown
# ADR-NNN: [Decision Title]

**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-NNN
**Date:** YYYY-MM-DD
**Deciders:** [who was involved]

## Context

What is the situation that requires a decision? What forces are at play?
Include technical constraints, business constraints, and team constraints.

## Options Considered

### Option 1: [Name]
- Description
- **Pros:** ...
- **Cons:** ...
- **Effort:** ...

### Option 2: [Name]
- Description
- **Pros:** ...
- **Cons:** ...
- **Effort:** ...

### Option 3: [Name] (if applicable)
...

## Decision

We chose **Option N** because [reasoning].

The key factors were:
1. [Most important reason]
2. [Second reason]
3. [Third reason]

## Consequences

### Positive
- [What gets better]

### Negative
- [What gets worse or harder]
- [What technical debt is accepted]

### Risks
- [What could go wrong with this decision]
- [What would trigger reconsideration]
```

## Guidelines

- Write ADRs for decisions that affect the system's future — not for trivial choices
- Include options you rejected and why — future readers need to understand the trade-offs
- Be honest about consequences — every decision has downsides
- Link to related ADRs when a decision builds on or supersedes another
- Keep them short — one page is ideal, two is the maximum

## Output

Write to `docs/adr/` or the project's ADR directory. Number sequentially.
