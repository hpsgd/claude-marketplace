---
name: write-bug-report
description: Write a structured bug report with reproduction steps, expected vs actual behaviour, and severity assessment.
argument-hint: "[bug description or failing test output]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Write a bug report for $ARGUMENTS.

## Systematic Investigation (MANDATORY — 4 phases before writing)

Do not write the bug report from the description alone. Investigate first. Every bug report is only as useful as the evidence behind it.

### Phase 1: Evidence Gathering

1. **Read the error message.** Read it again. What does it _actually_ say? Copy it verbatim — never paraphrase
2. **Reproduce the bug.** If you cannot reproduce it, you cannot report it accurately. Document the exact steps that trigger the failure
3. **Check recent changes:** `git log --oneline -20` — did something change recently that correlates with the symptom?
4. **Gather diagnostic evidence at every component boundary:**
   - What enters the component? (request payload, function arguments, event data)
   - What exits the component? (response, return value, side effects)
   - Where does the data transform from correct to incorrect?
5. **Capture the environment:** OS, runtime version, browser (if web), configuration flags, feature flags, environment (dev/staging/prod)

### Phase 2: Pattern Analysis

1. Find a **working example** of the same operation in the codebase or recent git history
2. Compare against the broken path — identify ALL differences, not just the first one
3. Check if the bug is **isolated** or **systemic** — does the same pattern break elsewhere?
4. Check if the bug is a **regression** — use `git log`, `git bisect`, or test history to find when it last worked

### Phase 3: Root Cause Tracing

1. Trace the execution path from trigger to symptom. Map every function call, data transformation, and boundary crossing
2. Identify the **exact point of failure** — the line where behaviour diverges from expectation
3. Distinguish between:
   - **Root cause** — the underlying defect (e.g., missing null check)
   - **Proximate cause** — the immediate trigger (e.g., a null value arrived)
   - **Contributing factors** — conditions that made it possible (e.g., no input validation upstream)
4. If root cause cannot be determined, state what is known and what is unknown. Never guess

### Phase 4: Coverage Gap Analysis

1. **Should a test have caught this?** Search for existing tests covering the affected code path
2. If tests exist but missed it — why? Wrong assertion? Missing edge case? Test not running?
3. If no tests exist — note the coverage gap as an action item
4. Check if the bug would be caught by:
   - Type checking (would stricter types prevent this?)
   - Linting rules (is there a rule that would flag this pattern?)
   - Runtime validation (would input validation at the boundary catch this?)

## Severity Assessment

Assign severity based on impact, not frequency:

| Severity | Criteria | Examples |
|---|---|---|
| **Critical** | Data loss, security breach, complete service outage, financial impact | Passwords logged in plaintext, database corruption, payment charged twice |
| **High** | Major feature broken for all users, no workaround | Login fails, search returns no results, file upload silently drops data |
| **Medium** | Feature degraded, workaround exists, or affects subset of users | Slow performance under load, incorrect sort order, formatting broken on mobile |
| **Low** | Cosmetic, minor UX issue, or edge case with trivial impact | Typo in UI, misaligned icon, tooltip shows raw key instead of translated text |

### Severity Modifiers

- **Upgrade one level** if: affects data integrity, is a security issue, or has no workaround
- **Downgrade one level** if: only affects internal tools, has easy workaround, or is behind a feature flag
- **Never downgrade** Critical — Critical is Critical

## Reproduction Protocol

Reproduction steps must pass the "stranger test" — someone unfamiliar with the codebase must be able to follow them without asking questions.

Rules for reproduction steps:
1. Each step is ONE action (click, type, run command)
2. Include exact inputs — "enter 'test@example.com'" not "enter an email"
3. Include preconditions — "logged in as admin" not just "on the settings page"
4. Specify the starting state — "with a fresh database" or "after creating 3 items"
5. Include the observation point — "observe that..." at each step where behaviour matters
6. If timing matters, note it — "wait for the spinner to disappear before clicking"
7. If intermittent, document: frequency (1 in 5, sometimes, always), conditions that seem to increase likelihood, any timing dependencies

### Reproduction Evidence

```bash
# Always include exact commands for code-level bugs
$ [exact command]
[exact output, verbatim]
$ echo $?
[exit code]
```

## Bug Report Template

```markdown
## [BUG] <concise title describing the defect>

### Severity
[Critical / High / Medium / Low] — [one-line justification]

### Environment
- **OS:** [e.g., macOS 15.3, Ubuntu 24.04]
- **Runtime:** [e.g., Node 22.1, .NET 9, Python 3.13]
- **Browser:** [if applicable — name and version]
- **Commit:** [git SHA]
- **Configuration:** [any relevant flags, env vars, feature flags]

### Summary
[1-2 sentences describing the defect. What is broken and who is affected.]

### Steps to Reproduce
1. [Precondition / starting state]
2. [Action 1 — exact input]
3. [Action 2 — exact input]
4. [Observation point — what you see]

### Expected Behaviour
[What should happen, with reference to spec/requirement if available]

### Actual Behaviour
[What actually happens — include exact error messages, stack traces, screenshots]

```
[Exact error output, verbatim — never paraphrased]
```

### Root Cause Analysis
- **Root cause:** [the underlying defect, or "under investigation"]
- **Proximate cause:** [the immediate trigger]
- **Affected code:** `[file:line]` — [brief description of the defect]
- **Introduced in:** [commit SHA or "unknown"] — [date if known]

### Regression?
- [ ] Yes — last worked in [commit/version]. Broken by [commit/PR if known]
- [ ] No — this has never worked correctly
- [ ] Unknown — no prior test coverage

### Coverage Gap
- **Existing tests:** [do tests exist for this path? did they pass?]
- **Gap:** [what test is missing that would have caught this?]
- **Recommended test:** [brief description of the test to add]

### Workaround
[If known — exact steps to work around the issue. "None known" if none]

### Suggested Fix
[If root cause is known — specific code change. Otherwise omit this section]

### Evidence
| Artifact | Value |
|---|---|
| Error message | [verbatim] |
| Command run | [exact command] |
| Exit code | [0/1] |
| Stack trace | [key frames] |
| Git bisect result | [good..bad range, if performed] |
```

## Anti-Patterns (NEVER do these)

- **Paraphrasing error messages** — copy verbatim, always. "It threw an error" is not a bug report
- **Vague reproduction steps** — "click around in settings" tells the developer nothing
- **Assuming the cause** — "the database is broken" when you haven't traced the actual failure
- **Bundling multiple bugs** — one defect per report. If you find two bugs, write two reports
- **Omitting environment** — "it doesn't work" without specifying where, when, or how
- **Severity inflation** — calling everything Critical undermines triage. Use the criteria above
- **Proposing fixes without evidence** — the suggested fix must follow from the root cause analysis, not from intuition

## Output

Deliver the complete bug report using the template above. Every field must be filled or explicitly marked as "under investigation". Empty sections are not acceptable.

## Related Skills

- `/qa-engineer:generate-tests` — when tests reveal defects, write a bug report. When a bug is fixed, add a regression test.
