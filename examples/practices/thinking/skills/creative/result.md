# Creative

Scenario: A product team wants fresh ideas for reducing drop-off during user onboarding. They're stuck on a linear wizard approach and want genuinely different alternatives.

## Prompt

> /creative We're losing 60% of new users before they complete our 7-step onboarding wizard for Nexus, our project management tool. The current flow is: account setup → invite team → create first project → add tasks → connect integrations → set notifications → take a tour. Most users drop off at step 3. What are some genuinely different approaches?

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Problem Reframing

**Problem as stated:** 60% of users abandon a 7-step onboarding wizard before completing it; most drop at step 3 (create first project).

**Who has this problem:** A team lead or solo PM who signed up to evaluate whether Nexus can replace their current tool — they're time-poor, skeptical, and need to see value before they commit mental energy to setup.

**Why it matters:** Users who don't activate don't retain. Every dropped user is wasted acquisition spend and a missed chance at word-of-mouth.

**What's been tried:** A linear, sequential wizard that gates the product behind 7 completion steps.

**Constraint inventory:** Team-based product, current 7-step sequence, drop-off specifically at the first step requiring real creative/cognitive investment (naming and scoping a project).

---

## 1. Problem Reframing

### Reframe 1 — As a user story
"A team lead who needs to know if Nexus will work for their team, because they're evaluating tools under time pressure, but currently must invent a project from scratch on a blank canvas before they've seen a single thing the tool actually does."

### Reframe 2 — As a constraint
"We can't ask users to create something valuable from scratch before showing them what valuable looks like — so what else could work?"

### Reframe 3 — As an analogy
"This is like a cooking class that makes you buy all the ingredients, chop the vegetables, and heat the pan before you've tasted a single bite. The class might be wonderful, but you've already lost half the students before the food appears."

**Selected framing: Reframe 2.** It directly attacks the core assumption hidden in the current flow — that users are willing to invest creative energy before experiencing value. Reframes 1 and 3 are consistent with it, but Reframe 2 produces the widest solution space because it forces the question: *what else could work instead of blank-canvas creation?*

---

## 2. Options

---

### Option 1: Delete to Fit

**Description:** Users arrive at a fully-configured workspace — not a wizard, not an empty canvas. A sample project is already created with realistic tasks, fake team members, connected integrations, and configured notifications. Onboarding becomes: "Does this look right? Keep what fits, delete or rename what doesn't." The first interaction is *editing* not *creating*.

**What's genuinely good about it:**
- Deletion and modification require less cognitive load than creation from scratch — this is well-established in UX research
- It shows users what a well-configured Nexus workspace *looks like*, teaching by example
- Every user immediately sees a populated, functional-looking product — the value proposition is visible in seconds

**Biggest risk:**
- If the sample project feels irrelevant to the user's domain (a software team sees a marketing campaign project), they disengage faster than a blank canvas
- Requires multiple high-quality templates segmented by role/industry, or a way to select the right one upfront

**Effort:** Medium — building 5–8 industry-specific sample workspaces and the "edit to claim" UX pattern

**Reversibility:** Easy — A/B testable against the current wizard

**Combinability:** Strong pairing with Option 2 (AI selects the right template) and Option 5 (user's stated goal shapes which template is shown)

---

### Option 2: Concierge AI Setup

**Description:** Replace the wizard with a 3-question conversational intake: "What's your team size? What kind of work do you manage — software, marketing, operations, something else? Describe one project you're working on right now." A language model uses the answers to generate a pre-configured workspace: the project is already named, tasks are pre-seeded based on the described work, the team structure reflects their size, and the notification defaults match their role type. No blank canvas, no arbitrary naming, no structural decisions.

**What's genuinely good about it:**
- Eliminates the blank canvas problem entirely — the workspace reflects the user's own words back at them
- Aligns with user expectations in 2025; conversational setup no longer feels novel
- Reduces "step 3 drop-off" to zero because the project is created *for* the user, not *by* the user

**Biggest risk:**
- A poorly generated workspace creates distrust early — the first impression is "this tool got me wrong"
- Requires prompt engineering, workspace generation logic, and extensive testing across diverse inputs; the failure mode is visible and immediately harmful

**Effort:** High — LLM integration, prompt design, output validation, fallback handling, and multi-domain testing

**Reversibility:** Moderate — can be disabled if quality is inconsistent, but the investment is substantial

**Combinability:** Works as a smarter front-end for Option 1 (AI picks the right template from a curated library rather than generating from scratch — lower risk, lower effort)

---

### Option 3: Progressive Disclosure Setup (No Wizard at All)

**Description:** Abolish the wizard entirely. On account creation, the user lands directly in a functional — though sparse — Nexus workspace. A persistent "setup score" lives in the sidebar: a progress bar showing what's been configured (0/7) with contextual prompts that appear when relevant ("Your team doesn't know about Nexus yet — invite them in 30 seconds"). Each prompt triggers only when the user is in a context where it makes sense — not as a blocking gate. The product is fully usable from minute one.

**What's genuinely good about it:**
- Eliminates the gating that creates drop-off — users who would have abandoned the wizard now stay in the product
- Respects different user readiness levels; power users who already know what they're doing aren't forced through steps they don't need
- Setup prompts are contextually relevant (you see "connect your Jira" when you're in the integrations area, not as step 5 of a linear flow)

**Biggest risk:**
- Without gates, the majority of users never complete setup and miss features that would have retained them — especially integrations and notifications, which drive daily-use habits
- Requires sophisticated behavioral tracking to know *when* to surface each prompt without becoming annoying

**Effort:** Medium-High — the wizard redesign is relatively simple, but building contextual prompt logic and measuring downstream activation is genuinely complex

**Reversibility:** Hard — this changes the onboarding philosophy; hard to go back once shipped

**Combinability:** This is a long-term architectural target that most other options could feed into as a later phase

---

### Option 4: Real Work, First Day (Game Tutorial Pattern)

**Description:** The onboarding wizard and the product merge into one. On sign-up, the user is dropped into a pre-created "Getting Started" project with a task list that *is* the onboarding. "Add your first team member" is a Nexus task. Clicking it opens the real invite flow — not a modal overlaid on a wizard. "Connect your first integration" is a task in the project board. Users complete onboarding by using Nexus to manage their onboarding — the medium *is* the message.

This is how Portal teaches you to play Portal: the tutorial is indistinguishable from the game.

**What's genuinely good about it:**
- Users are inside the real product from the first click — no context switch between "wizard mode" and "real mode"
- Every completed onboarding task demonstrates a feature of Nexus through actual use, not explanation
- Creates an early win: the user ends their first session with a completed project (even if it's a meta-project about setup)

**Biggest risk:**
- The "Getting Started" project might feel contrived or patronising to users who signed up because they have real work to migrate immediately
- Task-based onboarding only works if the tasks map clearly to real product features — badly designed tasks teach nothing and feel like busywork

**Effort:** Medium — requires careful task design, click-to-execute task interactions, and completion tracking

**Reversibility:** Easy — can A/B test as an alternative to the current wizard

**Combinability:** Strong with Option 5 — the guided project is built around the user's stated goal, not a generic "Getting Started" project

---

### Option 5: Goal-First Onboarding (Commitment Device)

**Description:** Before the wizard starts, ask one question: "What do you want to have running in Nexus in the next 30 days?" The answer (two sentences, free text) is stored and used to personalise every subsequent step. "Create your first project" becomes "Create the [user's stated initiative] project." The invite step becomes "Invite the team working on [user's stated initiative]." Every step references their commitment — it's no longer abstract setup, it's investment toward something they said they wanted.

**What's genuinely good about it:**
- Transforms "create first project" from a blank-canvas problem into a named, motivated task — the project already has meaning before the user types anything
- No AI required, no additional infrastructure — it's a UX and copy change that injects a personalisation token throughout the wizard
- Users who state a goal have a reason to finish; the commitment creates mild accountability

**Biggest risk:**
- The goal-setting question itself could become a new drop-off point if it feels like work or feels vague ("I don't know how to answer this")
- Requires careful prompt design to make the question feel lightweight and to handle edge cases ("I just want to try it")

**Effort:** Low — primarily UX writing and token injection, with a fallback for users who skip the question

**Reversibility:** Very easy — toggle it on or off, A/B testable trivially

**Combinability:** Pairs with almost everything; Option 1, Option 4, and the hybrid below all benefit from knowing the user's goal upfront

---

### Option 6: Unlock Economics (Value-First Milestones)

**Description:** Each completed onboarding step immediately unlocks a concrete product capability rather than just "moving forward." Completing step 3 (create first project) unlocks access to 50 project templates. Completing step 4 (add tasks) unlocks the AI task generator. Completing step 5 (connect integrations) grants 90 days free on the premium integration tier. The wizard becomes a progression system with visible, immediate payoffs — not a hoop to jump through.

**What's genuinely good about it:**
- Each step has a clear "why" — users who hesitate now have an immediate reason to proceed
- Frames Nexus as a product that rewards engagement, creating a positive association from the first session

**Biggest risk:**
- Users may feel the features are being held hostage — "why do I have to do this to access something I paid for?"
- The unlocks need to be genuinely valuable; if the reward is weak, the commitment device backfires

**Effort:** Medium — requires designing unlock mechanics, possibly building premium feature gates, and careful communication of the value exchange

**Reversibility:** Medium — changes how features are gated; unwinding requires care

**Combinability:** Works as a complementary layer over Option 4 or Option 5

---

## 3. Recommended Path

### Hybrid: "Drop-In and Grow" (Options 5 + 1 + 4)

Phase 1 (low effort, high signal — ship in weeks):

> Apply Option 5 immediately. Add a single question before the wizard: "What's the first project or initiative you want to manage in Nexus?" Use the answer to pre-fill the project name in step 3 and to personalise step-copy throughout. This directly attacks the blank-canvas drop-off at step 3 with minimal engineering.

Phase 2 (medium effort, validated by phase 1 data):

> Replace the wizard with Option 4. Convert the "Getting Started" project into a task-based onboarding that uses the goal from step 1 as its title. Users complete onboarding by doing real Nexus actions in a real project, not by clicking "Next" through a wizard.

Phase 3 (if phase 2 data supports it):

> Introduce Option 1-style template seeding. Based on the user's stated goal and any role/industry signal collected at signup, pre-populate the project with realistic tasks rather than leaving it empty.

**Why this combination:**
- Phase 1 is a low-risk, high-leverage copy/UX change that directly addresses step 3 drop-off
- Phase 2 eliminates the wizard/product context switch that makes onboarding feel like a tax
- Phase 3 solves the blank canvas problem that drives step 3 abandonment without requiring AI infrastructure upfront

**What to do first:**
Run the goal-collection question as an A/B test on 50% of new signups. Track step 3 completion rate. If completion lifts by more than 10 percentage points, the personalisation signal is real and you have a mandate for Phase 2.

**What to watch for:**
- Does adding the goal question reduce overall wizard starts (new drop-off before step 1)?
- Does step 3 completion lift when the project name is pre-filled?
- Do users who state a goal complete more of the wizard than users who skip the question?

---

## 4. Wild Card

**Wild card: Abandon onboarding entirely — let the first email do it instead**

**Why it seems wrong:** If users are dropping off in the product, the obvious fix is to fix the product. Delegating to email feels like giving up.

**Why it might be right:** The 60% who drop at step 3 are not refusing to learn Nexus — they're refusing to learn it *right now*, in this format, when they're in exploration mode and haven't committed. Email reaches them at a different time, in a different mental state, with zero competitive context. A well-crafted drip sequence — "Here's how to create your first project (takes 2 minutes)" sent 24 hours after signup — catches the user when they're actually ready to use the tool, not when they're in evaluation mode. Calendly's early growth was largely driven by users who signed up, left, came back from an email, and *then* completed setup. The wizard completion rate is measuring the wrong thing: what matters is whether the user activates, not whether they finish the wizard in one session.

**When to revisit:** If A/B tests on the wizard show diminishing returns and you find that a significant share of users who dropped off step 3 come back to the product within 7 days — that's evidence that the timing problem is real, and email-driven re-activation is worth a serious test.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.0/17.0 (82%) |
| Evaluated | 2026-05-01 |
| Target duration | 147420 ms |
| Target cost | $0.1413 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 analyses the problem before generating ideas — identifies who has the problem, consequences, and constraints | PASS | Problem Reframing section identifies who: 'A team lead or solo PM who signed up to evaluate whether Nexus can replace their current tool — they're time-poor, skeptical'; consequences: 'Users who don't activate don't retain. Every dropped user is wasted acquisition spend'; constraints: 'Team-based product, current 7-step sequence, drop-off specifically at the first step requiring real creative/cognitive investment' |
| c2 | Step 2 produces all three reframes (user story, constraint, analogy) and states which was selected for ideation and why | PASS | Reframe 1 is a user story ('A team lead who needs to know if Nexus will work...'), Reframe 2 is a constraint ('We can't ask users to create something valuable from scratch...'), Reframe 3 is an analogy (the cooking class). Output explicitly states 'Selected framing: Reframe 2' with reasoning that 'it produces the widest solution space because it forces the question: what else could work instead of blank-canvas creation?' |
| c3 | Step 3 applies all five mandatory diversity techniques (inversion, extreme scale, remove constraints, cross-domain transfer, worst idea first) producing at least one option from each | FAIL | Inversion is present (Option 1 'Delete to Fit', Option 3 'No Wizard At All'), remove constraints is present (Option 3), cross-domain transfer is present (Option 4 borrows from Portal). However, no option applies extreme scale thinking (10x/0.1x users surfacing different implications) and no option is explicitly framed as 'worst idea first' — a genuinely bad idea whose failure mode reveals insight. Two of the five mandatory techniques are absent. |
| c4 | At least 5 options pass all three quality tests — distinct, feasible, and specific enough to act on | PASS | Six options are presented — Delete to Fit, Concierge AI Setup, Progressive Disclosure Setup, Real Work First Day, Goal-First Onboarding, Unlock Economics — each with a specific mechanism, distinct from one another, and feasible (effort estimates provided). All six are specific enough to act on. |
| c5 | Step 4 evaluates each option with genuine pros, biggest risk, effort estimate, and reversibility | PASS | Every one of the six options contains 'What's genuinely good about it', 'Biggest risk', 'Effort' (with level e.g. 'Low', 'Medium', 'High'), and 'Reversibility' (e.g. 'Very easy', 'Hard', 'Medium'). All four components present across all options. |
| c6 | A wild card option is included in the output — unconventional but argued seriously | PASS | Section '4. Wild Card' presents 'Abandon onboarding entirely — let the first email do it instead', argued seriously with references to Calendly's growth strategy, user mental state during evaluation vs. readiness modes, and specific trigger conditions ('if A/B tests on the wizard show diminishing returns and you find that a significant share of users who dropped off step 3 come back within 7 days'). |
| c7 | Recommended path specifies what to do first as a concrete immediate action | PASS | 'Run the goal-collection question as an A/B test on 50% of new signups. Track step 3 completion rate. If completion lifts by more than 10 percentage points, the personalisation signal is real and you have a mandate for Phase 2.' Also: 'Apply Option 5 immediately. Add a single question before the wizard: What's the first project or initiative you want to manage in Nexus?' |
| c8 | Options named with descriptive memorable names (not "Option 1", "Option 2") | PARTIAL | Each option has a descriptive name ('Delete to Fit', 'Concierge AI Setup', 'Progressive Disclosure Setup', 'Real Work, First Day', 'Goal-First Onboarding', 'Unlock Economics'). However, these names are prefaced with 'Option 1', 'Option 2' etc. throughout — the criterion explicitly flags this numbering as what to avoid. Names are memorable but the numbered labeling persists. |
| c9 | Output addresses step 3 (create first project) explicitly as the dropoff hotspot — at least 2 of the generated options target reducing friction at that specific step, not generic onboarding ideas | PASS | Problem Reframing explicitly identifies step 3 as 'the first step requiring real creative/cognitive investment (naming and scoping a project)'. Option 1 (users arrive at pre-populated workspace, edit instead of create), Option 2 (AI creates the project for the user), and Option 5 ('Create your first project' becomes 'Create the [user's stated initiative] project' with pre-filled name) all directly target step 3 friction. |
| c10 | Output's inversion option flips the wizard premise (e.g. "no onboarding wizard at all — drop the user into a sample project pre-populated with their email contacts") rather than a slight tweak | PASS | Option 1 'Delete to Fit': 'Users arrive at a fully-configured workspace — not a wizard, not an empty canvas. A sample project is already created with realistic tasks, fake team members, connected integrations... Onboarding becomes: Does this look right? Keep what fits, delete or rename what doesn't.' This directly matches the criterion's example pattern. Option 3 further abolishes the wizard entirely. |
| c11 | Output's extreme-scale option imagines onboarding for 10x or 0.1x users (e.g. "1,000 simultaneous account-creators in a workshop" or "single user, no team yet") and surfaces a different design implication | FAIL | No option in the output considers extreme scale scenarios — neither 1,000 simultaneous users (e.g. a corporate rollout or workshop) nor a single solo user with no team (which would surface different implications for the 'invite team' step). All six options address a generic individual user scenario. The extreme scale diversity technique is entirely absent. |
| c12 | Output's remove-constraints option drops one of the 7 steps as non-essential (e.g. "skip integrations and notifications for week 1, prompt later in-app") with reasoning | PASS | Option 3 'Progressive Disclosure Setup (No Wizard at All)' abolishes the mandatory gating of all 7 steps: 'contextual prompts that appear when relevant — not as a blocking gate... connect your Jira when you're in the integrations area, not as step 5 of a linear flow. The product is fully usable from minute one.' This removes the constraint of sequential step completion and defers steps (including integrations/notifications) to contextually appropriate moments. |
| c13 | Output's cross-domain transfer option borrows a pattern from outside SaaS onboarding — e.g. how Duolingo's progressive disclosure works, how IKEA furniture instructions order steps, how a Mario tutorial level introduces mechanics | PASS | Option 4 'Real Work, First Day (Game Tutorial Pattern)' explicitly names Portal as the source: 'This is how Portal teaches you to play Portal: the tutorial is indistinguishable from the game.' The cross-domain transfer from video game tutorial design to SaaS onboarding is explicit and specific. |
| c14 | Output's worst-idea option is genuinely bad (e.g. "force users to invite 5 colleagues before they can do anything") and explains what the failure mode reveals — not a softened "it could work in some scenarios" | FAIL | No option in the output is framed as a deliberately bad idea whose failure mode reveals insight. Option 6 'Unlock Economics' mentions a risk that 'users may feel the features are being held hostage' but is presented as a viable option, not a worst idea. The Wild Card ('abandon onboarding for email') is argued as potentially correct, not as a bad idea. The worst-idea-first diversity technique is entirely absent. |
| c15 | Output produces at least 5 distinct, feasible, specific options — each has a memorable name (not "Option 1, 2, 3"), a specific mechanism, a primary risk, and an effort estimate | PASS | Six options present, each with: a descriptive name ('Delete to Fit', 'Concierge AI Setup', etc.), a specific mechanism (e.g. 'A language model uses the answers to generate a pre-configured workspace'), a primary risk ('A poorly generated workspace creates distrust early'), and an effort estimate ('High — LLM integration, prompt design, output validation...'). All four components are present for all options. |
| c16 | Output's wild-card option is non-obvious but argued seriously — e.g. "make onboarding optional, run a Loom walkthrough instead of a wizard" — not a joke entry | PASS | 'Abandon onboarding entirely — let the first email do it instead' is non-obvious (counter to the implicit brief to fix the wizard) and argued seriously: cites Calendly's growth, distinguishes exploration vs. readiness mental states, specifies the data trigger ('if a significant share of users who dropped off step 3 come back within 7 days'), and explains why wizard completion rate may be the wrong metric. |
| c17 | Output's recommended path names a concrete first action — "ship the sample-project-on-signup version as a 1-week experiment, measure step-3 completion against control" — not "consider trying X" | PASS | 'Run the goal-collection question as an A/B test on 50% of new signups. Track step 3 completion rate. If completion lifts by more than 10 percentage points, the personalisation signal is real and you have a mandate for Phase 2.' Specific rollout percentage, specific metric to track, and specific threshold for action are all stated. |
| c18 | Output addresses the 60% dropoff with a hypothesis about WHY users abandon at step 3 — is creating-a-project blocked by team-not-set-up-yet, or is it the cognitive load of a real first project — and matches options to that hypothesis | PARTIAL | The output identifies one hypothesis — cognitive load / blank canvas: 'the first step requiring real creative/cognitive investment (naming and scoping a project)' and Reframe 2 ('We can't ask users to create something valuable from scratch before showing them what valuable looks like'). Options 1, 2, and 5 are explicitly matched to this hypothesis. However, the criterion asks about distinguishing between competing hypotheses (team-not-set-up blocking vs. cognitive load of project creation); the output only pursues one explanation without considering or ruling out the alternative. |

### Notes

The output is a strong creative response that excels at problem framing (clear who/consequences/constraints analysis), producing three structured reframes with explicit selection reasoning, evaluating all options with pros/risks/effort/reversibility, and delivering a concrete phased recommended path with a specific A/B test. The wild card (defer to email re-activation) is non-obvious and argued with genuine evidence. Where the output falls short is in applying all five mandatory diversity techniques: extreme scale (imagining 1,000-user workshop vs. solo user scenarios) and worst-idea-first (a genuinely bad idea whose failure reveals something) are entirely absent — the six options are all earnest, feasible proposals rather than including one deliberately bad idea to learn from. Options also carry 'Option 1/2/3' numbering alongside their descriptive names, which the criterion flags as undesirable. The hypothesis about step 3 abandonment is single-threaded (blank canvas cognitive load) without explicitly considering or ruling out the competing hypothesis (team not yet set up blocking meaningful project creation).
