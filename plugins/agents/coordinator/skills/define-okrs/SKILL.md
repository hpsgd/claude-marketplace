---
name: define-okrs
description: Define OKRs (Objectives and Key Results) for a product initiative, quarter, or team. Enforces baselines, measurement methods, and the 70% completion target philosophy.
argument-hint: "[initiative, quarter, or team to define OKRs for]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

Define OKRs for $ARGUMENTS.

Follow every step below. OKRs without baselines and measurement methods are useless — this process ensures every OKR is actionable.

---

## Step 1: Understand the Context

Before writing any OKRs, establish:

1. **Time horizon**: What period do these OKRs cover? (Quarter is standard. Shorter for sprints, longer for annual planning.)
2. **Scope**: Is this for a product, a team, a specific initiative, or the whole company?
3. **Parent OKRs**: Do these ladder up to a higher-level objective? If so, read and reference it. Every team OKR should visibly connect to a company or department objective.
4. **Current state**: What happened last period? Which OKRs were hit, missed, or abandoned? This context prevents repeating failed approaches.

---

## Step 2: Write Objectives

Each objective must meet ALL of these criteria:

### Objective Rules

1. **Qualitative, not quantitative.** Objectives describe the desired future state in human language. Numbers go in Key Results, never in Objectives.
   - Bad: "Increase NPS from 32 to 50"
   - Good: "Become the product customers actively recommend to peers"

2. **Inspiring and memorable.** If you cannot remember the objective without looking it up, it is too bland. Objectives should create energy.
   - Bad: "Improve platform reliability"
   - Good: "Make downtime a distant memory for our customers"

3. **Time-bound by the OKR period.** The objective should be achievable within the quarter (or whatever period is set). Multi-quarter objectives belong one level up.

4. **Outcome-oriented, not activity-oriented.**
   - Bad: "Launch the new onboarding flow" — that is an activity
   - Good: "Make new users productive on day one" — that is an outcome

5. **Limited to 2-4 objectives per team per quarter.** More than 4 means nothing is truly a priority. If you have more than 4 candidates, force-rank and cut.

### Anti-Patterns for Objectives
- Business-as-usual dressed up as an objective ("Keep the site running")
- Objectives that are actually key results ("Reduce churn by 20%")
- Objectives so broad they could mean anything ("Be world-class")
- Objectives that no one would disagree with ("Deliver value to customers")

---

## Step 3: Write Key Results

Each objective gets 3-5 Key Results. Fewer than 3 means the objective is not well-defined. More than 5 means the objective is too broad — split it.

### Key Result Rules

1. **Quantitative with a specific number.** Every KR has a metric, a baseline, and a target.
   ```
   KR: Reduce median time-to-first-value from 14 minutes to 4 minutes
        ↑ metric                              ↑ baseline    ↑ target
   ```

2. **Baselines are mandatory.** A target without a baseline is a guess, not a goal.
   - If the baseline is known, state it with the data source: "Current: 14 min (measured via Mixpanel, Q4 average)"
   - If the baseline is unknown, the FIRST Key Result must be: "Establish baseline measurement for [metric] by [date]" — this is the only acceptable non-numeric KR

3. **Outcomes, not outputs.**
   - Output (bad): "Ship 3 new features"
   - Outcome (good): "Increase weekly active usage from 45% to 65%"
   - The distinction: outputs are things you control. Outcomes are the results of those things. OKRs measure outcomes.

4. **70% completion = success.** Targets should be ambitious enough that achieving 70% represents a strong result. 100% means you set the bar too low. Below 50% means the target was unrealistic or the approach was wrong.

5. **No binary KRs.** "Launch feature X" is binary — it is either done or not. Convert to: "Feature X adopted by 30% of eligible users within 4 weeks of launch."

6. **Include the measurement method.** For each KR, state exactly how it will be measured:
   - What tool or data source?
   - What query or report?
   - Who is responsible for measuring?
   - How often is it measured?

### Leading vs. Lagging Indicators

Every set of Key Results should include both:

**Leading indicators** — things that change quickly and predict future outcomes:
- Feature adoption rate (first week)
- Funnel conversion at a specific step
- Support ticket volume for a specific category
- User engagement frequency

**Lagging indicators** — things that confirm the outcome but take time to materialise:
- Retention rate (needs 30-90 days)
- Revenue impact (needs a full billing cycle)
- NPS or satisfaction score (needs a survey cycle)
- Churn rate (needs months to stabilise)

A good OKR set has at least one leading KR (so you can course-correct early) and at least one lagging KR (so you know if the outcome was real).

---

## Step 4: Validate the OKR Set

Run every OKR through this checklist:

### Objective Validation
- [ ] Qualitative — no numbers in the objective
- [ ] Inspiring — would motivate the team if read aloud
- [ ] Achievable within the time period — not multi-quarter
- [ ] Outcome-oriented — describes the future state, not activities
- [ ] Distinct — does not overlap significantly with another objective

### Key Result Validation
- [ ] Has a specific metric with a number
- [ ] Baseline is stated (or first KR is to establish it)
- [ ] Target follows the 70% rule — ambitious but not absurd
- [ ] Measures an outcome, not an output
- [ ] Measurement method is documented (tool, query, frequency, owner)
- [ ] Not binary — has a spectrum of achievement
- [ ] Mix of leading and lagging indicators across the KR set

### Set-Level Validation
- [ ] 2-4 objectives total (no more)
- [ ] 3-5 key results per objective
- [ ] KRs across objectives do not contradict each other
- [ ] The set covers both growth AND health (do not optimise one at the expense of the other)
- [ ] At least one KR is a guardrail metric (something that should NOT get worse while you pursue the others)

---

## Step 5: Define the Scoring Framework

At the end of the period, each KR is scored on a 0-1 scale:

| Score | Meaning |
|-------|---------|
| 0.0 | No progress |
| 0.3 | Some progress but fell well short |
| 0.5 | Made meaningful progress, hit roughly half the target |
| 0.7 | Strong result — this is the expected "good" outcome |
| 1.0 | Fully achieved — target may have been too easy |

**Team OKR score** = average of all KR scores. A team score of 0.6-0.7 indicates healthy ambition and strong execution.

---

## Output Format

```markdown
# OKRs: [Team/Initiative] — [Period]

**Context:** [1-2 sentences on what happened last period and what is driving this period's focus]

**Parent objective:** [Reference to the company/department OKR this ladders up to, if applicable]

---

## Objective 1: [Qualitative, inspiring statement]

| KR | Metric | Baseline | Target | Measurement | Type |
|----|--------|----------|--------|-------------|------|
| KR1 | [Metric name] | [Current value + source] | [Target value] | [Tool, query, frequency] | Leading |
| KR2 | [Metric name] | [Current value + source] | [Target value] | [Tool, query, frequency] | Lagging |
| KR3 | [Metric name] | [Current value + source] | [Target value] | [Tool, query, frequency] | Guardrail |

**Why this objective:** [2-3 sentences on why this matters now]

**Key initiatives (inputs, not measured):** [What the team plans to do to move these KRs — listed for context, not as commitments]

---

## Objective 2: [Qualitative, inspiring statement]

[Same format]

---

## Risks and Dependencies
- [Risk or dependency that could affect achievement]
- [Risk or dependency that could affect achievement]
```

Write the output to a file: `docs/okrs-[team-or-initiative]-[period].md`.
