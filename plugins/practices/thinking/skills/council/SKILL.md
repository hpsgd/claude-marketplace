---
name: council
description: "Simulate a structured debate between diverse expert perspectives. Use when weighing options, making decisions, or needing multiple viewpoints on a problem."
argument-hint: "[question, decision, or proposal to debate]"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

Convene a council of diverse perspectives to debate $ARGUMENTS through genuine intellectual friction.

## How This Differs From Red Team

Council is **collaborative-adversarial** — experts debate to find the best path forward, building on each other's points. `/red-team` is **purely adversarial** — the goal is to break the argument. Use council when choosing between options; use red-team when stress-testing a decision already made.

## Step 1: Select perspectives (mandatory)

Define 4 perspectives relevant to the topic. Each perspective must create genuine tension with at least one other — do not select 4 people who agree.

For each perspective, state:

```markdown
### [Perspective name] — [one-sentence stance]

**Core argument:** [Their strongest case in 2–3 sentences]
**Primary concern:** [What they are most worried about]
**What they would sacrifice:** [What trade-off they accept]
```

**Choosing perspectives:**
- At least 2 must be in direct tension (e.g., speed vs quality, user value vs technical debt)
- At least 1 must represent a non-obvious angle (the voice not usually in the room)
- Perspectives are roles, not strawmen — each must have a legitimate case

**Default perspectives** (adapt for the specific topic):
- **The Pragmatist**: What ships fastest and works well enough?
- **The Architect**: What's the right long-term design?
- **The User Advocate**: What do users actually experience?
- **The Skeptic**: What could go wrong? What are we not seeing?

**Output:** 4 perspectives with opening positions.

## Step 2: Debate — responses (mandatory)

Each perspective responds to the others' actual arguments. This must be genuine engagement, not performative disagreement.

For each perspective:

```markdown
### [Perspective] responds

**Agrees with [other perspective] on:** [specific point] — because [reasoning]
**Disagrees with [other perspective] on:** [specific point] — because [evidence or reasoning]
**What [other perspective] is missing:** [blind spot] — specifically [what they haven't considered]
**Strongest concession:** [The best point the opposition made that weakens their own position]
```

**Rules for debate:**
- Every response must engage with a specific claim, not a general position
- "I disagree" without reasoning is not a response
- Every perspective must make at least one concession — if nobody concedes anything, the debate is performative

**Output:** Each perspective's response with specific agreements, disagreements, and concessions.

## Step 3: Synthesis — position shifts (mandatory)

Each perspective reflects on the debate and states how their position has evolved:

```markdown
### [Perspective] — revised position

**Original stance:** [one sentence]
**Shifted to:** [one sentence — how the debate changed their view]
**Key insight from debate:** [what they learned they didn't know before]
**Remaining non-negotiable:** [what they still won't compromise on, and why]
```

**Output:** Each perspective's revised position with explicit shifts.

## Step 4: Final synthesis (mandatory)

Synthesise across all perspectives:

```markdown
### Points of consensus
[What all perspectives agree on after debate — these are high-confidence conclusions]

### Remaining tensions
[Genuine disagreements that debate alone cannot resolve — these need data, experiments, or authority to decide]

### Recommended decision
[Weighing the strongest arguments from all sides, state the recommendation and primary reasoning]

### Risk register
[Concerns raised during debate that should be monitored regardless of decision]

| Risk | Raised by | Severity | Monitoring signal |
|---|---|---|---|
| [risk] | [perspective] | High/Medium/Low | [what to watch for] |
```

**Output:** Consensus, tensions, recommendation, and risk register.

## Rules

- **Genuine tension is mandatory.** If all perspectives agree from the start, you've chosen the wrong perspectives. Re-select.
- **Concessions are mandatory.** Every perspective must acknowledge at least one point from the opposition. A debate with no concessions is propaganda.
- **Specificity over generality.** "The Architect disagrees with the Pragmatist on the database choice because shared-nothing scales better under their projected load" is a response. "The Architect prefers a better design" is not.
- **No false balance.** If the evidence overwhelmingly supports one perspective, say so in the synthesis. Council is not about pretending all options are equal.
- **Time-box the debate.** Three rounds (opening, response, synthesis) — no more. If the question isn't clearer after three rounds, it needs data, not more debate.

## Output Format

```markdown
## Council: [topic]

### Perspectives
[4 perspectives with opening positions from Step 1]

### Debate
[Responses from Step 2]

### Position Shifts
[Revised positions from Step 3]

### Synthesis
**Consensus:** [agreed points]
**Tensions:** [unresolved disagreements]
**Recommendation:** [decision with reasoning]
**Risks:** [risk register table]
```

## Related Skills

- `/red-team` — for purely adversarial stress-testing after a decision is made. Council decides; red-team validates.
- `/first-principles` — when the council reveals that the framing itself is wrong and the problem needs decomposition.
- `/iterative-depth` — for structured multi-lens analysis without the debate format.
