---
name: evaluate-technology
description: "Evaluate a technology, framework, or tool against weighted criteria. Produces a structured comparison with scored trade-offs and a recommendation. Use when choosing between technologies or assessing fitness of a single option."
argument-hint: "[technology to evaluate, or 'X vs Y' comparison]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep, WebSearch, WebFetch
---

Evaluate $ARGUMENTS for fitness against the project's needs.

## Process (sequential — do not skip steps)

### Step 1: Define evaluation criteria

Before researching, establish what matters. Start with these defaults and adjust for the specific evaluation:

| Criterion | Weight (1–5) | Why it matters |
|---|---|---|
| Maturity / stability | | Production readiness, breaking change history |
| Community / ecosystem | | Long-term support, plugins, answers on Stack Overflow |
| Team familiarity | | Ramp-up cost, hiring pool |
| Performance | | Meets non-functional requirements under load |
| Maintenance burden | | Ongoing cost of ownership, upgrade friction |
| Lock-in risk | | Can we migrate away? Standard interfaces or proprietary? |
| Cost | | Licensing, infrastructure, operational spend |
| Integration | | Works with existing stack, language, CI/CD |

**Rules for criteria:**
- Add domain-specific criteria where relevant (e.g., "HIPAA compliance" for healthcare, "bundle size" for frontend)
- Remove criteria that genuinely don't apply — justify each removal
- Assign weights BEFORE research to prevent post-hoc rationalisation
- Every criterion must have a weight — no blanks

**Output:** A completed criteria table with weights and justifications.

### Step 2: Research each option

For each technology under evaluation, produce a structured research brief:

```markdown
### [Technology name]

**What:** [One-sentence description — what it is and what problem it solves]
**Version:** [Current stable version, release date]
**License:** [License type — MIT, Apache 2.0, BSL, proprietary, etc.]
**Notable adopters:** [3–5 companies or projects using it in production]

#### Maturity signals
- First stable release: [date]
- Release cadence: [frequency]
- Breaking changes in last 2 major versions: [count and severity]
- Open issues / PRs: [count, trend]

#### Community signals
- GitHub stars: [count] | npm/PyPI weekly downloads: [count]
- Stack Overflow questions: [count, answer rate]
- Active maintainers: [count, bus factor]
- Discord/forum activity: [qualitative — active, moderate, quiet]

#### Known limitations
- [Limitation 1 — sourced from issues, forums, or migration guides]
- [Limitation 2]
- [Search: "[tech] problems", "[tech] limitations", "[tech] vs alternatives"]
```

**Output:** One research brief per option.

### Step 3: Score against criteria

Rate each option against each criterion on a 1–5 scale. Multiply by weight for a weighted score.

```markdown
| Criterion | Weight | Option A | | Option B | |
|---|---|---|---|---|---|
| | | Raw (1–5) | Weighted | Raw (1–5) | Weighted |
| Maturity / stability | 5 | 4 | 20 | 3 | 15 |
| Community / ecosystem | 3 | 5 | 15 | 4 | 12 |
| ... | | | | | |
| **Total** | | | **X** | | **Y** |
```

**Rules for scoring:**
- Every score must have a one-sentence justification — no bare numbers
- If you lack data for a criterion, score it 3 (neutral) and flag it as "unverified"
- Do not round or average — the weighted total is the score

**Output:** Completed scoring matrix with justifications.

### Step 4: Identify trade-offs and risks

No technology wins on every dimension. Explicitly state:

```markdown
### Trade-offs

| Choosing Option A means... | Choosing Option B means... |
|---|---|
| [Advantage A has over B] | [Advantage B has over A] |
| [Cost of choosing A] | [Cost of choosing B] |

### Risks to monitor post-adoption

| Risk | Trigger signal | Mitigation |
|---|---|---|
| [Risk 1] | [What you'd see if this risk materialises] | [What you'd do] |
| [Risk 2] | [Trigger] | [Mitigation] |
```

**Output:** Trade-off comparison and risk register.

### Step 5: Recommend

State the recommendation clearly:

```markdown
### Recommendation

**Choose: [Option]**

**Primary reason:** [The single most important factor]
**Secondary reasons:** [Supporting factors]
**What we sacrifice:** [Explicit trade-off acknowledgement]
**Reconsideration triggers:** [Conditions that would change this recommendation]
```

If the evaluation warrants a formal record, suggest writing an ADR using `/architect:write-adr`.

If neither option is clearly better, say so — recommend a time-boxed spike or prototype instead of a forced choice.

## Anti-Patterns (NEVER do these)

- **Conclusion-first evaluation** — deciding the winner before scoring, then fitting criteria to match. Weights must be set in Step 1, before research.
- **Popularity as proxy** — GitHub stars and npm downloads measure awareness, not quality. They are one signal among many, not the deciding factor.
- **Ignoring total cost of ownership** — a free library with no docs costs more than a paid one with good support. Score maintenance burden and team familiarity, not just the license.
- **Comparing unequals** — comparing a framework to a library, or a managed service to a self-hosted tool, without normalising the scope. State what each option requires you to build on top.
- **Binary scoring** — scoring everything 1 or 5 defeats the purpose. Use the full 1–5 range with justifications.
- **Skipping the "what if we're wrong" step** — every recommendation needs reconsideration triggers. Technology choices are expensive to reverse.

## Output Format

```markdown
# Technology Evaluation: [subject]

## Evaluation Criteria
[Weighted criteria table from Step 1]

## Research
### [Option A]
[Research brief]
### [Option B]
[Research brief]

## Scoring Matrix
[Weighted scoring table from Step 3]

## Trade-offs
[Trade-off table from Step 4]

## Risks
[Risk register from Step 4]

## Recommendation
[Recommendation from Step 5]

## Recommended Follow-ups
- [ ] ADR for this decision (if applicable)
- [ ] Spike/prototype for low-confidence areas
- [ ] Re-evaluate on [date or trigger condition]
```
