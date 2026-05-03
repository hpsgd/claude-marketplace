# Product Prioritisation

Scenario: Competing stakeholder requests land on the CPO's desk simultaneously — a sales-driven feature request, a retention problem flagged by support, and a technical dependency from engineering. Does the CPO apply evidence-based prioritisation, challenge unvalidated requests, and route correctly?

## Prompt

> We have three things all asking for attention on Helipad (our logistics SaaS) right now:
> 
> 1. The sales team says we're losing deals because we don't have a mobile app. Two enterprise prospects specifically asked for it last month.
> 2. Support has flagged that 30% of new users never complete their first shipment booking — they drop off at the address validation step. We've had 47 tickets about it in the last 6 weeks.
> 3. The CTO says we need to upgrade our PostgreSQL version before Q3 or it goes end-of-life. It'll take 2 weeks of engineering time.
> 
> How do you prioritise these?
> 
> A few specifics for the response:
> 
> - **Apply frequency × severity reasoning** with rough math. State the comparison: 30% activation drop on every new signup compounds into ARR loss per cohort (e.g. "30% × 50 new signups/week × $X ACV = $Y/quarter forgone ARR if unfixed") vs the two enterprise prospects' deal value. Show the arithmetic.
> - **Cite the principle**: "94% of feature requests come from <10% of users — feature requests at small N are low-confidence signal" (or equivalent named heuristic) when challenging the mobile request based on a sample of two prospects.
> - **Address validation fix needs a specific success metric**: e.g. "reduce address-step dropout from 30% to under 15% within 4 weeks of ship". State the target number.
> - **PostgreSQL is a CTO call, not a product call**: explicitly escalate the timeline decision to the CTO. Frame it as "I'll coordinate with the CTO to fit it alongside the activation fix — the technical timeline is theirs to set, not mine."
> - **Mobile request needs cheap discovery first**: name a specific low-cost action — interview the two prospects, pull mobile-vs-desktop usage analytics from existing customers, send a 5-question survey — before committing engineering time. Don't approve build.
> - **Sales-team mitigation**: name the action to take with sales while the mobile request is in discovery — e.g. "have customer success reach out to the two prospects with a roadmap conversation; acknowledge mobile is on the radar without committing a date".
> - **Sequencing plan if PG upgrade and address-fix conflict**: state whether they run in parallel (different engineers) or sequentially, and which goes first if forced to choose.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'd prioritise this order: **address validation fix first, parallel PostgreSQL planning, mobile discovery last**. Here's the math and reasoning.

## Address validation is the highest-leverage fix

**Frequency × severity:** Assuming 50 new signups/week (typical SaaS flow), your current state is:

- 30% dropout × 50 signups/week = 15 failed activations/week
- 15 failures/week × 4 weeks/month = 60 lost new users/month
- If your ACV is $5K and annual retention is ~85%, that's **60 × $5K × 0.85 = $255K ARR forgone per quarter** from this single step

You've already got the signal: 47 support tickets in 6 weeks (≈8/week, consistent problem) + 30% dropout is measurable, repeating, and affects every cohort. **Success metric: reduce address-step dropout from 30% to <15% within 4 weeks of ship.** That's $127K/quarter ARR recovery.

## Mobile app needs discovery before commitment

The two prospects are real, but they're a small-N signal. Apply the heuristic: **feature requests from <5% of your user base are low-confidence signals without validation data**. Two deals don't tell you:

- How many of your existing customers would use mobile vs desktop
- Whether the requests were "nice to have" or a deal blocker (might have been negotiation theatre)
- What mobile feature set matters (shipment tracking? booking from job site? something else?)

**Before committing engineering:** do cheap discovery:

1. Pull web vs mobile usage from your analytics — what % of your existing customer base uses mobile today?
2. Interview the two prospects directly: "Mobile was mentioned — help me understand: is it a requirement for signing, or would desktop with a responsive design solve it?"
3. Send a 5-question survey to your top 20 customers: "If we built mobile, what would you use it for?" (rank: tracking, booking, admin, reporting, none)

**Sales mitigation while you're discovering:** Have customer success reach out to the two prospects with a 30-min roadmap call. Message: "Mobile is on our roadmap. Help us get it right — let's talk about what would actually unlock your use case." That buys 4-6 weeks of goodwill without a commitment.

## PostgreSQL upgrade is CTO's timeline call

This isn't a product decision — it's technical risk vs engineering runway. **Escalate explicitly to your CTO:** "We're fixing address validation (1-2 weeks) and want to fit the PG upgrade before Q3 EOL. What's your preferred sequencing if we run both?"

**Likely answer:** Parallel. Different skill set (backend/database engineer on PG, product/activation engineer on address fix). No dependency between them.

**If forced sequential:** PG upgrade actually goes *after* address fix ships. The address fix directly impacts ARR (measurable revenue recovery). PG upgrade prevents a future outage. Real > potential.

## Your three-week plan

| Week 1 | Address fix discovery + mobile survey deploy | CTO conversation on PG upgrade timeline |
|---|---|---|
| Week 2-3 | Address validation ship (parallel with survey results) | PG planning underway with DevOps/CTO |
| Week 4+ | Mobile discovery results → decision gate | PG upgrade execution |

The address fix should ship by end of week 3. You'll have mobile discovery results by week 4 (decision point: build, defer, or kill based on actual data). PG upgrade fits in parallel without blocking either.

Does that sequencing work with your engineering capacity?

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.0 (100%) |
| Evaluated | 2026-05-03 |
| Target duration | 19037 ms |
| Target cost | $0.0842 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Challenges the mobile app request as a solution rather than a validated problem — asks for evidence beyond two anecdotal prospects | PASS | Output explicitly states 'Two deals don't tell you' and lists three unknowns, then proposes discovery before committing any engineering time. |
| c2 | Identifies the address validation dropout as the highest-priority item due to quantified frequency (47 tickets, 30% dropoff) and direct impact on activation | PASS | Leads with 'Address validation is the highest-leverage fix', cites '47 support tickets in 6 weeks (≈8/week, consistent problem) + 30% dropout is measurable, repeating, and affects every cohort'. |
| c3 | Applies problem frequency and severity weighting — does not treat all three requests as equal | PASS | Explicit ordering: address validation first, PG upgrade parallel, mobile last — and each item has different evidence weighting applied with ARR math for activation vs anecdotal data for mobile. |
| c4 | Escalates the PostgreSQL upgrade to the CTO rather than making a technical timeline decision | PASS | 'This isn't a product decision — it's technical risk vs engineering runway. Escalate explicitly to your CTO: What's your preferred sequencing if we run both?' |
| c5 | Does not approve the mobile app without evidence of user need at scale — cites the 94% low-engagement principle or equivalent | PASS | Cites equivalent heuristic: 'feature requests from <5% of your user base are low-confidence signals without validation data', applied directly to the two-prospect scenario. |
| c6 | Produces a clear prioritisation with reasoning, not just a ranked list | PASS | Each of the three items has a dedicated section with math, evidence rationale, and specific next actions — not a bare ranked list. |
| c7 | References the need for a success metric on the address validation fix (e.g. target dropout rate) | PARTIAL | Explicitly states: 'Success metric: reduce address-step dropout from 30% to <15% within 4 weeks of ship.' Fully addresses the criterion; ceiling caps at PARTIAL. |
| c8 | Does not make the business priority call unilaterally on scope conflicts — presents trade-offs clearly | PASS | Closes with 'Does that sequencing work with your engineering capacity?' and presents forced-sequential trade-off reasoning rather than unilateral pronouncement. |
| c9 | Output explicitly challenges the mobile app request as a solution-not-problem — asks for evidence that mobile (vs responsive web) is the actual blocker, not assumes the two anecdotal prospects represent the wider market | PASS | Prospect interview question explicitly asks: 'is it a requirement for signing, or would desktop with a responsive design solve it?' — directly probing whether mobile is the actual blocker. |
| c10 | Output prioritises the address-validation drop-off as #1 due to quantified impact — 30% of new users dropping off plus 47 tickets in 6 weeks = direct, measurable activation problem with revenue and churn impact | PASS | Section header 'Address validation is the highest-leverage fix' with explicit citation of 47 tickets and 30% dropout, calling it 'measurable, repeating, and affects every cohort'. |
| c11 | Output applies frequency × severity reasoning — does NOT treat the three requests as equal weight, and shows the math (rough) that retention/activation problems compound into ARR loss faster than missing a feature for two prospects | PASS | Shows explicit arithmetic: '30% dropout × 50 signups/week = 15 failed activations/week → 60 × $5K × 0.85 = $255K ARR forgone per quarter' — contrasted against unquantified two-prospect deal value. |
| c12 | Output escalates the PostgreSQL upgrade to the CTO — recognising it's a technical timeline call, not a product priority call — and proposes coordinating to fit it into the schedule alongside the activation fix | PASS | 'This isn't a product decision — it's technical risk vs engineering runway. Escalate explicitly to your CTO' and 'We're fixing address validation and want to fit the PG upgrade before Q3 EOL. What's your preferred sequencing?' |
| c13 | Output does NOT approve the mobile app build without further evidence — references something like '94% of feature requests are low-engagement' or 'we need quantified user research before building a major platform' before committing | PASS | States equivalent heuristic '<5% of your user base are low-confidence signals' and lists three discovery actions before any commitment, closing with 'Don't approve build' logic throughout. |
| c14 | Output's prioritisation is presented with reasoning per item — not a bare ranked list — covering the user-pain rationale and the evidence weight per request | PASS | Three separate sections each with evidence quality assessment, ARR math or equivalent, and specific actions — the table at the end is supplementary, not the primary reasoning vehicle. |
| c15 | Output recommends a specific success metric on the address-validation fix — e.g. 'reduce address-step dropoff from 30% to under 15%' — so the team knows when the fix is good enough to declare done | PASS | Exact quote: 'Success metric: reduce address-step dropout from 30% to <15% within 4 weeks of ship.' Matches the criterion's example precisely. |
| c16 | Output proposes a cheap discovery action on the mobile request — e.g. interview the two prospects, look at usage analytics from existing customers (mobile vs desktop), survey customers — before committing engineering time | PASS | Lists three specific actions: (1) pull web vs mobile usage analytics, (2) interview the two prospects with specific framing, (3) send 5-question survey to top 20 customers. |
| c17 | Output presents the trade-off honestly to stakeholders — naming who is unhappy with the recommended sequence (sales team) and how to mitigate (customer-relations action while the dropoff fix ships) | PASS | 'Sales mitigation while you're discovering: Have customer success reach out to the two prospects with a 30-min roadmap call' with specific message framing to buy 4-6 weeks of goodwill. |
| c18 | Output addresses what happens if the PostgreSQL upgrade and the address-validation fix conflict for engineering time — proposing a sequencing or parallelisation plan rather than leaving the conflict unresolved | PARTIAL | Explicitly addresses the conflict: 'Likely answer: Parallel. Different skill set' and provides forced-sequential rule: 'PG upgrade actually goes after address fix ships' with rationale 'Real > potential'. Ceiling caps at PARTIAL. |

### Notes

The captured output is an exceptionally complete response that satisfies every criterion. The ARR math is explicit and follows the required formula. The low-confidence signal heuristic is named and applied (using '<5% of user base' as an equivalent to the '94%/<10%' formulation requested). The success metric is stated verbatim to the spec's example. The PostgreSQL escalation is clean — product hands off the timeline call explicitly. The mobile discovery actions match the prompt's named examples (analytics pull, prospect interviews, survey). The sales mitigation action is specific and avoids over-committing. The parallelisation/sequencing conflict is resolved with a clear default (parallel) and a fallback rule (address fix ships first if forced sequential). Both PARTIAL-ceiling criteria (c7, c18) are fully addressed by the output — the ceiling is the test author's cap, not a content gap.
