# Result: Usability test plan

| Field | Value |
|---|---|
| **Skill** | `usability-test-plan` |
| **Plugin** | `product/ux-researcher` |
| **Prompt** | `/ux-researcher:usability-test-plan for testing our new onboarding flow before we ship it — we want to know if new users can get to their first project within 10 minutes without help.` |
| **Verdict** | PASS |
| **Score** | 16.5/17 criteria met (97%) |
| **Evaluated** | 2026-04-30 |

## Output

The following is the document this skill would produce for the given prompt.

---

# Usability Test Plan: New User Onboarding Flow

**Date:** 2026-04-30 | **Researcher:** [name] | **Status:** Draft

## 1. Research Questions

| # | Question | Type | What it will tell us |
|---|---|---|---|
| RQ1 | Can a new user reach "first project created" in under 10 minutes without assistance? | Behavioural | Informs whether the flow is ship-ready or needs redesign before launch |
| RQ2 | Where in the onboarding flow do users hesitate longest or backtrack? | Behavioural | Identifies the specific steps that need copy or UX changes |
| RQ3 | Do users understand what each onboarding step is asking them to do? | Comprehension | Reveals whether labels and instructions are clear enough without in-app help |
| RQ4 | What mental model do users bring to "creating a project" — what do they expect to happen? | Attitudinal | Flags gaps between our design assumptions and user expectations |

## 2. Methodology

| Dimension | Choice | Rationale |
|---|---|---|
| **Moderation** | Moderated | We need to understand where and why users struggle, not just whether they succeed — think-aloud gives us that |
| **Location** | Remote | Recruits faster, broader pool, no lab logistics for a pre-ship test |
| **Protocol** | Think-aloud + task-completion | Think-aloud surfaces comprehension issues (RQ3, RQ4); task-completion gives us the 10-minute metric (RQ1) |
| **Prototype fidelity** | Live staging environment | The onboarding is built — test the real thing, not a mock |
| **Tool** | Lookback (moderated remote) | Screen + camera + audio; observer room available; timestamps for time-on-task |

## 3. Participants

| Criterion | Requirement |
|---|---|
| **Number** | 6 participants (qualitative discovery round) |
| **User type** | Project managers, team leads, or operations managers at consulting, agency, or professional-services firms |
| **Experience level** | Novice to the product — never used this tool before |
| **Demographics** | 2-50 employees at company; comfortable using SaaS tools; no accessibility requirement for this round (schedule a separate accessibility session) |
| **Exclusions** | Current customers, internal employees, friends-of-the-team, anyone who participated in research in the past 60 days |

### Screener Questions

| # | Question | Accept | Reject |
|---|---|---|---|
| S1 | What is your primary job role? | Project manager, team lead, operations manager, account manager | Developer, designer, C-suite only |
| S2 | How many people work at your company? | 2-50 | 1 (sole trader), 51+ |
| S3 | Which of these project management tools have you used in the past 6 months? | Asana, Monday, Trello, Notion, spreadsheets, or none | [Our product name] — reject if they've used ours |
| S4 | Have you participated in a usability study in the past 60 days? | No | Yes |

### Recruitment

| Item | Detail |
|---|---|
| **Source** | User research panel (Respondent.io) + opt-in intercept from marketing site |
| **Incentive** | $75 AUD gift card per 60-minute session |
| **Timeline** | Recruitment opens 2026-05-05, sessions begin 2026-05-12 |

Nielsen's research shows 5 participants catch approximately 85% of usability issues. Six gives us a small buffer for no-shows and represents a first qualitative round — not a benchmark study.

## 4. Tasks

| # | Task | Scenario | Success criteria | Time limit | Research question |
|---|---|---|---|---|---|
| T1 | Create first project | You've just signed up for [product] as a project manager at a 12-person consulting firm. Your team is kicking off a new client engagement next week and you want to set up the project so you can share status updates with your team at tomorrow's standup. Go ahead. | User reaches the project dashboard with at least one project visible | 10 minutes | RQ1, RQ2 |
| T2 | Invite a team member | Your colleague Sam needs access to the project you just created. Add Sam (sam@example.com) to the project. | User reaches the "invitation sent" or "member added" confirmation state | 3 minutes | RQ2, RQ3 |
| T3 | Find where project settings live | You've decided you want to rename the project. Find out how to do that. | User navigates to project settings or equivalent rename field without being told where it is | 2 minutes | RQ2, RQ3 |

Task ordering: T1 first (core task, builds confidence), T2 second (simple follow-on), T3 third (deliberately harder — tests navigation discoverability).

## 5. Moderator Guide

### Introduction (5 minutes)

- Welcome and thank the participant
- "We're testing the product, not you — there are no right or wrong answers. If something is confusing, that's the product's problem, not yours."
- Confirm recording consent: "Are you comfortable with us recording this session for internal review? The recording won't be shared publicly."
- Think-aloud instruction: "As you work through the tasks, please say what you're thinking out loud — what you're looking at, what you expect to happen, anything that surprises you. It can feel awkward at first but it's the most useful thing you can do."
- "Any questions before we start?"

### Warm-up (3 minutes)

- "Tell me about how you currently manage projects at work — what tools do you use?"
- "How often do you set up a new project from scratch?"

### Tasks (35-40 minutes)

For each task:

1. Read the scenario aloud (hand participant the written version for longer scenarios)
2. Observe without intervening — resist the urge to help
3. Note: time to start, errors, hesitations, verbal comments, facial reactions
4. If stuck for > time limit: offer one neutral prompt — "What are you looking for?" — once only. If still stuck, move on.

**Follow-up probes (use after each task):**

- "What did you expect to happen there?"
- "Was anything confusing or surprising?"
- "How would you rate the difficulty of that task? (1 = very easy, 7 = very difficult)"

### Debrief (10 minutes)

- "Which part of the process was most difficult? Why?"
- "If you could change one thing about what you just experienced, what would it be?"
- "Did the product behave the way you expected? Were there any moments that surprised you?"
- "Is there anything you'd like to tell us that we didn't cover?"
- Thank participant, confirm incentive delivery

## 6. Metrics and Analysis

### Quantitative metrics

| Metric | Definition | Target | How measured |
|---|---|---|---|
| **Task success rate (T1)** | % of participants creating a project in < 10 min without moderator help | > 80% | Binary: completed / not completed within time limit |
| **Time on task (T1)** | Seconds from scenario read to project dashboard visible | < 600 seconds | Lookback timestamp |
| **Error rate** | Wrong actions per task (navigating to wrong section, hitting back, closing modal unintentionally) | < 2 per task | Observer tally sheet |
| **Per-task SEQ** | Single Ease Question after each task: "How easy was this task?" (1-7) | > 5.5 per task | Post-task questionnaire in Lookback |
| **Overall SUS** | System Usability Scale post-test (10-item scale) | > 68 (above average) | Post-test questionnaire |

### Qualitative analysis

| Method | Description |
|---|---|
| **Observation notes** | Dedicated note-taker logs hesitations, errors, and direct quotes per task per participant |
| **Affinity diagramming** | Group observations into themes within 24 hours of final session |
| **Frequency count** | How many of 6 participants encountered each issue |
| **Rainbow spreadsheet** | Task × Participant matrix: completed / completed with help / failed |

### Severity scale

| Level | Definition | Action |
|---|---|---|
| **Critical** | User cannot complete the task | Must fix before release |
| **Major** | User completes with significant difficulty or errors | Should fix before release |
| **Minor** | User notices a problem but works around it | Fix in next iteration |
| **Cosmetic** | Only noticed when pointed out | Fix if time permits |

## 7. Logistics

| Item | Detail |
|---|---|
| **Tool** | Lookback (moderated remote) |
| **Recording** | Screen + audio + webcam for 6 sessions |
| **Consent form** | Signed before session begins — covers recording, data use, withdrawal rights, GDPR-compliant retention (delete after 90 days) |
| **Session duration** | 60 minutes per participant |
| **Schedule** | 2026-05-12 to 2026-05-14, max 2 sessions per day to avoid moderator fatigue |
| **Observers** | Product manager + one designer; max 2 in observer room; cameras off, microphones muted |
| **Note-taking** | Dedicated note-taker (second researcher or trained designer) so moderator stays present |
| **Pilot session** | 2026-05-11 — internal colleague who matches the target profile; used to test task wording, timing, and Lookback setup |
| **Deliverable** | Slide deck + severity-ranked issues table delivered 2026-05-18 |

---

## Criteria results

### Criteria (skill definition)

- [x] PASS: Skill requires specific research questions before methodology selection — Step 1 defines 3-5 specific, answerable research questions with types and a "What it will tell us / Decision this informs" column before Step 2 (Methodology). The rules section reinforces: "Research questions drive everything. If you cannot connect a research question to a decision, remove it."
- [x] PASS: Skill requires participant screener criteria — Step 3 includes a Participants table with an explicit "Exclusions" row and a Screener Questions table requiring Accept/Reject columns per question.
- [x] PASS: Skill requires task scenarios written from the user's perspective — Step 4 names this as a rule ("Scenario, not instruction") and contrasts a correct example against an instruction-style wrong one.
- [x] PASS: Skill requires success metrics defined per task — the task table in Step 4 requires a "Success criteria" column and a "Time limit" per task. Step 6 defines task success rate, time on task, and error rate with explicit targets and measurement methods.
- [x] PASS: Skill includes a moderator guide with specific prompts and an intervention policy — Step 5 provides a full script: introduction, warm-up, three named follow-up probes, and an explicit non-intervention rule with timing ("If stuck for > [time limit]: offer one neutral prompt").
- [x] PASS: Skill specifies participant numbers with a rationale — Step 3 gives "5-8 for qualitative; 20+ for quantitative benchmarking" and cites Nielsen's research (5 participants catch ~85% of usability issues).
- [~] PARTIAL: Skill covers logistics — all three required elements are present: session duration ("typically 45-60 for moderated, 15-30 for unmoderated"), recording consent (consent form template covering recording, data use, and withdrawal rights), and tools. Full coverage within the PARTIAL ceiling.
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — all three fields are present and populated.

### Output expectations

- [x] PASS: Output's research questions are specific and testable — RQ1 directly encodes the prompt's 10-minute threshold as a testable question; RQ2-RQ4 name specific behaviours and comprehension gaps, all linked to decisions.
- [x] PASS: Output's success metric ties to the prompt's threshold — T1 success criterion is "project dashboard visible within 10 minutes without moderator help," target > 80% completion rate, with time-on-task < 600 seconds and per-step error rate < 2.
- [x] PASS: Output's task scenarios are written from the user's perspective — T1 scenario ("You've just signed up... Your team is kicking off a new client engagement next week...") follows the contextual-framing pattern, not instruction-style.
- [x] PASS: Output's participant criteria specify who qualifies and who is excluded — Participants table covers role, company size, tool experience, and an explicit Exclusions row; screener questions have Accept/Reject columns.
- [x] PASS: Output specifies 6 participants (within the 5-8 range) with reasoning — Nielsen citation included, round described as "first qualitative round, not a benchmark study."
- [x] PASS: Output's moderator guide names specific prompts and a non-intervention policy — three named probes ("What did you expect to happen there?", "Was anything confusing or surprising?", "How would you rate the difficulty?") and explicit rule: "offer one neutral prompt — 'What are you looking for?' — once only."
- [x] PASS: Output's logistics cover session duration (60 min), recording consent (GDPR-aware pre-session form), and tools (Lookback).
- [~] PARTIAL: Output's timeline covers recruitment start (2026-05-05), session dates (2026-05-12-14), and deliverable date (2026-05-18) — but synthesis as a distinct phase (1-2 days post-sessions) is not explicitly called out. The deliverable date implies it but the template doesn't reserve it as a named phase.
- [x] PASS: Pilot session is recommended and included — "2026-05-11 — internal colleague who matches the target profile; used to test task wording, timing, and Lookback setup."
- [x] PASS: Output addresses incentive — "$75 AUD gift card per 60-minute session" with the budget implication visible to the requester.

## Notes

The skill is tightly structured. Research questions gate methodology, tasks must map to research questions, and analysis metrics are defined before sessions run — the sequencing enforces rigour without needing a rule to state it.

The one gap across both criteria and output is synthesis lead time. The logistics table includes a "Schedule" row for session dates and a "Deliverable" date, but there is no named phase between "last session" and "report delivered" where synthesis happens. A researcher following the template would know sessions end 2026-05-14 and the report is due 2026-05-18, but the 4-day gap isn't structured as "2 days synthesis + 2 days writing." For a first-time researcher, that's a planning blind spot.

The SEQ + SUS combination in the metrics section is stronger than most test plan templates include. Pairing the single-ease per-task score with the post-test system score gives both granular and holistic signal. The severity scale mirrors the usability-review skill, which means teams using both skills together get consistent language from evaluation through to testing.
