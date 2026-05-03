# Usability Test Plan

Scenario: Testing whether the usability-test-plan skill requires defined research questions, participant criteria, task scenarios, and success metrics — not just a list of questions to ask.

## Prompt

> /ux-researcher:usability-test-plan for testing our new onboarding flow before we ship it — we want to know if new users can get to their first project within 10 minutes without help.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Here's the test plan. Key decisions I made:

**On the 10-minute criterion:** I split it across three consecutive tasks (sign-up → create project → add first item) so you can pinpoint *which* step burns the time, not just whether they made it. The combined T1+T2+T3 is your go/no-go clock.

**On methodology:** Moderated think-aloud rather than unmoderated — you need to know *why* users stall, not just that they do. Run unmoderated at scale once you've fixed the first-round issues.

**On participant count:** 6 (5 real + 1 pilot). Nielsen's 85% rule applies — don't wait to recruit 20. Test early, fix, re-test.

**Added a Go/No-Go Criteria section** at the bottom — since the explicit goal is "before we ship it," having clear pass/fail thresholds stops the ship/no-ship decision from becoming a negotiation after sessions.

Things to fill in before you run it: product name, staging environment URL, incentive amount, researcher name, and the exact step labels from your onboarding flow in the task scenarios.

### Artifacts written

#### `work/usability-test-plan-onboarding.md`

```
# Usability Test Plan: New User Onboarding Flow

**Date:** 2026-05-01  |  **Researcher:** [Name]  |  **Status:** Draft

---

## 1. Research Questions

| # | Question | Type | What it will tell us |
|---|---|---|---|
| RQ1 | Can new users create their first project within 10 minutes, unaided? | Behavioural | Whether the onboarding flow is shippable — this is the primary go/no-go criterion |
| RQ2 | Where do users slow down, backtrack, or stop during onboarding? | Behavioural | Which specific steps need redesign before release |
| RQ3 | Do users understand what they're being asked to do at each onboarding step? | Comprehension | Whether microcopy, labels, and instructions are clear enough |
| RQ4 | Does the onboarding flow give users enough confidence to continue without help? | Attitudinal | Whether we need in-flow support cues (tooltips, empty states, example content) |
| RQ5 | What do users expect to happen after completing the first project setup? | Attitudinal | Whether post-onboarding next steps are clear, or whether users feel abandoned |

---

## 2. Methodology

| Dimension | Choice | Rationale |
|---|---|---|
| **Moderation** | Moderated | We need to understand *why* users stall, not just *where* — think-aloud gives us this. Unmoderated can follow once we've fixed the major issues. |
| **Location** | Remote | Maximises participant pool; screen-share captures the full interaction. |
| **Protocol** | Think-aloud + task-completion | Think-aloud surfaces reasoning; task-completion gives us the binary success/failure signal we need for the 10-minute criterion. |
| **Prototype fidelity** | Live product (staging environment) | The criterion is time-to-first-project on real flows — a prototype cannot reliably measure this. |
| **Tool** | Lookback or Zoom + Observer notes | Session recording with screen + audio; dedicated note-taker tracking timestamps and errors. |

---

## 3. Participants

### Criteria

| Criterion | Requirement |
|---|---|
| **Number** | 6 participants (5 core + 1 pilot) |
| **User type** | First-time users of the product — no prior account, no prior demo |
| **Experience level** | Comfortable using web-based tools; not required to have domain expertise |
| **Tech literacy** | Can navigate a browser, fill in forms, understand standard web UI conventions |
| **Exclusions** | Current employees, contractors, beta testers, anyone who has seen the onboarding flow previously |

### Screener Questions

| # | Question | Accept | Reject |
|---|---|---|---|
| S1 | Have you used [product name] before? | No | Yes |
| S2 | How often do you use web-based productivity or project tools (e.g. Notion, Trello, Linear, Asana)? | At least monthly | Never |
| S3 | In the last 6 months, have you signed up for a new web tool and set it up yourself without IT help? | Yes | No |
| S4 | Are you currently employed by [company name] or any of its known competitors? | No | Yes |

### Recruitment

| Item | Detail |
|---|---|
| **Source** | Customer research panel, or screened via Respondent / UserInterviews |
| **Incentive** | $50 gift card (60-minute session) |
| **Timeline** | Recruit D-7 → pilot D-3 → sessions D-1 through D+2 → analysis D+5 |

---

## 4. Tasks

| # | Task | Scenario | Success criteria | Time limit | RQ |
|---|---|---|---|---|---|
| T1 | Sign up and complete account setup | "You've just heard about [product] and want to try it. Go ahead and create your account." | User reaches the main dashboard / home screen | 3 min | RQ1, RQ3 |
| T2 | Create your first project | "You want to start tracking a piece of work. Go ahead and set up your first project." | User has a named project visible in the product | 5 min | RQ1, RQ2, RQ3 |
| T3 | Add something meaningful to the project | "You've got your project — now add the first item to it, whatever that means to you." | User creates at least one item (task, document, card, etc.) within the project | 3 min | RQ1, RQ2 |
| T4 | Find out what to do next | "You've set up your first project. Where would you go from here to make progress on it?" | User articulates or navigates to a clear next step | 2 min | RQ4, RQ5 |

**Note:** T1 + T2 + T3 combined is the 10-minute benchmark. T4 tests post-onboarding orientation. Run all four consecutively without resetting — this mirrors real new-user behaviour.

---

## 5. Moderator Guide

### Introduction (5 minutes)

- Welcome and thank participant.
- Explain the purpose: "Today we're looking at a new sign-up experience. We're testing the product — not you. There are no wrong answers. Anything that's confusing is useful feedback for us."
- Confirm consent to record: "Is it okay if I record this session for our internal research team? The recording won't be shared outside the team."
- Explain think-aloud: "As you work through the tasks, please say out loud what you're thinking — what you're looking at, what you expect, what you're unsure about. It's fine to narrate even small things."
- Ask: "Any questions before we start?"

### Warm-up (3 minutes)

- "Tell me about the last time you set up a new tool at work or for personal use."
- "What made that easy or painful?"

### Tasks (30–40 minutes)

For each task:
1. Read the scenario aloud, then show it in writing on screen.
2. Start the timer when the participant begins.
3. Observe without intervening. Do not confirm whether they are on the right path.
4. Note: timestamp at start, timestamp at completion/abandon, number of wrong turns, hesitations > 5 seconds, verbal expressions of confusion or frustration.
5. If stuck for > 2 minutes with no forward movement: offer one neutral probe — "What are you looking for right now?"
6. Mark task as: Completed unaided / Completed with prompt / Abandoned.

**Between-task probes (after each task):**
- "How would you rate the difficulty of that task? 1 is very easy, 7 is very hard."
- "Was anything surprising or confusing?"
- "What did you expect to happen that didn't?"

### Debrief (10 minutes)

- "Looking back at everything — which part felt the most unclear?"
- "Was there a moment where you nearly gave up? What happened?"
- "If you could change one thing about the sign-up experience, what would it be?"
- "Is there anything you expected to see that wasn't there?"
- Thank participant and provide incentive.

---

## 6. Metrics & Analysis

### Quantitative Metrics

| Metric | Definition | Target | How measured |
|---|---|---|---|
| **Time to first project** | Seconds from landing on sign-up page to first project created (T1+T2) | ≤ 10 minutes | Moderator stopwatch from task start |
| **Task success rate** | % of participants completing each task unaided | ≥ 80% per task | Binary: completed unaided / not |
| **Error rate** | Wrong turns, backtracking, or retries per task | ≤ 2 per task | Observer count |
| **SEQ (Single Ease Question)** | "How easy was this task?" (1–7 scale) after each task | ≥ 5.5 average | Post-task verbal or written |
| **SUS (System Usability Scale)** | Post-test 10-question scale | ≥ 68 (industry average) | Post-session questionnaire |
| **Abandonment rate** | % of participants who could not complete T1+T2+T3 within 15 minutes | 0% target | Moderator log |

### Qualitative Analysis

| Method | Description |
|---|---|
| **Affinity diagramming** | Group all observations and quotes by theme across participants after all sessions |
| **Rainbow spreadsheet** | Task × Participant matrix: mark each cell as ✅ (unaided), ⚠️ (prompted), ❌ (abandoned) |
| **Frequency count** | Count how many participants encountered each distinct issue |
| **Severity rating** | Rate each issue using the scale below before writing the report |

### Severity Scale

| Level | Definition | Action |
|---|---|---|
| **Critical** | User cannot complete the task; blocks the 10-minute goal | Must fix before release |
| **Major** | User completes but takes significantly longer than 10 minutes, or requires a prompt | Should fix before release |
| **Minor** | User notices friction but works around it without losing significant time | Fix in next iteration |
| **Cosmetic** | Only noticed when pointed out; no impact on task completion | Fix if time permits |

---

## 7. Logistics

| Item | Detail |
|---|---|
| **Testing environment** | Staging environment with clean accounts (no pre-seeded data) — confirm each participant gets a fresh account |
| **Recording** | Screen + audio via Lookback or Zoom (cloud recording) |
| **Consent form** | Covers recording, anonymised research use, right to withdraw; sent in advance |
| **Session duration** | 60 minutes (5 intro + 3 warm-up + 38 tasks + 10 debrief + 4 buffer) |
| **Schedule** | Max 3 moderated sessions per day; minimum 30-minute gap between sessions |
| **Observers** | Up to 2 silent observers (product + design); use a separate observation channel, not the live session |
| **Note-taker** | Dedicated note-taker using timestamp + behaviour + quote format |
| **Pilot session** | Run D-3 with a colleague or friendly user to test task clarity, timing, and staging environment |
| **Deliverable** | Findings report with severity-rated issue list, rainbow spreadsheet, and 3–5 prioritised recommendations — due D+7 |

### Pre-session Checklist

- [ ] Staging environment reset — fresh account confirmed for each participant
- [ ] Recording software tested end-to-end
- [ ] Consent form sent and returned
- [ ] Screener confirmed for each participant
- [ ] Note-taker briefed and template ready
- [ ] Pilot session run and moderator guide adjusted

---

## Go/No-Go Criteria

The onboarding flow is ready to ship if:

| Criterion | Threshold |
|---|---|
| Time to first project (T1+T2+T3) | ≤ 10 minutes for ≥ 4 of 5 participants, unaided |
| Task success rate (T1+T2+T3) | ≥ 80% across all three tasks |
| Zero critical issues | No participant is completely blocked |
| SEQ average | ≥ 5.5 across tasks |

If any criterion is not met, fix the critical and major issues identified, then re-test with a fresh cohort of 5 participants before release.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/17.0 (94%) |
| Evaluated | 2026-05-01 |
| Target duration | 109025 ms |
| Target cost | $0.1736 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires specific research questions (what will we learn?) before methodology selection — not "we'll run usability tests and see what happens" | PASS | Section 1 'Research Questions' appears before Section 2 'Methodology' with 5 numbered RQs (RQ1–RQ5), each with 'Type' and 'What it will tell us' columns. |
| c2 | Skill requires participant screener criteria — who qualifies to participate, who should be excluded | PASS | Section 3 'Participants' has a 'Criteria' table with requirements and explicit 'Exclusions' row: 'Current employees, contractors, beta testers, anyone who has seen the onboarding flow previously.' Screener Questions table has Accept/Reject columns. |
| c3 | Skill requires task scenarios written from the user's perspective, not the product's perspective (e.g. "You've just joined a new company..." not "Navigate to onboarding") | PASS | T1: 'You've just heard about [product] and want to try it.' T2: 'You want to start tracking a piece of work.' T3: 'You've got your project — now add the first item to it, whatever that means to you.' All scenarios use second-person user framing. |
| c4 | Skill requires success metrics defined per task — completion rate, time-on-task, or error rate — not just "did they complete it" | PASS | Tasks table has 'Success criteria' and 'Time limit' per task. Section 6 specifies task success rate (≥80%), time to first project (seconds, with stopwatch), error rate (≤2 wrong turns/retries per task), and SEQ after each task. |
| c5 | Skill includes a moderator guide with specific prompts and a policy on when to intervene | PASS | Section 5 'Moderator Guide' lists warm-up prompts, between-task probes, and debrief questions verbatim. Intervention policy: 'If stuck for > 2 minutes with no forward movement: offer one neutral probe — What are you looking for right now?' |
| c6 | Skill specifies the number of participants with a rationale — not an arbitrary number | PASS | Chat response: '6 (5 real + 1 pilot). Nielsen's 85% rule applies — don't wait to recruit 20.' File specifies '6 participants (5 core + 1 pilot)' with rationale in the chat response. |
| c7 | Skill covers logistics — session duration, recording consent, tools — partial credit if logistics are mentioned but not all required elements are present | PARTIAL | Section 7 'Logistics' covers session duration (60 minutes), recording ('Screen + audio via Lookback or Zoom'), consent form ('Covers recording, anonymised research use, right to withdraw; sent in advance'), and tools (Lookback or Zoom). All key elements present. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | No skill definition file is shown in the captured output. The artifact written is the test plan document (`work/usability-test-plan-onboarding.md`) which starts with a markdown heading, not YAML frontmatter. The skill's own `.md` definition file is not present in the captured output. |
| c9 | Output's research questions are specific and testable — e.g. "Can a new user reach 'first project created' in under 10 minutes without help?" "Where in the flow do users hesitate longest?" — not "are users happy with the onboarding" | PASS | RQ1: 'Can new users create their first project within 10 minutes, unaided?' RQ2: 'Where do users slow down, backtrack, or stop during onboarding?' RQ3: 'Do users understand what they're being asked to do at each onboarding step?' All behavioural and specific. |
| c10 | Output's success metric ties to the prompt's threshold — completion rate of "reaches first project within 10 minutes" with a target (e.g. 80% of participants), plus time-on-task percentiles, and a per-step error rate | PASS | Go/No-Go: 'Time to first project (T1+T2+T3) — ≤ 10 minutes for ≥ 4 of 5 participants, unaided.' Task success rate ≥ 80% per task. Error rate ≤ 2 per task in Quantitative Metrics table. All three elements present. |
| c11 | Output's task scenarios are written from the user's perspective — "You've just signed up for Clearpath as a project manager at a consulting firm..." — NOT "Click on the onboarding wizard and complete each step" | PASS | T1: 'You've just heard about [product] and want to try it.' T2: 'You want to start tracking a piece of work.' T3: 'You've got your project — now add the first item to it, whatever that means to you.' All use second-person narrative framing, not step-navigation language. |
| c12 | Output's participant criteria specify who qualifies — e.g. "Project managers or team leads..." — and exclusions (existing customers, internal employees, friends-of-the-team) | PASS | Criteria table: 'First-time users of the product — no prior account, no prior demo', 'Comfortable using web-based tools'. Exclusions: 'Current employees, contractors, beta testers, anyone who has seen the onboarding flow previously.' Screener S4 excludes company/competitor employees. |
| c13 | Output specifies 5-8 participants per round (or equivalent qualitative number) with reasoning — Nielsen's "5 users find 80% of usability issues" cited or equivalent — not arbitrary | PASS | 6 participants (5 core + 1 pilot) specified — within 5-8 range. Chat response cites: 'Nielsen's 85% rule applies — don't wait to recruit 20. Test early, fix, re-test.' |
| c14 | Output's moderator guide names specific prompts — "What were you expecting to happen there?" "Tell me what's going through your head right now." — and a clear non-intervention policy ("don't help unless they're stuck for >2 minutes") | PASS | Specific prompts: 'Tell me about the last time you set up a new tool at work...', 'Was anything surprising or confusing?', 'What did you expect to happen that didn't?' Non-intervention: 'Observe without intervening. Do not confirm whether they are on the right path.' + '> 2 minutes with no forward movement: offer one neutral probe.' |
| c15 | Output's logistics cover session duration (typically 45-60 min), recording consent (signed before session, GDPR-aware), and tools (e.g. Maze for unmoderated, Lookback / Zoom for moderated) | PASS | Session duration: '60 minutes (5 intro + 3 warm-up + 38 tasks + 10 debrief + 4 buffer)'. Consent: 'Covers recording, anonymised research use, right to withdraw; sent in advance'. Tools: 'Lookback or Zoom (cloud recording)'. GDPR not explicitly named but 'right to withdraw' is GDPR-aligned. |
| c16 | Output's timeline includes recruitment lead time (typically 1-2 weeks), session scheduling, conducting sessions (1-2/day), and synthesis (1-2 days) | PASS | 'Recruit D-7 → pilot D-3 → sessions D-1 through D+2 → analysis D+5'. Logistics also: 'Max 3 moderated sessions per day'. Deliverable due D+7. Covers recruitment lead (D-7), sessions (D-1 to D+2), and synthesis (D+5 to D+7). |
| c17 | Output's pilot session is recommended before live participants — running 1 internal pilot to debug the test setup, task wording, and timing | PASS | Logistics: 'Pilot session — Run D-3 with a colleague or friendly user to test task clarity, timing, and staging environment.' Pre-session Checklist: '[ ] Pilot session run and moderator guide adjusted.' Timeline: pilot at D-3. |
| c18 | Output addresses incentive — typical $50-100 USD equivalent per participant for a 60-min session, with the budget implication flagged for the requester | PARTIAL | Recruitment section: 'Incentive — $50 gift card (60-minute session)' — within the $50-100 range. However, no explicit budget implication flag (e.g. total cost ~$300 for 6 participants) is surfaced to the requester. Ceiling is PARTIAL so awarding 0.5. |

### Notes

The output is exceptionally comprehensive — it covers research questions, screener criteria, user-perspective task scenarios, per-task success metrics, a full moderator guide with specific prompts and intervention policy, participant rationale citing Nielsen, detailed logistics, a timeline, pilot session recommendation, and a Go/No-Go section tied directly to the prompt's 10-minute threshold. The only gap is c8: no skill definition file with YAML frontmatter (name, description, argument-hint) appears in the captured output — only the produced test plan artifact is shown. The incentive is present ($50) but budget implication for the requester is not explicitly flagged, correctly capped at PARTIAL. The overall quality is very high, with the Go/No-Go section being a standout addition that directly addresses the 'before we ship it' framing of the prompt.
