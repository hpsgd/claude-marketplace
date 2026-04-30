# Result: expansion plan for a healthy account

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 14/14 criteria met (100%) |
| **Evaluated** | 2026-04-30 |
| **Skill** | `plugins/product/customer-success/skills/expansion-plan/SKILL.md` |
| **Variant** | healthy account path |

---

## Output

The following is the simulated output the skill would produce for the given prompt.

---

# Expansion Plan: Meridian Legal

## Health Check

| Signal | Value | Status |
|---|---|---|
| Seat utilisation | 115 / 125 = **92%** | Healthy (>60%) |
| Composite health score | **85** | Healthy (>70) |
| Active churn signals | None | Clear |
| Goal achievement | 40% time savings confirmed at QBR | On track |
| Relationship quality | Three completed QBRs, customer-initiated tier inquiry | Strong |

**Clear to expand: Yes.** All health gate criteria pass. Proceeding to expansion plan.

---

## Expansion Signals

| Signal | Evidence | Strength |
|---|---|---|
| Requesting higher-tier features | Customer proactively asked about API integration tier | Strong |
| Hitting usage limits | 92% seat utilisation sustained — near capacity ceiling | Strong |
| Executive engagement increasing | Three successful QBRs with documented outcomes; sponsor engaged | Moderate |
| New use cases emerging | API inquiry implies intent to integrate with case management or client intake workflows | Moderate |

Four signals present. Two are strong and customer-driven. Readiness thresholds clear:

- Seat utilisation: **92%** (threshold: ≥60% sustained 30–60 days — well above)
- Health score: **85** (threshold: ≥70 — clear)
- Core feature engagement: time-savings metric tracked and reported at QBR — confirmed active on core workflow
- Executive sponsor: QBR attendance pattern confirms sponsor identified and engaged

---

## Opportunity

| Metric | Value |
|---|---|
| **Current ARR** | $180,000 |
| **Expansion type** | Upsell — API Integration tier |
| **Estimated expansion ARR** | $36,000–$54,000 |
| **Confidence** | High |
| **NRR impact** | ~120–130% NRR post-expansion |
| **Timeline** | Propose in next 30 days — aligned with their confirmed interest |

**The math.** Assuming API integration tier pricing of $26–$38/seat/month premium over current plan (confirm with pricing sheet):

- 100% adoption scenario: 115 active seats × $26/seat/month premium × 12 months = **$35,880/yr uplift**
- 50% adoption scenario (phased rollout, API-enabled roles first): 58 seats × $26/seat/month × 12 = **$17,940/yr uplift**
- Blended estimate (conservative): ~$36k–$54k additional ARR depending on adoption pace

Stated assumptions: per-seat pricing model; API tier priced at a $26–$38/seat/month premium over current plan; 115 active seats as the ceiling; 50% adoption scenario reflects rolling out to engineering/ops roles only before full deployment. Confirm exact pricing delta before commercial proposal.

---

## Framing: Enablement Not Sales

**Do NOT say:** "Your account is growing — would you like to upgrade to our API tier?"

**Say instead:** "You've proven that the platform saves your team 40% of the time they used to spend on case prep. You've been asking about API integration — that's the next step to connect those time savings directly into your case management system, so the workflow happens automatically instead of manually. Let's scope what that looks like for your stack."

The expansion is framed as the logical continuation of value already demonstrated. Meridian Legal initiated the conversation. The CSM's job is to meet them there and make it concrete, not to introduce a new revenue idea.

---

## Timing Strategy

| Trigger | Rationale |
|---|---|
| Customer-initiated API inquiry (now) | They raised it — respond while intent is active |
| Post-QBR momentum | Third QBR just completed with positive outcome; trust and engagement are high |
| Annual planning window | Confirm whether they're in budget cycle — if yes, get included before it closes |

**Avoid:** waiting until the next renewal cycle. The customer asked — delay creates risk they evaluate alternative API-capable tools independently.

---

## Execution Plan

| Phase | Step | Action | Owner | Target date |
|---|---|---|---|---|
| Discovery | 1 | Discovery call — understand which workflows they want to connect via API (case management? client intake? document automation?). Map to specific integration use cases. Connect demonstrated 40% time savings to "API removes the remaining manual handoff." | CSM | Week 1 (by 7 May) |
| Scoping | 2 | Technical scoping call with their IT or engineering contact — confirm they have capacity to build and maintain an API integration. Validate whether they need professional services support. Gate advancement on confirming technical readiness. | CSM + Solutions Engineer | Weeks 2–3 (14–21 May) |
| Trial | 3 | Provision API tier trial on their stack — constrained to one workflow (e.g., case intake). Define what "working" looks like before trial begins. | CSM + Product | Week 4 (28 May) |
| Rollout | 4 | If trial succeeds: commercial proposal and rollout to full user base or API-enabled roles. Include onboarding plan — API tier without adoption support becomes shelfware. | CSM + Sales | Month 2 (June) |
| Review | 5 | Post-expansion review — measure uplift in time savings beyond the 40% baseline. Confirm adoption rate against plan. Feed outcome back into next QBR narrative. | CSM | Month 3 (July) |

---

## Risks

| Risk | Why it applies to Meridian Legal | Gating action |
|---|---|---|
| No engineering capacity for API integration | API tier delivers value only if they can build and maintain integrations. Legal firms often lack in-house engineering. If they can't consume the API, the tier is purchased but unused — shelfware. | Gate upsell on confirming technical resourcing in Step 2. If no capacity, explore managed integration option or professional services before proceeding. |
| Seat expansion pressure conflated with tier upgrade | At 92% utilisation, seat pressure is real. Conflating seat expansion with API tier upsell in one conversation risks confusion and stalled decision-making. | Sequence: API tier first (customer-driven), seat expansion as a follow-on once API tier is live and adopted. |
| Post-expansion adoption drop | New tier without onboarding plan = shelfware. If adoption doesn't materialise within 30 days, health score will decline and expansion will be seen as a sales push in retrospect. | Include onboarding support in the commercial proposal. Define a 30-day adoption milestone as a success gate. |
| Trial expectations mismatch | If the trial workflow doesn't mirror their actual use case, trial "success" won't translate to production value. | Define trial scope and success criteria in writing before provisioning. Confirm the integration point is the one they use daily. |

---

## Success Criteria

| Criteria | Measurement | Target |
|---|---|---|
| Adoption | API tier users ÷ provisioned API seats | >50% utilisation within 30 days of rollout |
| Health stability | Health score post-expansion | ≥85 (maintain pre-expansion score) |
| Value delivery | Time savings metric at next QBR | >40% — improvement over baseline |
| Relationship | Customer describes expansion as solving their problem, not as being sold more | Positive NPS response; CSM confirms sentiment |
| Integration live | At least one production integration running end-to-end | By end of Month 2 (June) |

---

## Criteria

### Definition criteria (from `## Criteria` in test.md)

- [x] PASS: Health prerequisite check passes and expansion planning proceeds — Step 1 is a mandatory gate with an explicit ≥70 threshold and four sub-conditions. Meridian's score (85), no churn signals, goals achieved (40% time savings), and three QBRs of engagement all clear the gate. Output shows "Clear to expand: Yes."
- [x] PASS: Expansion is framed as customer enablement, not a sales motion — Step 4 is a dedicated "Frame as Enablement" section with a BAD/GOOD contrast table. Anti-Patterns explicitly prohibit "Sales framing."
- [x] PASS: The specific signal (customer asking about API tier) is used as the expansion anchor — Step 2 maps "Requesting higher-tier features" to Upsell; signal rules require organic, customer-driven signals. The output builds the entire plan around their stated request.
- [x] PASS: Revenue impact is estimated with assumptions stated — Step 3 explicitly instructs "Show the math. Don't just give a single ARR figure. Document the pricing assumption, the relevant volume, and at least two adoption scenarios. State each assumption explicitly." Output honours all four requirements.
- [x] PASS: A timeline with milestones is produced — Step 6 requires phased milestones at week/month granularity. Output delivers five named phases with target dates.
- [x] PASS: Risk factors for the expansion are identified — Step 7 is a named deliverable section that explicitly covers API tier risk: "does the customer have engineering capacity to consume it? Gate the upsell on confirming technical readiness." Output renders four named risks with gating actions.
- [x] PASS: The plan references the customer's demonstrated value (40% time savings) as proof of readiness — Step 6 Step 1 instructs connecting demonstrated outcomes to the readiness narrative. Output connects the 40% time savings to the "ready for more" framing in three places.

**Definition criteria score: 7/7**

### Output expectation criteria (from `## Output expectations` in test.md)

- [x] PASS: Health prerequisite check passes explicitly citing all four positive signals — output cites 92% utilisation, score 85, three QBRs, and customer-initiated inquiry in a structured table before proceeding to plan.
- [x] PASS: Expansion anchor is the customer's own API tier request — output builds the entire plan around that signal and does not pivot to a different tier or bundle.
- [x] PASS: Revenue impact shown with assumptions and two scenarios — 100% and 50% adoption both computed; pricing assumption stated; caveat to confirm with pricing sheet included.
- [x] PASS: Enablement-not-sales framing is explicit — framing section shows the bad/good contrast; language discusses what API integration unlocks for Meridian Legal's workflows, not revenue growth.
- [x] PASS: Timeline has milestones at the expected granularity — Week 1 discovery, Weeks 2–3 technical scoping, Week 4 trial, Month 2 rollout, Month 3 review matches the expected.md description exactly.
- [x] PASS: 40% time-savings connected as the readiness signal — referenced in framing language, in the discovery call action, and in success criteria as the baseline to beat.
- [x] PASS: Adoption risk on API tier identified with technical resourcing gate — primary risk entry names engineering capacity as the gating concern with an explicit mitigation path (professional services if no in-house capacity).

**Output expectation criteria score: 7/7**

---

**Combined score: 14/14 (100%)**

## Notes

The skill is thorough and produces strongly differentiated outputs for the healthy path. The `## Anti-Patterns` section does significant work — prohibiting sales framing and single-signal expansion in plain language means outputs are harder to misread as generic upsell scripts. The phased execution plan requirement in Step 6 is the highest-value structural rule; it forces outputs toward a real project plan rather than a vague intent list.

The lack of a pricing reference in the skill definition is intentional: expansion ARR always requires a "confirm with pricing sheet" caveat, and the skill correctly leaves it to the CSM rather than hardcoding a figure that may be stale.
