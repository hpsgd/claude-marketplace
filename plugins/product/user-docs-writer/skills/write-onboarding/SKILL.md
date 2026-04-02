---
name: write-onboarding
description: "Write onboarding content — welcome flow, getting-started guide, or first-run experience. Optimised for time-to-first-value. Use when creating new user onboarding or improving activation rates."
argument-hint: "[product area or user type to write onboarding for]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Write onboarding content for $ARGUMENTS using the mandatory process and structure below.

**Core principle: The fastest path from signup to genuine value.** Every sentence either moves the user closer to their "aha moment" or gets cut.

## Step 1 — Define the value path

Before writing, map the journey from signup to value:

1. **Identify the target user.** Who is this onboarding for? What do they already know? What did they sign up hoping to accomplish?
2. **Define the "aha moment."** What is the single experience that makes the user think "this is worth my time"? Be specific — not "understand the product" but "see their first dashboard with real data."
3. **Map the minimum steps.** What is the absolute minimum a user must do to reach the aha moment? List every action.
4. **Identify drop-off risks.** Where in the flow might a user abandon? What causes confusion, friction, or doubt?

```markdown
### Value path

| Element | Definition |
|---|---|
| **Target user** | [Who, what they know, what they want] |
| **Aha moment** | [Specific experience that delivers first value] |
| **Minimum steps** | [Count] steps to reach aha moment |
| **Time target** | [Minutes] from signup to aha moment |
| **Primary drop-off risk** | [Where and why users abandon] |
```

**Output:** Completed value path table.

## Step 2 — Write the welcome

The first screen or section after signup. Must answer three questions instantly:

```markdown
## Welcome to [Product]

[One sentence: what the product does for THEM — not what it is, but what it enables.]

**In the next [N] minutes, you'll [specific outcome].**

Here's what we'll do:
1. [First action — framed as benefit, not task]
2. [Second action]
3. [Third action — this is the aha moment]
```

**Rules for the welcome:**
- Lead with the user's goal, not the product's features. "You'll have your first report in 5 minutes" not "Our analytics platform offers..."
- State the time commitment upfront. Users need to know if they have time for this.
- No more than 3 steps visible. Progressive disclosure — don't show everything at once.
- No jargon. If the product has specific terminology, introduce it in context later.

**Output:** Welcome section with time commitment and step preview.

## Step 3 — Write each onboarding step

Each step in the onboarding flow follows this format:

```markdown
## Step N: [Action verb] [what they'll accomplish]

[One sentence: why this step matters to THEM.]

### What to do

1. [Specific action with exact UI location: "Click **New Project** in the top-right corner"]
2. [Next action with example input: "Enter a project name, e.g., 'My first dashboard'"]
3. [Final action for this step]

### You should see

[Describe or show what the user should see after completing the step.
 Include a description of the expected UI state.]

### If something's not right

- **[Problem]:** [One-line fix — e.g., "If the button is greyed out, check that you've verified your email"]
```

**Rules for each step:**
- **One goal per step.** Each step achieves one thing the user can see or verify.
- **Under 2 minutes per step.** If a step takes longer, break it into sub-steps.
- **Show, don't tell.** Use the product to teach the product. Don't explain concepts — have the user do something that demonstrates the concept.
- **Use exact UI element names.** Bold the names: "Click **Create**" not "click the create button."
- **Provide example inputs.** Don't say "enter a name" — say "enter a name, e.g., 'My first project'."
- **Include the escape hatch.** If something goes wrong at this step, give a one-line fix.

**Output:** All onboarding steps with actions, expected results, and troubleshooting.

## Step 4 — Write the aha moment confirmation

When the user reaches the value moment, confirm it explicitly:

```markdown
## You're set up!

[One sentence celebrating what they just accomplished — specific to what they built/created/configured.]

### What you just did
- [Concrete outcome 1 — e.g., "Created your first project with live data"]
- [Concrete outcome 2 — e.g., "Set up your first automated alert"]

### What to explore next

| If you want to... | Go here |
|---|---|
| [Common next goal] | [Link with brief description] |
| [Second common goal] | [Link with brief description] |
| [Power-user goal] | [Link with brief description] |
```

**Rules for the aha moment:**
- Name what they accomplished, not what features they used
- Limit "next steps" to 3 options — more creates decision paralysis
- Link to deeper content, don't summarise it here

**Output:** Completion confirmation with specific outcomes and next steps.

## Step 5 — Quality checks

| Check | Requirement |
|---|---|
| Time test | Can a new user complete the full onboarding in the stated time? |
| Aha moment reached | Does the flow end with the user seeing real value, not just a configured state? |
| No jargon | Would a first-time user understand every term without a glossary? |
| One action per step | Does each step do exactly one thing? |
| Expected results present | Does every step show what success looks like? |
| Escape hatches | Does every step have a "if this didn't work" fallback? |
| Progressive disclosure | Is information revealed only when needed, not all at once? |
| Example inputs provided | Does every input field have a suggested value? |

## Rules

- Every step must take under 2 minutes. If you can't get to the aha moment in 5 steps, you're onboarding to too much. Narrow the scope.
- Use the product to teach the product. Don't explain what a dashboard is — have the user create one. Experience beats explanation.
- Never front-load configuration. Ask for the minimum to start (name + one setting), then let the user refine later. "You can change this anytime in Settings" is a powerful phrase.
- Progressive disclosure is mandatory. The user sees step 1, then step 2 appears. Not a wall of 10 steps at once.
- Write for the user who will abandon in 30 seconds if they don't see value. Every sentence must earn its place.
- Do not document features during onboarding. Onboarding gets the user to value. Feature documentation is a separate concern — cross-reference `/user-docs-writer:write-user-guide` for comprehensive feature docs and `/user-docs-writer:write-kb-article` for specific questions.

## Output Format

```markdown
# Getting Started with [Product] — [User Type]

**Time to complete:** [N] minutes
**What you'll accomplish:** [Specific outcome]

## Welcome
[Welcome section from Step 2]

## Step 1: [First action]
[Step content from Step 3]

## Step 2: [Second action]
[Step content]

## Step 3: [Aha moment action]
[Step content]

## You're set up!
[Confirmation from Step 4]

---
Last verified: [date]
Product version: [version]
```
