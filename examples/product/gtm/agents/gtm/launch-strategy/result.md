# Launch Strategy

Scenario: A GTM manager needs a go-to-market plan for a new analytics feature being added to a B2B project management tool.

## Prompt

> We're launching "Clearpath Analytics" next month — a new analytics module for our project management tool. Key capabilities:
> 
> - Real-time project health dashboard (RAG status across all projects)
> - Resource utilisation reports (who's overloaded, who's under-utilised)
> - On-time delivery rate trends by team and project type
> - Executive summary reports (PDF/email, weekly)
> 
> Target customers: Existing Clearpath customers with 50+ seats (we have 340 of them). New pricing: $15/seat/month add-on. We think mid-market operations directors and PMOs are the buyers.
> 
> Main competitors: Asana's reporting, Monday.com dashboards. We think we're better at the executive summary piece specifically.
> 
> Can you help me build the launch strategy?
> 
> A few specifics for the response:
> 
> - Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
> - Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
> - For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
> - When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
> - Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll build a comprehensive launch plan for Clearpath Analytics following the tier system. Let me work through each phase.

## Step 1 — Launch Tier Assessment

**Tier 1 — Major** ✓

**Rationale:** This is a new analytics product module with its own pricing model ($15/seat/month), targeting a specific buyer persona (operations directors/PMOs), competing directly against established players (Asana, Monday.com). The launch requires coordinated messaging, competitive positioning, and customer education. 4-week timeline is tight for Tier 1, but feasible with focused execution.

---

## Step 2 — Pre-Launch Checklist

I'll create the checklist with owners and dates. Assuming mid-June launch (June 15), working backward:

| # | Item | Owner | Due | Status |
|---|---|---|---|---|
| **POSITIONING & MESSAGING** |
| 1 | One-sentence description finalized | Product/Marketing | May 11 | Pending |
| 2 | Target audience persona doc (ops directors, PMOs, 50+ seat orgs) | Marketing | May 11 | Pending |
| 3 | Key benefit articulated (vs. "what it does") | Marketing/Product | May 11 | Pending |
| 4 | Positioning canvas completed using `gtm:positioning` | Marketing | May 15 | Pending |
| 5 | Competitive positioning finalized (Asana vs Monday.com analysis) | Marketing | May 15 | Pending |
| **LANDING PAGE & ANNOUNCEMENT** |
| 6 | Announcement page drafted (feature overview + pricing) | Marketing/Content | May 12 | Pending |
| 7 | Hero copy finalized (headline, subhead, CTA) | Marketing/Content | May 13 | Pending |
| 8 | Product screenshots & demo video (dashboard, reports, summaries) | Product/Design | May 14 | Pending |
| 9 | SEO metadata set (title, description, OG tags, schema) | Marketing | May 15 | Pending |
| 10 | Landing page URL decided + redirects configured | Ops/Marketing | May 15 | Pending |
| 11 | Landing page live on staging (preview URL shared with stakeholders) | Ops/Engineering | May 16 | Pending |
| **DOCUMENTATION** |
| 12 | User guide written (setup, dashboard walkthrough, reports setup) | Product/Docs | May 14 | Pending |
| 13 | Admin guide (pricing, seat management, billing) | Ops/Docs | May 14 | Pending |
| 14 | API documentation updated (if new endpoints exist) | Engineering/Docs | May 14 | Pending |
| 15 | Changelog entry drafted | Docs | May 15 | Pending |
| 16 | Known limitations documented (what doesn't it do yet?) | Product | May 14 | Pending |
| **SUPPORT READINESS** |
| 17 | FAQ document (top 10 ops director questions) | Support/Product | May 13 | Pending |
| 18 | Support team walkthrough (live training, not just docs) | Support Lead | May 16 | Pending |
| 19 | Escalation path defined (bug = X, feedback = Y) | Support Lead | May 13 | Pending |
| 20 | Known issues list shared with support team | Engineering | May 15 | Pending |
| 21 | KB articles drafted (common tasks: setup, interpreting RAG status, exporting reports) | Support/Docs | May 14 | Pending |
| 22 | Support staffing plan for launch week (extra coverage during launch) | Support Lead | May 10 | Pending |
| **EMAIL** |
| 23 | Announcement email drafted (clear subject, single CTA) | Marketing | May 13 | Pending |
| 24 | Email segments defined (all 340 customers vs. target segment first?) | Marketing | May 12 | Pending |
| 25 | Onboarding email sequence updated (3-4 emails over first week) | Marketing | May 14 | Pending |
| 26 | Email tested across clients (Outlook, Gmail, Apple Mail) | Marketing | May 15 | Pending |
| 27 | Send time scheduled (Tuesday-Thursday, 10am EST launch) | Marketing | May 15 | Pending |
| **SOCIAL MEDIA** |
| 28 | Social posts drafted (LinkedIn, Twitter/X) — not copy-paste versions | Marketing | May 13 | Pending |
| 29 | Visual assets created (dashboard screenshot, comparison chart, hero image) | Design | May 14 | Pending |
| 30 | Post-launch content planned (tips, use cases, customer stories for days 2-7) | Marketing | May 13 | Pending |
| **ANALYTICS & TRACKING** |
| 31 | Success metrics defined with targets (adoption %, activation rate, trial-to-paid) | Product/Analytics | May 11 | Pending |
| 32 | Tracking events implemented (feature view, report export, PDF sent, etc.) | Engineering | May 14 | Pending |
| 33 | Analytics dashboard created or updated (real-time launch metrics) | Analytics | May 15 | Pending |
| 34 | Baseline captured (current usage patterns for comparison) | Analytics | May 16 | Pending |
| **TECHNICAL READINESS** |
| 35 | Feature flags configured (can toggle off without deploy) | Engineering | May 12 | Pending |
| 36 | Gradual rollout plan defined (% schedule + advancement criteria) | Engineering/Product | May 12 | Pending |
| 37 | Rollback procedure documented and tested | Engineering | May 14 | Pending |
| 38 | Load testing completed (spike expected on launch day) | Engineering/Ops | May 15 | Pending |
| 39 | Monitoring and alerting configured (error rates, API latency, DB load) | Ops/Engineering | May 15 | Pending |
| 40 | Error budget assessed (acceptable error rate during launch) | Engineering | May 14 | Pending |

---

## Step 3 — Rollout Strategy

**Strategy: Percentage rollout with cohort-based preference**

Why this approach: Analytics adoption typically needs hands-on education; a phased rollout lets you calibrate support and fix issues before full release. Cohort-based phase-in (targeting high-value existing customers first) drives early wins and word-of-mouth.

```
Rollout plan for Clearpath Analytics:

Stage 1 (June 15-17): Internal team + 5 early-adopter customers
- Enable for Clearpath team (dogfood, catch obvious bugs)
- Enable for 5 handpicked customers (call them first, offer live onboarding)
- Monitor: error rate, support tickets, feature usage
- Kill switch: feature flag "analytics.rollout.enabled"
- Advancement criteria: zero critical bugs, support team confident, customers providing positive feedback

Stage 2 (June 18-21): 10% of user base (~34 accounts)
- Target: mix of high-seat-count orgs (50+ seats) and early adopters from beta
- Monitor: error rates < 0.5%, support volume < 5 tickets/day, adoption rate > 15%
- Advancement criteria: no rollback-worthy incidents, positive NPS feedback

Stage 3 (June 22-28): 50% of user base (~170 accounts)
- Full messaging push (email, social, in-app banner)
- Continued monitoring: adoption, conversion to paid plan
- Advancement criteria: ready for full release

Stage 4 (June 29): 100% rollout
- Public announcement
- All existing Clearpath customers see the module
- Evaluate: adoption rate, conversion rate, support load vs. forecast

Kill switch: Feature flag "analytics.rollout.enabled" — can be toggled off immediately if errors exceed 1% or support volume hits 20+ tickets/day.

Rollback trigger: Any of the following:
  - Error rate > 1% for 30 minutes
  - Support tickets related to analytics > 20 in a single day
  - Critical security issue discovered
  - Performance degradation > 20% on main dashboard
```

---

## Step 4 — Launch Day Run-of-Show (June 15)

| Time | Action | Owner | Notes |
|---|---|---|---|
| **08:00 EST** | War room opens — all hands on deck | Ops Lead | Slack: #clearpath-analytics-launch. Mute other commitments. |
| **08:15** | Final production deployment verified | Engineering | Smoke test: dashboard loads, reports generate, email export works. |
| **08:30** | Monitoring dashboards opened and baseline confirmed | Ops/Analytics | Links: [error rate], [adoption], [support tickets], [API latency]. Alert thresholds armed. |
| **08:45** | Feature flag set to Stage 1 (internal + 5 early adopters) | Engineering | Confirm via dashboard. Internal team should see module immediately. |
| **09:00** | Call 5 early-adopter customers (pre-scheduled) | Sales/CS | Introduce feature, offer live 30-min onboarding. Capture initial feedback. |
| **09:30** | Announcement email sent to all 340 existing customers | Marketing | Subject: "Introducing Clearpath Analytics: Real-time project health & team insights". Single CTA: "Explore Analytics". |
| **10:00** | Landing page published (goes live) | Ops | https://clearpath.io/analytics (or equivalent). All links live. |
| **10:05** | Social posts published (LinkedIn, Twitter/X) | Marketing | 3 separate, platform-appropriate posts (not duplicates). |
| **10:10** | In-app notification banner deployed (non-intrusive) | Product | "New: Clearpath Analytics is now available. Explore real-time dashboards." |
| **10:15** | Changelog entry published | Docs | Include: what's new, pricing, link to full docs. |
| **10:30–11:30** | Monitor + triage phase | All teams | Check: error rate (baseline), support tickets (expect some, <5 OK), feature usage (track logins to analytics module). |
| **11:30** | First status update posted | Ops Lead | Post to war room: "Launch status: [GREEN/YELLOW/RED]. Error rate: X%. Support: N tickets. Adoption so far: X%." |
| **13:00–17:00** | Ongoing monitoring + live customer support | Support + Product | Field questions, capture feedback, identify quick-win bugs vs. deferred items. |
| **17:00** | End-of-day standup | All hands | Lessons learned first 8 hours, any rollback decisions, plan for tomorrow. |

---

## Step 5 — Communication Plan

| Audience | Channel | Key Message | Owner | When |
|---|---|---|---|---|
| **Internal team** | Slack (#general) | "Launching Clearpath Analytics today, 10am EST. War room: #clearpath-analytics-launch. Rollback plan if needed: [link]." | Ops Lead | 8:30am launch day |
| **Support team** | Live briefing + email | FAQ, known issues, escalation paths, "Please be proactive: offer onboarding calls to any customer who asks." | Support Lead | May 16 (one day before) |
| **All 340 existing customers** | Email | Announcement: benefits (RAG status, utilization, trends), pricing ($15/seat/month, no charge for 14-day trial), CTA to explore. | Marketing | 9:30am launch day |
| **Operations directors / PMO segment** | Email (secondary wave) | Targeted message: "See team health in seconds. Identify resource conflicts before they happen." | Marketing | June 17 (2 days later, softer pitch) |
| **Social followers** | LinkedIn + Twitter/X | Post 1: Product teaser (dashboard screenshot). Post 2: Use case (e.g., "ops director's first morning with Clearpath Analytics"). Post 3: Pricing/trial CTA. | Marketing | 10:05am launch day |
| **Partner integrations** | Email (if applicable) | If other tools integrate with Clearpath: "New analytics data available via API." | Sales/Partnerships | May 30 (pre-launch) |
| **Existing premium customers (if any)** | Personal outreach | Calls from CSM: "We've built something specifically for operations teams like yours. I'd love to walk you through it." | Sales/CS | June 16-17 |

---

## Step 6 — Success Metrics

| Metric | Target | Measurement Method | Baseline | Review Date |
|---|---|---|---|---|
| **Feature adoption** (% of 340 customers who view analytics module at least once) | 30% by end of week 1 | Dashboard event tracking | 0% | June 22 |
| **Activation rate** (% who generate at least one report or view dashboard) | 15% by end of week 1 | Event: "report_generated" or "dashboard_viewed" | 0% | June 22 |
| **Trial-to-paid conversion** (% who add seats to analytics plan) | 8% within 30 days | Billing system conversion tracking | N/A | July 15 |
| **Error rate** (on feature) | < 0.5% during launch week | Error tracking / monitoring system | — | June 22 |
| **Support volume** (tickets related to analytics) | < 10/day during launch week | Support ticket tagging | 0 | June 22 |
| **Executive summary PDF generation** (most valuable feature) | 10+ PDFs sent by end of week 1 | Event: "pdf_generated" + "pdf_sent_via_email" | 0 | June 22 |
| **Time to first dashboard view** (speed of adoption friction) | Median < 5 minutes from module discovery | Session tracking | N/A | June 22 |
| **Customer satisfaction** (NPS on analytics feature) | ≥ 40 | In-app survey after first use | N/A | June 30 |

---

## Step 7 — Post-Launch Review (7-Day: June 22)

| Metric | Baseline | Target | Day 1 | Day 3 | Day 7 | Status |
|---|---|---|---|---|---|---|
| Feature adoption (% of 340) | 0% | 30% | 8% | 18% | ? | Track |
| Activation rate (% who generated report) | 0% | 15% | 3% | 10% | ? | Track |
| Error rate | — | <0.5% | ? | ? | ? | Track |
| Support tickets (analytics-related) | 0 | <10/day | ? | ? | ? | Track |
| Revenue impact (new analytics seats sold) | $0 | $1,500+ (100 seats × $15) | ? | ? | ? | Track |

**Review attendees:** Product Lead, Engineering Lead, Marketing Lead, Support Lead, Operations Director, Customer Success Manager

**Review template:**

- [ ] **Top 3 things that went well** — what should we repeat?
  - [ ] (Example: customer response to "executive summary" feature)
  - [ ] (Example: support team handled volume efficiently)
  - [ ] (Example: zero critical bugs during rollout)

- [ ] **Top 3 things that didn't go well** — what should we fix?
  - [ ] (Example: adoption rate below target, why?)
  - [ ] (Example: support tickets clustered around X issue)
  - [ ] (Example: specific feature not working as expected)

- [ ] **Unexpected outcomes** — what surprised us?
  - [ ] (Example: unexpected user segment adopted faster)
  - [ ] (Example: feature used differently than predicted)

- [ ] **User feedback themes** (use `gtm:feedback-synthesis` skill to analyze support tickets and NPS comments)
  - [ ] Most requested next feature?
  - [ ] Biggest pain point?
  - [ ] Most valued capability?

- [ ] **Follow-up items:**
  - [ ] Critical bugs to fix immediately?
  - [ ] Quick wins to ship in days 8-14?
  - [ ] Documentation to improve?
  - [ ] Next feature based on feedback?

- [ ] **Decisions:**
  - [ ] Continue to 100% rollout? Yes / No / Conditional?
  - [ ] What changes based on feedback?
  - [ ] Update roadmap based on learnings?

---

## Recommended Parallel Work Tracks

Since you're in 4-week sprint mode, run these in parallel:

1. **Run `gtm:positioning` skill** (May 11–15) → Creates positioning canvas, clarifies "why choose us over Asana/Monday?"
2. **Run `gtm:competitive-analysis` skill** (May 11–15) → Deep competitive assessment (Asana reporting gaps, Monday.com dashboards limitations)
3. **Create battle cards** (May 15–16) → One-pagers for sales on how to position vs. each competitor
4. **Run `gtm:feedback-synthesis` post-launch** (June 22) → Aggregate support tickets + NPS feedback for review

---

## Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Adoption slower than 30% target | Medium | Revenue impact | Offer free trial extension (14 → 30 days). Run targeted webinars for PMO segment during week 2. |
| Support volume spikes unexpectedly | Medium | Team burnout | Pre-plan overflow capacity. Identify simple FAQ-answerable tickets that support can deflect to docs. |
| Feature bugs discovered post-launch | Low | Credibility | Rollback plan ready. Commit to 24-hr bug fix SLA for critical issues. |
| Competitive response from Asana/Monday | Medium | Messaging pressure | Pre-prepared talking points on "why our executive summary is different" (battle cards). |
| Low engagement on social posts | Medium | Reach impact | Boost LinkedIn posts if needed. Leverage customer testimonials early (week 2) to drive social proof. |

---

## DRAFT — Requires Human Review

**Next steps for you:**
1. Review and adjust launch tier, dates, metrics, and team owners based on your actual capacity
2. Run `gtm:positioning` and `gtm:competitive-analysis` skills in parallel to refine messaging
3. Confirm Stage 1 early-adopter customer list (5 handpicked accounts)
4. Lock in team owners for each checklist item
5. Adjust rollout percentages if 340-customer universe doesn't match your segment breakdown

---

**DRAFT — Requires Human Review**

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 11.0/16.0 (69%) |
| Evaluated | 2026-05-04 |
| Target duration | 59402 ms |
| Target cost | $0.0728 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | All marketing copy, messaging, and campaign content is labelled DRAFT and flagged for human review before use | PASS | The output closes with '## DRAFT — Requires Human Review' and a second '**DRAFT — Requires Human Review**' footer, and the 'Next steps for you' section opens with 'Review and adjust launch tier, dates, metrics, and team owners.' Document-level DRAFT labelling covers the entire artifact including all embedded marketing copy. |
| c2 | Applies positioning work before tactics — identifies the competitive alternative (Asana/Monday reporting), differentiator (executive summaries), and target segment (operations directors/PMOs at 50+ seat accounts) before writing messages | PASS | Step 1 rationale names 'competing directly against established players (Asana, Monday.com)' and notes the executive summary differentiator. Step 2 items 2, 4, and 5 name the persona ('ops directors, PMOs, 50+ seat orgs'), positioning canvas, and competitive positioning — all listed before the Step 5 messaging content. All three positioning elements are established structurally before the messages section. |
| c3 | Leads messaging with the customer problem (e.g. blind spots in project health, lack of exec visibility) rather than feature descriptions | PARTIAL | The ops director segment message reads 'See team health in seconds. Identify resource conflicts before they happen.' — outcome-oriented but not a vivid pain articulation. The main announcement email is described as leading with 'benefits (RAG status, utilization, trends)' which is feature-adjacent. No 'execs keep asking you for status and you spend half a day pulling a report' type framing appears anywhere in the output. |
| c4 | Recommends a launch tier (given 340 existing customers and $15/seat add-on, this is likely a Tier 2 or Tier 1 launch — not a silent rollout) | PASS | Step 1 opens with 'Tier 1 — Major ✓' and provides explicit rationale: 'new analytics product module with its own pricing model ($15/seat/month), targeting a specific buyer persona... competing directly against established players.' |
| c5 | Distinguishes between the existing customer expansion play (340 accounts) and any net-new motion — these require different approaches | FAIL | The output is entirely focused on the 340 existing customers. Net-new acquisition is never mentioned, referenced, or distinguished from the expansion play. No acknowledgement that these require different channels, messaging, or sales motions appears anywhere in the output. |
| c6 | Includes a post-launch review plan with success metrics — partial credit if metrics are named but no review timeline or owner is specified | PARTIAL | Step 6 names eight metrics with targets and a June 22 review date. Step 7 includes a full review template with named attendees ('Product Lead, Engineering Lead, Marketing Lead, Support Lead, Operations Director, Customer Success Manager'). All three elements are present; ceiling caps score at PARTIAL. |
| c7 | Produces a structured launch plan with phases and owners, not a list of marketing ideas | PASS | Seven numbered steps with structured tables, named owners, and dates throughout: pre-launch checklist (40-item table with Owner/Due columns), rollout stages with named kill-switch conditions, launch day run-of-show (time/action/owner/notes table), communication plan (audience/channel/owner/when table), metrics table, post-launch review with attendees. |
| c8 | Output sizes the existing-customer revenue opportunity — 340 accounts × 50+ seats × $15/seat/month — yielding the upper-bound ARR (~$3M+) and a realistic conversion target (e.g. '30% adoption in year 1 → ~$900K ARR uplift') | FAIL | No ARR calculation appears. The only revenue figure is '$1,500+ (100 seats × $15)' in Step 7's review table, which is a narrow day-one tracking placeholder, not an opportunity sizing. The 340 × 50+ × $15 × 12 = ~$3M upper-bound ARR and any conversion-to-ARR scenario (e.g. 30% → $900K) are absent. |
| c9 | Output's positioning anchors against Asana / Monday native reporting as the competitive alternatives, with the executive summary as the named differentiator — not a generic feature list | PASS | Step 1 rationale: 'competing directly against established players (Asana, Monday.com).' Step 2 item 5: 'Competitive positioning finalized (Asana vs Monday.com analysis).' Risk Mitigation: 'Pre-prepared talking points on "why our executive summary is different" (battle cards).' Executive summary named specifically as the differentiator, not a generic capability list. |
| c10 | Output's customer-problem framing leads with the operations director / PMO pain — e.g. 'execs ask "how are projects tracking?" and you spend half a day pulling a manual report' — not 'we have a new analytics module' | PARTIAL | The ops director segment message — 'See team health in seconds. Identify resource conflicts before they happen.' — gestures at outcomes rather than features, but there is no vivid pain articulation (no 'half a day pulling reports' equivalent). The announcement email is described as leading with 'benefits (RAG status, utilization, trends)' which is feature-adjacent. Problem framing is surface-level rather than deeply customer-pain-led. |
| c11 | Output classifies this as Tier 1 or Tier 2 launch given 340 existing customers, $15/seat ARR uplift, and a 3-year-customer-base activation event — explicitly NOT a silent rollout | PASS | Step 1: 'Tier 1 — Major ✓' with explicit rationale including the new pricing model, specific buyer persona, and direct competition with Asana and Monday.com. Silent rollout is never suggested. |
| c12 | Output separates the existing-customer expansion motion (CSM-led, in-product upsell, QBR conversations) from any net-new acquisition motion — different channels, different messaging, different sales process | FAIL | Net-new acquisition is never mentioned in the output. While CSM-led outreach appears in the Communication Plan ('Calls from CSM: "We've built something specifically for operations teams like yours"'), no distinction is drawn between the expansion motion and a net-new motion. The two plays are not separated, compared, or even contrasted. |
| c13 | Output's launch plan has phases with owners and dates — Pre-launch (weeks -4 to 0): readiness checklist, sales enablement, beta close-out; Launch week: announcements, in-product, customer comms; Post-launch (weeks 1-12): adoption tracking, expansion plays, feedback loops | PARTIAL | Pre-launch (May 10–16, Step 2) and launch week (June 15, Step 4) are detailed with owners and dates. However, the post-launch period covers only Day 7 (June 22 review in Step 7) — no weeks 1–12 (30/60/90-day) expansion playbook, no multi-month adoption tracking cadence, no feedback loop structure beyond the 7-day window. |
| c14 | Output's marketing copy and messaging examples are labelled DRAFT — explicitly flagged for human review before publication | PASS | '## DRAFT — Requires Human Review' section header and '**DRAFT — Requires Human Review**' at document close. 'Next steps for you: 1. Review and adjust...' explicitly flags human review before use. Document-level labelling applies to all embedded copy. |
| c15 | Output's post-launch review plan names success metrics (e.g. trial signups, paid conversions, % of 340-base activated, $ ARR uplift), a review date (e.g. 'Day 30, Day 60, Day 90 reviews'), and a review owner | PASS | Step 6 names eight success metrics including 'Feature adoption (% of 340 customers)', 'Trial-to-paid conversion', 'Error rate', 'NPS' — each with a target, measurement method, and review date of June 22. Step 7 names review attendees: 'Product Lead, Engineering Lead, Marketing Lead, Support Lead, Operations Director, Customer Success Manager.' All three required elements present. |
| c16 | Output addresses internal readiness alongside external launch — sales enablement (battle cards, demo scripts), CSM enablement (expansion playbooks), support training, docs ready before announce | PASS | Step 2 includes: support FAQ (item 17), support team walkthrough/training (item 18), escalation path (item 19), KB articles (item 21), support staffing plan (item 22), user guide (item 12), admin guide (item 13), API docs (item 14). Risk Mitigation and Recommended Work Tracks include battle cards. CSM personal outreach appears in Step 5. Demo scripts are not mentioned, but core internal readiness pillars are covered. |
| c17 | Output addresses pricing communication carefully — $15/seat add-on for existing customers may need grandfathering for early adopters or volume discounting at the 340 mid-market scale | FAIL | The output mentions '$15/seat/month, no charge for 14-day trial' in the announcement email description (Step 5) and 'Trial-to-paid conversion: 8% within 30 days' in Step 6. No mention of grandfathering for early adopters, volume discounting for large seat counts, or any pricing strategy nuance for the 340-account mid-market base. Pricing communication is surface-level. |

### Notes

The output is a well-structured, operationally detailed launch plan that scores strongly on format (Tier 1 classification, phased rollout, run-of-show, communication plan, internal readiness checklist). Its main gaps are: (1) it never sizes the revenue opportunity with explicit ARR math (340 × 50+ × $15 × 12 = ~$3M upper bound), missing c8 entirely; (2) it never distinguishes the existing-customer expansion play from a net-new acquisition motion, failing both c5 and c12; (3) customer-problem framing remains outcome-adjacent rather than pain-led, earning only partial credit on c3 and c10; (4) the post-launch horizon covers only seven days, leaving the weeks 1–12 adoption/expansion tracking cadence absent (c13 partial); and (5) pricing nuance (grandfathering, volume discounts) is untouched (c17 fail). These four gaps collectively pull the score below the 80% threshold needed for a PASS verdict.
