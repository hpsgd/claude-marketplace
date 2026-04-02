---
name: persona-definition
description: "Define a research-backed user persona grounded in real behaviour, not demographics or stereotypes. Produces a structured persona with goals, frustrations, and behaviour patterns backed by evidence. Use to represent a customer segment for product and design decisions."
argument-hint: "[user segment or product area to define persona for]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Persona Definition

Define a persona for $ARGUMENTS using the mandatory process below. Personas are archetypes grounded in evidence, not fictional characters with backstories.

## Step 1: Gather evidence (mandatory)

Before defining any attributes, identify the data sources:

```markdown
### Evidence inventory

| Source | Type | Volume | Recency |
|---|---|---|---|
| [Support tickets] | Qualitative | [N tickets reviewed] | [date range] |
| [Analytics] | Quantitative | [metrics available] | [date range] |
| [User interviews] | Qualitative | [N interviews] | [date range] |
| [Sales data] | Quantitative | [deal records, objections] | [date range] |
| [Product usage] | Quantitative | [feature adoption, session data] | [date range] |
```

**Rules for evidence:**
- Every persona attribute in Step 3 must trace back to at least 3 data points from this inventory
- If evidence is thin (fewer than 5 data points total), flag the persona as "hypothesis — needs validation" rather than "research-backed"
- No evidence = no persona. Do not invent attributes to fill gaps

**Output:** Evidence inventory table with sources, types, and volumes.

## Step 2: Identify distinct segments (mandatory)

Before writing a persona, confirm it represents a genuinely distinct segment:

```markdown
### Segment validation

**Proposed segment:** [who this persona represents]
**Distinguishing behaviours:** [what this segment does differently from other segments — not demographics]
**Decision test:** Would this persona make a DIFFERENT product decision than another persona? [Yes — example / No — merge with existing]
**Assignment test:** Could two team members independently assign the same real customer to this persona? [Yes — clear / No — too vague]
```

**Rules for segments:**
- 3–5 personas maximum per product. More means segments aren't distinct enough
- Segments are defined by behaviour and goals, not demographics. "Enterprise admin" is better than "Male, 35-45, MBA"
- If two personas would make the same product decisions, merge them

**Output:** Segment validation with both tests passed.

## Step 3: Write the persona (mandatory)

Use this exact format:

```markdown
## Persona: [descriptive archetype name — e.g., "First-time evaluator" not "Sarah"]

**Segment:** [which customer segment this represents]
**Evidence base:** [N interviews, M support tickets, analytics from X — from Step 1]
**Confidence:** [High (10+ data points) / Medium (5-9) / Low (3-4) / Hypothesis (<3)]

### Context
| Attribute | Value | Evidence |
|---|---|---|
| **Role** | [professional context] | [source] |
| **Technical sophistication** | [novice / intermediate / advanced] | [source] |
| **Decision authority** | [can buy solo / needs approval / influences] | [source] |
| **Time pressure** | [exploring / evaluating with deadline / urgent need] | [source] |

### Goals (ranked by importance)
1. **[Primary goal]** — what success looks like in THEIR words [evidence source]
2. **[Secondary goal]** — [evidence source]

### Frustrations (ranked by severity)
1. **[Current pain with existing solutions]** — [evidence: quote or data point]
2. **[What they've tried that didn't work]** — [evidence]

### Behaviour Patterns
| Behaviour | Pattern | Evidence |
|---|---|---|
| **Discovery** | [how they find solutions] | [source] |
| **Evaluation** | [how they compare — features? price? reviews? trial?] | [source] |
| **Decision trigger** | [what tips them over the edge to buy/adopt] | [source] |
| **Learning style** | [docs? video? trial-and-error? ask a colleague?] | [source] |

### Success Criteria
[How THEY would judge the product successful — in their words, not ours. Include the metric they would use.]

### Anti-Persona Signals
[Characteristics that indicate someone is NOT this persona — helps with segmentation and prevents over-broad targeting]
- [Signal 1: behaviour or attribute that disqualifies]
- [Signal 2]
```

**Output:** Complete persona in the format above.

## Step 4: Validate the persona (mandatory)

After writing, verify quality:

| Check | Question | Pass/Fail |
|---|---|---|
| Assignment test | Could two people independently assign a real customer to this persona? | |
| Decision test | Does this persona make different product decisions than other personas? | |
| Evidence threshold | Is every attribute backed by at least 3 data points? | |
| No stereotypes | Are attributes based on observed behaviour, not assumed demographics? | |
| Actionable | Could a product team use this persona to make a specific decision TODAY? | |

If any check fails, revise the persona before finalising.

**Output:** Validation checklist with pass/fail for each criterion.

## Rules

- **Evidence over invention.** Every attribute must trace to real data. "I think users want X" is not evidence. "12 of 15 interviewees mentioned X as their top priority" is evidence.
- **Behaviours over demographics.** Age, gender, and job title do not predict product decisions. Goals, frustrations, and behaviour patterns do. Never use a human name for a persona.
- **3–5 personas maximum.** If you need more, your segments aren't distinct. Merge until each persona would make genuinely different product decisions.
- **Anti-persona signals are mandatory.** Knowing who is NOT this persona is as valuable as knowing who is. Without anti-signals, every customer looks like every persona.
- **Update on evidence, not schedule.** Personas change when new evidence contradicts them, not on a quarterly calendar. Stale personas are worse than no personas.
- **Hypothesis personas are valid but must be labelled.** If evidence is thin, say so. A hypothesis persona is useful for planning research; a falsely confident persona is dangerous for product decisions.

## Output Format

```markdown
# Persona: [archetype name]

## Evidence Base
[Evidence inventory from Step 1]

## Segment Validation
[Tests from Step 2]

## Persona Profile
[Full persona from Step 3]

## Validation
[Checklist from Step 4]

## Recommended Next Steps
- [Research needed to strengthen low-confidence attributes]
- [Decisions this persona can inform immediately]
```

## Related Skills

- `/ux-researcher:journey-map` — map the end-to-end experience for this persona. Define the persona first, then map their journey.
- `/ux-researcher:usability-review` — review a specific flow from this persona's perspective.
