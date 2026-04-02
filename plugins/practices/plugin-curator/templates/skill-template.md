# Skill Definition Template

Every skill in this marketplace follows this structure. Skills are standalone — they work without the parent agent's context.

---

```markdown
---
name: {kebab-case-name}
description: "{What this skill does — one sentence, specific enough for auto-invocation matching}."
argument-hint: "[{what the user provides}]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
paths:                              # CONDITIONAL — only if the skill auto-triggers on specific files
  - "**/*.{ext}"
---

# {Skill Title}

{One paragraph: what this skill does for $ARGUMENTS. Reference related skills if applicable.}

## Step 1: {First mandatory step}                            [Steps are REQUIRED and sequential]

{What to do, how to do it, what evidence to produce.
Steps are mandatory and blocking — you cannot skip to a later step.}

## Step 2: {Second mandatory step}

{Continue the process...}

## Step N: {Final step}

{...}

## Rules                                                      [REQUIRED]

{Specific rules for this skill. Written as imperatives.
Include anti-patterns: what NOT to do and why.}

## Output Format                                              [REQUIRED]

{Structured template showing exactly what the skill produces.
Should include all fields — nothing left to interpretation.}
```

## Quality Criteria for Skill Definitions

A well-written skill definition:

- [ ] Is 100-300 lines (not a stub, not a novel)
- [ ] Has a description specific enough for auto-invocation matching
- [ ] Is self-contained — works without reading the parent agent first
- [ ] Has sequential, mandatory steps (not suggestions or options)
- [ ] Each step produces a verifiable output
- [ ] Has Rules section with specific imperatives and anti-patterns
- [ ] Has a structured Output Format (not "present your findings")
- [ ] References related skills where appropriate (e.g., "see `/isc` for criteria decomposition")
- [ ] Uses generic examples (no private/internal references)
- [ ] Links external tools/frameworks on first mention
- [ ] Has `argument-hint` that tells the user what to provide
- [ ] Has `paths` filter if the skill should auto-trigger on specific file types
