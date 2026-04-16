# Creative onboarding flow ideation

A product team wants fresh ideas for reducing drop-off during user onboarding. They're stuck on a linear wizard approach and want genuinely different alternatives.

## Prompt

> /creative We're losing 60% of new users before they complete our 7-step onboarding wizard for Nexus, our project management tool. The current flow is: account setup → invite team → create first project → add tasks → connect integrations → set notifications → take a tour. Most users drop off at step 3. What are some genuinely different approaches?

```markdown

## Output

### Creative: Reduce Nexus onboarding drop-off

#### Step 1 — Problem understanding

Problem as stated: 60% drop-off before completing 7-step wizard
Who has this problem: New Nexus users, likely small team leads who signed up expecting quick value
Why it matters: Conversion to active user is the core metric; 60% drop-off means 60% of marketing spend wasted
What's been tried: Linear 7-step wizard — drop-off cliff at step 3 (create first project)
Constraints: Engineering bandwidth (medium); can't redesign auth; existing users not disrupted

Drop at step 3 is diagnostic. The wizard asks for commitment (create a project) before the user has seen value.

#### Step 2 — Reframes

**Reframe 1 — As a user story:**
"A team lead who needs to try the tool before committing, because they don't know if it fits their workflow, but currently they're asked to create a project before they've seen any feature work."

**Reframe 2 — As a constraint:**
"We can't ask users to create real content before they understand the tool, so what if we removed content creation from onboarding entirely?"

**Reframe 3 — As an analogy:**
"This is like a cooking class that requires you to buy all the ingredients before you've seen the recipe."

**Selected reframe:** Reframe 2 (constraint removal) — opens the most creative space by challenging the assumption that onboarding must involve creating content.

#### Step 3 — Options

##### Technique 1 — Inversion
Remove the wizard entirely. Launch users into a pre-built demo workspace with sample projects and tasks populated. When ready, a sticky "Set up your real workspace" starts a 2-step setup.

##### Technique 2 — Extreme scale
Solo mode: for users who sign up without a team, skip invite-team entirely. Create a solo project template. Show individual value first, upsell team features once they've seen it.

##### Technique 3 — Remove constraints
Templates-first: replace the blank canvas with 12 industry templates. Selection takes 10 seconds. User gets to "ah, this is how it works" in 90 seconds instead of 7 minutes.

##### Technique 4 — Cross-domain transfer
Game tutorial model: guided overlay walks user through adding one task, assigning it, moving it to Done. No form. No wizard. Just the product teaching itself through use.

##### Technique 5 — Worst idea first
Make onboarding take 20 minutes: 30-question assessment. The kernel: the customisation is the value. Strip to 5 questions and the workspace feels curated, not generic.

#### Step 4 — Evaluation

##### Option A: "Live Demo" — demo workspace on first login

| Field | Value |
|---|---|
| What's genuinely good about it | Eliminates the creation-commitment problem. Users see value before committing. |
| Biggest risk | Users explore and don't transition to real workspace. Sticky banner may not create urgency. |
| Effort | High — 4-6 weeks to build and maintain a compelling demo dataset. |
| Reversibility | Easy — A/B testable alongside existing wizard. |


##### Option B: "Solo First" — team-optional onboarding

| Field | Value |
|---|---|
| What's genuinely good about it | Surgical fix. Removes one blocking step for solo signups. Ships in a sprint. |
| Biggest risk | Solo users may not convert to paying customers — team collaboration is the core value prop. |
| Effort | Low — 1 sprint. |
| Reversibility | Trivially reversible. |


##### Option C: "Template Sprint" — industry templates replace blank canvas

| Field | Value |
|---|---|
| What's genuinely good about it | Blank canvas paralysis is documented. Templates are a proven solution. |
| Biggest risk | Templates are someone else's project structure. Users may dismiss as "not relevant." |
| Effort | Medium — 2-3 weeks. |
| Reversibility | Easy — templates coexist with blank project creation. |


##### Option D: "Game Tutorial" — guided task in the real UI

| Field | Value |
|---|---|
| What's genuinely good about it | Learns by doing. Creates muscle memory before commitment. |
| Biggest risk | Tutorial ends and blank canvas problem returns. |
| Effort | Medium — 3-4 weeks for guided overlay system. |
| Reversibility | Easy. |


##### Option E: "Personalised Workspace" — 5-question setup assessment

| Field | Value |
|---|---|
| What's genuinely good about it | Customisation creates ownership. User sees themselves in the tool from minute one. |
| Biggest risk | 5 questions may move the drop-off point earlier. |
| Effort | High. |
| Reversibility | Moderate. |


#### Recommended path

**Recommendation:** Option B (Solo First) + Option C (Template Sprint) in sequence

**What to do first:** This week, add "Skip for now" to the invite-team step and measure drop-off at step 3 in the next cohort. If it improves, ship Option B. If not, Template Sprint is the next experiment.

**What to watch for:** If skip rate on invite-team exceeds 60%, solo-first becomes a permanent design decision.

---

#### Wild card

**Wild card: "Abandon the wizard, let the product teach itself"**
Why it seems wrong: Users will be confused with no guidance. Support tickets will spike.
Why it might be right: Wizards optimise for completion of a flow, not understanding. Users who complete the wizard and then churn are just as lost as those who abandon it. The wizard covers up a discoverability problem.
When to revisit: If churn at day 7 is high despite completed wizards.
```

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 (94%) |
| Evaluated | 2026-04-16 |


- [x] PASS: Step 1 analyses problem before generating ideas — Step 1 is "Understand before ideating" with a defined template (problem as stated, who has it, why it matters, what's been tried, constraints). The definition states "Do not skip this step. The most common failure mode in brainstorming is solving the wrong problem creatively."
- [x] PASS: Step 2 produces all three reframes with selection and reasoning — Step 2 defines exactly three reframe types: "As a user story," "As a constraint," "As an analogy." The definition states "After all three reframes, pick the framing that opens the most creative space. State which one and why." All three are mandatory and the selection must be stated.
- [x] PASS: Step 3 applies all five mandatory diversity techniques — Step 3 lists five under "Mandatory diversity techniques": Inversion, Extreme scale, Remove constraints, Cross-domain transfer, Worst idea first. The definition states "Apply each technique to generate at least one option." All five are mandatory.
- [x] PASS: At least 5 options pass all three quality tests — Step 3 states "at least 5 genuinely different approaches" must pass all three tests: distinct, feasible, and specific. The quality bar is explicitly defined with an example of what fails ("'Use AI' is not an option") and what passes. The definition provides a quality gate: "If you have fewer than 5 options that pass all three tests, go back to the techniques and push harder."
- [x] PASS: Step 4 evaluates with genuine pros, biggest risk, effort, and reversibility — Step 4 template requires: "What's genuinely good about it," "What's the biggest risk," "Effort to implement," "Reversibility." All four fields are mandatory. The evaluation rules also state what counts as a genuine pro ("Reduces cost by 60%" not "It's innovative").
- [x] PASS: Wild card included and argued seriously — the Rules section states "The wild card is mandatory." Step 6 output section defines the wild card template with three required fields: "Why it seems wrong," "Why it might be right," "When to revisit." The wild card cannot be omitted.
- [x] PASS: Recommended path specifies concrete immediate action — Step 6 output template includes "What to do first — Immediate next step — make it concrete." This is a required field in the recommended path section.
- [~] PARTIAL: Options named with descriptive memorable names — the Rules section states "Name every option. Names should be descriptive and memorable." The rule exists and is specific. However it is in the Rules section rather than a template field requirement — it is enforced by instruction rather than structure. PARTIAL ceiling applies per criterion prefix.

### Notes

The creative skill is strong. The five mandatory diversity techniques ensure the solution space is genuinely explored rather than anchored on the first idea. The "worst idea first" technique is the most distinctive — the instruction to find the kernel of a good idea inside the bad one is a well-established creativity technique. Step 5 (Combine and synthesise) is defined in the process but is not in the Output Format as a mandatory section — the combination recommendation appears as part of the recommended path, which is slightly inconsistent. The evaluation rules ("Innovative is not a pro. Reduces cost by 60% is a pro") are precise and prevent hollow evaluations.
