---
name: {kebab-case-name}
description: "{What this skill does — specific enough for auto-invocation matching}."
argument-hint: "[{what the user provides}]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

<!-- FRONTMATTER RULES:
- allowed-tools: principle of least access — only include tools the skill actually needs.
  Read-only skills: Read, Glob, Grep. Skills that create files: add Write, Edit.
  Skills that run commands: add Bash. The list above is an example, not a default.

- name: kebab-case, matches the directory name
- description: CRITICAL — Claude may only read this to decide whether to invoke the skill.
  Must be specific enough that Claude can match user intent to this skill.
  Bad:  "Helps with testing" (too vague — matches everything)
  Good: "Write a BDD feature specification in Gherkin with step definitions.
        Use for defining behaviour before implementation in Python projects."
  Include: (1) what it produces, (2) when to use it, (3) any file type triggers
- argument-hint: tells the user what to provide. Wrapped in [brackets].
- user-invocable: true if the user can call it directly via /plugin:skill-name
- allowed-tools: only the tools this skill needs
- paths: (OPTIONAL) add if the skill should auto-trigger on specific file types
  Example: paths: ["**/*.py"] for Python-specific skills
-->

# {Skill Title}

{One paragraph: what this skill does for $ARGUMENTS. Reference related skills if applicable — e.g., "This skill implements the acceptance criteria defined by the `/test-strategy` skill."}

## Step 1: {First mandatory step}

<!-- Steps are REQUIRED, sequential, and blocking. Cannot skip to a later step.
Each step should produce a verifiable output. -->

{What to do, how to do it, what evidence to produce.}

## Step 2: {Second mandatory step}

{Continue the process...}

## Step N: {Final step}

{...}

## Rules

<!-- REQUIRED — specific imperatives and anti-patterns. Not suggestions. -->

- {Rule as imperative — "Always X" or "Never Y"}
- {Anti-pattern — "Don't X because Y. Instead, Z."}

## Output Format

<!-- REQUIRED — structured template. All fields present, nothing left to interpretation. -->

{Exact template showing what the skill produces.}

---

<!-- QUALITY CRITERIA (used by plugin-curator audit):
- [ ] 100-300 lines
- [ ] Description specific enough for auto-invocation matching
- [ ] Self-contained — works without reading the parent agent first
- [ ] Sequential mandatory steps (not suggestions or options)
- [ ] Each step produces a verifiable output
- [ ] Rules section with specific imperatives and anti-patterns
- [ ] Structured output format (not "present your findings")
- [ ] References related skills where appropriate
- [ ] Generic examples only (no private/internal references)
- [ ] External tools linked on first mention
- [ ] argument-hint tells user what to provide
- [ ] Frontmatter description is precise enough for auto-invocation
-->
