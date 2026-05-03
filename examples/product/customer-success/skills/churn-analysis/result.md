# Churn Analysis

Scenario: Testing whether the churn-analysis skill requires timeline reconstruction, root cause diagnosis, churn probability scoring, and an intervention design — not just a list of churn reasons.

## Prompt

> /customer-success:churn-analysis for Bradwick & Sons who just submitted a cancellation request. They were a $68k ARR customer, used us for 14 months, and cited "not getting enough value" as their reason for leaving.
> 
> A few specifics for the response:
> 
> - **Root cause framework** — explicitly weigh ALL five categories (product fit, onboarding failure, relationship breakdown / champion change, competitive displacement, external factors) before picking the most-evidence-backed one. Show which were dismissed and why.
> - **Broader-pattern check** — a dedicated section asking "is this part of a trend?". Compare to other recent churned accounts at similar tenure (~14 months) and similar ARR band; recommend a cohort review (e.g. "third 14-month customer to cite value in the past quarter — investigate year-2 value-articulation gap").
> - **Feedback loop** — list specific changes to feed back into onboarding, QBR cadence, and product positioning so the next Bradwick doesn't follow the same path.
> - **Post-cancellation handling** — cover all three: exit interview to capture honest feedback, references / referrals if relationship was healthy, win-back triggers and timing for the future.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll work through this churn analysis systematically using the root cause framework, pattern check, and feedback loop you've requested. Note that I'm working from the limited info provided — the actual analysis will need CRM/usage data you have on file.

---

## Churn Analysis: Bradwick & Sons

### Risk Summary
- **Churn probability:** High (likely already decided — cancellation submitted, not churn risk)
- **Risk score:** 15+ (already churned, analysis is post-mortem + prevention)
- **ARR at risk:** $68,000 (already lost unless win-back succeeds)
- **Time to action:** Within 48 hours for exit interview; win-back decisions within 1 week

---

### Step 1: Active Signals (Known)

You've stated one explicit signal; I'm inferring the rest from the pattern:

| Signal category | Indicators | Severity | Evidence |
|---|---|---|---|
| **Value gap** | Stated as cancellation reason | Critical | "Not getting enough value" (direct quote) |
| **Engagement decline** (assumed) | Likely went quiet before submitting cancellation | High | Timeline TBD — when did engagement drop? |
| **Usage pattern** (unknown) | Need to check: feature adoption, session frequency, key workflows abandoned | High | Requires usage dashboard review |
| **Relationship status** (unknown) | Was there an engaged champion? Who submitted the cancellation? | High | Requires stakeholder review |
| **Competitive signal** (unknown) | Was a competitor evaluation underway? | Medium | Requires sales/support ticket review |

**Critical gaps to fill immediately:**
- Usage dashboard: DAU, key feature adoption, session duration trends over past 6 months
- Communication log: last interaction date, tone, responsiveness to outreach
- QBR history: were quarterly reviews happening? ROI articulated?
- Support tickets: volume, sentiment, unresolved issues
- Stakeholder map: original champion still there? New decision-maker? Budget holder engaged?

---

### Step 2: Timeline Reconstruction (Hypothesis)

Without actual dates, here's the likely pattern for a 14-month $68k customer citing value issues. **You'll need to validate against actual data:**

| Period | Likely event | Signal | Notes |
|---|---|---|---|
| **Month 0–2 (Launch)** | Onboarding → go-live | Usage spike, high engagement | Typical honeymoon period |
| **Month 3–6 (Evaluation)** | Initial value realization | Engagement stable or declining? | Critical period — did they hit Time to First Value? |
| **Month 6–10 (Middle phase)** | Adoption plateau or decline | Usage trends flat → declining | No new workflow adoption; core goals not met |
| **Month 11–13 (Pre-churn)** | Engagement drops significantly | Silent deterioration | Fewer logins, no QBR scheduled or attended, ignored outreach |
| **Month 14 (Cancellation)** | Cancellation submitted | Decision already made | Not a sudden change — the decision was made weeks/months ago |

**Inflection point to identify:** When did engagement start declining? Was there a specific trigger (product change, team change, unresolved issue, feature request denied)?

---

### Step 3: Root Cause Diagnosis — Five-Category Framework

Let me weigh each explicitly with what we know + what we need to verify:

#### **1. Product-Market Fit**
- **Hypothesis:** LIKELY PRIMARY — "not getting enough value" suggests the product isn't solving their core problem
- **Evidence needed:**
  - Did they adopt core features or use workarounds?
  - Were their use cases edge cases or mainstream?
  - Did they request features for "basic functionality" (red flag)?
- **Verdict:** Cannot rule out without usage data. Check feature adoption dashboard.

#### **2. Onboarding Failure**
- **Hypothesis:** POSSIBLE — "not getting enough value" after 14 months suggests value was never clearly articulated
- **Evidence needed:**
  - How long was onboarding? Did they hit TFFV (Time to First Value) in week 1–2?
  - Were success metrics defined upfront?
  - Was there a dedicated onboarding plan or did they self-serve?
- **Verdict:** At 14 months, onboarding alone isn't the issue — but failed onboarding in months 1–2 cascades. Check onboarding records and initial project plan.

#### **3. Value Delivery Gap (Year-2 Problem)**
- **Hypothesis:** HIGHLY LIKELY — "not getting enough value" at 14 months is a classic Year-2 pattern
- **Evidence needed:**
  - Was ROI measured and communicated back to them?
  - Did the business case from Month 0 match Month 14 reality?
  - Were QBRs happening? Was value demonstrated with data?
- **Verdict:** This is the highest-confidence diagnosis. 14-month tenure suggests they got SOME value initially (otherwise they'd churn at month 3–4). Year-2 churn almost always points to: they got initial value but are now stagnant AND the value story wasn't reinforced. **This is a value-articulation and QBR cadence failure.**

#### **4. Relationship Breakdown / Champion Change**
- **Hypothesis:** CONTRIBUTING but likely secondary
- **Evidence needed:**
  - Who was the original champion? Did they leave or get sidelined?
  - Is the current decision-maker the same person who bought?
  - How responsive have they been to outreach in the past 3 months?
- **Verdict:** Check stakeholder history. If champion left AND value wasn't reinforced elsewhere, they become vulnerable. If champion is still there and engaged, this isn't primary.

#### **5. External Factors / Competitive Displacement**
- **Hypothesis:** UNLIKELY as primary cause, but check
- **Evidence needed:**
  - Did budget get cut? Org reorg? Strategy shift?
  - Evidence of competitor evaluation?
  - Price complaint in the cancellation note?
- **Verdict:** Would expect different language ("budget constraints", "switching to X") if this were primary. Low probability.

**Root Cause Ranking (high to low confidence):**

1. **Value Delivery Gap / Year-2 Stagnation** (Primary) — "not getting enough value" + 14-month tenure is the classic Year-2 pattern. Value was demonstrated early, but QBRs and value reinforcement fell off.
2. **Onboarding Cascades** (Secondary) — onboarding failure in months 1–2 cascades to Year-2 if it was never fixed
3. **Relationship Loss** (Contributing) — if champion left + value wasn't articulated elsewhere, they become vulnerable
4. **Product-Market Fit** (Lower probability) — true PMF misses usually show up at month 3–6, not month 14
5. **Competitive Pressure** (Unlikely primary) — possible but not indicated by language

---

### Step 4: Broader-Pattern Check — Cohort Analysis

**This is critical.** Before treating this as a one-off, flag the pattern:

**Questions to answer:**
- How many other customers churned at ~12–16 month tenure in the past 12 months?
- How many cited "value" / "not meeting ROI" / "underutilization"?
- What's the churn rate by tenure band? (Months 3–6, 6–12, 12–18, 18+)

**Likely finding (hypothesis):** You probably have a **Year-2 Value-Articulation Gap**. Customers get initial value, then plateau, and if QBRs aren't reinforcing that value or expanding the use case, they churn in month 12–16. This is a systematic problem, not a Bradwick-specific one.

**Recommended action:** Flag for CSM leadership review:
- Pull all churn reasons from the past 18 months
- Segment by tenure band
- If "value", "ROI", "utilization" appear 3+ times in the 12–18 month cohort → you have a systemic Year-2 onboarding/QBR/value-articulation problem
- Trigger a formal cohort review (recommend: investigate Year-2 QBR effectiveness and value-story consistency)

---

### Step 5: Intervention Plan (Post-Churn Win-Back)

Cancellation already submitted, so this is **exit → learn → win-back** sequence:

#### **Phase 1: Exit Interview (48 hours)**
| Action | Owner | Timeline | Success criteria |
|---|---|---|---|
| Schedule exit interview with Bradwick decision-maker | CSM + Sales | Within 24h | Call booked, conducted, documented |
| Ask specifically about Year-2 experience | CSM | Call | Understand: When did value feeling decline? What would have helped? |
| Ask about competitive evaluation | Sales | Call | Did they look at alternatives? Which? Why? |
| Offer references if relationship was healthy | Sales | Call | If they had positive experience and would recommend, capture as reference |
| Document honest feedback | CSM | Within 48h of call | Debrief captured, shared with product/onboarding teams |

**Key questions for the call:**
- "Help me understand — when did you first feel like value was dropping?"
- "What would have changed your mind in month 12–14?"
- "Did we miss something about how you were trying to use the product?"
- "Would you be open to revisiting this in 6 months if we made [specific change]?"

#### **Phase 2: Feedback Loop — Prevent Next Bradwick**

Feed this back into three areas:

**A. Onboarding & Success**
- Review Bradwick's onboarding record: did they hit TFFV? Were success metrics defined?
- **Change:** For all $50k+ ARR customers, require signed success plan at Month 1 (goals, metrics, timeline to value)
- **Change:** Schedule mandatory QBR at Month 3 (not Month 6) to validate early value and adjust if off-track

**B. QBR Cadence & Value Articulation**
- Did Bradwick have QBRs? If yes, were they about ROI/value or just feature updates?
- **Change:** For customers in Year 2, QBRs must include: ROI measurement, goal progress, expansion opportunities. Not just "here's what we shipped"
- **Change:** At Month 10–12, proactive "Year-2 value check-in" to assess satisfaction BEFORE renewal

**C. Product Positioning**
- What was Bradwick trying to achieve? Did the product deliver that, or were they in an edge case?
- **Change:** Improve onboarding ICP targeting — make sure Year-2 patterns are captured in the success criteria for new signings

#### **Phase 3: Win-Back Triggers**

When would you re-engage Bradwick?

| Trigger | Timing | Approach |
|---|---|---|
| Product ships major feature addressing their original use case | 6–12 months | "We built X — want to see if it changes the math?" |
| You solve the Year-2 value-articulation gap (new QBR template, case studies) | 3–6 months | "We've changed how we work with customers in Year 2. Here's what's different." |
| Competitive contract expires or renewal comes | 12+ months | "Evaluating again? Let's talk about what's changed." |
| Budget recovers / org re-prioritizes | Unknown | Sales watches for signals; triggers outreach |

**Win-back probability:** Moderate. They left citing value, not relationship or price. If you genuinely fix value articulation, they might return. But timing matters — too soon (1–2 months) looks desperate; too late (18+ months) they've moved on.

---

### Step 6: Retention Economics (Learning)

| Metric | Value |
|---|---|
| **ARR lost (Bradwick)** | $68,000 |
| **Replacement cost** | $340,000–476,000 (5–7x retention cost) |
| **Prevention cost** (if systemic Year-2 problem) | Modest: better QBR template, CSM training, Month 10–12 check-in process |
| **ROI of fixing Year-2 gap** | High — prevents future Bradwick-pattern churn |

**Strategic question:** Is this a one-off or a cohort pattern? If it's a cohort, the $68k loss is actually a signal that you're losing $200k–400k annually to the same root cause across multiple customers. That shifts the priority urgently.

---

### Summary & Next Steps

**Diagnosis:** Bradwick is a **Year-2 value-articulation gap** churn. They got initial value (which is why they lasted 14 months), but Year-2 stagnation + lack of QBR/ROI reinforcement → churn.

**Immediate actions (this week):**
1. Exit interview — understand exactly when value feeling declined
2. Check cohort pattern — are there 2–3 other "value citation" churns at 12–18 month mark?
3. If systemic: escalate to CSM leadership for Year-2 QBR process redesign
4. Capture Bradwick as reference if relationship was solid

**Longer-term (next 60 days):**
- Update QBR template to require ROI measurement in Year 2
- Add Month 10–12 "value check-in" to CSM playbook
- Train onboarding team on Year-2 value-expansion conversation

**Win-back window:** 6–12 months, triggered by major feature launch or process improvement launch (e.g., "We've redesigned how we help customers realize Year-2 value").

---

Want me to help structure the exit interview questions, or dig into the cohort analysis once you pull churn data from your CRM?

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.5/16.5 (94%) |
| Evaluated | 2026-05-03 |
| Target duration | 44906 ms |
| Target cost | $0.0983 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires signal identification — cataloguing all available signals (usage data, support tickets, health scores, engagement) before forming hypotheses | PASS | Step 1 'Active Signals (Known)' contains a table cataloguing signal categories (value gap, engagement decline, usage pattern, relationship status, competitive signal) with severity/evidence columns, followed by a 'Critical gaps to fill immediately' list naming usage dashboard, communication log, QBR history, support tickets, and stakeholder map as missing data. |
| c2 | Skill requires timeline reconstruction — building a chronological view of the account relationship to identify when health started declining | PASS | Step 2 'Timeline Reconstruction (Hypothesis)' is a table spanning Month 0–2 through Month 14 with distinct phases, flagging Month 11–13 as 'silent deterioration' and Month 14 as decision already made. It explicitly asks 'When did engagement start declining?' and notes the inflection point needs identification. |
| c3 | Skill produces a root cause diagnosis — distinguishing between product fit, onboarding failure, relationship breakdown, competitive displacement, and external factors | PASS | Step 3 'Root Cause Diagnosis — Five-Category Framework' explicitly covers all five: Product-Market Fit, Onboarding Failure, Value Delivery Gap, Relationship Breakdown/Champion Change, and External Factors/Competitive Displacement. Each has hypothesis, evidence needed, and verdict. A ranked list concludes with Value Delivery Gap as primary cause. |
| c4 | Skill requires a churn probability score or risk classification, not just qualitative assessment | PASS | Risk Summary at the top shows 'Churn probability: High (likely already decided)' and 'Risk score: 15+ (already churned, analysis is post-mortem + prevention)' with 'ARR at risk: $68,000' and a time-to-action window — this is a quantified classification with reasoning. |
| c5 | Skill includes an intervention design — what could be done now to attempt recovery, if anything | PASS | Step 5 'Intervention Plan (Post-Churn Win-Back)' has three phases: Phase 1 (exit interview within 48 hours with a table of specific actions and success criteria), Phase 2 (feedback loop changes), and Phase 3 (win-back triggers with a timing table). |
| c6 | Skill requires retention economics — calculating the value of retaining vs losing this customer and comparing intervention cost | PASS | Step 6 'Retention Economics (Learning)' table shows ARR lost ($68,000), replacement cost ($340,000–476,000 at 5–7x), prevention cost described as 'Modest: better QBR template, CSM training', and ROI of fixing Year-2 gap as 'High'. Recommendation ties to the math: 'the $68k loss is actually a signal that you're losing $200k–400k annually.' |
| c7 | Skill feeds findings into a pattern or trend — is this churn part of a broader trend or an isolated incident — partial credit if this is mentioned but not required as a step | PARTIAL | Step 4 'Broader-Pattern Check — Cohort Analysis' is a dedicated section hypothesising a 'Year-2 Value-Articulation Gap' pattern and recommending pulling all churn reasons from the past 18 months, segmenting by tenure band, and triggering a formal cohort review if 'value/ROI/utilization' appear 3+ times in the 12–18 month band. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output is entirely a prose analysis response starting with 'I'll work through this churn analysis systematically…'. No YAML frontmatter with name, description, or argument-hint fields appears anywhere in the output. |
| c9 | Output's signal inventory enumerates what data exists for Bradwick & Sons — usage history, support tickets, health scores, QBR notes, last engagement points — and what data is MISSING (which is itself a signal) | PASS | Step 1 table labels signals as 'direct quote' (known), '(assumed)', and '(unknown)', with severity levels. The 'Critical gaps to fill immediately' list names five missing data sources: usage dashboard (DAU, feature adoption, session duration), communication log, QBR history, support tickets, and stakeholder map — explicitly framing absence as a signal. |
| c10 | Output's timeline reconstruction is chronological from contract start to cancellation — identifying when health started to decline (e.g. 'month 8 saw MAU drop 30%') rather than treating the 14-month span as a flat block | PASS | Step 2 table breaks the 14-month span into five distinct phases with assigned events and signals at each. Month 6–10 is flagged as 'adoption plateau or decline', Month 11–13 as 'silent deterioration: fewer logins, no QBR scheduled or attended, ignored outreach', distinguishing these from the earlier honeymoon phase. |
| c11 | Output's root cause diagnosis distinguishes between the categories — product fit, onboarding failure, relationship breakdown (champion change, exec turnover), competitive displacement, external factors — and picks the most-evidence-backed cause for Bradwick | PASS | Step 3 walks through all five categories individually with hypothesis, evidence needed, and verdict for each. Root Cause Ranking selects 'Value Delivery Gap / Year-2 Stagnation' as primary with explicit reasoning: '"not getting enough value" + 14-month tenure is the classic Year-2 pattern'. Product-Market Fit ranked 4th with reason it typically surfaces at month 3–6. |
| c12 | Output produces a churn probability score or risk classification — though they've already cancelled, the score retrospectively classifies whether this was preventable / inevitable / surprising — with reasoning | PASS | Risk Summary states 'Churn probability: High' and 'Risk score: 15+' with parenthetical reasoning. The output implicitly classifies the churn as preventable through QBR and Year-2 value-articulation improvements, stating 'Win-back probability: Moderate' — they left for value reasons, not relationship/price, suggesting if the root cause is fixed they may return. |
| c13 | Output's intervention design names what could be attempted now — last-call save offer, root-cause-of-pain conversation, pause-vs-cancel option — or explicitly states 'intervention will not change the outcome' with reasoning | PASS | Phase 1 of Step 5 designs the immediate intervention as an exit interview within 24–48 hours, with specific probing questions functioning as a root-cause-of-pain conversation: 'When did you first feel like value was dropping?', 'What would have changed your mind in month 12–14?', 'Would you be open to revisiting this in 6 months if we made [specific change]?' The output accepts the cancellation is final without explicitly stating it's irreversible. |
| c14 | Output's retention economics calculates the value of saving Bradwick ($68k ARR) vs the cost of intervention (CSM time, discount, custom work), with a recommendation tied to the math | PARTIAL | Step 6 quantifies ARR lost ($68,000) and replacement cost ($340,000–476,000), but intervention cost is described only qualitatively ('Modest: better QBR template, CSM training, Month 10-12 check-in process') without a dollar figure. The recommendation is tied to the math ('$200k–400k annually if systemic') but the cost-vs-benefit calculation for the specific Bradwick intervention (CSM hours, discount offered) is not explicitly completed. |
| c15 | Output addresses the cited reason 'not getting enough value' by digging deeper — value relative to what? Compared to expectations at sale? Compared to alternatives? — rather than accepting the surface answer | PASS | Step 3, Category 3 asks 'Was ROI measured and communicated back to them?', 'Did the business case from Month 0 match Month 14 reality?', and 'Were QBRs happening? Was value demonstrated with data?' Exit interview questions probe 'when did you first feel like value was dropping?' and 'what would have changed your mind?' — unpacking the value gap against original expectations rather than accepting the surface reason. |
| c16 | Output flags whether this churn fits a broader pattern — e.g. 'third 14-month customer to cite value in the past quarter, suggesting a year-2 value-articulation gap' — with a recommendation to investigate | PASS | Step 4 'Broader-Pattern Check — Cohort Analysis' states 'Likely finding (hypothesis): You probably have a Year-2 Value-Articulation Gap.' Recommended action: 'Pull all churn reasons from the past 18 months, segment by tenure band, if "value", "ROI", "utilization" appear 3+ times in the 12–18 month cohort → you have a systemic Year-2 onboarding/QBR/value-articulation problem. Trigger a formal cohort review.' |
| c17 | Output proposes specific learnings to feed back into onboarding, QBR cadence, or product positioning — what should change so the next Bradwick doesn't follow the same path | PARTIAL | Phase 2 'Feedback Loop — Prevent Next Bradwick' covers three areas with specific changes: A. Onboarding (require signed success plan at Month 1, mandatory QBR at Month 3); B. QBR Cadence (QBRs must include ROI measurement in Year 2, add Month 10–12 'value check-in'); C. Product Positioning (improve onboarding ICP targeting for Year-2 patterns). Detailed and actionable. |
| c18 | Output addresses post-cancellation handling — exit interview to capture honest feedback, references / referrals if relationship was healthy, win-back triggers for the future | PARTIAL | Phase 1 covers exit interview (scheduled within 24h, documented within 48h). Phase 1 table includes 'Offer references if relationship was healthy → capture as reference.' Phase 3 covers win-back triggers with a table listing three scenarios (major feature release, Year-2 process improvement, competitor contract expiry) with timing and approach. All three elements present. |

### Notes

The output is a thorough, well-structured churn analysis that covers nearly every required dimension. It excels at the root cause framework (all five categories explicitly weighed and ranked), timeline reconstruction (broken into five distinct phases), cohort pattern analysis (a dedicated Step 4), and feedback loops (three specific change areas). The one clear gap is c8: the captured output is a chat response with no YAML frontmatter — the skill definition metadata is absent from what was produced. c14 is scored PARTIAL because intervention cost is described qualitatively ('Modest') rather than computed alongside the $68k ARR figure. The post-cancellation section (c18) covers all three required elements (exit interview, references, win-back) though the referral angle is brief. Overall the analysis is detailed, specific, and actionable, achieving 93.9% of available points.
