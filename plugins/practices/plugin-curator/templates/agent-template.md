# Agent Definition Template

Every agent in this marketplace follows this structure. Sections marked REQUIRED must be present. Sections marked CONDITIONAL are included when applicable.

---

```markdown
---
name: {kebab-case-name}
description: "{Role} — {domain summary}. Use when {trigger conditions}."
tools: Read, Write, Edit, Bash, Glob, Grep
model: sonnet  # sonnet for specialists, opus for leadership (coordinator, cpo, cto, grc-lead)
---

# {Role Title}

**Core:** {One paragraph — what this agent owns and does. Written in second person ("You own...")}

**Non-negotiable:** {The 2-3 absolute rules this agent never breaks. Specific, not vague.}

## Pre-Flight (MANDATORY)                                    [REQUIRED for implementation agents]

### Step 1: Read the project conventions

```
Read(file_path="CLAUDE.md")
Read(file_path=".claude/CLAUDE.md")
```

Check for installed rules in `.claude/rules/` — these are your primary constraints.
Key rules for this agent: `{relevant-rule-1}`, `{relevant-rule-2}`.

### Step 2: Understand existing patterns

{Agent-specific: what to look for in the codebase before starting work}

### Step 3: Classify the work

| Type | Approach |
|---|---|
| {work type 1} | {approach} |
| {work type 2} | {approach} |

## {Domain-Specific Methodology}                             [REQUIRED — the main content]

{The core of the agent — processes, rules, patterns, anti-patterns.
This is where the agent's expertise lives. Structure varies by domain
but should include mandatory steps, not suggestions.}

## Evidence / Output Format                                   [REQUIRED]

{Structured output template showing what the agent produces.
Should be consistent enough to be machine-parseable.
Include all required fields — nothing optional in the output.}

## Failure Caps                                               [REQUIRED for implementation agents]

{When to STOP and escalate rather than continue trying.
Typically: 3 consecutive failures on the same issue → stop.}

## Decision Checkpoints (MANDATORY)                           [REQUIRED for implementation agents]

**STOP and ask before:**

| Trigger | Why |
|---|---|
| {condition that requires human input} | {why this can't be decided autonomously} |

## Collaboration                                              [REQUIRED]

| Role | How you work together |
|---|---|
| {related agent} | {what you give/receive} |

## Principles                                                 [REQUIRED]

{5-10 opinionated principles. Not generic advice — specific to this domain.
Each principle should be actionable and falsifiable.}

## What You Don't Do                                          [REQUIRED]

{Explicit boundaries. What this agent leaves to others.
Each item names the agent who DOES own it.}
```

## Quality Criteria for Agent Definitions

A well-written agent definition:

- [ ] Is 150-300 lines (not a stub, not a novel)
- [ ] Has a clear Core statement that explains ownership in one paragraph
- [ ] Has Non-negotiable rules that are specific (not "do good work")
- [ ] Has Pre-Flight steps that read project conventions before acting
- [ ] Has domain methodology with MANDATORY steps (not suggestions)
- [ ] Has a structured Output Format (not prose)
- [ ] Has Failure Caps (when to stop trying)
- [ ] Has Decision Checkpoints (when to ask before proceeding)
- [ ] Has a Collaboration table (who they work with and how)
- [ ] Has Principles that are opinionated and domain-specific
- [ ] Has "What You Don't Do" that names who DOES own each excluded thing
- [ ] Uses no private/internal references (generic examples only)
- [ ] Links external tools/frameworks on first mention (markdown hyperlinks)
- [ ] Uses `model: sonnet` for specialists, `model: opus` for leadership
