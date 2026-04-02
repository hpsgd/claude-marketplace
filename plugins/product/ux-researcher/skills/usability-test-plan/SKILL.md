---
name: usability-test-plan
description: "Plan a usability test — define research questions, tasks, participant criteria, and analysis approach. Produces a structured test plan ready for execution. Use before conducting moderated or unmoderated usability testing with real users."
argument-hint: "[feature or flow to test]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Usability Test Plan

Plan a usability test for $ARGUMENTS. This skill produces a structured test plan covering research questions, methodology, participants, tasks, and analysis. Use this before running any moderated or unmoderated usability test — a test without a plan produces anecdotes, not insights.

## Step 1: Define Research Questions

Start with what you want to learn. Research questions drive every subsequent decision — methodology, tasks, participants, and analysis.

Define 3-5 specific, answerable research questions:

```markdown
### Research Questions

| # | Question | Type | What it will tell us |
|---|---|---|---|
| RQ1 | [Specific question — e.g., "Can users complete checkout without assistance?"] | Behavioural / Attitudinal | [Decision this informs] |
| RQ2 | [e.g., "Where do users get confused in the onboarding flow?"] | Behavioural | [Decision this informs] |
| RQ3 | [e.g., "Do users understand what the pricing tiers include?"] | Comprehension | [Decision this informs] |
| RQ4 | [e.g., "How does the new navigation compare to the current one?"] | Comparative | [Decision this informs] |
```

**Good research questions are:**
- Specific — "Can users find the export button?" not "Is the UI good?"
- Answerable — observable through user behaviour, not speculation
- Decision-linked — the answer changes what we build

**Output:** 3-5 research questions with types and the decisions they inform.

## Step 2: Choose Methodology

Select the testing approach based on research questions and constraints:

```markdown
### Methodology

| Dimension | Choice | Rationale |
|---|---|---|
| **Moderation** | Moderated / Unmoderated | [Why — moderated for exploration, unmoderated for scale] |
| **Location** | Remote / In-person | [Why — remote for reach, in-person for context] |
| **Protocol** | Think-aloud / Task-completion / A/B comparison | [Why — think-aloud for discovery, task-completion for benchmarking] |
| **Prototype fidelity** | Live product / High-fidelity prototype / Low-fidelity wireframe | [Why — match to development stage] |
| **Tool** | [UserTesting / Lookback / Maze / in-person with recording] | [Why — capabilities needed] |
```

**Method selection guide:**
- **Exploration** (understanding problems) → Moderated think-aloud
- **Validation** (confirming solutions) → Unmoderated task-completion
- **Benchmarking** (measuring performance) → Unmoderated with quantitative metrics
- **Comparison** (A vs B) → Within-subjects or between-subjects design

**Output:** Methodology table with rationale for each choice.

## Step 3: Define Participant Criteria

Determine who to test with and how to find them:

```markdown
### Participants

| Criterion | Requirement |
|---|---|
| **Number** | [5-8 for qualitative; 20+ for quantitative benchmarking] |
| **User type** | [Match to personas — e.g., "Small business owner, 1-10 employees"] |
| **Experience level** | [Novice / Intermediate / Expert with the product or domain] |
| **Demographics** | [Relevant demographics — age range, accessibility needs, tech literacy] |
| **Exclusions** | [Who to exclude — employees, recent participants, competitors] |

### Screener Questions

| # | Question | Accept | Reject |
|---|---|---|---|
| S1 | [Screening question — e.g., "How often do you use project management tools?"] | [Daily/Weekly] | [Never] |
| S2 | [e.g., "What is your role?"] | [Manager, Team Lead] | [Developer, Designer] |
| S3 | [e.g., "Have you used [product] before?"] | [Yes, in last 30 days] | [Never used it] |

### Recruitment

| Item | Detail |
|---|---|
| **Source** | [Customer panel / Recruitment agency / Social media / In-app intercept] |
| **Incentive** | [Amount and form — e.g., "$50 gift card"] |
| **Timeline** | [Recruitment start → sessions complete] |
```

[Nielsen's research](https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/) shows 5 participants catch approximately 85% of usability issues. Use 5 for qualitative discovery, more for quantitative benchmarking.

**Output:** Participant criteria, screener questions, and recruitment plan.

## Step 4: Design Tasks

Create realistic scenarios that map to research questions:

```markdown
### Task Design

| # | Task | Scenario | Success criteria | Time limit | Research question |
|---|---|---|---|---|---|
| T1 | [Action-oriented task name] | [Realistic context — "You want to invite a colleague to your project..."] | [Observable outcome — "User reaches the invitation confirmation screen"] | [minutes] | RQ1 |
| T2 | ... | ... | ... | ... | RQ2 |
| T3 | ... | ... | ... | ... | RQ1, RQ3 |
```

**Task design rules:**
- **Scenario, not instruction.** "You need to change your billing address" not "Click Settings, then Billing, then Edit Address"
- **One goal per task.** Compound tasks confuse analysis — split them
- **Order matters.** Start with simple tasks to build confidence, increase difficulty gradually
- **Include a deliberately difficult task.** One task should push the interface — this reveals breaking points
- **Cover all research questions.** Every RQ maps to at least one task; every task maps to at least one RQ

**Output:** Task table with scenarios, success criteria, time limits, and RQ mapping.

## Step 5: Write Moderator Guide

Script the session to ensure consistency across participants:

```markdown
### Moderator Guide

#### Introduction (5 minutes)
- Welcome and thank participant
- Explain purpose: "We're testing the [product/feature], not you — there are no wrong answers"
- Confirm recording consent
- Explain think-aloud protocol (if applicable): "Please say what you're thinking as you work through the tasks"
- Ask: "Do you have any questions before we start?"

#### Warm-up (3 minutes)
- [Background question — "Tell me about how you currently [relevant activity]"]
- [Familiarity question — "How often do you [relevant task]?"]

#### Tasks (30-40 minutes)
For each task:
1. Read the scenario aloud (or share written scenario for unmoderated)
2. Observe without intervening
3. Note: time to complete, errors, hesitations, verbal comments
4. If stuck for > [time limit]: offer one neutral prompt ("What are you looking for?")

**Follow-up probes (use after each task):**
- "What did you expect to happen there?"
- "Was anything confusing or surprising?"
- "How would you rate the difficulty of that task? (1-5)"

#### Debrief (5-10 minutes)
- "Which task was most difficult? Why?"
- "What would you change about this experience?"
- "Is there anything else you'd like to share?"
- Thank participant, provide incentive
```

**Output:** Complete moderator guide with introduction, tasks, probes, and debrief.

## Step 6: Define Metrics and Analysis Plan

Decide what to measure and how to analyse it before running sessions:

```markdown
### Quantitative Metrics

| Metric | Definition | Target | How measured |
|---|---|---|---|
| **Task success rate** | % of participants completing the task | > 80% | Binary: completed / not completed |
| **Time on task** | Seconds from task start to completion | < [target]s | Stopwatch / tool timer |
| **Error rate** | Number of wrong actions per task | < 2 per task | Observer count |
| **Satisfaction (SEQ)** | [Single Ease Question](https://measuringu.com/seq10/) — "How easy was this task?" (1-7) | > 5.5 | Post-task questionnaire |
| **System satisfaction (SUS)** | [System Usability Scale](https://measuringu.com/sus/) — post-test | > 68 (above average) | Post-test questionnaire |

### Qualitative Analysis

| Method | Description |
|---|---|
| **Affinity diagramming** | Group observations into themes across participants |
| **Severity rating** | Rate each issue: [Critical / Major / Minor / Cosmetic] |
| **Frequency count** | How many participants encountered each issue |
| **Rainbow spreadsheet** | Task × Participant matrix showing success/failure/assistance patterns |

### Severity Scale

| Level | Definition | Action |
|---|---|---|
| **Critical** | User cannot complete the task | Must fix before release |
| **Major** | User completes with significant difficulty or errors | Should fix before release |
| **Minor** | User notices but works around it | Fix in next iteration |
| **Cosmetic** | Noticed only when pointed out | Fix if time permits |
```

**Output:** Metrics table with targets, qualitative analysis approach, and severity scale.

## Step 7: Plan Logistics

```markdown
### Logistics

| Item | Detail |
|---|---|
| **Tool** | [Recording/testing platform] |
| **Recording** | [Screen + audio / Screen + audio + video / Notes only] |
| **Consent form** | [Template — covers recording, data use, withdrawal rights] |
| **Session duration** | [minutes — typically 45-60 for moderated, 15-30 for unmoderated] |
| **Schedule** | [Date range, sessions per day — max 4 moderated sessions/day to avoid fatigue] |
| **Observers** | [Who watches — product, design, engineering; max 2 observers per session] |
| **Note-taking** | [Dedicated note-taker or recording-only] |
| **Pilot session** | [Date — run one pilot to test the guide before real sessions] |
| **Deliverable** | [Report format and delivery date] |
```

Always run a **pilot session** with a colleague or friendly user before real sessions. The pilot tests your test — unclear tasks, timing issues, and technical problems.

**Output:** Logistics checklist with dates, tools, and responsibilities.

## Rules

- **Research questions drive everything.** If you cannot connect a task to a research question, remove it. If you cannot connect a research question to a decision, remove it.
- **5 participants catches 85% of usability issues.** Do not delay testing to recruit 20 people for qualitative research. Test early with 5, iterate, test again.
- **Tasks must be realistic scenarios, not instructions.** "Find how to export your data" is a scenario. "Click the gear icon and select Export" is a walkthrough. Walkthroughs test memory, not usability.
- **Never lead the participant.** "Do you think this button is hard to find?" is leading. "Tell me what you're looking for" is neutral. The moderator guide must contain only neutral probes.
- **Define analysis before running sessions.** Deciding how to analyse data after collection introduces bias. The metrics and severity scale are decided in the plan, not the report.
- **Pilot the test before running it.** An untested test plan wastes participants. Always run one pilot session.

## Output Format

```markdown
# Usability Test Plan: [Feature/Flow Name]

**Date:** [date]  |  **Researcher:** [name]  |  **Status:** [Draft/Approved/In progress/Complete]

## 1. Research Questions
[From Step 1 — 3-5 questions with types]

## 2. Methodology
[From Step 2 — moderation, location, protocol, tools]

## 3. Participants
[From Step 3 — criteria, screener, recruitment]

## 4. Tasks
[From Step 4 — scenarios with success criteria]

## 5. Moderator Guide
[From Step 5 — introduction, tasks, probes, debrief]

## 6. Metrics & Analysis
[From Step 6 — quantitative targets, qualitative approach, severity scale]

## 7. Logistics
[From Step 7 — schedule, tools, pilot, deliverables]
```

## Related Skills

- `/ux-researcher:usability-review` — heuristic evaluation without users. Use as a complement: heuristic review finds obvious issues cheaply, usability testing finds issues only real users reveal.
- `/ux-researcher:persona-definition` — participant criteria should align with defined personas. Define personas first if they don't exist.
