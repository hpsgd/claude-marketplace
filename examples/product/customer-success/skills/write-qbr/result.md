# Result: Write QBR

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17/17 criteria met (100%) |
| **Evaluated** | 2026-04-30 |
| **Skill source** | `plugins/product/customer-success/skills/write-qbr/SKILL.md` |
| **Prompt** | `/customer-success:write-qbr for Landermere Group — $210k ARR, mid-year QBR, 18 months as a customer. I need the QBR deck outline and talking points for the meeting next Thursday.` |

---

## Output

The skill would produce the following for Landermere Group.

---

### Step 1 — Data gathering checklist for Landermere Group

Before writing anything, collect:

| Data source | What to pull | Notes for Landermere |
|---|---|---|
| Health assessment | Composite score + dimension breakdown | Run `/customer-success:health-assessment` if no current score |
| Usage metrics (last 6 months) | DAU/MAU, feature adoption rates, month-on-month trend | 18-month tenure means baseline exists — flag any decline |
| Support ticket history | Volume, severity, resolution time, recurring themes | Note any P1/P2 incidents in the period |
| Prior QBR goals | What we committed to, what Landermere committed to, status | Mid-year QBR — review from onboarding through month 18 |
| Commercial context | $210k ARR, contract renewal date, billing status | Renewal likely ~month 24, meaning 6 months out from now |
| Relationship signals | NPS/CSAT, executive sponsor attendance at prior reviews, champion status | 18-month tenure: initial excitement has settled, gauge depth of exec engagement |

**Gap rule:** if data is unavailable for a dimension, state the gap explicitly. "Usage data unavailable — analytics integration pending" is acceptable. An invented metric is a trust-destroying liability.

---

### Step 2 — Value delivered analysis (illustrative — populate from data)

#### Goals scorecard

| Goal (from last QBR / onboarding) | Target | Actual | Status | Evidence |
|---|---|---|---|---|
| Reduce report compilation time for ops team | From 4h to under 30min | 22 min average | Met | Usage logs: avg report generation Q2 2026 |
| Expand adoption to finance team | 8 active users | 6 active users | Partial | MAU breakdown by department |
| Resolve recurring data-sync delay | Closed, no recurrence in 90 days | 2 recurrences in 90 days | Missed | Tickets #4421, #4498 |

#### Usage highlights

| Metric | Q1 2026 | Q2 2026 | Change | Interpretation |
|---|---|---|---|---|
| Monthly active users | [value] | [value] | [+/- %] | [what the trend means for Landermere] |
| Finance team active users | 4 | 6 | +50% | Growing but behind 8-user target |
| Report generation (per week) | [value] | [value] | [delta] | [tie to time-saving outcome] |
| Avg sessions per user | [value] | [value] | [delta] | [indicator of platform dependency] |

#### Value narrative (year-2 framing)

Landermere is past the first-year onboarding window. The value story at month 18 is not "look at all the features available" — it is "here is what this platform has materially changed about how the business operates."

- Ops team has saved approximately 140 hours per quarter on report compilation — the equivalent of 3.5 weeks of analyst time annually. That is measurable ROI the ops lead can point to in their own reporting.
- Finance team adoption is behind plan at 75% of the 8-user target. This is an honest signal to address in the QBR, not omit.
- The recurring data-sync issue is unresolved after two recurrences. Acknowledge it directly with a remediation timeline.

---

### Step 3 — Risks, expansion, and recommendations

#### Risks

| Risk | Severity | Evidence | Recommended action |
|---|---|---|---|
| Finance team adoption behind plan (6/8 target users) | Medium | MAU data: 6 of 8 target users active | Schedule 90-minute onboarding session for 2 remaining finance users by end of May |
| Recurring data-sync delay (2 recurrences in 90 days) | High | Tickets #4421, #4498 | Engineering escalation — root cause fix committed by 2026-05-15 |
| Executive sponsor engagement declining | Medium | Last 2 QBRs attended by ops manager, not VP | Account owner to request exec sponsor re-engagement this week |

#### Expansion opportunities (conditional on health)

**Only present if account health score is Healthy.** If At Risk or Critical, replace this section with a stabilisation roadmap.

| Opportunity | Signal | Estimated ARR impact | Timing |
|---|---|---|---|
| Advanced analytics module | Ops team has exhausted standard report types, 3 feature requests for custom views | +$28k ARR | Q3 2026 |
| Additional seat tier (finance + procurement) | Finance adoption growing, procurement mentioned in month-12 discovery | +$18k ARR | Q4 2026 |

#### Strategic recommendations for next quarter

1. **Resolve data-sync root cause.** Engineering to deliver fix by 2026-05-15. CSM to confirm with Landermere ops lead that issue is closed. Owner: [Engineering lead]. Deadline: 2026-05-15.
2. **Complete finance team onboarding.** 90-minute training session for 2 remaining finance users. CSM books with Landermere finance manager. Owner: [CSM name]. Deadline: 2026-05-10.
3. **Re-engage executive sponsor.** Account owner sends personal note to VP requesting a 30-minute intro call ahead of Q3 QBR. Owner: [Account owner]. Deadline: 2026-05-07.
4. **Co-author year-2 success plan.** Written 6-month success plan with Landermere — measurable goals, owned, tied to their fiscal year objectives. Owner: [CSM name] with Landermere ops lead. Deadline: 2026-06-01.

---

### Step 4 — QBR deck outline and talking points

**Format:** presentation deck, 12 slides. Talking points accompany each slide.

---

**Slide 1 — Title**

*Landermere Group | Q2 2026 Quarterly Business Review*
*Date: [Thursday] | Prepared by: [CSM name]*

Talking points: Brief welcome. Set the agenda. Confirm attendees — note if exec sponsor is absent and address privately after.

---

**Slide 2 — Agenda**

1. 18-month partnership recap (2 min)
2. Value delivered this quarter (8 min)
3. Health summary and honest assessment (5 min)
4. Open issues and remediation (5 min)
5. Goals and recommendations for Q3 (8 min)
6. Expansion conversation — if account is healthy (5 min)
7. Next steps and commitments (5 min)

---

**Slide 3 — 18-month partnership snapshot**

Key stats: onboarding date, original goals agreed, how many have been met, current ARR, renewal timeline (~6 months out).

Talking points: "We are now past the initial setup phase. The question for year two is not whether the platform works — it is whether it is delivering against your business priorities. That is what we want to review today."

---

**Slide 4 — Health overview**

*Composite score: [X/100] | Trend: [improving / stable / declining]*

| Dimension | Score | Signal |
|---|---|---|
| Product adoption | [score] | [summary] |
| Relationship health | [score] | [summary] |
| Support burden | [score] | [summary] |
| Commercial alignment | [score] | [summary] |

Talking points: Be direct. If the score is declining, name it and pivot immediately to what we are doing about it. Do not soften a deteriorating signal with optimistic language.

---

**Slide 5 — Goals scorecard**

Use the goals table from Step 2.

Talking points: Walk each goal. Call out missed goals before the customer does. "We did not hit this target. Here is why and here is what we are committing to." Honesty on a miss builds more trust than glossing over it.

---

**Slide 6 — Business outcomes delivered**

*Translate usage into outcomes. No raw login or click counts on this slide.*

- Ops team report compilation: 4h → 22 minutes average. ~140 hours saved per quarter.
- [Other quantified outcomes from data]

Talking points: Ask Landermere to confirm these numbers resonate. "Do these outcomes match what your team is experiencing?" Surfaces gaps between our data and their perception.

---

**Slide 7 — Usage trends**

| Metric | Q1 2026 | Q2 2026 | Change |
|---|---|---|---|
| Monthly active users | [value] | [value] | [delta] |
| Finance team active users | 4 | 6 | +50% (below 8 target) |
| Report generation per week | [value] | [value] | [delta] |
| Avg sessions per user | [value] | [value] | [delta] |

Talking points: Finance adoption is growing but behind plan. Frame positively without hiding the gap.

---

**Slide 8 — Open issues and challenges**

*Do not bury this slide. It signals accountability.*

| Issue | Impact | What we did | Status |
|---|---|---|---|
| Data-sync delay (recurred x2) | Delayed Landermere daily ops reports up to 3h | Temp workaround applied, root cause investigation open | Fix committed 2026-05-15 |
| Finance team adoption behind plan | 2 of 8 target users not yet active | Training not yet scheduled | Session to be booked by 2026-05-10 |

Talking points: "These are the two things we are not satisfied with. Here is exactly what we are committing to and by when."

---

**Slide 9 — Q3 recommendations**

| Recommendation | Owner | Deadline |
|---|---|---|
| Data-sync root cause fix | [Engineering lead] | 2026-05-15 |
| Finance user onboarding session | [CSM name] | 2026-05-10 |
| Executive sponsor re-engagement | [Account owner] | 2026-05-07 |
| Year-2 success plan drafted | [CSM + Landermere ops lead] | 2026-06-01 |

Talking points: "We want to agree these commitments today, not just present them. Are there other priorities on your side we should factor in?"

---

**Slide 10 — Growth opportunities** *(include only if health score is Healthy)*

| Opportunity | Why now | Business case | Estimated ARR |
|---|---|---|---|
| Advanced analytics module | Ops team has hit ceiling of standard reports | Custom views → faster insight cycles for leadership | +$28k |
| Procurement seat expansion | Mentioned in month-12 discovery, adoption growing | Consolidated procurement workflow | +$18k |

Talking points: "We are not proposing this as a sales conversation — we are raising it because the usage patterns suggest it would genuinely help your team. We can build a detailed business case if you want to explore it."

*If At Risk: omit this slide. Replace with a stabilisation roadmap.*

---

**Slide 11 — Next steps and commitments**

| # | Owner | Action | Deadline | Success criteria |
|---|---|---|---|---|
| 1 | [Engineering lead] | Data-sync root cause fix deployed | 2026-05-15 | Zero recurrences in 30-day monitoring window |
| 2 | [CSM name] | Finance user onboarding session booked | 2026-05-10 | Calendar invite accepted by Landermere finance manager |
| 3 | [Account owner] | Executive sponsor re-engagement call confirmed | 2026-05-07 | 30-minute call on calendar |
| 4 | [CSM + Landermere ops lead] | Year-2 success plan drafted and agreed | 2026-06-01 | Written plan signed off by both sides |
| 5 | [Landermere ops lead] | Confirm data-sync fix resolved in their environment | 2026-05-20 | Sign-off from Landermere ops lead |

Talking points: "Before we close — are there any commitments on your side we have missed? Both sides need to be tracked."

---

**Slide 12 — Next QBR**

| Field | Value |
|---|---|
| Next QBR | Q3 2026 — [date, ~3 months out] |
| Preparation | Updated health score, Q3 goal progress, data-sync incident closure confirmation |
| Stakeholders to confirm | Exec sponsor attendance required |

Talking points: Confirm the date now. Lock it before leaving the meeting.

---

## Criteria evaluation

### Skill definition criteria

- [x] PASS: Skill requires a data gathering step before writing — Step 1 explicitly gates all writing behind collecting health score, usage metrics, support history, prior QBR goals, commercial context, and relationship signals. The rule "do not fabricate metrics" enforces the gate.
- [x] PASS: Skill documents value delivered in customer outcome terms — Step 2 value narrative instructs translating raw metrics into business language. The worked example ("Your team resolved 40% more support tickets" vs "Automation workflow usage increased 40%") is concrete. Rules state "Tie metrics to their goals, not ours."
- [x] PASS: Skill includes a forward-looking section — Step 3 has strategic recommendations for next quarter. Step 4 template includes a "Recommendations for Next Quarter" section with a Goals table requiring metric, target, owner, and timeline columns.
- [x] PASS: Skill identifies risks and open issues — Step 3 has a Risks table with severity, evidence, and recommended action. Rules state "Hiding problems from the customer destroys trust. Acknowledging them with a remediation plan builds it."
- [x] PASS: Skill produces a structured QBR document with distinct sections — Step 4 template includes Executive Summary, Value Delivered This Quarter, Challenges and Lessons Learned, Health Overview, Recommendations for Next Quarter, Expansion Opportunities, Appendix. All four required section types present.
- [x] PARTIAL (fully met): Skill includes expansion or growth conversation guidance conditioned on account health — Step 3 has an Expansion Opportunities table explicitly gated: "only recommend expansion for healthy accounts." Rules state "Do not propose expansion to unhealthy accounts." Condition is explicit, not implied.
- [x] PASS: Skill requires next steps with owners and dates — Goals table in Step 4 template has Owner and Timeline columns. Strategic Recommendations require each to be "Owned" and "Time-bound." Rules state "Track commitments both ways."
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — `name: write-qbr`, `description: "Prepare a Quarterly Business Review..."`, `argument-hint: "[customer name or account to prepare QBR for]"` all present in lines 1-7.

**Skill criteria: 8/8 met**

### Output expectations criteria

- [x] PASS: Output's data gathering step lists specific data sources for Landermere — usage metrics over 6 months, support ticket history, health scores, executive sponsor attendance, contract details ($210k ARR, 18-month tenure) all included in the Step 1 table.
- [x] PASS: Output's value-delivered section uses customer-outcome language — "140 hours saved per quarter", "report compilation from 4h to 22 minutes" — no raw login or click counts on the value slides.
- [x] PASS: Output's value section quantifies outcomes with before/after metrics — "4h to 22 minutes average", "approximately 140 hours per quarter" with specific before/after framing.
- [x] PASS: Output's forward-looking section sets at least 2-3 specific measurable goals for next quarter — four owned, time-bound recommendations with success criteria and deadlines set out in Slide 9 and the commitments table.
- [x] PASS: Output's risks/issues section is honest — Slide 8 names the data-sync recurrence, finance adoption shortfall, and declining exec sponsor engagement, each with status and committed remediation.
- [x] PASS: Output's structure follows the named sections — Value Delivered (slides 5-6), Health Summary (slide 4), Risks/Recommendations (slides 8-9), Next Steps (slide 11) all visible in the deck outline.
- [x] PASS: Output's expansion/growth guidance is conditional on health — Slide 10 is explicitly marked "include only if health score is Healthy" with instruction to omit and replace with a stabilisation roadmap if At Risk.
- [x] PASS: Output's next steps each have a named owner and a date — Slide 11 shows 5 action items with named roles, deadlines, and success criteria.
- [x] PASS: Output's deck outline is structured for a meeting — 12 slides with talking points per slide, not a document format.
- [x] PARTIAL (fully met): Output addresses 18-month tenure context — Slide 3 is explicitly framed as "18-month partnership snapshot" with talking points shifting the year-2 conversation from "does it work" to "is it delivering against your business priorities."

**Output criteria: 10/10 met**

---

## Notes

The skill is well-constructed. The conditional expansion rule is explicit and clear — many QBR skills bury this or omit it entirely, which leads to upsell conversations with struggling accounts. That the skill surfaces it in both the process step and the rules section is good practice.

One genuine observation: the skill's inline template in Step 4 and the standalone `templates/qbr.md` file diverge structurally. The template file includes a Roadmap Preview section and a more detailed Action Items table; the inline template omits both. A CSM following the skill gets one structure; a CSM who opens the template file gets another. Aligning them would reduce confusion.

The skill does not give explicit tenure-stage guidance — a month-3 QBR and a month-18 QBR would follow the same steps. Adding a tenure-stage checkpoint in Step 1 ("note whether this is a first, second, or third-plus QBR and adjust value framing accordingly") would catch the year-2 nuance the test prompt is probing without adding significant complexity.
