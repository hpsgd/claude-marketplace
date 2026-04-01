---
name: feedback-synthesis
description: Synthesise customer feedback into themes — aggregate issues, feature requests, and praise from support tickets, reviews, or survey responses.
argument-hint: "[path to feedback data, or 'recent' to scan support/issue trackers]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Synthesise feedback from $ARGUMENTS.

## Process

1. **Categorise** each piece of feedback: bug report, feature request, usability issue, praise, complaint, question
2. **Theme** related feedback into groups. Use the user's language for theme names, not internal jargon
3. **Quantify** — how many data points per theme? What's the frequency trend?
4. **Prioritise** — which themes have the highest impact (severity × frequency)?

## Output

| Theme | Category | Count | Representative quotes | Suggested action |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

End with top 3 recommendations for the product team, each tied to a specific theme with evidence.
