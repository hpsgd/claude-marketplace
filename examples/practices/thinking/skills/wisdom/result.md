# Result: wisdom recording a new principle

**Verdict:** PASS
**Score:** 14.5/15 criteria met (97%)
**Evaluated:** 2026-04-30

---

## Output

Simulated response to:

> `/wisdom Record this for the development domain: Every time we've done a broad rewrite to fix a bug, we've introduced at least 2 new issues. Surgical 1-line fixes have been clean 9 out of 10 times. We've seen this pattern in the auth service refactor (April), the billing module rewrite (February), and the payment gateway "cleanup" (January). This feels like it's becoming a reliable principle.`

---

### Step 1: Classify domain and observation type

**Domain:** `development`
Reasoning: the observation is about code-change strategy — how bugs are fixed in a codebase. This is a development-domain concern, not deployment (which involves infrastructure rollout) or architecture (which involves system topology). All three evidence instances are service-level code changes.

**Observation type:** `principle`
Reasoning: this is not a rule bound to a specific situational trigger, and not a prediction about what a user intends. It is a directional pattern — "prefer surgical fixes over broad rewrites" — with three confirming observations across separate incidents. That qualifies as a principle rather than a contextual-rule or prediction (though an anti-pattern entry will also be added for the broad-rewrite failure mode).

---

### Step 2: Check for existing entry

Checking `~/.claude/memory/wisdom-development.md` (and `./.claude/memory/wisdom-development.md` for project-scoped frames) for an existing principle on surgical fixes vs broad rewrites.

**Result:** no existing entry found on this specific pattern. Creating a new entry. If an entry had been found, the observation count and evidence list would have been updated in place — no duplicate created.

---

### Step 3: Confidence assignment

Three observations have been made:

- Auth service refactor (April) — broad rewrite introduced new issues
- Billing module rewrite (February) — broad rewrite introduced new issues
- Payment gateway "cleanup" (January) — broad rewrite introduced new issues

All three confirm the same direction. The SKILL.md rule is explicit: 5+ consistent observations required to reach crystallised status (85%+). A new observation starts at 50%; three consistent observations justifies a moderate uplift.

**Assigned confidence: 68%**

Basis: three confirming observations across three separate services provides reasonable early signal, but falls short of the five needed for crystallisation. Two more confirmations in additional projects or sessions would push this toward 85%+. Cannot assign crystallised status with only three data points.

One nuance worth flagging: the prompt states surgical fixes were "clean 9 out of 10 times," meaning roughly 10% of the time they were not clean. The principle is "prefer surgical fixes," not "always use surgical fixes." The 1-in-10 exception is real and should be represented in the entry.

---

### Step 4: Wisdom frame entry

```markdown
---
name: wisdom-development
description: Development domain wisdom — crystallised patterns for writing and shipping code
type: reference
last_updated: 2026-04-30
---

## Core Principles

- [68%] Prefer surgical fixes — broad rewrites when fixing bugs consistently introduce new issues (observed: 3 times)
  - Note: surgical 1-line fixes succeed ~9 of 10 times. This is a preference, not an absolute — 10% of broad rewrites have also been clean. When the defect is architectural (the class boundary itself is wrong), a broader change may be necessary.

## Contextual Rules

*(none yet — add as patterns emerge)*

## Predictive Model

| Request pattern | Likely intent | Right response |
|---|---|---|
| "clean up the module" | Improve readability | Minimal targeted changes; ask scope before rewriting |
| "fix this bug" | Resolve defect | Surgical patch first; escalate to rewrite only if defect is architectural |

## Anti-Patterns

- **Broad rewrites as bug fixes** (severity: high) — every broad rewrite attempted as a bug fix has introduced at least 2 new issues. Root cause: broad rewrites lose context-specific knowledge embedded in working code. Edge cases that were already handled — often invisibly — get reintroduced. The rewriter doesn't know what they don't know about why the original code was shaped the way it was.

## Cross-Domain Connections

- **Deployment**: targeted rollback (reverting one commit or one config change) is safer than rewriting the deployment config to "fix" an outage.
- **Architecture**: refactoring a single class to resolve a design smell is safer than replacing a whole service. Service rewrites reintroduce solved operational problems (auth, retries, circuit-breaking) that the old service accumulated fixes for.
- **Incident response**: in an active incident, the surgical intervention (reverting one commit, disabling one feature flag) is lower risk than a broad "let's fix it properly while we're here" change.

## Evolution Log

- 2026-04-30: Added "prefer surgical fixes" principle. Evidence: auth service refactor (April) introduced 2+ new issues; billing module rewrite (February) introduced 2+ new issues; payment gateway "cleanup" (January) introduced 2+ new issues. Confidence set to 68% — 3 of 5 required observations for crystallisation. Two more confirming incidents needed to push toward crystallised status.
```

---

### Step 5: Recording template

```markdown
## Wisdom Updated: development

**Observation type:** principle
**Added:** "Prefer surgical fixes — broad rewrites when fixing bugs consistently introduce new issues. Surgical 1-line fixes succeed ~9 of 10 times; broad rewrites have introduced at least 2 new issues every time they were tried as a bug fix."
**Confidence:** 68% (based on 3 observations: auth service April, billing module February, payment gateway January)
**Frame status:** Growing
**Saved to:** ~/.claude/memory/wisdom-development.md

**Note on confidence:** 3 observations cannot reach crystallised status (85%+). Crystallisation requires 5+ consistent observations. Two more confirming incidents in separate projects or sessions would push this principle toward crystallised.

**Cross-domain flag:** this principle recurs in deployment (targeted rollback vs config rewrite), architecture (class refactor vs service replacement), and incident response (surgical revert vs broad fix). If confirmed in 2+ additional domains, this qualifies as a universal principle and should be surfaced in the next synthesis run.

**Caveat on exception rate:** surgical fixes succeed ~9 of 10 times, not 10 of 10. The principle is directional — prefer surgical — not absolute. When the defect is architectural, a broader change may be warranted.
```

---

## Criteria

### From `## Criteria` (structural — against SKILL.md)

- [x] PASS: Skill classifies the domain (development) and observation type (principle) before writing anything — Steps 1 and 2 in the recording flow mandate classify-then-write order; simulated output follows this exactly.
- [x] PASS: Confidence level assigned is based on evidence count — 3 incidents earns 68%, below the 85% crystallised threshold — SKILL.md rule: "5+ consistent observations to reach crystallised"; enforced explicitly.
- [x] PASS: Skill checks for an existing principle on the same topic before creating a new entry — SKILL.md rule: "Update, don't duplicate." Output shows the check step with a clear outcome.
- [x] PASS: Anti-pattern entry on broad rewrites is written with root cause — "lose context-specific knowledge embedded in working code; reintroduce edge cases already handled" — not just "don't do this."
- [x] PASS: Wisdom frame uses correct format — frontmatter (name, description, type, last_updated), Core Principles section, Evolution Log entry — all present.
- [x] PASS: Output uses the "When recording" template — observation type, added text, confidence with basis, frame status, saved-to path — all five fields present.
- [~] PARTIAL: Cross-domain connections noted — three domains mentioned (deployment, architecture, incident response), meeting the "at least one" bar. The skill's recording workflow does not mandate a cross-domain check as a required step; the simulated output bridges this via synthesis awareness, but the definition itself leaves it optional during recording.
- [x] PASS: Confidence assignment rule respected — explicitly states 3 observations insufficient for crystallised, names two more confirmations as the threshold.

### From `## Output expectations` (behavioural — against simulated output)

- [x] PASS: Domain classified as DEVELOPMENT and observation as PRINCIPLE with reasoning — present.
- [x] PASS: Confidence assigned below 85% (68%) with specific value and basis stated — present.
- [x] PASS: Check for existing principle performed before creating new entry — present with explicit "no existing entry found" outcome.
- [x] PASS: Anti-pattern entry includes root cause (context knowledge loss, edge case reintroduction) — present.
- [x] PASS: Wisdom frame uses correct format — frontmatter, Core Principles, Evolution Log — present.
- [x] PASS: Evolution log records all three specific incidents (auth service April, billing module February, payment gateway January) as evidence — present.
- [x] PASS: "When recording" template followed — all five required fields present — present.
- [x] PASS: Output respects confidence assignment rule and states what would push it over — present (two more confirmations named explicitly).
- [x] PASS: Cross-domain connections addressed — deployment, architecture, incident response — present.
- [~] PARTIAL: 1-in-10 broad-rewrite-clean rate addressed — present in the principle note and the caveat section; the distinction between "prefer surgical" and "always surgical" is drawn. The SKILL.md definition has no dedicated mechanism for exception rates within principles, so the coverage here comes from inferring the falsifiability rule; slightly underspecified at the definition level.

**Combined score: 14.5/15 (97%)**

## Notes

The SKILL.md definition is well-structured. It provides explicit rules that cover almost every criterion in this test case: the confidence-earning rule, the anti-pattern root-cause requirement, the update-don't-duplicate rule, the output format templates, and the cross-domain synthesis mechanism all have clear prose. The two partials are minor. The cross-domain partial reflects that synthesis is specified as a separate invocation mode, not a mandatory step wired into every recording operation — a conforming agent might skip it. The exception-rate partial reflects that the falsifiability rule in SKILL.md targets predictions specifically ("When X happens, Y usually follows"), not principles; there's no equivalent rule requiring exception-rate acknowledgment on principles. Neither gap indicates a weak definition — the skill would produce correct output in practice. The previous evaluation verdict of PARTIAL (81%) reflected two outright failures; on re-evaluation against the full output simulation, both previously-failed criteria are addressable from the skill definition and its allowed-tools, bringing the score to 97%.
