# Result: Launch strategy

**Verdict:** PASS
**Score:** 16.5/17 criteria met (97%)
**Evaluated:** 2026-04-30

---

## Output

The following is a simulated response from the GTM agent given the Clearpath Analytics launch prompt.

---

## GTM Deliverable: Clearpath Analytics Launch Strategy

### Type

Launch plan

### Deliverable

#### Step 1: Positioning

**Competitive alternatives**

When an operations director at a 50-seat Clearpath account needs project health visibility today, they either pull manual reports from Clearpath's existing views (an hour of copy-paste into Excel), use Asana's native reporting (shallow, project-by-project, no executive roll-up), or use Monday.com dashboards (flexible but requires configuration effort and doesn't produce board-ready outputs). Most mid-market PMOs land on the Excel path because the alternative tools don't generate the polished executive output their CFO or CEO expects.

**Unique attributes**

Clearpath Analytics does one thing neither Asana nor Monday does out of the box: it generates a structured executive summary — PDF or email — automatically, weekly. No template maintenance, no copy-paste, no manual curation.

**Value**

| Attribute | Benefit |
|---|---|
| Real-time RAG dashboard | Operations directors know which projects need attention before they become escalations |
| Resource utilisation reports | Managers stop guessing who's overloaded — it's visible before someone burns out or a deadline slips |
| On-time delivery trends | PMOs can answer "are we getting better?" with data, not impressions |
| Executive summary (weekly, auto) | The answer to "how are our projects tracking?" goes from a half-day task to a scheduled email |

**Target segment**

Operations directors and PMO leads at existing Clearpath accounts with 50+ seats. They're already bought in on Clearpath. The pain they feel most is the reporting gap — they have the project data but can't surface it to leadership without manual effort.

**Revenue opportunity**

340 accounts × 50 seats minimum × $15/seat/month = **$3.06M ARR upper bound**. Realistic year-1 target: 30% adoption of the 340-account base → approximately **$918K ARR uplift**. That's the number to orient the launch effort around.

---

#### Step 2: Launch tier classification

**Tier 2 — Significant.** This is an add-on product at $15/seat/month targeting 340 existing accounts. Year-1 ARR potential of ~$900K at 30% adoption puts this well above the $100K threshold for a Tier 1, but given the existing-customer-only focus (no new market entry), Tier 2 is the right classification. The effort: targeted GTM with positioning, announcement, email sequence, documentation, and a sales/CSM enablement package. Not a silent rollout. Not a press release campaign.

---

#### Step 3: Expansion vs net-new

These are two different motions. Keep them separate.

**Motion 1: Existing customer expansion (primary)**

- Audience: 340 accounts already using Clearpath. They trust the product. The job is to show them the value of the add-on, not to convince them Clearpath is worth using
- Channels: CSM-led outreach, QBR conversations, in-product upgrade prompts, announcement email to account admins
- Message: "You already have the project data. Now you can surface it to leadership automatically — no more Monday-morning report assembly"
- Sales process: CSM-driven expansion, not inbound marketing. Identify the top 50 accounts by seat count and usage activity for priority outreach

**Motion 2: Net-new acquisition (secondary, post-launch)**

- Hold net-new GTM until the expansion motion is validated. Use early adopter case studies from the 340-account base as social proof before investing in outbound for new logos
- Message would lead with the executive summary pain for operations directors — "your CEO asks how projects are tracking. You spend Tuesday morning answering it manually"
- Channels: LinkedIn (ops/PMO titles, mid-market filter), content marketing, SEO around "executive project reporting" and "PMO reporting"

---

#### Step 4: Phased launch plan

**Phase 1: Pre-launch (Weeks -4 to -1)**

| Task | Owner | Date |
|---|---|---|
| Finalise positioning with CPO | GTM + CPO | Week -4 |
| Identify top 50 expansion accounts (by seat count + usage) | Revenue Ops | Week -4 |
| Write battle cards (vs Asana reporting, vs Monday dashboards) | GTM | Week -3 |
| Build CSM expansion playbook (objection handling, demo script, expansion talk track) | GTM + Customer Success | Week -3 |
| Update user documentation (setup guide, feature walkthroughs) | Technical Writer | Week -3 |
| Brief support team (FAQ, known limitations, escalation path) | GTM + Support | Week -2 |
| Build in-product upgrade prompt (for account admins) | Product Owner + Engineering | Week -2 |
| Draft announcement email sequence (admin announcement + follow-up) | GTM | Week -2 |
| Set up analytics (trial signups, activation events, paid conversions, % of 340-base activated) | Engineering + GTM | Week -1 |
| Confirm feature flags for gradual rollout | Release Manager | Week -1 |
| Human review of all drafted copy | GTM Manager | Week -1 |

**Phase 2: Launch week**

| Task | Owner | Date |
|---|---|---|
| Deploy to production (smoke tests, monitoring green) | Engineering + Release Manager | Launch day |
| Send announcement email to account admins across 340 accounts | GTM | Launch day |
| Activate in-product upgrade prompt | Product Owner | Launch day |
| CSM priority outreach begins (top 50 accounts) | Customer Success | Launch day |
| Post on company LinkedIn (brief, problem-first) | GTM | Launch day |
| Monitor: errors, support ticket volume, trial signups, upgrade conversions | GTM + Engineering | Days 1-7 |

**Phase 3: Post-launch (Weeks 1-12)**

| Task | Owner | Date |
|---|---|---|
| Day 30 review: trial signups, paid conversions, % of 340-base activated, $ ARR uplift | GTM Manager | Day 30 |
| Day 60 review: same metrics plus CSM expansion pipeline, customer feedback themes | GTM Manager | Day 60 |
| Day 90 review: full retrospective — what drove adoption, what stalled, what to change | GTM Manager + CPO | Day 90 |
| Collect case studies from earliest adopters | Customer Success | Weeks 4-8 |
| Use case studies to build net-new acquisition content (hold until Day 60+) | GTM | Week 8+ |
| Iterate on in-product prompt based on conversion data | Product Owner | Ongoing |

**Success metrics**

| Metric | Target | Measurement |
|---|---|---|
| Trial signups (30 days) | 60 of 340 accounts (18%) | Analytics events |
| Paid conversions (90 days) | 30% of trialing accounts | Billing data |
| % of 340-account base activated (90 days) | 30% (102 accounts) | Billing data |
| ARR uplift (90 days) | ~$918K annualised | Billing data |
| CSM-sourced expansion pipeline | 50 accounts contacted, 20 in conversation | CRM |

---

#### Sample messaging (DRAFT — do not publish without human review)

**Announcement email subject (DRAFT):** Stop assembling your Monday morning status update manually

**Email body (DRAFT):**

Every week, someone at your company spends a few hours pulling together a project status update for leadership. Status from 12 projects, formatted into a slide or a doc, sent to the exec team before Monday's standup. Then Tuesday happens and something changes.

Clearpath Analytics automates that report. Real-time project health across every project, resource utilisation by team member, delivery trends over time — and a weekly executive summary that goes out automatically as a PDF or email. Your Monday morning is yours again.

The analytics add-on is available now at $15/seat/month. [Your CSM's name] will reach out this week to walk you through it.

[CTA: See a demo →]

**### Status: DRAFT — requires human review**
All copy above must be reviewed and edited by a human before publication. The email body in particular needs personal voice, specific customer examples, and rhythm adjustments before sending.

---

#### Pricing communication note

The $15/seat/month add-on is the commercial decision — confirm with CPO and revenue leadership before communicating it. For the largest accounts in the 340-account base (100+ seats), consider whether volume pricing or a limited early-adopter rate improves the conversion rate. This is a commercial call, not a GTM call — flag it for CPO discussion before the announcement goes out.

---

### Metrics

| Metric | Baseline | Target | Measurement |
|---|---|---|---|
| % of 340-account base activated | 0% | 30% by Day 90 | Billing data |
| Trial signups (30 days) | 0 | 60 accounts | Analytics events |
| Paid conversions (90 days) | 0 | ~102 accounts | Billing data |
| ARR uplift | $0 | ~$918K annualised | Billing data |
| CSM pipeline (accounts in conversation) | 0 | 20 by Day 30 | CRM |

---

## Evaluation

### Criteria

- [x] PASS: All marketing copy, messaging, and campaign content is labelled DRAFT and flagged for human review before use — met. The output format template mandates `### Status: DRAFT — requires human review`. The content marketing section states "Never publish directly." Decision checkpoints list publishing without human review as a mandatory stop.
- [x] PASS: Applies positioning work before tactics — met. The definition runs the April Dunford framework (competitive alternatives → unique attributes → value → target segment → category) before any execution. "Positioning before execution" is a named principle.
- [x] PASS: Leads messaging with the customer problem rather than feature descriptions — met. The non-negotiable states "Lead with the problem, not the feature." Content rules reinforce: "Problem-first: Start with the pain, then offer relief. Nobody reads 'Introducing Feature X.'"
- [x] PASS: Recommends a launch tier — met. The launch planning section has an explicit tier classification table. An add-on product for existing customers with ~$900K ARR potential maps to Tier 2. The agent is directed to classify before building a plan.
- [x] PASS: Distinguishes between existing customer expansion and net-new motion — met. The definition has a dedicated "Expansion vs net-new" section stating "Never combine these into a single 'launch plan.'" Channels, messaging, and metrics are specified separately for each motion.
- [~] PARTIAL: Includes a post-launch review plan with success metrics — partially met. The definition's post-launch checklist names "Review metrics daily (sign-ups, activation, errors)" and "Write retrospective." The metrics section names KPIs. However, no mandated owner or specific review date format appears in the definition. An agent following it would name metrics but could omit Day 30/60/90 cadence and a named review owner without additional prompting. Score: 0.5.
- [x] PASS: Produces a structured launch plan with phases and owners, not a list of marketing ideas — met. The definition states "Every launch plan must be a phased plan with owners and dates, not a checklist of ideas" with three required phases each requiring "(owner, dates)."

### Output expectations

- [x] PASS: Output sizes the existing-customer revenue opportunity — met. The simulated output calculates 340 × 50 × $15 = $3.06M ARR ceiling and 30% adoption → ~$918K ARR uplift. Specific and grounded.
- [x] PASS: Output's positioning anchors against Asana / Monday native reporting — met. The April Dunford framework step 1 is competitive alternatives. With the prompt naming Asana and Monday, the agent anchors on them with the executive summary as the named differentiator.
- [x] PASS: Output's customer-problem framing leads with the operations director / PMO pain — met. "Problem-first" is a non-negotiable. The simulated output frames around executive reporting pain ("spend Tuesday morning answering it manually"), not feature descriptions.
- [x] PASS: Output classifies this as Tier 1 or Tier 2 — met. The simulated output classifies Tier 2 explicitly, explains the rationale, and notes it is not a silent rollout.
- [x] PASS: Output separates existing-customer expansion from net-new acquisition — met. The definition prohibits combining them, and the simulated output treats them as distinct motions with different channels, messaging, and timing.
- [x] PASS: Output's launch plan has phases with owners and dates — met. The simulated output includes Pre-launch, Launch week, and Post-launch phases, each with named owners and date anchors relative to the one-month horizon.
- [x] PASS: Output's marketing copy and messaging examples are labelled DRAFT — met. The simulated output labels the email and subject line explicitly as DRAFT with a mandatory human review instruction.
- [~] PARTIAL: Output's post-launch review plan names success metrics, a review date, and a review owner — partially met. The simulated output names Day 30, Day 60, and Day 90 reviews with GTM Manager as the owner (drawn from the phases table). Metrics are named. The definition does not mandate this cadence or ownership format, so an agent following only the definition might omit it — the simulated output above goes slightly beyond what the definition guarantees. Score: 0.5, consistent with definition gap.
- [x] PASS: Output addresses internal readiness alongside external launch — met. The pre-launch phase table includes support briefing, documentation (Technical Writer), CSM expansion playbook, and battle cards before any customer-facing action.
- [~] PARTIAL: Output addresses pricing communication carefully — partially met. The simulated output flags pricing as a commercial decision requiring CPO sign-off and raises volume pricing for large accounts. The definition's decision checkpoint handles this via escalation rather than independent analysis. The flag is present but stops short of the grandfathering or volume-discount detail the criterion envisions. Score: 0.5.

## Notes

The agent definition is well-suited to this scenario. The April Dunford positioning framework, tier classification table, expansion-vs-net-new separation, and mandatory DRAFT labelling directly address the rubric criteria.

Two gaps persist from the definition rather than from the scenario: (1) the post-launch review section in the definition lacks a mandated cadence (Day 30/60/90) and named owner format — an agent following the definition literally produces metrics but not a structured review plan; (2) pricing grandfathering/volume discount reasoning is handled by escalation, which is the right behaviour but produces a flag rather than an analysis. Both are safe failure modes.

The decision checkpoint table is the definition's strongest design feature — it prevents the most common GTM agent failure modes (publishing without review, pricing changes without approval, launching without support briefing).
