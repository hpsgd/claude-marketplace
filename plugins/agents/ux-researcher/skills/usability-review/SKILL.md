---
name: usability-review
description: "Review a product, feature, or flow for usability issues using Nielsen's 10 heuristics. Use for experience audits, friction identification, or pre-launch UX review."
argument-hint: "[feature, flow, or area to review]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

# Usability Review

Review $ARGUMENTS against Nielsen's 10 usability heuristics.

## Process

### Step 1: Walk the flow

Go through the feature/flow as a user would. Note every point of friction, confusion, or delight.

### Step 2: Evaluate against heuristics

| Heuristic | Check | Common violations |
|---|---|---|
| **Visibility of system status** | Loading states, progress indicators, confirmation messages | Missing spinners, no feedback on save, silent failures |
| **Match real world** | User's language, familiar concepts, natural order | Internal jargon, technical error codes, unintuitive ordering |
| **User control** | Undo, back, escape, cancel | No undo, modal traps, irreversible one-click actions |
| **Consistency** | Same action = same result, same term = same meaning | Different buttons for same action, inconsistent terminology |
| **Error prevention** | Confirmation for destructive actions, smart defaults, constraints | Easy misclicks, no confirmation on delete, no input masks |
| **Recognition over recall** | Visible options, breadcrumbs, recent history | Hidden features, memory-dependent workflows, no context |
| **Flexibility** | Keyboard shortcuts, bulk operations, customisation | Mouse-only interactions, one-at-a-time operations |
| **Aesthetic/minimal** | Every element earns its place, no visual noise | Decorative clutter, unused UI elements, information overload |
| **Help with errors** | Clear message, cause, recovery action | "Error 500", "Invalid input" with no guidance, blame language |
| **Help and docs** | Contextual help, searchable docs, tooltips | No in-context help, docs buried, no search |

### Step 3: Rate severity

| Severity | Criteria |
|---|---|
| **Critical** | Users cannot complete the task |
| **Major** | Users struggle significantly or frequently |
| **Minor** | Users notice but work around it |
| **Enhancement** | Users would benefit but aren't blocked |

### Output

```markdown
## Usability Review: [scope]

### Findings

| # | Heuristic | Severity | Finding | Location | Recommendation |
|---|---|---|---|---|---|
| 1 | [which heuristic] | Critical | [what's wrong] | [where] | [specific fix] |

### Summary
- Critical: [count]
- Major: [count]
- Minor: [count]
- Enhancement: [count]

### Top 3 Recommendations
1. [Highest impact fix]
2. [Second]
3. [Third]
```
