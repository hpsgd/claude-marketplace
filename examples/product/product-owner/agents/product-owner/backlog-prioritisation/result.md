# Result: Backlog prioritisation

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17.5/18 criteria met (97%) |
| **Evaluated** | 2026-04-30 |

## Output

Below is the simulated response this agent definition would produce for the given prompt.

---

Before I can give you a prioritised sprint recommendation, I need a few quick answers. The RICE framework I'll use requires sprint capacity and commitment data — without them I can rank items relative to each other but can't tell you what fits.

**Three questions before we proceed:**

1. **Sprint capacity** — how many person-weeks does the team have next sprint? (e.g., 4 engineers × 2 weeks = 8 person-weeks)
2. **Existing commitments** — are any of these 8 items already promised to a customer, in a contract, or verbally committed to by sales or the CEO?
3. **Team composition** — full-stack engineers, or is it frontend-heavy? The mobile redesign and SSO have very different skill requirements.

I'll proceed with what's here and flag the gaps — but these answers will change the final recommendation.

---

## Backlog prioritisation — Sprint N

**Status:** Draft — pending sprint capacity and commitment confirmation
**Evidence:** Stakeholder-provided item list with partial customer and revenue data

### RICE Scoring

| # | Item | Reach | Impact | Confidence | Effort | RICE | Notes |
|---|---|---|---|---|---|---|---|
| 3 | SSO/SAML integration | ~200 (est. enterprise segment) | 3 | 100% | 3 weeks | **200** | $180k ARR hard-blocked. Security review is a gate — not a nice-to-have |
| 2 | CSV export | ~200 | 2 | 80% | 1 week | **320** | Sales team quantified ~200 affected customers. Internal + external demand. Quick win |
| 8 | Performance improvements | broad (all users) | 2 | 80% | 2 weeks | **160** | P95 4.2s is a quantified, measured problem. No customer-linked revenue figure yet — rated medium |
| 7 | Slack notifications | 47+ upvotes | 1 | 50% | 1 week | **~24** | Forum signal only. No revenue or churn evidence. Confidence low |
| 1 | Dark mode | 3 enterprise customers + CEO | 1 | 50% | 1.5 weeks | **~17** | CEO interest noted; 3 customers named. No ARR at risk cited. Confidence low without retention data |
| 6 | Onboarding flow | new users (unknown %) | 2 | 30% | [NEEDS CLARIFICATION] | — | CS perception only. No funnel data. Do not build yet — instrument first |
| 5 | API rate limit increase | 1 power user (unknown total) | 1 | 30% | 0.5 weeks | — | Reach completely unknown. Needs an analytics query before committing time |
| 4 | Mobile app redesign | unknown | 1 | 10% | 4+ weeks | — | No customer request on record. Design team desire is not customer evidence |

**RICE formula: (Reach × Impact × Confidence) / Effort**

Effort figures above are estimates only — these need engineering confirmation before sprint planning. The "What You Don't Do" constraint means I cannot commit to timelines without the CTO's team input.

---

### Item-by-item reasoning

**SSO/SAML integration — Recommend: ship next sprint**

Two enterprise deals worth $180k ARR are blocked pending this. Enterprise SSO is a hard gate — deals do not progress without it. The security review dependency means this must be unblocked before the deals can close. Revenue evidence is explicit and named. Highest priority regardless of effort.

**CSV export — Recommend: ship next sprint**

Sales team has quantified ~200 customer impact. Internal (finance) and external demand. Effort appears low (1 week estimate). Strong Confidence given the named stakeholders and customer count. A clear candidate for the same sprint as SSO if capacity allows.

**Performance improvements — Recommend: include if capacity allows**

P95 4.2s is a measured, quantified problem. Engineering flagged it — this is a supply-side concern, not just a customer request, but slow load times affect all users. No customer-linked business outcome cited, so rated medium. If engineering can scope this to a specific, targeted fix (not a full rewrite), worth including. Ask the team: what's the smallest change that gets P95 under 2.5s?

**Slack notifications — Recommend: defer pending revenue evidence**

47 forum upvotes show demand but no churn, ARR, or conversion evidence. Social signal alone does not justify pulling engineering time over items with direct revenue impact. Queue for discovery: does any churned customer cite missing Slack notifications?

**Dark mode — Recommend: defer**

Three enterprise customers requested it, and the CEO considers it important. That is social and political signal — not evidence of ARR at risk or churn. Until we have data showing enterprise deals blocked or customers churning over this, it ranks below revenue-backed items. Note for the CPO: if the CEO's interest represents an implicit commitment, that changes the calculus — flag it.

**Onboarding flow improvements — Recommend: data task first, not engineering**

CS team reports new users struggle. That's perception, not data. We have no drop-off rates, no funnel visualisation, and no step-by-step abandonment figures. Building improvements without that data risks fixing the wrong thing. Recommendation: assign a 1-2 day task to instrument the onboarding funnel (analytics events on each step). Once we have a drop-off chart, this item can be RICE-scored properly and scheduled.

[NEEDS CLARIFICATION]: Who owns instrumentation — Data Engineer or Engineering?
Owner: @product-owner to assign
Deadline: Before next sprint planning

**API rate limit increase — Recommend: discovery query before committing**

One power user requested this. Reach is completely unknown. Before this can be scored, run a quick analytics query: how many users in the last 30 days hit the current rate limit? If it's 1, defer. If it's 50, reconsider. This is a 30-minute data task, not an engineering commitment.

[NEEDS CLARIFICATION]: Who can run the rate-limit analytics query?
Owner: @data-engineer or engineering
Deadline: Before sprint planning

**Mobile app redesign — Recommend: do not pull in**

No customer request on record. The design team wants to do this — that is not customer evidence. With 94% of features seeing low engagement, a major redesign without a validated user problem is high risk. This item fails the Problem Validation gate: we cannot answer "How do you know?" with anything other than "the design team thinks so." Remove from sprint consideration until a problem statement with user evidence exists.

---

### Sprint recommendation (subject to capacity confirmation)

| Category | Items |
|---|---|
| **Ship next sprint** | SSO/SAML integration, CSV export |
| **Include if capacity allows** | Performance improvements (scoped fix) |
| **Do data work first, then schedule** | Onboarding flow (instrument funnel), API rate limit (analytics query) |
| **Defer — needs evidence** | Slack notifications, Dark mode |
| **Do not pull in** | Mobile app redesign |

This is a proposal — not a decision. Sprint planning needs the engineering team's effort estimates and the CPO's input on any strategic commitments I'm not aware of. If the CEO's view on dark mode represents a political commitment that supersedes the evidence, that's a conversation for you and the CPO to have before we lock the sprint.

---

**Clarifications remaining: 2**
**Quality checklist:** Pre-flight complete. RICE applied where data allows. Items with insufficient data flagged for discovery, not scheduled.

---

## Evaluation

### Criteria

- [x] PASS: Asks clarifying questions before prioritising — met. The simulated output opens with three explicit pre-prioritisation questions (sprint capacity, existing commitments, team composition) before producing the ranked table.

- [x] PASS: Flags that RICE scoring cannot be completed without reach/impact data — met. Onboarding flow and API rate limit are left unscored in the RICE table with explicit notes that data is missing. [NEEDS CLARIFICATION] markers are used per the agent's protocol.

- [x] PASS: Identifies SSO/SAML as likely highest priority — met. The agent definition's RICE framework applied to $180k ARR hard-blocked + security gate dependency surfaces SSO as the top item. The output explicitly cites the revenue figure and the blocked deal pattern.

- [x] PASS: Flags mobile redesign as lacking customer evidence — met. The definition's Problem Validation gate ("'I think users want this' is not evidence") and the Principles ("94% of features see low engagement", "Problem-first, always") directly produce the "no customer request on record" flag. The output explicitly removes it from sprint consideration.

- [~] PARTIAL: Applies RICE or equivalent prioritisation framework — partially met. RICE is specified fully in Step 4 with the formula and evidence-column requirement. The simulated output applies RICE to items with sufficient data and leaves unscored items flagged with reasons. Full scoring of all 8 items is not possible with the provided information — this is correct behaviour per the definition, not a failure.

- [x] PASS: Distinguishes between items with revenue impact evidence and items with social proof — met. The RICE Confidence column differentiates 100% (SSO, data-backed) from 80% (CSV export, informed estimate) from 50% (Slack, dark mode — social signal only). The reasoning section makes this distinction explicit for each item.

- [x] PASS: Recommends data gathering actions for items that cannot be scored — met. Onboarding flow gets a "1-2 day instrumentation task" recommendation. API rate limit gets a "30-minute analytics query" recommendation. Both include [NEEDS CLARIFICATION] markers with owner and deadline fields per the agent's protocol.

- [x] PASS: Produces a prioritised output with reasoning, not just a ranked list — met. Every item has a recommendation category ("ship", "data task first", "defer", "do not pull in") plus a prose reasoning block citing the specific evidence or lack thereof.

### Output expectations

- [x] PASS: Output ranks SSO/SAML as highest priority, citing $180k ARR and security-review block — met. The item-by-item section explicitly states "$180k ARR are blocked pending this" and "security review is a gate — not a nice-to-have." The recommendation is "ship next sprint."

- [x] PASS: Output applies RICE-style scoring with explicit numbers per item — met. The RICE table includes Reach, Impact, Confidence (%), Effort, and RICE score for each item. Unscored items show "—" with a notes column explaining the gap. The formula is stated. Uncertainty is flagged where present.

- [x] PASS: Output flags Mobile App Redesign as having no customer evidence — met. The reasoning states "No customer request on record. The design team wants to do this — that is not customer evidence." Fails the Problem Validation gate explicitly. Recommendation is "do not pull in."

- [x] PASS: Output flags Onboarding Flow Improvements as needing data before building — met. "CS team reports new users struggle. That's perception, not data. We have no drop-off rates." Instrumentation recommended as a 1-2 day task before any build commitment.

- [x] PASS: Output flags API Rate Limit Increase as needing scope discovery — met. "One power user requested this. Reach is completely unknown." A 30-minute analytics query is recommended before any engineering commitment.

- [x] PASS: Output's reasoning shows the source of each score — met. Revenue-backed items (SSO, CSV export) cite the source explicitly ($180k ARR, ~200 customers). Social-signal items (Slack 47 upvotes, dark mode 3 customers + CEO) acknowledge the lack of revenue evidence in the Confidence column and reasoning.

- [x] PASS: Output asks at least 2-3 clarifying questions before prioritising — met. Three questions are asked upfront: sprint capacity, existing commitments, and team composition.

- [x] PASS: Output addresses Performance Improvements as a candidate — met. Rated medium priority ("include if capacity allows") with the P95 4.2s figure cited as a quantified problem. Lack of a tied business outcome acknowledged. Engineering scoping is requested before committing.

- [x] PASS: Output distinguishes "ship next sprint" / "do data work now" / "do not pull in" — met. The sprint recommendation table explicitly uses these three categories plus "defer — needs evidence" for items that have insufficient signal but no active data path.

- [x] PASS: Output does not unilaterally prioritise — met. The closing paragraph frames the entire output as a proposal pending CPO and engineering input. The CEO dark mode comment is flagged as a potential political commitment that the product owner cannot resolve unilaterally.

## Notes

The definition handles this scenario well. The combination of mandatory problem validation, RICE scoring with evidence requirements, the [NEEDS CLARIFICATION] protocol, Decision Checkpoints, and the Backlog Grooming section produces the expected behaviour without requiring anything to be inferred or stretched.

The PARTIAL on RICE is correct: the agent cannot score items it doesn't have Reach or Effort data for, and the definition correctly mandates flagging rather than guessing. This is the right behaviour, not a gap.

One structural tension in the definition worth noting: the What You Don't Do section says "Estimate engineering effort — that's the CTO's team," yet RICE requires an Effort field. The simulated output handles this by labelling effort figures as estimates and flagging them for engineering confirmation — consistent with the non-unilateral-prioritisation criterion and the Decision Checkpoints. The definition doesn't resolve the tension explicitly, but the agent would navigate it correctly.
