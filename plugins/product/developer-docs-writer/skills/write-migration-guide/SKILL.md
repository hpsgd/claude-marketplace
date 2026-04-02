---
name: write-migration-guide
description: "Write a migration guide for a breaking change -- API version upgrade, database schema change, or major version transition. Produces step-by-step migration instructions with before/after examples, rollback plan, and timeline. Use when shipping breaking changes that require customer or developer action."
argument-hint: "[breaking change, version upgrade, or migration to document]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Write Migration Guide

Write a migration guide for $ARGUMENTS. Every breaking change needs a clear path from old to new — with code examples, a rollback plan, and a deprecation timeline. Developers will judge the quality of the change by the quality of the migration guide.

## Step 1: Document what's changing (mandatory)

```markdown
### Change summary

| Element | Detail |
|---|---|
| **What changed** | [concise description of the breaking change] |
| **Why it changed** | [rationale — performance, security, consistency, deprecation] |
| **Old version** | [version number, API version, schema version] |
| **New version** | [version number] |
| **Change type** | [API breaking change / schema migration / library major version / config change / protocol change] |

### Before / After overview

**Before (v[old]):**
```[language]
// Old approach
[code showing current usage]
```

**After (v[new]):**
```[language]
// New approach
[code showing new usage]
```

**Key difference:** [one sentence explaining the conceptual change, not just the syntax change]
```

**Rules for documenting changes:**
- Always explain WHY the change was made. "We renamed the field" is not a reason. "We renamed `user_id` to `account_id` because the entity represents an account, not a user, and the old name caused integration bugs" is a reason
- Before/after examples must use realistic code, not pseudo-code. Developers will copy-paste these

**Output:** Change summary table with before/after code examples.

## Step 2: Assess impact (mandatory)

```markdown
### Impact assessment

| Dimension | Detail |
|---|---|
| **Who is affected** | [all users of API v2 / users of the payments module / anyone using custom auth] |
| **What code needs to change** | [API calls to /v2/users, database queries against users table, SDK method calls] |
| **Estimated migration effort** | [minutes / hours / days — be honest] |
| **Risk level** | [Low — cosmetic changes / Medium — logic changes / High — data migration required] |
| **Can old and new coexist?** | [Yes — both versions supported until [date] / No — hard cutover required] |

### Who does NOT need to migrate
[Explicitly state who is unaffected — this saves developers time checking whether they need to act]
```

**Rules for impact assessment:**
- Be honest about effort. "5 minutes" when it's actually 2 hours destroys trust
- State who is NOT affected — this is as valuable as stating who is

**Output:** Impact assessment table with affected scope and effort estimate.

## Step 3: Write migration steps (mandatory)

Numbered, specific, copy-pasteable steps:

```markdown
### Migration steps

#### Prerequisites
- [ ] [prerequisite — e.g. "Upgrade SDK to v3.2+ before starting"]
- [ ] [prerequisite — e.g. "Back up your database"]
- [ ] [prerequisite — e.g. "Read the full breaking changes table in Step 4"]

#### Step 1: [action]

[Explanation of what this step does and why]

**Before:**
```[language]
[old code]
```

**After:**
```[language]
[new code]
```

[Any notes, gotchas, or edge cases for this step]

#### Step 2: [action]
[Continue pattern...]

#### Step N: Verify migration
[How to confirm everything works — see Step 7]
```

**Rules for migration steps:**
- Every step must have a before/after code example. Prose alone is not sufficient for a migration guide
- Steps must be ordered. If Step 3 depends on Step 1, say so explicitly
- Include the full code change, not just the changed line. Developers need context to find the right place in their code
- If a step can be automated, provide the script (see automation rule below)

**Output:** Numbered migration steps with before/after code examples.

## Step 4: Document breaking changes exhaustively (mandatory)

```markdown
### Breaking changes

| # | What changed | Old behaviour | New behaviour | Action required | Example |
|---|---|---|---|---|---|
| 1 | [specific change] | [old] | [new] | [what developer must do] | [code snippet] |
| 2 | [change] | [old] | [new] | [action] | [example] |
| 3 | [change] | [old] | [new] | [action] | [example] |

### Non-breaking changes (no action required)
| What changed | Old behaviour | New behaviour | Why no action needed |
|---|---|---|---|
| [change] | [old] | [new] | [backwards compatible because...] |
```

**Rules for breaking changes:**
- EVERY breaking change gets its own row. Do not combine multiple changes into "various API improvements"
- The "Action required" column must be specific enough to act on. "Update your code" is not an action. "Change `getUser(id)` to `getAccount(id)`" is an action
- Include non-breaking changes separately — developers need to know what they can ignore

**Output:** Exhaustive breaking changes table with actions and examples.

## Step 5: Provide coexistence guidance (mandatory)

```markdown
### Coexistence and deprecation timeline

| Date | Event | Action required |
|---|---|---|
| [date] | New version released | Migration guide available, start migrating |
| [date] | Deprecation warning added to old version | Old version still works but logs warnings |
| [date] | Old version enters maintenance mode | Security fixes only, no new features |
| [date] | Old version end-of-life | Old version stops working / returns errors |

### Running old and new simultaneously
[Can they coexist? If yes, how. If no, what's the cutover strategy]

**Dual-write/dual-read guidance:**
[If applicable — how to support both old and new during transition]
```

**Rules for coexistence:**
- Every deprecation needs a timeline with actual dates (or "X months after release"), not "eventually"
- If old and new cannot coexist, the migration window must be clearly communicated and reasonable for the effort required

**Output:** Deprecation timeline and coexistence strategy.

## Step 6: Write rollback instructions (mandatory)

```markdown
### Rollback plan

**If migration fails, revert with these steps:**

#### Prerequisites for rollback
- [ ] [what must be true for rollback to work — e.g. "database backup taken before Step 3"]

#### Rollback steps
1. [specific revert action]
2. [next revert action]
3. [verify rollback successful]

#### Rollback limitations
- [what cannot be rolled back — e.g. "data written in new format requires manual conversion"]
- [time window — e.g. "rollback only possible within 24h before new data accumulates"]

#### Point of no return
[Which step in the migration, if any, makes rollback impossible — and how to prepare for it]
```

**Rules for rollback:**
- Every migration guide MUST have a rollback plan. "You can't roll back" is a valid answer but must be stated explicitly with the reason
- Identify the point of no return — the step after which rollback is no longer possible
- If rollback requires a database restore, say so and ensure the backup step is in the prerequisites

**Output:** Rollback instructions with limitations and point of no return.

## Step 7: Add verification steps (mandatory)

```markdown
### Verification

#### Automated verification
```[language]
// Script or commands to verify migration was successful
[verification code — e.g. health check endpoint, test suite, query]
```

#### Manual verification checklist
- [ ] [check — e.g. "API returns v3 response format"]
- [ ] [check — e.g. "Dashboard loads without errors"]
- [ ] [check — e.g. "Existing data displays correctly"]
- [ ] [check — e.g. "New features are accessible"]

#### Common post-migration issues
| Symptom | Cause | Fix |
|---|---|---|
| [what you see] | [why it happens] | [how to fix] |
| [symptom] | [cause] | [fix] |
```

**Output:** Verification script, manual checklist, and troubleshooting table.

## Rules

- **Every breaking change needs a before/after code example.** Prose alone is not sufficient. Developers read code, not paragraphs.
- **Provide a deprecation timeline.** "Old version will be deprecated" without a date is not a plan. Give dates or relative timeframes.
- **Automated migration scripts are better than manual steps.** If you can write a codemod, sed command, or migration script, include it. Manual steps introduce human error.
- **Test the migration guide before publishing.** Run every command, verify every example, attempt the rollback. A migration guide with broken examples is worse than no guide.
- **Never hide breaking changes.** Undocumented breaking changes erode trust faster than any other documentation failure. When in doubt, list it.
- **Effort estimates must be honest.** Underestimating migration effort is a form of lying to your developers. Round up, not down.

## Output Format

```markdown
# Migration Guide: [old version] -> [new version]

## What's Changing
[From Step 1 — summary and before/after]

## Impact Assessment
[From Step 2]

## Migration Steps
[From Step 3 — numbered with code examples]

## Breaking Changes
[From Step 4 — exhaustive table]

## Deprecation Timeline
[From Step 5]

## Rollback Plan
[From Step 6]

## Verification
[From Step 7]

---
Migration: [old] -> [new]
Estimated effort: [time]
Deprecation date: [date]
Last updated: [date]
```

## Related Skills

- `/developer-docs-writer:write-api-docs` — write the API reference for the new version. The migration guide gets developers to the new version; the API docs help them use it.
- `/release-manager:release-plan` — migration is part of the release. The release plan should reference this migration guide and allocate time for customer migration support.
