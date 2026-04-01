---
name: triage-tickets
description: Triage support tickets or issues — categorise, assign severity, identify routing, and flag patterns.
argument-hint: "[ticket content, issue list, or path to issues]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Triage $ARGUMENTS.

## For each ticket

1. **Category**: bug, feature request, how-to question, complaint, integration issue
2. **Severity**: critical (system down, data loss), high (major feature broken), medium (degraded experience), low (cosmetic, minor)
3. **Routing**: engineering (bug), product (feature request), documentation (how-to), support (account/billing)
4. **Workaround**: is there a known workaround? Include it
5. **Pattern**: have we seen this before? Flag duplicates or trends

## Output

Present as a triaged table sorted by severity, then flag any patterns (3+ tickets on the same issue = escalate to product/engineering).
