---
name: review-standards
description: "Review code changes against general quality and writing style standards — cross-cutting concerns that apply to every language and file type. Auto-invoked during code review."
argument-hint: "[files, PR, or git range to review]"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

Review code changes against general quality and writing style standards. This skill covers cross-cutting concerns that apply to every language and every file type.

## Mandatory Process

Execute these checks in order. Do not skip steps. Every finding requires file, line, and evidence.

### Pass 1: Dead Code Detection

Search for code that serves no purpose:

1. **Commented-out code** — grep for blocks of commented code (not explanatory comments). Any `// oldFunction()` or `/* former implementation */` is a violation. Version control preserves history; commented code is noise.
2. **Unreachable code** — statements after unconditional returns, breaks, or throws. Check `switch` cases that fall through to dead default branches.
3. **Unused imports** — imports that nothing in the file references. Run the language-appropriate tool or grep for the imported name.
4. **Unused variables** — declared but never read. Pay attention to destructured values where only some fields are used.
5. **Unused functions** — exported functions with zero call sites across the codebase. Use `Grep` to verify: `grep -r "functionName" --include="*.ts"` (adjust extension). A function with zero callers outside its own file and test file is dead.
6. **Feature flags for shipped features** — conditionals around features that have been live for months. These are dead branches waiting to confuse someone.

### Pass 2: Lint Suppression Audit

Every suppression is a code smell until proven otherwise.

1. **Find all suppressions**: grep for language-specific patterns:
   - TypeScript/JS: `// eslint-disable`, `// @ts-ignore`, `// @ts-expect-error`, `// @ts-nocheck`
   - Python: `# noqa`, `# type: ignore`, `# nosec`
   - C#: `#pragma warning disable`, `[SuppressMessage]`
   - Go: `//nolint`
   - General: `// noinspection`
2. **Check for justification**: Each suppression must have an inline comment explaining why. Bare suppressions without explanation are always a finding.
3. **Check for scope**: Line-level suppressions are acceptable. File-level or block-level suppressions are findings unless they address a known tooling bug (and say so).
4. **Check for staleness**: Does the suppression still apply? If the code around it changed, the reason for the suppression may no longer exist.

### Pass 3: Single Responsibility Check

For every function or method in the changed files:

1. **Line count**: Functions over 40 lines warrant scrutiny. Over 80 lines is a finding unless the function is a clearly linear pipeline (e.g., a build script).
2. **Parameter count**: More than 4 parameters suggests the function does too much or needs a configuration object.
3. **Return type complexity**: Functions that return different shapes depending on code paths indicate mixed responsibilities.
4. **Naming**: If the function name contains "And" or "Or" (e.g., `validateAndSave`, `fetchOrCreate`), it handles two concerns.
5. **Nesting depth**: More than 3 levels of nesting (if inside if inside loop) is a finding. Extract inner logic.

### Pass 4: Error Handling Quality

1. **Thrown strings**: `throw "something went wrong"` or `raise Exception("error")` — must use typed/custom errors with enough context to debug.
2. **Swallowed errors**: Empty catch blocks, `catch (e) {}`, `except: pass`, `catch { }` — always a finding.
3. **Generic catches**: `catch (Exception)` at a level where specific exceptions should be handled individually.
4. **Error messages**: Do error messages include enough context to diagnose the problem? "Failed" is useless. "Failed to fetch user {id}: connection timeout after 5s" is actionable.
5. **Error propagation**: Are errors from dependencies wrapped with context, or do raw database/HTTP errors leak to callers?

### Pass 5: Writing Style (Docs, Comments, Copy)

Only run this pass if the diff includes documentation, comments, README content, UI copy, or commit messages.

1. **Banned words** — flag any occurrence:
   `delve`, `tapestry`, `landscape`, `nuanced`, `robust`, `crucial`, `vital`, `realm`,
   `foster`, `leverage`, `facilitate`, `utilize`, `comprehensive`, `holistic`, `synergy`,
   `paradigm`, `ecosystem`, `streamline`, `empower`, `cutting-edge`, `game-changing`,
   `dive into`, `at the end of the day`, `when it comes to`

2. **Banned phrases** — flag any occurrence:
   - "It's important to note", "It's worth mentioning"
   - "In today's world", "In the modern era"
   - "At its core", "At the heart of"
   - "This allows us to", "This enables us to"
   - "A myriad of", "A plethora of"
   - "Moving forward", "Going forward"
   - "Best practices" (say what the practice actually is)

3. **Voice and structure**:
   - Passive voice ("was implemented", "is handled by") — rewrite to active
   - Participial phrase openers ("-ing" constructions at sentence start) — rewrite to direct subject-verb
   - Sentences over 30 words — split or tighten
   - Em dashes: 2 per document maximum. More than that indicates overuse as a crutch

4. **Comment quality**:
   - Comments that restate the code ("increment i by 1") — remove
   - Comments that explain WHY, not WHAT — keep and encourage
   - TODO comments without owner or ticket reference — finding

## Anti-Patterns

Do not flag these — they are acceptable:

- Short utility functions (under 10 lines) without doc comments
- Suppressions with a linked issue number and explanation
- Commented code in test files used as examples or templates (but verify)
- Functions with many parameters if they are builder/factory patterns

## Evidence Format

Every finding must follow this structure:

```
### [SEVERITY] [Category]: [Short description]

**File:** `path/to/file.ext:42`
**Evidence:** [exact code or grep output showing the violation]
**Standard:** [which rule from this skill is violated]
**Fix:** [concrete code or action to resolve it]
```

Severity levels:
- **CRITICAL** — must fix before merge. Swallowed errors, security-relevant suppressions, dead code hiding bugs.
- **IMPORTANT** — should fix before merge. Lint suppressions without justification, functions with mixed responsibilities.
- **SUGGESTION** — improve when convenient. Style issues, minor naming concerns, comment quality.

## Output Template

```
## General Standards Review

### Summary
- Files reviewed: N
- Findings: X critical, Y important, Z suggestions
- Suppressions: N found, M unjustified
- Dead code: N instances

### Findings

[findings grouped by severity, each following the evidence format above]

### Clean Areas
[brief note on what was done well — this matters for calibration]
```

## Zero-Finding Gate

If you find zero issues, state that explicitly: "No findings. All changed files pass general standards review." Do not manufacture findings to appear thorough.

## Related Skills

- Language-specific reviews for deeper checks: `/coding-standards:review-dotnet`, `/coding-standards:review-python`, `/coding-standards:review-typescript`
- `/coding-standards:review-git` — commit message and PR conventions. Run alongside when reviewing PRs.
