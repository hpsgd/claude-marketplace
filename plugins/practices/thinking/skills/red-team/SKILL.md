---
name: red-team
description: "Adversarial analysis to stress-test an idea, plan, or argument. Use to find every weakness before they find you. Purely adversarial — for balanced debate, use /council instead."
argument-hint: "[idea, plan, or argument to attack]"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

Apply adversarial analysis to stress-test $ARGUMENTS. The goal is to find every weakness, not to be balanced.

**When to use red-team vs council:** Red-team is purely adversarial — attack the idea to find breaking points. `/council` is collaborative-adversarial — experts debate to find the best path forward. Use red-team when you need to validate robustness of a decision already made; use council when you need to choose between options.

## Step 1: Decompose into atomic claims (mandatory)

Break the argument into independently testable claims:

```markdown
### Claim inventory

| # | Claim | Type | Confidence |
|---|---|---|---|
| 1 | [specific claim] | Stated | [how confident is the author?] |
| 2 | [implied claim] | Implied | [inferred from context] |
| 3 | [required but unstated] | Required | [necessary for argument to hold] |
```

**Claim types:**
- **Stated**: Explicitly claimed in the argument
- **Implied**: Assumed but not stated — often the weakest points
- **Required**: Necessary for the argument to hold but not mentioned — often invisible

A plan with 5 sections typically decomposes into 15–25 atomic claims. If you find fewer than 10, you haven't decomposed far enough.

**Output:** Complete claim inventory with types and confidence levels.

## Step 2: Steelman — build the strongest version (mandatory)

Before attacking, construct the **strongest possible version** of the argument. This ensures the red team attacks the best version, not a strawman.

```markdown
### Steelman

The strongest case for this argument:

1. [Strongest supporting point — with evidence]
2. [Second strongest point]
3. [Third point]
...up to 8 key points

**Best available evidence:** [what data or precedent supports this]
**Strongest framing:** [how would the most skilled advocate present this?]
```

**Rules for steelmanning:**
- Fix obvious weaknesses before attacking — find the version the author would write with unlimited time
- Add the best supporting evidence, even if the author didn't include it
- Frame it in its most compelling form

**Output:** Steelmanned version with up to 8 key points.

## Step 3: Attack every claim (mandatory)

For each claim from Step 1, apply these attack vectors:

```markdown
### Attack: [Claim #N] — "[claim text]"

**Disproof test:** What evidence would disprove this? [specific evidence]
**Failure conditions:** Under what conditions does this fail? [scenarios]
**Weakest link:** What's the weakest step in the reasoning? [specific step]
**Unverified assumption:** What's assumed but not tested? [assumption]
**Strongest opposition:** Who would disagree most, and what's their best argument? [argument]
```

After attacking all claims, classify findings:

```markdown
### Findings by severity

**Critical weaknesses** (would cause failure):
| # | Claim attacked | Weakness | Evidence | Impact |
|---|---|---|---|---|
| 1 | [claim #] | [weakness] | [why this breaks the argument] | [consequence] |

**Significant risks** (could cause failure under conditions):
| # | Claim attacked | Risk | Trigger conditions | Likelihood |
|---|---|---|---|---|
| 1 | [claim #] | [risk] | [when this becomes a problem] | High/Medium/Low |

**Unverified assumptions** (unknown whether true):
| # | Claim attacked | Assumption | How to verify | Cost of being wrong |
|---|---|---|---|---|
| 1 | [claim #] | [assumption] | [experiment or data needed] | [impact] |
```

**Output:** Classified attack findings with evidence.

## Step 4: Verdict and recommendations (mandatory)

```markdown
### Verdict

**Overall robustness:** [Robust / Conditionally sound / Fragile / Fatally flawed]

**Confidence in verdict:** [High / Medium / Low] — because [reasoning]

### Recommendations

**Must address before proceeding:**
1. [Critical weakness] — suggested fix: [approach]

**Should address if possible:**
1. [Significant risk] — mitigation: [approach]

**Verify when possible:**
1. [Unverified assumption] — how to test: [method]
```

**Output:** Overall verdict with prioritised recommendations.

## Rules

- **Attack the steelman, not the strawman.** If you're attacking an obviously weak version, you're wasting time. Build the strongest version first (Step 2), then attack that.
- **Specificity is mandatory.** "This might not work" is not a finding. "Claim #3 assumes constant network latency, but spikes above 500ms would cause cascading timeouts in the sync path" is a finding.
- **Implied claims are the richest target.** What the author didn't say is often more vulnerable than what they did. Focus on Required and Implied claims.
- **Severity matters more than count.** One critical weakness outweighs ten minor risks. Don't pad findings with trivia to appear thorough.
- **Never soften the verdict.** If the argument is fatally flawed, say so. The purpose of red-teaming is to find truth, not to be diplomatic.
- **The goal is improvement, not destruction.** Every weakness identified should come with a direction for fixing it.

## Output Format

```markdown
## Red Team: [subject]

### Claim Inventory
[Decomposed claims from Step 1]

### Steelman
[Strongest version from Step 2]

### Attack Findings
[Classified findings from Step 3]

### Verdict
[Overall assessment from Step 4]

### Recommendations
[Prioritised fixes from Step 4]
```

## Related Skills

- `/council` — for collaborative debate when choosing between options. Red-team validates; council decides.
- `/first-principles` — when the red-team reveals that the argument's foundations need re-examination.
