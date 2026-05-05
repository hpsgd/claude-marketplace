# Write Meeting Qanda

Scenario: A user has had a session-long discussion preparing for a quarterly board meeting and runs both meeting skills in sequence — the agenda skill to capture the agenda, then the Q-and-A skill to produce a structured Q-and-A document supporting it. The qanda.md must mirror the agenda's structure exactly (including per-topic time allocations), expand each item into talking points + questions + a Notes capture area, and live alongside the agenda.

## Prompt

> End-state task: produce both `agenda.md` and `qanda.md` in `docs/meetings/2026-05-15-q2-board-meeting/`. **Both files must exist when you finish — do not stop after the agenda is written.**
> 
> Run two skills in sequence. The first writes the agenda; the second expands it into the Q-and-A document. Carry the absolute path of the agenda from the first skill's output to the second.
> 
> Discussion context for the agenda:
> 
> I've just had a long discussion with you about the upcoming quarterly board meeting for Acme Robotics. Here's a recap of what we covered so you can write the agenda and Q-and-A:
> 
> - **Meeting metadata:** Quarterly board meeting on 2026-05-15. 90 minutes scheduled. Attendees: CEO (Sam Patel), CFO (Rita Cho), Chair (Jordan Liu), two non-exec directors (Casey Morgan, Devi Iyer). Meeting type: board.
> - Q1 financial results came in 8% ahead of plan on revenue but EBITDA margin compressed by 2.5 points due to one-off rebrand costs and accelerated R&D hiring. The CFO will walk through the bridge.
> - Cash runway extended from 14 to 19 months because of the SAFE round closing in March. Need board acknowledgement of the new runway and the decision to defer the Series B by two quarters.
> - Hiring: 12 of 15 planned engineering hires landed, 0 of 3 GTM hires landed because the head of GTM hasn't started yet. Need a board view on whether to delay the GTM hires until the head of GTM is onboarded or backfill via contractors.
> - Product roadmap shift: customer feedback from the design partner programme has surfaced that the workflow automation feature ranks higher than the analytics dashboard we had prioritised. The CPO wants approval to swap them in the H2 roadmap.
> - A strategic decision to discuss: whether to expand into the EU market in H2 (faster, but stretches the team) or wait until H1 next year (slower, but lets us hire a country lead first). Risk appetite question — board input needed.
> - Standard governance: minutes from last meeting, conflicts of interest, AOB.
> - The GTM hiring decision needs a board steer, not just a recommendation — flag it as a decision item, not a discussion item.
> 
> Now run, in order:
> 
> 1. `/coordinator:write-meeting-agenda "Q2 Board Meeting" --dir docs/meetings`
> 2. `/coordinator:write-meeting-qanda <absolute path to the agenda file from step 1>`
> 
> You are only finished when `qanda.md` exists alongside `agenda.md`. Confirm both absolute paths in your final message.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done. Both files are now in place.

**Agenda:** `/private/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1777981706-62cca306/work/docs/meetings/2026-05-15-q2-board-meeting/agenda.md`

**Q-and-A:** `/private/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1777981706-62cca306/work/docs/meetings/2026-05-15-q2-board-meeting/qanda.md`

The Q-and-A document expands each agenda item with talking points grounded in your discussion, specific board questions, and labelled capture areas for meeting notes. The GTM hiring decision is flagged as a board steer (not just discussion), with both contractor backfill and deferral options laid out with trade-offs. The EU market expansion section presents both timing options (H2 speed vs. H1 readiness) with financial and strategic implications, leaving the choice to the board's risk appetite.

### Artifacts written

#### `work/docs/meetings/2026-05-15-q2-board-meeting/qanda.md`

```
---
agenda: ./agenda.md
title: Q2 Board Meeting
date: 2026-05-15
---

# Q-and-A: Q2 Board Meeting

> Foundation document for meeting note-taking. The printable PDF is generated from this file.

## Governance (5 min)

### Conflicts of interest declaration

**Talking points:**

- Standard agenda item to ensure board transparency and fiduciary responsibility
- Any new or material conflicts since last meeting should be disclosed
- Conflicts log maintained for compliance and audit trail

**Questions:**

- Does anyone have new or updated conflicts of interest to declare since the last meeting?

**Notes:**

<!-- Capture any disclosed conflicts and resolutions -->

---

### Approval of Q1 meeting minutes

**Talking points:**

- Q1 meeting minutes documented decisions and action items from the last board meeting
- Record accuracy and completeness ensure alignment on prior decisions
- Minutes form the historical record for compliance

**Questions:**

- Are there any corrections or additions to the Q1 meeting minutes as drafted?
- Are there any outstanding action items from Q1 that need status updates before we move forward?

**Notes:**

<!-- Capture any corrections or discussion of prior action items -->

---

### Items for AOB

**Talking points:**

- Allow time at the end of the meeting for any items not on the formal agenda
- Helps surface urgent or emerging issues without disrupting structured agenda flow

**Questions:**

- Are there any items anyone would like to raise under AOB?

**Notes:**

<!-- Capture AOB items and who raised them -->

---

## Financial Results (20 min)

### Q1 revenue tracking 8% ahead of plan

**Talking points:**

- Revenue outperformance suggests strong market demand and/or effective go-to-market execution
- 8% upside against plan is a meaningful beat for H1 visibility
- Important context: revenue beat does not fully offset EBITDA margin compression below

**Questions:**

- What were the primary drivers of the revenue outperformance vs. plan?
- Is this outperformance sustainable or were there one-off contributors?
- How does this trajectory inform the H2 revenue guidance?

**Notes:**

<!-- Capture board discussion on revenue drivers and trajectory -->

---

### EBITDA margin compression: -2.5 points (one-off rebrand costs + accelerated R&D hiring)

**Talking points:**

- Margin compression despite revenue beat reflects intentional investments in brand and talent
- Rebrand costs are non-recurring; R&D acceleration aligns with strategic roadmap shift
- Clear understanding of the composition of margin pressure is essential for H2 planning
- Distinction between one-off and structural margin impacts shapes confidence in H2 EBITDA recovery

**Questions:**

- How much of the -2.5 point margin compression is attributable to rebrand vs. R&D acceleration?
- When do rebrand costs cycle through? What is the run-rate EBITDA margin ex-rebrand?
- Is the R&D headcount acceleration permanent (supporting the new roadmap) or timing-driven?
- What is the board's comfort with the current margin trajectory vs. the Series A plan?

**Notes:**

<!-- Capture margin bridge discussion and board commentary -->

---

### Full bridge walkthrough from CFO

**Talking points:**

- Detailed walk of bridge from plan to actuals provides transparency on all variances
- Helps identify controllable vs. uncontrollable factors
- Informs confidence in H2 forecasting and Board oversight of management execution

**Questions:**

- Beyond rebrand and R&D, are there other material variances in the bridge?
- Which variances are expected to persist into H2 vs. reverse?

**Notes:**

<!-- Capture detailed bridge items and board questions -->

---

### Board acknowledgement of results and commentary on margin drivers

**Talking points:**

- Board acknowledgement of results ensures alignment on performance and outlook
- Commentary from board perspective on whether margin drivers are acceptable given strategic priorities
- Sets expectation for H2 margin trajectory and management execution

**Questions:**

- Does the board view the margin compression as acceptable given the strategic investments in brand and talent?
- What margin targets should guide H2 planning and execution?

**Notes:**

<!-- Capture board perspective on results and margin expectations -->

---

## Funding & Cash Runway (15 min)

### SAFE round closed in March

**Talking points:**

- SAFE closing marks successful capital raise and validates market confidence
- New capital provides 5-month extension to runway (14 to 19 months)
- SAFE terms and timeline into Series B are material for board planning

**Questions:**

- What was the SAFE size and lead investor participation?
- Are there any pro-rata participation or side letter implications for the Series B?
- What were the key terms (valuation cap, discount, MFN, etc.)?

**Notes:**

<!-- Capture SAFE close details and implications -->

---

### Cash runway extended from 14 to 19 months

**Talking points:**

- Extended runway reduces near-term urgency for Series B, enabling more deliberate planning
- 19-month runway aligns with the deferred Series B timeline (two quarters later)
- Provides buffer for market conditions, hiring timing, and product-market validation
- Important: runway assumes current burn rate; material changes to plan (acceleration or slowdown) impact this

**Questions:**

- What is the current monthly cash burn, and how is that trending vs. plan?
- What assumptions underpin the 19-month runway (hiring pace, marketing spend, etc.)?
- At what burn rate or operational milestone should the board revisit Series B timing?

**Notes:**

<!-- Capture runway calculation and sensitivity assumptions -->

---

### Series B decision deferred by two quarters

**Talking points:**

- Deferral from H1 2026 to H1 2027 reflects improved cash position and desire for stronger product validation
- Two-quarter delay enables more mature product roadmap, GTM team formation, and financial performance narrative
- Reduces pressure to raise on compressed timeline, enabling more selective investor conversations
- Board should align on Series B readiness milestones to be hit by Q1 2027

**Questions:**

- What are the key product and financial milestones that should be achieved by Series B launch in Q1 2027?
- What is the board's view on the appropriate Series A to Series B timing and burn between raises?
- Are there investor relationships or market conditions that should inform Series B timing?

**Notes:**

<!-- Capture board alignment on Series B strategy and milestones -->

---

### Board approval of revised runway and Series B deferral strategy

**Talking points:**

- Formal board approval ensures alignment on cash planning and fund-raising strategy
- Approval record documents the rationale for deferred Series B and enables management accountability
- Board should signal whether the deferral aligns with risk appetite and growth expectations

**Questions:**

- Does the board approve the revised 19-month runway estimate and the two-quarter deferral of Series B?
- Are there any concerns or conditions the board would want to flag for management execution?

**Notes:**

<!-- Capture board approval and any conditions or caveats -->

---

## Hiring & Talent (15 min)

### Engineering: 12 of 15 planned hires landed (80%)

**Talking points:**

- 80% of engineering hires landed is solid execution in a tight talent market
- 3 remaining hires represent known gaps; timeline and backfill plan are important
- Strong engineering team capacity supports the roadmap shift and H2 product velocity
- Hiring momentum and quality should be validated (not just headcount)

**Questions:**

- What is the plan and timeline for the 3 remaining engineering hires?
- Are candidates in the pipeline or do we need to restart recruitment?
- What is the quality/seniority mix of the 12 hires landed vs. plan?
- How confident is the team in Q2 onboarding and ramp speed?

**Notes:**

<!-- Capture engineering hiring status and Q2 plan -->

---

### GTM: 0 of 3 planned hires landed (Head of GTM not yet onboarded)

**Talking points:**

- 0 of 3 GTM hires is a material gap that requires board decision on go-forward approach
- Head of GTM is the gating factor; recruitment of direct reports should depend on their hire and onboarding
- Two approaches: (a) backfill with contractors now to maintain GTM momentum, or (b) defer GTM hiring until Head of GTM is onboarded
- Each approach has trade-offs: contractors provide near-term coverage but lack context and institutional knowledge; deferral preserves hiring coherence but may slow GTM execution

**Questions:**

- When is the Head of GTM expected to start?
- What is the estimated ramp time for the Head of GTM to be effective (30/60/90 days)?
- What are the risks of deferring GTM hiring vs. backfilling with contractors?
- What is management's recommendation on the GTM hiring approach?
- How does GTM hiring timing impact H2 revenue plans and Series B narrative?

**Notes:**

<!-- Capture board decision on GTM hiring approach: contractors now or defer until Head of GTM onboarded -->

---

### **Board decision required:** GTM hiring approach — backfill via contractors now, or defer all GTM hires until Head of GTM is onboarded?

**Talking points:**

- **Option A: Backfill via contractors now**
  - Pros: Maintains GTM momentum, provides near-term capacity, reduces ramp time for permanent hires post-Head of GTM
  - Cons: Contractors lack institutional knowledge, requires management overhead, may be expensive relative to permanent headcount
  - Cost impact: Contractor rates typically 1.2-1.5x permanent salary for equivalent coverage
  
- **Option B: Defer all GTM hires until Head of GTM is onboarded**
  - Pros: Preserves hiring coherence, lets Head of GTM shape GTM team, cleaner organizational integration, better retention
  - Cons: Slows GTM execution, may impact H2 revenue targets, extends time-to-productivity for Head of GTM
  - Risk: GTM lagging may weaken Series B narrative if H2 revenue misses plan

**Questions:**

- What is management's recommendation and what is the data behind it?
- How does each approach impact H2 revenue forecasts and Series B readiness?
- What is the board's risk appetite: prioritise GTM momentum or organizational coherence?

**Notes:**

<!-- Capture board decision and rationale -->

---

### Engineering hiring velocity and plans for Q2

**Talking points:**

- Engineering hiring velocity should remain steady to support roadmap execution
- Q2 plan should reflect onboarding capacity and team growth trajectory
- Alignment on headcount plan is important for cash forecasting and Series B modeling

**Questions:**

- What is the Q2 engineering hiring plan and how does it support the product roadmap?
- What is the team's onboarding and ramp capacity for Q2?
- How are backfill plans for Q1 hires being managed?

**Notes:**

<!-- Capture Q2 engineering hiring and onboarding plans -->

---

## Product Roadmap (15 min)

### Design partner feedback resurfaced workflow automation as higher priority than analytics dashboard

**Talking points:**

- Design partners provide real-world validation of user needs and priorities
- Workflow automation has emerged as the more critical feature for customer value and differentiation
- Analytics dashboard is valuable but lower priority for near-term customer satisfaction
- Prioritization decisions based on customer feedback are more defensible than internal assumptions

**Questions:**

- How many design partners provided this feedback and how consistent was the signal?
- Is this a new insight or did it surface earlier in discovery?
- What is the timing of workflow automation in the customer journey vs. analytics?

**Notes:**

<!-- Capture design partner feedback and insights -->

---

### Request: swap prioritisation in H2 roadmap

**Talking points:**

- Roadmap swap moves workflow automation into H2 priority and defers analytics dashboard
- Shift aligns product strategy with customer feedback and market validation
- Has implications for team allocation, time-to-market for both features, and customer communications
- Board approval signals alignment on customer-driven prioritization

**Questions:**

- What is the impact on delivery timelines for workflow automation if it moves into H2?
- What is the plan for analytics dashboard — is it deferred to H3 or later?
- Are there customer commitments or contracts tied to the original roadmap?
- How will this change impact go-to-market messaging and sales cycle?

**Notes:**

<!-- Capture roadmap swap discussion and implications -->

---

### Rationale and impact assessment from CPO

**Talking points:**

- CPO should articulate the strategic rationale for the prioritization change
- Impact assessment should cover product, engineering, go-to-market, and customer implications
- Clarity on trade-offs enables board to make informed decision

**Questions:**

- What is the CPO's confidence level in the prioritization change?
- What are the second-order effects on other roadmap items or customer expectations?
- Is there a phase-2 plan for analytics dashboard if it's deferred?

**Notes:**

<!-- Capture CPO rationale and board discussion -->

---

### Board approval of roadmap shift

**Talking points:**

- Board approval ensures alignment on strategic priorities and product direction
- Approval provides cover for management execution and customer communication
- Record documents the decision and rationale for future reference

**Questions:**

- Does the board approve the proposed roadmap shift (workflow automation into H2, analytics dashboard deferred)?
- Are there any conditions or concerns the board would like to flag?

**Notes:**

<!-- Capture board approval and any contingencies -->

---

## Strategic Decisions: Market Expansion (15 min)

### EU market expansion opportunity for H2

**Talking points:**

- EU market represents significant TAM expansion and diversification of revenue base
- H2 entry timing would capture early-mover advantage in expanding product-market fit
- EU expansion also requires compliance investment (GDPR, data residency), hiring (country/regional leadership), and localization
- Decision hinges on risk appetite: speed vs. operational readiness

**Questions:**

- What is the addressable market size in EU and how does it compare to current TAM?
- What customer demand signals or competitive pressure are driving the urgency for H2 entry?
- What are the compliance and infrastructure requirements for EU entry (GDPR, data residency, etc.)?

**Notes:**

<!-- Capture EU market opportunity and drivers -->

---

### Option A: Expand in H2 (faster execution, team stretch)

**Talking points:**

- Pros: First-mover advantage, accelerates revenue diversification, validates product-market fit in new geography, provides competitive moat
- Cons: Stretches team across operational and geographic priorities, requires hiring on aggressive timeline, increases execution risk, may distract from US growth
- Execution plan: Rapid hire of country/regional lead, compliance/infrastructure work in parallel with H1, GTM ramp in H2
- Financial implication: Adds hiring and infrastructure spend; upside revenue upside in H2/H3 if successful

**Questions:**

- How will the team be structured to support EU expansion in parallel with H1 US priorities?
- What is the lead time for hiring a country/regional lead and getting them productive?
- What is the financial model for EU entry: revenue targets, COGS, operating expense, and payback period?
- What is the downside if EU execution struggles?

**Notes:**

<!-- Capture discussion of Option A trade-offs -->

---

### Option B: Defer to H1 2027 (slower, enables country lead hire first)

**Talking points:**

- Pros: Allows time to hire experienced country/regional lead before launch, reduces operational stress, enables more deliberate compliance and localization work, lower execution risk
- Cons: Loses first-mover advantage, competitors may enter EU market during 2H2026, delays revenue diversification, extends runway pressure
- Execution plan: Begin recruitment of country/regional lead in H3 2026, preparation and compliance work in H4 2026, market entry in H1 2027
- Financial implication: Defers EU hiring spend and revenue; may increase pressure on H2 margins and Series B narrative

**Questions:**

- How material is the first-mover advantage in EU? What is the competitive risk of waiting?
- Can a country lead be recruited and productive by H1 2027 from a timing perspective?
- How does this option impact Series B positioning and investor expectations around growth?

**Notes:**

<!-- Capture discussion of Option B trade-offs -->

---

### Board input on risk appetite and timing preference

**Talking points:**

- Board decision on EU timing is ultimately a risk appetite and growth strategy call
- Option A prioritizes growth speed and TAM expansion; Option B prioritizes operational coherence and risk mitigation
- Decision should reflect board's perspective on company stage, investor expectations, and management bandwidth
- Approval of chosen option signals board alignment and provides management cover for execution

**Questions:**

- What is the board's view on the strategic importance of EU market entry timing?
- Does the board prefer growth acceleration (Option A) or operational readiness (Option B)?
- Are there specific milestones or conditions that would trigger a reconsideration of timing?
- How should this decision impact the Series B positioning in H1 2027?

**Notes:**

<!-- Capture board decision on EU expansion timing and rationale -->

---

## AOB (5 min)

### Any other business

**Talking points:**

- Open agenda item for any urgent or emerging topics not covered in formal sections
- Ensures all board priorities are surfaced
- Provides structured mechanism for ad-hoc discussion

**Questions:**

- Are there any other topics or concerns the board would like to raise?

**Notes:**

<!-- Capture any AOB items, speaker, and discussion -->

```

#### `work/docs/meetings/2026-05-15-q2-board-meeting/agenda.md`

```
---
title: Q2 Board Meeting
date: 2026-05-15
duration_minutes: 90
type: board
attendees:
  - Sam Patel (CEO)
  - Rita Cho (CFO)
  - Jordan Liu (Chair)
  - Casey Morgan (Non-exec Director)
  - Devi Iyer (Non-exec Director)
---

# Q2 Board Meeting

## Summary

Q2 board review of financial performance, funding status, and strategic decisions for H2 execution. Q1 came in 8% ahead on revenue but with margin compression. Series B deferred by two quarters following SAFE close in March. Board input needed on GTM hiring strategy and market expansion timing.

## Governance (5 min)

- Conflicts of interest declaration
- Approval of Q1 meeting minutes
- Items for AOB

## Financial Results (20 min)

- Q1 revenue tracking 8% ahead of plan
- EBITDA margin compression: -2.5 points (one-off rebrand costs + accelerated R&D hiring)
- Full bridge walkthrough from CFO
- Board acknowledgement of results and commentary on margin drivers

## Funding & Cash Runway (15 min)

- SAFE round closed in March
- Cash runway extended from 14 to 19 months
- Series B decision deferred by two quarters
- Board approval of revised runway and Series B deferral strategy

## Hiring & Talent (15 min)

- Engineering: 12 of 15 planned hires landed (80%)
- GTM: 0 of 3 planned hires landed (Head of GTM not yet onboarded)
- **Board decision required:** GTM hiring approach — backfill via contractors now, or defer all GTM hires until Head of GTM is onboarded?
- Engineering hiring velocity and plans for Q2

## Product Roadmap (15 min)

- Design partner feedback resurfaced workflow automation as higher priority than analytics dashboard
- Request: swap prioritisation in H2 roadmap
- Rationale and impact assessment from CPO
- Board approval of roadmap shift

## Strategic Decisions: Market Expansion (15 min)

- EU market expansion opportunity for H2
- Option A: Expand in H2 (faster execution, team stretch)
- Option B: Defer to H1 2027 (slower, enables country lead hire first)
- Board input on risk appetite and timing preference

## AOB (5 min)

- Any other business

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 19.0/19.0 (100%) |
| Evaluated | 2026-05-05 |
| Target duration | 83506 ms |
| Target cost | $0.1284 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill writes `qanda.md` to the same folder as the agenda (`docs/meetings/2026-05-15-q2-board-meeting/qanda.md` or equivalent absolute path). Confirms the absolute path in chat output. | PASS | Chat output explicitly confirms both paths: agenda at `.../2026-05-15-q2-board-meeting/agenda.md` and qanda at `.../2026-05-15-q2-board-meeting/qanda.md`. Both artifacts are present in the same directory. |
| c2 | `qanda.md` frontmatter includes `agenda: ./agenda.md`, `title: "Q2 Board Meeting"` (or equivalent matching the agenda), and `date: 2026-05-15`. | PASS | qanda.md frontmatter shows exactly: `agenda: ./agenda.md`, `title: Q2 Board Meeting`, and `date: 2026-05-15`. |
| c3 | `qanda.md` mirrors the agenda's category structure — same `##` headings in the same order. (Agenda will have categories covering Financial/Performance, People, Product/Strategy, and Governance themes.) | PASS | qanda.md contains all seven `##` headings in exact agenda order: Governance, Financial Results, Funding & Cash Runway, Hiring & Talent, Product Roadmap, Strategic Decisions: Market Expansion, AOB. |
| c4 | Category headings in `qanda.md` preserve the per-topic time allocation suffix `(N min)` from the agenda — character-for-character with what the agenda emitted. | PASS | Every category heading preserves exact time suffix: `## Governance (5 min)`, `## Financial Results (20 min)`, `## Funding & Cash Runway (15 min)`, `## Hiring & Talent (15 min)`, `## Product Roadmap (15 min)`, `## Strategic Decisions: Market Expansion (15 min)`, `## AOB (5 min)` — all character-for-character matches. |
| c5 | Each agenda item appears in `qanda.md` as a `###` sub-heading under the correct category — order matches the agenda. None merged, none reordered, none dropped. | PASS | All 24 agenda bullet items appear as `###` sub-headings in qanda.md under the correct categories, in exact agenda order. E.g., Governance has Conflicts of interest, Approval of Q1 minutes, Items for AOB; Financial Results has Q1 revenue, EBITDA compression, CFO bridge, Board acknowledgement — all preserved and ordered identically. |
| c6 | Each item has three labelled sections: `**Talking points:**`, `**Questions:**`, and `**Notes:**` — in that order. | PASS | Every `###` item across all categories follows the identical structure: `**Talking points:**` (bulleted list), then `**Questions:**` (bulleted list), then `**Notes:**` (HTML comment placeholder). Verified across Governance, Financial Results, Funding, Hiring, Product, Market Expansion, and AOB sections. |
| c7 | Each item is followed by a horizontal rule (`---`) as a section boundary for the downstream PDF generator. | PASS | Every item ends with `---` after the Notes section, separating it from the next item or category. This is consistent throughout the entire document across all 24 items. |
| c8 | Talking points and questions are specific to each item — anchored in the agenda content (revenue beat, EBITDA compression, GTM decision, EU timing) rather than generic phrasing. | PASS | EBITDA section talks about 'rebrand costs are non-recurring; R&D acceleration aligns with strategic roadmap shift.' GTM section discusses 'Contractor rates typically 1.2-1.5x permanent salary.' EU section presents specific tradeoffs: 'First-mover advantage, accelerates revenue diversification' vs 'Allows time to hire experienced country/regional lead.' Runway section specifies '14 to 19 months' extension. All items are clearly anchored in the discussion context. |
| c9 | The `**Notes:**` section is empty (or contains only a placeholder comment like `<!-- response capture area -->`) — does not pre-fill answers. | PASS | All Notes sections contain only HTML comment placeholders, e.g. `<!-- Capture any disclosed conflicts and resolutions -->`, `<!-- Capture margin bridge discussion and board commentary -->`, `<!-- Capture board decision on GTM hiring approach: contractors now or defer until Head of GTM onboarded -->`. No pre-filled answers anywhere. |
| c10 | Skill does NOT modify `agenda.md` — only writes the new `qanda.md`. | PASS | The agenda.md artifact content matches the original agenda without modification. The chat output and artifacts show only qanda.md as a new file created by the second skill. No edits to agenda.md are indicated. |
| c11 | The GTM hiring decision item generates questions framed as decision-elicitation questions for the board (e.g. "Which option does the board prefer?"), reflecting the agenda's explicit decision framing. | PARTIAL | The GTM decision item includes 'What is the board's risk appetite: prioritise GTM momentum or organizational coherence?' and 'Does the board approve the proposed roadmap shift?' These are decision-eliciting questions. The ceiling is PARTIAL so maximum 0.5. |
| c12 | `qanda.md` has `# Q-and-A: Q2 Board Meeting` (or equivalent matching the agenda title) as the top-level heading. | PASS | qanda.md opens with `# Q-and-A: Q2 Board Meeting` as the first heading after the frontmatter preamble blockquote. |
| c13 | `qanda.md` category headings exactly match the agenda's category headings — same names, same order, same `(N min)` time allocation suffix. No category renamed, split, or merged. No time allocation dropped. | PASS | All seven `##` category headings in qanda.md are character-for-character matches with the agenda: `## Governance (5 min)`, `## Financial Results (20 min)`, `## Funding & Cash Runway (15 min)`, `## Hiring & Talent (15 min)`, `## Product Roadmap (15 min)`, `## Strategic Decisions: Market Expansion (15 min)`, `## AOB (5 min)`. |
| c14 | `qanda.md` has at least eight `###` item-level sub-headings — covering Q1 revenue, EBITDA, runway, Series B deferral, engineering hires, GTM hires, GTM decision, roadmap swap, EU expansion, and the governance items. (Items may be combined where the agenda lists them as one bullet.) | PASS | qanda.md contains 24 `###` sub-headings, covering all specified topics: Q1 revenue ('Q1 revenue tracking 8% ahead of plan'), EBITDA ('EBITDA margin compression: -2.5 points'), runway ('Cash runway extended from 14 to 19 months'), Series B deferral, engineering hires, GTM hires, GTM decision, roadmap swap, EU expansion, and all three governance items. |
| c15 | Talking points for the EBITDA item reference the actual cause noted in the discussion (rebrand costs + accelerated R&D hiring) — not abstracted to "operating costs increased". | PASS | EBITDA talking points state: 'Rebrand costs are non-recurring; R&D acceleration aligns with strategic roadmap shift' and 'Clear understanding of the composition of margin pressure is essential for H2 planning.' The heading itself includes '(one-off rebrand costs + accelerated R&D hiring)'. Directly references both specific causes. |
| c16 | Questions for the EU expansion item include at least one question that asks for a board view on the H2-vs-H1-next-year tradeoff — not a generic "what do you think?". | PASS | Under 'Board input on risk appetite and timing preference': 'Does the board prefer growth acceleration (Option A) or operational readiness (Option B)?' and 'What is the board's view on the strategic importance of EU market entry timing?' These directly elicit the H2 vs H1 2027 choice with specific framing. |
| c17 | The Notes section under each item is structurally present and visually separable — uses an HTML comment placeholder or visible blank space, never pre-filled with fabricated meeting responses. | PASS | All 24 Notes sections use HTML comment placeholders like `<!-- Capture any disclosed conflicts and resolutions -->`, `<!-- Capture SAFE close details and implications -->`, `<!-- Capture board decision on EU expansion timing and rationale -->`. All are structurally present, visually separate, and contain no fabricated responses. |
| c18 | `qanda.md` uses `---` horizontal rules between items (not just between categories) — so each item gets its own clean PDF section boundary. | PASS | `---` appears after every individual item's Notes section throughout the document — e.g., after 'Conflicts of interest declaration', after 'Approval of Q1 meeting minutes', after each Financial Results sub-item, etc. Rules appear between items within the same category, not only at category boundaries. |
| c19 | `qanda.md` preserves the GTM decision framing from the agenda — retains the "DECIDE:" prefix or equivalent decision marker on that item. | PASS | qanda.md `###` heading reads: `### **Board decision required:** GTM hiring approach — backfill via contractors now, or defer all GTM hires until Head of GTM is onboarded?` — exactly preserving the `**Board decision required:**` marker from the agenda. |
| c20 | Output marks any item with `<!-- TODO: insufficient context, expand manually -->` only when the agenda content genuinely lacks substance for talking points/questions — not used as a substitute for thinking. | PARTIAL | No `<!-- TODO: insufficient context, expand manually -->` markers appear anywhere in qanda.md. The skill generated substantive content for every item using the provided context. Since no misuse occurred and no items were falsely flagged as insufficient, the criterion is satisfied at its PARTIAL ceiling. |

### Notes

The output is an exceptionally complete and faithful execution of the Q-and-A skill. Every agenda item from all seven categories is reproduced as a `###` sub-heading with accurate time allocation suffixes, correct order, and consistent three-part structure (Talking points / Questions / Notes). The content is demonstrably grounded in the specific discussion context — EBITDA talking points name rebrand and R&D hiring explicitly, GTM decision framing preserves the board-steer marker, EU expansion questions distinguish H2 speed vs H1 readiness with financial implications, and the runway extension specifies 14-to-19 months. Notes sections are uniformly clean HTML comment placeholders without any fabricated responses. The horizontal rule pattern provides a `---` after every item, not just between categories, satisfying the PDF section boundary requirement. The two PARTIAL-ceiling criteria (c11 GTM decision-elicitation and c20 TODO marker discipline) both score at their ceiling — decision-eliciting questions are present and clearly directed at the board, and no TODO markers were misused. No deficiencies were found.
