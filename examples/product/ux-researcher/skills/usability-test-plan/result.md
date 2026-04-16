# Usability test plan

Testing whether the usability-test-plan skill requires defined research questions, participant criteria, task scenarios, and success metrics — not just a list of questions to ask.

## Prompt

> /ux-researcher:usability-test-plan for testing our new onboarding flow before we ship it — we want to know if new users can get to their first project within 10 minutes without help.

## Output

**Usability Test Plan: New Onboarding Flow**

**Date:** 2026-04-16 | **Researcher:** [name] | **Status:** Draft

**Research questions:**

| # | Question | Type | What it will tell us |
|---|---|---|---|
| RQ1 | Can new users complete the onboarding flow without assistance and reach their first project within 10 minutes? | Behavioural | Ship/no-ship decision |
| RQ2 | Where in the flow do users pause, hesitate, or make errors? | Behavioural | Which steps to redesign |
| RQ3 | Do users understand the value of each onboarding step while completing it? | Comprehension | Copy/UX writing improvements |
| RQ4 | What is the perceived difficulty of each step? | Attitudinal | Prioritisation of post-launch fixes |

**Methodology:**

| Dimension | Choice | Rationale |
|---|---|---|
| **Moderation** | Moderated | Need to understand WHY users hesitate, not just IF they complete |
| **Location** | Remote | Reach across company sizes and geographies |
| **Protocol** | Think-aloud | Surface confusion as it happens |
| **Prototype fidelity** | Live product (staging) | Pre-ship validation — must test the real thing |
| **Tool** | Lookback | Screen + audio recording, remote facilitation |

**Participants:**

Number: 6 (Nielsen's research shows 5 participants catch ~85% of usability issues; 6 provides a buffer for no-shows)

| Criterion | Requirement |
|---|---|
| **User type** | New to Clearpath — no prior account |
| **Role** | Project manager, team lead, or operations role |
| **Tech literacy** | Comfortable with web apps; not a developer |
| **Company size** | 20–500 employees |
| **Exclusions** | Clearpath employees, current customers, participants in last 60 days, software developers |

**Screener questions:**

| # | Question | Accept | Reject |
|---|---|---|---|
| S1 | "Do you currently use Clearpath?" | No | Yes |
| S2 | "What is your primary role?" | PM, team lead, ops | Developer, designer |
| S3 | "How often do you use project management software?" | Daily/Weekly | Never |

**Tasks:**

| # | Task | Scenario | Success criteria | Time limit | RQ |
|---|---|---|---|---|---|
| T1 | Set up workspace | "You just started at a new company. They use Clearpath for project tracking. You've been sent an invite — log in and get your workspace set up." | Reaches project creation screen without help | 10 min | RQ1, RQ2 |
| T2 | Invite team members | "Your manager asked you to add two team members to the workspace." | 2 invites sent successfully | 5 min | RQ1, RQ2 |
| T3 | Create first project | "Create your first project from a template." | Project created with at least one task | 5 min | RQ1, RQ2, RQ3 |

**Moderator guide:**

Introduction (5 minutes): Welcome participant, explain purpose ("We're testing the product, not you — there are no wrong answers"), confirm recording consent, explain think-aloud protocol.

Warm-up: "Tell me about how you currently track projects at work." "How often do you use project management tools?"

Per task: Read scenario aloud. Observe without intervening. Note hesitations (>5s), backtracking, verbal confusion.

Intervention policy: Only intervene if participant is stuck for >3 minutes with no progress. Neutral prompt only: "What are you looking for right now?"

Follow-up probes (post each task):
- "What did you expect to happen when you [action]?"
- "Was anything confusing or surprising?"
- "On a scale of 1–7, how easy was that task?" (SEQ)

Debrief (5–10 min): "Which task felt hardest? Why?" "What would you change?" Thank participant, provide incentive.

**Metrics:**

| Metric | Definition | Target | How measured |
|---|---|---|---|
| Task success rate | % completing T1–T3 unassisted | ≥80% | Binary per task |
| Time on task (T1) | Seconds from task start to first project created | <600s | Stopwatch |
| Error rate | Wrong actions or backtracking per task | <2 per task | Observer count |
| SEQ | Single Ease Question per task (1–7) | ≥5.5 | Post-task questionnaire |
| SUS | System Usability Scale post-test | >68 | Post-test questionnaire |

**Logistics:**

| Item | Detail |
|---|---|
| **Tool** | Lookback (remote, think-aloud recording) |
| **Recording** | Screen + audio |
| **Consent form** | Written form emailed before session; verbal confirmation at start |
| **Session duration** | 60 minutes (tasks 20–30 min, intro + debrief 30 min) |
| **Schedule** | Max 2 sessions/day to avoid moderator fatigue |
| **Observers** | Product and design; max 2 per session |
| **Pilot session** | Run with internal colleague before first real session |
| **Deliverable** | Findings report with severity ratings within 5 days of final session |

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 criteria met (93.75%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Research questions before methodology — Step 1 is dedicated to defining research questions and explicitly precedes Step 2 (methodology selection). Rules state: "Research questions drive everything. If you cannot connect a task to a research question, remove it." Questions must specify the decision they inform.
- [x] PASS: Participant screener criteria — Step 3 requires screener questions with Accept/Reject columns, plus an explicit exclusions list. The template enforces this structure; vague participant descriptions are not sufficient.
- [x] PASS: Task scenarios from user perspective — Step 4 rules state explicitly: "Scenario, not instruction. 'You need to change your billing address' not 'Click Settings, then Billing, then Edit Address.'" The scenario framing is required; instruction-style tasks are explicitly rejected.
- [x] PASS: Success metrics per task — the task table template in Step 4 requires "Success criteria" and "Time limit" as mandatory columns per task. Step 6 requires quantitative metrics with targets (task success rate, time-on-task, error rate, SEQ, SUS) with explicit target values and how-measured columns.
- [x] PASS: Moderator guide with specific prompts and intervention policy — Step 5 is a mandatory moderator guide covering introduction, warm-up, per-task observation protocol, intervention policy (when and how to intervene), follow-up probes, and debrief. The intervention policy includes specific timing ("if stuck for > [time limit]") and the exact neutral prompt to use.
- [x] PASS: Participant count with rationale — Step 3 explicitly references Nielsen's research ("5 participants catch approximately 85% of usability issues") as the rationale. The footnote is incorporated directly into the template, making an arbitrary count non-compliant.
- [~] PARTIAL: Logistics — Step 7 is a mandatory logistics checklist covering tool, recording, consent form, session duration, schedule, observers, note-taking, pilot session, and deliverable. All required elements are present. Criterion ceiling is PARTIAL — 0.5 regardless.
- [x] PASS: Valid YAML frontmatter — name, description, and argument-hint are all present in the skill's YAML header. `user-invocable: true` and `argument-hint: "[feature or flow to test]"` are explicit.

### Notes

The pilot session is explicitly required in both Step 7 and the Rules section ("An untested test plan wastes participants"), making it one of the stronger practical elements. The metrics section goes beyond most test plan templates by including SUS post-test alongside per-task SEQ. The severity scale in Step 6 mirrors the usability-review skill's severity scale — consistency between skills is a design strength for teams using both together.
