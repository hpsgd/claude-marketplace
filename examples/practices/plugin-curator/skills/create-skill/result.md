# Create skill new skill for existing agent

A contributor asks the create-skill skill to add a `review-go` skill to the coding-standards agent, covering Go-specific conventions for type safety, error handling, and testing patterns.

## Prompt

> /create-skill review-go for coding-standards — Go code review skill covering error handling patterns, interface usage, goroutine safety, and table-driven tests.

```markdown
[Step 1: Reading template and conventions]
Read(file_path="${CLAUDE_PLUGIN_ROOT}/templates/skill-template.md") ✓
Read(file_path="CLAUDE.md") ✓

[Step 2: Identifying parent agent]
find plugins -path "*/coding-standards/agents/*.md" → plugins/practices/coding-standards/agents/coding-standards.md ✓
Reading parent agent...
find plugins -path "*/coding-standards/skills/*/SKILL.md" → existing skills:

## Output

- review-dotnet/SKILL.md
- review-git/SKILL.md
- review-python/SKILL.md
- review-standards/SKILL.md
- review-typescript/SKILL.md

No review-go skill exists. Go-specific checks are not covered by review-standards (language-agnostic) or any sibling.

[Step 3: Domain research]
Go error handling: errors.Is/As, fmt.Errorf %w wrapping
Interface patterns: small interfaces, accept interfaces return structs
Goroutine safety: race detector, sync.Mutex/RWMutex, channel patterns
Testing: table-driven tests, testify, go test -race

[Step 4: Creating directory]
mkdir -p plugins/practices/coding-standards/skills/review-go ✓

[Step 5: Writing SKILL.md]
Writing plugins/practices/coding-standards/skills/review-go/SKILL.md ✓ (158 lines)

Frontmatter:
---
name: review-go
description: "Review Go code against team conventions — error handling, interface design, goroutine safety,
and table-driven tests. Auto-invoked when reviewing .go files."
argument-hint: "[files, PR, or git range to review]"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
paths:
  - "**/*.go"
---

[Step 6: Self-containment check]
Reading skill as a first-time reader...
- Methodology defined within the skill
- Each step has concrete grep commands
- Output template is self-explanatory
Self-contained: ✅

[Step 7: README update]
Added review-go to coding-standards agent's skill list in README.md ✓

[Step 8: Verify]
12/12 quality criteria met ✓

### Created: review-go (coding-standards)

- **Path:** `plugins/practices/coding-standards/skills/review-go/SKILL.md`
- **Lines:** 158
- **Description:** "Review Go code against team conventions — error handling, interface design, goroutine safety, and table-driven tests. Auto-invoked when reviewing .go files."
- **Self-contained:** Yes
- **README updated:** Yes
- **Quality score:** 12/12 criteria met
```

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 criteria met (93.75%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Step 1 reads skill template and CLAUDE.md — Step 1 lists both as explicit `Read()` calls: `Read(file_path="${CLAUDE_PLUGIN_ROOT}/templates/skill-template.md")` and `Read(file_path="CLAUDE.md")`. These are the first two operations, before any creation. The step states "The template defines the MANDATORY structure. Every field is required unless explicitly marked optional."
- [x] PASS: Step 2 reads parent agent AND checks sibling skills — Step 2 includes both find commands: one for the agent definition (`find plugins -path "*/{agent-name}/agents/*.md"`) and one for existing sibling skills (`find plugins -path "*/{agent-name}/skills/*/SKILL.md"`). The Anti-Patterns section calls out "Agent duplication — copying the parent agent's methodology verbatim" as a failure mode, reinforcing the sibling check purpose.
- [x] PASS: SKILL.md frontmatter includes all required fields — Step 5 "Frontmatter (all fields required)" section explicitly lists: name, description, argument-hint, user-invocable, and allowed-tools. The heading states "all fields required" with no exceptions for these five.
- [x] PASS: Description specific enough for auto-invocation — Step 5 states "`description` is CRITICAL — Claude may only read this to decide whether to invoke. Must include (1) what it produces, (2) when to use it." The Anti-Patterns section provides a counter-example: "'Helps with testing' matches everything and triggers on nothing. 'Write E2E acceptance tests in Playwright for a user story' matches precisely."
- [x] PASS: Skill body includes sequential steps, rules, and output format — Step 5 body structure table marks "Sequential steps", "Rules / Anti-patterns", and "Output format" each as Required. The table also marks the Opening paragraph as Required.
- [x] PASS: Step 6 self-containment check performed — Step 6 "Verify self-containment" defines a four-check table: Understandable, Executable, Complete, Bounded. Each check has a Pass criteria column. The step is numbered and sequential, and is explicitly called out as a required step.
- [x] PASS: README updated — Step 7 states "Add the skill to the parent agent's row in the agent table in README.md." It is a separate numbered step with a single unambiguous instruction.
- [~] PARTIAL: Generic examples only — Step 5 quality targets include "Generic examples only (no private references)" and the mental audit in Step 8 includes it as a checklist item. The rule and the check both exist. However there is no structural enforcement mechanism — no grep command or verification step is defined for private references in skills (unlike the agent creation verification in create-agent's Step 10). It is a quality target checked only as a mental audit, not a mechanically enforced constraint. PARTIAL ceiling applies per criterion prefix.

## Notes

No changes to this skill since previous evaluation. Verdict unchanged at PASS (93.75%). The mental audit in Step 8 references 12 criteria, matching the Output Format's `Quality score: X/12` — these align correctly. The one minor gap noted previously remains: `paths` is marked optional in the frontmatter section, but for a file-type-specific skill like review-go the `paths` trigger is near-essential for auto-invocation. Optional labelling may lead contributors to skip it.
