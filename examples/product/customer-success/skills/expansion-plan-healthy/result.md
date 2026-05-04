# Expansion Plan Healthy

Scenario: A customer success manager requests an expansion plan for a high-performing account. The account has strong utilisation, positive QBR history, and the customer has proactively asked about a higher tier. The skill should pass the health gate and produce a real expansion plan.

## Prompt

> /customer-success:expansion-plan Meridian Legal is at $180k ARR, 92% seat utilisation (115/125 seats), health score 85, just completed their third QBR showing 40% time savings. They've been asking about our API integration tier.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll run a formal expansion plan for Meridian Legal. Let me work through the process systematically.

---

# Expansion Plan: Meridian Legal

## Health Check
- **Seat utilisation:** 115 active / 125 licensed = **92%** ✓
- **Health score:** **85** (Strong) ✓
- **Churn signals:** None identified; customer is proactive and engaged
- **Goals achieved:** Third QBR showing **40% time savings** — clear value delivery ✓
- **Relationship:** Sponsor is engaged; customer initiating feature requests (organic signal) ✓
- **Clear to expand:** **YES** — account is healthy and showing strong expansion readiness

---

## Expansion Signals

| Signal | Evidence | Strength |
|---|---|---|
| Requesting higher-tier features | Customer explicitly asking about API integration tier | **Strong** |
| High sustained utilisation | 92% seat utilisation for extended period (implied by 3 successful QBRs) | **Strong** |
| Demonstrated value & engagement | 40% time savings achieved in third QBR; proactive engagement | **Strong** |
| Organic growth signal | Customer identifying integration need themselves, not prompted by sales | **Strong** |

**Readiness assessment:** All quantified thresholds met. Customer is ready for expansion conversation.

---

## Opportunity

| Metric | Value |
|---|---|
| **Current ARR** | $180,000 |
| **Current per-seat cost** | $1,440/seat/year (derived: $180k ÷ 125 seats) |
| **Expansion type** | **Tier upgrade** (API integration requires higher-tier capabilities) |
| **Expansion ARR (baseline scenario)** | $63,000 (35% premium for API-enabled tier) |
| **Expansion ARR (upside scenario)** | $77,400 (add 10 seats + tier upgrade) |
| **Post-expansion ARR (baseline)** | $243,000 (+35% NRR) |
| **Post-expansion ARR (upside)** | $257,400 (+43% NRR) |
| **Confidence** | **High** — customer is requesting the tier explicitly; no discovery needed on their intent |

**Pricing assumptions:**
- Baseline: shift from current tier to API-enabled tier at ~35% ARR premium ($63k expansion)
- Upside: fill 10 remaining unlicensed seats ($14.4k) + upgrade tier ($63k) = $77.4k expansion
- Both scenarios assume per-seat pricing model holds through tier change

**Adoption scenarios:**
- **Conservative (60% adoption):** API capabilities used by subset of org; customer sees 50% of projected integration ROI within 6 months
- **Full adoption (100%):** API fully integrated into their workflows; customer achieves stated automation goals and plans multi-year roadmap extensions

---

## Expansion Framing

**Current narrative (customer perspective):**
"We've saved 40% of time on [core workflow]. But we're still doing manual handoffs to our other systems — we'd love to automate that too."

**Enablement framing (CSM/sales perspective):**
"You've already validated significant time savings with the core product — 40% is substantial. The API integration tier removes the manual handoffs you mentioned, letting your team focus on higher-value work. Let's extend that ROI to the rest of your workflow."

**Why this works:** Connects their proven success to the next logical step. Positions API as scaling what's already working, not as a sales add-on.

---

## Timing Strategy

| Trigger | Why now | Action |
|---|---|---|
| **Post-QBR momentum** | Third QBR just completed; customer is energised by results; natural moment to discuss "what's next" | Use QBR debrief call (this week) as entry point for expansion conversation |
| **Their planning cycle** | Assume they're in mid-year planning (May); budget allocation for H2 is happening now | Position API tier as part of their H2 automation roadmap |
| **Before renewal** | If renewal is coming up (check contract), API tier conversation before renewal locks in higher ARR earlier | Confirm renewal timing; front-load conversation if renewal is Q3–Q4 |

**Avoid:** mid-integration crisis, support escalation, or when their champion is distracted by other initiatives.

---

## Risks & Gating Actions

| Risk | Why it applies to Meridian | Gating action |
|---|---|---|
| **Technical readiness** | API integration requires engineering capacity or third-party integration work. If they lack capacity, tier becomes shelfware. | Confirm in discovery call that they have dev resources OR are willing to engage a systems integrator. Don't proceed without this. |
| **Feature scope creep** | "API integration" is broad. Different customers need different endpoints. Undefined scope = poor implementation experience. | Before proposal: define the 3–5 specific workflows they want to automate. Use those to scope the API deliverable. |
| **Onboarding burden** | API tiers require more education (docs, SDKs, support). Poor onboarding = adoption failure even if tier is purchased. | Plan a structured onboarding program: kickoff → implementation → validation → go-live. Assign CSM + Product Engineer as pair. |
| **Adoption risk / ROI realisation** | Customer bought the tier but integration stalls internally. They stop using it. | Establish success metrics upfront: "by Day 60, these 5 workflows are automated via API." Schedule 30-day and 60-day review checkpoints. |
| **Price sensitivity** | At 92% utilisation, they're getting strong per-user ROI from current tier. A 35% jump might not feel proportional if they can't see exactly where the cost goes. | In proposal, itemise what the tier unlocks: API calls per month, integration support, SLA, etc. Connect cost to tangible benefits. |

---

## Execution Plan

| Phase | Action | Owner | Timeline |
|---|---|---|---|
| **1. Readiness confirmation** | Confirm renewal timing, identify technical owner, validate integration needs | CSM | This week (post-QBR) |
| **2. Discovery** | Call with customer: "What workflows would you automate if you could integrate with your other tools?" Identify top 3–5 integration scenarios. | CSM | Week 2 |
| **3. Scoping proposal** | Internal: scope the API deliverables to match their top use cases. Prepare pricing for Scenario A (tier upgrade) and Scenario B (upsell add-on). | CSM + Product Lead | Week 2–3 |
| **4. Proposal & demo** | Present expansion proposal in customer call. Show working API example matching one of their workflows. | CSM + Product | Week 3–4 |
| **5. Commercial close** | Negotiate contract terms. Confirm implementation timeline (typically 4–8 weeks for API integration). | CSM + Sales | Week 4–5 |
| **6. Implementation kickoff** | Assign CSM + Product Engineer pair. Agree on go-live date and success metrics. | CSM + Product | Week 6 |
| **7. Post-launch review** | 30-day check-in: are integrations working? 60-day review: adoption metrics vs. baseline. | CSM | Week 10 & 14 |

**Milestones at customer's pace:**
- **Exploration** (weeks 1–2): What do you want to automate?
- **Design** (weeks 3–4): Here's how the API solves it
- **Commitment** (week 5): Contract signed
- **Build** (weeks 6–10): Implementation and testing
- **Launch** (week 11): Go-live
- **Realise** (weeks 12+): Monitor adoption and value

---

## Success Criteria

| Criteria | Measurement | Target |
|---|---|---|
| **API adoption** | API endpoints being called; workflows automated via integration | >50% of defined use cases live and callable within 60 days post-launch |
| **Health maintenance** | Health score stable or improved post-expansion | Score ≥ 85 (current level) at 90-day review |
| **Value realisation** | Customer confirms automation working and delivering expected time savings | "The API integration reduced [manual workflow] by X%" (quantified by customer) at 60-day review |
| **Relationship strength** | Expansion felt enabling, not transactional; champion remains engaged | NPS maintained or improved; customer initiates next expansion conversation within 12 months |
| **Commercial performance** | Churn risk does not increase; customer renews at expanded tier | Renewal > $243k ARR at next contract cycle |

---

## Next Steps

1. **This week:** CSM reaches out post-QBR to explore their integration roadmap — frame as "what comes next after your time savings?"
2. **Week 2:** Conduct technical discovery to map their top 3–5 integration scenarios
3. **Week 3:** Present proposal (tier upgrade + implementation plan) with working demo
4. **Week 4–5:** Close commercial terms and schedule implementation kickoff

**Success signal:** Customer sees API tier as the logical next step in their automation journey, not as a sales push. The 40% time savings they've already achieved gives confidence that the next tier will deliver.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 13.5/13.5 (100%) |
| Evaluated | 2026-05-04 |
| Target duration | 41968 ms |
| Target cost | $0.0556 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | PASS: Health prerequisite check passes and expansion planning proceeds | PASS | The output has an explicit 'Health Check' section with five bullet points verifying seat utilisation (92% ✓), health score 85 ✓, no churn signals, QBR goals achieved ✓, and relationship quality ✓, concluding 'Clear to expand: YES' before proceeding to the full plan. |
| c2 | PASS: Expansion is framed as customer enablement, not a sales motion | PASS | The 'Expansion Framing' section explicitly states 'Positions API as scaling what's already working, not as a sales add-on.' The enablement framing quotes the customer-facing narrative as 'removing manual handoffs' and extending proven ROI, not growing account revenue. |
| c3 | PASS: The specific signal (customer asking about API tier) is used as the expansion anchor | PASS | The Expansion Signals table lists 'Customer explicitly asking about API integration tier' as the first and 'Strong' signal. The Opportunity section sets expansion type as 'Tier upgrade (API integration requires higher-tier capabilities)' and the entire plan is anchored to the API tier, with no pivot to bundles or other products. |
| c4 | PASS: Revenue impact is estimated with assumptions stated | PASS | The Opportunity table derives current per-seat cost ($1,440/seat/year from $180k ÷ 125 seats), calculates baseline expansion at 35% ARR premium ($63k) and upside including 10 additional seats ($77.4k), with post-expansion ARR of $243k–$257.4k. Pricing assumptions are stated explicitly in a separate 'Pricing assumptions' subsection. |
| c5 | PASS: A timeline with milestones is produced, not just 'upsell them' | PASS | The Execution Plan table has 7 named phases with owners and timelines (this week, Week 2, Week 2–3, Week 3–4, Week 4–5, Week 6, Week 10 & 14). A second 'Milestones at customer's pace' breakdown maps phases from Exploration through Realise with week numbers. |
| c6 | PARTIAL: Risk factors for the expansion are identified (e.g., adoption risk on a new tier) | PARTIAL | A 'Risks & Gating Actions' table identifies five risks with gating actions: Technical readiness, Feature scope creep, Onboarding burden, Adoption risk/ROI realisation, and Price sensitivity. The content exceeds the criterion's example but ceiling is PARTIAL. |
| c7 | PASS: The plan references the customer's demonstrated value (40% time savings) as proof of readiness | PASS | 40% time savings appears in the Health Check ('Third QBR showing 40% time savings — clear value delivery ✓'), Expansion Signals table, Expansion Framing ('40% is substantial'), Timing Strategy ('customer is energised by results'), and Next Steps ('frame as what comes next after your time savings?'). |
| c8 | PASS: Output's health prerequisite check passes explicitly — citing the four positive signals (92% utilisation, health score 85, 3 successful QBRs, customer-initiated tier inquiry) — and proceeds to plan | PASS | The Health Check section explicitly cites all four signals: 92% seat utilisation ✓, health score 85 ✓, 'Third QBR showing 40% time savings' ✓, and 'customer initiating feature requests (organic signal) ✓'. Concludes 'Clear to expand: YES' before proceeding. |
| c9 | PASS: Output uses the customer's specific request (asking about API integration tier) as the expansion anchor — meeting them where they are, NOT pivoting to a different tier or bundle | PASS | The Opportunity section labels expansion type as 'Tier upgrade (API integration requires higher-tier capabilities)' and every section — signals, framing, timeline, risks — is scoped to the API integration tier. No alternative tier or bundle is proposed. |
| c10 | PASS: Output's revenue impact estimate is shown with assumptions — e.g. "API tier adds $X/seat or $Y flat; 115 active seats currently; potential ARR uplift $Z assuming 100% adoption, $Z/2 assuming 50%" — with the math and the assumption stated | PASS | Per-seat math shown ($180k ÷ 125 seats = $1,440/seat/year). Baseline uplift ($63k = 35% premium) and upside ($77.4k = 10 seats × $1,440 + $63k) calculated with formulas stated. Adoption scenarios explicitly modelled at 60% (conservative) and 100% (full adoption) with projected ROI outcomes described. |
| c11 | PASS: Output's enablement-not-sales framing is visible — the recommendation discusses what API integration would unlock for Meridian Legal (e.g. integrating with their case management system, automating client intake), NOT "let's grow account revenue" | PASS | Expansion Framing customer narrative: 'we're still doing manual handoffs to our other systems — we'd love to automate that too.' CSM framing: 'The API integration tier removes the manual handoffs...letting your team focus on higher-value work.' Success Criteria includes NPS and 'expansion felt enabling, not transactional.' No revenue-growth language. |
| c12 | PASS: Output's timeline has milestones — Week 1: discovery call to understand the integration use case; Week 2-3: technical scoping with their IT; Week 4: API tier trial with their stack; Month 2: production rollout; Month 3: review uplift in time savings | PASS | Execution Plan phases match the criterion's milestone pattern: Phase 1 (this week) = readiness/context, Phase 2 (Week 2) = discovery call for integration use cases, Phase 3 (Weeks 2–3) = scoping proposal with internal tech team, Phase 4 (Weeks 3–4) = proposal with working demo, Phase 7 (Weeks 10 & 14) = post-launch adoption reviews including value realisation check. |
| c13 | PASS: Output references the demonstrated 40% time-savings as the "we're ready for more" signal — connecting the QBR-proven value to the expansion ask rather than treating expansion as new | PASS | Enablement framing: 'You've already validated significant time savings with the core product — 40% is substantial. The API integration tier removes the manual handoffs...Let's extend that ROI to the rest of your workflow.' Next Steps: 'frame as what comes next after your time savings?' The expansion is explicitly built on proven value, not treated as a fresh ask. |
| c14 | PASS: Output identifies adoption risks — API tier requires technical resourcing on their side; if they don't have engineering capacity, the tier is bought but underused; recommends gating the upsell on confirming their technical readiness | PASS | Risks table: 'Technical readiness: API integration requires engineering capacity or third-party integration work. If they lack capacity, tier becomes shelfware. → Confirm in discovery call that they have dev resources OR are willing to engage a systems integrator. Don't proceed without this.' Adoption risk row also covers stalled implementation scenario. |

### Notes

The captured output is a comprehensive, well-structured expansion plan that satisfies every criterion fully. The health gate is explicit with all four required signals called out individually. Revenue math is shown with derivations and dual adoption scenarios. The framing consistently positions the API tier as enabling the customer's own stated goal (removing manual handoffs) rather than growing ARR. The 40% time savings is used as a recurring 'proof of readiness' thread woven through signals, framing, timing strategy, and next steps. The risks section is thorough — five risks with specific gating actions, including the technically-critical 'don't proceed without confirming dev capacity' gate. The timeline is detailed across seven named phases. The only ceiling-capped criterion (c6) was scored PARTIAL as required regardless of output quality. No gaps or omissions were identified across all 14 criteria.
