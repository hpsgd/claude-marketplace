# Write onboarding

Testing whether the write-onboarding skill defines a value path before writing content, includes an "aha moment" confirmation step, and measures progress toward first value.

## Prompt

> /user-docs-writer:write-onboarding for new Clearpath users — the in-product onboarding experience that takes someone from account creation to completing their first project milestone.

## Output

**Getting Started with Clearpath — New User**


| Field | Value |
|---|---|
| Time to complete | 5 minutes |
| What you'll accomplish | Complete your first project milestone with your team. |


**Value path (Step 1 — before writing):**

| Element | Definition |
|---|---|
| Target user | New account holder, likely a project manager, no Clearpath experience |
| Aha moment | User sees their first completed task inside a project with at least one teammate |
| Minimum steps | 5: create workspace → invite teammate → create project → assign task → mark complete |
| Time target | 5 minutes |
| Primary drop-off risk | Step 3 — too many project options presented at once |

**Welcome:**

> Welcome to Clearpath
>
> In the next 5 minutes, you'll set up your workspace and complete your first project milestone together.
>
> Here's what we'll do:
> 1. Invite a teammate
> 2. Create your first project
> 3. Assign and complete your first task

**Step 1 of 5: Invite your first teammate**

Working alone is fine, but Clearpath shows its value when your team can see each other's work.

1. Click **Invite team members** in the sidebar.
2. Enter a colleague's email address, e.g. `colleague@example.com`.
3. Click **Send invite**.
   Your teammate receives an email. They appear in your workspace as "Pending" until they accept.

**Step 5 of 5: Complete your first task**

When a task is marked complete, everyone on the project can see it instantly.

1. Open your project.
2. Find the task you just created and click the checkbox next to it.
   The task moves to "Completed" and shows your name and timestamp.

**You're set up!**

You've completed your first project milestone in Clearpath. Here's what you just did:
- Created your first project with live collaboration
- Assigned a task to a team member
- Completed your first tracked milestone

**What to explore next:**

| If you want to... | Go here |
|---|---|
| Add more team members | Settings > Team |
| Start tracking time | Time Tracking guide |
| Set up notifications | Settings > Notifications |

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 criteria met (93.75%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Value path defined first — Step 1 "Define the value path" is the first step and must be completed before writing any content. The skill requires a completed value path table (target user, aha moment, minimum steps, time target, primary drop-off risk) as its output before Step 2 begins.
- [x] PASS: Aha moment confirmation required — Step 4 "Write the aha moment confirmation" is a required step with an explicit template. Rules state "Name what they accomplished, not what features they used." The completion screen template requires specific outcomes ("Created your first project with live data") not generic confirmation ("Setup complete"). Directly enforced.
- [x] PASS: Welcome contextualises outcome — Step 2 requires "In the next [N] minutes, you'll [specific outcome]" as mandatory. The rule "Lead with the user's goal, not the product's features" explicitly rejects greeting-only welcomes.
- [x] PASS: Benefit per step required — Step 3's step format mandates "[One sentence: why this step matters to THEM.]" before the "What to do" list. Instruction-only steps are not the required format. The template cannot be followed without the benefit sentence.
- [x] PASS: Progress indicators required — the Output Format template now uses "## Step 1 of [N]:", "## Step 2 of [N]:", "## Step 3 of [N]:" headers. This is a structural requirement in the output template: every step header must include the total count. A contributor following the template produces "Step N of M" headers at every step, giving users their position within the full flow.
- [~] PARTIAL: Skip/abandon handling — Step 1 requires identifying "Primary drop-off risk" in the value path table. Step 3 mandates an "If something's not right" escape hatch per step. Step 5 quality checks include "Escape hatches." Abandonment recovery (what the product shows when a user returns after leaving mid-flow) is not addressed. Criterion ceiling is PARTIAL per its prefix. Score: 0.5.
- [x] PASS: Plain language only — Rules section states "No jargon. If the product has specific terminology, introduce it in context later." Step 5 quality check explicitly requires "No jargon: Would a first-time user understand every term without a glossary?" Both enforce this.
- [x] PASS: Valid YAML frontmatter — contains `name: write-onboarding`, `description`, and `argument-hint` fields.

## Notes

Criterion 5 now passes. The output template was updated to use "Step N of [N]:" heading format throughout — "## Step 1 of [N]: [First action]", "## Step 2 of [N]: [Second action]", etc. This is a structural requirement: the template cannot be followed without producing "Step N of M" headers, which tell users their position in the total flow at every step.

The verdict moves from PARTIAL (81%) to PASS (93.75%). The one remaining gap is abandonment recovery (criterion 6), which has a PARTIAL ceiling. The skill handles drop-off risk identification and per-step escape hatches, but not the re-entry state when a user returns after abandoning mid-flow. That's a real omission given the value path step explicitly asks about drop-off risks — the connection to recovery UX isn't made.
