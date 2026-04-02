---
name: code-review
description: Perform a structured code review of staged or recent changes
argument-hint: "[branch or commit range, e.g. 'main..HEAD']"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

Perform a structured four-pass code review with multi-signal scoring. This methodology catches bugs, security issues, and quality problems systematically — not by skimming the diff.

## Before Starting

1. **Determine scope**: Run `git diff $ARGUMENTS` (default: `git diff --staged` if no argument). Count the files and lines changed.
2. **Read full context**: For every changed file, read the entire file — not just the diff. You need surrounding context to judge whether the change is correct.
3. **Identify the intent**: What is this change trying to do? Read commit messages, PR description, or ask. You cannot review correctness without knowing the goal.

## Pass 1: Context and Intent

Understand before judging.

1. **What changed** — list every file and summarise the change in one line each.
2. **Why it changed** — what problem does this solve? What feature does it add?
3. **What didn't change but should have** — are there related files that need updating? Tests? Documentation? Configuration? Types?
4. **Dependency impact** — does this change affect other modules, services, or consumers? Check for exported API changes.

Output a brief context summary before proceeding to Pass 2.

## Pass 2: Correctness

The most important pass. Does the code do what it intends?

For each changed file, check:

1. **Logic errors**:
   - Off-by-one errors in loops, slices, ranges
   - Incorrect boolean logic (De Morgan violations, inverted conditions)
   - Missing `break` in switch/match statements
   - Integer overflow or underflow with arithmetic on untrusted input
   - Floating-point comparison with `==`

2. **Null/undefined/nil handling**:
   - Can any variable be null where it is accessed without a check?
   - Optional chaining used correctly? Or masking a bug by silently returning undefined?
   - Database queries that return null — is the "not found" case handled?

3. **Race conditions**:
   - Shared mutable state accessed without synchronization
   - Check-then-act patterns without atomicity (TOCTOU)
   - Concurrent writes to the same resource

4. **Edge cases**:
   - Empty collections (empty array, empty string, empty map)
   - Zero values, negative values, maximum values
   - Unicode / special characters in string processing
   - Timezone handling in date operations

5. **Error handling**:
   - Are all error paths handled? Not just the happy path?
   - Do errors propagate correctly? Or get swallowed?
   - Are error messages actionable?

6. **State management**:
   - Can state become inconsistent? (partial updates, failed transactions)
   - Are cleanup paths correct? (finally blocks, defer, destructors)

### Scoring — HARD vs SOFT Signals

- **HARD signal**: A correctness issue that will cause wrong behavior in production. Off-by-one on a billing calculation. Missing null check on a required field. Unhandled error that crashes the process. These are blockers.
- **SOFT signal**: A correctness concern that might cause issues under specific conditions. A race condition that requires exact timing. An edge case that current usage patterns avoid. These are important but not blocking.

## Pass 3: Security

Check for vulnerabilities that an attacker could exploit.

1. **Injection** — is any user input concatenated into:
   - SQL queries (use parameterized queries)
   - Shell commands (use safe APIs, never `exec(userInput)`)
   - HTML output (escape or use framework auto-escaping)
   - Regular expressions (ReDoS with unbounded quantifiers)
   - File paths (path traversal with `../`)

2. **Authentication and authorization**:
   - Are new endpoints protected by auth middleware?
   - Are authorization checks present for every operation that modifies data?
   - Is the user's identity verified before acting on their behalf?

3. **Data exposure**:
   - Are secrets in config files, not in code?
   - Do API responses include only the fields the client needs? (no full database rows)
   - Are logs free of PII, tokens, and passwords?
   - Are error messages safe for external users? (no stack traces, no internal paths)

4. **Cryptography**:
   - No custom crypto (use established libraries)
   - No weak algorithms (MD5, SHA1 for security, ECB mode)
   - No hardcoded keys, IVs, or salts

Each security finding is a HARD signal by default.

## Pass 4: Quality and Maintainability

The code works and is secure. Now: is it maintainable?

1. **Readability**:
   - Can you understand what a function does from its name and signature?
   - Are variable names descriptive? (`data`, `result`, `temp`, `val` are red flags)
   - Is the control flow straightforward? Or does it require mental gymnastics?

2. **Duplication**:
   - Is code duplicated from elsewhere in the codebase? Grep for similar patterns.
   - Could shared logic be extracted without over-abstracting?

3. **Performance** (only flag if measurable or obvious):
   - N+1 queries (database call inside a loop)
   - O(n^2) algorithms on unbounded data
   - Unnecessary re-renders (React) or re-computations
   - Missing database indexes for new query patterns
   - Large payloads transferred when only a subset is needed

4. **Test coverage**:
   - Are new code paths tested?
   - Do tests cover the happy path AND at least one error path?
   - Are tests testing behavior or implementation details?
   - Are there tests for the edge cases identified in Pass 2?

Quality findings are SOFT signals unless they introduce measurable performance regression or make the code unmaintainable.

## Friction Scan

After the four passes, do a friction scan:

1. **Developer experience** — will the next person who touches this code understand it quickly?
2. **Debugging** — if this breaks in production, can you diagnose the problem from the logs and error messages?
3. **Rollback** — can this change be safely reverted without data migration?
4. **Feature flags** — should this change be behind a feature flag?

## Output Format

```
## Code Review: [brief description of what was reviewed]

### Context
[2-3 sentences: what changed, why, what the intent is]

### Findings

#### Blockers (HARD signals — must fix before merge)

[Each finding:]
**[Category]** `file:line` — [description]
**Evidence:** [code or grep output]
**Fix:** [concrete suggestion]

#### Important (SOFT signals — should fix, not blocking)

[same format]

#### Suggestions (quality improvements)

[same format]

### Friction Notes
[any friction scan observations]

### Verdict

**[APPROVE | REQUEST_CHANGES | NEEDS_DISCUSSION]**

- APPROVE: Zero blockers, suggestions are optional
- REQUEST_CHANGES: One or more blockers present
- NEEDS_DISCUSSION: Architectural concerns that need team input

Files reviewed: N | Blockers: X | Important: Y | Suggestions: Z
```

## Zero-Finding Gate

If the code is clean, say so. "No findings across all four passes. The change is correct, secure, and well-structured. APPROVE." Do not manufacture issues to appear thorough — false positives erode trust.

## Calibration Rules

- A finding without evidence is not a finding. Show the code.
- A finding without a fix suggestion is incomplete. Propose the change.
- "Consider whether..." is not a finding. Either it is a problem or it is not.
- Performance concerns without measurement or obvious complexity analysis are noise.
- Style preferences that are not codified in team standards are not findings.
