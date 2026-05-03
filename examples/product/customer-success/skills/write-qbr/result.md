# Write Qbr

Scenario: Testing whether the write-qbr skill requires gathering account data before writing, documents value delivered in customer terms, and includes forward-looking recommendations with risks.

## Prompt

> /customer-success:write-qbr for Landermere Group — $210k ARR, mid-year QBR, 18 months as a customer. I need the QBR deck outline and talking points for the meeting next Thursday.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

QBR brief saved to `landermere-group-qbr-2026-h1.md`.

**One question before you prep this further:** You mentioned a "deck outline and talking points" — what I've produced is a structured brief (sections map 1:1 to slides) with talking points per section. If you need actual slide titles + 3-4 bullet talking points per slide (presentation-ready format rather than a reference doc), I can restructure it that way. Which format are you taking into the room?

**What's in the doc now:**
- 60-minute agenda with owner and purpose per segment
- Goals scorecard template (pull from last QBR notes)
- Win framing, challenge acknowledgement section with direct talking points
- Health overview (flagged: run `/health-assessment` to populate it)
- H2 goals table + expansion opportunity section (gated on account health)
- Pre-meeting checklist — all `[DATA NEEDED]` fields must be filled before Thursday

No metrics were fabricated. Every gap is explicitly labelled.

### Artifacts written

#### `work/landermere-group-qbr-2026-h1.md`

```
# Quarterly Business Review: Landermere Group

**Period:** H1 2026 (January – April 2026)
**Prepared by:** [CSM Name]
**Date:** 2026-05-07
**ARR:** $210,000
**Tenure:** 18 months (customer since ~November 2024)
**Next QBR:** [Q3 2026 — suggest scheduling now]

---

> **Data gaps flagged in this document.** Fields marked `[DATA NEEDED]` must be filled from CRM, product analytics, and support systems before the meeting. Do not present placeholders to the customer. Talking points are ready to use once numbers are filled in.

---

## Executive Summary

Landermere Group is entering their second year as a customer at $210k ARR. [HEALTH STATUS — e.g., "The account is healthy with strong adoption in X, though Y remains an area to develop together."] This review covers [key wins — e.g., "the successful rollout to the operations team and a 30% reduction in manual reporting time"], acknowledges [key challenge — e.g., "slower-than-planned adoption of the analytics module"], and proposes a focused plan for H2 2026 including [top recommendation — e.g., "a structured onboarding sprint for the remaining 15 unlicensed users"].

**Talking point (open the meeting with this):**
> "We're at the 18-month mark — a good moment to step back, look at what's actually moved for your team, and make sure what we're building together is tracking to your goals for the rest of the year. I want to spend most of this time on where you want to go, not just looking backwards."

---

## 1. Value Delivered This Half

### Goals Scorecard

*Pull from last QBR or account plan. These are what both sides committed to in November 2025 or your H2 2025 review.*

| Goal | Owner | Target | Actual | Status | Notes |
|---|---|---|---|---|---|
| [Goal 1 — e.g., Expand to ops team] | [Us / Customer] | [DATA NEEDED] | [DATA NEEDED] | Met / Partial / Missed | [Talking point if missed — own it, have a remediation] |
| [Goal 2] | [Us / Customer] | [DATA NEEDED] | [DATA NEEDED] | Met / Partial / Missed | |
| [Goal 3] | [Us / Customer] | [DATA NEEDED] | [DATA NEEDED] | Met / Partial / Missed | |

**If a goal was missed:** Address it directly before the customer raises it.
> "We committed to [X] by [date] and didn't deliver. Here's what got in the way, and here's what we're doing differently in H2."

### Key Wins

Replace placeholders with 2-3 specific, quantified wins before the meeting.

1. **[Win 1 — quantified]** e.g., "Your team closed [X] more [tickets / cases / reports] per week in Q1 versus Q4 2024, using [feature] — an estimated saving of [Y hours / $Z] over the half."
2. **[Win 2 — quantified]** e.g., "The [team / department] rollout in [month] brought active users from [N] to [N+X], giving [business outcome]."
3. **[Win 3 — quantified]** e.g., "Response time for [customer's KPI] dropped from [X] to [Y] after the [workflow / integration] was implemented in [month]."

**Talking point:**
> "The number I want to draw your attention to is [most impressive metric]. That translates directly to [business outcome they care about] — [frame it in their language, not ours]."

### Usage Trends

| Metric | H2 2025 | H1 2026 | Change | What it means |
|---|---|---|---|---|
| Active users (DAU/MAU) | [DATA NEEDED] | [DATA NEEDED] | [+/- %] | [Interpretation] |
| [Feature 1] adoption | [DATA NEEDED] | [DATA NEEDED] | [+/- %] | [Interpretation] |
| [Feature 2] adoption | [DATA NEEDED] | [DATA NEEDED] | [+/- %] | [Interpretation] |
| Seat utilisation | [DATA NEEDED] | [DATA NEEDED] | [+/- %] | [If <80% — flag as risk] |

---

## 2. Challenges and Lessons Learned

*Be direct. Customers know when things went wrong — what they're watching for is whether you know, and what you're doing about it.*

| Challenge | Business impact | Our response | Current status |
|---|---|---|---|
| [e.g., Support ticket spike in Feb] | [e.g., Delayed [workflow] for 2 weeks] | [e.g., Hot-fixed in 72h, root cause addressed in v[X]] | Resolved / In progress / Monitoring |
| [e.g., Slow feature X adoption] | [e.g., [Team] still running manual process] | [e.g., Scheduled training for [date]] | In progress |
| [e.g., P1 incident if applicable] | [DATA NEEDED] | [DATA NEEDED] | [DATA NEEDED] |

**Talking point for any challenge:**
> "I want to be direct about [issue]. It impacted [specific thing] and that wasn't acceptable. What we did was [response]. What we've changed so it doesn't happen again is [structural fix]. Do you have questions about that?"

---

## 3. Health Overview

*Run `/customer-success:health-assessment` to populate this section accurately. Do not estimate.*

- **Composite score:** [DATA NEEDED — 0-100]
- **Trend:** [Improving / Stable / Declining]
- **Dimension breakdown:**

| Dimension | Score | Signal |
|---|---|---|
| Product adoption | [DATA NEEDED] | [Key observation] |
| Engagement | [DATA NEEDED] | [Meeting attendance, responsiveness] |
| Relationship | [DATA NEEDED] | [Sponsor strength, champion status] |
| Value realisation | [DATA NEEDED] | [ROI indicators] |
| Commercial | [DATA NEEDED] | [Renewal date, billing status] |

**Talking point (do not read scores aloud — translate them):**
> "Overall we're in [good shape / a stable position / a place I want to improve with you]. The area I want us to focus on together in H2 is [lowest dimension], because that's where I think there's the most upside."

---

## 4. Recommendations for H2 2026

### Goals — Both Sides

*Each goal must be specific, owned, and time-bound. "Increase adoption" is not a goal.*

| Goal | How measured | Target | Owner | By when |
|---|---|---|---|---|
| [e.g., Train analytics team on reporting module] | Session held, [N] users active post-training | [N] users active within 30 days | Us | 2026-06-30 |
| [e.g., Expand to [department/team]] | Seats activated | [N] seats | Customer (Champion: [name]) | 2026-07-31 |
| [e.g., Integrate with [their tool]] | Integration live and in use | [usage metric] | Shared | 2026-08-31 |
| [e.g., Achieve [business KPI]] | [metric] | [target] | Customer | End of Q3 |

**Talking point:**
> "I'd like us to end today with 3-4 goals that we're both accountable to. Not a wishlist — things with owners and dates, so when we sit down in [Q3 date] we can score ourselves honestly."

### Expansion Opportunities

*Only include this section if the account health supports it. If the account is At Risk or Critical, remove this section and focus on stabilisation.*

| Opportunity | Signal | Business case | ARR impact | Proposed next step |
|---|---|---|---|---|
| [e.g., Additional seats] | [e.g., Seat utilisation at 95%, [N] requests from unlicensed users] | [Removes bottleneck for [team], enables [outcome]] | [+$X ARR] | [Pricing conversation with [sponsor] in [month]] |
| [e.g., Add-on / module] | [e.g., Frequent feature requests for [X]] | [Would replace [current tool/process] saving [Y]] | [+$X ARR] | [Demo scheduled / offer a pilot] |

**Talking point (frame expansion as enablement, not upsell):**
> "One thing I noticed in the data is [signal]. A few of your colleagues have asked about [feature/seats] but don't have access. I'd like to understand if that's creating friction — not because I want to sell you more, but because if it's blocking [outcome], it's worth talking about."

---

## 5. Commercial Context

- **Renewal date:** [DATA NEEDED]
- **Current tier:** [DATA NEEDED]
- **Billing status:** [DATA NEEDED — any outstanding items?]
- **Pricing discussions:** [DATA NEEDED — any active negotiations?]

**If renewal is within 90 days:** Raise it directly in the meeting.
> "Your renewal comes up in [month]. I want to make sure we're aligned on value well before then, so there are no surprises. What would need to be true for this to be an easy decision for you?"

**If renewal is >90 days:** Do not lead with it. Let value drive the conversation.

---

## Agenda (60-minute meeting)

| Time | Segment | Owner | Notes |
|---|---|---|---|
| 0:00–0:05 | Welcome + agenda | CSM | Set tone: strategic, not a demo |
| 0:05–0:15 | Their update — business context | Customer | Ask: "What's changed for your team or business since we last spoke?" |
| 0:15–0:30 | Value delivered + goals scorecard | CSM | Lead with wins; address misses directly |
| 0:30–0:40 | Challenges + what we're doing | CSM | Be direct; have remediation ready |
| 0:40–0:52 | H2 goals + expansion (if healthy) | CSM + Customer | Co-create goals; don't present a fait accompli |
| 0:52–0:58 | Commit to next steps | Both | Assign owners and dates before leaving the room |
| 0:58–1:00 | Close | CSM | Confirm next QBR date |

**Opening question (get them talking first):**
> "Before I run through anything — what's top of mind for you going into H2? What does success look like for your team by the end of the year?"

**Closing question:**
> "Is there anything we didn't cover today that would change how you're thinking about the next six months with us?"

---

## Appendix

### A. Support Ticket Summary (H1 2026)

| Category | Volume | Avg resolution | P1/P2 incidents | Trend vs H2 2025 |
|---|---|---|---|---|
| [Category 1] | [DATA NEEDED] | [DATA NEEDED] | [DATA NEEDED] | [Up/Down/Flat] |
| [Category 2] | [DATA NEEDED] | [DATA NEEDED] | [DATA NEEDED] | [Up/Down/Flat] |
| Total | [DATA NEEDED] | [DATA NEEDED] | [DATA NEEDED] | [Up/Down/Flat] |

### B. Feature Adoption Breakdown

| Feature | Users active | % of licensed seats | Trend |
|---|---|---|---|
| [Core feature 1] | [DATA NEEDED] | [DATA NEEDED] | [Up/Down/Flat] |
| [Core feature 2] | [DATA NEEDED] | [DATA NEEDED] | [Up/Down/Flat] |
| [Feature with low adoption] | [DATA NEEDED] | [DATA NEEDED] | Flag for training |

### C. Product Updates Delivered (H1 2026)

*List releases relevant to Landermere's use case only. Frame as outcomes, not changelog entries.*

- [Release/feature] → [what it enabled for them]
- [Release/feature] → [what it enabled for them]

---

## Pre-meeting checklist

Before Thursday 2026-05-07:

- [ ] Pull usage metrics from analytics for H1 2026 vs H2 2025
- [ ] Pull support ticket summary and flag any P1/P2 incidents
- [ ] Confirm goals from the last QBR (check CRM notes / previous deck)
- [ ] Run `/customer-success:health-assessment` and fill Section 3
- [ ] Fill all `[DATA NEEDED]` fields — do not present with gaps
- [ ] Confirm attendees: executive sponsor attending? If not, reschedule or reset expectations
- [ ] Send agenda to customer contact 48h before the meeting
- [ ] If renewal is within 90 days, brief your manager before the meeting
- [ ] Book the Q3 QBR slot before the H1 meeting ends

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 13.0/17.0 (76%) |
| Evaluated | 2026-05-01 |
| Target duration | 157767 ms |
| Target cost | $0.4669 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires a data gathering step before writing — usage metrics, support history, health scores, business outcomes | PARTIAL | The skill wrote the document immediately with [DATA NEEDED] placeholders rather than pausing to gather data first. However, it integrates data gathering through a pre-meeting checklist ('Pull usage metrics from analytics for H1 2026 vs H2 2025', 'Pull support ticket summary', 'Run /customer-success:health-assessment') and a top-of-document note: 'Fields marked [DATA NEEDED] must be filled from CRM, product analytics, and support systems before the meeting.' Data gathering is flagged as required but is not a prerequisite step before writing. |
| c2 | Skill documents value delivered in customer outcome terms — not product usage statistics alone (e.g. "reduced report time from 4h to 20min" not "used the reports feature 340 times") | PASS | Key Wins template explicitly frames outcomes in customer terms: 'an estimated saving of [Y hours / $Z] over the half', 'Response time for [customer's KPI] dropped from [X] to [Y]'. Talking point reinforces: 'That translates directly to [business outcome they care about] — [frame it in their language, not ours].' The template explicitly avoids raw usage statistics. |
| c3 | Skill includes a forward-looking section — goals for the next quarter, not just a retrospective | PASS | Section 4 'Recommendations for H2 2026' is a full forward-looking section with a goals table (owner, measure, target, date) and an expansion opportunities table. Agenda also allocates 12 minutes to 'H2 goals + expansion (if healthy)' from 0:40–0:52. |
| c4 | Skill identifies risks and open issues — the QBR is not only a celebration of success | PASS | Section 2 'Challenges and Lessons Learned' is dedicated to honest challenge disclosure: 'Be direct. Customers know when things went wrong.' Usage Trends table notes 'If <80% [seat utilisation] — flag as risk.' Expansion section says 'If the account is At Risk or Critical, remove this section and focus on stabilisation.' Challenge talking point: 'I want to be direct about [issue]. It impacted [specific thing] and that wasn't acceptable.' |
| c5 | Skill produces a structured QBR document with distinct sections: value delivered, health summary, risks/recommendations, next steps | PASS | Document contains clearly delineated numbered sections: '1. Value Delivered This Half', '2. Challenges and Lessons Learned', '3. Health Overview', '4. Recommendations for H2 2026', '5. Commercial Context', plus a 60-minute Agenda with a 'Commit to next steps' segment. |
| c6 | Skill includes expansion or growth conversation guidance — partial credit if upsell is mentioned but not conditioned on account health | PARTIAL | Section 4 'Expansion Opportunities' includes explicit guidance and a talking point: 'One thing I noticed in the data is [signal].' The section is explicitly conditioned on health: 'Only include this section if the account health supports it. If the account is At Risk or Critical, remove this section.' This exceeds the partial-credit bar but ceiling is capped at PARTIAL. |
| c7 | Skill requires next steps with owners and dates — not a general "we'll follow up" | PASS | Goals table in Section 4 has explicit 'Owner' and 'By when' columns with example dates (2026-06-30, 2026-07-31, 2026-08-31). Talking point reinforces: 'Not a wishlist — things with owners and dates, so when we sit down in [Q3 date] we can score ourselves honestly.' Agenda allocates time to 'Commit to next steps — Assign owners and dates before leaving the room.' |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output contains only the QBR document artifact and chat response. No YAML frontmatter with name, description, or argument-hint fields appears anywhere in the captured output. The skill definition file itself is not shown. |
| c9 | Output's data gathering step lists the specific data sources needed for Landermere — usage metrics over the last 6 months, support ticket history, health scores, executive contacts attended/missed in prior QBRs, contract details ($210k ARR, 18-month tenure) | PARTIAL | Pre-meeting checklist covers: 'Pull usage metrics from analytics for H1 2026 vs H2 2025' ✓, 'Pull support ticket summary and flag any P1/P2 incidents' ✓, 'Run /customer-success:health-assessment' ✓, 'Confirm goals from the last QBR (check CRM notes / previous deck)' ✓, ARR/tenure in document header ✓. Missing: executive contacts attended/missed in prior QBRs is not listed as a data source to gather; only current meeting attendance is checked ('Confirm attendees: executive sponsor attending?'). |
| c10 | Output's value-delivered section uses customer-outcome language — e.g. "saved 12 FTE hours per week on report generation", "reduced order-processing errors by 22%" — NOT "logged in 3,400 times" or "used the dashboard 47 times" | PASS | Key Wins section template examples use outcome language: 'an estimated saving of [Y hours / $Z] over the half', 'giving [business outcome]', 'Response time for [customer's KPI] dropped from [X] to [Y]'. Usage Trends table includes 'What it means' column requiring interpretation, not raw stats. Talking point: 'frame it in their language, not ours.' |
| c11 | Output's value section quantifies outcomes with before/after metrics — not "improved efficiency", but "reduced report compilation from 4 hours to 20 minutes per report" | PASS | Win 1 example: 'Your team closed [X] more [tickets] per week in Q1 versus Q4 2024 — an estimated saving of [Y hours / $Z]'. Win 3: 'Response time...dropped from [X] to [Y] after [workflow]'. Usage Trends table has explicit 'H2 2025' vs 'H1 2026' comparison columns. The template is structurally designed for before/after quantification throughout. |
| c12 | Output's forward-looking section sets goals for the next quarter — at least 2-3 specific, measurable customer outcomes Landermere wants to achieve, not "continue using the platform" | PARTIAL | Section 4 goals table has 4 example goals with measurable outcomes (e.g., '[N] users active within 30 days', 'Integration live and in use', 'Seats activated') and specific dates (2026-06-30, 2026-07-31, 2026-08-31, End Q3). However, all are generic template examples — none are Landermere-specific goals. The criterion asks for outcomes 'Landermere wants to achieve,' which requires account-specific data the skill did not gather. |
| c13 | Output's risks/issues section is honest — flags any deteriorating signals (declining MAU, missed deadlines, executive sponsor changes) and presents them, not just successes | PARTIAL | Section 2 has a challenge table with columns for business impact, response, and status. Usage trends table notes 'If <80% [seat utilisation] — flag as risk.' Talking points instruct direct acknowledgement of misses. However, all Landermere-specific risks are [DATA NEEDED] placeholders — no actual deteriorating signals for Landermere are identified because no data was gathered. |
| c14 | Output's structure follows the named sections — Value Delivered, Health Summary, Risks/Recommendations, Next Steps — visible in the deck outline, not buried | PASS | Sections are clearly numbered and titled at top level: '1. Value Delivered This Half', '3. Health Overview' (= Health Summary), '2. Challenges and Lessons Learned' + '4. Recommendations for H2 2026' (= Risks/Recommendations), and Next Steps appear in both the goals table and the agenda segment '0:52–0:58 Commit to next steps'. All are top-level headings, not buried. |
| c15 | Output's expansion / growth conversation guidance is conditional on health — if Landermere is healthy, opportunities are surfaced; if not, expansion is held back with reasoning | PASS | Section 4 Expansion Opportunities contains an explicit conditional gate: 'Only include this section if the account health supports it. If the account is At Risk or Critical, remove this section and focus on stabilisation.' This directly conditions expansion guidance on health status. |
| c16 | Output's next steps each have an owner (named person, not "the team") and a date — at minimum 3 actionable next steps, not "we'll follow up next quarter" | PARTIAL | Goals table has 4 rows with 'Owner' and 'By when' columns and specific dates. However, owners are generic: 'Us', 'Customer (Champion: [name])', 'Shared' — not named persons. The [name] placeholder is never filled. Pre-meeting checklist has 9 specific tasks with a Thursday deadline but no named individual owners. The structure requires named owners but the template doesn't enforce them. |
| c17 | Output's deck outline is structured for a meeting (10-15 slides typical) with talking points per slide, not a Word document | PARTIAL | The chat response explicitly acknowledges the format gap: 'what I've produced is a structured brief (sections map 1:1 to slides) with talking points per section' and offers 'actual slide titles + 3-4 bullet talking points per slide (presentation-ready format rather than a reference doc)'. The output is a reference document with narrative sections, not a deck outline with numbered slides and title-plus-bullets format. Each section does include talking points, giving partial credit. |
| c18 | Output addresses 18-month tenure context — Landermere is past first-year wow factor, so the QBR should focus on year-2 value-articulation and not just feature adoption | PARTIAL | Document header notes 'Tenure: 18 months (customer since ~November 2024)'. Executive summary says 'Landermere Group is entering their second year as a customer.' Opening talking point references '18-month mark — a good moment to step back, look at what's actually moved.' However, the QBR does not explicitly frame itself as a year-2 value-articulation review distinct from year-1 feature adoption framing; there's no explicit pivot away from feature adoption to deeper strategic value for a mature account. |

### Notes

The skill produces a well-structured QBR brief with strong customer-outcome framing, explicit risk acknowledgement, health-conditioned expansion guidance, and a comprehensive pre-meeting checklist. Its main weaknesses are: (1) it writes first with [DATA NEEDED] placeholders rather than requiring a data-gathering step before writing; (2) YAML frontmatter for the skill definition is not visible in the output; (3) the format is a reference document, not a presentation-ready deck outline — the chat response acknowledges this and offers to reformat; (4) forward-looking goals and risk signals are all generic templates, not Landermere-specific; (5) next-step owners use generic labels ('Us', 'Shared') rather than named persons. The 18-month tenure context is mentioned but not meaningfully developed as a year-2 strategic framing distinct from first-year onboarding. Overall the output is useful and professionally structured but falls short on data-first discipline and presentation format requirements.
