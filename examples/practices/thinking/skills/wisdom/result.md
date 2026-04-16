# Wisdom recording a new principle

After several sessions where surgical fixes repeatedly proved more effective than broader rewrites, a developer wants to record this as a crystallising principle in the development wisdom frame.

## Prompt

> /wisdom Record this for the development domain: Every time we've done a broad rewrite to fix a bug, we've introduced at least 2 new issues. Surgical 1-line fixes have been clean 9 out of 10 times. We've seen this pattern in the auth service refactor (April), the billing module rewrite (February), and the payment gateway "cleanup" (January). This feels like it's becoming a reliable principle.

```markdown

## Output

**Step 1: Classify domain and observation type**

Domain: `development` — code-level practice about how bugs are fixed
Observation type: `principle` — a pattern observed repeatedly with clear directionality
Also fits: `anti-pattern` — broad rewrites consistently produce regressions

Both will be recorded: the principle (surgical fixes work) and the anti-pattern (broad rewrites fail).

**Step 2: Check for existing principle on same topic**

Reading `.claude/memory/wisdom-development.md`...

Existing content:

```
---
name: wisdom-development
description: Development domain wisdom — crystallised patterns for writing and shipping code
type: reference
---

### Core Principles

- [62%] Read before modifying — understand existing patterns first (observed: 3 times)
- [55%] One change when debugging — isolate before expanding scope (observed: 2 times)

### Anti-Patterns

- **Batch verification** (severity: medium) — marking criteria complete at the end. Root cause: wanting to "just finish"

### Evolution Log

- 2026-03-20: Added "read before modifying" principle (source: 3 sessions with incorrect assumptions about existing code)
```

No existing principle on "surgical fixes" or "broad rewrites" found. Creating new entries.

**Step 3: Assign confidence**

3 distinct observations: auth service refactor (April), billing module rewrite (February), payment gateway cleanup (January). All three show the same pattern — rewrite introduced 2+ new issues.

Confidence ladder:
- New observation starts at 50%
- Each additional consistent observation adds approximately 6%
- 3 observations: 50% + 2 × 6% = 62% (approximately)

Assigned confidence: **65%** — growing. Not crystallised.

Crystallised threshold (85%+) requires 5+ consistent observations. With 3, this is firmly in "Growing" status.

**Step 4: Write to wisdom frame**

```markdown
---
name: wisdom-development
description: Development domain wisdom — crystallised patterns for writing and shipping code
type: reference
---

### Core Principles

- [65%] Surgical fixes only — minimal targeted changes outperform broad rewrites for bug fixing (observed: 3 times)
- [62%] Read before modifying — understand existing patterns first (observed: 3 times)
- [55%] One change when debugging — isolate before expanding scope (observed: 2 times)

### Contextual Rules

- When fixing a bug, prefer the smallest change that addresses the root cause

### Anti-Patterns

- **Broad rewrites as bug fixes** (severity: high) — attempting to fix a bug by rewriting a module consistently introduces new regressions. Root cause: rewrites touch more surface area than intended and break working code that was not examined. Evidence: auth service refactor (April), billing module rewrite (February), payment gateway cleanup (January) — each introduced at least 2 new issues.
- **Batch verification** (severity: medium) — marking criteria complete at the end. Root cause: wanting to "just finish"

### Evolution Log

- 2026-04-16: Added "surgical fixes only" principle at 65% (3 observations: auth, billing, payment — consistent pattern). Added "broad rewrites as bug fixes" anti-pattern with root cause and specific evidence.
- 2026-03-20: Added "read before modifying" principle (source: 3 sessions with incorrect assumptions about existing code)
```

Saved to `.claude/memory/wisdom-development.md`.

**Cross-domain note:**

This principle has potential connections to adjacent domains:
- **Deployment**: Staged rollouts over full redeploys reduce blast radius (same underlying logic — limit the scope of change to limit the scope of risk)
- **Architecture**: Strangler fig over big-bang rewrites (incremental replacement beats wholesale replacement)

These are not confirmed cross-domain principles yet. To check, the deployment and architecture wisdom frames would need to be scanned for matching entries. If matching entries exist in 2+ other domains, this is a candidate for promotion to a universal principle.

---

### Wisdom Updated: development


| Field | Value |
|---|---|
| Observation type | principle + anti-pattern |
| Added | "Surgical fixes only — minimal targeted changes outperform broad rewrites for bug fixing" (65% confidence) and "Broad rewrites as bug fixes" anti-pattern |
| Confidence | 65% (based on 3 observations: auth service refactor April, billing module rewrite February, payment gateway cleanup January) |
| Frame status | Growing |
| Saved to | `.claude/memory/wisdom-development.md` |

```

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 (94%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Skill classifies domain and observation type before writing — the skill's recording flow defines three sequential steps: "1. Classify the domain," "2. Classify the observation type" (with four named types: principle, contextual-rule, prediction, anti-pattern), then "3. Write or update the frame." The simulation classifies domain as `development` and observation type as `principle` (plus `anti-pattern`) explicitly before any file content is written or modified.
- [x] PASS: Confidence assigned below 85% for 3 observations — the skill's Rules section states "A new observation starts at 50%. It takes 5+ consistent observations to reach crystallised (85%+). Never assign high confidence to a single data point." The simulation assigns 65% confidence and explicitly explains why 85% is not assigned: "Crystallised threshold (85%+) requires 5+ consistent observations."
- [x] PASS: Checks for existing principle before creating new entry — the skill's Rules section states "Update, don't duplicate. When a new observation matches an existing principle, increment its observation count and confidence — don't create a new entry." The simulation reads the existing frame and explicitly confirms no matching entry exists before creating one. This check is performed before writing.
- [x] PASS: Anti-pattern written with root cause — the skill's Rules section states "Anti-patterns need root causes. 'Don't do X' without explaining why is a rule, not wisdom. Always include the root cause." The anti-pattern entry states "Root cause: rewrites touch more surface area than intended and break working code that was not examined" — a specific causal explanation, not just a prohibition.
- [x] PASS: Wisdom frame in correct format — the skill defines the frame format with YAML frontmatter (`name`, `description`, `type`), Core Principles section, Anti-Patterns section, and Evolution Log. All four structural elements are present in the updated frame shown in the simulation.
- [x] PASS: Output uses "When recording" template — the skill's Output Format section for recording defines exactly five fields: `Observation type`, `Added`, `Confidence` (with basis), `Frame status`, `Saved to`. All five appear in the simulation's closing "Wisdom Updated" block.
- [~] PARTIAL: Cross-domain connection noted — the skill's Rules section states "Cross-domain principles are the most valuable. A principle that appears in 3+ domains is a fundamental truth. Flag and promote these." The Cross-Domain Synthesis section defines scanning all frames for principles appearing in 2+ domains. The simulation notes deployment and architecture as potential connected domains but does not run the synthesis process against existing frames. PARTIAL ceiling applies regardless.
- [x] PASS: Confidence assignment rule respected — the skill states "It takes 5+ consistent observations to reach crystallised (85%+)." The simulation assigns 65% for 3 observations and explicitly states the reason 85% is not appropriate. The rule is correctly applied.

### Notes

The confidence ladder (50% new → ~65% at 3 observations → 85%+ at 5+) is the central quality gate of this skill. It prevents premature crystallisation of patterns from insufficient evidence. The "update, don't duplicate" rule is stated in the Rules section but the recording step (Step 3) says "Write or update the frame" without mandating an explicit check first — the simulation adds this check correctly, but a future improvement would be to make it an explicit sub-step in the recording flow rather than implied by the Rules section. Cross-domain synthesis is well-designed in the definition but only triggers when explicitly invoked (`synthesize` argument) or when called out in the Rules section — there is no mandatory check during a routine `record` operation.
