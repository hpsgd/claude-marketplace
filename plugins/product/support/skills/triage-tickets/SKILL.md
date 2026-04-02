---
name: triage-tickets
description: Triage support tickets or issues — categorise, assign severity, identify routing, and flag patterns.
argument-hint: "[ticket content, issue list, or path to issues]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Triage $ARGUMENTS using the mandatory process below. Every step is required — do not skip any.

## Step 1 — Ingest and normalise

Read every ticket. For each, extract:
- **Ticket ID** (or assign a sequential one if absent)
- **Reporter** (name, account, plan tier if available)
- **Raw summary** — one sentence capturing what the user actually said
- **Reproduction signal** — does the ticket contain steps to reproduce, error messages, or screenshots?

If tickets are in a file or directory, use `Read`, `Glob`, or `Grep` to pull them. If they are inline, parse directly.

## Step 2 — Classify each ticket

Apply ALL of the following dimensions to every ticket:

### Category

| Category | Use when |
|---|---|
| Bug | Something that worked before is now broken, or behaves contrary to documentation |
| Feature request | User wants new functionality that does not exist |
| How-to question | User is trying to accomplish something and needs guidance |
| Account / billing | Login, permissions, invoices, plan changes |
| Integration issue | Problem occurs at the boundary with a third-party system |
| Performance | Slowness, timeouts, resource exhaustion — system works but poorly |
| Data issue | Missing, corrupted, or incorrect data |
| Complaint | Expressing dissatisfaction without a specific technical issue |

### Severity

| Severity | Definition | Response target | Examples |
|---|---|---|---|
| **Critical** | System down, data loss, security breach, or complete blocker for multiple users | Acknowledge within 1 hour, update every 2 hours | Production outage, data deletion, auth bypass |
| **High** | Major feature broken for a user, no workaround available | Acknowledge within 4 hours, update daily | Cannot export data, payment processing fails |
| **Medium** | Feature degraded but workaround exists, or issue affects a non-critical path | Acknowledge within 1 business day | Slow report generation, UI glitch on one browser |
| **Low** | Cosmetic issue, minor inconvenience, or question with self-serve answer | Acknowledge within 2 business days | Typo in UI, color preference, "how do I?" |

Severity escalation rules:
- Enterprise or high-tier customer reporting → raise severity by one level
- Issue mentions data loss or security → automatically Critical
- Issue blocks a user from core workflow → at least High

### Routing

| Route to | When |
|---|---|
| Engineering — bugs | Confirmed bug with reproduction steps |
| Engineering — infrastructure | Performance, uptime, scaling issues |
| Product | Feature requests, UX complaints with 3+ occurrences |
| Documentation | How-to questions answerable by better docs |
| Support (self) | Account, billing, known-issue with documented workaround |
| Security | Any mention of unauthorised access, data exposure, vulnerability |

### Workaround

For every ticket, answer: **Is there a known workaround?**
- If yes: state the workaround in 1-2 sentences, cite the source (KB article, prior ticket)
- If no: state "No known workaround" explicitly
- If uncertain: state "Workaround unknown — needs investigation"

## Step 3 — Detect patterns

After classifying all tickets, scan for patterns:

- **Duplicate cluster**: 2+ tickets describing the same root issue → group them, note the count
- **Escalation trigger**: 3+ tickets on the same issue → flag for immediate escalation to product/engineering with this template:

```
PATTERN ESCALATION
Issue: [one-line description]
Ticket count: [N]
Affected users: [list or count]
Severity: [highest severity among the cluster]
Sample ticket IDs: [up to 5]
First reported: [date of earliest ticket]
Workaround available: [yes/no]
Recommended action: [suggested next step]
```

- **Regression signal**: issue appeared after a known deploy or release → flag with the release version
- **Trend direction**: is this issue increasing, stable, or decreasing over the batch?

## Step 4 — Generate bug reports for engineering

For every ticket routed to engineering, produce a structured bug report:

```
## Bug Report: [title]

**Source tickets**: [IDs]
**Severity**: [level]
**Category**: [bug / performance / infrastructure]

### Description
[What is happening, in plain language]

### Steps to reproduce
1. [Step]
2. [Step]
3. [Step]

### Expected behaviour
[What should happen]

### Actual behaviour
[What happens instead]

### Environment
- Product version: [if known]
- Browser/OS/client: [if known]
- Account/plan: [if known]

### Supporting evidence
[Error messages, screenshots, logs — quote directly from the ticket]

### Workaround
[If any]
```

If the ticket lacks reproduction steps, state what is missing and recommend the support agent ask the user for specific information.

## Step 5 — Output

### Triage table

Present ALL tickets in a single table, sorted by severity (Critical first), then by category:

| Ticket ID | Summary | Category | Severity | Route to | Workaround | Pattern cluster |
|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... |

### Pattern summary

After the table, list:
1. **Escalations triggered** — any pattern clusters hitting the 3+ threshold
2. **Regression candidates** — issues potentially linked to recent changes
3. **Workaround gaps** — high/critical tickets with no known workaround (these need KB articles)

### Metrics

- Total tickets triaged: [N]
- By severity: Critical [N], High [N], Medium [N], Low [N]
- By routing: Engineering [N], Product [N], Docs [N], Support [N], Security [N]
- Patterns detected: [N] clusters covering [N] tickets

## Rules

- Never downplay a user's reported severity without evidence. If a user says "this is urgent," treat it as at least High until investigation says otherwise.
- When in doubt about category, pick the one that gets the ticket to the right team faster.
- Always preserve the user's original language in the summary — do not sanitise or corporate-speak their words.
- If a ticket contains multiple issues, split it into separate entries in the triage table.
- Every Critical and High ticket MUST have a recommended next action, not just a routing destination.
