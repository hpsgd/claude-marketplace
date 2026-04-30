# Result: Triage tickets

| Field | Value |
|---|---|
| **Skill** | `triage-tickets` |
| **Plugin** | `product/support` |
| **Verdict** | PARTIAL |
| **Score** | 15.5/18 criteria met (86%) |
| **Evaluated** | 2026-04-30 |

## Output

Simulated response to: `/support:triage-tickets for this batch of 18 new support tickets received overnight, ranging from billing questions to feature requests to what appear to be related login errors from multiple customers.`

---

### Step 1 — Ingest and normalise

Reading all 18 tickets before classification begins.

| Ticket ID | Reporter | Plan | Raw summary | Reproduction signal |
|---|---|---|---|---|
| T-001 | Alice Chen | Pro | "I can't log in — getting a blank screen after entering credentials" | No steps, no error message |
| T-002 | Marcus Webb | Free | "Login page just spins forever, never gets in" | Browser: Chrome; no error code |
| T-003 | Priya Nair | Enterprise | "All 14 people on our team cannot log in as of 9pm last night" | Error: 503 on auth endpoint; time-stamped |
| T-004 | Jordan Lee | Pro | "Same login issue others might be having — blank redirect" | None |
| T-005 | Sarah Kim | Free | "How do I export my data to CSV?" | N/A — question |
| T-006 | Daniel Okafor | Pro | "Invoices from March are showing wrong amounts" | Screenshots attached; account #8821 |
| T-007 | Fiona Clarke | Enterprise | "Reports take 10+ minutes to generate — was instant last week" | Repro: run any report > 500 rows |
| T-008 | Tom Reyes | Free | "Would love a dark mode option" | N/A — feature request |
| T-009 | Nina Petrov | Pro | "Login broken, tried on Firefox and Chrome, same result" | Two browsers confirmed |
| T-010 | Raj Patel | Pro | "Export button does nothing when I click it" | Steps provided; browser: Safari |
| T-011 | Emily Wu | Enterprise | "Payment failed but we were still charged — need refund" | Transaction ID: TXN-44892 |
| T-012 | Chris Hall | Free | "The font in the dashboard looks off on mobile" | Screenshot attached; iOS 17 |
| T-013 | Aisha Osei | Pro | "Getting error 'session expired' immediately after logging in" | Repro confirmed; timestamp 22:14 |
| T-014 | Ben Morris | Free | "Can you add Zapier integration?" | N/A — feature request |
| T-015 | Lena Schmidt | Enterprise | "Data import silently dropped 2,000 rows — no error shown" | CSV sample attached |
| T-016 | Omar Hassan | Pro | "How do I set up SSO for my team?" | N/A — question |
| T-017 | Yuki Tanaka | Free | "Your pricing page says one thing, my invoice says another" | Screenshot of pricing page vs invoice |
| T-018 | Grace Obi | Pro | "Dashboard loading slowly since yesterday morning" | Repro: login, wait 15s for dashboard |

---

### Step 2 — Classify each ticket

*(Applied to all 18 after full ingest.)*

**Pattern note before table:** Tickets T-001, T-002, T-003, T-004, T-009, T-013 all describe login failures with similar onset time (~9pm previous evening). Flagging for Step 3 pattern detection.

---

### Step 3 — Pattern detection

**Login failure cluster (T-001, T-002, T-003, T-004, T-009, T-013): 6 tickets**

Escalation threshold met (3+). Generating escalation:

```
PATTERN ESCALATION
Issue: Auth service returning blank screens, infinite spinner, and session-expired
        errors immediately post-login across Pro and Enterprise plans
Ticket count: 6
Affected users: 14 (T-003 alone), plus 5 individual reporters = 19+ confirmed
Severity: Critical (Enterprise customer affected; multiple users blocked from core workflow)
Sample ticket IDs: T-001, T-002, T-003, T-004, T-009, T-013
First reported: T-003 timestamps auth failures from 21:00 previous evening
Workaround available: No
Recommended action: Escalate to Engineering on-call immediately; check auth service
                    logs from 20:45 onward; assess whether deploy preceded onset;
                    post status update to all affected accounts within 30 minutes
```

**Regression signal:** T-007 (report generation 10+ minutes, was instant last week) and T-018 (dashboard slow since yesterday morning) may share root cause with the auth cluster if a deploy degraded the session/query layer. Flag for engineering to cross-reference.

**Trend direction:** Login failures are acute (single overnight window), not gradual. Billing discrepancy tickets (T-006, T-017) appear unrelated but are worth grouping for the billing team.

---

### Step 5 — Triage table

Sorted by severity (Critical first), then category.

| Ticket ID | Summary | Category | Severity | Route to | Workaround | Pattern cluster |
|---|---|---|---|---|---|---|
| T-003 | 14-person Enterprise team cannot log in since 9pm | Bug | Critical | Engineering — bugs | None | LOGIN-001 |
| T-015 | Data import silently dropped 2,000 rows, no error | Data issue | Critical | Engineering — bugs | None | — |
| T-011 | Payment failed but customer was still charged | Account / billing | Critical | Support (self) → Finance | Raise dispute via billing portal | — |
| T-001 | Blank screen after login on Pro account | Bug | High | Engineering — bugs | None | LOGIN-001 |
| T-002 | Login page spins forever, never authenticates | Bug | High | Engineering — bugs | None | LOGIN-001 |
| T-004 | Blank redirect loop on login | Bug | High | Engineering — bugs | None | LOGIN-001 |
| T-009 | Login broken on Firefox and Chrome | Bug | High | Engineering — bugs | None | LOGIN-001 |
| T-013 | Session expired immediately after login at 22:14 | Bug | High | Engineering — bugs | None | LOGIN-001 |
| T-010 | Export button does nothing in Safari | Bug | High | Engineering — bugs | Workaround unknown — needs investigation | — |
| T-007 | Reports take 10+ min to generate (was instant) | Performance | High | Engineering — infrastructure | None | PERF-001 (possible) |
| T-006 | March invoices showing incorrect amounts | Account / billing | Medium | Support (self) → Finance | Customer to contact billing@; attach account # | — |
| T-016 | How to set up SSO for team | How-to question | Medium | Documentation | KB article: /docs/sso-setup | — |
| T-018 | Dashboard loading slowly since yesterday | Performance | Medium | Engineering — infrastructure | None | PERF-001 (possible) |
| T-017 | Pricing page contradicts invoice amount | Account / billing | Medium | Support (self) → Finance | Customer to contact billing@; attach screenshot | — |
| T-005 | How do I export data to CSV? | How-to question | Low | Documentation | KB article: /docs/export-csv | — |
| T-008 | Feature request: dark mode | Feature request | Low | Product | N/A | — |
| T-014 | Feature request: Zapier integration | Feature request | Low | Product | N/A | — |
| T-012 | Dashboard font looks off on mobile (iOS 17) | Bug | Low | Engineering — bugs | None known; cosmetic only | — |

---

### Pattern summary

**Escalations triggered**

- **LOGIN-001** — 6 tickets (T-001, T-002, T-003, T-004, T-009, T-013). Critical. Engineering on-call. No workaround. 19+ users blocked. Escalation notice sent above.

**Regression candidates**

- LOGIN-001 onset correlates with 21:00 timestamp on T-003. Engineering to check deployment log.
- PERF-001 (T-007, T-018): report generation and dashboard degradation both date from "yesterday morning" — may be a shared infrastructure regression.

**Workaround gaps**

- T-003, T-001, T-002, T-004, T-009, T-013: all Critical/High login bugs — no workaround exists. KB article cannot substitute; requires engineering fix.
- T-015: data import silently dropping rows — Critical, no workaround. Needs engineering and a KB article explaining what import validation errors look like.
- T-010: export button broken in Safari — needs investigation before a workaround can be documented.

---

### Metrics

| Metric | Value |
|---|---|
| Total tickets triaged | 18 |
| Critical | 3 |
| High | 7 |
| Medium | 4 |
| Low | 4 |
| Engineering — bugs | 8 |
| Engineering — infrastructure | 2 |
| Product | 2 |
| Documentation | 2 |
| Support / Finance | 3 |
| Security | 0 |
| Patterns detected | 1 confirmed (LOGIN-001), 1 candidate (PERF-001) covering 8 tickets |

---

### Bug reports for engineering (Critical/High sample)

**LOGIN-001 consolidated bug report**

```markdown
## Bug Report: Authentication service failure — login blocked for 19+ users

**Source tickets**: T-001, T-002, T-003, T-004, T-009, T-013
**Severity**: Critical
**Category**: Bug

### Description
Multiple Pro and Enterprise users are unable to log in. Symptoms include blank
screens after credential entry, infinite spinner on the login page, and immediate
"session expired" errors. Onset time is approximately 21:00 the previous evening.

### Steps to reproduce
1. Navigate to login page
2. Enter valid credentials
3. Submit — observe blank screen, infinite spinner, or immediate session expiry

### Expected behaviour
Successful authentication and redirect to dashboard

### Actual behaviour
Blank screen, infinite spinner, or "session expired" error immediately post-submit

### Environment
- Browsers: Chrome (T-002), Firefox + Chrome (T-009)
- Plans: Free (T-002), Pro (T-001, T-004, T-009, T-013), Enterprise (T-003)
- Auth endpoint error on T-003: 503

### Supporting evidence
T-003 (Enterprise): "All 14 people on our team cannot log in as of 9pm last night" — error: 503 on auth endpoint
T-013: "Getting 'session expired' immediately after logging in" — timestamp 22:14

### Workaround
None known
```

---

## Criteria results

- [x] PASS: Skill classifies each ticket across multiple dimensions — category (bug/question/feature/billing), severity, and routing destination — met: Step 2 covers 8 categories, 4 severity levels, 6 routing destinations
- [x] PASS: Skill includes pattern detection — when 3 or more tickets match the same root issue, they should be grouped and escalated — met: Step 3 explicitly states "Escalation trigger: 3+ tickets on the same issue"
- [x] PASS: Skill generates a bug report or incident escalation for patterns that suggest a systemic issue — met: Step 3 includes a PATTERN ESCALATION template; Step 4 produces structured bug reports for engineering
- [x] PASS: Skill produces a structured triage table as output — met: Step 5 specifies a table with defined columns
- [x] PASS: Skill requires an ingest step — reading all tickets before classifying any — met: Step 1 reads every ticket; classification is Step 2, sequenced after ingest
- [~] PARTIAL: Skill assigns a response SLA or priority to each ticket — partially met: severity table in Step 2 includes explicit response targets (Critical: 1h ack, High: 4h ack, Medium: 1BD, Low: 2BD) but the triage table output schema does not include a Priority or SLA column — severity does this work implicitly, not per-row
- [x] PASS: Skill routes tickets to appropriate teams or owners, not just classifies them — met: routing table maps issue types to six named destinations; Step 2 requires routing as a classification dimension on every ticket
- [x] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields — met: frontmatter contains all three required fields plus user-invocable and allowed-tools

## Output expectations results

- [x] PASS: Output's ingest step reads ALL 18 tickets BEFORE classifying any — met: Step 1 ingests all 18; classification follows in Step 2
- [x] PASS: Output's triage table classifies each ticket across the dimensions — category, severity, and routing destination — met: table includes Category, Severity, Route to columns for all 18
- [x] PASS: Output detects the login-error pattern — multiple tickets sharing the same root cause are GROUPED — met: T-001, T-002, T-003, T-004, T-009, T-013 grouped into LOGIN-001
- [x] PASS: Output generates an incident escalation for the login pattern — met: PATTERN ESCALATION block names affected user count (19+), first reported time (21:00), sample ticket IDs, and recommends engineering on-call
- [ ] FAIL: Output's structured triage table has the required columns — Ticket ID, Customer, Category, Severity, Routing, Priority, Pattern Group, Suggested Owner — not met: skill schema specifies Ticket ID, Summary, Category, Severity, Route to, Workaround, Pattern cluster — Customer, Priority, and Suggested Owner are absent from the table definition; simulated output follows the skill schema
- [ ] FAIL: Output assigns a response SLA per ticket based on severity with explicit values per row — not met: SLA targets exist in the Step 2 severity reference table but are not a column in the output triage table schema; per-ticket SLA is not surfaced in the deliverable
- [x] PASS: Output routes billing tickets to billing/finance, feature requests to product, bugs to engineering, questions to support agents — met: routing table and simulated triage table distinguish all four destinations
- [x] PASS: Output identifies tickets answerable from KB articles or self-serve — met: T-005 and T-016 routed to Documentation with KB links; workaround column cites KB articles for billing questions
- [x] PASS: Output's pattern detection rule is explicit — 3+ tickets matching the same root cause trigger an incident escalation — met: Step 3 states threshold explicitly; simulated output applies it to 6-ticket LOGIN-001 cluster
- [~] PARTIAL: Output addresses tickets that need follow-up classification — tickets needing more info get a separate state — partially met: Step 4 instructs the agent to state what is missing and ask for specifics, but the triage table schema has no formal "needs more info" state; T-001 and T-002 (no reproduction steps) blend into the regular Bug classification rather than getting a distinct status

## Notes

The skill's five-step pipeline is logically sequenced and structurally sound. Scoring gaps concentrate in the output table schema: Suggested Owner and Priority are not columns, and per-row SLA is defined in the Step 2 reference table but never surfaced in the Step 5 deliverable. For a handoff artifact the table is the working document — decisions that live only in the reference table require the reader to cross-reference manually, which defeats the purpose.

The "needs more info" handling is procedural (Step 4) but not formalised as a ticket state. A triage table used across a support team needs an explicit status value so unclassified tickets don't get misrouted or silently dropped.

Both gaps are fixable with minor additions to the Step 5 table schema: add Priority (derived from severity), Suggested Owner (named person or queue), and Status (Open / Needs info / Escalated / Deflected). The five-step process and escalation logic are otherwise solid.
