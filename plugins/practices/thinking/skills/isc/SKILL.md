---
name: isc
description: Decompose a request into Identifiable, Specific, Verifiable Criteria before executing. Use at the start of any non-trivial task to ensure nothing is missed.
argument-hint: "[task or request to decompose]"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

Decompose $ARGUMENTS into ISC (Identifiable, Specific, Verifiable Criteria) before executing.

ISC is the foundation of the `/algorithm` skill's seven-phase methodology. It can also be used standalone for any task that benefits from upfront decomposition.

## Why

Most incomplete work comes from latching onto one part of a request and missing the rest. ISC forces you to read the entire request — including negatives and implied requirements — and turn it into a checklist you can verify.

## Step 1: Reverse Engineer the Request

Read everything. Extract five categories:

1. **Explicit wants** — what was directly asked for
2. **Implied wants** — what's necessary but not stated (e.g., "update the API" implies tests still pass)
3. **Explicit not-wanted** — what was asked to NOT do, remove, or avoid
4. **Implied not-wanted** — things that would be unwelcome even though not stated (e.g., don't refactor unrelated code)
5. **Gotchas** — things likely to go wrong or be forgotten based on the nature of the request

## Step 2: Determine Effort Level

| Effort | Time budget | ISC range | When |
|--------|-------------|-----------|------|
| Trivial | <30s | 2-4 | One-liner fix, typo |
| Quick | <1min | 4-8 | Small focused change |
| Standard | <2min | 8-16 | Normal request (default) |
| Extended | <8min | 16-32 | Multi-file quality work |
| Advanced | <16min | 24-48 | Substantial design + implementation |
| Deep | <32min | 40-80 | Complex multi-system work |
| Comprehensive | <120min | 64-150 | Large-scale, no time pressure |

Default to **Standard** unless the request clearly warrants more.

## Step 3: Extract Atomic Criteria

For each requirement, create a criterion that is:

- **Identifiable**: Can you point to it? A specific file, line, behavior, or output
- **Specific**: Is there exactly one interpretation? "Looks good" fails. "Renders at 1024px without horizontal scroll" passes
- **Verifiable**: Can you prove it's done? What tool would you use? What would you see?

### The Splitting Test

Apply to EVERY criterion. If any test triggers, split:

1. **"And"/"With" test**: Does it join two verifiable things? "Update the title and fix the link" → two criteria
2. **Independent failure test**: Can part A pass while part B fails? → separate criteria
3. **Scope word test**: Contains "all", "every", "complete", "full"? → enumerate what they actually mean
4. **Domain boundary test**: Crosses UI/API/data/logic boundaries? → one criterion per boundary

### Domain-Specific Decomposition

Split differently depending on what you're working on:

- **UI/Visual**: One criterion per element, per state, per breakpoint
- **Data/API**: One per field, per validation rule, per error case, per edge case
- **Logic/Flow**: One per branch, per transition, per boundary condition
- **Content**: One per section, per format requirement, per tone requirement
- **Infrastructure**: One per service, per config change, per permission

## Step 4: ISC Count Gate

Count your criteria. If below the effort tier floor, you haven't decomposed enough — go back and re-split.

| Effort | Minimum criteria |
|--------|-----------------|
| Trivial | 2 |
| Quick | 4 |
| Standard | 8 |
| Extended | 16 |
| Advanced | 24 |
| Deep | 40 |
| Comprehensive | 64 |

Below floor = re-decompose. You're grouping things that should be separate.

## Step 5: Present and Execute

Present criteria as a numbered checklist:
```
- [ ] ISC-1: [atomic criterion]
- [ ] ISC-2: [atomic criterion]
...
```

Mark each criterion complete **immediately** as it passes during execution — don't batch at the end.

## Step 6: Verify

After completing the work, verify every criterion with evidence:
- ✅ Verified — with evidence (test output, file content, grep result)
- ❌ Not met — with explanation of what's missing
- ⚠️ Partially met — with detail on what remains

No criterion should be marked complete without evidence from a tool (Read, Bash, Grep, etc.). "I believe it's correct" is not verification.

## Example

Request: "Update the README, fix the broken links, and remove references to Chris"

**Effort**: Quick (4-8 ISC)

**Criteria:**
- [ ] ISC-1: README content updated to reflect current state
- [ ] ISC-2: Each link in README resolves (verified per-link)
- [ ] ISC-3: No references to "Chris" in README (`grep -i chris README.md` returns nothing)
- [ ] ISC-4: No changes to files other than README.md
- [ ] ISC-5: Content unrelated to the update is unchanged (diff shows only targeted changes)

## Output Format

The output is the ISC checklist produced in Step 5 — each criterion as a checkable item with its verification command. See the example in Step 5 above.

## Related Skills

- `/algorithm` — ISC decomposition is Phase 1 of the algorithm. Use the full algorithm for execution after defining criteria.
- `/scientific-method` — when criteria require investigation or experimentation to verify.
