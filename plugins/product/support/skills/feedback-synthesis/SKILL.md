---
name: feedback-synthesis
description: Synthesise customer feedback into themes — aggregate issues, feature requests, and praise from support tickets, reviews, or survey responses.
argument-hint: "[path to feedback data, or 'recent' to scan support/issue trackers]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Synthesise feedback from $ARGUMENTS using the mandatory process below. Every step is required.

## Step 1 — Ingest all feedback

Read every piece of feedback in the input. If pointed at files or directories, use `Glob` and `Read` to pull them. Count the total number of data points before proceeding.

For each piece of feedback, extract:
- **Source** — where it came from (support ticket, NPS survey, app review, social media, sales call, etc.)
- **Date** — when it was submitted (or "undated" if unknown)
- **User segment** — plan tier, role, tenure, or any available segmentation
- **Raw quote** — the user's exact words (preserve verbatim, do not paraphrase yet)
- **Sentiment** — positive, negative, neutral, or mixed

## Step 2 — Categorise each data point

Assign exactly one primary category:

| Category | Definition | Examples |
|---|---|---|
| Bug report | Something is broken or behaving incorrectly | "The export button doesn't work," "I get an error when..." |
| Feature request | User wants something that doesn't exist | "It would be great if...," "Can you add...," "I wish..." |
| Usability issue | Feature exists but is confusing, slow, or hard to find | "I couldn't figure out how to...," "It took me 20 minutes to..." |
| Praise | Positive feedback about something specific | "Love the new dashboard," "Support was incredibly fast" |
| Complaint | General dissatisfaction, often emotional, without a specific technical issue | "This is frustrating," "I'm considering switching" |
| Question | User doesn't understand something (signals a docs/onboarding gap) | "How do I...?," "What does X mean?" |

If a single piece of feedback contains multiple categories (e.g., praise + feature request), split it into separate data points.

## Step 3 — Build themes

Group related feedback into themes. Mandatory rules for theming:

1. **Use the user's language** — theme names must come from what users actually said, not internal jargon. "Can't find the export button" not "Export discoverability deficit." "Wish I could bulk edit" not "Batch operations enhancement."
2. **Merge only when the root cause is the same** — "slow dashboard" and "slow reports" are different themes unless they share a root cause. When uncertain, keep them separate.
3. **Every theme needs 2+ data points** — a single data point is not a theme, it's an outlier. List outliers separately.
4. **Sub-themes are allowed** — if a theme has 10+ data points, break it into sub-themes for clarity.
5. **Preserve representative quotes** — select 2-3 direct quotes per theme that best capture the sentiment and specifics. Choose quotes that are vivid and concrete, not generic.

## Step 4 — Quantify and trend

For each theme, calculate:

- **Count** — total data points in this theme
- **Percentage** — of total feedback
- **Category breakdown** — how many are bugs vs. feature requests vs. complaints, etc.
- **Sentiment balance** — ratio of positive to negative within the theme
- **Trend direction** — if dates are available: increasing, stable, or decreasing over time. If dates are unavailable, state "trend unknown."
- **Segment concentration** — is this theme concentrated in a specific user segment? (e.g., "80% from enterprise users," "mostly new users in first 30 days")

## Step 5 — Pattern detection

Scan for these specific patterns and flag any that apply:

| Pattern | Detection rule | Action |
|---|---|---|
| Escalating issue | Theme count increasing over 3+ time periods | Flag as urgent, likely getting worse |
| Silent churn signal | Complaints + no feature requests from same users | These users have stopped asking and may leave |
| Onboarding gap | Questions or usability issues concentrated in new users | Recommend onboarding improvements |
| Power user friction | Feature requests from high-usage or enterprise users | Prioritise — these users are invested |
| Praise cluster | Praise concentrated on a specific feature | Protect this feature from regression, use in marketing |
| Bug-complaint bridge | Bug reports and complaints referencing the same area | Bug is causing broader dissatisfaction |

## Step 6 — Prioritise

Score each theme using:

**Impact = Severity × Frequency × Segment weight**

Where:
- Severity: Critical (4), High (3), Medium (2), Low (1)
- Frequency: use the count directly
- Segment weight: Enterprise/paid (1.5×), Free (1.0×), Unknown (1.0×)

Sort themes by impact score descending.

## Step 7 — Output

### Feedback summary

- **Total data points analysed**: [N]
- **Date range**: [earliest] to [latest]
- **Sources**: [list with counts]
- **Overall sentiment**: [positive/negative/mixed with percentages]

### Theme table

| Rank | Theme | Category | Count | % | Trend | Segment | Impact score | Representative quotes |
|---|---|---|---|---|---|---|---|---|
| 1 | ... | ... | ... | ... | ... | ... | ... | "..." |

### Patterns detected

List any patterns from Step 5 that were found, with evidence.

### Top 3 recommendations

Each recommendation MUST:
1. **Name the theme it addresses** — with the count and trend
2. **State the specific action** — not "improve X" but "add bulk edit to the contacts page" or "rewrite the export documentation with screenshots"
3. **Provide the evidence** — cite the quotes and counts that support this recommendation
4. **Estimate the reach** — how many users or what percentage of feedback this would address

Format:

```
### Recommendation 1: [action]
Theme: [theme name] ([N] data points, [trend])
Evidence: [2-3 quotes]
Reach: [N users / N% of feedback]
Rationale: [why this matters and why now]
```

### Outliers

List any single data points that didn't fit into themes but are worth noting (novel ideas, early signals, unusual requests).

## Rules

- Never discard feedback because it's inconvenient or contradicts a product direction. Report what users said, not what the team wants to hear.
- Quantify everything. "Users are unhappy" is not a finding. "23 of 45 feedback items (51%) express frustration with search" is.
- Distinguish between what users say they want (stated needs) and what their behaviour suggests they need (latent needs). Note the distinction when relevant.
- If the sample size is small (<30 data points), caveat conclusions explicitly: "Based on a small sample — validate before acting."

## Related Skills

- `/support:triage-tickets` — triaged tickets are the primary input for feedback synthesis. Triage first, then synthesise.
- `/support:write-kb-article` — when synthesis reveals a recurring user problem, write a KB article to address it.
