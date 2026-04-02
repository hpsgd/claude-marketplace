---
name: write-integration-guide
description: "Write a step-by-step integration tutorial — connecting your product with another service, framework, or platform. Produces a complete, runnable guide from prerequisites through working example."
argument-hint: "[integration target, e.g. 'Stripe payments' or 'GitHub webhooks']"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Write an integration guide for $ARGUMENTS using the mandatory process and structure below.

## Step 1 — Research the integration

Before writing, understand what you're documenting:

1. Search the codebase for existing integration code, SDK usage, or API calls related to the target using `Grep` and `Glob`
2. Identify the authentication method (API keys, OAuth, webhooks, etc.)
3. Find configuration files, environment variables, and dependencies required
4. Check for existing documentation or examples to avoid duplication
5. Identify the minimum viable integration — what is the smallest working example?

**Output:** A list of endpoints/methods used, auth requirements, dependencies, and the scope of the guide.

## Step 2 — Write the guide header

Every integration guide starts with a clear promise and context:

```markdown
# Integrating [Product] with [Target]

[One sentence: what the reader will have built by the end of this guide.]

## What you'll build

[2–3 sentences describing the working integration. Be specific — not "connect to Stripe" but "accept one-time payments using Stripe Checkout, with webhook handling for payment confirmation."]

## Prerequisites

- [ ] [Account/access requirement] — sign up at: [link]
- [ ] [API key or credential] — get it from: [exact location in dashboard]
- [ ] [Tool or dependency] — install: `[command]`
- [ ] [Language/framework version] — minimum: [version]
- [ ] [Prior knowledge or setup] — see: [link to prerequisite guide]
```

**Rules for prerequisites:**
- Every credential must say where to find it — never just "an API key"
- Every tool must include the install command
- Every prerequisite that takes more than 5 minutes to obtain gets a time warning

**Output:** Completed guide header with all prerequisites.

## Step 3 — Write the step-by-step integration

Numbered steps. Each step MUST follow this format:

```markdown
## Step N: [What you're doing and why]

[1–2 sentences explaining what this step accomplishes.]

\`\`\`[language]
[Complete, copy-pasteable code — not fragments]
\`\`\`

**What this does:** [Explain the non-obvious parts of the code]

**Expected result:**
\`\`\`
[What the reader should see — console output, API response, or UI state]
\`\`\`
```

**Rules for steps:**
- **One concept per step.** "Install the SDK and configure authentication" is two steps.
- **Every code block must be copy-pasteable.** No `<placeholder>` without explaining what to substitute and how to find the value.
- **Show the full file context** on first introduction, then show only the changed lines in subsequent steps. Mark additions clearly.
- **Every step needs expected output.** The reader must be able to confirm what they see matches what they should see.
- **Use realistic data in examples.** Not `"test"`, `"foo"`, or `"YOUR_VALUE"` — use plausible values like `"acct_1A2B3C"` or `"sk_test_abc123"`.
- **State environment variables explicitly.** Show how to set them: `export STRIPE_SECRET_KEY=sk_test_...  # From your Stripe dashboard > Developers > API keys`

**Output:** Complete numbered steps covering install, configure, implement, and verify.

## Step 4 — Write the complete example

After the step-by-step, provide a single, complete, runnable example that combines everything:

```markdown
## Complete example

Here's the full integration in one place. You can use this as a starting point.

\`\`\`[language]
[Complete working code — every import, every config line, every handler.
 A reader should be able to copy this entire block into a new file and run it.]
\`\`\`

**Run it:**
\`\`\`bash
[Exact command to run the example]
\`\`\`

**Expected result:**
\`\`\`
[What success looks like]
\`\`\`
```

This is mandatory — fragments scattered across steps are not enough. Developers want to clone and run.

**Output:** A single self-contained code example.

## Step 5 — Write troubleshooting and next steps

```markdown
## Troubleshooting

### [Error message or symptom]
**Cause:** [Why this happens]
**Fix:** [How to resolve it]

### [Common mistake]
**Cause:** [Why developers hit this]
**Fix:** [What to do instead]

## Next steps

- [Natural follow-on: "Add webhook signature verification" with link]
- [Scaling concern: "Handle high-volume events with a queue"]
- [Related guide: "See the [SDK guide](/path) for advanced configuration"]
```

Include at minimum:
- The most common authentication error
- The most common configuration mistake
- What happens if the external service is unavailable

**Output:** Troubleshooting section with 3+ entries, and next steps with links.

## Step 6 — Quality checks

| Check | Requirement |
|---|---|
| Complete example runs | Can someone copy the complete example into a new project and have it work? |
| Every step has expected output | Does the reader know what success looks like at every point? |
| No placeholder credentials | Are all `YOUR_KEY` values explained with where to find them? |
| Prerequisites are exhaustive | Will the reader hit a "you need X" surprise at step 5? |
| Realistic data | Are examples using plausible values, not "foo" or "test"? |
| External links present | Are sign-up pages, dashboard locations, and reference docs linked? |
| Troubleshooting covers auth | Is the most common auth failure documented? |

## Rules

- The complete example is non-negotiable. An integration guide without a runnable example is a recipe, not a guide.
- Write for a developer who knows their own stack but has never used the target service. Don't explain what an API key is — do explain where to find this specific one.
- If the integration requires a test/sandbox environment, use it in all examples and state this clearly. Never show production credentials or URLs in examples.
- Every external link must point to the official documentation of the target service. Do not link to blog posts or third-party tutorials.
- If the integration has breaking version differences, state the version this guide covers in the header and note any version-specific steps.
- Cross-reference the `/developer-docs-writer:write-sdk-guide` skill if the integration involves an SDK, and `/developer-docs-writer:write-api-docs` for the underlying API reference.

## Output Format

```markdown
# Integrating with [Service Name]

## Prerequisites
- [Runtime/language version]
- [Account/credentials needed — with link to where to get them]
- [Dependencies to install]

## Quick Start
[Fewest steps to a working integration — 5 minutes or less]

## Complete Example
[Full, runnable code with comments explaining each section]

## Step-by-Step Walkthrough
### Step 1: [Authentication]
[Code + expected output]

### Step 2: [Core operation]
[Code + expected output]

### Step N: [Final step]
[Code + expected output]

## Troubleshooting
| Symptom | Cause | Fix |
|---|---|---|
| [error message] | [why it happens] | [how to fix] |

## Next Steps
- [Link to full API reference]
- [Link to SDK guide if applicable]
- [Link to advanced use cases]
```
