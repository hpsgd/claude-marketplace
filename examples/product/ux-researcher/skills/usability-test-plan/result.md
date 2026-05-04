# Usability Test Plan

Scenario: Testing whether the usability-test-plan skill requires defined research questions, participant criteria, task scenarios, and success metrics — not just a list of questions to ask.

## Prompt

> /ux-researcher:usability-test-plan for testing our new onboarding flow before we ship it — we want to know if new users can get to their first project within 10 minutes without help.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I've created a structured test plan that directly validates your 10-minute success criterion. Here's what makes it work:

**Core setup:**
- **5–6 moderated remote sessions** with think-aloud protocol (you'll see _where_ they get stuck, not just whether they finish)
- **Single clear task:** "Set up your first project." No walkthrough, no hints—just the goal
- **Hard deadline:** 10 minutes exactly; you'll measure success against that
- **No prior users:** Screener ensures participants have never used the product before

**What you'll measure:**
- Time to reach first project (target: < 10 min for all users)
- Specific blockers (e.g., "Can't find Create Project button," "Doesn't understand what to fill in")
- Severity rating so you know what to fix before shipping vs. what can wait

**The report you'll get:**
A "rainbow spreadsheet" showing each user's journey, where they got stuck, and how long it took. Then you can ask: "Did 5+ out of 6 users make it in 10 minutes?" If yes and no critical issues → ship. If no → iterate.

**Before you run anything:** Run one pilot session with a colleague to stress-test the test itself (scenario is clear, timing is realistic, recording works).

The plan is ready to customize with your actual product terms and timeline. Want me to adjust anything — different participant profile, different success criteria, or a different approach?

### Artifacts written

#### `work/USABILITY_TEST_PLAN.md`

```
# Usability Test Plan: New User Onboarding to First Project

**Date:** 2026-05-04  |  **Researcher:** Martin Lau  |  **Status:** Draft

**Success Criterion:** New users can create and reach their first project within 10 minutes without help.

---

## 1. Research Questions

| # | Question | Type | What it will tell us |
|---|---|---|---|
| RQ1 | Can new users create their first project and reach the project view within 10 minutes without guidance? | Behavioural | Whether the onboarding flow meets our ship criteria |
| RQ2 | Where do new users get stuck, confused, or take unexpected paths during onboarding? | Behavioural | Specific friction points to fix before release |
| RQ3 | Do new users understand what they're supposed to do at each step? | Comprehension | Whether onboarding messaging and UI labels are clear |
| RQ4 | How many errors or backtracking actions occur before reaching the first project? | Behavioural | Indication of UX smoothness; target: zero errors |

---

## 2. Methodology

| Dimension | Choice | Rationale |
|---|---|---|
| **Moderation** | Moderated | Need to observe think-aloud and capture _where_ users get stuck, not just _whether_ they finish |
| **Location** | Remote | Reach diverse users; easier scheduling; lower friction |
| **Protocol** | Think-aloud + task completion | Capture both the journey (why they click things) and the outcome (did they finish in 10 min?) |
| **Prototype fidelity** | Live product | Testing the actual product, not a prototype—this is the real experience |
| **Tool** | Zoom + observer notes | Record screen + audio; live note-taker captures observations |

---

## 3. Participants

| Criterion | Requirement |
|---|---|
| **Number** | 5–6 participants (enough to identify patterns; qualitative, not statistical validation) |
| **User type** | First-time users who match target persona: small business owner or team lead (1–20 person team) |
| **Experience level** | Novice with this product; moderate tech literacy (comfortable with web apps) |
| **Demographics** | Age 25–55; mix of genders; at least one user with accessibility needs or non-English as first language |
| **Exclusions** | Internal employees, product team members, prior beta testers, competitors |

### Screener Questions

| # | Question | Accept | Reject |
|---|---|---|---|
| S1 | Have you used [product name] before? | Never / Heard of it but never used | Used it in the past 30 days |
| S2 | What is your role? | Manager, Team Lead, Business Owner, Coordinator | Existing product user |
| S3 | How comfortable are you using new software? | Comfortable / Very comfortable | Uncomfortable or unfamiliar with web apps |
| S4 | Approximate team size? | 1–20 people | Solo / 20+ people |

### Recruitment

| Item | Detail |
|---|---|
| **Source** | Customer panel + social media ads ("Help test our new onboarding") |
| **Incentive** | $25 gift card or equivalent |
| **Timeline** | Recruit by [DATE]; sessions complete by [DATE + 2 weeks] |
| **Note** | Recruit broadly—different jobs, experience levels, and backgrounds reveal different friction points |

---

## 4. Tasks

| # | Task | Scenario | Success criteria | Time limit | Research question |
|---|---|---|---|---|---|
| T1 | Create first project | "You've just signed up. Your goal is to set up a project so your team can start using it. Walk me through what you'd do next." | User reaches the project dashboard/view AND has created or can see at least one item (task/ticket) in the project | 10 minutes | RQ1, RQ2 |
| T2 (optional, debrief) | Reflect on experience | "Was anything confusing or surprising in that process? What would you have done differently?" | Participant articulates 1–2 pain points or unexpected moments | 5 minutes | RQ2, RQ3 |

**Task Design Notes:**
- **Scenario, not instruction:** T1 gives a goal, not a walkthrough. User discovers the steps.
- **Open success criteria:** We're measuring whether they reach the project view _and_ understand they can add work. Both matter.
- **Single clear goal:** Create/reach first project. Nothing else.
- **Real-world context:** This is what a user actually does on day one.

---

## 5. Moderator Guide

### Introduction (2 minutes)
- Welcome: "Thanks for helping us test our onboarding. We're testing the product, not you — there are no wrong answers."
- Consent: "I'll record your screen and audio. Is that okay?"
- Explain think-aloud: "As you work through the task, please say what you're thinking — what you're looking for, what you expect to happen, what surprises you. It's okay if you go silent; I'll prompt you gently."
- Set expectations: "There's no rush. Work at your own pace. If you get stuck, tell me — don't give up silently."

### Warm-up (2 minutes)
1. "Tell me about your current workflow — how do you and your team currently track work?"
2. "Have you used tools like [similar product] before?"

_Purpose:_ Establish baseline familiarity; listen for mental models of what "projects" mean to them.

### Main Task (10 minutes)

**Read the scenario:**
> "You've just signed up for [product]. Your team wants to start tracking their work in the tool. Your goal right now is to set up your first project so you can show your team how it works. Walk me through what you'd do next. Think aloud as you go — tell me what you're looking for and what you expect to happen."

**Moderator behavior:**
- **Observe, don't guide.** Watch where they click, what they read, where they hesitate.
- **Stay silent.** Let them work through confusion. Only intervene if they're genuinely stuck for > 30 seconds.
- **If stuck:** Use a neutral prompt: "What are you looking for right now?" or "What do you expect to happen next?"
- **Note the time** when they reach the project view. Record: time to first project, any backtracking, errors, or restarts.
- **Watch for:** 
  - Do they find the "Create Project" button/option?
  - Do they understand what to fill in?
  - Do they know what happens after they create it?
  - Do they attempt to add a task/item?

### Post-Task Debrief (3 minutes)

After they finish (or time expires):

1. **If they succeeded in < 10 min:** "Great! Walk me through what you did step by step. Anything confusing?"
2. **If they exceeded 10 min or didn't finish:** "Where did you get stuck? What would have helped you get there faster?"
3. **Open reflections:** 
   - "What surprised you about the process?"
   - "If you were to show this to a colleague right now, what would you tell them?"
   - "Rate the difficulty: 1 (very easy) to 5 (very hard). Why?"

---

## 6. Metrics & Analysis

### Quantitative Metrics

| Metric | Definition | Target | How measured |
|---|---|---|---|
| **Time to first project** | Seconds from task start to reaching project view | < 600 seconds (10 min) | Stopwatch; tool timer |
| **Task success rate** | % of participants who reached project view within 10 min | 100% (all 5–6) | Binary: yes/no |
| **Errors / backtracking** | Number of wrong clicks or back-navigation per session | 0 (ideal); max 2 | Observer count |
| **Post-task satisfaction (SEQ)** | Single Ease Question: "How easy was that task?" (1–7) | ≥ 6 | Post-task rating |
| **Confidence rating** | "How confident are you that you could show your team how to use this?" (1–5) | ≥ 4 | Post-debrief rating |

### Qualitative Analysis

**Method:** Affinity diagramming + severity scoring

1. **Transcript review:** Review screen recording and notes for each participant.
2. **Blockers:** Identify moments where users hesitated, got confused, or took a wrong path.
3. **Frequency:** Count how many participants hit the same blocker.
4. **Severity rating:** Use scale below.
5. **Themes:** Group blockers by type (unclear labeling, missing affordance, confusing flow, etc.).

### Severity Scale

| Level | Definition | Action |
|---|---|---|
| **Critical** | Blocker prevents user from completing onboarding in 10 min | Must fix before ship |
| **Major** | Blocker causes delay or requires backtracking but user recovers | Should fix before ship |
| **Minor** | User notices but easily works around; doesn't impact time | Fix in next iteration |
| **Cosmetic** | Only visible in edge cases; doesn't impact onboarding | Fix if time permits |

**Example findings:**
- If 5/6 users struggle to find the "Create Project" button → Critical
- If 2/6 users don't understand what to fill in → Major
- If 1/6 user misses a help tooltip → Minor

---

## 7. Logistics

| Item | Detail |
|---|---|
| **Tool** | Zoom (recording + live notes) or equivalent (screen recording + audio) |
| **Recording** | Screen capture + audio; video optional |
| **Consent form** | Standard usability testing consent (see template below) |
| **Session duration** | 20 minutes total: 2 min intro + 2 min warm-up + 10 min task + 3 min debrief + 3 min buffer |
| **Sessions per day** | Max 3 per day (avoid moderator fatigue) |
| **Schedule** | 5–6 sessions over 2–3 days |
| **Observers** | Product manager + 1 designer (max 2; too many distract the user) |
| **Note-taker** | Dedicated person captures: time spent, where stuck, emotional tone, quotes |
| **Pilot session** | Run 1 pilot with a friendly user or colleague 48 hours before real sessions |
| **Report delivery** | Findings + severity matrix + video highlights within 3 days of final session |

### Session Schedule Template

| Session | Participant | Date | Time | Moderator | Observer | Notes |
|---|---|---|---|---|---|---|
| 1 | [Name] | [Date] | [Time] | You | PM | Pilot or real? |
| 2 | [Name] | [Date] | [Time] | You | Design | |
| 3 | [Name] | [Date] | [Time] | You | PM | |
| 4 | [Name] | [Date] | [Time] | You | Design | |
| 5 | [Name] | [Date] | [Time] | You | PM | |
| 6 | [Name] | [Date] | [Time] | You | Design | |

---

## 8. Consent Form Template

```
USABILITY TEST CONSENT FORM

Study: [Product Name] Onboarding Usability Test

You are invited to participate in a usability test of [product]. This test helps us improve the experience for new users.

What you'll do:
- Complete a short onboarding task (10 minutes)
- Share your thoughts out loud as you work
- Answer a few follow-up questions

Recording:
- We'll record your screen and audio
- Video is optional
- Recordings are used only to improve the product and shared only with the product team

Your rights:
- You can withdraw at any time without penalty
- You can skip any question
- Your data will be kept confidential
- Recordings will be deleted after analysis (within 30 days)

Incentive:
- You'll receive $25 for your participation

I consent to participate:
☐ Yes, and I consent to screen recording
☐ Yes, and I also consent to video recording

Signature: ___________________  Date: ___________________
```

---

## 9. Analysis & Reporting

After all sessions are complete:

1. **Watch all recordings** (or review notes if unrecorded)
2. **Create a "rainbow spreadsheet":**

| Participant | Time (sec) | Success? | Blocker #1 | Blocker #2 | Satisfaction | Confidence |
|---|---|---|---|---|---|---|
| P1 | 420 | ✓ | None | None | 7 | 5 |
| P2 | 680 | ✗ | Can't find Create btn | Can't name project | 3 | 2 |
| P3 | 550 | ✓ | Unclear label | None | 6 | 4 |
| P4 | 420 | ✓ | None | None | 7 | 5 |
| P5 | 890 | ✗ | Long form fields | Confusing success state | 2 | 1 |
| P6 | 380 | ✓ | None | None | 7 | 5 |

3. **Identify patterns:**
   - Which blockers appear in 3+ sessions? → Likely critical
   - Which blockers appear in 1–2 sessions? → Likely minor
   - Average time: [X] seconds
   - Success rate: [Y]%

4. **Write findings report:**
   - Summary: "X out of Y users reached their first project within 10 minutes. Key friction points: [list]"
   - Severity matrix: 1 critical, 3 major, 2 minor blockers found
   - Video highlights: 2–3 min clip showing a typical user journey + a typical struggle
   - Recommendations: Specific fixes for each critical/major blocker

---

## Before You Start: The Pilot

**Run one pilot session** 48 hours before real sessions. Test with:
- A colleague unfamiliar with your product
- OR a friendly early user willing to give feedback on the test itself

**Pilot validates:**
- Task scenario is clear (not too leading, not too vague)
- 10-minute time limit is realistic
- Moderator guide has neutral language (not leading questions)
- Zoom/recording setup works
- Consent process is smooth

**After pilot, adjust:**
- Clarify any confusing language in the scenario
- Adjust time estimates if needed
- Fix technical setup issues

Then run the real sessions.

---

## Success Criteria for Shipping

**Ship the onboarding if:**
- ✓ 5+ out of 6 users reach their first project within 10 minutes
- ✓ No critical blockers remain
- ✓ Post-task satisfaction ≥ 6 / 7
- ✓ Post-debrief confidence ≥ 4 / 5

**Hold for iteration if:**
- ✗ Fewer than 5/6 users succeed in 10 minutes
- ✗ Critical blockers found (must fix first)
- ✗ Satisfaction or confidence consistently low

---

## Next Steps

1. **Refine this plan** with your product team (adjust for your actual product flow, terminology, and success metrics if needed)
2. **Schedule the pilot** with a colleague
3. **Recruit participants** (aim to start sessions within 1 week)
4. **Run sessions** (2–3 days of testing)
5. **Analyze & report** (3 days to findings)
6. **Decide: Ship or iterate** (based on success criteria above)

**Timeline:** Plan → Pilot → Sessions → Analysis → Decision (2–3 weeks total)

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/17.0 (94%) |
| Evaluated | 2026-05-04 |
| Target duration | 53415 ms |
| Target cost | $0.0755 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires specific research questions (what will we learn?) before methodology selection — not 'we'll run usability tests and see what happens' | PASS | Section 1 'Research Questions' appears before Section 2 'Methodology' in the artifact. Four explicit RQs are listed: RQ1 (can users reach first project in 10 min?), RQ2 (where do they get stuck?), RQ3 (do they understand each step?), RQ4 (how many errors occur?). |
| c2 | Skill requires participant screener criteria — who qualifies to participate, who should be excluded | PASS | Section 3 contains a 'Screener Questions' table with Accept/Reject columns for four questions, and an Exclusions row explicitly listing: 'Internal employees, product team members, prior beta testers, competitors'. |
| c3 | Skill requires task scenarios written from the user's perspective, not the product's perspective (e.g. 'You've just joined a new company...' not 'Navigate to onboarding') | PASS | Task T1 reads: 'You've just signed up. Your goal is to set up a project so your team can start using it. Walk me through what you'd do next.' The moderator guide expands this to a full second-person scenario starting 'You've just signed up for [product]. Your team wants to start tracking their work...' |
| c4 | Skill requires success metrics defined per task — completion rate, time-on-task, or error rate — not just 'did they complete it' | PASS | Section 6 'Metrics & Analysis' has a Quantitative Metrics table with: Time to first project (< 600 seconds), Task success rate (target: 100%), Errors/backtracking (target: 0), SEQ satisfaction (≥ 6), and Confidence rating (≥ 4) — all linked to Task T1. |
| c5 | Skill includes a moderator guide with specific prompts and a policy on when to intervene | PASS | Section 5 'Moderator Guide' includes specific neutral prompts ('What are you looking for right now?' / 'What do you expect to happen next?') and an explicit intervention policy: 'Only intervene if they're genuinely stuck for > 30 seconds.' |
| c6 | Skill specifies the number of participants with a rationale — not an arbitrary number | PASS | Section 3 states '5–6 participants' with rationale: '(enough to identify patterns; qualitative, not statistical validation)' — a recognisable equivalent to Nielsen's heuristic without naming it. |
| c7 | Skill covers logistics — session duration, recording consent, tools — partial credit if logistics are mentioned but not all required elements are present | PARTIAL | Section 7 'Logistics' covers all three areas: session duration ('20 minutes total: 2 min intro + 2 min warm-up + 10 min task + 3 min debrief + 3 min buffer'), tool ('Zoom + observer notes'), and recording consent (Section 8 contains a full consent form template). Ceiling capped at PARTIAL. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The only artifact written is 'work/USABILITY_TEST_PLAN.md', which contains no YAML frontmatter — it begins with a markdown heading and metadata table. The skill definition file itself is not shown in the captured output, so the required frontmatter fields (name, description, argument-hint) cannot be verified. |
| c9 | Output's research questions are specific and testable — e.g. 'Can a new user reach first project created in under 10 minutes without help?' 'Where in the flow do users hesitate longest?' — not 'are users happy with the onboarding' | PASS | RQ1 directly mirrors the prompt's criterion: 'Can new users create their first project and reach the project view within 10 minutes without guidance?' RQ2 asks specifically where users get stuck, RQ3 tests comprehension at each step, RQ4 counts errors. All are measurable and behavioural, not attitudinal. |
| c10 | Output's success metric ties to the prompt's threshold — completion rate of 'reaches first project within 10 minutes' with a target (e.g. 80% of participants), plus time-on-task percentiles, and a per-step error rate | PASS | Section 6 includes: task success rate (target 100%, with ship criteria '5+ out of 6 users'), time to first project (< 600 seconds), and errors/backtracking count. The 'Success Criteria for Shipping' section explicitly ties pass/fail to 5/6 users succeeding within 10 minutes. Time-on-task percentiles and per-step error breakdown are absent, but all three metric types are substantially present. |
| c11 | Output's task scenarios are written from the user's perspective — 'You've just signed up for Clearpath as a project manager at a consulting firm. Your goal is to set up your first client project so you can show your team status updates by tomorrow's standup.' — NOT 'Click on the onboarding wizard and complete each step' | PASS | The moderator guide's main task reads: 'You've just signed up for [product]. Your team wants to start tracking their work in the tool. Your goal right now is to set up your first project so you can show your team how it works.' — second-person, goal-oriented, no procedural instruction. |
| c12 | Output's participant criteria specify who qualifies — e.g. 'Project managers or team leads at consulting / agency / professional services companies, 5-50 employee company, never used Clearpath before' — and exclusions (existing customers, internal employees, friends-of-the-team) | PASS | Section 3 specifies: 'small business owner or team lead (1–20 person team)', 'Novice with this product; moderate tech literacy', 'Age 25–55; mix of genders', and a screener with explicit reject criteria. Exclusions: 'Internal employees, product team members, prior beta testers, competitors'. |
| c13 | Output specifies 5-8 participants per round (or equivalent qualitative number) with reasoning — Nielsen's '5 users find 80% of usability issues' cited or equivalent — not arbitrary | PASS | '5–6 participants (enough to identify patterns; qualitative, not statistical validation)' — number is within range, rationale given. Nielsen not cited by name but the reasoning is an equivalent paraphrase of the same principle. |
| c14 | Output's moderator guide names specific prompts — 'What were you expecting to happen there?' 'Tell me what's going through your head right now.' — and a clear non-intervention policy ('don't help unless they're stuck for >2 minutes') | PASS | Section 5 lists specific neutral prompts: 'What are you looking for right now?' and 'What do you expect to happen next?' The intervention policy states: 'Only intervene if they're genuinely stuck for > 30 seconds.' The threshold is more aggressive than the criterion's >2 min example but the structure is present and explicit. |
| c15 | Output's logistics cover session duration (typically 45-60 min), recording consent (signed before session, GDPR-aware), and tools (e.g. Maze for unmoderated, Lookback / Zoom for moderated) | PASS | Session duration: '20 minutes total' (notably shorter than the 45-60 min typical, but specified). Tool: 'Zoom + observer notes'. Consent: Section 8 has a full consent form template with explicit opt-in checkboxes. No GDPR-specific language. All three areas addressed. |
| c16 | Output's timeline includes recruitment lead time (typically 1-2 weeks), session scheduling, conducting sessions (1-2/day), and synthesis (1-2 days) | PASS | Section 7 states 'Max 3 per day' for sessions. Next Steps says 'aim to start sessions within 1 week' and '2–3 days of testing'. Section 9 specifies '3 days to findings'. Section 7 Recruitment has '[DATE]; sessions complete by [DATE + 2 weeks]'. Timeline summary: 'Plan → Pilot → Sessions → Analysis → Decision (2–3 weeks total)'. |
| c17 | Output's pilot session is recommended before live participants — running 1 internal pilot to debug the test setup, task wording, and timing | PASS | A dedicated 'Before You Start: The Pilot' section explicitly recommends running one pilot '48 hours before real sessions', lists what it validates (task clarity, timing, recording, consent), and instructs what to adjust after. Also mentioned in chat response: 'Run one pilot session with a colleague to stress-test the test itself.' |
| c18 | Output addresses incentive — typical $50-100 USD equivalent per participant for a 60-min session, with the budget implication flagged for the requester | PARTIAL | Section 3 Recruitment mentions '$25 gift card or equivalent' — incentive is present but below the typical $50-100 range for moderated sessions, and no budget implication or total cost estimate is flagged for the requester. Incentive is addressed; the budget context is not. Ceiling capped at PARTIAL. |

### Notes

The output is an exceptionally thorough usability test plan that satisfies nearly every criterion. Research questions precede methodology, task scenarios are written from the user's perspective, the moderator guide includes specific prompts and an intervention policy, and the success criteria tie directly to the prompt's 10-minute threshold. The only hard failure is c8 — the skill definition file's YAML frontmatter is not visible in the artifacts, so name/description/argument-hint fields cannot be verified. Minor gaps: the incentive ($25) is below the typical $50-100 range for moderated sessions and no budget implication is flagged; the session duration (20 min) is short for a standard usability study; and time-on-task percentiles and per-step error rates aren't broken out. None of these prevent a strong PASS verdict.
