---
name: social-media-footprint
description: "Map publicly visible social media presence for a person or organisation across platforms. Public content only — no access to locked, private, or friends-gated content."
argument-hint: "[person or organisation name]"
user-invocable: true
allowed-tools: WebSearch, WebFetch
---

Map the public social media footprint for $ARGUMENTS.

> [!IMPORTANT]
> For people (not organisations): this skill requires the investigator agent's full authorisation gate before invocation.

## Step 1: Platform search

Search for the subject on each platform. For organisations, look for official accounts. For individuals, look for public profiles.

| Platform | Search method |
|---|---|
| LinkedIn | Name search; for organisations, company page search |
| Twitter/X | `twitter.com/search?q=[name]` or name search |
| Facebook | Name/page search — public content only |
| Instagram | Username search — public accounts only |
| TikTok | Username search |
| YouTube | Channel search |
| GitHub | Username or organisation search |
| Reddit | Username search (for individuals who post publicly under their name) |

Record: account URL, handle, follower/subscriber count, account creation date if visible, posting cadence (active / occasional / dormant).

## Step 2: Username patterns

Once a username is found on one platform, search the same username across others.

Tools: [Namechk](https://namechk.com) (public availability search), manual search on major platforms.

Consistent usernames across platforms are a strong identity signal. Inconsistent ones may indicate separate accounts for different contexts (professional vs personal).

## Step 3: Content assessment

For each active account, review public posts to establish:

- Primary topics and themes
- Tone and audience (professional, community, personal expression)
- Posting frequency and recency
- Notable public statements or positions
- Engagement patterns (comments, shares, replies from others)

Scope: public content only. Do not attempt to view locked, private, or friends-gated content by any means.

## Step 4: Organisational accounts (organisations only)

For organisation investigations, map:

- Official verified accounts vs unofficial fan/community pages
- Employee accounts that post about work publicly
- Executive accounts (often the most informative signal of direction and culture)
- Product-specific sub-accounts

## Rules

- Public content only. No access to locked, private, or friends-gated content — this is a hard limit with no exceptions.
- Don't screen-scrape, don't attempt to infer private content, don't attempt to bypass platform access controls.
- For individuals: scope to public professional presence unless the gate record explicitly expands to personal accounts.
- Content assessment produces observations, not character conclusions. "Posts frequently about [topic]" is an observation. "This person is [character judgement]" is not your call.
- A well-curated, private social presence is a finding. It means the subject is intentional about their public footprint.

## Output format

```markdown
### Social media footprint: [Name]

**Gate record (if individual):** [link or copy]
**Date:** [today]

#### Accounts found

| Platform | Account/URL | Followers | Cadence | Notes |
|---|---|---|---|---|

#### Username pattern

[Consistent handle across platforms — or variation noted]

#### Content themes

[Per active platform: primary topics, tone, notable content — public only]

#### Organisational accounts (if applicable)

[Official vs unofficial, executive accounts, product accounts]

#### Accounts not found

[Platforms searched with no results — absence noted as finding]

#### Observations

[Patterns, gaps, anomalies worth noting]
```
