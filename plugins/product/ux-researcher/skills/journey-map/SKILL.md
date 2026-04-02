---
name: journey-map
description: "Map a customer journey — stages, touchpoints, actions, emotions, pain points, and opportunities. Produces a structured journey map with critical moments and prioritised recommendations. Use for understanding end-to-end user experience or identifying friction across touchpoints."
argument-hint: "[user type and journey to map, e.g. 'new user onboarding' or 'enterprise procurement']"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Journey Map

Map the customer journey for $ARGUMENTS using the mandatory process below.

## Step 1: Define scope (mandatory)

```markdown
### Journey scope

| Element | Definition |
|---|---|
| **User type** | [Specific — not "users" but "first-time evaluator on free trial"] |
| **Journey** | [Which journey: discovery, evaluation, onboarding, core task, support, renewal, expansion] |
| **Start point** | [Where the journey begins — first awareness, signup, first login] |
| **End point** | [Where it ends — task completed, value achieved, churned] |
| **Success metric** | [The number that tells you this journey is working — time-to-first-value, completion rate, NPS] |
```

**Rules for scope:**
- One journey per map. "The entire user experience" is not a journey — it's 5 journeys
- The user type must be specific enough that you can walk the journey as them. Reference a persona from `/ux-researcher:persona-definition` if available
- Start and end points must be concrete events, not states

**Output:** Journey scope table.

## Step 2: Gather evidence (mandatory)

Before mapping, identify what data informs each stage:

```markdown
### Evidence sources

| Source | What it tells us | Coverage |
|---|---|---|
| Support tickets | Where users get stuck, what they complain about | [stages covered] |
| Analytics | Drop-off points, time per stage, conversion rates | [stages covered] |
| Session recordings | Actual user behaviour, confusion points | [stages covered] |
| User interviews | Motivations, emotions, unspoken frustrations | [stages covered] |
| Product usage data | Feature adoption, ignored features, usage patterns | [stages covered] |
| Sales/CS conversations | Objections, expectations, satisfaction | [stages covered] |

**Evidence gaps:** [stages with no data — flag as hypothesis]
```

**Rules for evidence:**
- Stages backed by data are "evidence-based." Stages with no data are "hypothesis" — label them clearly
- Analytics tell you WHAT happened. Qualitative data tells you WHY. You need both
- If evidence is sparse, the journey map is a hypothesis to be validated, not a fact to be acted on

**Output:** Evidence source table with coverage and gaps identified.

## Step 3: Map stages (mandatory)

For each stage of the journey, complete this table:

```markdown
### Stage [N]: [name]

**User goal at this stage:** [what they're trying to achieve]
**Duration:** [typical time spent in this stage]
**Evidence basis:** [evidence-based / hypothesis]

| Element | Detail |
|---|---|
| **Touchpoints** | [every interaction point: website, app, email, docs, support, social media] |
| **Actions** | [what the user does: searches, clicks, reads, configures, asks for help] |
| **Thinking** | [questions and concerns: "Is this the right tool?", "How do I set this up?"] |
| **Feeling** | [emotional state: confident, confused, frustrated, delighted, anxious, overwhelmed] |
| **Pain points** | [friction, confusion, delays, dead ends, unmet expectations] |
| **Opportunities** | [how to improve this stage — specific, actionable ideas] |

**Drop-off risk:** [High / Medium / Low] — [what causes users to leave at this stage]
```

Repeat for every stage from start point to end point. Typical journeys have 4–7 stages.

**Output:** Complete stage maps with all elements filled.

## Step 4: Identify critical moments (mandatory)

```markdown
### Critical moments

| Moment | Stage | Description | Impact | Evidence |
|---|---|---|---|---|
| **Moment of truth** | [stage] | [the make-or-break interaction — usually first value or first error] | [what happens if this goes wrong] | [data source] |
| **Biggest drop-off** | [stage] | [where users are most likely to leave] | [conversion/retention impact] | [data] |
| **Delight opportunity** | [stage] | [where exceeding expectations has disproportionate impact] | [loyalty/referral impact] | [data] |

### Key metric
**Time to first value:** [duration from start point to genuine value — the metric that predicts retention]
```

**Output:** Critical moments table with evidence.

## Step 5: Synthesise and recommend (mandatory)

```markdown
### Journey health

| Stage | Feeling | Drop-off risk | Top pain point | Top opportunity |
|---|---|---|---|---|
| [stage 1] | [emoji + word] | [H/M/L] | [pain] | [opportunity] |
| [stage 2] | [feeling] | [risk] | [pain] | [opportunity] |

### Recommendations (prioritised by impact on success metric)

| Priority | Recommendation | Stage affected | Expected impact on [success metric] | Effort |
|---|---|---|---|---|
| 1 | [specific fix] | [stage] | [projected improvement] | [S/M/L] |
| 2 | [fix] | [stage] | [improvement] | [effort] |
| 3 | [fix] | [stage] | [improvement] | [effort] |
```

**Output:** Journey health summary and prioritised recommendations.

## Rules

- **One journey, one map.** Combining "onboarding" and "power user workflow" into one map produces noise, not insight. Separate them.
- **Evidence over assumption.** Every pain point should cite where the evidence came from. "Users probably find this confusing" is speculation. "37% drop-off at step 3, with 12 support tickets about the config screen" is evidence.
- **Feelings are data.** Emotional states at each stage are not decoration — they predict churn, referrals, and support load. Include them with the same rigour as actions and touchpoints.
- **Hypothesis stages must be labelled.** If you don't have data for a stage, map it anyway but mark it clearly. A hypothesis journey map is a research plan — it tells you what to validate next.
- **Opportunities must be specific.** "Improve the onboarding" is not an opportunity. "Add a progress bar showing 3/5 steps completed" is an opportunity.
- **Pain points without evidence are opinions.** Every pain point must reference a data source (support tickets, analytics, interviews, or session recordings). If no source exists, mark it as hypothesis.

## Output Format

```markdown
## Journey: [name] — [user type]

### Scope
[From Step 1]

### Evidence Sources
[From Step 2]

### Stage 1: [name]
[Full stage map from Step 3]

### Stage N: [name]
[Full stage map]

### Critical Moments
[From Step 4]

### Journey Health
[Summary table from Step 5]

### Recommendations
[Prioritised table from Step 5]

---
Evidence basis: [X of Y stages evidence-based, Z hypothesis]
Last updated: [date]
```

## Related Skills

- `/ux-researcher:persona-definition` — define the user type before mapping their journey. The persona's goals and frustrations inform every stage.
- `/ux-researcher:usability-review` — for deep-diving into a specific stage or touchpoint that the journey map flags as high-friction.
