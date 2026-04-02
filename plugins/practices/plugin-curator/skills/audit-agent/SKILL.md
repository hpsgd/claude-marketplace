---
name: audit-agent
description: "Audit an agent definition against the standard template. Reports structural gaps with specific evidence for each finding."
argument-hint: "[agent name, or 'all' to audit every agent]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Audit $ARGUMENTS against the agent template quality criteria.

## Process (sequential — do not skip steps)

### Step 1: Read the template

```
Read(file_path="${CLAUDE_PLUGIN_ROOT}/templates/agent-template.md")
```

The template defines the MANDATORY structure. The quality criteria at the bottom of the template are the audit checklist.

### Step 2: Find the agent(s) to audit

If `$ARGUMENTS` is "all", find every agent:
```bash
find plugins -path '*/agents/*.md' -not -path '*/plugin-curator/*' | sort
```

Otherwise, locate the specific agent by name.

### Step 3: Evaluate each quality criterion

For EACH agent, check all 15 criteria. Score as ✅ (met), ⚠️ (partially met — with reason), or ❌ (missing).

**Criterion 1: Line count (150–300 lines)**

| Lines | Score |
|---|---|
| 150–300 | ✅ |
| 120–149 | ⚠️ Short — may lack depth |
| < 120 | ❌ Too short |
| > 300 | ⚠️ Long — consider extracting to skills |

**Criterion 2: Core statement**

First paragraph after the title. Must explain what the agent owns in one paragraph, using second person ("You own...").

| Quality | Score |
|---|---|
| Clear ownership statement, second person | ✅ |
| Present but vague or third person | ⚠️ |
| Missing | ❌ |

**Criterion 3: Non-negotiable rules**

Specific, falsifiable rules the agent never breaks. Not vague ("do good work") — specific ("Every AI feature has evaluation criteria BEFORE implementation").

**Criterion 4: Pre-Flight reads project conventions**

Must include Step 1 reading CLAUDE.md and .claude/CLAUDE.md and checking for installed rules.

**Criterion 5: Domain methodology has MANDATORY steps**

The core content section must have steps framed as mandatory, not suggestions.

**Criterion 6: Structured output format**

A template showing what the agent produces. All fields defined, copy-pasteable.

**Exemptions:**
- N/A for leadership agents (coordinator, cpo, cto, grc-lead) — they coordinate rather than produce artefacts
- N/A for doc-writer agents — their domain methodology IS their output template

**Criterion 7: Failure caps**

When to STOP and escalate. Standard: 3 consecutive failures → stop. 10 minutes without progress → stop.

**Criterion 8: Decision checkpoints**

Table of triggers where the agent must STOP and ask before proceeding.

**Criterion 9: Collaboration table**

Table showing who the agent works with and how.

**Criterion 10: Principles**

5–10 opinionated, domain-specific principles. Each has a bold name and explanation. Must be specific to this agent's domain, not generic advice.

**Criterion 11: "What You Don't Do"**

Explicit boundaries. Each excluded activity names who DOES own it.

**Criterion 12: No private/internal references**

No private company names, internal packages, proprietary tools, or project-specific details.

**Criterion 13: External tools linked**

Tool names mentioned in prose should have markdown hyperlinks on first mention.

**Exemptions:** N/A if the agent doesn't mention specific external tools in prose (e.g., leadership agents that discuss process, not tooling).

When marking down: cite the SPECIFIC unlinked tool mention with its line number. E.g., "Line 91: 'k6' mentioned without hyperlink".

**Criterion 14: Correct model**

| Agent type | Expected model |
|---|---|
| Leadership (coordinator, cpo, cto, grc-lead) | opus |
| Specialists (all others) | sonnet |

**Criterion 15: Frontmatter description precision**

The `description` field must include: (1) the role, (2) what it does, (3) when to use it. Format: "{Role} — {what it owns}. Use when {triggers}."

### Step 4: Evidence requirements

**Every non-passing criterion MUST include:**
1. What was looked for (the criterion)
2. What was found or not found (the specific evidence)
3. Where it was found or expected (file location, line number if applicable)

For the links criterion specifically: list EACH unlinked tool mention with its line number.

### Step 5: Produce the report

**Single agent audit** — full 15-criterion detail.

**"All" audit** — summary table first, then detail for non-passing agents only.

## Anti-Patterns (NEVER do these)

- **Vague findings** — "links need work" is not a finding. "Line 91: 'k6' mentioned without hyperlink" is a finding
- **Passing without evidence** — every ✅ should be verifiable. "Pre-Flight: ✅ — reads CLAUDE.md at line 18" not just "✅"
- **Applying exemptions incorrectly** — output format is only N/A for leadership and doc-writer agents. Tool links is only N/A when no tools are mentioned. Don't exempt agents that should have these sections
- **Counting template comments** — HTML comments from the template don't count as content
- **Auditing the plugin-curator** — skip the plugin-curator agent in "all" audits (it follows its own meta-structure)

## Output Format

### Single agent

```markdown
## Agent Audit: {agent-name}

### Summary
- **Lines:** {count} (target: 150–300)
- **Quality score:** {X}/15 criteria met ({Y} N/A)
- **Model:** {model} ({correct/incorrect})

### Criteria

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Line count (150–300) | ✅/⚠️/❌ | {count} lines |
| 2 | Core statement | ✅/⚠️/❌ | {quote first line or issue} |
| 3 | Non-negotiable rules | ✅/⚠️/❌ | {specific or vague?} |
| 4 | Pre-Flight | ✅/⚠️/❌ | {reads CLAUDE.md? line ref} |
| 5 | Mandatory methodology | ✅/⚠️/❌ | {mandatory steps or suggestions?} |
| 6 | Output format | ✅/⚠️/❌/N/A | {template present?} |
| 7 | Failure caps | ✅/⚠️/❌ | {present? line ref} |
| 8 | Decision checkpoints | ✅/⚠️/❌ | {present? count of triggers} |
| 9 | Collaboration table | ✅/⚠️/❌ | {present? count of roles} |
| 10 | Principles | ✅/⚠️/❌ | {count, domain-specific?} |
| 11 | What You Don't Do | ✅/⚠️/❌ | {present? names owners?} |
| 12 | No private refs | ✅/⚠️/❌ | {clean or specific finding} |
| 13 | Tool links | ✅/⚠️/❌/N/A | {linked or specific unlinked tool + line} |
| 14 | Correct model | ✅/⚠️/❌ | {model} — expected {expected} |
| 15 | Description precision | ✅/⚠️/❌ | {includes role + domain + triggers?} |

### Recommended Actions
1. {highest priority fix}
2. {second priority}
```

### All agents

```markdown
## Agent Audit: All Agents

### Summary
- **Total agents:** {count}
- **At 15/15:** {count}
- **Below 15/15:** {count}

### Results

| Agent | Lines | Score | Status |
|---|---|---|---|
| {name} | {N} | {X}/15 | ✅ or {specific issue with evidence} |

Sort by agent name.

### Detail (non-passing agents only)

#### {agent-name} — {X}/15

| Criterion | Status | Evidence |
|---|---|---|
| {criterion} | ❌ | {what was expected, what was found, where} |
```
