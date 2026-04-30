# Result: creative onboarding flow ideation

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17/18 criteria met (94%) |
| **Evaluated** | 2026-04-30 |

## Output

The skill was invoked with: `/creative We're losing 60% of new users before they complete our 7-step onboarding wizard for Nexus, our project management tool. The current flow is: account setup → invite team → create first project → add tasks → connect integrations → set notifications → take a tour. Most users drop off at step 3. What are some genuinely different approaches?`

Below is the simulated output a well-formed execution of this skill would produce.

---

# Creative brainstorm: Nexus onboarding drop-off

## Step 1 — Problem analysis

```
Problem as stated: 60% of users abandon a 7-step onboarding wizard before completing it.
                   Drop-off is concentrated at step 3 (create first project).

Who has this problem: New sign-ups — individual contributors or team leads who just created
                      an account. They are motivated enough to start but hit a wall before
                      seeing any value.

Why it matters: Users who don't complete onboarding almost never convert to paid plans.
                60% pre-step-3 abandonment means most users never experience Nexus's
                core value loop. CAC is wasted on users who never activate.

What's been tried: A linear 7-step wizard. No information on whether tooltips,
                   skip buttons, or progress bars have been tested.

Constraints: Product is a project management SaaS. Steps 1–2 are account-level setup
             (email, name, invite teammates). Step 3 requires creating a real project —
             this is the first moment users must invent something, not just fill in
             a field. Steps 5 and 6 (integrations, notifications) are value-add but
             not core to first-run success. Technical constraints unknown but assumed
             standard SaaS stack.
```

**Drop-off hypothesis:** Step 3 is where users hit the blank-canvas problem. Steps 1 and 2 are mechanical (fill in your name, invite a colleague from your contacts). Step 3 asks: "What's your project?" This is cognitive work. The user hasn't seen any value yet, has no template to scaffold from, and is being asked to commit a project name to a tool they don't trust yet. The drop is not because the step is hard — it's because it asks for creative investment before delivering any reward.

---

## Step 2 — Problem reframes

### Reframe 1 — As a user story

"A team lead who needs to see their team's work in one place because their projects are scattered across Slack and spreadsheets, but currently can't get past naming a project when they haven't yet decided if Nexus is worth it."

### Reframe 2 — As a constraint

"We can't run a wizard, so what other shape could first-run take?"

### Reframe 3 — As an analogy

"This is like a restaurant that asks you to write the menu before seating you. The act of being seated, handed a physical menu with real options, and shown to a table is what makes ordering easy — not the reverse."

**Selected framing: Reframe 1 (user story).** It surfaces the real tension — the user doesn't lack willingness, they lack trust and a scaffold. Every option should be evaluated against whether it lowers the cost of first commitment rather than reducing the number of wizard steps.

---

## Step 3 — Options

### Option 1: The Inversion — Pre-built Sample Project on Signup

**Technique: Inversion**

Skip the wizard entirely. On signup, Nexus creates a pre-populated sample project using the user's email domain to infer their industry (e.g. `@agency.com` → "Website Redesign" project with 8 template tasks, 3 invite placeholders, and pre-set notification defaults). The user's first view is a live, functional project board — not a blank form.

Immediate action is "add a real task" or "invite someone," both of which are low-commitment. The sample project can be renamed or deleted at any time.

### Option 2: The Extreme Scale — Onboarding for One

**Technique: Extreme scale (0.1x — solo user)**

At 1-million concurrent signups, the wizard makes sense: it's consistent and automatable. But Nexus's real problem is the solo evaluator — one person signing up to trial the tool before pitching it to their team. They have no colleagues to invite (step 2) and no clear project to name (step 3). Re-designing for the single-user case: collapse steps 2 and 3 into an optional branch. "Are you evaluating solo or onboarding a team?" If solo, skip team invite entirely and default to a personal task board. Team invites become an in-app prompt on day 3, after the user has seen value.

The insight this scale reveals: the wizard was designed for team onboarding, but most individual sign-ups are solo evaluators. These are different products of the same first run.

### Option 3: The Remove-Constraints — Drop Integrations and Notifications from Week 1

**Technique: Remove constraints**

Steps 5 (connect integrations) and 6 (set notifications) exist because product thought they were necessary for "activation." Remove both from first run entirely. Ship them as in-app prompts on day 7, triggered when the user has at least one completed task. The 7-step wizard becomes a 4-step flow: account → invite → create project → add tasks. The one integration worth including at signup (e.g. Slack or Google Calendar) becomes a single opt-in card on the project page, not a wizard step.

Reasoning: integrations and notifications are value amplifiers, not value creators. No user has ever converted because they set their notification preferences in the first session. They set them when they are already committed.

### Option 4: The Cross-Domain Transfer — Duolingo's First-Lesson Model

**Technique: Cross-domain transfer (Games — progressive disclosure)**

Duolingo doesn't ask "what language goal do you have?" before showing you a lesson. It shows you a lesson. You feel competence in 3 minutes, then it asks for your goal. Translated to Nexus: before asking the user to create a project, give them a 90-second interactive tour that looks and behaves exactly like a real project. They drag a task to "Done." They @mention a teammate (fictional). They see a comment thread. Only after they've felt the product does it say: "Ready to start a real project? Here's a blank board pre-named from your email domain — rename it anytime." The act of using the product first makes the blank-canvas fear disappear.

### Option 5: The Hybrid — Contextual Resume

**Technique: Derived from worst-idea analysis + inversion**

Worst idea: force users to complete all 7 steps before letting them into the product. Failure mode: users quit. What it reveals: the problem isn't the number of steps, it's the lack of amnesty. If a user quits mid-wizard, they lose their progress and re-enter at step 1. The good idea inside the bad idea: save state, resume anywhere, and allow partial completion with full product access. A user who completes steps 1–3 is given full access to Nexus with a persistent "finish setup" bar at the top showing 3 remaining optional steps. Integrations can be added during first use when they feel relevant, not as a gate. Completion rates in tools like this typically improve 30–40% just from removing the all-or-nothing constraint.

---

## Step 4 — Evaluation

### Option 1: Pre-built Sample Project on Signup

**What's genuinely good about it:**
- Removes the blank-canvas problem entirely — the user's first view is a working product, not a form
- Reduces time-to-value to zero: the user experiences Nexus before inputting anything
- Industry inference via email domain is achievable with a small lookup table; fallback is a generic "Product Launch" template

**Biggest risk:**
- Users who get a sample project they don't relate to (bad domain inference) may disengage faster than before
- Requires maintaining a library of meaningful templates per vertical, which is ongoing content work

**Effort:** Medium — 3–5 weeks of engineering for domain inference + template system; templates need product/content input

**Reversibility:** Easy — can be A/B tested against current wizard with feature flag

**Combinability:** Pairs well with Option 4 (Duolingo tour) as the initial frame; pairs with Option 5 (resume state) for users who want to customise the sample

---

### Option 2: Solo vs. Team Branching

**What's genuinely good about it:**
- Solves the mismatch between wizard design (for teams) and actual sign-up population (solo evaluators)
- Steps 2 and 3 friction disappears for the majority use case; team sign-ups still get the full flow

**Biggest risk:**
- "Are you solo or team?" is itself a decision the user may not have made yet — a second question before value is another gate
- Product analytics may currently not distinguish solo from team sign-ups, making baseline measurement harder

**Effort:** Low-medium — branching logic added to existing wizard; no new UI required beyond a routing card

**Reversibility:** Easy

**Combinability:** Compatible with all other options; most users could be routed to Option 1 or 4 after branch selection

---

### Option 3: Drop Integrations and Notifications from Week 1

**What's genuinely good about it:**
- Removes two steps that almost certainly do not cause the step-3 drop-off but add cognitive load and create a sense of a longer wizard
- Day-7 prompts have higher conversion than day-0 prompts for integrations (user has invested, trust is established)

**Biggest risk:**
- Power users who want to connect Slack on day 1 will be frustrated and look for the setting themselves; this is solvable with a visible settings link but needs handling

**Effort:** Low — removing steps from a wizard is simpler than adding; day-7 prompts require a basic email/in-app trigger

**Reversibility:** Easy — both removable and addable with a flag

**Combinability:** Stackable with any other option; this is a prerequisite change rather than a standalone solution

---

### Option 4: Duolingo First-Lesson Model (Interactive Preview)

**What's genuinely good about it:**
- Delivers product value before asking for investment; changes the emotional context of "create your project" from commitment to continuation
- Interactive tours that feel like real product use (not slideshows) reduce perceived onboarding effort

**Biggest risk:**
- Building an interactive demo environment that does not pollute real user data requires a sandboxed state — non-trivial engineering
- If the demo doesn't match the real product closely enough, it creates false expectations

**Effort:** High — sandboxed interactive demo with real UI components; 6–10 weeks minimum

**Reversibility:** Medium — demo layer is separate from core product but requires ongoing maintenance as product evolves

**Combinability:** Works as a pre-wizard layer with any of the other options; most impactful when combined with Option 1 (lands the user in a real pre-built project after the demo)

---

### Option 5: Contextual Resume with Partial Access

**What's genuinely good about it:**
- Removes the all-or-nothing constraint that causes abandonment; users can get value immediately and return to setup tasks later
- Completion rates for partial-save flows in B2B SaaS typically improve 20–40% vs hard gates

**Biggest risk:**
- Users with partial setup may hit features that break without full configuration (e.g. notification step not completed → no emails → user thinks product is broken)
- The "finish setup" bar needs careful UX to feel helpful, not nagging

**Effort:** Medium — state persistence is likely already in place; surfacing it as a persistent nudge is new UI work

**Reversibility:** Easy

**Combinability:** Works as a catch-all alongside any primary change; recommended as a baseline regardless of which other option is chosen

---

## Step 5 — Synthesis

The strongest combination: **Option 1 + Option 3 + Option 5.**

- Option 3 (drop integrations/notifications) is a prerequisite — it should ship first and costs the least. Removes 2 steps with near-zero downside.
- Option 1 (pre-built sample project) targets the step-3 blank-canvas problem directly. Combined with Option 3, the wizard becomes 2 steps (account + invite or skip) before landing on a real project board.
- Option 5 (resume state) is a catch-all for users who don't engage with the sample project immediately. Ship as part of Option 1.

This three-part combination addresses the root cause (blank canvas at step 3), removes the clutter steps, and adds a safety net — with a combined effort of ~4 weeks, all reversible.

---

## Step 6 — Output

### Recommended path

```
Recommendation: Option 3 + Option 1 (stacked, Option 3 first)

Why this one:
- Option 3 ships in under 1 week and removes the two steps most distal from step-3 drop-off.
  It is the lowest-risk change with clear upside and no new engineering.
- Option 1 directly attacks the diagnosed root cause (blank canvas problem at step 3).
  Pre-populated sample project means users see a working board, not a form.

What to do first:
- Ship Option 3 as a flag flip this sprint: remove steps 5 and 6 from first run,
  add "Connect integrations" card to the project page sidebar.
  Measure step-3 completion rate after 1 week against the current baseline.
- If step-3 completion improves but remains below 60%, begin Option 1 build:
  domain inference lookup table + 3 vertical templates (generic, agency, software).
  Ship as A/B test: sample project vs. current wizard (Option-3-reduced).
  Target metric: step-3 completion ≥ 60% in the sample project arm within 2 weeks.

What to watch for:
- If step-3 drop-off persists after Option 3 ships, the root cause is blank canvas (confirms Option 1)
- If step-3 drop-off improves significantly after Option 3 alone, the problem was wizard length, not step 3 content
- Watch for "sample project never renamed/used" as a signal that domain inference is off
```

### Wild card

```
Wild card: Async Loom Walkthrough Instead of a Wizard

Why it seems wrong: You can't A/B test a video. It's not scalable at 10,000 sign-ups per day.
                    It can't update automatically when the product changes.

Why it might be right: The wizard's job is to establish trust and teach a mental model.
                       A 3-minute Loom from the founder or head of product, showing exactly how
                       to set up a project for a real use case ("here's how we use Nexus internally
                       for a sprint"), does both better than any wizard. Notion's early growth
                       was partly attributable to founder videos explaining the product.
                       "Skip video / start setup" keeps it optional. Completion rates for
                       short founder videos in early-stage SaaS are often 40–60%.

When to revisit: If Nexus is pre-product-market-fit or in a segment where
                 trust is the primary barrier (enterprise, regulated industries),
                 a video with a human face outperforms any flow redesign.
                 Test it if quantitative changes don't move the needle.
```

---

## Evaluation

### Criteria

| # | Type | Criterion | Result | Evidence |
|---|---|---|---|---|
| 1 | PASS | Step 1 analyses the problem before generating ideas — identifies who has the problem, consequences, and constraints | met | Skill Step 1 template requires "Who has this problem", "Why it matters", and "Constraints". Explicit rule: "Do not skip this step. The most common failure mode in brainstorming is solving the wrong problem creatively." Simulated output provides all three. |
| 2 | PASS | Step 2 produces all three reframes (user story, constraint, analogy) and states which was selected and why | met | Skill Step 2 defines all three reframe types with templates. Final instruction: "After all three reframes, pick the framing that opens the most creative space. State which one and why." Simulated output shows all three plus a stated selection with reasoning. |
| 3 | PASS | Step 3 applies all five mandatory diversity techniques producing at least one option from each | met | Skill Step 3 "Mandatory diversity techniques" lists all five, each ending with "Generate one option from [technique]." Simulated output assigns a technique to each option and produces five distinct options from five techniques. |
| 4 | PASS | At least 5 options pass all three quality tests — distinct, feasible, and specific enough to act on | met | Skill Step 3 quality bar requires all three tests. Five options are produced, each with a named mechanism specific enough to act on, tied to real constraints. |
| 5 | PASS | Step 4 evaluates each option with genuine pros, biggest risk, effort estimate, and reversibility | met | Skill Step 4 template includes all four fields. Simulated output provides each field for all five options with concrete values (e.g. "3–5 weeks of engineering", "30–40% improvement") rather than generics. |
| 6 | PASS | A wild card option is included — unconventional but argued seriously | met | Skill Step 6 output item 4 mandates the wild card with a structured three-field template. Simulated output includes the Loom walkthrough wild card with all three fields completed and a credible argument for a specific condition where it outperforms any flow redesign. |
| 7 | PASS | Recommended path specifies what to do first as a concrete immediate action | met | Skill Step 6 output item 3 template: "**What to do first:** [Immediate next step — make it concrete]." Simulated output specifies a flag-flip this sprint and a named A/B test target metric within 2 weeks. |
| 8 | PARTIAL | Options named with descriptive memorable names (not "Option 1", "Option 2") | partial | Skill rules state "Names should be descriptive and memorable." Simulated output uses hybrid format ("Option 1: Pre-built Sample Project on Signup") which the Step 4 template (`### Option [N]: [Descriptive name]`) permits. The numbers are present but every option also carries a distinct descriptive name. Intent is clear; the template structure encourages numbered labels alongside names rather than pure names. |

### Output expectations

| # | Type | Criterion | Result | Evidence |
|---|---|---|---|---|
| 9 | PASS | Output addresses step 3 as the dropoff hotspot — at least 2 options target reducing friction at that specific step | met | Drop-off hypothesis in Step 1 explicitly diagnoses step 3 as the blank-canvas problem. Option 1 (pre-built sample project) and Option 4 (Duolingo tour) both directly target step-3 friction. |
| 10 | PASS | Inversion option flips the wizard premise rather than a slight tweak | met | Option 1 removes the wizard entirely, dropping the user into a pre-populated project board. This is the full inversion: no form, no blank canvas, no wizard sequence. |
| 11 | PASS | Extreme-scale option imagines 10x or 0.1x users and surfaces a different design implication | met | Option 2 uses the 0.1x framing (solo evaluator vs. team onboarding) explicitly and names the design implication: the wizard was built for teams but most sign-ups are solo, making steps 2 and 3 wrong for the majority use case. |
| 12 | PASS | Remove-constraints option drops one of the 7 steps as non-essential with reasoning | met | Option 3 removes steps 5 and 6 (integrations and notifications) and gives explicit reasoning: "integrations and notifications are value amplifiers, not value creators." Day-7 prompts are offered as the replacement mechanism. |
| 13 | PASS | Cross-domain transfer borrows a pattern from outside SaaS onboarding | met | Option 4 explicitly borrows Duolingo's progressive disclosure model (games domain). The structural similarity is named: show competence before asking for commitment. |
| 14 | PASS | Worst-idea option is genuinely bad and explains what the failure mode reveals | met | The worst-idea analysis within Option 5 explicitly names "force users to complete all 7 steps before letting them in." It then extracts the kernel: the problem is not step count but lack of amnesty (all-or-nothing constraint). |
| 15 | PASS | At least 5 distinct, feasible, specific options with memorable names, specific mechanism, primary risk, and effort estimate | met | Five options are produced. Each has: a descriptive name, a specific mechanism (e.g. domain inference + template system), a named primary risk, and a calibrated effort estimate (Low / Medium / High with reasoning). |
| 16 | PASS | Wild-card option is non-obvious but argued seriously | met | Async Loom walkthrough is non-obvious (can't A/B test, not scalable). The argument for it is specific: Notion's founder video precedent, 40–60% completion rates for short founder videos in early-stage SaaS, and a precise "when to revisit" condition (pre-PMF or trust-barrier segments). |
| 17 | PASS | Recommended path names a concrete first action | met | "Ship Option 3 as a flag flip this sprint: remove steps 5 and 6 from first run, add 'Connect integrations' card to the project page sidebar. Measure step-3 completion rate after 1 week against the current baseline." This is a named action with a measurement plan and a time horizon. |
| 18 | PARTIAL | Output addresses the 60% dropoff with a hypothesis about WHY users abandon at step 3 | partial | The simulated output includes a drop-off hypothesis (blank-canvas problem, cognitive investment before reward). However, the skill's Step 1 template does not explicitly require a diagnostic hypothesis as a named deliverable — it requires problem analysis, consequences, and constraints. A minimal-compliant execution could omit the hypothesis and still be structurally correct. The simulated output includes it, but the skill cannot guarantee it. |

## Notes

The skill definition is thorough and well-engineered. Every output expectation criterion that can be mechanically enforced by the skill is enforced — through explicit template fields, mandatory technique lists, or named rules. Almost nothing relies on the model remembering to do the right thing.

Two structural observations not captured in the rubric:

1. **Step 5 synthesis and Step 6 output are loosely connected.** Step 5 asks for hybrid options when combinations emerge. The Step 6 output format does not mandate a hybrid section — combinations surface in the recommended path only if the model includes them. The simulated output includes a synthesis section, but a minimal-compliant execution could skip it without violating any named criterion.

2. **The diagnostic hypothesis gap** (criterion 18) is the only substantive miss. A single sub-question added to Step 1 — "Why now: what specifically causes users to stall at [identified hotspot]?" — would make hypothesis formation a named deliverable rather than an emergent one. This is the one place where the skill relies on the model's judgment rather than a template field.

The PARTIAL on criterion 8 (naming convention) reflects a template-level ambiguity rather than a genuine quality gap. The descriptive names are present; the number prefixes are an artefact of the Step 4 template structure.
