# Creative

Scenario: A product team wants fresh ideas for reducing drop-off during user onboarding. They're stuck on a linear wizard approach and want genuinely different alternatives.

## Prompt

> /creative We're losing 60% of new users before they complete our 7-step onboarding wizard for Nexus, our project management tool. The current flow is: account setup → invite team → create first project → add tasks → connect integrations → set notifications → take a tour. Most users drop off at step 3. What are some genuinely different approaches?

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll work through the structured creative process for Nexus onboarding.

## Problem reframing

### Reframe 1 — As a user story
A person evaluating project management tools because their team is struggling with coordination, but feels overwhelmed by setup questions and configuration options, so they abandon the tool to try the next one that feels simpler.

### Reframe 2 — As a constraint  
We can't require users to complete a 7-step wizard, so what else could work?

### Reframe 3 — As an analogy
This is like consumer app first-run onboarding (Slack, Figma, Discord) because both involve unfamiliar interface, unclear initial value, decision fatigue, and high abandonment cost.

**Selected framing:** Reframe 2 (constraint-based). It reframes the problem from "how do we make the wizard better?" to "how do we get users to value without a wizard at all?" That opens the solution space much wider.

---

## Five genuinely different approaches

### Option 1: Rapid-fire micro-onboarding

**What it is:**  
Eliminate the modal wizard. User lands in their empty workspace with one visible action: "Create your first task." After they complete it, the UI surfaces the next logical action ("Invite a teammate" or "Create a project"). Still sequential, but feels organic and optional rather than mandatory.

**What's genuinely good:**
- Cuts cognitive load from "seven steps in a modal" to "one button visible"
- Shows value in <30 seconds (users see their first task created)
- Users stay in the product, not the wizard — dramatically reduces abandonment
- Defers team setup until users want it (removes friction for solos and evaluators)
- Measurably faster time-to-first-action

**Biggest risk:**  
Some users may never set up team/project structure — they stay in "lite mode." Also requires you to correctly predict what the next action should be, or you've just moved the confusion around.

**Effort:** Medium (UI/UX redesign + analytics-driven suggestion logic).  
**Reversibility:** Easy (can always show a setup prompt later).  
**Combinability:** Works perfectly with Option 5 (self-selection). Also layers cleanly with Option 4 (templates).

---

### Option 2: Solo-first onboarding

**What it is:**  
Reorder so team setup is optional and deferred. Users start as solo users, create their first task, see value immediately. Team setup is a secondary flow introduced later ("Want to collaborate?"). Respects different user journeys without penalising solo workflows.

**What's genuinely good:**
- Opens up a new user segment (solo freelancers, individuals)
- Removes a blocker for solo evaluators (no "who should I invite?" friction)
- Allows asynchronous team onboarding (individual signs up, evaluates, then brings teammates)
- Respects that many evaluation flows start solo, not team

**Biggest risk:**  
May reduce initial team size and depth (users less likely to add teammates later). Also fragments your onboarding analytics (some users take solo path, some team).

**Effort:** Medium (mostly reordering UI flows and messaging).  
**Reversibility:** Easy (prompt for team setup at any time).  
**Combinability:** Pairs naturally with Option 1 (progression unlocks team features after first task).

---

### Option 3: Gamified microflow

**What it is:**  
Transform onboarding into lightweight achievements. Each action ("Create first task," "Invite teammate," "Complete a task") earns a badge or milestone. Users don't feel like they're grinding through a checklist — they feel like they're unlocking features. Progress bars and streaks maintain momentum.

**What's genuinely good:**
- Reframes the same mandatory actions as optional rewards (psychological shift)
- Maintains engagement through game mechanics (proven to work in other products)
- Can drive desired behaviours (encourage team setup, connect integrations) through badge design
- Measurably increases time-in-product and completion likelihood

**Biggest risk:**  
If badges feel hollow, users dismiss them (risk of seeming juvenile). Also doesn't solve the underlying problem — users still need to set up teams; they just feel better about it. Over-gamification can feel manipulative.

**Effort:** Medium-to-High (achievement tracking, badge assets, notifications, streak logic).  
**Reversibility:** Easy (disable badges, revert to plain onboarding).  
**Combinability:** Layers well on top of Option 1 (gamify the micro-progression).

---

### Option 4: Template-driven defaults

**What it is:**  
On signup, offer 3-5 pre-built templates ("Personal Productivity," "Team Sprint," "Weekly Planning," "Bug Tracking"). User picks one, lands in a pre-populated workspace with sample projects and tasks. They immediately see how Nexus works (drag-drop, status changes, etc.). Zero configuration upfront.

**What's genuinely good:**
- Collapses setup time (pick a template, you're done)
- Shows product value immediately (users see a working example, not a blank canvas)
- Demonstrates features in context (drag-drop, completion, etc.) rather than explaining them
- Reduces the "what should my first project be?" cognitive block
- Can be personalised based on signup context

**Biggest risk:**  
Templates may not match the user's actual workflow, creating frustration. Sample data could feel confusing. Users may delete templates and feel lost. Requires maintaining multiple paths.

**Effort:** Low-to-Medium (create templates, seed logic; reuses existing features).  
**Reversibility:** Easy ("Start fresh" button; delete templates).  
**Combinability:** Works well with Option 1 (template provides initial structure, then micro-onboarding takes over for next actions).

---

### Option 5: Self-selection signup

**What it is:**  
At signup, ask once: "Have you used project management tools like Asana, Monday, or Jira?" Route to one of two paths. **Express** (experienced users): skip wizard, go straight to blank workspace. **Guided** (novices): a gentler 3-4 step wizard focused on core use case.

**What's genuinely good:**
- Removes all friction for ~30% of users (experienced users skip entirely)
- Lets novices access help without feeling condescended to
- Respects self-assessment (trusts users to know their needs)
- Dramatically lowers drop-off for power users
- Lowest implementation cost

**Biggest risk:**  
Users may misselect their own experience level. Creates two support paths. Doesn't solve the core problem — just routes around it for one cohort.

**Effort:** Low (routing logic + shorter wizard).  
**Reversibility:** Very easy (remove routing, everyone gets standard path).  
**Combinability:** Combines with nearly everything. Express users get minimal landing; guided users can get Option 4 (templates) or Option 1 (micro-flow).

---

## Recommended path

**Recommendation:** Option 5 (self-selection) + Option 1 (micro-onboarding for novices)

**Why this one:**
- Immediately recovers 30-40% of drop-off (experienced users skip the wizard)
- Remaining users get a progressive, un-pressured flow instead of a wall
- Low implementation cost; measurable impact in weeks
- Testable in parallel (self-selection routes people; each path can iterate independently)

**What to do first:**
1. Quick survey: ask 20-30 churned users "Did the 7-step wizard feel overwhelming?"
2. Design the self-selection question (one simple binary: "Used similar tools before?")
3. For experienced users: design minimal landing (blank workspace + optional inline tips)
4. For novices: redesign landing state for micro-flow (one action visible; next action surfaces progressively)
5. Measure: drop-off by segment, time-to-first-action, completion rate week-over-week

**What to watch for:**
- Do experienced users actually engage differently when they skip the wizard? (validates the approach)
- Do novice users progress through micro-flow, or still drop at step 3? (indicates whether the problem is the flow structure or the actions themselves)
- Do "experienced" users actually ask for help? (if high support tickets, recalibrate messaging)
- Overall drop-off trend (target: move from 60% to 40-45% in 4 weeks)

---

## Wild card: Invert the product

**Why it seems wrong:** Nexus is a project management tool. It should help users build team structure and process, not skip that work.

**Why it might be right:** The 60% drop-off at step 3 (create first project) suggests users don't feel value until deep into setup. What if the value prop were inverted?

Instead of "complete setup to unlock the tool," position as "lightweight task list that also scales to teams."

Launch with minimal core: task creation, drag-drop, completion. Team features are secondary. This shifts everything:
- Positioning: "task list that grows with you" instead of "team PM platform"
- Onboarding: no setup, just start capturing tasks
- Pricing: freemium (single user free, teams pay)
- Competition: you're fighting Todoist and Apple Reminders, not Asana

**When to revisit:** If analysis shows your drop-off cohort are people who "just want a simple list." If your actual market is solo + small team, not enterprise coordination.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/17.0 (85%) |
| Evaluated | 2026-05-04 |
| Target duration | 78081 ms |
| Target cost | $0.0717 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 analyses the problem before generating ideas — identifies who has the problem, consequences, and constraints | PASS | Reframe 1 identifies who ('a person evaluating project management tools because their team is struggling with coordination'), Reframe 3 names consequences ('they abandon the tool to try the next one that feels simpler'), and Reframe 2 states the constraint ('we can't require users to complete a 7-step wizard'). All three appear before any options are generated. |
| c2 | Step 2 produces all three reframes (user story, constraint, analogy) and states which was selected for ideation and why | PASS | Reframe 1 (user story), Reframe 2 (constraint), and Reframe 3 (analogy to consumer app onboarding) are all present. 'Selected framing: Reframe 2 (constraint-based)' is explicitly stated with reasoning: 'It reframes the problem from how do we make the wizard better? to how do we get users to value without a wizard at all? That opens the solution space much wider.' |
| c3 | Step 3 applies all five mandatory diversity techniques (inversion, extreme scale, remove constraints, cross-domain transfer, worst idea first) producing at least one option from each | FAIL | The five options cover some techniques — Option 1 (remove constraints), Option 2 (extreme scale/solo), Option 3 (cross-domain/gaming), wild card (inversion) — but there is no 'worst idea first' option anywhere in the output. None of the five main options is framed as a deliberately bad idea designed to reveal what the failure mode shows. The technique is entirely absent. |
| c4 | At least 5 options pass all three quality tests — distinct, feasible, and specific enough to act on | PASS | All five options (Rapid-fire micro-onboarding, Solo-first onboarding, Gamified microflow, Template-driven defaults, Self-selection signup) are conceptually distinct from each other, each has a plausible implementation path within an existing SaaS product, and each describes a specific mechanism (e.g., 'User lands in their empty workspace with one visible action: Create your first task'). |
| c5 | Step 4 evaluates each option with genuine pros, biggest risk, effort estimate, and reversibility | PASS | Every option includes bulleted pros, a 'Biggest risk:' paragraph, an 'Effort:' rating (e.g., 'Medium', 'Low-to-Medium', 'Medium-to-High'), and a 'Reversibility:' rating. For example, Option 3 has 'Biggest risk: If badges feel hollow, users dismiss them', 'Effort: Medium-to-High', 'Reversibility: Easy'. |
| c6 | A wild card option is included in the output — unconventional but argued seriously | PASS | The 'Wild card: Invert the product' section explicitly argues for repositioning Nexus as a 'lightweight task list that also scales to teams,' addressing competitive positioning (fighting Todoist vs Asana), pricing model (freemium), and providing a 'when to revisit' trigger condition. |
| c7 | Recommended path specifies what to do first as a concrete immediate action | PASS | 'What to do first: 1. Quick survey: ask 20-30 churned users Did the 7-step wizard feel overwhelming?' is a specific, immediately executable action naming a sample size and a specific question to ask. |
| c8 | Options named with descriptive memorable names (not "Option 1", "Option 2") | PARTIAL | Options have descriptive names ('Rapid-fire micro-onboarding', 'Solo-first onboarding', 'Gamified microflow', 'Template-driven defaults', 'Self-selection signup') but every heading is prefixed with 'Option 1:', 'Option 2:', etc. The ceiling is PARTIAL; descriptive names exist alongside the forbidden numbering pattern. |
| c9 | Output addresses step 3 (create first project) explicitly as the dropoff hotspot — at least 2 of the generated options target reducing friction at that specific step, not generic onboarding ideas | PASS | Option 4 explicitly says 'Reduces the what should my first project be? cognitive block'. The wild card says 'The 60% drop-off at step 3 (create first project) suggests users don't feel value until deep into setup.' Option 1 replaces the project-creation step with task creation as the first action, directly targeting the step 3 moment. |
| c10 | Output's inversion option flips the wizard premise (e.g. "no onboarding wizard at all — drop the user into a sample project pre-populated with their email contacts") rather than a slight tweak | PASS | The wild card 'Invert the product' states 'Instead of complete setup to unlock the tool, position as lightweight task list that also scales to teams' and 'Launch with minimal core: task creation, drag-drop, completion. Team features are secondary.' This is a full inversion of the wizard premise, not an incremental adjustment. |
| c11 | Output's extreme-scale option imagines onboarding for 10x or 0.1x users (e.g. "1,000 simultaneous account-creators in a workshop" or "single user, no team yet") and surfaces a different design implication | PASS | Option 2 'Solo-first onboarding' explicitly addresses the 0.1x case ('Opens up a new user segment (solo freelancers, individuals)') and surfaces a distinct design implication: defer team setup entirely, create a solo workflow, and 'Allows asynchronous team onboarding (individual signs up, evaluates, then brings teammates).' The single-user case matches the criterion's own example 'single user, no team yet.' |
| c12 | Output's remove-constraints option drops one of the 7 steps as non-essential (e.g. "skip integrations and notifications for week 1, prompt later in-app") with reasoning | PASS | Option 2 explicitly drops 'invite team' (step 2) as an initial requirement, with reasoning: 'Removes a blocker for solo evaluators (no who should I invite? friction)' and 'Respects that many evaluation flows start solo, not team.' Option 1 drops the entire wizard structure with reasoning about cognitive load reduction. |
| c13 | Output's cross-domain transfer option borrows a pattern from outside SaaS onboarding — e.g. how Duolingo's progressive disclosure works, how IKEA furniture instructions order steps, how a Mario tutorial level introduces mechanics | PARTIAL | Option 3 'Gamified microflow' borrows from gaming ('Badges or milestones,' 'streaks maintain momentum,' 'proven game mechanics') which is outside SaaS onboarding. However, it doesn't cite any specific non-SaaS reference (no Duolingo, IKEA, Mario or equivalent named example). The cross-domain transfer is present but shallow. |
| c14 | Output's worst-idea option is genuinely bad (e.g. "force users to invite 5 colleagues before they can do anything") and explains what the failure mode reveals — not a softened "it could work in some scenarios" | FAIL | No worst-idea option exists in the output. All five main options are presented as genuinely viable approaches with pros listed first. The wild card ('Invert the product') is unconventional but argued as a serious strategic pivot, not as a deliberately bad idea. The 'worst idea first' technique is entirely absent from the output. |
| c15 | Output produces at least 5 distinct, feasible, specific options — each has a memorable name (not "Option 1, 2, 3"), a specific mechanism, a primary risk, and an effort estimate | PASS | All five options have memorable descriptive names ('Rapid-fire micro-onboarding', 'Gamified microflow', etc.), specific mechanisms described in detail, 'Biggest risk:' paragraphs, and 'Effort:' ratings. The numbered prefix ('Option 1:') is a formatting issue but the four required elements are all present for every option. |
| c16 | Output's wild-card option is non-obvious but argued seriously — e.g. "make onboarding optional, run a Loom walkthrough instead of a wizard" — not a joke entry | PASS | 'Invert the product' includes competitive repositioning analysis (fighting Todoist vs Asana), pricing model implications (freemium), and a 'When to revisit' conditional trigger. It challenges core product positioning and is argued with genuine seriousness, not as a joke. |
| c17 | Output's recommended path names a concrete first action — "ship the sample-project-on-signup version as a 1-week experiment, measure step-3 completion against control" — not "consider trying X" | PASS | 'What to do first: 1. Quick survey: ask 20-30 churned users Did the 7-step wizard feel overwhelming?' names a specific action (survey), a specific sample size (20-30), and a specific question to ask. It is actionable immediately without further elaboration. |
| c18 | Output addresses the 60% dropoff with a hypothesis about WHY users abandon at step 3 — is creating-a-project blocked by team-not-set-up-yet, or is it the cognitive load of a real first project — and matches options to that hypothesis | PARTIAL | The wild card references 'users don't feel value until deep into setup' and Option 4 mentions 'the what should my first project be? cognitive block', which points toward cognitive load. Reframe 3 lists 'decision fatigue' as a driver. However, the output never explicitly distinguishes between the two competing hypotheses ('team-not-set-up-yet blocking progress' vs. 'cognitive load of naming/scoping a real first project') or explicitly matches each option to a tested hypothesis. The ceiling is PARTIAL. |

### Notes

The output is strong overall — it completes the reframing step cleanly, evaluates all five options with consistent structure (pros, risk, effort, reversibility), includes a seriously argued wild card, and produces a concrete recommended path. The primary gap is the complete absence of a 'worst idea first' option, which causes both c3 and c14 to fail. This is a skill-level structural miss: none of the five main options is framed as a deliberately bad idea designed to expose what the failure mode reveals. The cross-domain transfer criterion also scores only partial because Option 3 (Gamified microflow) borrows generically from 'game mechanics' without citing a specific non-SaaS reference. Options are labeled 'Option 1: Name' rather than just the name, costing the partial-ceiling c8. The WHY hypothesis about step 3 abandonment is hinted at (cognitive load, decision fatigue) but never explicitly structured as competing hypotheses with options matched to each, limiting c18 to partial. At 85.3%, the output clears the PASS threshold despite these gaps.
