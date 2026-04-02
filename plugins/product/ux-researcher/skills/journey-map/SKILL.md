---
name: journey-map
description: "Map a customer journey — stages, touchpoints, actions, emotions, pain points, and opportunities. Use for understanding end-to-end user experience or identifying friction."
argument-hint: "[user type and journey to map, e.g. 'new user onboarding' or 'enterprise procurement']"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Journey Map

Map the customer journey for $ARGUMENTS.

## Process

### Step 1: Define scope

- **User type:** Who is taking this journey? Be specific (not "users")
- **Journey:** Which journey? (discovery, evaluation, onboarding, core task, support, renewal, expansion)
- **Start point:** Where does the journey begin? (first awareness, signup, first login)
- **End point:** Where does it end? (task completed, value achieved, churned)

### Step 2: Identify evidence sources

Before mapping, gather evidence:
- Support tickets (what users complain about at each stage)
- Analytics (where users drop off, how long each stage takes)
- Existing documentation (onboarding guides, help articles)
- Feature usage data (what gets used, what gets ignored)

### Step 3: Map stages

For each stage of the journey:

| Element | What to capture |
|---|---|
| **Stage name** | The phase (Awareness, Evaluation, Signup, Onboarding, First Value, Ongoing Use) |
| **User goal** | What the user is trying to achieve at this stage |
| **Touchpoints** | Every interaction point (website, app, email, docs, support, social) |
| **Actions** | What the user does (searches, clicks, reads, configures, asks for help) |
| **Thinking** | Questions and concerns ("Is this the right tool?", "How do I set this up?") |
| **Feeling** | Emotional state (confident, confused, frustrated, delighted, anxious) |
| **Pain points** | Friction, confusion, delays, dead ends |
| **Opportunities** | How to improve this stage |

### Step 4: Identify critical moments

- **Moment of truth:** The make-or-break interaction (usually first value or first error)
- **Biggest drop-off risk:** Where users are most likely to leave
- **Delight opportunity:** Where exceeding expectations has disproportionate impact
- **Time to first value:** How long from signup to genuine value — the metric that predicts retention

### Output

```markdown
## Journey: [name] — [user type]

### Overview
- Start: [where the journey begins]
- End: [where the journey ends]
- Critical metric: [time to first value, completion rate, etc.]
- Evidence sources: [what data informed this map]

### Stage 1: [name]
**Goal:** [what the user wants]

| Touchpoint | Action | Thinking | Feeling | Pain points |
|---|---|---|---|---|
| [channel] | [action] | [question] | [emotion] | [friction] |

**Opportunities:** [improvements]

[Repeat for each stage]

### Critical Moments
1. **Moment of truth:** [description]
2. **Biggest drop-off risk:** [where and why]
3. **Delight opportunity:** [where and how]

### Recommendations (prioritised by impact)
1. [Fix] — affects [stage], expected impact [metric improvement]
2. [Fix]
3. [Fix]
```
