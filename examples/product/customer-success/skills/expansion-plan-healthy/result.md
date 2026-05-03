# Expansion Plan Healthy

Scenario: A customer success manager requests an expansion plan for a high-performing account. The account has strong utilisation, positive QBR history, and the customer has proactively asked about a higher tier. The skill should pass the health gate and produce a real expansion plan.

## Prompt

> /customer-success:expansion-plan Meridian Legal is at $180k ARR, 92% seat utilisation (115/125 seats), health score 85, just completed their third QBR showing 40% time savings. They've been asking about our API integration tier.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

# Expansion Plan: Meridian Legal

## Health Check
- **Seat utilisation:** 115 / 125 = **92%**
- **Health score:** **85 / 100**
- **Status:** Healthy
- **Clear to expand:** **Yes**

All gates clear. No churn signals. Third QBR delivered, 40% time savings confirmed as a quantified outcome, and the customer is organically asking about the next tier.

---

## Expansion Signals

| Signal | Evidence | Strength |
|---|---|---|
| Hitting usage limits | 92% seat utilisation (115/125) — 10 seats headroom. Any team growth trips the ceiling within one hiring cycle | Strong |
| Requesting higher-tier feature | Customer proactively asked about API integration tier — inbound, not sales-led | Strong |
| After success milestone | Third QBR just completed with 40% time savings demonstrated. Customer is in a value-confirmed, receptive state | Strong |
| Executive engagement | Three QBRs completed signals sustained executive sponsorship and structured engagement | Moderate |

Four signals present, three strong, all organic. Quantified readiness check: utilisation 92% (exceeds 60% threshold), health 85 (exceeds 70 threshold), QBR engagement confirmed, executive sponsor active.

---

## Opportunity

**Current ARR:** $180,000
**Pricing basis:** $180k ÷ 125 seats = **$1,440 / seat / year**

### Expansion type: Combined — Seat Expansion + API Tier Upsell

Two independent value drivers are present simultaneously. Model them separately so the commercial proposal can be staged if needed.

#### Driver 1 — Seat Expansion

| Scenario | New seats | Rate | Expansion ARR |
|---|---|---|---|
| Conservative (10 seats) | 135 total | $1,440/seat | **+$14,400** |
| Base (20 seats) | 145 total | $1,440/seat | **+$28,800** |
| Optimistic (30 seats) | 155 total | $1,440/seat | **+$43,200** |

*Assumption: same per-seat rate applies for expansion block. Adjust if volume discount applies at 150+ seats.*

#### Driver 2 — API Integration Tier Upsell

Without confirmed API tier pricing, two common models are presented. Confirm actuals before proposal:

| Pricing model | Assumption | Expansion ARR |
|---|---|---|
| Flat platform fee | $2,500/month (usage-based entry point) | **+$30,000** |
| Per-seat premium | $240/seat/year × 125 seats | **+$30,000** |

Both models land similarly. Use whichever aligns to your actual pricing structure.

#### Combined Scenarios

| Scenario | Seat expansion | API tier | Total expansion ARR | New ARR | NRR |
|---|---|---|---|---|---|
| Conservative | +$14,400 (10 seats) | +$30,000 | **+$44,400** | $224,400 | 125% |
| Base | +$28,800 (20 seats) | +$30,000 | **+$58,800** | $238,800 | 133% |
| Optimistic | +$43,200 (30 seats) | +$30,000 | **+$73,200** | $253,200 | 141% |

**Confidence:** High (seat driver) + Medium (API tier — pending technical readiness confirmation)
**Timeline:** Commercial proposal by end of May 2026, aligned to likely mid-year budget review cycle

---

## Approach

**Framing:** Meridian has already proven 40% time savings at the current tier. The API integration tier removes the manual handoff step — their productivity gains get embedded into existing firm workflows rather than living inside the product. Seats frame as team enablement: "Your team has grown to the point where access is a bottleneck, not the work itself."

**Timing:** Strike within two weeks of the QBR. The 40% time savings figure is fresh and confirmed. The customer referenced the API tier themselves — this is a warm door, not a cold pitch. Waiting past the end of May risks the momentum cooling and budget attention shifting to other priorities.

**Trigger:** The customer's own question about the API tier is the entry point. Respond to it directly, not as a product pitch, but as a scoping conversation: "You mentioned the API tier — tell us more about the workflow you're trying to connect. Let's make sure it's the right fit before we scope anything."

---

## Risks

| Risk | Why it applies | Gating action |
|---|---|---|
| Engineering capacity for API integration | API tier only delivers value if the customer can build and maintain integrations. Legal tech firms often have limited in-house engineering | Confirm internal engineering resource or SI partner before proposing the tier. If capacity is absent, scope an implementation support package alongside the tier |
| Seat expansion onboarding load | Adding 10–30 users to a 115-person deployment requires structured onboarding. Doing it without a plan creates a negative experience for new users and risks health score regression | Agree a rollout plan (cohort size, onboarding sessions, champions identified) before seats go live |
| API integration complexity extending time-to-value | If the integration takes 3–6 months to build, the customer will judge the tier on post-go-live results that are distant from the sale. Expectation gap risks post-expansion dissatisfaction | Set realistic milestones in the scoping call. Define a 30-day early-value checkpoint that doesn't depend on full integration completion (e.g. a read-only API use case) |
| Seat ceiling hit mid-year | At 92% utilisation and any team growth, the customer could hit 125/125 before a seat expansion is formalised | Flag this to the customer now as part of the conversation — framing it as proactive planning, not a sales push |

---

## Execution Plan

| Phase | Step | Action | Owner | Date |
|---|---|---|---|---|
| Discovery | 1 | Prepare value summary: 40% time savings → firm-level impact (billable hours recovered, matter throughput). Connect QBR outcomes explicitly to API tier readiness narrative | CSM | May 7, 2026 |
| Discovery | 2 | Schedule API discovery call — respond to their question directly. Goal: understand the workflow they want to connect, not pitch the tier | CSM | May 9, 2026 |
| Scoping | 3 | Technical readiness assessment: confirm whether internal engineering capacity exists or SI partner is needed. Size the integration scope | CSM + Solutions | May 16, 2026 |
| Scoping | 4 | Seat headroom conversation: present utilisation data (92%), propose expansion block (10–30 seats), confirm current headcount trajectory | CSM | May 16, 2026 |
| Trial | 5 | API tier demo / sandbox access — focus on the specific workflow identified in discovery. Involve their technical lead | CSM + Product | May 23, 2026 |
| Commercial | 6 | Commercial proposal: staged option (seats first, API tier with defined start date) OR combined. Present both adoption scenarios | CSM + Sales | June 5, 2026 |
| Rollout | 7 | Seat expansion rollout — cohort-based onboarding, champions identified per team | CSM | June 19 – July 10, 2026 |
| Rollout | 8 | API integration kickoff — milestones agreed, 30-day early-value checkpoint defined | CSM + Solutions | June 19, 2026 |
| Review | 9 | Post-expansion review: adoption metrics, health score check, customer confirmation of value | CSM | August 15, 2026 |

---

## Success Criteria

| Criteria | Measurement | Target | Date |
|---|---|---|---|
| Seat adoption | New seats active (logged in, using core features) within 30 days of provisioning | ≥ 50% of new seats active | July 31, 2026 |
| API tier activation | At least one integration live and processing real workflows | First production workflow running | July 31, 2026 |
| Health stability | Health score stable or improved post-expansion | Score ≥ 85 (pre-expansion baseline) | August 15, 2026 |
| Value confirmed | Customer explicitly confirms API tier is reducing the manual handoff they described in discovery | Positive verbal or written confirmation at post-expansion review | August 15, 2026 |
| Relationship maintained | Expansion was experienced as enablement — no friction in commercial conversation, NPS maintained | No relationship score regression at next QBR | Q3 QBR, 2026 |

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 13.5/13.5 (100%) |
| Evaluated | 2026-05-01 |
| Target duration | 70308 ms |
| Target cost | $0.0998 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | PASS: Health prerequisite check passes and expansion planning proceeds | PASS | Explicit 'Health Check' section states 'Clear to expand: Yes' with seat utilisation 92%, health score 85/100, and 'Status: Healthy'. Output proceeds directly to full expansion planning. |
| c2 | PASS: Expansion is framed as customer enablement, not a sales motion | PASS | Approach section: 'The API integration tier removes the manual handoff step — their productivity gains get embedded into existing firm workflows.' Trigger section says to respond 'not as a product pitch, but as a scoping conversation.' |
| c3 | PASS: The specific signal (customer asking about API tier) is used as the expansion anchor | PASS | Expansion Signals table lists 'Requesting higher-tier feature: Customer proactively asked about API integration tier — inbound, not sales-led' as a Strong signal. Trigger section: 'The customer's own question about the API tier is the entry point.' |
| c4 | PASS: Revenue impact is estimated with assumptions stated | PASS | Pricing basis derived ($180k ÷ 125 seats = $1,440/seat/year). Seat expansion scenarios (conservative/base/optimistic) shown. API tier modeled in two ways with stated assumptions: 'Without confirmed API tier pricing, two common models are presented. Confirm actuals before proposal.' |
| c5 | PASS: A timeline with milestones is produced, not just 'upsell them' | PASS | 9-step Execution Plan with specific dates: May 7 (value summary), May 9 (discovery call), May 16 (technical assessment + seat conversation), May 23 (demo/sandbox), June 5 (commercial proposal), June 19–July 10 (rollout), August 15 (post-expansion review). |
| c6 | PARTIAL: Risk factors for the expansion are identified (e.g., adoption risk on a new tier) | PARTIAL | Dedicated Risks section lists 4 risks with gating actions: engineering capacity for API integration, seat expansion onboarding load, API complexity extending time-to-value, and seat ceiling hit mid-year. Ceiling capped at PARTIAL. |
| c7 | PASS: The plan references the customer's demonstrated value (40% time savings) as proof of readiness | PASS | Referenced in Health Check ('40% time savings confirmed'), Expansion Signals ('Third QBR just completed with 40% time savings demonstrated. Customer is in a value-confirmed, receptive state'), and Approach ('Meridian has already proven 40% time savings at the current tier'). |
| c8 | PASS: Output's health prerequisite check passes explicitly — citing the four positive signals (92% utilisation, health score 85, 3 successful QBRs, customer-initiated tier inquiry) — and proceeds to plan | PASS | Health Check section lists utilisation 92%, health score 85. Quantified readiness check line: 'utilisation 92% (exceeds 60% threshold), health 85 (exceeds 70 threshold), QBR engagement confirmed, executive sponsor active.' All four signals explicitly cited. |
| c9 | PASS: Output uses the customer's specific request (asking about API integration tier) as the expansion anchor — meeting them where they are, NOT pivoting to a different tier or bundle | PASS | Trigger section: 'The customer's own question about the API tier is the entry point. Respond to it directly, not as a product pitch, but as a scoping conversation.' Driver 2 is entirely built around the API Integration Tier the customer mentioned. |
| c10 | PASS: Output's revenue impact estimate is shown with assumptions — e.g. 'API tier adds $X/seat or $Y flat; 115 active seats currently; potential ARR uplift $Z assuming 100% adoption, $Z/2 assuming 50%' — with the math and the assumption stated | PASS | Math shown: $180k ÷ 125 = $1,440/seat. Seat expansion ARR calculated per scenario. API tier modeled as flat $2,500/month ($30k/year) or $240/seat × 125 ($30k/year) with explicit note 'Confirm actuals before proposal.' Combined scenario table shows NRR 125–141%. |
| c11 | PASS: Output's enablement-not-sales framing is visible — the recommendation discusses what API integration would unlock for Meridian Legal (e.g. integrating with their case management system, automating client intake), NOT 'let's grow account revenue' | PASS | Approach: 'The API integration tier removes the manual handoff step — their productivity gains get embedded into existing firm workflows rather than living inside the product.' Scoping framing: 'Tell us more about the workflow you're trying to connect. Let's make sure it's the right fit before we scope anything.' |
| c12 | PASS: Output's timeline has milestones — Week 1: discovery call to understand the integration use case; Week 2-3: technical scoping with their IT; Week 4: API tier trial with their stack; Month 2: production rollout; Month 3: review uplift in time savings | PASS | Execution Plan maps exactly: May 9 (discovery call), May 16 (technical readiness assessment = scoping), May 23 (API tier demo/sandbox = trial), June 19 (API integration kickoff = rollout), August 15 (post-expansion review with adoption metrics and value confirmation). |
| c13 | PASS: Output references the demonstrated 40% time-savings as the 'we're ready for more' signal — connecting the QBR-proven value to the expansion ask rather than treating expansion as new | PASS | Approach section directly connects: 'Meridian has already proven 40% time savings at the current tier. The API integration tier removes the manual handoff step.' Expansion Signals: 'Customer is in a value-confirmed, receptive state.' Execution Plan Step 1 builds the value narrative from QBR outcomes. |
| c14 | PASS: Output identifies adoption risks — API tier requires technical resourcing on their side; if they don't have engineering capacity, the tier is bought but underused; recommends gating the upsell on confirming their technical readiness | PASS | Risks table: 'Engineering capacity for API integration — API tier only delivers value if the customer can build and maintain integrations. Legal tech firms often have limited in-house engineering. Gating action: Confirm internal engineering resource or SI partner before proposing the tier. If capacity is absent, scope an implementation support package.' |

### Notes

The output is a comprehensive, high-quality expansion plan that satisfies every criterion fully. The health gate is explicit and structured with numeric thresholds. All four readiness signals are cited. Revenue modelling shows clear arithmetic with stated assumptions and two API-tier pricing scenarios. The timeline is concrete with dated milestones spanning May through August 2026 that map cleanly to the discovery→scoping→trial→rollout→review arc. The enablement framing is sustained throughout — the trigger is positioned as a scoping conversation not a pitch, and the approach section explicitly connects the productivity gain to workflow embedding. Risk identification is thorough with gating actions for each risk. The only ceiling cap is c6 (PARTIAL by design), which the output fully earned at 0.5. No gaps or weaknesses detected.
