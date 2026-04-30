# Result: Write JTBD

**Verdict:** PARTIAL
**Score:** 16/18.5 criteria met (86%)
**Evaluated:** 2026-04-30

---

## Output

Simulated output for the prompt: `/product-owner:write-jtbd for the reporting and analytics area of our project management tool, focusing on how operations directors use our data.`

---

# Jobs-to-be-Done Analysis: Reporting & Analytics — Operations Directors

## Job Performer

| Field | Description |
|-------|-------------|
| **Performer** | Operations director at a mid-market company (150–800 employees), accountable for delivery outcomes across 6–15 concurrent projects, no dedicated PMO function |
| **Triggering context** | Weekly exec team meeting is 48 hours away; status has not been compiled yet; three project leads have not updated their trackers |
| **Current solution** | Manual spreadsheet rollup — pulling status from individual project trackers into a master Excel file, copying screenshots into a PowerPoint deck |
| **Frequency** | Weekly for exec reporting; ad hoc for board packs, investor updates, and project steering meetings |
| **Emotional state** | Anxious and time-pressured — dreads the compilation process, worried they will miss something that surfaces as a surprise in the meeting |

## Core Functional Job

> When I need to report portfolio status to my exec team,
> I want to pull together a reliable cross-project view without manual data compilation,
> so I can communicate delivery confidence and surface risks before they become surprises.

## Related Jobs

### Functional

| Sequence | Job Statement | Relationship |
|----------|---------------|--------------|
| Before | When I know an exec meeting is upcoming, I want to confirm which projects need status updates, so I can chase the right people with enough lead time | Precondition — data quality depends on timely updates from project leads |
| During | When I am reviewing portfolio status, I want to drill into a flagged project to understand the root cause of a delay, so I can speak to it with confidence rather than escalating to the project lead live in the meeting | Happens alongside core job — depth behind the summary |
| After | When I have presented to the exec team, I want to distribute a written summary to stakeholders who were not in the room, so I can ensure alignment without scheduling follow-up meetings | Follow-up — extends the reporting job into async distribution |

### Emotional

- I want to feel in control of portfolio outcomes when preparing for exec reporting
- I want to feel confident that the numbers I am presenting are accurate and current
- I want to avoid feeling caught off-guard by a project going red that I did not know about
- I want to avoid feeling embarrassed in front of the exec team when I cannot explain a project's status

### Social

- I want to be seen as the operations leader who has the answers — not the one who needs to check and come back
- I want to be seen as proactive by my CEO — someone who surfaces problems before they escalate
- I want to avoid being seen as the person who was the last to know about a project slipping

## Desired Outcomes

| # | Job | Outcome Statement | Importance (1–10) | Current Satisfaction (1–10) | Opportunity Score | Classification |
|---|-----|-------------------|-------------------|-----------------------------|-------------------|----------------|
| 1 | Core | Minimise the time it takes to compile a cross-project status view for exec reporting | 9 | 2 | 9 + max(9−2, 0) = **16** | Underserved |
| 2 | Core | Minimise the likelihood of presenting inaccurate data due to stale project updates | 9 | 3 | 9 + max(9−3, 0) = **15** | Underserved |
| 3 | Core | Increase the confidence that red/amber flags are visible before the exec meeting rather than discovered during it | 10 | 2 | 10 + max(10−2, 0) = **18** | Underserved |
| 4 | Core | Minimise the number of follow-up questions to project leads needed before producing a portfolio summary | 8 | 4 | 8 + max(8−4, 0) = **12** | Borderline underserved |
| 5 | Core | Increase the ability to drill into a project's data without switching tools or requesting exports | 8 | 2 | 8 + max(8−2, 0) = **14** | Underserved |
| 6 | Core | Minimise the effort required to produce different views for different audiences (exec vs board vs project team) | 7 | 3 | 7 + max(7−3, 0) = **11** | Adequately served |
| 7 | Core | Increase the confidence that data is current — not cached from yesterday or last week | 9 | 3 | 9 + max(9−3, 0) = **15** | Underserved |
| 8 | Core | Minimise the likelihood of missing a project that is trending toward late delivery | 9 | 4 | 9 + max(9−4, 0) = **14** | Underserved |
| 9 | Related (before) | Minimise the time spent chasing project leads for status updates before a reporting cycle | 8 | 3 | 8 + max(8−3, 0) = **13** | Underserved |
| 10 | Related (during) | Increase the ability to export a clean summary for distribution without reformatting | 7 | 4 | 7 + max(7−4, 0) = **10** | Adequately served |
| 11 | Related (after) | Minimise the time between presenting in the meeting and distributing a written summary to absent stakeholders | 6 | 5 | 6 + max(6−5, 0) = **7** | Adequately served |
| 12 | Core | Minimise the likelihood of data accuracy issues caused by manual copy-paste between tools | 8 | 2 | 8 + max(8−2, 0) = **14** | Underserved |

## Hiring / Firing Criteria

### Hiring (switching triggers)

| Trigger | Description | Concrete Example |
|---------|-------------|------------------|
| **Push** | Spreadsheet rollup broke down at scale — too many projects, too many people updating the same file, version conflicts every week | "We hit 12 active projects and the master tracker became unusable — two people overwrote each other's updates on the same day I needed to present" |
| **Pull** | Saw a demo where cross-project status populated automatically from project-level data, saving the manual compilation step | "A peer at a similar company said they went from 4 hours of prep to 20 minutes — that was the moment I booked a trial" |
| **Anxiety** | Fear of losing historical reporting data accumulated over 2+ years in spreadsheets | "We have 18 months of weekly status history in Excel — I am worried that disappears if we migrate" |
| **Habit** | Finance and the exec team are used to the existing PowerPoint format — switching the output format feels like a political battle | "My CFO has a specific slide format they want — I do not know if a new tool will let me match it" |

### Firing (churn triggers)

1. Data freshness failure — project leads stopped updating in the tool, so the portfolio view became stale; the ops director reverted to manual tracking because it was more reliable. **Sudden.**
2. Missing mobile access — exec team started reviewing status on phones between meetings; the tool had no usable mobile experience, making it useless for the audience that mattered most. **Gradual.**
3. Export limitations — the ops director needed a specific format for board packs; the tool's export produced an unusable layout requiring 90 minutes of reformatting each time. **Gradual.**
4. Lack of cross-project drill-down — the summary level was fine, but when the CEO asked a follow-up question about a specific project, the ops director could not get to the answer in the tool during the meeting. Lost credibility once, switched tools within 3 months. **Gradual.**
5. Pricing model shift — vendor moved from per-seat to per-project pricing; costs tripled overnight for a portfolio of 14 projects. **Sudden.**

## Product Implications

### Opportunity Landscape

| Category | Outcomes |
|----------|----------|
| **Underserved** (score >12) | Time to compile portfolio view; data accuracy / staleness; early visibility of red flags; ability to drill into project data; data currency (freshness); missing projects trending late; chasing updates from leads; copy-paste accuracy errors |
| **Adequately served** (6–12) | Multi-audience views; export quality; post-meeting distribution speed |
| **Overserved** (<6) | None identified at this level |

### Recommendations

**What to build — ranked by opportunity score:**

| Outcome (Underserved) | What to Build | Success Metric |
|-----------------------|---------------|----------------|
| Early visibility of red flags (score 18) | Automated risk surface — projects trending late highlighted before the reporting cycle, not during it | % of red flags visible 24h+ before weekly exec meeting |
| Time to compile portfolio view (score 16) | Auto-aggregated portfolio dashboard pulling live project data — zero manual compilation | Time from login to shareable portfolio view (target: under 5 minutes) |
| Data currency (score 15) | Real-time sync indicator per project — show data age; alert ops director when a project has not updated in >48h | % of projects with data currency <24h at time of exec meeting |
| Data accuracy — staleness (score 15) | Automated staleness detection with escalation nudge to project leads | Reduction in "last updated >7 days ago" rate at time of reporting |
| Drill-down capability (score 14) | Project-level detail accessible from portfolio summary in ≤2 clicks | Time to retrieve root-cause detail from portfolio view |
| Trending-late detection (score 14) | Predictive delivery risk — flag projects where velocity data indicates slippage before the milestone is missed | Reduction in surprises: projects that miss a milestone without a prior flag |

**What NOT to build (deprioritise):**

- Post-meeting distribution workflows — adequately served; optimising further yields diminishing returns
- Complex multi-format exports — worth maintaining parity, not a differentiation opportunity at current satisfaction levels

---

## Results

### Criteria (skill definition check)

- [x] PASS: Skill requires a core functional job statement in the canonical format: "When I [situation], I want to [motivation], so I can [outcome]" — met: Step 2 defines the exact three-part format and states "Write exactly one core functional job"
- [x] PASS: Skill requires emotional jobs AND social jobs — met: Step 3 covers both as separate required categories with their own templates, reinforced by "Do not skip emotional and social jobs"
- [x] PASS: Skill requires an outcome table with Importance, Current Satisfaction, and Opportunity Score columns — met: Step 4 defines the table with all three columns and an example row
- [x] PASS: Skill defines the Opportunity Score formula with underserved/overserved thresholds — met: formula is `Importance + max(Importance - Satisfaction, 0)`, thresholds stated as >12 (underserved) and <6 (overserved)
- [x] PASS: Skill requires hiring and firing criteria — met: Step 5 covers both directions with a Push/Pull/Anxiety/Habit table for switching triggers and a top-5 firing moments list with sudden/gradual classification
- [x] PASS: Skill prohibits solution-specific job statements — met: the Rules section explicitly calls out `"I want to use the dashboard"` as wrong, with an explanation and a corrected alternative
- [~] PARTIAL: Skill requires at least 8 outcome statements for the core job — partially met at full credit ceiling (PARTIAL type): Step 4 states "Write at least 8 outcomes for the core job" — minimum is specified, but the PARTIAL ceiling applies regardless
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — met: all three fields present in the frontmatter block

### Output expectations (simulated output check)

- [x] PASS: Output's core functional job is in the canonical format — met: the simulated core job follows "When I… I want to… so I can…" and is solution-agnostic (no mention of dashboard, module, or feature)
- [x] PASS: Output identifies the operations director as the JTBD performer with context — met: performer table specifies mid-market operations director, portfolio of 6–15 projects, no PMO, weekly exec reporting trigger
- [x] PASS: Output produces emotional jobs AND social jobs — met: four emotional jobs and three social jobs listed, both categories present
- [x] PASS: Output's outcome table has at least 8 rows — met: 12 outcome rows produced, 8+ for core job
- [x] PASS: Output's Opportunity Scores are computed via the formula with math shown — met: each row shows the arithmetic inline (e.g. `9 + max(9−2, 0) = 16`) and applies the correct thresholds
- [~] PARTIAL: Output's hiring criteria name concrete switching triggers — partially met: Push and Pull entries include specific concrete examples; Anxiety and Habit examples are concrete but slightly generic; the skill does not require this level of specificity, so some entries could be vaguer in a compliant output
- [x] PASS: Output's firing criteria name what causes operations directors to switch away — met: five firing moments listed, each with sudden/gradual classification and a concrete incident
- [x] PASS: Output is solution-agnostic — met: all job statements and outcomes describe desired future states independent of the product; no references to "the analytics module" or "the dashboard"
- [x] PASS: Output addresses the data dimension explicitly — met: data freshness, data accuracy, data currency, drill-down capability, and copy-paste accuracy errors each appear as explicit outcomes
- [~] PARTIAL: Output addresses team-level vs portfolio-level outcomes — partially met: portfolio framing is clear throughout (cross-project view, portfolio dashboard, portfolio summary); the distinction between portfolio-level and team-level is implicit rather than stated explicitly

## Notes

The skill is methodologically solid. It references both Christensen (JTBD theory) and Ulwick (Outcome-Driven Innovation), the Opportunity Score formula is precise with correct thresholds, and the prohibition on solution-specific statements is reinforced in both the per-step rules and the final Rules section.

The main structural gap: the skill models concrete examples in Step 5 (Push: "My spreadsheet broke when we hit 10,000 rows") but does not require that level of specificity in the output. A compliant output could produce vague hiring triggers while still satisfying the skill definition.

One dead reference: the final line points to `templates/jtbd-canvas.md` as the output structure, but this template is not validated or provided within the skill. If absent, the reference is a dead end and a compliant agent may not produce the expected output shape.

The skill's instruction to "Write the output to a file: `docs/jtbd-[area].md`" is functional for invocable skills but assumes the `docs/` directory exists — no guard or directory-creation step is included.
