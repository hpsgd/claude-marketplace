# Triage tickets

Testing whether the triage-tickets skill classifies tickets across all required dimensions, includes pattern detection, and produces a structured triage table.

## Prompt

> /support:triage-tickets for this batch of 18 new support tickets received overnight, ranging from billing questions to feature requests to what appear to be related login errors from multiple customers.

## Output

**Triage: 18 tickets (overnight batch)**

**Step 1 — Ingest complete.** All 18 tickets read before classification begins.

**Pattern detected:** 5 tickets describe login failure after password reset, sharing the same "Token expired" error message across different customer accounts. Escalation threshold met (≥3).

**Pattern escalation:**

```
PATTERN ESCALATION
Issue: Login token expiry after password reset
Ticket count: 5
Affected users: Bradwick, Fenwick, Harlow, Thornton, Meridian
Severity: Critical
Sample ticket IDs: T-001, T-002, T-003, T-004, T-005
First reported: 2026-04-14 23:14 UTC
Workaround available: No
Recommended action: Investigate token generation service; check for deploy at ~23:00 UTC
```

**Triage table:**

| Ticket ID | Summary | Category | Severity | Route to | Workaround | Pattern cluster |
|---|---|---|---|---|---|---|
| T-001 | Cannot log in after password reset — "Token expired" | Bug | Critical | Engineering — bugs | None | Login-token-001 |
| T-002 | Password reset completed but login fails immediately | Bug | Critical | Engineering — bugs | None | Login-token-001 |
| T-003 | Token expired error after resetting password | Bug | Critical | Engineering — bugs | None | Login-token-001 |
| T-004 | Can't log in, reset my password twice | Bug | Critical | Engineering — bugs | None | Login-token-001 |
| T-005 | Still getting token error after third reset attempt | Bug | Critical | Engineering — bugs | None | Login-token-001 |
| T-006 | Invoice shows wrong amount for March | Account/billing | Low | Support | None needed | — |
| T-007 | Feature request: bulk export for all projects | Feature request | Low | Product | Manual export | — |
| ... | ... | ... | ... | ... | ... | — |

**Pattern summary**

- Escalations triggered: 1 (Login token expiry — 5 tickets, Critical)
- Regression candidates: Login-token-001 — check for deploy at ~23:00 UTC on 2026-04-14
- Workaround gaps: T-001 through T-005 (Critical, no workaround)

**Metrics:** Critical: 5 | Low: 13. Routing: Engineering: 5, Product: 2, Support: 8, Docs: 3. Patterns: 1 cluster covering 5 tickets.

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 criteria met (94%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Multi-dimension classification — Step 2 requires classifying every ticket across Category (8 options listed), Severity (4 levels with definitions), and Routing (6 destinations). All three dimensions are mandatory and applied to every ticket.
- [x] PASS: Pattern detection at 3+ tickets — Step 3 defines "Escalation trigger: 3+ tickets on the same issue → flag for immediate escalation to product/engineering." The threshold is explicit and the escalation template is provided.
- [x] PASS: Bug report / incident escalation generated — Step 4 requires a structured bug report for every ticket routed to engineering, with 8 mandatory fields. A pattern escalation does not replace this — individual engineering tickets also get bug reports.
- [x] PASS: Structured triage table — Step 5 Output specifies "Present ALL tickets in a single table, sorted by severity (Critical first), then by category" with 7 required columns. Prose summaries are not accepted.
- [x] PASS: Ingest before classifying — Step 1 is titled "Ingest and normalise" and states "Read every ticket" before any classification step. This ordering is structural, not optional.
- [~] PARTIAL: Response SLA per ticket — the Severity table (Step 2) includes explicit response targets: Critical = "Acknowledge within 1 hour, update every 2 hours," High = "Acknowledge within 4 hours," Medium = "Acknowledge within 1 business day," Low = "Acknowledge within 2 business days." SLA targets are defined but attached to severity levels rather than assigned to individual tickets as a column in the triage table. Criterion prefix is PARTIAL — maximum 0.5 points.
- [x] PASS: Routing to specific teams — Step 2 Routing table provides 6 named destinations (Engineering bugs, Engineering infrastructure, Product, Documentation, Support, Security). The triage table output requires a "Route to" column. Unrouted tickets are not permitted.
- [x] PASS: Valid YAML frontmatter — the skill has `name: triage-tickets`, `description`, and `argument-hint` fields.

### Notes

The SLA criterion scores PARTIAL per its prefix. The definition does contain explicit SLA targets (e.g., "Acknowledge within 1 hour" for Critical) in the severity table — these are substantive, not vague. However, the SLA is attached to the severity level rather than surfaced as a per-ticket column in the triage table output format. Adding a "Response by" column to the output table would make this a clean PASS under a PASS-prefixed criterion.

The Rules section adds meaningful constraints beyond the step structure: "Never downplay a user's reported severity without evidence," "Always preserve the user's original language," and "Every Critical and High ticket MUST have a recommended next action." These are enforcement mechanisms not captured in the criteria.
