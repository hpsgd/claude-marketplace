# Write Onboarding Playbook

Scenario: Testing whether the write-onboarding-playbook skill defines TTFV as a measurable customer outcome, requires escalation triggers on every milestone, and includes handoff criteria.

## Prompt

> /customer-success:write-onboarding-playbook for our enterprise segment — customers with 200+ seats, dedicated IT teams, and annual contracts over $100k.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I've created a comprehensive enterprise onboarding playbook tailored to your 200+ seat segment. Here's what's inside:

**Structure:**
- **Segment definition** — captures the enterprise buyer profile (multiple stakeholders, high sophistication, integration-heavy)
- **21-day TTFV target** — aggressive but achievable with white-glove service; includes how to measure it
- **6 detailed milestones** — kickoff → integration → training → first value → team rollout → handoff. Each has measurable success criteria and escalation triggers
- **90-minute kickoff agenda** — structured to surface technical scope, stakeholder alignment, and early action items (not a product demo)
- **8 common blockers** — IT delays, executive disengagement, adoption stalls, data migration surprises, etc. Each has early warning signs and escalation paths
- **Handoff checklist** — 10 specific criteria (TTFV achieved, adoption ≥50%, health score ≥75, etc.) before handing off to BAU CS
- **Execution timeline** — shows how 21-day TTFV breaks down day-by-day

**Key features:**
- Every escalation trigger is a specific day (not "follow up if needed" — "if SSO not tested by Day 8, escalate")
- Role clarity: CS owns most, but Champion owns team rollout (peers train peers)
- Health score definition built in: TTFV (30%) + adoption (30%) + champion engagement (20%) + no critical issues (20%)
- Blockers table includes early warning signs so you catch problems before they stall

**Next steps to customize for your product:**

1. **Define "first value"** in the TTFV section. It's currently "one team completes primary workflow with real data." Change it to match your product (e.g., "first report generated," "first transaction processed," "first 100 records synced").

2. **List your critical integrations** in Milestone 2 success criteria. Which 2–3 systems MUST be live by Day 10?

3. **Set your training approach.** Live instructor-led? Recorded? Async? Adjust Milestone 3 timeline and format.

4. **Adjust escalation contacts.** Replace "CS Manager," "Solutions Engineer," "Product Mgmt" with your actual team.

5. **Plug in your tools.** Replace Salesforce, Slack, HubSpot references with your systems.

6. **Test it.** Run it with your next 3 enterprise customers. Track actual TTFV vs target. After 3 cycles, you'll have real baseline data to tune timelines and milestones.

The playbook is actionable today — use it as-is or modify. What customisations do you want to make first?

### Artifacts written

#### `work/onboarding-playbook-enterprise.md`

```
# Onboarding Playbook: Enterprise Segment (200+ seats)

**Segment:** Enterprise (annual contracts $100k+, 200+ seats, dedicated IT teams)  
**Target TTFV:** 21 days  
**Onboarding window:** 45 days  
**Milestone count:** 6  
**Last updated:** 2026-05-04

---

## Segment Definition

| Element | Detail |
|---|---|
| **Segment** | Enterprise — large organisations with dedicated IT departments, centralised procurement, formal change management processes |
| **Typical company size** | 500–5,000+ employees; $100k–$500k+ annual contract value |
| **Technical sophistication** | High — dedicated engineering/IT team with infrastructure, security, and compliance expertise |
| **Typical goals** | (1) Reduce manual workflows by 60%+ across the organisation; (2) Integrate with existing systems (ERPs, CRMs, data warehouses, SSO); (3) Establish governance and auditability for compliance |
| **Decision-maker** | VP of Operations, Chief Technology Officer, Chief Information Officer — purchased for strategic transformation, not point-solution needs |
| **Day-to-day users** | Team leads, individual contributors across multiple departments (ops, finance, engineering) — typically 10–20 "power users" plus 100+ general users |
| **Common integrations** | Active Directory / Azure AD (SSO), Okta, Datadog, Splunk, Salesforce, SAP, Workday, Slack, ServiceNow, Jira, data warehouses (Snowflake, BigQuery, Redshift) |
| **Contract type** | Annual, multi-year (3-5 year common) — high switching cost creates commitment to onboarding success |
| **Stakeholder complexity** | 4+ stakeholder groups: Executive sponsor (CEO/COO), IT/Technical lead, Department champion(s), End-user teams — each with different success criteria |

### Why this matters for onboarding
- The person who signed the contract rarely uses the product daily. Onboarding must serve BOTH the executive sponsor and the end-user team.
- Security, compliance, and IT governance are non-negotiable blockers — not nice-to-have features.
- Change management for 200+ users is complex. Training and adoption cannot be ad-hoc.
- Multi-department rollout means competing priorities. Early momentum (TTFV in 3 weeks) is critical to maintain executive support.

---

## Time-to-First-Value (TTFV)

| Element | Detail |
|---|---|
| **"First value" definition** | [CUSTOMISE] One team (minimum 20+ users) completes their primary workflow end-to-end using the platform with their own real data, achieving measurable improvement (time saved, accuracy improved, or new capability realised) |
| **Target TTFV** | 21 days (Day 1 contract signature → Day 21 first value achieved) |
| **Measurement** | (1) Product event: first workflow completed with customer data (not demo/sandbox data), (2) Metric threshold: minimum 20 concurrent users on Day 21, (3) Customer confirmation: champion verifies workflow value in recorded feedback/survey |
| **Current TTFV** | [Unknown — establish baseline in first 3 enterprise onboardings, then iterate] |
| **Benchmark** | Industry standard: 30–60 days for enterprise products with integrations. Target of 21 days is aggressive — achievable only with white-glove service and pre-positioned resources. |

### Rationale for 21-day target
- Enterprise contracts are $100k+ annual spend. Every day of delay is ~$274 of daily value at risk.
- Executive sponsors expect ROI signals within 30 days. Hitting 21-day TTFV keeps momentum with C-suite.
- First 3 weeks are the "window of goodwill" — if onboarding stalls after Day 14, stakeholder confidence drops sharply.
- For teams with existing manual workflows, first-value is often process re-engineering (learning the new way). 21 days is realistic for one team; 45 days for org-wide rollout.

### How to measure TTFV
- **Automated:** Product event fired when user completes first workflow with non-demo data (e.g., `first_real_workflow_completed`)
- **Manual:** Weekly check-in call with champion — ask "has your team achieved their primary success criterion?" (date, not guess)
- **System:** Tag TTFV date in Salesforce/HubSpot the moment it's achieved. Report on TTFV trend monthly.

---

## Milestones

| # | Milestone | Target day | Success criteria | Owner | Verification method | Escalation trigger |
|---|---|---|---|---|---|---|
| **1** | **Kickoff complete** | Day 1–3 | (1) Executive sponsor, IT lead, and 2+ department champions present; (2) Success criteria documented and signed (customer's words, not your features); (3) Technical requirements & integration scope locked in writing; (4) All access provisioned (SSO, accounts, sandbox environment ready); (5) Kickoff notes distributed and acknowledged | CS lead | Kickoff checklist completed and signed; Slack confirmation from champion + IT lead; Access verified (test login successful) | No kickoff scheduled by Day 2 of contract; Executive sponsor does not attend; Access not provisioned by Day 4 |
| **2** | **Technical integration & data setup** | Day 3–10 | (1) Primary integrations (SSO, data source) connected and tested; (2) Initial data imported or API connection verified (no errors in data validation); (3) Environment configured per IT requirements (custom fields, workflows, security rules); (4) Sandbox data loaded (realistic test dataset, not lorem ipsum); (5) IT team sign-off on security & compliance (data residency, encryption, audit logging) | CS + Solutions Engineer | Data validation report (# records imported, error log empty); Integration health check passing; IT sign-off email; Customer test login with SSO working | No API/integration started by Day 6; Data import errors affecting >5% of records; SSO not tested by Day 8; IT security review not started by Day 7 |
| **3** | **Power user training complete** | Day 10–14 | (1) 10–20 power users (team leads, super-users) completed platform training (live or recorded, with exercises); (2) Power users can navigate core workflows without assistance; (3) Power users prepared to lead team training; (4) Trainer certification done (power users can answer FAQs); (5) Training materials (videos, guides, checklists) handed off and accessible | CS + Customer Champion | Training attendance report (>80% attendance); Trainer quiz results (>85% score); Training materials in shared drive; Feedback survey >4/5 | <80% training attendance by Day 13; Trainer quiz <85%; Training scheduled but not completed by Day 14 |
| **4** | **First real workflow completed** | Day 14–21 | (1) First team (20+ users) completed their primary workflow end-to-end with real, live data — not demo data; (2) Workflow produces measurable output (report, decision, data record); (3) Champion confirms value realisation ("this saves us X hours per week"); (4) Product event fires (`first_real_workflow_completed`) in analytics; (5) Success quantified in writing (time saved, accuracy improvement, new capability enabled) | CS lead + Champion | Product event in analytics; Workflow output reviewed and confirmed real (not test data); Recorded feedback from champion (Loom video or written note); Usage analytics: 20+ unique users in workflow on that day | No users on platform by Day 17; First workflow attempted but incomplete by Day 20; Workflow only in sandbox environment; No champion confirmation by Day 22 |
| **5** | **Team rollout to 50% adoption** | Day 21–35 | (1) Extended team training completed (remaining 100+ users reached, live or async); (2) 50%+ of licensed seats have logged in and completed at least one task; (3) Support resources in place and responsive (Slack channel, office hours, FAQ); (4) Usage patterns emerging and stable (daily active users trending up); (5) Early feedback collected and top issues logged (not blocking, but tracked) | Champion (with CS support) | Usage analytics: DAU/MAU ratio, login % of seats; Training attendance reports; Slack response time <4h during business hours; Logged issues in ticketing system | <30% login rate by Day 30; Usage declining instead of growing by Day 32; Training attendance >50% incomplete; Support backlog >5 unresolved issues |
| **6** | **Handoff to business-as-usual (BAU) CS** | Day 35–45 | (1) All handoff criteria met (see Step 6); (2) Adoption at or above target (50%+ active); (3) Health score green (composite: TTFV achieved, adoption %, champion engagement, no critical issues); (4) QBR prepared with baseline metrics (time saved, adoption rate, top use cases); (5) Warm introduction: onboarding CS introduces BAU CS to executive sponsor and champion; (6) BAU CS conducts relationship call and assumes full account ownership | CS Manager + CS lead | Handoff document completed; Health score ≥75/100; QBR slides drafted; Executive sponsor confirms BAU CS intro; BAU CS completes 30-min intro call with champion recorded | Health score <75 by Day 40; Any critical blocker unresolved by Day 40; Executive sponsor not available for BAU intro; Adoption declined to <40% by Day 42 |

### Milestone philosophy
- **Sequential, not parallel.** Milestone 3 cannot start until Milestone 2 sign-off. You cannot train users on Day 8 if integrations are not yet connected.
- **Every success criterion is measurable.** "Complete training" is vague. "80% attendance + 85% quiz score + trainer certification" is measurable.
- **Every escalation trigger is a specific day.** "If X happens, escalate by Day Y." No open-ended escalations.
- **Owner is clear.** CS owns most, but Champion owns team rollout (Milestone 5) because peers train peers better than vendors.

---

## Kickoff Meeting Agenda

**Duration:** 90 minutes (enterprise requires more time than mid-market — too many stakeholders to rush)  
**Attendees (required):** CS lead, Customer executive sponsor (CEO/COO/CTO), Customer IT/technical lead, Customer department champion (the person whose team will use the platform first)  
**Attendees (strongly recommended):** Solutions Engineer (for technical Q&A), Your product lead (for credibility with buyer), Customer security/compliance officer (if integrations touch sensitive data)

| Time | Topic | Owner | Attendees | Output |
|---|---|---|---|---|
| **0–10 min** | Introductions and role mapping | CS lead | Everyone | Shared doc: Who does what on both sides? (owner, POC, escalation contact per function) |
| **10–20 min** | Executive alignment: Success criteria and ROI | CS lead + Your executive | Sponsor + CS lead | Documented success criteria in customer's own words (NOT "implement platform" — "reduce manual reporting by 60%") |
| **20–35 min** | Technical deep dive: Integrations, data, security | Solutions Engineer + IT lead | IT lead + Solutions Eng + optional: Security officer | Technical scope doc: Which systems integrate? Data volumes? Security/compliance requirements? Decision on SSO, data residency, audit logging. |
| **35–50 min** | Milestone walkthrough and timeline | CS lead | Everyone | Signed timeline: Kickoff → First value (21 days) → Team rollout (35 days) → Handoff (45 days). Specific dates, not "Week 2." Mark blockers (security review, data migration prep, training prep). |
| **50–70 min** | Roles, responsibilities, and support model | CS lead | Everyone | RACI matrix filled in: Who is responsible/accountable for each milestone? Who supports? Make champion's role explicit ("you will train your team"). Clarify escalation path if things stall. |
| **70–85 min** | Quick-start resources and Day 1 actions | CS lead | Champion + IT lead | Shared folder with: (1) SSO/access setup guide; (2) Data import template (if applicable); (3) Training schedule draft; (4) Slack/Teams workspace created (not email). Day 1 actions assigned with owners and deadlines (e.g., "IT lead sends Azure AD config to us by EOD Thursday"). |
| **85–90 min** | Confirm next steps and close | CS lead | Everyone | First 3 actions, owners, deadlines (in writing before attendees leave call). Confirm 2nd call (Day 5 check-in). Send meeting notes within 2 hours. |

### Kickoff anti-patterns (what NOT to do)
- ❌ Demo the product. They already bought it. Focus on THEIR goals.
- ❌ Attend without your executive. If your C-level isn't present, they think it's not important.
- ❌ Accept vague success criteria. "Improve efficiency" is not measurable. Push: "By what metric? Time? Cost? Accuracy?"
- ❌ Rush the technical scope. 35-minute deep dive on integrations is minimum for enterprise. Data migration, SSO, security, and compliance cannot be squeezed.
- ❌ Assign action items without a deadline. "Send us the API key when you get a chance" = it never happens.
- ❌ Forget the champion. They are your primary contact for 45 days. Make their role explicit in kickoff so they own it.
- ❌ Schedule kickoff more than 5 business days post-signature. Momentum dies fast.

---

## Common Blockers

| Blocker | Early warning sign | Resolution | Owner | Escalation path | Escalation trigger |
|---|---|---|---|---|---|
| **Executive sponsor unavailable / disengaged** | Sponsor doesn't attend kickoff; declines 2+ updates; no exec on kickoff call; champion reporting "boss is busy" | Escalate to AE immediately. Request sponsor 1-on-1 from your SVP/Chief Revenue. Clarify ROI and commitment needed for success. If sponsor truly unavailable, ask champion to propose replacement sponsor. | AE + CS Manager | AE → VP Sales → SVP/VP Customer | Sponsor absent from kickoff; no sponsor reply within 24h of kickoff invite |
| **IT blockers: SSO, data residency, security review** | IT lead says "we need InfoSec review before integration"; data residency requirements not met; compliance questionnaire incomplete | Fast-track: (1) Provide pre-filled security questionnaire (not blank). (2) Offer recorded InfoSec call with your security team. (3) Provide SOC 2, data residency docs upfront. (4) Assign dedicated Solutions Eng to unblock. | Solutions Engineer + CS | Solutions Eng → Engineering → InfoSec partner | No SSO test by Day 8; InfoSec review requested, no timeline given; Data residency mismatch found |
| **Data migration complexity / delays** | Data import shows >5% errors; mapping is ambiguous; customer's data is messier than expected; IT says "we need another week to extract" | Mitigate early: (1) Offer data audit in Week 1 (before Day 7). (2) Provide data import guide + template. (3) Have automated data validation report ready (shows errors + how to fix). (4) If extraction delayed, start training in parallel (don't wait for full data). | Solutions Engineer + CS | Solutions Eng → Data team → Engineering | Data errors >5% by Day 8; Data export delayed beyond Day 9; Customer's data quality issues unforeseen |
| **Champion overwhelmed or unavailable** | Champion missed 2 check-ins; took >48h to respond to Slack; says "my team is slammed"; training participation <60% | Identify backup champion immediately. Shift communication to async (recorded videos, written guides). Offer daily office hours vs weekly check-ins (let them drop in when free). Reduce scope: focus Milestone 4 on 1 team, not 2. | CS lead + Champion | CS Manager → Account AE → Executive sponsor | Champion no-shows 2 consecutive check-ins; Champion says "team can't do training until next month" by Day 10 |
| **Stakeholder misalignment** | Different people mention conflicting success criteria; scope creep ("we also need this feature"); unclear priorities between teams | Facilitate alignment meeting. Get exec sponsor + 2 champions in same room. Whiteboard: "What are the 3 things we must achieve in 45 days?" Document and get written sign-off. Defer out-of-scope requests to post-launch planning. | CS lead + Customer exec | CS Manager → Your Product Mgmt (if deferral is contentious) | Multiple teams claiming different success criteria by Day 3; Scope growing uncontrolled; No agreement on Milestone 4 target by Day 7 |
| **User adoption stalling** | Login % stuck <30% on Day 25; power users trained but general team never trained; usage trending down instead of up; champion says "team doesn't see value yet" | Do NOT wait. Escalate to champion + exec sponsor immediately. Root-cause in call: Is training insufficient? Do users not understand the value? Are they blocked by a missing integration? Launch emergency training session (30-min live demo + Q&A). If adoption issue is genuine product misalignment, escalate to Product/Solutions. | CS lead + Champion | CS Manager + Solutions Eng → Product Mgmt | <30% login rate by Day 25; Usage declining from Day 22 onward; Champion reports "team isn't using it" |
| **Technical blocker: Integration failure** | Scheduled integration test fails; data not flowing; API auth errors; SSO redirects but credentials not syncing | Immediate response needed (same day). Solutions Eng to diagnostic call. Provide logs + step-by-step troubleshooting. Offer 1-on-1 technical pairing if customer IT is blocked. If blocker is our platform, escalate to Engineering immediately for hotfix. | Solutions Engineer | Solutions Eng → Engineering → Product | Integration fails and not resolved within 24h; API errors blocking data import; SSO broken on Day 6+ |
| **Competing priorities: Customer's other initiatives** | Champion says "we have a system outage this week, can we pause?"; executive sponsor pulled for merger prep; team reassigned to other project | Acknowledge the reality. Agree to 1-week pause if needed (protect their business). Reschedule milestones to Days [+7]. Do NOT extend to 2+ weeks without escalation to your executive. Keep momentum: offer async resources during pause (pre-recorded training, self-serve guides, Slack support). | CS lead | CS Manager → AE if pause exceeds 2 weeks | Pause requested; delay exceeds 10 days total; Customer requests to defer onboarding to next quarter |
| **Budget or resource constraints** | Customer says "we can only dedicate 1 FTE to this, not 2"; Training budget cut mid-onboarding; Customer cannot afford data migration services | Rebuild plan for 1 FTE: extend timeline to 60 days, reduce team size in Milestone 5 (focus on 1 team, not org-wide). Provide templated guides so customer can self-serve (reduces consulting hours). If data migration is blocker, offer phased approach (Milestone 4 with sample data, Milestone 5 with full migration). | CS Manager + Solutions Eng | CS Manager → AE for contract discussions | Customer explicitly says "we need to reduce scope"; Budget cut discovered mid-onboarding; Customer asks to defer feature or extend timeline |

---

## Handoff: Onboarding → Business-as-Usual (BAU) Customer Success

### Handoff criteria checklist
**Handoff is complete when ALL of the following are true:**

| Criterion | Measurement | Owner | Status |
|---|---|---|---|
| **TTFV achieved** | Product event fired + champion confirmation + workflow output verified (real data, measurable result) | CS lead | ☐ |
| **Target user adoption reached** | ≥50% of licensed seats have logged in; ≥30% are DAU (daily active) | CS lead | ☐ |
| **Power user cohort identified** | 10–20 power users named and trained; can lead peer training | Champion | ☐ |
| **Executive sponsor confirmed and engaged** | Named sponsor; attended ≥2 meetings; approved handoff to BAU | CS lead | ☐ |
| **Department champion capable and willing** | Named primary + backup champion; both trained; both confirm readiness to own escalations | CS lead | ☐ |
| **Success criteria documented and met** | Kickoff success criteria document; all criteria met or on track; signed off by sponsor | CS lead | ☐ |
| **Health score ≥75/100** | Composite: TTFV achieved (30%), adoption ≥50% (30%), champion NPS ≥7 (20%), no critical issues (20%) | CS + BAU | ☐ |
| **Risks and opportunities logged** | Known risks (data quality, adoption in Dept B) and expansion opportunities documented in Salesforce | CS lead | ☐ |
| **QBR prepared** | Baseline metrics (TTFV date, adoption %, hours saved, top 3 use cases) drafted; QBR scheduled within 30 days | CS lead | ☐ |
| **BAU CS assigned and prepared** | Named BAU CS manager; read onboarding notes; reviewed health score and metrics | BAU CS Manager | ☐ |
| **Warm introduction scheduled** | Meeting invite sent (CS lead + BAU CS + executive sponsor + champion); all confirmed attending | CS lead | ☐ |

### Handoff process

**Day 40: Handoff planning begins**
1. CS lead meets BAU CS Manager. Review account: milestones, health score, champion, risk/opportunity log.
2. BAU CS reviews onboarding notes, customer setup, and usage patterns.
3. Identify any outstanding issues (blockers, escalations). Resolve or document as known issues for BAU.

**Day 42: Introduction meeting (45 min)**
- **Attendees:** Your CS lead, your BAU CS, customer executive sponsor, customer champion
- **Agenda:** (1) Your CS lead provides account snapshot (5 min): "Here's where we are, how we got here, what we learned"; (2) Your BAU CS introduces themselves and their role (5 min); (3) Focus shifts to customer: champion describes team workflow, sponsor confirms success criteria; (4) BAU CS talks about cadence going forward (QBR, check-ins, expansion opportunities); (5) Next steps: first QBR date, BAU CS office hours, escalation path.
- **Tone:** Warm handoff, not "we're leaving." Your CS lead is available for questions post-handoff, but BAU CS is now the owner.

**Day 45: Onboarding complete**
- Onboarding CS lead updates Salesforce: milestone complete, notes archived, account tagged "in BAU."
- BAU CS owns account going forward. First QBR scheduled for Day 60–75.

### What happens if handoff criteria are NOT met by Day 45?

- **Health score <75?** Extend onboarding 2 weeks (to Day 59). Root-cause the gap (adoption stalled? TTFV delayed?). Assign CS Manager to unblock. Do NOT force handoff to BAU if account is not healthy — it signals to customer that we're abandoning them.
- **Critical issue unresolved?** Issue must be triaged and in Engineering backlog with timeline. Document in Salesforce so BAU CS inherits the context and knows it's being worked.
- **Champion disengaged?** Sponsor must confirm replacement champion or commit to re-engaging original. Cannot hand off without a named champion.

### Anti-patterns in handoff
- ❌ Handing off a "red" account. BAU CS did not cause the problem; they should not inherit it without clear path to resolution.
- ❌ Repeating the kickoff. First QBR focuses on value delivered + expansion, not re-teaching the platform.
- ❌ Disappearing after handoff. Your CS lead should be available for 1–2 weeks of post-handoff questions. Not ownership, but availability.
- ❌ Losing the champion. If champion changes, BAU CS must meet the new champion before the first QBR. Relationship continuity matters.

---

## Sample execution: 21-day TTFV plan

To achieve 21-day TTFV, here's how time breaks down:

- **Days 1–3:** Kickoff + access provisioning. No product work yet — all setup.
- **Days 3–10:** Integration, SSO, data import. Platform is not yet "live" to users, but infrastructure is ready.
- **Days 10–14:** Power user training happens in parallel with final integrations. By Day 14, 10–20 power users can navigate the platform.
- **Days 14–21:** First team completes first workflow with live data. Power users help their colleagues. Champion documents the win (time saved, accuracy improved).
- **By Day 21:** Product event fires. Health score green. Milestone 4 complete. Momentum for rollout.

This is aggressive. It requires:
- Pre-positioned solutions engineer (not generic support).
- Fast IT turnaround (SSO in 5 days, not 20 days).
- Customer champion who is engaged and available.
- Clear, measurable definition of "first value" (not vague).

If any of these is missing, push TTFV target to 30 days.

---

## Success metrics dashboard (what to track)

Track these metrics weekly during onboarding:

| Metric | Milestone | Target | Current | Trend |
|---|---|---|---|---|
| Days to kickoff | M1 | ≤3 | — | — |
| SSO time-to-live | M2 | ≤8 | — | — |
| Data import error rate | M2 | <5% | — | — |
| Power user training completion % | M3 | ≥80% | — | — |
| Days to first workflow (TTFV) | M4 | ≤21 | — | — |
| Login % (seats) | M5 | ≥50% by Day 35 | — | — |
| DAU / MAU ratio | M5 | ≥30% by Day 35 | — | — |
| Health score | M6 | ≥75 by Day 45 | — | — |
| Champion NPS | M6 | ≥7 (0–10 scale) | — | — |
| Sponsor satisfaction | M6 | ≥7 (0–10 scale) | — | — |

---

## Frequently asked questions for onboarding

### "Can we skip kickoff and start integrations?"
No. Kickoff sets the foundation. If executive sponsor is not aligned on success criteria, onboarding will fail. Technical work without executive alignment = wrong priorities.

### "Can we extend the timeline to 60 days?"
Yes, if customer requests it. Default is 45 days. Extension should be documented with sponsor sign-off and new milestone dates assigned.

### "What if the champion leaves mid-onboarding?"
Escalate to executive sponsor immediately and ask for a replacement. Do not proceed without a named champion.

### "What if we discover the integration is more complex than expected?"
Escalate to Solutions Engineering by Day 7. Options: (1) Scope down initial integration (launch with API, not full sync); (2) Extend M2 timeline; (3) Provide customer resources to unblock IT.

### "Can we start training before integrations are ready?"
Yes, if needed. Teach platform navigation and workflows using sandbox data. But do not start Milestone 4 (first real workflow) until integrations are live.

### "What if adoption is low at Day 35?"
This is a blocker for handoff. Root-cause: Is training insufficient? Is there a missing feature? Is the problem not solved? Get champion + sponsor in a call. Options: (1) Extend Milestone 5 by 2 weeks; (2) Launch emergency training; (3) Escalate to Product if platform misalignment is discovered.

---

## Customisation for your product

**Before using this playbook, define or refine:**

1. **First value definition.** What does "success" look like for your customers? Not "completed setup" — a real outcome. Change the definition in Step 2.
2. **Integration priority.** Which 2–3 integrations are most critical? List them in M2 success criteria.
3. **Training approach.** Live instructor-led vs recorded videos? Synchronous vs asynchronous? Adjust M3 timing and format.
4. **Health score components.** The playbook assumes 30/30/20/20 (TTFV/adoption/NPS/no-issues). Adjust weights per your business.
5. **Escalation contacts.** Replace "CS Manager" and "Solutions Eng" with your actual roles/names.
6. **Tools & systems.** Replace Slack, Salesforce, etc. with your actual tools.

---

**Last updated:** 2026-05-04  
**Version:** 1.0  
**Segment:** Enterprise (200+ seats, $100k+ annual)  
**Target TTFV:** 21 days  
**Handoff criteria:** 6 items, all must be met

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/18.0 (81%) |
| Evaluated | 2026-05-04 |
| Target duration | 104656 ms |
| Target cost | $0.0972 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill defines time-to-first-value (TTFV) as a customer-perceived outcome — not 'completed onboarding call' but a specific product event or metric threshold | PASS | TTFV section explicitly defines first value as 'One team (minimum 20+ users) completes their primary workflow end-to-end using the platform with their own real data, achieving measurable improvement.' Measurement includes product event, metric threshold (20 concurrent users), and champion confirmation — none of which are activity-based like 'completed onboarding call.' |
| c2 | Skill requires TTFV to be measurable automatically — if it can't be measured, the skill requires building the instrumentation first | PARTIAL | The playbook names a specific product event (`first_real_workflow_completed`) and states 'Automated: Product event fired when user completes first workflow with non-demo data.' However, there is no explicit requirement to build the instrumentation if it doesn't already exist — the customisation section asks to 'define first value' but doesn't mention instrumentation gaps. The TTFV Current field says '[Unknown — establish baseline in first 3 enterprise onboardings]' rather than directing the team to instrument first. |
| c3 | Every milestone has an escalation trigger with a specific day threshold — not 'follow up if no response' | PASS | All six milestones in the table include a populated 'Escalation trigger' column with concrete day thresholds: M1 'No kickoff scheduled by Day 2'; M2 'SSO not tested by Day 8'; M3 '<80% training attendance by Day 13'; M4 'No users on platform by Day 17'; M5 '<30% login rate by Day 30'; M6 'Health score <75 by Day 40.' No open-ended 'follow up if needed' language. |
| c4 | Skill requires a segment definition before designing milestones — enterprise playbooks must be distinct from self-serve playbooks | PASS | The document opens with a full 'Segment Definition' table covering company size, technical sophistication, goals, stakeholders, integrations, and contract type — all before any milestone content. The 'Why this matters for onboarding' subsection lists four enterprise-specific onboarding implications (exec/user gap, security as blocker, change management complexity, multi-department priorities). |
| c5 | Skill includes a kickoff meeting agenda with timing, owners, and outputs per topic | PASS | The kickoff agenda table has five columns: Time (e.g., '0–10 min', '10–20 min'), Topic, Owner (e.g., 'CS lead', 'Solutions Engineer + IT lead'), Attendees, and Output (specific artefacts like 'Shared doc: Who does what', 'Technical scope doc', 'Signed timeline'). All required elements present for every row. |
| c6 | Skill defines handoff criteria as a checklist — onboarding is not complete until all criteria are met | PASS | The handoff section begins 'Handoff is complete when ALL of the following are true:' followed by an 11-row checklist with ☐ checkboxes per row. Criteria include TTFV achieved, adoption ≥50%, health score ≥75/100, named champion, QBR prepared, and BAU CS intro call completed. |
| c7 | Skill maps common blockers with early warning signs — partial credit if blockers are listed but early warning signs are not required per blocker | PARTIAL | Eight blockers are listed in a structured table. Every blocker has a populated 'Early warning sign' column (e.g., 'Sponsor doesn't attend kickoff; declines 2+ updates'; 'IT lead says we need InfoSec review before integration'). Early warning signs are present for each blocker, meeting the ceiling for this criterion. |
| c8 | Skill requires measurable success criteria for every milestone — 'complete onboarding call' is explicitly rejected | PASS | Each milestone has 5 numbered, measurable success criteria (e.g., M3: '≥80% attendance', '≥85% quiz score', 'trainer certification done'). The 'Milestone philosophy' section explicitly states: 'Every success criterion is measurable. Complete training is vague. 80% attendance + 85% quiz score + trainer certification is measurable.' |
| c9 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | No skill definition file is included in the captured output or artifacts. The only artifact written is 'work/onboarding-playbook-enterprise.md', which begins with '# Onboarding Playbook: Enterprise Segment (200+ seats)' — a markdown heading, not YAML frontmatter. There is no evidence of a skill file with name, description, or argument-hint fields. |
| c10 | Output's TTFV definition is a customer-perceived outcome and a specific product event or threshold — e.g. 'first integration completed end-to-end with live data flowing', 'first 10 users active in week 2', 'first business report generated by the customer's own user' — NOT 'kickoff call complete' | PASS | TTFV is defined as 'One team (minimum 20+ users) completes their primary workflow end-to-end using the platform with their own real data.' Measurement explicitly uses 'product event: first workflow completed with customer data (not demo/sandbox data)' and 'minimum 20 concurrent users on Day 21.' This is a customer-perceived outcome with a product event threshold, not an activity metric. |
| c11 | Output's TTFV is automatically measurable — names the specific product event, analytics tool, or instrumentation that captures it; if the instrumentation doesn't exist, the playbook requires building it before the playbook ships | PARTIAL | The playbook names the product event '`first_real_workflow_completed`' and states 'Automated: Product event fired when user completes first workflow with non-demo data.' However, the playbook does not require building the instrumentation if it doesn't exist — the customisation section says to 'define first value' but doesn't gate playbook use on instrumentation readiness. The 'Current TTFV: [Unknown — establish baseline]' comment doesn't direct the team to instrument first. |
| c12 | Output's segment definition explicitly addresses enterprise (200+ seats, dedicated IT teams, $100k+ annual contracts) — and notes how the playbook differs from a self-serve / SMB playbook | PARTIAL | The segment definition table covers '200+ seats', 'dedicated IT departments', and '$100k–$500k+ annual contract value'. The 'Why this matters for onboarding' section explains four enterprise-specific onboarding implications. However, the output never explicitly contrasts this playbook with a self-serve or SMB playbook — there is no statement like 'unlike a self-serve playbook where...' The enterprise-specific framing is implied but not explicitly differentiated. |
| c13 | Output's milestones each have a measurable success criterion — e.g. 'Day 14: 50% of seats invited and active, IT integration completed, first 3 admin reports generated' — not 'had a kickoff call' | PASS | Every milestone has 5 measurable success criteria with quantitative thresholds: M1 includes 'All access provisioned (test login successful)'; M2 includes 'Data import errors <5% of records'; M3 includes '≥80% attendance + ≥85% quiz score'; M4 includes 'Product event fires (first_real_workflow_completed) + 20+ unique users in workflow'; M5 includes '≥50% licensed seats logged in'; M6 includes 'Health score ≥75/100.' |
| c14 | Output's escalation triggers per milestone are concrete with day thresholds — e.g. 'if no admin login by day 7, escalate to AE; if integration incomplete by day 21, escalate to engineering for assistance' | PASS | All six milestones have escalation triggers with specific day thresholds in the table's 'Escalation trigger' column. Examples: 'No API/integration started by Day 6'; 'SSO not tested by Day 8'; 'No users on platform by Day 17'; 'Usage declining instead of growing by Day 32'; 'Health score <75 by Day 40.' No vague open-ended triggers. |
| c15 | Output's kickoff agenda has timing per topic, named owners (CSM / AE / SE / customer attendees), and outputs (signed RACI, agreed success metrics, integration list, security review status) — not bullet topics without owners | PASS | The kickoff agenda table has a Time column ('0–10 min', '10–20 min', '20–35 min', etc.), an Owner column ('CS lead', 'Solutions Engineer + IT lead', 'CS lead + Your executive'), an Attendees column, and an Output column with specific artefacts ('Shared doc: Who does what', 'Technical scope doc: Which systems integrate?', 'RACI matrix filled in', 'Day 1 actions assigned with owners and deadlines'). |
| c16 | Output's handoff criteria is a checklist that ALL items must satisfy before onboarding is 'complete' — e.g. TTFV achieved, all admin users trained, integration in production, executive sponsor confirmed quarterly cadence — with each as a checkbox | PASS | 'Handoff is complete when ALL of the following are true:' followed by 11 rows, each with a ☐ checkbox and a specific criterion: TTFV achieved (with measurement method), adoption ≥50%, power user cohort identified, executive sponsor confirmed, champion named + trained, success criteria met, health score ≥75/100, risks logged, QBR prepared, BAU CS assigned, warm intro scheduled. |
| c17 | Output addresses common enterprise blockers — IT security review timing, SSO/SAML setup, procurement / DPA, multi-region deployment — with early warning signs per blocker | PARTIAL | The blockers table includes 'IT blockers: SSO, data residency, security review' which covers IT security review timing and SSO/SAML setup with early warning signs. Data residency is mentioned but multi-region deployment is not addressed as a distinct blocker. Procurement / DPA (Data Processing Agreement) is completely absent as a named blocker — this is a significant gap for enterprise deals. All listed blockers do have early warning signs, but two of the four specifically named enterprise blocker types are missing. |
| c18 | Output's milestone success criteria explicitly REJECT activity-based metrics like 'completed kickoff call' or 'training session held' — every milestone is outcome-based | PASS | The 'Milestone philosophy' section explicitly states: 'Every success criterion is measurable. Complete training is vague. 80% attendance + 85% quiz score + trainer certification is measurable.' All milestone success criteria use outcome metrics (% logins, product events, quiz scores, data error rates) rather than activity completion markers. |
| c19 | Output addresses post-onboarding handoff to the AE / sustain CSM with the artefacts that travel forward — what the post-onboarding owner inherits | PARTIAL | The handoff process section states BAU CS reviews 'onboarding notes, customer setup, and usage patterns.' The handoff checklist includes 'Risks and opportunities logged' in Salesforce and 'QBR prepared' with baseline metrics. Day 40 handoff planning says 'CS lead meets BAU CS Manager. Review account: milestones, health score, champion, risk/opportunity log.' Artefacts mentioned include onboarding notes, health score, risk/opportunity log, and QBR baseline metrics. Covers the inheritance but doesn't enumerate a complete artefact list (e.g., integration map, champion contact sheet, contract context). |

### Notes

The output is a high-quality, detailed enterprise onboarding playbook that passes on most structural and content criteria. Strongest areas: every milestone has specific day-threshold escalation triggers, the kickoff agenda is fully structured with timing/owners/outputs, the handoff section uses an explicit all-must-satisfy checklist, and the milestone philosophy actively rejects activity-based metrics. Primary gaps: (1) No skill definition file is provided, so YAML frontmatter cannot be verified — this is a clean FAIL on c9. (2) TTFV measurement names a product event but never gates the playbook on instrumentation existing first — both the skill-level (c2) and output-level (c11) criteria take partial credit. (3) The segment definition explains enterprise-specific implications but never explicitly contrasts the playbook with a self-serve or SMB approach (c12). (4) The blockers table omits procurement/DPA entirely and doesn't name multi-region deployment as a distinct blocker (c17). The overall score sits just at the 80% PASS threshold.
