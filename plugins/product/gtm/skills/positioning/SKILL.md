---
name: positioning
description: Define product positioning using the April Dunford framework — competitive alternatives, unique attributes, value, target customer, market category.
argument-hint: "[product or feature to position]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep, WebSearch
---

Define positioning for $ARGUMENTS using the April Dunford framework. Follow the five steps below in exact order — the sequence matters because each step builds on the previous one.

## Why this order matters

Most positioning exercises start with the market category ("we're a CRM") and work backwards. This is wrong. You don't get to pick your category until you understand what makes you different and who cares. Dunford's framework starts with competitive alternatives and works forward to the category that makes your value obvious.

## Step 1 — Competitive alternatives

**Question: If your product didn't exist, what would customers do instead?**

List every alternative. Be honest and thorough. Include:

- **Direct competitors** — products in the same category doing the same thing
- **Adjacent competitors** — products in a neighbouring category that solve the same underlying problem
- **Manual processes** — spreadsheets, email, pen and paper, hiring a person
- **Status quo** — doing nothing, living with the problem
- **In-house solutions** — building it themselves, internal tools

Rules:
- List at least 5 alternatives. If you can only think of 2, you haven't looked hard enough.
- The most dangerous competitors are often not the ones that look like you — they're the ones your customers are actually using today.
- "Do nothing" is always a competitor. If the pain isn't bad enough to change, you lose to inertia.
- Rank alternatives by how frequently customers actually choose them (not by how similar they are to your product).

Output for Step 1:

| Alternative | Type | How often chosen | Why customers pick it |
|---|---|---|---|
| [name] | Direct / Adjacent / Manual / Status quo / In-house | High / Medium / Low | [reason] |

## Step 2 — Unique attributes

**Question: What do you have that the alternatives don't?**

For each competitive alternative from Step 1, identify what your product does that it cannot. These must be:

- **Factually true** — you actually have this, right now, not on the roadmap
- **Verifiable** — a customer could confirm this in a demo or trial
- **Unique** — the alternative genuinely lacks this, not "we do it slightly better"

Categories of attributes:
- Features or capabilities (technology, integrations, functionality)
- Architecture or approach (how you solve the problem, not just what you solve)
- Business model (pricing, packaging, terms)
- Team or expertise (domain knowledge, support quality)
- Community or ecosystem (partners, marketplace, user community)

Output for Step 2:

| Unique attribute | Why it matters | Which alternatives lack it |
|---|---|---|
| [attribute] | [what this enables] | [list of alternatives] |

Rules:
- "Better UX" is not an attribute. "3-step setup vs. 12-step wizard" is.
- "Faster" is not an attribute. "Sub-100ms response time vs. 2-3 second average" is.
- If you can't be specific, the attribute isn't real yet.
- Discard attributes that are table stakes (everyone has them or will soon).
- Keep only the attributes that create genuine separation from alternatives.

## Step 3 — Value mapping

**Question: What does each unique attribute enable for the customer?**

Map every unique attribute from Step 2 to the customer value it delivers. Move from feature → capability → outcome → business impact.

| Unique attribute | Capability it creates | Outcome for the user | Business impact |
|---|---|---|---|
| [attribute] | [what it lets them do] | [what changes in their workflow] | [revenue, cost, risk, time] |

Rules:
- Value must be stated in customer terms, not product terms. "Automated data pipeline" is product. "Spend zero engineering hours on data sync" is value.
- Every attribute must connect to a business impact. If it doesn't move revenue, reduce cost, mitigate risk, or save time — it's not a value, it's a feature.
- The best value propositions are quantifiable: "Save 10 hours per week" beats "Save time."
- If an attribute doesn't map to meaningful value, drop it. Not every feature matters for positioning.

## Step 4 — Target customer

**Question: Who cares most about the value you deliver?**

Define the customer segment that gets the most value from your unique attributes. Be specific — "everyone" is not a target.

Define the target using:

- **Company characteristics** — size, industry, stage, tech stack, growth rate
- **Buyer role** — title, department, what they're responsible for
- **Situation** — what trigger or pain point makes them look for a solution right now?
- **Current behaviour** — what are they using today (from Step 1)?
- **Must-have requirements** — what do they absolutely need that you absolutely have?

The best target customers have ALL of these properties:
1. They feel the pain your product solves acutely
2. They recognise the value of your unique attributes immediately
3. They have the budget and authority to buy
4. They can be reached through channels you can afford
5. They will tell others (word of mouth potential)

Output for Step 4:

```
Target customer profile:

Company: [characteristics]
Buyer: [role and responsibilities]
Trigger: [what makes them start looking]
Current solution: [what they use today]
Must-haves: [requirements that match your unique attributes]
Deal-breakers: [what would disqualify your product]
```

Rules:
- Start narrow. "Mid-market SaaS companies with 50-200 employees who have outgrown spreadsheet-based customer tracking" is better than "businesses who need a CRM."
- The target customer is not everyone who could use your product. It's the segment that would be most disappointed if your product disappeared.
- If your target customer description doesn't exclude anyone, it's too broad.

## Step 5 — Market category

**Question: What frame of reference makes your value obvious to your target customer?**

The market category is the context you set so customers immediately understand what you do and why it matters. You have three strategic options:

| Strategy | When to use | Example |
|---|---|---|
| **Existing category** | Your differentiators are clear within the category | "CRM for real estate teams" |
| **Subcategory** | You want the benefits of the existing category but need to stand apart | "Conversational CRM" (new kind of CRM) |
| **New category** | No existing category captures your value, and you have the resources to educate the market | "Revenue Operations Platform" |

Rules:
- Default to an existing category unless you have a strong reason not to. Creating a new category is expensive and slow.
- The category should make your value proposition obvious. If you have to explain what the category means, it's the wrong category.
- Test: can your target customer understand what you do in under 10 seconds with this category?
- The category name must pass the "Google test" — would your target customer search for this term?

## Step 6 — Assemble the positioning

### Positioning canvas

```
┌─────────────────────────────────────────────────┐
│ COMPETITIVE ALTERNATIVES                         │
│ [list from Step 1]                               │
├─────────────────────────────────────────────────┤
│ UNIQUE ATTRIBUTES         │ VALUE               │
│ [from Step 2]              │ [from Step 3]       │
├─────────────────────────────────────────────────┤
│ TARGET CUSTOMER                                  │
│ [from Step 4]                                    │
├─────────────────────────────────────────────────┤
│ MARKET CATEGORY                                  │
│ [from Step 5]                                    │
└─────────────────────────────────────────────────┘
```

### Positioning statement

Use this template:

```
For [target customer] who [situation/trigger],
[product] is a [market category]
that [key value proposition].
Unlike [primary competitive alternative],
[product] [primary unique attribute and its value].
```

Write one version. Then write a tighter version. Use the tighter one.

### Tagline

Distil the positioning into one sentence (under 10 words). The tagline should:
- Communicate the primary value, not the feature
- Be specific to your target customer
- Pass the "competitor test" — could a competitor truthfully say the same thing? If yes, it's too generic.

Bad: "The better way to manage your business"
Good: "Ship customer emails in minutes, not sprints"

### Sales narrative

Write a 3-sentence version a salesperson could use in conversation:

```
Sentence 1: [The problem your target customer has — stated in their words]
Sentence 2: [What your product does about it — stated as the outcome, not the feature]
Sentence 3: [Why you specifically — the unique attribute that alternatives lack]
```

## Step 7 — Validation questions

After completing the positioning, test it against these questions. If the answer to any is "no," revisit the relevant step.

| Question | Tests | If "no" |
|---|---|---|
| Would your best customers agree with the competitive alternatives list? | Step 1 accuracy | Talk to customers |
| Are your unique attributes truly unique, or will competitors match them in 6 months? | Step 2 durability | Find more defensible attributes |
| Does the value resonate with target customers in their own words? | Step 3 relevance | Reframe in customer language |
| Would your target customer self-identify with your description? | Step 4 specificity | Narrow the target |
| Does the market category help or confuse? | Step 5 clarity | Choose a different frame |
| Could your positioning be mistaken for a competitor's? | Overall differentiation | The whole thing needs work |
| Can a new employee explain what you do after reading this? | Clarity | Simplify |

## Rules

- Positioning is not aspirational. It describes what is true today, not what you hope will be true next quarter.
- Specificity beats breadth. Positioning that tries to appeal to everyone appeals to no one.
- The customer's language always wins over internal jargon. If customers call it "email blasts," don't position around "campaign orchestration."
- Positioning must be revisited when: you launch a major feature, a competitor shifts strategy, your target customer changes, or your win/loss reasons change.
- Good positioning makes marketing, sales, and product decisions easier. If it doesn't help the team make decisions, it's not specific enough.

## Related Skills

- `/gtm:competitive-analysis` — run a competitive analysis before positioning to understand the landscape you're positioning against.
- `/gtm:launch-plan` — positioning feeds directly into launch messaging and materials.
