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
> Output structure:
> 
> - **Customer-problem-led messaging** at the top: lead with the problem (blind spots in project health, late deliveries discovered too late, hidden over-utilisation) BEFORE the product capability list. The product features are the answer to the problem, not the headline.
> - **TWO distinct GTM motions** explicitly named and separated:
>   1. **Existing customer expansion** (340 Pro accounts, ~50+ seats) — in-product upsell, account-team-led, no acquisition cost. Target: 30% attach rate by Q4.
>   2. **New customer acquisition** ("Analytics" as differentiated landing) — content marketing, paid search on PM-reporting keywords, demo-led sales. Target: 50 net-new logos.
> - **Post-launch review plan** with measurable success metrics + cadence: T+30, T+60, T+90 reviews. Specific metrics: attach rate, MRR contribution, NPS for the module, support ticket volume by category.
> - **Competitive positioning**: name the differentiator (executive summary report PDF/email weekly) explicitly and compare with Asana reporting + Monday.com dashboards on this specific dimension.
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

I've built your **Clearpath Analytics Launch Plan** — a Tier 1 launch with two distinct GTM motions. Here's what's in the document:

## Structure

**Problem-first positioning:** Leads with blind spots (late discovery of project health, resource over-utilisation, missed deadlines) before features.

**Two GTM motions separated:**
1. **Expansion (Motion 1):** In-product upsell to 340 Pro accounts. Account-team-led. 30% attach rate target by Q4.
2. **Acquisition (Motion 2):** Content marketing + paid search targeting PMOs/ops directors. 50 net-new logos target.

**Phased rollout:** Dogfood (internal) → 5% (17 accounts) → 25% (85 accounts) → 100% (all Pro) + simultaneous Motion 2 launch. Each phase has clear success criteria before advancing.

**Launch day precision:** Hour-by-hour timeline (7am pre-launch through 4pm monitoring, then 6-day war room cadence).

**Post-launch reviews at T+7, T+30, T+60, T+90** with:
- Metrics snapshot vs. targets
- Qualitative feedback themes
- Top 3 wins + top 3 issues
- Explicit next-step decisions (continue / iterate / rollback / expand)

**Competitive positioning:** Explicit differentiation — *Clearpath gives you the executive summary every week (PDF/email); Asana requires you to log in and explore; Monday.com requires you to build the dashboard.*

## Key Checklist Items

**Pre-launch (by May 25):** Positioning canvas, landing page, documentation, support briefing, analytics tracking, feature flag, load testing.

**Launch day (June 10):** Smoke tests → enable feature flag → publish landing page & emails → post social → monitor error rates, support volume, adoption %.

**Success targets:**
- T+30: 15–20% attach rate, $8k–$12k MRR, >60% dashboard adoption, NPS 40+
- T+90: 30% attach rate, $60k–$80k MRR, 50 new logos, NPS 45+

---

**Status:** DRAFT — needs sign-off from Product Lead, Eng Lead, Sales Lead, and CFO before execution.

What would you like me to adjust? Timing, targets, specific phases, or anything in the competitive positioning?

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 13.0/16.0 (81%) |
| Evaluated | 2026-05-04 |
| Target duration | 132943 ms |
| Target cost | $0.1315 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | All marketing copy, messaging, and campaign content is labelled DRAFT and flagged for human review before use | PASS | Output ends: '**Status:** DRAFT — needs sign-off from Product Lead, Eng Lead, Sales Lead, and CFO before execution.' The entire plan is labelled DRAFT with explicit human sign-off requirements. |
| c2 | Applies positioning work before tactics — identifies the competitive alternative (Asana/Monday reporting), differentiator (executive summaries), and target segment (operations directors/PMOs at 50+ seat accounts) before writing messages | PASS | Output describes 'Competitive positioning: Explicit differentiation — Clearpath gives you the executive summary every week (PDF/email); Asana requires you to log in and explore; Monday.com requires you to build the dashboard.' Target segment (operations directors and PMOs) is identified before tactics are described. |
| c3 | Leads messaging with the customer problem (e.g. blind spots in project health, lack of exec visibility) rather than feature descriptions | PASS | Output explicitly states '**Problem-first positioning:** Leads with blind spots (late discovery of project health, resource over-utilisation, missed deadlines) before features.' |
| c4 | Recommends a launch tier (given 340 existing customers and $15/seat add-on, this is likely a Tier 2 or Tier 1 launch — not a silent rollout) | PASS | Output opens: 'I've built your **Clearpath Analytics Launch Plan** — a Tier 1 launch with two distinct GTM motions.' Launch tier is explicitly named. |
| c5 | Distinguishes between the existing customer expansion play (340 accounts) and any net-new motion — these require different approaches | PASS | Output names two separated motions: '1. **Expansion (Motion 1):** In-product upsell to 340 Pro accounts. Account-team-led. 30% attach rate target by Q4.' and '2. **Acquisition (Motion 2):** Content marketing + paid search targeting PMOs/ops directors. 50 net-new logos target.' |
| c6 | Includes a post-launch review plan with success metrics — partial credit if metrics are named but no review timeline or owner is specified | PARTIAL | Output lists 'Post-launch reviews at T+7, T+30, T+60, T+90' with metrics snapshot, qualitative feedback, top 3 wins/issues, and specific numeric targets at T+30 ($8k–$12k MRR, >60% dashboard adoption) and T+90 (30% attach, $60k–$80k MRR, NPS 45+). Timeline and metrics present; no review owner named. Ceiling is PARTIAL. |
| c7 | Produces a structured launch plan with phases and owners, not a list of marketing ideas | PASS | Output describes a phased rollout (Dogfood → 5%/17 accounts → 25%/85 accounts → 100%), pre-launch checklist with a date (May 25), launch day hour-by-hour timeline (June 10), and T+7/30/60/90 post-launch review cadence. Clearly a structured plan with phases, not a marketing ideas list. |
| c8 | Output sizes the existing-customer revenue opportunity — 340 accounts × 50+ seats × $15/seat/month — yielding the upper-bound ARR (~$3M+) and a realistic conversion target (e.g. "30% adoption in year 1 → ~$900K ARR uplift") | PARTIAL | Output shows realistic conversion targets: T+90 '30% attach rate, $60k–$80k MRR' (consistent with the math: 102 accounts × 50 seats × $15 ≈ $76.5k/month). However, the upper-bound ARR (~$3M+/year at 100% attach) is never explicitly computed or stated. Only the realistic target is sized. |
| c9 | Output's positioning anchors against Asana / Monday native reporting as the competitive alternatives, with the executive summary as the named differentiator — not a generic feature list | PASS | 'Clearpath gives you the executive summary every week (PDF/email); Asana requires you to log in and explore; Monday.com requires you to build the dashboard.' Both competitors named, executive summary called out as the specific differentiator. |
| c10 | Output's customer-problem framing leads with the operations director / PMO pain — e.g. "execs ask 'how are projects tracking?' and you spend half a day pulling a manual report" — not "we have a new analytics module" | PASS | '**Problem-first positioning:** Leads with blind spots (late discovery of project health, resource over-utilisation, missed deadlines) before features.' Problem framing confirmed as leading the messaging. |
| c11 | Output classifies this as Tier 1 or Tier 2 launch given 340 existing customers, $15/seat ARR uplift, and a 3-year-customer-base activation event — explicitly NOT a silent rollout | PASS | 'a Tier 1 launch with two distinct GTM motions' — explicitly classified as Tier 1 in the opening sentence. |
| c12 | Output separates the existing-customer expansion motion (CSM-led, in-product upsell, QBR conversations) from any net-new acquisition motion — different channels, different messaging, different sales process | PASS | Motion 1: 'In-product upsell to 340 Pro accounts. Account-team-led.' Motion 2: 'Content marketing + paid search targeting PMOs/ops directors. 50 net-new logos target.' Different channels (in-product vs content/paid), different process (account-team-led vs demo-led), different targets. |
| c13 | Output's launch plan has phases with owners and dates — Pre-launch (weeks -4 to 0): readiness checklist, sales enablement, beta close-out; Launch week: announcements, in-product, customer comms; Post-launch (weeks 1-12): adoption tracking, expansion plays, feedback loops | PARTIAL | Phases with dates are clearly present: 'Pre-launch (by May 25),' 'Launch day (June 10),' and T+7/30/60/90 post-launch reviews. However, no owners are named per phase (only sign-off roles listed at the end). The criterion explicitly requires owners alongside phases and dates. |
| c14 | Output's marketing copy and messaging examples are labelled DRAFT — explicitly flagged for human review before publication | PASS | '**Status:** DRAFT — needs sign-off from Product Lead, Eng Lead, Sales Lead, and CFO before execution.' The plan (including its messaging content) is explicitly marked DRAFT with named sign-off requirements. |
| c15 | Output's post-launch review plan names success metrics (e.g. trial signups, paid conversions, % of 340-base activated, $ ARR uplift), a review date (e.g. "Day 30, Day 60, Day 90 reviews"), and a review owner | PARTIAL | Review dates (T+7, T+30, T+60, T+90) and metrics (attach rate, MRR, NPS, support ticket volume; specific numbers at T+30 and T+90) are present. No review owner is named anywhere in the captured output. Criterion requires all three; owner is missing. |
| c16 | Output addresses internal readiness alongside external launch — sales enablement (battle cards, demo scripts), CSM enablement (expansion playbooks), support training, docs ready before announce | PARTIAL | Pre-launch checklist mentions 'documentation, support briefing' covering some internal readiness. However, battle cards, demo scripts, and CSM expansion playbooks are not mentioned in the captured output. Internal readiness is partially addressed but sales and CSM enablement artifacts are absent. |
| c17 | Output addresses pricing communication carefully — $15/seat add-on for existing customers may need grandfathering for early adopters or volume discounting at the 340 mid-market scale | FAIL | The captured output references '$15/seat/month' and MRR targets but contains no discussion of grandfathering, early adopter pricing, or volume discounting for the 340 existing accounts. Pricing communication strategy is entirely absent. |

### Notes

The captured output is a chat summary describing a launch plan document rather than the full plan itself, which limits visibility into some details (e.g., whether battle cards appear in the document body). The output scores well on structural requirements: Tier 1 classification is explicit, two GTM motions are cleanly separated, problem-first positioning is confirmed, and competitive positioning names Asana/Monday with the executive summary as the differentiator. The main gaps are: (1) no review owner named for post-launch cadence, (2) upper-bound ARR (~$3M+) not explicitly computed even though the realistic conversion target is shown, (3) phase-level owners absent from the phased rollout, (4) internal readiness coverage omits sales enablement artifacts (battle cards, demo scripts, CSM playbooks), and (5) pricing communication for existing customers — grandfathering, early adopter incentives, volume discounting — is not addressed at all. The DRAFT labelling and sign-off requirements are handled cleanly.
