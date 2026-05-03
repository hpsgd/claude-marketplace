# Test: Triage tickets

Scenario: Testing whether the triage-tickets skill classifies tickets across all required dimensions, includes pattern detection, and produces a structured triage table.

## Prompt


/support:triage-tickets for this batch of 18 new support tickets received overnight, ranging from billing questions to feature requests to what appear to be related login errors from multiple customers.

---

**T-001** | sarah.johnson@brightpath.io | 2024-11-14 01:14
Subject: Can't log in — getting "Invalid credentials" error
Body: Hi, I've been locked out since late last night. My password is definitely correct — I reset it twice and it still gives me "Invalid credentials" when I try to sign in. Please help urgently, I have a client demo first thing this morning.

**T-002** | david.kim@novacycle.com | 2024-11-14 02:41
Subject: Authentication failing since 9pm — AUTH-500 error
Body: I'm getting an AUTH-500 error every time I try to log in. It started around 9pm last night. I've cleared my cache, tried a different browser, and reset my password. Same error. Is there an outage?

**T-003** | rachel.torres@helixgrowth.co | 2024-11-14 03:07
Subject: "Authentication service unavailable" — locked out
Body: Every time I try to log in I get "Authentication service unavailable. Please try again later." I've been trying for two hours. This is happening on both my laptop and my phone. My account is rachel.torres@helixgrowth.co.

**T-004** | priya.patel@stackvault.io | 2024-11-14 04:22
Subject: Login broken — same AUTH error as my colleague
Body: My colleague David Kim emailed you earlier about an AUTH-500 error. I'm having the exact same issue. We're both on the same account (Novacycle). Something is definitely wrong on your end.

**T-005** | james.liu@foundryops.com | 2024-11-14 03:55
Subject: Does the Pro plan include API access?
Body: Hi, I'm on the Starter plan and considering upgrading. I can't find a clear answer on your pricing page about whether the Pro plan includes API access, or if that's an add-on. Can you clarify before I upgrade?

**T-006** | emma.wilson@pearlanalytics.io | 2024-11-14 05:11
Subject: Charged twice this billing cycle
Body: I noticed two separate charges of $149 on my credit card this month, both labelled "Turtlestack Pro". My billing period runs the 1st to the 1st — there should only be one charge. Invoice numbers INV-8821 and INV-8847. Please advise.

**T-007** | carlos.mendez@lightspeedlogic.com | 2024-11-14 06:30
Subject: Downgrading from Pro to Starter — what happens to billing?
Body: I'd like to downgrade my plan at the end of this billing cycle. Can you tell me: do I keep Pro features until the end of the period, or do they drop immediately? And is there any prorating if I downgrade mid-cycle in the future? Thanks.

**T-008** | tom.bradley@northernedge.co | 2024-11-14 00:58
Subject: Feature request: bulk CSV export
Body: We've been manually copying data out of reports for months. A bulk CSV export of all report data with date filters would save us hours a week. Is this on your roadmap? Happy to elaborate on the use case if helpful.

**T-009** | fatima.alhassan@meridianux.com | 2024-11-14 01:45
Subject: Feature request: dark mode
Body: I spend a lot of time in the platform late at night and the white interface is pretty harsh on the eyes. Dark mode would be a huge quality-of-life improvement. Lots of tools have this now — any plans to add it?

**T-010** | noah.park@coastlinedata.io | 2024-11-14 07:02
Subject: SSO / SAML integration request
Body: Our company is rolling out SSO across all SaaS tools next quarter. We'll need to remove any tool that doesn't support SAML 2.0. Do you have a SAML integration, or is it on the roadmap? If so, what's the timeline?

**T-011** | alex.rivera@sunriseventures.co | 2024-11-14 02:10
Subject: How do I reset my password?
Body: Hi, I've forgotten my password and can't find the reset option on the login page. Can you walk me through how to reset it?

**T-012** | diane.foster@trellismgmt.com | 2024-11-14 04:50
Subject: Where is the API documentation?
Body: I'm a developer trying to integrate your API into our internal tooling. I can see there's an API but I can't find the documentation. Can you point me to the right place?

**T-013** | jake.morrison@blueridgecorp.com | 2024-11-14 06:15
Subject: How do I add team members to my account?
Body: I've just signed up on the Pro plan and I want to invite two colleagues. I can see a "Team" section in settings but I'm not sure what happens when I invite someone — do they get a separate account, or share mine? And is there a per-seat charge?

**T-014** | chloe.wang@vertexlabs.io | 2024-11-14 05:38
Subject: Dashboard taking 15+ seconds to load
Body: Since the update last Tuesday our main dashboard takes 15 seconds or more to load. Before that it was almost instant. I'm in Sydney on a 500Mbps connection so it's not my internet. It's been getting worse each day. Can you look into this?

**T-015** | marcus.chen@acme-corp.com | 2024-11-14 06:58
Subject: URGENT: Data export timing out — board meeting at 9am
Body: Our 180,000-record customer export has been failing since yesterday morning. Every attempt runs for about 90 seconds then fails with "Export failed. Please try again." I have a board meeting at 9am and need this data. Is there a workaround?

**T-016** | ben.adams@forgewire.co | 2024-11-14 03:20
Subject: Nothing is working
Body: Everything is broken. I can't do anything. Please help.

**T-017** | lily.chen@moonshotmedia.co | 2024-11-14 07:45
Subject: The report data looks wrong
Body: The numbers in my weekly summary report don't match what I see elsewhere. Something is off. Please check.

**T-018** | stefan.mueller@klausengroup.de | 2024-11-14 08:01
Subject: Account deletion and GDPR data removal request
Body: I would like to delete my account and request that all personal data associated with my account (email stefan.mueller@klausengroup.de, account ID KLG-3304) be permanently deleted in accordance with my rights under GDPR Article 17. Please confirm receipt and provide a timeline for completion.

---

Execution requirements (the triage output MUST follow these conventions):

- **Pattern Detection Rule (state explicitly at top)** — a single sentence: "Pattern escalation rule: 3 or more tickets matching the same root cause within a 24-hour window trigger an incident escalation rather than individual handling."
- **SLA Table (state once, then apply)** — declare the SLA-by-severity once near the top:
  ```
  | Severity | First-response SLA |
  |----------|--------------------|
  | Critical | 30 minutes         |
  | High     | 2 hours            |
  | Medium   | 24 hours           |
  | Low      | 3 business days    |
  ```
- **Triage Table** — exact columns in this order: `Ticket ID | Customer | Category | Severity | Priority | SLA | Routing | Suggested Owner | Pattern Group | State`. Every row populates EVERY column. State values: `Triage`, `Routed`, `Pattern-grouped`, `Needs-more-info`, `Deflected`.
- **"Needs-more-info" state** — apply this state to BOTH T-016 ("Everything is broken") and T-017 ("report data looks wrong") because they lack specifics. They are NOT classified as bugs without first asking the customer for reproduction details.
- **Pattern group for login errors** — group T-001, T-002, T-003, T-004 into a single Pattern Group (e.g. `PG-AUTH-500`) and emit ONE incident escalation row referencing the group rather than four individual engineering tickets. State the affected user count (4), the time window (~6 hours), and recommend on-call engineering escalation.
- **Routing diversity** — billing tickets (T-006, T-007) → Billing/Finance owner; feature requests (T-008, T-009, T-010) → Product owner; performance/data bugs (T-014, T-015) → Engineering; how-to questions with public docs (T-011, T-012, T-013) → Support agent with a deflection link to the KB; GDPR (T-018) → Legal/Privacy owner.

## Criteria


- [ ] PASS: Skill classifies each ticket across multiple dimensions — category (bug/question/feature/billing), severity, and routing destination
- [ ] PASS: Skill includes pattern detection — when 3 or more tickets match the same root issue, they should be grouped and escalated
- [ ] PASS: Skill generates a bug report or incident escalation for patterns that suggest a systemic issue — not just individual ticket responses
- [ ] PASS: Skill produces a structured triage table as output — not a prose summary of the ticket queue
- [ ] PASS: Skill requires an ingest step — reading all tickets before classifying any — to enable pattern detection across the full batch
- [ ] PARTIAL: Skill assigns a response SLA or priority to each ticket — partial credit if severity classification does this work implicitly
- [ ] PASS: Skill routes tickets to appropriate teams or owners, not just classifies them
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output's ingest step reads ALL 18 tickets BEFORE classifying any — pattern detection requires the full batch, not sequential processing
- [ ] PASS: Output's triage table classifies each ticket across the dimensions — category (bug / question / feature / billing), severity (critical / high / medium / low), and routing destination (engineering / billing / product / answered-in-place)
- [ ] PASS: Output detects the login-error pattern — multiple tickets sharing the same root cause are GROUPED into a single incident or bug report, not 3 separate engineering tickets
- [ ] PASS: Output generates an incident escalation for the login pattern — naming the affected user count, time window, and the recommended on-call escalation (engineering rather than support resolves it individually)
- [ ] PASS: Output's structured triage table has columns — Ticket ID, Customer, Category, Severity, Routing, Priority, Pattern Group (if applicable), Suggested Owner — not a prose summary
- [ ] PASS: Output assigns a response SLA per ticket based on severity — e.g. critical: respond in 30 min; high: 2h; medium: 24h; low: 3 business days — making expectations clear
- [ ] PASS: Output routes billing tickets to the billing/finance owner, feature requests to product, bugs to engineering, and questions to support agents — not just "engineering" for everything
- [ ] PASS: Output identifies tickets that can be answered from KB articles or self-serve — the support agent doesn't escalate questions that have public docs, recommending a deflection link instead
- [ ] PASS: Output's pattern detection rule is explicit — 3 or more tickets matching the same root cause within a defined window (e.g. 24 hours) trigger an incident escalation
- [ ] PARTIAL: Output addresses tickets that need follow-up classification — e.g. "needs more info from customer" tickets get a separate state, not classified as resolved or stuck
