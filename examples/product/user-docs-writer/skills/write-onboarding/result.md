# Result: Write onboarding

**Verdict:** PASS
**Score:** 15.5/16 criteria met (97%)
**Evaluated:** 2026-04-30

---

## Prompt

```
/user-docs-writer:write-onboarding for new Clearpath users — the in-product onboarding experience that takes someone from account creation to completing their first project milestone.
```

---

## Output

What follows is the full simulated output the skill would produce for the Clearpath prompt.

---

### Step 1 output — Value path

| Element | Definition |
|---|---|
| **Target user** | New Clearpath user: team lead or project manager, comfortable with web apps, signed up to get a project tracked and visible to their team |
| **Aha moment** | Seeing their first milestone marked complete and watching project status update automatically in the project view |
| **Minimum steps** | 4 steps to reach the aha moment |
| **Time target** | 5 minutes from account creation to first milestone completion |
| **Primary drop-off risk** | Step 2 (project creation): users abandon if asked for too much upfront (due dates, team members, tags). Keep it to name only and one milestone to create |

---

### Step 2 output — Welcome

```markdown
## Welcome to Clearpath

Clearpath keeps your team's work moving — you can see what's done, what's next, and who's on it at a glance.

**In the next 5 minutes, you'll create your first project, add a milestone, and mark it complete — so you can see how Clearpath tracks status in real time.**

Here's what we'll do:
1. Create a project — your team's home base for this work
2. Add a milestone — the first thing you'll aim to complete
3. Mark it done — and watch your project status update live
```

---

### Step 3 output — Onboarding steps

```markdown
## Step 1 of 4: Create your project

This is where your work lives. Give it a name and Clearpath takes care of the rest.

### What to do

1. Click **New Project** in the top-right corner of the dashboard.
2. Enter a project name, e.g., "Q2 Marketing Campaign".
3. Click **Create Project**.

### You should see

A new, empty project opens. The project header shows your name, a zero-milestone counter, and a status badge reading "Not started".

### If something's not right

- **New Project is greyed out:** your account may still be verifying — check your inbox for a confirmation email and click the link.

---

## Step 2 of 4: Add your first milestone

A milestone is a specific thing your team is aiming to finish. Adding one tells Clearpath what "done" looks like for this project.

### What to do

1. Click **Add milestone** inside the empty project view.
2. Enter a milestone name, e.g., "Draft brief approved".
3. Click **Save**.

### You should see

The milestone appears in the project view with a grey circle (not started) and your project status updates to "In progress".

### If something's not right

- **No Add milestone button:** make sure you're inside the project view, not the projects list. Click your project name to open it.

---

## Step 3 of 4: Assign the milestone to yourself

Assigning a milestone tells Clearpath who's responsible — so status stays accurate when things change.

### What to do

1. Click the milestone name "Draft brief approved".
2. Click **Assign** in the detail panel on the right.
3. Select your name from the list.

### You should see

Your name and avatar appear beside the milestone. The milestone detail panel shows "Assigned to: [Your name]".

### If something's not right

- **Your name isn't in the list:** your account invite may not be fully set up — sign out and sign back in, then try again.

---

## Step 4 of 4: Complete your first milestone

This is the moment. Mark the milestone done and watch Clearpath update your project status automatically.

### What to do

1. Click the grey circle beside "Draft brief approved".
2. The circle turns green and a completion time is recorded.

### You should see

The milestone circle turns green. The project status badge changes to "On track". The project header now shows "1 of 1 milestones complete".

### If something's not right

- **Circle won't turn green:** check that you're assigned to this milestone — only the assignee or a project admin can mark it complete.
```

---

### Step 4 output — Aha moment confirmation

```markdown
## You're set up!

You just tracked your first piece of work from open to complete — and saw Clearpath update your project status the moment it happened.

### What you just did
- Created a project your team can see and contribute to
- Added a milestone that defines what "done" means for this work
- Marked it complete and watched the project update in real time

### What to explore next

| If you want to... | Go here |
|---|---|
| Invite your team to this project | Settings → Members → Invite |
| Add more milestones with due dates | Inside your project → Add milestone → Set due date |
| See all your projects in one view | Dashboard → My projects |
```

---

### Step 5 output — Skip and abandon recovery

```markdown
## If a user skips or abandons at Step 2 (Add milestone)

**Empty-state nudge** (project view with no milestones):
You haven't added a milestone yet. Add one now to see how Clearpath tracks progress — it takes less than a minute.
[Primary action: "Add a milestone"]

**Re-engagement on next visit** (in-product tip, shown on first return):
Pick up where you left off — add your first milestone to see Clearpath in action.
[Primary action: "Resume setup"]

**Resume path:**
User lands directly on the Add milestone panel inside their project. Any project name they entered in Step 1 is preserved.

---

## If a user skips or abandons at Step 3 (Assign milestone)

**Empty-state nudge** (milestone detail panel, unassigned):
This milestone doesn't have an owner yet. Assign it so Clearpath can track who's responsible.
[Primary action: "Assign now"]

**Re-engagement on next visit** (in-product tip):
You're one step away from seeing Clearpath work — assign your milestone and mark it done.
[Primary action: "Resume setup"]

**Resume path:**
User lands on the milestone detail panel with the Assign dropdown pre-expanded.
```

---

### Step 6 output — Quality check table

| Check | Status |
|---|---|
| Time test | 4 steps at under 2 minutes each = well within 5-minute target |
| Aha moment reached | Yes — user sees real project status update, not just a configured state |
| No jargon | "Milestone" is a Clearpath product term; introduced in Step 2 with plain-language definition |
| One action per step | Each step does one thing: create project / add milestone / assign / complete |
| Expected results present | Every step has a "You should see" section |
| Escape hatches | Every step has "If something's not right" with a one-line fix |
| Progressive disclosure | Steps reveal one at a time; welcome shows only 3 steps |
| Example inputs provided | Step 1: "Q2 Marketing Campaign". Step 2: "Draft brief approved" |

---

### Full assembled output

```markdown
# Getting Started with Clearpath — New Users

**Time to complete:** 5 minutes
**What you'll accomplish:** Create your first project, add a milestone, and complete it — so you can see how Clearpath tracks status in real time.

## Welcome

Clearpath keeps your team's work moving — you can see what's done, what's next, and who's on it at a glance.

**In the next 5 minutes, you'll create your first project, add a milestone, and mark it complete — so you can see how Clearpath tracks status in real time.**

Here's what we'll do:
1. Create a project — your team's home base for this work
2. Add a milestone — the first thing you'll aim to complete
3. Mark it done — and watch your project status update live

## Step 1 of 4: Create your project

This is where your work lives. Give it a name and Clearpath takes care of the rest.

[... step content ...]

## Step 2 of 4: Add your first milestone

A milestone is a specific thing your team is aiming to finish...

[... step content ...]

## Step 3 of 4: Assign the milestone to yourself

Assigning a milestone tells Clearpath who's responsible...

[... step content ...]

## Step 4 of 4: Complete your first milestone

This is the moment. Mark the milestone done and watch Clearpath update your project status automatically.

[... step content ...]

## You're set up!

You just tracked your first piece of work from open to complete...

[... confirmation content ...]

---
Last verified: 2026-04-30
Product version: [version]
```

---

## Evaluation

### Criteria (skill definition)

- [x] PASS: Skill requires defining the value path first — Step 1 mandates completing a value path table (target user, aha moment, minimum steps, time target, drop-off risks) before any content is written — met
- [x] PASS: Skill requires an "aha moment" step — Step 4 is a dedicated required section titled "Write the aha moment confirmation", explicitly distinct from "completed setup", with a template requiring concrete outcomes and real product output — met
- [x] PASS: Skill requires a welcome step that contextualises what the user will achieve — Step 2 template mandates "In the next [N] minutes, you'll [specific outcome]" and rules require leading with the user's goal, not product features — met
- [x] PASS: Each onboarding step includes the benefit — Step 3 template includes "One sentence: why this step matters to THEM" as a required line in the step format — met
- [x] PASS: Skill requires progress indicators — Output Format uses "Step N of [N]:" headers on every step, making position-in-flow a structural requirement that cannot be omitted — met
- [x] PASS: Skill addresses skip/abandon — Step 5 is a full mandatory section with a template covering empty-state nudge, re-engagement on next visit, and resume path for each drop-off risk from Step 1 — met (full credit; it's required design, not a mention)
- [x] PASS: Skill uses plain language only — "No jargon" enforced in Step 2 welcome rules, Step 6 quality checklist, and the Rules section — met
- [x] PASS: Skill has valid YAML frontmatter — name, description, and argument-hint fields all present and correctly formed — met

**Criteria score: 8/8**

### Output expectations (simulated output)

- [x] PASS: Output defines the value path explicitly — Step 1 produces a completed value path table naming each element (target user, aha moment, minimum steps, time target, drop-off risk) before any UI copy — met
- [x] PASS: Output's welcome step contextualises what the user will achieve — "In the next 5 minutes, you'll create your first project, add a milestone, and mark it complete — so you can see how Clearpath tracks status in real time" — met
- [x] PASS: Output's per-step copy includes the benefit — Step 1: "This is where your work lives." Step 2: "A milestone is a specific thing your team is aiming to finish. Adding one tells Clearpath what 'done' looks like for this project." Benefit sentence present in every step — met
- [x] PASS: Output's progress indicator is named and specified — "Step 1 of 4:", "Step 2 of 4:", etc. on every step header; visible across the full flow — met
- [x] PASS: Output addresses skip/abandon paths — Step 5 covers two drop-off risks (milestone creation, milestone assignment) with empty-state nudge, re-engagement tip, and resume path for each — met
- [x] PASS: Output uses plain language only — "milestone" introduced with a plain-language definition on first use in Step 2; no other product jargon present — met
- [x] PASS: Output's onboarding length is appropriate — 4 steps to aha moment, under the 5-step limit; reasoning stated explicitly in the value path (minimum steps to see status update live) — met
- [~] PARTIAL: Output addresses celebration/reinforcement at the aha moment — Step 4 includes a celebration sentence ("You just tracked your first piece of work from open to complete") and a "What you just did" list; no animation, share-with-team prompt, or other visibility mechanics beyond text copy — partially met

**Output expectations score: 7.5/8**

**Combined score: 15.5/16 (97%)**

---

## Notes

The only gap is in aha moment celebration mechanics. The skill's Step 4 template produces strong text-based confirmation but does not require animation, share-with-team prompts, or any other visibility mechanisms that would make the value moment feel like an event. The criterion asks for these things; the skill produces copy without specifying how that copy is rendered or reinforced.

This is a genuine partial miss at the output level but an acceptable tradeoff for a documentation skill — rendering mechanics (confetti, modals, notifications) belong in the product's design spec, not a content skill. The skill could reasonably note that the aha moment copy should coordinate with a product design moment; it currently doesn't.

Everything else is tightly structured. The value path table in Step 1 is an effective forcing function — the template cannot be completed without naming the aha moment, minimum steps, and primary drop-off risk, which then drive every subsequent section. The skip/abandon step (Step 5) is genuinely required, not advisory.
