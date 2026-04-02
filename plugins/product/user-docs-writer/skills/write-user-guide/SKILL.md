---
name: write-user-guide
description: "Write a task-oriented user guide for a feature or workflow. Written in product language for non-technical readers. Produces step-by-step instructions with expected results and troubleshooting."
argument-hint: "[feature or workflow to document]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Write a user guide for $ARGUMENTS using the mandatory process and structure below.

**Core principle: A user guide answers "how do I do X?" for someone who has never done it before.** Every step is one action. Every action has an expected result. The reader never has to guess what to do next.

## Step 1 — Research the feature

Before writing, understand the complete workflow:

1. Search the codebase for the feature's UI components, routes, and handlers using `Grep` and `Glob`
2. Identify all the states the feature can be in (empty, loading, populated, error)
3. Find the permissions or roles required to access the feature
4. Check for existing documentation to avoid duplication
5. Identify the most common user tasks for this feature — prioritise by frequency

**Output:** A list of user tasks ranked by frequency, required permissions, and feature states.

## Step 2 — Write the guide header

```markdown
# [What the user wants to accomplish]

[One paragraph: what this guide covers, who it's for, and what you'll be able to do after reading it. Written as a promise to the reader.]

## Before you start

- **Required role:** [Specific role or permission — e.g., "Admin or Editor"]
- **Required plan:** [Plan tier, or "Available on all plans"]
- **You'll need:** [Any prior setup — e.g., "At least one project created"]
- **Time:** [Estimated minutes to complete]
```

**Rules for the header:**
- Title is what the user wants to DO, not what the feature IS. "Export your data as CSV" not "Data Export Feature"
- Prerequisites must be exhaustive — the reader should not hit a surprise permission wall at step 4
- If there are no prerequisites, state "No special requirements"

**Output:** Title, introduction paragraph, and prerequisites.

## Step 3 — Write step-by-step instructions

Numbered steps. Each step MUST follow this format:

```markdown
## Step N: [Action verb] [what to do]

[Optional: one sentence explaining why, if not obvious.]

1. [Navigate to exact location: "Go to **Settings** > **Team** > **Permissions**"]
2. [Specific action: "Click **Add Member**"]
3. [Input with example: "Enter the email address, e.g., `colleague@example.com`"]

**Expected result:** [What the user should see — e.g., "The new member appears in the team list with a 'Pending' badge."]
```

**Rules for steps:**
- **One action per step.** "Click Save and go to the next page" is two steps. Split them.
- **Use exact UI element names.** Read the actual UI and use those labels. Bold UI elements: "Click **Save**" not "click save." Do not paraphrase button labels.
- **Full navigation paths.** "Go to **Settings** > **Team** > **Permissions**" not "go to permissions."
- **Every step needs an expected result.** The reader must be able to confirm they're on track. Describe what they should SEE.
- **Include example inputs.** For every text field, dropdown, or selection, give a concrete example.
- **State timing for slow operations.** "This may take up to 30 seconds" or "The export will be emailed to you within 5 minutes."
- **Flag points of no return.** If a step is irreversible, warn before the action: "This cannot be undone. Make sure you've [verification step] before proceeding."

**Output:** Complete numbered steps with expected results.

## Step 4 — Write troubleshooting

Document the problems users are most likely to encounter:

```markdown
## Troubleshooting

### [Problem description — what the user sees]
**Why this happens:** [Cause in plain language]
**How to fix it:** [Specific steps to resolve]

### [Error message — quoted exactly as displayed]
**Why this happens:** [Cause]
**How to fix it:** [Steps]

### [Common mistake]
**Why this happens:** [What the user likely did]
**How to fix it:** [What to do instead]
```

Include at minimum:
- The most common error message for this workflow
- The most common user mistake (wrong permissions, wrong page, missing prerequisite)
- What happens if the user's environment differs (different browser, mobile vs desktop)

If there are no known issues, state: "No common issues reported. If you encounter a problem, contact support with the error message and the step where it occurred."

**Output:** Troubleshooting section with 3+ entries.

## Step 5 — Write related content and metadata

```markdown
## Related guides

- **[Next logical task]** — [one-line description with link]
- **[Alternative approach]** — [when to use this instead]
- **[Deeper topic]** — [for users who want to go further]

---
Last verified: [date]
Product area: [feature area]
Applies to: [plan tiers or "All plans"]
```

**Output:** Related guides section and metadata footer.

## Step 6 — Quality checks

| Check | Requirement |
|---|---|
| Task-oriented title | Does the title describe what the user wants to accomplish, not the feature name? |
| One action per step | Does each numbered step contain exactly one action? |
| Expected results | Does every step state what the user should see? |
| Exact UI labels | Are button names, menu items, and field labels quoted exactly as they appear? |
| Example inputs | Does every input field have a realistic example? |
| Full navigation paths | Does every "go to" instruction include the complete menu path? |
| No jargon | Would a non-technical user understand every term? |
| Troubleshooting present | Are the top 3 failure modes documented? |
| Prerequisites complete | Would a user with only the stated prerequisites succeed? |
| Tested | Have you verified every step against the actual product? |

## Rules

- Write for someone who has never used this feature before. Don't assume prior knowledge of the product beyond what's in the prerequisites.
- Use product language, not developer language. "Save your changes" not "persist the state." "Remove" not "delete the record." Match the vocabulary the user sees in the UI.
- Never write "simply," "just," or "easily." If it were simple, there wouldn't be a guide. These words make users feel bad when they struggle.
- Every step must be verifiable. If the user can't tell whether the step worked, the step is incomplete.
- Test every step yourself before publishing. If you cannot test (e.g., the feature isn't running), mark the guide as `Status: UNTESTED — verify before publishing`.
- Do not explain how the feature works internally. Users want to accomplish a task, not understand architecture. Save that for `/internal-docs-writer:write-architecture-doc`.
- Cross-reference `/user-docs-writer:write-kb-article` for common questions and `/user-docs-writer:write-onboarding` for first-time user flows.

## Output Format

```markdown
# [What the user wants to accomplish]

[Introduction paragraph]

## Before you start
[Prerequisites]

## Step 1: [Action]
[Instructions + expected result]

## Step 2: [Action]
[Instructions + expected result]

## Step N: [Final action]
[Instructions + expected result]

## Troubleshooting
[Common problems and fixes]

## Related guides
[Links to related content]

---
Last verified: [date]
Product area: [feature area]
Applies to: [plan tiers]
```
