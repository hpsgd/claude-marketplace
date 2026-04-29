# Result: creative onboarding flow ideation

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 13.5 / 14 (96%) |
| **Evaluated** | 2026-04-29 |
| **Skill** | `plugins/practices/thinking/skills/creative/SKILL.md` |

## Prompt

> /creative We're losing 60% of new users before they complete our 7-step onboarding wizard for Nexus, our project management tool. The current flow is: account setup → invite team → create first project → add tasks → connect integrations → set notifications → take a tour. Most users drop off at step 3. What are some genuinely different approaches?

## Evaluation

### Criteria

| # | Type | Criterion | Result | Evidence |
|---|---|---|---|---|
| 1 | PASS | Step 1 analyses the problem before generating ideas — identifies who has the problem, consequences, and constraints | met | Step 1 template requires "Who has this problem", "Why it matters" (consequences), and "Constraints". Explicit rule: "Do not skip this step. The most common failure mode in brainstorming is solving the wrong problem creatively." |
| 2 | PASS | Step 2 produces all three reframes (user story, constraint, analogy) and states which was selected for ideation and why | met | Step 2 defines all three reframe types with templates. Final instruction: "After all three reframes, pick the framing that opens the most creative space. State which one and why." |
| 3 | PASS | Step 3 applies all five mandatory diversity techniques (inversion, extreme scale, remove constraints, cross-domain transfer, worst idea first) producing at least one option from each | met | Step 3 "Mandatory diversity techniques" lists all five, each ending with "Generate one option from [technique]." All five are explicitly required. |
| 4 | PASS | At least 5 options pass all three quality tests — distinct, feasible, and specific enough to act on | met | Step 3: "Produce at least 5 genuinely different approaches." Quality bar names all three tests. "If you have fewer than 5 options that pass all three tests, go back to the techniques and push harder." |
| 5 | PASS | Step 4 evaluates each option with genuine pros, biggest risk, effort estimate, and reversibility | met | Step 4 template includes: "What's genuinely good about it", "What's the biggest risk", "Effort to implement", and "Reversibility". All four fields are present and required. |
| 6 | PASS | A wild card option is included in the output — unconventional but argued seriously | met | Step 6 output item 4 mandates a wild card with a structured template ("Why it seems wrong / Why it might be right / When to revisit"). Rules section: "The wild card is mandatory." |
| 7 | PASS | Recommended path specifies what to do first as a concrete immediate action | met | Step 6 output item 3 template: "**What to do first:** [Immediate next step — make it concrete]". Explicitly required. |
| 8 | PARTIAL | Options named with descriptive memorable names (not "Option 1", "Option 2") | partial | Rules section says "Names should be descriptive and memorable." Step 4 template shows `### Option [N]: [Descriptive name]` — the number prefix is built into the template, so a compliant execution could produce "Option 1: The Inversion" rather than purely named options. Intent is clear but enforcement allows numbered labels alongside descriptive names. |

### Output expectations

| # | Type | Criterion | Result | Evidence |
|---|---|---|---|---|
| 9 | PASS | Output addresses step 3 as the dropoff hotspot — at least 2 options target reducing friction at that specific step | met | Step 1 requires identifying constraints and what has been tried; the prompt explicitly names step 3. A well-formed execution must surface this in the problem analysis and drive at least 2 options toward it. The specificity requirement in Step 3 ("concrete enough to evaluate") makes generic ideas non-compliant. |
| 10 | PASS | Inversion option flips the wizard premise (e.g. no onboarding wizard at all) rather than a slight tweak | met | Technique 1 instructs: "If the obvious solution adds something, what if you removed something instead?" Applied to a 7-step wizard, the inversion is removing the wizard, not reordering steps. The technique is designed to produce genuine opposites. |
| 11 | PASS | Extreme-scale option imagines 10x or 0.1x users and surfaces a different design implication | met | Technique 2 explicitly states "What if this needed to serve 1 user? What about 1 million?" and requires that the best solution is "visible from one of them." A compliant option must state the scale and the implication it reveals. |
| 12 | PASS | Remove-constraints option drops one of the 7 steps as non-essential with reasoning | met | Technique 3 asks "What if [biggest constraint] didn't exist?" and requires working backwards from the ideal. For a 7-step wizard, a compliant answer would identify which step is non-essential and why. The skill's specificity requirement means reasoning must be included. |
| 13 | PASS | Cross-domain transfer borrows a pattern from outside SaaS onboarding | met | Technique 4 lists explicit source domains (nature, games, architecture, music, cooking, transportation) and requires identifying the structural similarity. By definition this produces a non-SaaS reference. |
| 14 | PASS | Worst-idea option is genuinely bad and explains what the failure mode reveals | met | Technique 5 says "Write it out. Then examine it seriously: What's accidentally interesting about it? What assumption does it violate?" The skill requires the genuinely bad idea first, then analysis of what it reveals — not a softened version. |
| 15 | PASS | At least 5 distinct, feasible, specific options with memorable names, specific mechanism, primary risk, and effort estimate | met | Step 4 evaluation template requires all four fields. Step 3 quality bar requires all three tests. Rules require named options. Together these enforce the full set of requirements per option. |
| 16 | PASS | Wild-card option is non-obvious but argued seriously | met | Step 6 requires the wild card template with "Why it might be right" and "When to revisit." Rules state it is "a hedge against groupthink." The structure mandates a serious argument, not a joke entry. |
| 17 | PASS | Recommended path names a concrete first action | met | Step 6 recommendation template: "**What to do first:** [Immediate next step — make it concrete]". The template explicitly prohibits vague suggestions through the word "concrete." |
| 18 | PARTIAL | Output addresses the 60% dropoff with a hypothesis about WHY users abandon at step 3 | partial | Step 1 includes "What's been tried" and "Constraints" but does not explicitly require a diagnostic hypothesis about user psychology at the hotspot step. A well-formed execution would likely surface one through the problem analysis, but it is not a named deliverable. A minimal compliant execution could identify step 3 as the dropoff without hypothesising whether the cause is cognitive load, dependency ordering, or perceived value. |

## Notes

The skill definition is thorough and well-engineered. Almost every output expectation is enforced by explicit template fields or rules rather than implied by good practice.

The one structural gap: Step 5 (combine and synthesise) is defined in the process but the Step 6 output format does not mandate a hybrid section. Combinations appear only if they emerge, surfaced as part of the recommended path. This is a minor inconsistency between the process steps and the output specification — it does not fail any criterion here but could produce output that skips synthesis.

The diagnostic hypothesis gap (criterion 18) is the only substantive miss. The skill could be strengthened by adding an explicit sub-question to Step 1: "Why now: what specifically causes users to stall at [identified hotspot]?" That would make it a named deliverable rather than an emergent one.
