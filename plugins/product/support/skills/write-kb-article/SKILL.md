---
name: write-kb-article
description: Write a knowledge base article from a resolved support issue, common question, or how-to topic.
argument-hint: "[topic, question, or resolved ticket summary]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

Write a knowledge base article for $ARGUMENTS using the mandatory structure and rules below.

## Step 1 — Research the topic

Before writing, gather all necessary information:

1. Search the codebase for relevant implementation details using `Grep` and `Glob`
2. Check for existing KB articles on the same or related topics to avoid duplication
3. If based on a support ticket, read the full ticket thread to understand the user's journey — what they tried, where they got stuck, what ultimately worked
4. Identify the product version or feature area this applies to

## Step 2 — Write the article

Use this exact structure. Every section is mandatory.

### Title

Write the title as the question the user would type into a search bar. Use their vocabulary, not internal terminology.

- Good: "How do I export my data as a CSV?"
- Bad: "Data Export Functionality Guide"
- Good: "Why am I getting a 'permission denied' error?"
- Bad: "Permission Error Troubleshooting Reference"

If you have access to source tickets, validate the title and short answer against the actual phrasing customers use. The title should match how users describe the problem (e.g. "export failing", "stuck on loading"), not how support describes the solution. Pull at least two ticket subject lines and confirm the title would be a plausible search query for someone who wrote one of them.

### Short answer

1-2 sentences that directly answer the question. This is for users who scan. It must be self-contained — a user who reads only this sentence should get the core answer.

- Good: "Go to Settings > Export > Download CSV. Your file will download immediately for datasets under 10,000 rows; larger exports are emailed to you."
- Bad: "Follow the steps below to learn about exporting."

Immediately after the short answer, add one sentence explaining WHY the constraint exists — the system behaviour the user is bumping into (e.g. "Exports time out at 30 seconds, so datasets over ~50,000 rows need to be split"). Users who understand the constraint stop fighting it; users who only have steps repeat the ticket the next time the situation differs.

### Prerequisites

List what the user needs before starting. Be explicit:
- Required role or permissions (e.g., "You must be an Admin or Owner")
- Required plan tier (e.g., "Available on Pro and Enterprise plans")
- Required tools or access (e.g., "You need access to the Admin Console")
- Required prior steps (e.g., "You must have already created a project")

If there are no prerequisites, state "No special requirements."

### Step-by-step instructions

Numbered steps. Each step MUST follow this format:

```
N. **[Action verb] [what to do]**
   [Exactly where to click/type/navigate — be precise about UI element names, menu paths, button labels]

   Expected result: [What the user should see after completing this step]
```

Rules for steps:
- One action per step. "Click Save and then navigate to..." is two steps.
- Use the exact names of UI elements as they appear in the product. Do not paraphrase button labels.
- Include the full navigation path: "Go to **Settings** > **Team** > **Permissions**" not "Go to permissions."
- If a step involves entering data, give a concrete example.
- If a step has a loading time or delay, mention it: "This may take up to 30 seconds."
- If a step can fail, note it: "If you see an error here, see the Troubleshooting section below."
- For any step where the UI element is non-obvious (a small icon, a hidden menu, a button in an unexpected location), add a screenshot — or, if you can't capture one, leave a placeholder: `![Screenshot: date filter in top-right of dashboard](TODO)`. Don't ship the article without flagging where visuals are needed.

### Troubleshooting

List the most common problems a user might encounter while following the steps. Format each as:

```
**Problem**: [What the user sees or experiences]
**Cause**: [Why this happens]
**Solution**: [How to fix it]
```

Include at minimum:
- The most common error message for this workflow
- The most common user mistake (wrong permissions, wrong page, missing prerequisite)
- What happens if the user's environment differs (different browser, mobile vs desktop, older version)

If there are no known issues, state: "No common issues reported. If you encounter a problem, contact support with the error message and the step where it occurred."

### Related articles

Link 3-5 related articles. Group them by relationship:

- **Next steps**: Articles the user is likely to need after completing this one
- **Related topics**: Articles covering related features or workflows
- **Background**: Articles explaining concepts referenced in this one

If related articles don't exist yet, list the titles that should be written and note them as "[To be created]".

### When the answer is a workaround

If the article's fix is a workaround rather than a real solution (e.g. "split your export into smaller batches" when the user has consistently large datasets), call that out and point to the real path. Examples:

- "If you're exporting datasets this size regularly, the date-range workaround is a band-aid. See API access for very large datasets, or contact support about an Enterprise plan."
- "This works for one-off cases. If you hit this every week, you want scheduled exports, not the manual fix above."

A power user who keeps hitting the same wall doesn't want a tidier workaround — they want to know there's a different door. Skip this section only when the fix actually solves the problem for everyone.

## Step 3 — Apply quality rules

Before finalising, verify the article against every rule:

| Rule | Check |
|---|---|
| One article, one question | Does this article answer exactly one question completely? If it answers two, split it. |
| User vocabulary | Are all terms the ones a user would use? Replace any internal jargon. |
| Scannable | Can a user find their answer without reading the whole article? (short answer, headings, bold key terms) |
| Testable | Could someone follow these steps on the live product right now and succeed? |
| Version-aware | If the answer is version-specific, is the version stated clearly at the top? |
| No assumptions | Does every step specify exactly where to go and what to click? No "navigate to the relevant section." |
| Error-path covered | Are the most common failure modes documented in Troubleshooting? |

## Step 4 — Add metadata

At the end of the article, include:

```
---
Last verified: [today's date]
Product area: [feature area]
Applies to: [plan tiers, or "All plans"]
Tags: [3-5 searchable tags]
---
```

## Maintenance rules

KB articles are living documents. Include this maintenance note at the bottom:

- **Update trigger**: This article must be reviewed when the [feature area] changes in a product release.
- **Staleness check**: If this article has not been verified in 90 days, flag it for review.
- **Helpfulness tracking**: If available, track article views vs. support tickets on the same topic. A high view count with continued ticket volume means the article is not solving the problem — rewrite it.
- **Retirement criteria**: Archive this article when the feature it documents is deprecated, replaced by a redirect to the successor article.

## Related Skills

- `/support:triage-tickets` — KB articles reduce ticket volume. When a triaged topic has high recurrence, write an article.
- `/support:feedback-synthesis` — feedback synthesis identifies the topics that most need KB coverage.
