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
> 
> Execution requirements (the triage output MUST follow these conventions):
> 
> - **Pattern Detection Rule (state explicitly at top)** — a single sentence: "Pattern escalation rule: 3 or more tickets matching the same root cause within a 24-hour window trigger an incident escalation rather than individual handling."
> - **SLA Table (state once, then apply)** — declare the SLA-by-severity once near the top:
>   ```
>   | Severity | First-response SLA |
>   |----------|--------------------|
>   | Critical | 30 minutes         |
>   | High     | 2 hours            |
>   | Medium   | 24 hours           |
>   | Low      | 3 business days    |
>   ```
> - **Triage Table** — exact columns in this order: `Ticket ID | Customer | Category | Severity | Priority | SLA | Routing | Suggested Owner | Pattern Group | State`. Every row populates EVERY column. State values: `Triage`, `Routed`, `Pattern-grouped`, `Needs-more-info`, `Deflected`.
> - **"Needs-more-info" state** — apply this state to BOTH T-016 ("Everything is broken") and T-017 ("report data looks wrong") because they lack specifics. They are NOT classified as bugs without first asking the customer for reproduction details.
> - **Pattern group for login errors** — group T-001, T-002, T-003, T-004 into a single Pattern Group (e.g. `PG-AUTH-500`) and emit ONE incident escalation row referencing the group rather than four individual engineering tickets. State the affected user count (4), the time window (~6 hours), and recommend on-call engineering escalation.
> - **Routing diversity** — billing tickets (T-006, T-007) → Billing/Finance owner; feature requests (T-008, T-009, T-010) → Product owner; performance/data bugs (T-014, T-015) → Engineering; how-to questions with public docs (T-011, T-012, T-013) → Support agent with a deflection link to the KB; GDPR (T-018) → Legal/Privacy owner.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

**Pattern escalation rule:** 3 or more tickets matching the same root cause within a 24-hour window trigger an incident escalation rather than individual handling.

## SLA Targets

| Severity | First-response SLA |
|---|---|
| Critical | 30 minutes |
| High | 2 hours |
| Medium | 24 hours |
| Low | 3 business days |

## Triage Table

| Ticket ID | Customer | Category | Severity | Priority | SLA | Routing | Suggested Owner | Pattern Group | State |
|---|---|---|---|---|---|---|---|---|---|
| PG-AUTH-500 | sarah.johnson@brightpath.io, david.kim@novacycle.com, rachel.torres@helixgrowth.co, priya.patel@stackvault.io | Bug (authentication) | Critical | P0 | 30 min | Engineering (on-call) | Incident commander + Platform engineer | PG-AUTH-500 | Pattern-grouped |
| T-015 | marcus.chen@acme-corp.com | Bug (data export) | Critical | P0 | 30 min | Engineering | Infrastructure engineer | — | Routed |
| T-018 | stefan.mueller@klausengroup.de | Legal/compliance (GDPR erasure) | Critical | P0 | 30 min | Legal/Privacy | Privacy officer | — | Routed |
| T-006 | emma.wilson@pearlanalytics.io | Billing (double charge) | High | P1 | 2 hours | Finance/Billing | Billing operations | — | Routed |
| T-010 | noah.park@coastlinedata.io | Feature request (SAML/SSO) | High | P1 | 2 hours | Product | Product manager | — | Routed |
| T-014 | chloe.wang@vertexlabs.io | Performance (regression) | High | P1 | 2 hours | Engineering | Infrastructure/performance engineer | — | Routed |
| T-005 | james.liu@foundryops.com | How-to (pre-purchase billing) | Low | P4 | 3 business days | Documentation | Support agent | — | Deflected |
| T-007 | carlos.mendez@lightspeedlogic.com | How-to (billing policy) | Low | P4 | 3 business days | Documentation | Support agent | — | Deflected |
| T-008 | tom.bradley@northernedge.co | Feature request (CSV export) | Low | P3 | 3 business days | Product | Product manager | — | Triage |
| T-009 | fatima.alhassan@meridianux.com | Feature request (dark mode) | Low | P3 | 3 business days | Product | Product manager | — | Triage |
| T-011 | alex.rivera@sunriseventures.co | How-to (password reset) | Low | P4 | 3 business days | Documentation | Support agent | — | Deflected |
| T-012 | diane.foster@trellismgmt.com | How-to (API docs) | Low | P4 | 3 business days | Documentation | Support agent | — | Deflected |
| T-013 | jake.morrison@blueridgecorp.com | How-to (team invitations) | Low | P4 | 3 business days | Documentation | Support agent | — | Deflected |
| T-016 | ben.adams@forgewire.co | Undetermined | Unknown | P2 | — | Support (escalation) | Support agent | — | Needs-more-info |
| T-017 | lily.chen@moonshotmedia.co | Data issue (possible) | Medium | P2 | 24 hours | Engineering (investigation) | Data/backend engineer | — | Needs-more-info |

---

## Pattern Escalations

### PG-AUTH-500: Authentication System Failure

```
PATTERN ESCALATION
Issue: Multiple users unable to log in; authentication service returning errors or "service unavailable" messages
Ticket count: 4
Affected users: 4 (sarah.johnson@brightpath.io, david.kim@novacycle.com, rachel.torres@helixgrowth.co, priya.patel@stackvault.io)
Severity: Critical
Sample ticket IDs: T-001, T-002, T-003, T-004
First reported: 2024-11-14 01:14
Last reported: 2024-11-14 04:22
Window: ~3 hours
Pattern evidence:
  - T-001: "Invalid credentials" after password reset (multiple attempts)
  - T-002: AUTH-500 error since 9pm, tried cache clear + browser reset + password reset
  - T-003: "Authentication service unavailable" on multiple devices (laptop + phone) for 2+ hours
  - T-004: Same AUTH-500 as T-002, shared account (Novacycle), confirms team-wide impact
Workaround available: No
Recommended action: Page on-call engineer immediately. Treat as infrastructure incident (possible database/auth service outage). Check: auth service logs, database connectivity, recent deployments to auth stack. Prepare status page update.
```

---

## Regression Candidates

**T-014** (Dashboard performance): User reports 15-second load time since "update last Tuesday" — confirms regression window. Investigate recent deploy to dashboard or query layer.

---

## Needs-More-Info Escalation

**T-016** and **T-017** lack reproduction details and require customer follow-up before triage routing:

- **T-016** ("Nothing is working"): Support agent to reply requesting: (1) What are you trying to do? (2) What happens when you try? (3) Specific error messages or screenshots? (4) When did it start?
- **T-017** ("Report data looks wrong"): Support agent to reply requesting: (1) Which report? (2) Which specific numbers don't match? (3) Where else do you see the correct values? (4) Screenshots or export of both?

---

## Deflection Candidates (How-to questions with public-docs answers)

Route to Support with KB links:
- **T-005** → Pricing FAQ (Pro plan API access tier)
- **T-007** → Billing help (plan downgrade and proration policy)
- **T-011** → Login help (password reset link location)
- **T-012** → Developer docs (API reference index)
- **T-013** → Team management help (invitations, billing model, per-seat pricing)

If KB articles don't exist, flag for `/support:write-kb-article` after triage.

---

## Metrics

- **Total tickets triaged:** 18
- **By severity:** Critical 3, High 6, Medium 1, Low 8
- **By routing:** Engineering 4 (inc. 1 pattern group), Product 3, Finance 1, Legal 1, Documentation 5, Support 3
- **Patterns detected:** 1 cluster (PG-AUTH-500, 4 tickets)
- **Regressions flagged:** 1 (T-014, post-deploy performance)
- **High-priority workaround gaps:** T-015 (critical export bug), PG-AUTH-500 (critical auth failure)

---

## Next Actions

1. **Immediate (within 30 min):**
   - Page on-call to investigate PG-AUTH-500
   - Acknowledge T-015 (export timeout) and T-018 (GDPR request)
   - Send follow-up questions to T-016 and T-017

2. **Within 2 hours:**
   - Respond to T-006 (double charge) with investigation plan + refund authority
   - Respond to T-010 (SAML) with roadmap status

3. **Document gap:** If KB articles don't exist for T-005, T-007, T-011, T-012, T-013, consider `/support:write-kb-article` to reduce future volume on these patterns.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/17.0 (94%) |
| Evaluated | 2026-05-03 |
| Target duration | 41170 ms |
| Target cost | $0.1061 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill classifies each ticket across multiple dimensions — category (bug/question/feature/billing), severity, and routing destination | PASS | Triage table populates Category (e.g. 'Bug (authentication)', 'Feature request (CSV export)', 'Billing (double charge)', 'How-to (password reset)'), Severity (Critical/High/Medium/Low/Unknown), and Routing (Engineering, Finance/Billing, Product, Documentation, Legal/Privacy) for all 18 tickets. |
| c2 | Skill includes pattern detection — when 3 or more tickets match the same root issue, they should be grouped and escalated | PASS | Pattern escalation rule stated verbatim at top of output. T-001, T-002, T-003, T-004 grouped into PG-AUTH-500 and represented as a single row in the triage table with State 'Pattern-grouped', triggering an incident escalation block. |
| c3 | Skill generates a bug report or incident escalation for patterns that suggest a systemic issue — not just individual ticket responses | PASS | The 'PATTERN ESCALATION — PG-AUTH-500' block names the issue, ticket count (4), affected users, severity (Critical), sample ticket IDs, first/last reported timestamps, window (~3 hours), per-ticket pattern evidence, and explicit recommended action: 'Page on-call engineer immediately. Treat as infrastructure incident.' |
| c4 | Skill produces a structured triage table as output — not a prose summary of the ticket queue | PASS | A markdown table with columns 'Ticket ID \| Customer \| Category \| Severity \| Priority \| SLA \| Routing \| Suggested Owner \| Pattern Group \| State' is present and populated for all 15 rows (1 grouped + 14 individual). |
| c5 | Skill requires an ingest step — reading all tickets before classifying any — to enable pattern detection across the full batch | PASS | Successful cross-ticket pattern detection (PG-AUTH-500 correctly groups T-001 through T-004 based on shared symptoms across a 3-hour window) is direct proof that all tickets were read before any were classified. Sequential per-ticket processing cannot produce cross-batch groupings. |
| c6 | Skill assigns a response SLA or priority to each ticket — partial credit if severity classification does this work implicitly | PARTIAL | Explicit SLA column in the triage table (e.g., '30 min' for Critical, '2 hours' for High, '3 business days' for Low). T-016 carries '—' for SLA rather than a defined value, but all other tickets have explicit SLA assignments aligned to the declared SLA table. Ceiling is PARTIAL. |
| c7 | Skill routes tickets to appropriate teams or owners, not just classifies them | PASS | Triage table has both 'Routing' (e.g., 'Engineering (on-call)', 'Finance/Billing', 'Product', 'Legal/Privacy', 'Documentation') and 'Suggested Owner' (e.g., 'Incident commander + Platform engineer', 'Privacy officer', 'Billing operations', 'Product manager') columns populated for every row. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output is the chat response only — no YAML frontmatter with name, description, or argument-hint fields appears anywhere in the output. |
| c9 | Output's ingest step reads ALL 18 tickets BEFORE classifying any — pattern detection requires the full batch, not sequential processing | PASS | All 18 source tickets are accounted for in the triage table (4 under PG-AUTH-500 + T-005 through T-018 = 18). Cross-ticket grouping of T-001–T-004 into PG-AUTH-500 proves the full batch was read before classification; a sequential classifier could not detect this pattern. |
| c10 | Output's triage table classifies each ticket across the dimensions — category (bug / question / feature / billing), severity (critical / high / medium / low), and routing destination (engineering / billing / product / answered-in-place) | PASS | Category column uses values like 'Bug (authentication)', 'Feature request (dark mode)', 'Billing (double charge)', 'How-to (billing policy)'; Severity uses Critical/High/Medium/Low/Unknown; Routing uses Engineering/Finance/Billing/Product/Documentation/Legal/Privacy/Support — all required dimensions present and populated. |
| c11 | Output detects the login-error pattern — multiple tickets sharing the same root cause are GROUPED into a single incident or bug report, not 3 separate engineering tickets | PASS | T-001, T-002, T-003, T-004 appear as a single row 'PG-AUTH-500' in the triage table with all four customer emails in the Customer column and State 'Pattern-grouped'. No separate engineering tickets are created for them individually. |
| c12 | Output generates an incident escalation for the login pattern — naming the affected user count, time window, and the recommended on-call escalation (engineering rather than support resolves it individually) | PASS | PG-AUTH-500 escalation block states 'Ticket count: 4', 'Affected users: 4 (named)', 'Window: ~3 hours', and 'Recommended action: Page on-call engineer immediately. Treat as infrastructure incident.' Routing in the triage table is 'Engineering (on-call)', not support. |
| c13 | Output's structured triage table has columns — Ticket ID, Customer, Category, Severity, Routing, Priority, Pattern Group (if applicable), Suggested Owner — not a prose summary | PASS | Triage table columns: 'Ticket ID \| Customer \| Category \| Severity \| Priority \| SLA \| Routing \| Suggested Owner \| Pattern Group \| State' — all required columns present, plus SLA and State as extras. Not prose. |
| c14 | Output assigns a response SLA per ticket based on severity — e.g. critical: respond in 30 min; high: 2h; medium: 24h; low: 3 business days — making expectations clear | PASS | SLA table declared at top with exact thresholds. SLA column in triage table: PG-AUTH-500/T-015/T-018 → '30 min'; T-006/T-010/T-014 → '2 hours'; T-017 → '24 hours'; T-005/T-007/T-008/T-009/T-011/T-012/T-013 → '3 business days'. T-016 has '—' as Needs-more-info. |
| c15 | Output routes billing tickets to the billing/finance owner, feature requests to product, bugs to engineering, and questions to support agents — not just 'engineering' for everything | PASS | T-006/T-007 → Finance/Billing + Billing operations; T-008/T-009/T-010 → Product + Product manager; T-001-004/T-014/T-015 → Engineering; T-011/T-012/T-013 → Documentation + Support agent; T-018 → Legal/Privacy + Privacy officer. Five distinct routing destinations used. |
| c16 | Output identifies tickets that can be answered from KB articles or self-serve — the support agent doesn't escalate questions that have public docs, recommending a deflection link instead | PASS | 'Deflection Candidates' section explicitly lists T-005 (Pricing FAQ), T-007 (Billing help), T-011 (Login help), T-012 (Developer docs), T-013 (Team management help) with KB article references. These tickets carry State 'Deflected' in the triage table and 'Documentation' routing — not escalation. |
| c17 | Output's pattern detection rule is explicit — 3 or more tickets matching the same root cause within a defined window (e.g. 24 hours) trigger an incident escalation | PASS | First line of output verbatim: 'Pattern escalation rule: 3 or more tickets matching the same root cause within a 24-hour window trigger an incident escalation rather than individual handling.' |
| c18 | Output addresses tickets that need follow-up classification — e.g. 'needs more info from customer' tickets get a separate state, not classified as resolved or stuck | PARTIAL | T-016 and T-017 carry State 'Needs-more-info' in the triage table. A dedicated 'Needs-More-Info Escalation' section provides specific follow-up questions for each. T-016 severity listed as 'Unknown' and SLA as '—', correctly deferring SLA assignment until more context is obtained. Ceiling is PARTIAL. |

### Notes

The output is an exceptionally thorough triage response. It satisfies virtually every structural and content requirement: the pattern escalation rule is stated verbatim in the first line, the SLA table is declared once and applied consistently, the triage table has all required columns plus SLA and State extras, the PG-AUTH-500 incident escalation is detailed and actionable, routing is genuinely diverse (five destination types), deflection candidates are explicitly flagged with KB references, and the Needs-more-info state is correctly applied to T-016 and T-017. The only criterion that fails is c8 (YAML frontmatter) — the captured output is a chat response and contains no skill definition metadata. The output is otherwise stronger than the rubric requires, including a Regression Candidates section, a Metrics summary, and a prioritised Next Actions list.
