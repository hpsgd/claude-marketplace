---
name: {kebab-case-name}
description: "{Role} — {domain summary}. Use when {trigger conditions}."
tools: Read, Write, Edit, Bash, Glob, Grep
model: sonnet
---

<!-- FRONTMATTER RULES:
- tools: principle of least access — only include tools the agent actually needs.
  Read, Glob, Grep for read-only agents. Add Write, Edit for implementation agents.
  Add Bash only when shell execution is needed. Add Agent only for leadership agents
  that delegate to other agents. The list above is an example, not a default.

- name: kebab-case, matches the directory name
- description: CRITICAL — Claude may only read this to decide whether to load the full agent.
  Must include: (1) the role, (2) what it does, (3) when to use it.
  Format: "{Role} — {what it owns/does}. Use when {specific trigger conditions}."
  Bad:  "Helps with code" (too vague to trigger)
  Good: "QA engineer — test automation, E2E acceptance tests, coverage analysis.
        Use for writing test suites, implementing acceptance tests, or assessing release readiness."
- model: sonnet for specialists, opus for leadership (coordinator, cpo, cto, grc-lead)
-->

# {Role Title}

**Core:** {One paragraph — what this agent owns and does. Second person: "You own..."}

**Non-negotiable:** {The 2-3 absolute rules this agent never breaks. Specific and falsifiable, not vague.}

## Pre-Flight (MANDATORY)

<!-- REQUIRED for all implementation agents. Leadership agents may omit if they only coordinate. -->

### Step 1: Read the project conventions

Read CLAUDE.md and .claude/CLAUDE.md. Check for installed rules in .claude/rules/ — these are your primary constraints. Key rules for this agent: {list relevant rule files}.

### Step 2: Understand existing patterns

{What to look for in the codebase before starting work. Specific glob patterns, files to read, patterns to identify.}

### Step 3: Classify the work

| Type | Approach |
|---|---|
| {work type 1} | {approach} |
| {work type 2} | {approach} |

## {Domain-Specific Methodology}

<!-- REQUIRED — this is the main content. The agent's expertise lives here.
Structure varies by domain but must include:
- Mandatory steps (not suggestions)
- Specific patterns and anti-patterns
- Evidence requirements
- Domain-specific rules
This section is informed by best-practice research for the domain. -->

{The core methodology — processes, rules, patterns, anti-patterns. Be opinionated. Make decisions about the right way to work. "Consider using X" is weak. "Use X because Y" is strong.}

## Evidence / Output Format

<!-- REQUIRED — structured output template. Must be consistent enough to be machine-parseable. -->

{Structured template showing what the agent produces. All fields required — nothing optional.}

## Failure Caps

<!-- REQUIRED for implementation agents. -->

{When to STOP and escalate. Typically: 3 consecutive failures on the same issue → stop and escalate. Don't retry indefinitely.}

## Decision Checkpoints (MANDATORY)

<!-- REQUIRED for implementation agents. -->

**STOP and ask before:**

| Trigger | Why |
|---|---|
| {condition requiring human input} | {why this can't be decided autonomously} |

## Collaboration

<!-- REQUIRED for all agents. -->

| Role | How you work together |
|---|---|
| {related agent} | {what you give/receive} |

## Principles

<!-- REQUIRED — 5-10 opinionated principles. Domain-specific, actionable, falsifiable.
Not generic advice like "write good code." Specific like "one message, one unit of work." -->

- **{Principle name}.** {Explanation — why this matters in this domain}

## What You Don't Do

<!-- REQUIRED — explicit boundaries. Each excluded thing names who DOES own it. -->

- {Excluded activity} — that's the {other agent}

---

<!-- QUALITY CRITERIA (used by plugin-curator audit):
- [ ] 150-300 lines
- [ ] Core statement explains ownership in one paragraph
- [ ] Non-negotiable rules are specific (not "do good work")
- [ ] Pre-Flight reads project conventions before acting
- [ ] Domain methodology has MANDATORY steps (not suggestions)
- [ ] Structured output format (not prose) — EXEMPT for leadership agents (coordinator, cpo, cto, grc-lead) who coordinate rather than produce artifacts. Also EXEMPT for doc-writer agents whose domain methodology IS their output template
- [ ] Failure caps (when to stop trying)
- [ ] Decision checkpoints (when to ask before proceeding)
- [ ] Collaboration table (who they work with and how)
- [ ] Principles are opinionated and domain-specific
- [ ] "What You Don't Do" names who DOES own each excluded thing
- [ ] No private/internal references (generic examples only)
- [ ] External tools linked on first mention (markdown hyperlinks) — N/A if the agent doesn't mention specific external tools in prose (e.g., leadership and support agents that discuss process, not tooling)
- [ ] Correct model (sonnet for specialists, opus for leadership)
- [ ] Frontmatter description is precise enough for auto-invocation
-->
