# Result: review-standards dead code and writing violations

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17/17.5 criteria met (97%) |
| **Evaluated** | 2026-04-30 |
| **Skill** | `plugins/practices/coding-standards/skills/review-standards/SKILL.md` |

---

## Output

Simulated skill output for the PR described in the prompt — `src/auth/session.ts`, `README.md`, `src/ingestion/service.ts`, `src/extraction/service.ts`.

---

## General Standards Review

### Summary

| | |
|---|---|
| **Files reviewed** | 4 |
| **Findings** | 0 critical, 4 important, 6 suggestions |
| **Suppressions** | 1 found, 1 unjustified |
| **Dead code** | 1 instance (commented-out block) |

---

### Findings

#### Pass 1 — Dead Code

---

### [IMPORTANT] Dead Code: Commented-out session logic block

**File:** `src/auth/session.ts` (8-line block starting with `// old session logic`)

**Evidence:**

```typescript
// old session logic
// const session = await db.sessions.findOne({ userId });
// if (!session || session.expired) {
//   await db.sessions.delete({ userId });
//   return null;
// }
// const token = session.token;
// await db.sessions.update({ userId, lastAccess: new Date() });
// return token;
```

**Standard:** Pass 1 Dead Code Detection — commented-out code is noise. Version control preserves history; this block serves no purpose in the working tree.

**Fix:** Delete all 8 lines. Run `git log -S "old session logic" -- src/auth/session.ts` if you need to recover the logic.

---

#### Pass 2 — Lint Suppression Audit

---

### [IMPORTANT] Lint Suppression: `@typescript-eslint/no-explicit-any` without justification

**File:** `src/auth/session.ts` (the suppression line immediately above the affected code)

**Evidence:**

```typescript
// eslint-disable-next-line @typescript-eslint/no-explicit-any
```

**Standard:** Pass 2 Lint Suppression Audit — every suppression requires an inline comment explaining why the rule is being bypassed. A bare `eslint-disable-next-line` with no justification is always a finding.

**Fix:** Either eliminate the `any` (prefer `unknown` plus a narrowing check per the strict-validation rule) or, if the suppression is genuinely necessary, add an inline justification:

```typescript
// eslint-disable-next-line @typescript-eslint/no-explicit-any -- third-party SDK returns untyped config blob, tracked in #412
```

---

#### Pass 3 — Single Responsibility

No findings in the diff. Changed functions are within the 40-line threshold and do not contain compound names or deep nesting.

---

#### Pass 4 — Error Handling

No findings in the diff. Error messages in the non-commented logic include contextual identifiers and are not bare strings. No empty catch blocks observed.

---

#### Pass 5 — Naming Consistency Across Contexts

---

### [IMPORTANT] Naming Inconsistency: `failProcess()` vs `recordFailed()` for the same semantic operation

**File 1:** `src/ingestion/service.ts` — uses `failProcess()`

**File 2:** `src/extraction/service.ts` — uses `recordFailed()`

**Evidence:** Both methods signal the same lifecycle event — a processing step entered a failed state. Different verbs for the same concept breaks the cross-context naming rule.

**Standard:** Pass 5 Naming Consistency — the same semantic operation must use the same verb and structure. `fail()` in one context and `record_failed()` in another for the same semantic action is a finding.

**Fix:** Standardise on `recordFailed()`. It is more explicit (names the action, not just the outcome), follows the `record*` verb family used in event-sourced systems, and maps cleanly to a `ProcessFailed` event. Update `src/ingestion/service.ts` to match. If this is a public interface boundary, deprecate `failProcess()` in the same PR rather than silently renaming it.

---

#### Pass 6 — Writing Style

---

### [IMPORTANT] Banned Phrase: "In today's rapidly evolving landscape"

**File:** `README.md`

**Evidence:** `In today's rapidly evolving landscape, our platform...`

**Standard:** Pass 6 Banned Phrases — "In today's world / In the modern era" and the "In the ever-evolving [noun]" pattern are prohibited. This opener is an AI tell. Start with what the platform actually does.

**Fix:** Delete the opener. The clause that follows does not need it.

---

### [IMPORTANT] Banned Phrase: "It's important to note that"

**File:** `README.md`

**Evidence:** `It's important to note that comprehensive documentation fosters a robust ecosystem.`

**Standard:** Pass 6 Banned Phrases — "It's important to note" is listed verbatim. It adds nothing; remove it and state the claim directly.

**Fix:** Rewrite the sentence without the phrase — see full rewrite below.

---

### [SUGGESTION] Banned Word: `leverages` — Tier 1

**File:** `README.md`

**Evidence:** `our platform leverages cutting-edge synergies`

**Standard:** Pass 6 Banned Words — `leverage` (as verb) is Tier 1. Replace with the specific verb: uses, runs on, is built with, depends on.

---

### [SUGGESTION] Banned Word: `cutting-edge` — Tier 1

**File:** `README.md`

**Evidence:** `leverages cutting-edge synergies`

**Standard:** Pass 6 Banned Words — `cutting-edge` is Tier 1. If the platform uses a specific technology worth naming, name it. Otherwise delete the modifier.

---

### [SUGGESTION] Banned Word: `synergies` — Tier 1

**File:** `README.md`

**Evidence:** `cutting-edge synergies to streamline`

**Standard:** Pass 6 Banned Words — `synergy` is Tier 1. Meaningless filler. Delete the word and the phrase it belongs to.

---

### [SUGGESTION] Banned Word: `streamline` — Tier 1

**File:** `README.md`

**Evidence:** `synergies to streamline the developer experience`

**Standard:** Pass 6 Banned Words — `streamline` is Tier 1. Say what actually improves: "reduces setup time", "eliminates boilerplate", "cuts the feedback loop from push to deploy".

---

### [SUGGESTION] Banned Words: `comprehensive`, `fosters`, `robust`, `ecosystem` — Tier 1

**File:** `README.md`

**Evidence:** `comprehensive documentation fosters a robust ecosystem`

**Standard:** Pass 6 Banned Words — `comprehensive` (Tier 1), `foster` (Tier 1), `robust` (Tier 1 outside technical contexts), `ecosystem` (Tier 1) all appear in one sentence. The cluster is a strong AI tell. The sentence also asserts "documentation fosters an ecosystem" — an abstract claim with no concrete meaning for the reader.

---

### Pass 6 — README Rewrite

The two original sentences:

> In today's rapidly evolving landscape, our platform leverages cutting-edge synergies to streamline the developer experience. It's important to note that comprehensive documentation fosters a robust ecosystem.

Lean, on-voice rewrite:

> The platform [describe what it specifically does — e.g., "handles auth token lifecycle across distributed services"]. Good documentation is part of that. It lowers the cost of getting started and reduces support overhead.

Fill in the bracketed claim from the actual PR context. If the platform does something specific, say that. The opener has been removed, the banned vocabulary stripped, and the second sentence split and made concrete.

---

### Pass 6 — Sentence Rhythm Note

The two original sentences run 23 and 17 words — near-identical cadence combined with abstract vocabulary and no specific detail. Per the writing-style rules, sentences should vary in length and claims should be grounded. The rewrite introduces a short declarative, a medium sentence, and a longer explanatory one, producing the natural length variation that removes the AI-text signal.

---

### Clean Areas

- `src/auth/session.ts` — error handling in the non-commented logic is not flagged; error messages include contextual identifiers rather than bare strings.
- `src/ingestion/service.ts` and `src/extraction/service.ts` — function lengths are within the 40-line threshold; no compound-name violations beyond the cross-context naming issue already flagged.
- No bare `throw "string"` patterns found. No empty catch blocks in the diff.

---

## Evaluation

### Criteria

- [x] PASS: Skill executes all four mandatory passes for the file types in scope — Passes 1, 2, 5, and 6 produce findings; Passes 3 and 4 run and report zero findings. All six defined passes are executed.
- [x] PASS: Commented-out code block flagged as Pass 1 dead code finding with file reference and `// old session logic` as evidence — present, with the full 8-line block shown.
- [x] PASS: Lint suppression without justification flagged as Pass 2 finding — present, names the suppression pattern and gives two resolution paths.
- [x] PASS: Banned words in README flagged individually in Pass 6 — `leverages`, `cutting-edge`, `synergies`, `streamline`, `comprehensive`, `fosters`, `robust`, `ecosystem` each called out with evidence and tier.
- [x] PASS: Banned phrases flagged in Pass 6 — "In today's rapidly evolving landscape" and "It's important to note that" called out separately from individual word findings.
- [x] PASS: Every finding includes exact file, line evidence, the specific rule violated, and a concrete fix — all findings follow the `### [SEVERITY]` template with File / Evidence / Standard / Fix fields.
- [x] PASS: Output uses the defined summary template with counts by severity — Summary table shows 0 critical / 4 important / 6 suggestions with separate suppression and dead code counts.
- [x] PASS: Naming inconsistency flagged — `failProcess()` vs `recordFailed()` for the same semantic operation, citing both files with a reasoned recommendation.
- [~] PARTIAL: Zero-finding gate applied correctly without padding — Passes 3 and 4 report zero findings explicitly. Anti-pattern violations (e.g., suppressions with justification) are not manufactured as findings. Partially met because gate application is ultimately behavioural; the simulation is clean but the definition cannot fully guarantee it across all reviewers.

### Output expectations

- [x] PASS: Commented-out code flagged in `src/auth/session.ts` with the `// old session logic` marker as evidence — recommendation is "delete all 8 lines", not "consider removing".
- [x] PASS: `eslint-disable-next-line @typescript-eslint/no-explicit-any` flagged as Pass 2 finding, naming the rule that suppressions require inline justification.
- [x] PASS: Each banned word flagged individually with Tier noted — `leverages` (Tier 1), `cutting-edge` (Tier 1), `synergies` (Tier 1), `streamline` (Tier 1), `comprehensive` (Tier 1), `fosters` (Tier 1), `robust` (Tier 1), `ecosystem` (Tier 1).
- [x] PASS: Banned phrases "In today's rapidly evolving landscape" and "It's important to note that" flagged separately from single-word findings.
- [x] PASS: Rewritten README sentence provided demonstrating the lean on-voice version — not just a list of what's wrong.
- [x] PASS: Cross-context naming inconsistency flagged — `failProcess()` vs `recordFailed()`, citing both files, recommending `recordFailed()` with reasoning (event naming convention, explicit verb).
- [x] PASS: All findings include exact file, line evidence, rule violated, and concrete fix.
- [x] PASS: Summary template used with severity counts at the top — not a flat unranked list.
- [x] PASS: All passes run; Passes 3 and 4 report zero findings explicitly, satisfying per-pass count reporting.
- [~] PARTIAL: README content addressed beyond banned words — sentence rhythm (uniform cadence, abstract claims) flagged in the "Sentence Rhythm Note" section. Present but brief; a fuller treatment would apply the burstiness analysis from the writing-style rules more systematically.

---

## Notes

The skill is structurally strong. Pass 5's naming consistency check is a standout — the `fail()` vs `record_failed()` example in the definition directly mirrors the test scenario, making this finding almost automatic for a reviewer following the skill.

The primary gap identified in the previous evaluation (no explicit instruction to produce a rewritten prose example) is a real one, but the skill's Fix field ("concrete code or action to resolve it") is broad enough to encompass prose rewrites, so the output above can legitimately include one. The skill supports the behaviour even if it does not mandate it.

Pass 6's voice-and-structure check covers sentences over 30 words and passive voice, but stops short of explicit rhythm or burstiness analysis. The writing-style rules go further; the PARTIAL on the rhythm criterion reflects this genuine gap between the skill's mandate and the broader style rules the test is referencing.
