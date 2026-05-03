# Triage Tickets

Scenario: Testing whether the triage-tickets skill classifies tickets across all required dimensions, includes pattern detection, and produces a structured triage table.

## Prompt

> /support:triage-tickets for this batch of 18 new support tickets received overnight, ranging from billing questions to feature requests to what appear to be related login errors from multiple customers.
> 
> ---
> 
> **T-001** | sarah.johnson@brightpath.io | 2024-11-14 01:14
> Subject: Can't log in — getting "Invalid credentials" error
> Body: Hi, I've been locked out since late last night. My password is definitely correct — I reset it twice and it still gives me "Invalid credentials" when I try to sign in. Please help urgently, I have a client demo first thing this morning.
> 
> **T-002** | david.kim@novacycle.com | 2024-11-14 02:41
> Subject: Authentication failing since 9pm — AUTH-500 error
> Body: I'm getting an AUTH-500 error every time I try to log in. It started around 9pm last night. I've cleared my cache, tried a different browser, and reset my password. Same error. Is there an outage?
> 
> **T-003** | rachel.torres@helixgrowth.co | 2024-11-14 03:07
> Subject: "Authentication service unavailable" — locked out
> Body: Every time I try to log in I get "Authentication service unavailable. Please try again later." I've been trying for two hours. This is happening on both my laptop and my phone. My account is rachel.torres@helixgrowth.co.
> 
> **T-004** | priya.patel@stackvault.io | 2024-11-14 04:22
> Subject: Login broken — same AUTH error as my colleague
> Body: My colleague David Kim emailed you earlier about an AUTH-500 error. I'm having the exact same issue. We're both on the same account (Novacycle). Something is definitely wrong on your end.
> 
> **T-005** | james.liu@foundryops.com | 2024-11-14 03:55
> Subject: Does the Pro plan include API access?
> Body: Hi, I'm on the Starter plan and considering upgrading. I can't find a clear answer on your pricing page about whether the Pro plan includes API access, or if that's an add-on. Can you clarify before I upgrade?
> 
> **T-006** | emma.wilson@pearlanalytics.io | 2024-11-14 05:11
> Subject: Charged twice this billing cycle
> Body: I noticed two separate charges of $149 on my credit card this month, both labelled "Turtlestack Pro". My billing period runs the 1st to the 1st — there should only be one charge. Invoice numbers INV-8821 and INV-8847. Please advise.
> 
> **T-007** | carlos.mendez@lightspeedlogic.com | 2024-11-14 06:30
> Subject: Downgrading from Pro to Starter — what happens to billing?
> Body: I'd like to downgrade my plan at the end of this billing cycle. Can you tell me: do I keep Pro features until the end of the period, or do they drop immediately? And is there any prorating if I downgrade mid-cycle in the future? Thanks.
> 
> **T-008** | tom.bradley@northernedge.co | 2024-11-14 00:58
> Subject: Feature request: bulk CSV export
> Body: We've been manually copying data out of reports for months. A bulk CSV export of all report data with date filters would save us hours a week. Is this on your roadmap? Happy to elaborate on the use case if helpful.
> 
> **T-009** | fatima.alhassan@meridianux.com | 2024-11-14 01:45
> Subject: Feature request: dark mode
> Body: I spend a lot of time in the platform late at night and the white interface is pretty harsh on the eyes. Dark mode would be a huge quality-of-life improvement. Lots of tools have this now — any plans to add it?
> 
> **T-010** | noah.park@coastlinedata.io | 2024-11-14 07:02
> Subject: SSO / SAML integration request
> Body: Our company is rolling out SSO across all SaaS tools next quarter. We'll need to remove any tool that doesn't support SAML 2.0. Do you have a SAML integration, or is it on the roadmap? If so, what's the timeline?
> 
> **T-011** | alex.rivera@sunriseventures.co | 2024-11-14 02:10
> Subject: How do I reset my password?
> Body: Hi, I've forgotten my password and can't find the reset option on the login page. Can you walk me through how to reset it?
> 
> **T-012** | diane.foster@trellismgmt.com | 2024-11-14 04:50
> Subject: Where is the API documentation?
> Body: I'm a developer trying to integrate your API into our internal tooling. I can see there's an API but I can't find the documentation. Can you point me to the right place?
> 
> **T-013** | jake.morrison@blueridgecorp.com | 2024-11-14 06:15
> Subject: How do I add team members to my account?
> Body: I've just signed up on the Pro plan and I want to invite two colleagues. I can see a "Team" section in settings but I'm not sure what happens when I invite someone — do they get a separate account, or share mine? And is there a per-seat charge?
> 
> **T-014** | chloe.wang@vertexlabs.io | 2024-11-14 05:38
> Subject: Dashboard taking 15+ seconds to load
> Body: Since the update last Tuesday our main dashboard takes 15 seconds or more to load. Before that it was almost instant. I'm in Sydney on a 500Mbps connection so it's not my internet. It's been getting worse each day. Can you look into this?
> 
> **T-015** | marcus.chen@acme-corp.com | 2024-11-14 06:58
> Subject: URGENT: Data export timing out — board meeting at 9am
> Body: Our 180,000-record customer export has been failing since yesterday morning. Every attempt runs for about 90 seconds then fails with "Export failed. Please try again." I have a board meeting at 9am and need this data. Is there a workaround?
> 
> **T-016** | ben.adams@forgewire.co | 2024-11-14 03:20
> Subject: Nothing is working
> Body: Everything is broken. I can't do anything. Please help.
> 
> **T-017** | lily.chen@moonshotmedia.co | 2024-11-14 07:45
> Subject: The report data looks wrong
> Body: The numbers in my weekly summary report don't match what I see elsewhere. Something is off. Please check.
> 
> **T-018** | stefan.mueller@klausengroup.de | 2024-11-14 08:01
> Subject: Account deletion and GDPR data removal request
> Body: I would like to delete my account and request that all personal data associated with my account (email stefan.mueller@klausengroup.de, account ID KLG-3304) be permanently deleted in accordance with my rights under GDPR Article 17. Please confirm receipt and provide a timeline for completion.
> 
> ---

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll triage this batch following the mandatory process step by step.

## Step 1 — Ingest and normalise

Parsed 18 tickets from your input with reporters, error messages, timing data, and account information.

## Step 2 — Classify each ticket

Applying all classification dimensions...

## Step 3 — Detect patterns

**CRITICAL FINDING**: 4 tickets (T-001, T-002, T-003, T-004) describe authentication failures in a 3-hour window starting ~9pm on 2024-11-14. Different error messages suggest cascading or partial service degradation rather than user-specific issues.

---

## Step 5 — Output

### Triage table

| Ticket ID | Summary | Category | Severity | Route to | Workaround | Pattern cluster |
|---|---|---|---|---|---|---|
| T-002 | AUTH-500 error on login, started 9pm, tried cache/browser/password reset | Bug | **Critical** | Engineering — infrastructure | No known workaround | AUTH outage (4 tickets) |
| T-003 | "Authentication service unavailable" error across laptop and phone | Bug | **Critical** | Engineering — infrastructure | No known workaround | AUTH outage (4 tickets) |
| T-004 | AUTH-500 error, same issue as colleague T-002 on Novacycle account | Bug | **Critical** | Engineering — infrastructure | No known workaround | AUTH outage (4 tickets) |
| T-015 | 180k-record export timing out after ~90s, board meeting at 9am, started yesterday | Performance | **Critical** | Engineering — infrastructure | Workaround unknown — needs investigation (possible: smaller batch export or emergency support) | Performance regression |
| T-018 | Account deletion + GDPR Article 17 data removal request (email: stefan.mueller@klausengroup.de, acct: KLG-3304) | Account / Legal | **Critical** | Support + Legal/Compliance | N/A — legal obligation, must process | GDPR request |
| T-001 | Can't log in, "Invalid credentials" error despite resetting password twice, has client demo | Account/Bug | **High** | Engineering — bugs | No known workaround | AUTH outage (4 tickets) |
| T-006 | Charged twice ($149) in one billing cycle, invoices INV-8821 and INV-8847 | Account/Billing | **High** | Support (self) | Support can investigate and issue refund/credit | Billing error |
| T-010 | SAML 2.0 SSO required by enterprise policy next quarter, will remove product if unavailable | Feature request / Integration | **High** | Product + Engineering | No | Enterprise requirement |
| T-014 | Dashboard loads in 15+ seconds since update last Tuesday (was instant), degrading daily | Performance / Bug | **High** | Engineering — performance | No known workaround | Regression since release |
| T-016 | "Everything is broken. I can't do anything." — vague, no specifics | Complaint | **Medium** | Support (immediate triage call) → Engineering | Unknown — needs clarification | Escalation needed |
| T-017 | Weekly summary report numbers don't match data elsewhere | Data issue | **Medium** | Engineering — bugs / data integrity | No known workaround | Data integrity concern |
| T-005 | Unclear if Pro plan includes API access (pricing page not clear) | How-to question / Documentation | **Low** | Documentation / Support (self) | Can upgrade and test, or email sales | Documentation gap |
| T-007 | Questions about plan downgrade: timing of feature drop and prorating rules | How-to question | **Low** | Documentation / Support (self) | Support or KB article can explain standard policy | Documentation gap |
| T-008 | Feature request: bulk CSV export with date filters (currently manual copy-paste) | Feature request | **Low** | Product | Manual workaround: copy-paste data (hours of manual work per week) | Feature request |
| T-009 | Feature request: dark mode for late-night use | Feature request | **Low** | Product | N/A for feature request | Feature request |
| T-011 | Forgotten password, can't find reset option on login page | How-to question | **Low** | Documentation / Support (self) | Support can walk through standard reset flow | Documentation gap |
| T-012 | Developer looking for API documentation, can see API exists but can't find docs | How-to question / Documentation | **Low** | Documentation / Support (self) | Support can point to docs (docs likely exist but are hard to find) | Documentation gap |
| T-013 | New Pro user: questions about team invites (separate account vs shared, per-seat charges) | How-to question | **Low** | Documentation / Support (self) | Documentation or support can explain onboarding workflow | Documentation gap |

---

## Pattern summary

### **Escalations triggered**

```
PATTERN ESCALATION #1
Issue: Authentication service outage / cascading auth failures
Ticket count: 4
Affected users: 4 paying customers (Sarah Johnson, David Kim, Rachel Torres, Priya Patel)
Affected accounts: Novacycle (2 users), Brightpath, Helixgrowth
Severity: Critical
Sample ticket IDs: T-002, T-003, T-004, T-001
First reported: 2024-11-14 01:14 (Sarah Johnson)
Latest reported: 2024-11-14 04:22 (Priya Patel)
Pattern: Different error messages (Invalid credentials, AUTH-500, service unavailable) in 3-hour window suggests partial service degradation, cascading failure, or intermittent outage. All occurred between 9pm and 4am.
Workaround available: No
Recommended action: 
  1. Check auth service status and logs immediately
  2. Verify whether all auth is down or specific user cohorts
  3. Send status update to all 4 affected customers within 30 min
  4. T-002 & T-004 are same error from same account — investigate if Novacycle account is locked/throttled
```

```
PATTERN ESCALATION #2
Issue: Data export timeout + business-critical deadline
Ticket count: 1 (but time-critical)
Affected user: Marcus Chen (acme-corp.com)
Severity: Critical
Sample ticket ID: T-015
Timeline: Failing since 2024-11-14 morning, board meeting at 9am (same day)
Data size: 180,000 records
Error: Timeout after ~90 seconds with "Export failed. Please try again."
Workaround available: Unknown — needs immediate investigation
Recommended action:
  1. Acknowledge immediately (within 30 min of ticket)
  2. Investigate if 180k export is hitting timeout ceiling
  3. If yes: escalate to engineering for emergency workaround (smaller batch export, async export, etc.)
  4. Offer emergency export or data pull from support if engineering cannot fix in time for 9am meeting
```

### Regression candidates

- **T-014**: Dashboard regression linked to "update last Tuesday" — check deployment notes and performance metrics for that release
- **T-015**: Possible timeout threshold regression or performance regression concurrent with T-014 (both started/escalated on same day)

### Workaround gaps

- **T-001, T-002, T-003, T-004** (AUTH cluster): No workarounds available — users are completely blocked
- **T-014** (dashboard slowness): No workarounds — affects core workflow daily
- **T-015** (export timeout): No documented workaround — emergency support intervention needed
- **T-017** (data mismatch): No workaround documented — needs investigation

**Recommended KB articles** to reduce future tickets:
1. "How to reset your password" (would answer T-011 + likely future tickets)
2. "API access: which plans include it?" (would answer T-005)
3. "Downgrading your plan: billing & feature timeline" (would answer T-007)
4. "Understanding team invitations: account sharing and per-seat pricing" (would answer T-013)

---

## Metrics

- **Total tickets triaged**: 18
- **By severity**: Critical [5], High [4], Medium [2], Low [7]
- **By routing**: Engineering [6], Support (self) [7], Product [3], Documentation [5], Legal [1]
- **Patterns detected**: 1 critical cluster (4 tickets), 1 enterprise blocker, 5 documentation gaps

---

## Recommended immediate actions

**Right now (within 1 hour)**:
1. **T-015** (Marcus Chen): Call him directly — 9am board meeting is imminent. Offer emergency data pull if export won't complete in time.
2. **T-002, T-003, T-004** (AUTH outage): Check auth service status. If production is down, send status page update. If not, investigate whether Novacycle account is locked or experiencing throttling.

**Within 2 hours**:
3. **T-001** (Sarah Johnson): Contact about client demo — determine if she's affected by T-002/T-003/T-004 cluster or separate issue.
4. **T-018** (Stefan Mueller): Acknowledge GDPR request and provide timeline for legal team.

**Within 1 business day**:
5. Publish 4 KB articles for T-005, T-007, T-011, T-013 to deflect similar tickets.
6. Route T-010 (Noah Park / Coastlinedata): Flag SAML request to Product with "enterprise blocker" context.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 13.5/17.0 (79%) |
| Evaluated | 2026-05-02 |
| Target duration | 53653 ms |
| Target cost | $0.0778 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill classifies each ticket across multiple dimensions — category (bug/question/feature/billing), severity, and routing destination | PASS | Triage table covers all 18 tickets with Category (Bug, Account/Billing, Feature request, How-to question, Performance, Complaint, Data issue, Account/Legal), Severity (Critical/High/Medium/Low), and Route to (Engineering, Support, Product, Documentation, Legal/Compliance) columns. |
| c2 | Skill includes pattern detection — when 3 or more tickets match the same root issue, they should be grouped and escalated | PASS | Step 3 — Detect patterns explicitly groups T-001, T-002, T-003, T-004 as 'AUTH outage (4 tickets)' cluster and triggers PATTERN ESCALATION #1. Additional pattern clusters (regression candidates, documentation gaps) are also identified. |
| c3 | Skill generates a bug report or incident escalation for patterns that suggest a systemic issue — not just individual ticket responses | PASS | PATTERN ESCALATION #1 is a structured incident report listing affected users (4 paying customers), accounts (Novacycle, Brightpath, Helixgrowth), error variants, timeline, and 4-step recommended action plan including 'Check auth service status and logs immediately'. |
| c4 | Skill produces a structured triage table as output — not a prose summary of the ticket queue | PASS | A markdown table with columns '\| Ticket ID \| Summary \| Category \| Severity \| Route to \| Workaround \| Pattern cluster \|' covers all 18 tickets in row-per-ticket format. |
| c5 | Skill requires an ingest step — reading all tickets before classifying any — to enable pattern detection across the full batch | PASS | Step 1 — Ingest and normalise states 'Parsed 18 tickets from your input with reporters, error messages, timing data, and account information.' This appears before Step 2 — Classify each ticket. |
| c6 | Skill assigns a response SLA or priority to each ticket — partial credit if severity classification does this work implicitly | PARTIAL | Severity column (Critical/High/Medium/Low) implicitly conveys priority for each ticket. The 'Recommended immediate actions' section groups by time ('within 1 hour', 'within 2 hours', 'within 1 business day') but these are ad-hoc and not tied to a systematic per-ticket SLA framework. |
| c7 | Skill routes tickets to appropriate teams or owners, not just classifies them | PASS | Every ticket row includes a 'Route to' value: 'Engineering — infrastructure', 'Support (self)', 'Product', 'Documentation / Support (self)', 'Support + Legal/Compliance', 'Support (immediate triage call) → Engineering'. Routing is specific, not generic. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output is entirely a chat response. No YAML frontmatter with name, description, or argument-hint fields appears anywhere in the output. There is no evidence to verify whether the underlying skill file has valid frontmatter. |
| c9 | Output's ingest step reads ALL 18 tickets BEFORE classifying any — pattern detection requires the full batch, not sequential processing | PASS | Step 1 explicitly says 'Parsed 18 tickets from your input' (all 18) before Step 2 — Classify each ticket. The structure confirms batch-first processing. |
| c10 | Output's triage table classifies each ticket across the dimensions — category (bug / question / feature / billing), severity (critical / high / medium / low), and routing destination (engineering / billing / product / answered-in-place) | PASS | All 18 tickets appear in the table with Category values spanning Bug, Account/Billing, Feature request, How-to question, Performance, Data issue, Account/Legal; Severity values Critical through Low; and Route to values covering Engineering, Support, Product, Documentation, and Legal. |
| c11 | Output detects the login-error pattern — multiple tickets sharing the same root cause are GROUPED into a single incident or bug report, not 3 separate engineering tickets | PASS | All four auth tickets (T-001, T-002, T-003, T-004) are tagged 'AUTH outage (4 tickets)' in the Pattern cluster column and consolidated under a single PATTERN ESCALATION #1 block rather than routed as independent engineering tickets. |
| c12 | Output generates an incident escalation for the login pattern — naming the affected user count, time window, and the recommended on-call escalation (engineering rather than support resolves it individually) | PASS | PATTERN ESCALATION #1 states 'Affected users: 4 paying customers', 'First reported: 2024-11-14 01:14 / Latest reported: 2024-11-14 04:22' (time window), and routes all four tickets to 'Engineering — infrastructure' rather than individual support agents. |
| c13 | Output's structured triage table has columns — Ticket ID, Customer, Category, Severity, Routing, Priority, Pattern Group (if applicable), Suggested Owner — not a prose summary | PARTIAL | Table columns are: Ticket ID ✓, Summary (not Customer) ✗, Category ✓, Severity ✓, Route to ✓, Workaround (not Priority) ✗, Pattern cluster ✓. Missing: Customer column (customer names/emails are in the source data but not the table), a distinct Priority column separate from Severity, and a Suggested Owner column (Route to partially fills this role). |
| c14 | Output assigns a response SLA per ticket based on severity — e.g. critical: respond in 30 min; high: 2h; medium: 24h; low: 3 business days — making expectations clear | FAIL | There is no SLA column in the triage table. The 'Recommended immediate actions' section mentions 'within 1 hour' and 'within 2 hours' for a handful of tickets, but this is an informal action plan — not a systematic per-ticket SLA assignment tied to severity levels. |
| c15 | Output routes billing tickets to the billing/finance owner, feature requests to product, bugs to engineering, and questions to support agents — not just 'engineering' for everything | PASS | Feature requests (T-008, T-009) → 'Product'; bugs (T-001–T-004, T-014, T-015) → 'Engineering — infrastructure' or 'Engineering — performance'; questions (T-011, T-012, T-013) → 'Documentation / Support (self)'; billing (T-006, T-007) → 'Support (self)'. Routing is differentiated, not monolithic. |
| c16 | Output identifies tickets that can be answered from KB articles or self-serve — the support agent doesn't escalate questions that have public docs, recommending a deflection link instead | PASS | 'Recommended KB articles to reduce future tickets' explicitly lists four articles for T-011 ('How to reset your password'), T-005 ('API access: which plans include it?'), T-007 ('Downgrading your plan'), T-013 ('Understanding team invitations'). These tickets are routed to 'Documentation / Support (self)' rather than escalated to engineering. |
| c17 | Output's pattern detection rule is explicit — 3 or more tickets matching the same root cause within a defined window (e.g. 24 hours) trigger an incident escalation | FAIL | The output detects a pattern ('4 tickets in a 3-hour window') but never states the triggering rule threshold explicitly (e.g., '3 or more tickets on the same root cause within 24 hours triggers escalation'). The detection outcome is present but the rule that fires it is not articulated. |
| c18 | Output addresses tickets that need follow-up classification — e.g. 'needs more info from customer' tickets get a separate state, not classified as resolved or stuck | PARTIAL | T-016 ('Everything is broken') is routed to 'Support (immediate triage call) → Engineering' signalling that more information is needed before classification. T-017 ('report data looks wrong') is classified as Medium/Data issue/Engineering without a 'needs more info' flag despite lacking specifics. Partial coverage — only one of the two vague tickets receives a distinct follow-up state. |

### Notes

The output is a strong, well-structured triage run that correctly handles the core requirements: batch ingest before classification, multi-dimensional classification for all 18 tickets, pattern detection grouping the 4-ticket AUTH cluster into a single escalation, differentiated routing across engineering/product/support/legal, and proactive KB deflection recommendations. It falls short on three criteria: (1) no YAML frontmatter is visible in the captured output (c8), (2) no per-ticket SLA column tied to severity levels (c14), and (3) the pattern detection threshold rule is never stated explicitly — we see the detection outcome but not the rule that triggers it (c17). The triage table also lacks a Customer column and doesn't distinguish Priority from Severity as separate columns (c13 PARTIAL). These gaps bring the score to 79.4%, just below the 80% PASS threshold.
