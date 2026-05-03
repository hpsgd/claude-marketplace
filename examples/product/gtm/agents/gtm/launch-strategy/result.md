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

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Here's the launch plan. Key decisions I made — flag any you want to revisit:

**Tier 1 — Major.** New priced add-on with billing, new positioning, and 340-account communication effort. That's not a standard feature launch.

**Beta → GA rollout.** Because this involves a purchase flow and billing, I'd rather validate that with 20 hand-picked accounts (May 26) before blasting the full announcement on June 1. Gives you a week to fix anything broken in the buy flow.

**42 pre-launch items, all owner-tagged by role.** You'll need to assign real names — every unowned item will slip.

**Conservative revenue targets:** 10% conversion (34 accounts) in 30 days, 20% (68 accounts) at 90 days. Adjust if you have seat-count data — I assumed ~85 seats avg.

**Three things I'd prioritise this week (May 1–7):**
1. Baseline your current upsell metrics (item 35) — you need this before you can measure impact
2. Pick the 20 beta accounts now — selection criteria are in the rollout section
3. Run the positioning canvas before writing any copy — the exec summary differentiator vs Asana/Monday needs to be sharp

The plan is saved to `clearpath-analytics-launch-plan.md`. Want me to run the positioning canvas next, or draft the announcement email?

### Artifacts written

#### `work/clearpath-analytics-launch-plan.md`

```
> **DRAFT — requires human review before execution begins**

---

# Launch Plan: Clearpath Analytics

**Launch date:** 2026-06-01
**Plan owner:** [Launch Owner]
**Last updated:** 2026-05-01

---

## Launch Tier: 1 — Major

**Rationale:** New priced add-on module ($15/seat/month) targeting 340 existing accounts. This is a revenue-generating product launch with new billing, new positioning, dedicated documentation, and a significant customer communication effort. It involves new pricing, multiple net-new capabilities, and has material impact on customer contracts. Tier 1 checklist applies in full.

---

## Pre-Launch Checklist

| # | Item | Owner | Due | Status |
|---|---|---|---|---|
| **Positioning and messaging** | | | | |
| 1 | Positioning canvas completed (`gtm:positioning` skill) — competitive alternatives, unique attributes, value frame vs Asana and Monday.com | Marketing | 2026-05-08 | Pending |
| 2 | One-sentence description approved — e.g. "Clearpath Analytics gives operations directors a real-time view of project health and a ready-to-send executive summary every week, without exporting to spreadsheets" | Launch Owner | 2026-05-08 | Pending |
| 3 | Primary buyer persona confirmed — mid-market Operations Director / PMO lead at 50+ seat account | Marketing | 2026-05-08 | Pending |
| 4 | Key benefit articulated in buyer terms: not "RAG dashboard" but "know which projects are at risk before your Monday standup" | Marketing | 2026-05-09 | Pending |
| 5 | Messaging approved by stakeholders (Product + Exec sign-off) | Launch Owner | 2026-05-12 | Pending |
| 6 | Battle card written vs Asana reporting and Monday.com dashboards (`gtm:write-battle-card` skill) — for sales and support use | Marketing | 2026-05-14 | Pending |
| **Landing page / in-app announcement** | | | | |
| 7 | Announcement page drafted — hero headline, three benefit bullets, pricing ($15/seat/month), CTA ("Start free trial" or "Add to your plan") | Marketing | 2026-05-14 | Pending |
| 8 | Screenshots / demo GIF created — show the executive summary email, the RAG dashboard, and a resource utilisation view | Product | 2026-05-16 | Pending |
| 9 | In-app upgrade prompt designed and implemented — shown to admin users on the main nav or dashboard | Engineering | 2026-05-21 | Pending |
| 10 | SEO metadata set (title, description, OG tags) on the announcement page | Marketing | 2026-05-21 | Pending |
| 11 | Pricing page updated to include Analytics add-on | Marketing | 2026-05-28 | Pending |
| 12 | Landing page live at preview URL for internal review | Engineering | 2026-05-23 | Pending |
| **Documentation** | | | | |
| 13 | Help center articles written: (a) getting started with Analytics, (b) configuring RAG thresholds, (c) scheduling executive summary emails, (d) reading the resource utilisation report | Product | 2026-05-16 | Pending |
| 14 | Known limitations documented — e.g., historical data depth, PDF export limits, seat count calculation method | Product | 2026-05-16 | Pending |
| 15 | Changelog entry drafted | Marketing | 2026-05-28 | Pending |
| 16 | Admin guide: how to enable Analytics for your organisation, manage user access, configure billing | Product | 2026-05-19 | Pending |
| **Support readiness** | | | | |
| 17 | FAQ document created — top 10 anticipated questions (billing, data freshness, PDF format, SSO access, cancellation) | Support | 2026-05-15 | Pending |
| 18 | Support team walkthrough completed — live demo, not just a doc | Product | 2026-05-21 | Pending |
| 19 | Escalation path defined: bug → Engineering on-call; billing question → [owner]; feature feedback → Product | Launch Owner | 2026-05-14 | Pending |
| 20 | Known issues shared with support team — any gaps, workarounds documented | Engineering | 2026-05-28 | Pending |
| 21 | Support staffing plan for launch week — extra coverage Mon 1 June through Fri 5 June | Support Lead | 2026-05-22 | Pending |
| **Email** | | | | |
| 22 | Announcement email drafted — subject line variants (A/B), clear single CTA, personalised to admin/billing contact | Marketing | 2026-05-19 | Pending |
| 23 | Email segment defined: all admin/billing contacts at accounts with 50+ seats (340 accounts) — confirm list with CRM | Marketing | 2026-05-14 | Pending |
| 24 | Beta invite email drafted (separate, more personal, for 20 beta accounts) | Marketing | 2026-05-14 | Pending |
| 25 | 7-day and 14-day follow-up emails drafted for non-openers and non-converters | Marketing | 2026-05-22 | Pending |
| 26 | All emails tested — rendered in Outlook, Gmail, Apple Mail; links verified | Marketing | 2026-05-29 | Pending |
| 27 | Launch email scheduled for 2026-06-01 at 09:00 in recipient's timezone (or 09:00 GMT as fallback) | Marketing | 2026-05-29 | Pending |
| **Social media** | | | | |
| 28 | LinkedIn post drafted — first-person voice, specific capability, targeted at operations/PMO audience | Marketing | 2026-05-26 | Pending |
| 29 | Twitter/X post drafted — short, punchy, link to announcement page | Marketing | 2026-05-26 | Pending |
| 30 | Visual assets created — dashboard screenshot, executive summary preview, one short screen-recording | Design | 2026-05-22 | Pending |
| 31 | Post-launch social content planned (days 3, 7): use case highlight, customer quote if available from beta | Marketing | 2026-05-28 | Pending |
| **Analytics and tracking** | | | | |
| 32 | Success metrics finalised and baselined (see Success Metrics section) | Product | 2026-05-09 | Pending |
| 33 | Tracking events implemented: module activated, dashboard viewed, exec summary sent, PDF downloaded, resource report viewed | Engineering | 2026-05-19 | Pending |
| 34 | Analytics dashboard created — real-time view of activations, trial starts, feature usage | Engineering | 2026-05-23 | Pending |
| 35 | Baseline captured: current upsell rate, support ticket volume, relevant engagement metrics | Product | 2026-05-07 | Pending |
| **Technical readiness** | | | | |
| 36 | Feature flag configured — Analytics module can be enabled/disabled per account without deploy | Engineering | 2026-05-16 | Pending |
| 37 | Billing integration tested end-to-end — add-on purchase flow, seat count calculation, invoice line item | Engineering | 2026-05-21 | Pending |
| 38 | PDF export tested across browsers and email clients | Engineering | 2026-05-21 | Pending |
| 39 | Rollback procedure documented — steps to disable module for specific accounts or globally | Engineering | 2026-05-22 | Pending |
| 40 | Load testing completed — exec summary email job at scale (340 accounts, weekly send) | Engineering | 2026-05-23 | Pending |
| 41 | Monitoring and alerting configured — email delivery failures, dashboard load times, PDF generation errors | Engineering | 2026-05-26 | Pending |
| 42 | Error budget defined: acceptable error rate <0.5% during first week | Engineering | 2026-05-22 | Pending |

---

## Rollout Strategy

**Approach: Beta → GA**

Rationale: Analytics is a priced add-on with billing implications. A beta cohort lets us validate the purchase flow, onboarding experience, and executive summary quality with real customers before the full announcement. Risk is low if the beta is small and hand-picked.

| Stage | Who | Date | Criteria to advance |
|---|---|---|---|
| **Internal dogfood** | Internal team only | 2026-05-19 | No critical bugs; billing flow works end-to-end |
| **Beta cohort** | 20 existing accounts (hand-picked: high-engagement, mix of company sizes) | 2026-05-26 | <3 critical bugs; support ticket volume <5; at least 15/20 send their first exec summary |
| **GA — full announcement** | All 340 qualifying accounts | 2026-06-01 | Beta criteria met; rollback plan tested; support staffed |

**Kill switch:** Feature flag `analytics_module_enabled` — can be set per account or globally.

**Rollback trigger:** Error rate exceeds 1% sustained for 30 minutes; or support tickets exceed 25 in the first 24 hours; or billing errors reported by >3 accounts.

**Beta selection criteria:** Pick 20 accounts from the 340 that are: (a) high product engagement scores, (b) have an identified champion who will give honest feedback, (c) span 2-3 different industries, (d) include at least 5 accounts with 100+ seats.

---

## Launch Day Run-of-Show — 2026-06-01

| Time (local) | Action | Owner | Notes |
|---|---|---|---|
| 07:00 | Final deployment to production verified | Engineering | Confirm feature flag is GA-ready |
| 07:15 | Smoke test core flows: purchase add-on, view RAG dashboard, schedule exec summary, download PDF | Product | Run against 2 internal test accounts |
| 07:30 | Monitoring dashboards open and being watched | Engineering | Share dashboard link in war room channel |
| 07:45 | War room Slack channel opened: `#analytics-launch` | Launch Owner | Invite: Product, Engineering, Marketing, Support lead |
| 07:50 | All team members online and confirmed available | Launch Owner | Engineering on-call active until 18:00 |
| 08:00 | Publish announcement page / update pricing page | Marketing | Verify live URL resolves correctly |
| 08:00 | Update in-app upgrade prompt to live state (visible to admin users) | Engineering | Confirm not showing to non-admin roles |
| 09:00 | Send announcement email to 340 qualifying accounts | Marketing | Monitor delivery rate and open rate in real-time |
| 09:05 | Post on LinkedIn | Marketing | Check for formatting issues on mobile |
| 09:10 | Post on Twitter/X | Marketing | |
| 09:15 | Post changelog entry | Marketing | |
| 10:00 | First status check: open rates, any error reports, support ticket count | Launch Owner | Post to `#analytics-launch`: "Status: 🟢/🟡/🔴" |
| 11:00 | Check error rates vs baseline — flag if >0.5% | Engineering | |
| 12:00 | Mid-day status update to team | Launch Owner | Any emerging issues? Any early conversions? |
| 15:00 | Read initial user feedback — support inbox, social replies, any beta customer messages | Support + Marketing | |
| 17:00 | End-of-day status update: activations, issues, support volume | Launch Owner | Share in `#analytics-launch` |
| 17:30 | Decision point: green to continue? Any issues requiring action overnight? | Launch Owner + Engineering | Document decision |

---

## Communication Plan

| Audience | Channel | Key message | Owner | When |
|---|---|---|---|---|
| Internal team | `#analytics-launch` Slack | "We're launching today. War room here. Kill switch: `analytics_module_enabled`. Rollback contact: [Eng lead]." | Launch Owner | 2026-06-01 07:45 |
| Support team | Live briefing + written FAQ | FAQ, known issues, escalation path — who to ping for what | Launch Owner | 2026-05-21 (1 week before) |
| Beta cohort (20 accounts) | Personal email from product lead | "You're getting early access — here's how to get started, here's who to call with questions" | Product | 2026-05-26 |
| Existing customers (340 accounts) | Announcement email | "Clearpath Analytics is here — real-time project health, resource reports, and a weekly exec summary auto-generated for you. Add it to your plan for $15/seat/month." | Marketing | 2026-06-01 09:00 |
| Non-openers (follow-up) | Email | Same message, different subject line | Marketing | 2026-06-08 |
| Non-converters (14-day) | Email | Use case / ROI angle — "How [similar company type] uses Analytics to cut reporting time" | Marketing | 2026-06-15 |
| Social followers | LinkedIn + Twitter/X | Feature announcement with visual, link to page | Marketing | 2026-06-01 09:05 |
| Press / analysts | Not required for this launch — existing customer focus only | — | — | — |

---

## Success Metrics

| Metric | Baseline | Target | Measurement | Review date |
|---|---|---|---|---|
| Accounts activated (purchased) — 30 days | 0 | 34 (10% of 340) | CRM / billing system | 2026-07-01 |
| Accounts activated — 90 days | 0 | 68 (20% of 340) | CRM / billing system | 2026-09-01 |
| Announcement email open rate | — | >40% | Email platform | 2026-06-03 |
| Announcement email click-to-activate rate | — | >8% | Email platform | 2026-06-08 |
| Executive summary sent (per active account, week 1) | — | >70% of activated accounts | Product analytics | 2026-06-08 |
| Weekly active accounts at day 30 | — | >80% of activated accounts | Product analytics | 2026-07-01 |
| Support ticket volume (analytics-related) | 0 | <15/week in weeks 1–2 | Support system | 2026-06-15 |
| Error rate (dashboard load, PDF generation) | — | <0.5% | Monitoring | Daily, week 1 |
| Add-on churn at 60 days | — | <5% of activated accounts | Billing system | 2026-08-01 |
| NPS for Analytics module (in-app survey at day 30) | — | >40 | In-app survey | 2026-07-01 |

**What "success" looks like on launch day:** 34+ accounts activating within 30 days, email open rate >40%, no critical bugs, support volume below threshold.

**Revenue context:** 34 accounts × ~85 seats avg × $15 = ~$43K MRR added in month 1. 68 accounts × 85 × $15 = ~$87K MRR at 90 days. These are conservative targets — revise if you have better seat count data.

---

## Post-Launch Review

**Scheduled:** 2026-06-09 (day 8 — end of first full week)
**Attendees:** Launch Owner, Product Lead, Marketing, Engineering Lead, Support Lead
**Location:** [meeting link]

### Metrics review template

| Metric | Baseline | Day 1 | Day 3 | Day 7 | Target | Status |
|---|---|---|---|---|---|---|
| Accounts activated | 0 | | | | 10 by day 7 | |
| Email open rate | — | | | | >40% | |
| Exec summaries sent | 0 | | | | >70% of activated | |
| Support tickets (analytics) | 0 | | | | <15/week | |
| Error rate | — | | | | <0.5% | |
| NPS (early signal) | — | | | | >40 | |

### Qualitative review

- [ ] **Top 3 things that went well**
- [ ] **Top 3 things that didn't go well**
- [ ] **Unexpected outcomes** — any surprises from beta or day-1 users?
- [ ] **User feedback themes** — what are people actually saying? (use `gtm:feedback-synthesis`)
- [ ] **Follow-up items** — bugs, quick wins, docs to improve

### Decision

- [ ] Continue rollout / no changes needed
- [ ] Iterate — [specific change] based on [specific feedback]
- [ ] Escalate — [issue] blocking adoption
- [ ] Update roadmap — [what we learned changes what we build next]

---

> **DRAFT — requires human review before execution begins**

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 13.0/16.0 (81%) |
| Evaluated | 2026-05-01 |
| Target duration | 138559 ms |
| Target cost | $0.2457 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | All marketing copy, messaging, and campaign content is labelled DRAFT and flagged for human review before use | PASS | The artifact opens and closes with '> **DRAFT — requires human review before execution begins**'. Chat response confirms 'The plan is saved to clearpath-analytics-launch-plan.md' without presenting any copy as final. |
| c2 | Applies positioning work before tactics — identifies the competitive alternative (Asana/Monday reporting), differentiator (executive summaries), and target segment (operations directors/PMOs at 50+ seat accounts) before writing messages | PASS | Pre-launch checklist item #1 (due May 8) is 'Positioning canvas completed… vs Asana and Monday.com', item #3 confirms 'mid-market Operations Director / PMO lead at 50+ seat account', and item #6 is battle card vs Asana/Monday — all before any copy or email tasks. Chat response says 'Run the positioning canvas before writing any copy.' |
| c3 | Leads messaging with the customer problem (e.g. blind spots in project health, lack of exec visibility) rather than feature descriptions | PASS | Checklist item #4 explicitly instructs: 'Key benefit articulated in buyer terms: not "RAG dashboard" but "know which projects are at risk before your Monday standup"'. One-sentence description example includes 'without exporting to spreadsheets', pointing to the pain. The plan structurally mandates problem framing over feature language. |
| c4 | Recommends a launch tier (given 340 existing customers and $15/seat add-on, this is likely a Tier 2 or Tier 1 launch — not a silent rollout) | PASS | Artifact has explicit '## Launch Tier: 1 — Major' section with rationale: 'New priced add-on module ($15/seat/month) targeting 340 existing accounts… Tier 1 checklist applies in full.' |
| c5 | Distinguishes between the existing customer expansion play (340 accounts) and any net-new motion — these require different approaches | PARTIAL | Communication plan notes 'Not required for this launch — existing customer focus only' for press/analysts, and all channels target the 340 qualifying accounts. However, there is no explicit section naming 'net-new acquisition' as a separate motion with different channels, messaging, or process — the distinction is implicit rather than deliberate. |
| c6 | Includes a post-launch review plan with success metrics — partial credit if metrics are named but no review timeline or owner is specified | PARTIAL | Post-Launch Review section specifies date (2026-06-09), attendees including 'Launch Owner', a metrics template with Day 1/3/7 columns, and a qualitative review checklist. Success metrics table includes 30-day and 90-day review dates. Ceiling is PARTIAL. |
| c7 | Produces a structured launch plan with phases and owners, not a list of marketing ideas | PASS | Artifact contains: 42-item pre-launch checklist with Owner and Due columns, Rollout Strategy table with stages and advancement criteria, Launch Day Run-of-Show with timed actions and owners, Communication Plan table, Success Metrics table, and Post-Launch Review template — all owner-tagged. |
| c8 | Output sizes the existing-customer revenue opportunity — 340 accounts × 50+ seats × $15/seat/month — yielding the upper-bound ARR (~$3M+) and a realistic conversion target (e.g. '30% adoption in year 1 → ~$900K ARR uplift') | PARTIAL | Revenue context in success metrics section shows '34 accounts × ~85 seats avg × $15 = ~$43K MRR' and '68 accounts × 85 × $15 = ~$87K MRR at 90 days'. However, the upper-bound ARR (~$5.2M: 340 × 85 × $15 × 12) is never calculated, and there is no year-1 adoption framing (e.g., 30% → ~$900K ARR). |
| c9 | Output's positioning anchors against Asana / Monday native reporting as the competitive alternatives, with the executive summary as the named differentiator — not a generic feature list | PASS | Item #1: 'Positioning canvas… competitive alternatives… vs Asana and Monday.com'. Item #6: 'Battle card written vs Asana reporting and Monday.com dashboards'. Chat response: 'the exec summary differentiator vs Asana/Monday needs to be sharp'. Executive summary is highlighted as the specific differentiator. |
| c10 | Output's customer-problem framing leads with the operations director / PMO pain — e.g. 'execs ask 'how are projects tracking?' and you spend half a day pulling a manual report' — not 'we have a new analytics module' | PARTIAL | Item #4 reframes RAG dashboard as 'know which projects are at risk before your Monday standup', which is benefit/problem-adjacent. However, the actual messaging example in the communication plan leads with features: 'real-time project health, resource reports, and a weekly exec summary auto-generated for you' — not the specific exec-pain narrative (execs asking, manual reporting burden) the criterion describes. |
| c11 | Output classifies this as Tier 1 or Tier 2 launch given 340 existing customers, $15/seat ARR uplift, and a 3-year-customer-base activation event — explicitly NOT a silent rollout | PASS | '## Launch Tier: 1 — Major' with explicit rationale citing new billing, new positioning, 340-account communication effort, and material impact on customer contracts. Chat response: 'That's not a standard feature launch.' |
| c12 | Output separates the existing-customer expansion motion (CSM-led, in-product upsell, QBR conversations) from any net-new acquisition motion — different channels, different messaging, different sales process | PARTIAL | In-product upsell prompt is present (item #9). Press/analysts are excluded ('existing customer focus only'). However, CSM-led motion, QBR conversations, and expansion playbooks are entirely absent. There is no explicit comparison of expansion vs. net-new channels, messaging, or sales process — only in-product and email channels are covered. |
| c13 | Output's launch plan has phases with owners and dates — Pre-launch (weeks -4 to 0): readiness checklist, sales enablement, beta close-out; Launch week: announcements, in-product, customer comms; Post-launch (weeks 1-12): adoption tracking, expansion plays, feedback loops | PASS | Pre-launch checklist runs May 7–29 with 42 owner-tagged items including battle cards, support training, beta. Rollout Strategy table has Internal dogfood (May 19), Beta (May 26), GA (June 1). Launch Day Run-of-Show covers June 1 in detail. Post-launch review scheduled June 9 with 30-day (July 1) and 90-day (Sept 1) metric checkpoints. |
| c14 | Output's marketing copy and messaging examples are labelled DRAFT — explicitly flagged for human review before publication | PASS | Document-level DRAFT label appears at both top and bottom of the artifact. All marketing copy items (announcement email, LinkedIn post, Twitter post) are 'Pending' tasks rather than completed copy, consistent with the overall DRAFT designation. |
| c15 | Output's post-launch review plan names success metrics (e.g. trial signups, paid conversions, % of 340-base activated, $ ARR uplift), a review date (e.g. 'Day 30, Day 60, Day 90 reviews'), and a review owner | PASS | Post-launch review section: date 2026-06-09, owner 'Launch Owner'. Success metrics table names accounts activated (% of 340), MRR targets, email open rate, exec summaries sent, NPS — with review dates 2026-07-01 (Day 30) and 2026-09-01 (Day 90). Day 60 is absent but Day 30/90 are present. |
| c16 | Output addresses internal readiness alongside external launch — sales enablement (battle cards, demo scripts), CSM enablement (expansion playbooks), support training, docs ready before announce | PARTIAL | Battle card is item #6 (due May 14). Support training: items #17–21 (FAQ, walkthrough, escalation path, staffing plan). Docs: items #13–16 (help center, admin guide, changelog). Missing: demo scripts and CSM expansion playbooks — no customer success enablement material is included. |
| c17 | Output addresses pricing communication carefully — $15/seat add-on for existing customers may need grandfathering for early adopters or volume discounting at the 340 mid-market scale | FAIL | No mention of grandfathering, early-adopter pricing, or volume discounting anywhere in the artifact or chat response. FAQ item #17 lists 'billing' as a topic but does not specify grandfathering or discount considerations. $15/seat/month is stated as a flat price throughout. |

### Notes

The output is a solid, well-structured Tier 1 launch plan with clear phasing, owner-tagged tasks, DRAFT labeling, and appropriate positioning sequencing. Strong areas: launch tier classification, structured checklist with 42 owner-tagged items, competitive anchoring against Asana/Monday with exec summary as differentiator, beta-to-GA rollout rationale, and post-launch review scaffolding. Key gaps: (1) no upper-bound ARR calculation (~$5.2M potential vs. the ~$43K–$87K MRR targets shown); (2) CSM-led expansion motion and QBR conversations are entirely absent — only in-product upsell and email channels are present; (3) the actual messaging example in the communication plan leads with features rather than exec pain; (4) no mention of grandfathering or volume discounting for the existing mid-market customer base; (5) the net-new vs. expansion-motion distinction is implicit rather than explicit. Verdict sits just above the 80% PASS threshold.
