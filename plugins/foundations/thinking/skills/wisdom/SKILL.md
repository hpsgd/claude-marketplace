---
name: wisdom
description: Build and query domain-specific wisdom frames — crystallised patterns from accumulated experience. Use to capture high-confidence principles or to consult accumulated wisdom before making decisions.
argument-hint: "[observation to record, domain to query, or 'synthesize' to find cross-domain patterns]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Manage wisdom frames — domain-specific collections of crystallised behavioral knowledge. Use `$ARGUMENTS` to record observations, query a domain, or synthesise cross-domain patterns.

Wisdom frames are fed by the `/learning` skill — individual learnings accumulate, and when patterns emerge (5+ learnings in a category), they crystallise into wisdom frame principles.

## What is a Wisdom Frame?

A wisdom frame is a living document for a specific domain (e.g., communication, development, deployment, architecture) that accumulates:

- **Core principles**: High-confidence patterns verified through repeated observation
- **Contextual rules**: Rules that apply in specific situations
- **Predictive model**: "When X happens, Y is usually the right response"
- **Anti-patterns**: Things that consistently go wrong, with root causes
- **Cross-domain connections**: Links to related domains

Each principle has a **confidence level** based on how many times it's been observed and verified. Principles above 85% confidence are considered crystallised — reliable enough to act on without re-verification.

## Recording an Observation

When you notice a pattern worth capturing:

### 1. Classify the domain

Common domains: `communication`, `development`, `deployment`, `architecture`, `content-creation`, `testing`, `debugging`, `design`

### 2. Classify the observation type

- **principle**: A high-confidence pattern ("When writing PRs, leading with the why gets faster reviews")
- **contextual-rule**: A rule for specific situations ("In monorepos, always run full CI not just the changed project")
- **prediction**: A request→response pattern ("When the user says 'clean up', they mean minimal targeted changes, not refactoring")
- **anti-pattern**: Something that consistently fails ("Mocking the database in tests masked a real migration bug")

### 3. Write or update the frame

Store wisdom frames in the project's memory directory as `wisdom-{domain}.md`:

```markdown
---
name: wisdom-development
description: Development domain wisdom — crystallised patterns for writing and shipping code
type: reference
---

## Core Principles

- [CRYSTAL 92%] Surgical fixes only — never rearchitect as a fix (observed: 12 times)
- [CRYSTAL 87%] Read before modifying — understand existing patterns first (observed: 8 times)
- [68%] One change when debugging — isolate before expanding scope (observed: 4 times)

## Contextual Rules

- In monorepos: run full CI across all projects before pushing
- When touching API endpoints: verify both unit and integration tests

## Predictive Model

| Request pattern | Likely intent | Right response |
|---|---|---|
| "clean up" | Minimal targeted fix | Small diff, no refactoring |
| "make it better" | Improve specific quality | Ask which dimension |

## Anti-Patterns

- **Mocking everything** (severity: high) — masks real integration failures. Root cause: speed over correctness
- **Batch verification** (severity: medium) — marking criteria complete at the end. Root cause: wanting to "just finish"

## Evolution Log

- 2026-04-01: Added "surgical fixes" principle (source: repeated correction)
```

## Querying Wisdom

When starting work in a domain, query the relevant wisdom frame:

1. Identify which domains are relevant to the current task
2. Load the wisdom frames for those domains
3. Surface any principles or anti-patterns that apply
4. Flag predictions that match the current request pattern

## Cross-Domain Synthesis

When asked to synthesise, or when wisdom frames have grown substantially:

1. Scan all frames for principles that appear in 2+ domains
2. Identify anti-patterns that recur across domains
3. Look for predictions that generalise
4. Present cross-domain principles sorted by confidence and occurrence count

Cross-domain principles are especially valuable — they represent fundamental truths about how work should be done, not domain-specific quirks.

## Frame Health

Assess each frame periodically:
- **Growing**: Updated within 7 days, 10+ observations — actively learning
- **Stable**: Updated within 30 days — mature and reliable
- **Stale**: Not updated in 30+ days — may need review or retirement
