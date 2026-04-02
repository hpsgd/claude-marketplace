---
name: usability-review
description: "Review a product, feature, or flow for usability issues using Nielsen's 10 heuristics. Produces a prioritised findings table with severity ratings and specific fix recommendations. Use for experience audits, friction identification, or pre-launch UX review."
argument-hint: "[feature, flow, or area to review]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

# Usability Review

Review $ARGUMENTS against [Nielsen's 10 usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) using the mandatory process below.

## Step 1: Define scope and walkthrough (mandatory)

Before evaluating heuristics, walk the flow as a user would:

```markdown
### Scope

**Feature/flow:** [what is being reviewed]
**Target user:** [who uses this — reference a persona if available]
**Entry point:** [where the user starts]
**Success state:** [what "done" looks like for the user]
**Walkthrough notes:**
1. [First thing the user sees/does — note friction or delight]
2. [Second interaction — note any confusion]
3. [Continue through the complete flow]
```

**Rules for walkthrough:**
- Complete the ENTIRE flow, not just the happy path
- Note every point of friction, confusion, or delight — even minor ones
- Try to break the flow: what happens with empty states, errors, back-navigation, browser refresh?

**Output:** Scope definition and annotated walkthrough notes.

## Step 2: Evaluate against heuristics (mandatory)

For each of Nielsen's 10 heuristics, check the flow for violations:

| # | Heuristic | What to check | Common violations |
|---|---|---|---|
| 1 | **Visibility of system status** | Loading states, progress indicators, confirmation messages, sync status | Missing spinners, no feedback on save, silent failures, stale data indicators |
| 2 | **Match between system and real world** | User's language, familiar concepts, natural ordering | Internal jargon, technical error codes, unintuitive ordering, developer vocabulary |
| 3 | **User control and freedom** | Undo, back, escape, cancel, redo | No undo, modal traps, irreversible one-click actions, no way to cancel in-progress operations |
| 4 | **Consistency and standards** | Same action = same result, same term = same meaning, platform conventions | Different buttons for same action, inconsistent terminology, non-standard icons |
| 5 | **Error prevention** | Confirmation for destructive actions, smart defaults, input constraints | Easy misclicks, no confirmation on delete, no input masks, ambiguous defaults |
| 6 | **Recognition over recall** | Visible options, breadcrumbs, recent history, contextual help | Hidden features, memory-dependent workflows, no context clues, buried settings |
| 7 | **Flexibility and efficiency** | Keyboard shortcuts, bulk operations, customisation, expert paths | Mouse-only interactions, one-at-a-time operations, no shortcuts for power users |
| 8 | **Aesthetic and minimalist design** | Every element earns its place, information hierarchy, visual clarity | Decorative clutter, unused UI elements, information overload, poor hierarchy |
| 9 | **Help users recognise and recover from errors** | Clear message, cause, recovery action | "Error 500", "Invalid input" with no guidance, blame language, no recovery path |
| 10 | **Help and documentation** | Contextual help, searchable docs, tooltips, onboarding | No in-context help, docs buried or outdated, no search, tooltips on wrong elements |

For each violation found:

```markdown
### Finding: [short description]

**Heuristic:** [number and name]
**Location:** [exact screen/component/interaction]
**Severity:** [Critical / Major / Minor / Enhancement]
**What happens:** [what the user experiences]
**Why it's a problem:** [impact on task completion or user confidence]
**Recommendation:** [specific fix — not "improve this" but "add a loading spinner that appears after 200ms"]
```

**Output:** Individual findings with severity, location, and specific recommendations.

## Step 3: Rate severity (mandatory)

Apply consistent severity ratings:

| Severity | Criteria | Impact | Example |
|---|---|---|---|
| **Critical** | Users cannot complete the task at all | Task failure | Form submits but nothing happens, no error shown |
| **Major** | Users struggle significantly or abandon frequently | High friction, potential churn | 5-step process to do a common action, confusing error messages |
| **Minor** | Users notice but find a workaround | Annoyance, reduced confidence | Inconsistent button placement, missing breadcrumbs |
| **Enhancement** | Users would benefit but aren't blocked | Opportunity for delight | No keyboard shortcuts for frequent actions, no bulk operations |

**Rules for severity:**
- Severity is based on IMPACT TO THE USER, not technical difficulty to fix
- A critical finding that affects 5% of users is still critical for those users
- If you're unsure between two severities, pick the higher one — it's better to over-prioritise than to dismiss a real problem

**Output:** All findings with consistent severity ratings.

## Step 4: Prioritise and synthesise (mandatory)

```markdown
### Findings summary

| # | Heuristic | Severity | Finding | Location | Fix |
|---|---|---|---|---|---|
| 1 | [heuristic name] | Critical | [what's wrong] | [where] | [specific recommendation] |
| 2 | [heuristic] | Major | [finding] | [location] | [fix] |
| ... | | | | | |

### Severity distribution
- **Critical:** [count] — must fix before launch/release
- **Major:** [count] — fix in current cycle
- **Minor:** [count] — fix when touching the area
- **Enhancement:** [count] — backlog

### Heuristic coverage
| Heuristic | Findings | Worst severity |
|---|---|---|
| 1. Visibility of system status | [count] | [severity or "No issues"] |
| 2. Match real world | [count] | [severity] |
| ... | | |

### Top 3 Recommendations (by impact)
1. **[Highest impact fix]** — [which findings it addresses, expected improvement]
2. **[Second]** — [detail]
3. **[Third]** — [detail]
```

**Output:** Prioritised findings table, severity distribution, heuristic coverage, and top 3 recommendations.

## Rules

- **Specific fixes, not vague feedback.** "Improve the error handling" is not a recommendation. "Replace the 'Error 500' message with 'We couldn't save your changes. Check your network connection and try again. If this persists, contact support@example.com'" is a recommendation.
- **Every finding needs a location.** "The app has consistency issues" is not a finding. "The Save button is blue on the Settings page and green on the Profile page" is a finding.
- **Walk the unhappy path.** Most usability issues hide in error states, empty states, edge cases, and recovery flows — not in the golden path. Test what happens when things go wrong.
- **Don't conflate aesthetics with usability.** "I don't like the colour" is a preference, not a heuristic violation. Every finding must map to a specific heuristic and explain the impact on task completion.
- **Zero findings is a valid result.** If the flow is genuinely well-designed, say so. Do not manufacture findings to appear thorough.
- **Acknowledge what works.** Note 1–2 things the flow does well. This builds trust in the review and helps the team understand what to preserve.

## Output Format

```markdown
## Usability Review: [scope]

### Scope and Walkthrough
[From Step 1]

### Findings
[Prioritised table from Step 4]

### Severity Distribution
[Counts from Step 4]

### Heuristic Coverage
[Coverage table from Step 4]

### Top 3 Recommendations
[Prioritised fixes from Step 4]

### What Works Well
- [1–2 positive observations]
```

## Related Skills

- `/ux-researcher:persona-definition` — define the target user before reviewing. A usability review is more valuable when done from a specific persona's perspective.
- `/ux-researcher:journey-map` — for mapping the end-to-end experience across multiple touchpoints, not just a single flow.
- `/ui-designer:accessibility-audit` — for accessibility-specific evaluation (WCAG compliance), which complements heuristic review.
