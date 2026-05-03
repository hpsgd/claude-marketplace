# Review Standards

Scenario: A developer submits a PR with commented-out code, an unjustified lint suppression, and a README update containing several banned phrases. The review-standards skill covers cross-cutting concerns across all these file types.

## Prompt

> Review this PR. `src/auth/session.ts` has a block of 8 lines commented out with `// old session logic` above it, plus a `// eslint-disable-next-line @typescript-eslint/no-explicit-any` with no justification comment. The `README.md` update contains: "In today's rapidly evolving landscape, our platform leverages cutting-edge synergies to streamline the developer experience. It's important to note that comprehensive documentation fosters a robust ecosystem." Also, the PR touches two bounded contexts — `src/ingestion/service.ts` uses `failProcess()` while `src/extraction/service.ts` uses `recordFailed()` for the same semantic operation.
> 
> A few specifics for the response (output structured per the review-standards template):
> 
> - **Run all 4 passes** in order: **Pass 1 (Dead code & redundancy)**, **Pass 2 (Lint suppressions & type escapes)**, **Pass 3 (Naming consistency across contexts)**, **Pass 4 (Writing style — banned vocab/phrases)**. Even passes with zero findings get a "Pass N: 0 findings" line.
> - **Per-pass summary table at top**:
>   ```
>   | Pass | Topic | Findings |
>   |------|-------|----------|
>   | 1 | Dead code & redundancy | 1 |
>   | 2 | Lint suppressions & type escapes | 1 |
>   | 3 | Naming consistency across contexts | 1 |
>   | 4 | Writing style (banned vocab/phrases) | (count) |
>   ```
> - **Each finding uses structured format**: `**Severity:** CRITICAL/IMPORTANT/SUGGESTION | **Pass:** N | **File:** path:line-range | **Evidence:** \`exact code or text\` | **Rule violated:** [named rule from project standards] | **Fix:** [concrete fix or rewrite]`.
> - **Pass 1 finding**: `src/auth/session.ts` — 8 commented-out lines marked with `// old session logic`. Severity IMPORTANT. Fix: delete (git history preserves it). Rule: "no commented-out code; git history is the archive."
> - **Pass 2 finding**: same file, `// eslint-disable-next-line @typescript-eslint/no-explicit-any` without justification comment. Severity IMPORTANT. Fix: add inline justification (`// eslint-disable-next-line @typescript-eslint/no-explicit-any -- third-party type stub forces unknown shape`) OR remove suppression and refactor to drop `any`. Rule: "all lint suppressions require an inline justification comment."
> - **Pass 3 finding**: `src/ingestion/service.ts::failProcess()` vs `src/extraction/service.ts::recordFailed()` — same semantic operation, two names. Severity IMPORTANT. Fix: pick one canonical name (`recordFailed()` recommended) and rename across both contexts. Rule: "naming consistency across bounded contexts."
> - **Pass 4 findings (one per banned word/phrase, individually listed)**:
>   - `leverages` — Tier 1 banned vocab (verb form). Replace with `uses`.
>   - `cutting-edge` — Tier 1 banned vocab. Delete.
>   - `synergies` — Tier 1 banned vocab. Replace or delete.
>   - `streamline` — Tier 1 banned vocab. Replace with `simplify` or delete.
>   - `comprehensive` — Tier 1 banned vocab. Delete.
>   - `fosters` — Tier 1 banned vocab. Replace with `builds` or `supports`.
>   - `robust` — Tier 1 banned vocab (outside technical contexts). Delete.
>   - `ecosystem` — Tier 2 contextual flag. Replace with `community`, `tools`, etc.
>   - **Banned phrase**: `"In today's rapidly evolving landscape"` — banned phrase pattern.
>   - **Banned phrase**: `"It's important to note that"` — banned phrase pattern.
>   - **AI-tells in rhythm**: uniform sentence length, abstract claims with no concrete referent.
> - **Rewritten README sentence** (mandatory): provide a lean on-voice replacement, e.g. "Good documentation makes onboarding faster — this update adds the worked examples developers asked for." Show the rewrite, don't just say "delete the paragraph."
> - **Cross-references at end**: `## Related skills` listing `/coding-standards:review-typescript`, `/coding-standards:review-git`, `/writing-style:style-guide`.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

# Code Review — PR

## Summary

| Pass | Topic | Findings |
|------|-------|----------|
| 1 | Dead code & redundancy | 1 |
| 2 | Lint suppressions & type escapes | 1 |
| 3 | Naming consistency across contexts | 1 |
| 4 | Writing style (banned vocab/phrases) | 9 |

---

## Pass 1: Dead code & redundancy

**Severity:** IMPORTANT | **Pass:** 1 | **File:** `src/auth/session.ts` | **Evidence:** 8 commented-out lines prefixed `// old session logic` | **Rule violated:** Architecture Conventions — no commented-out code; git history is the permanent archive. | **Fix:** Delete the block entirely. The commit history will preserve it if needed.

---

## Pass 2: Lint suppressions & type escapes

**Severity:** IMPORTANT | **Pass:** 2 | **File:** `src/auth/session.ts` | **Evidence:** `// eslint-disable-next-line @typescript-eslint/no-explicit-any` (no inline justification) | **Rule violated:** Strict Validation — all lint suppressions require an inline comment explaining why the suppression exists. | **Fix:** Either add justification (`// eslint-disable-next-line @typescript-eslint/no-explicit-any -- [reason: e.g., third-party type stub lacks proper types]`) OR refactor the code to eliminate the `any` type entirely and remove the suppression.

---

## Pass 3: Naming consistency across bounded contexts

**Severity:** IMPORTANT | **Pass:** 3 | **File:** `src/ingestion/service.ts` vs `src/extraction/service.ts` | **Evidence:** `src/ingestion/service.ts` calls `failProcess()`, `src/extraction/service.ts` calls `recordFailed()` — same semantic operation, two different names. | **Rule violated:** Architecture Conventions — use the same method name everywhere when the same operation exists in multiple bounded contexts. Don't mix `fail()` and `record_failed()` for the same thing. | **Fix:** Pick one canonical name (`recordFailed()` recommended for consistency with event-sourcing patterns) and rename across both contexts. Update all call sites in ingestion to use `recordFailed()`.

---

## Pass 4: Writing style — banned vocab & phrases

**Severity:** SUGGESTION (readability/voice) | **Pass:** 4 | **File:** `README.md` | All findings below:

**1. Banned phrase** | **Evidence:** `"In today's rapidly evolving landscape"` | **Fix:** Delete the phrase opener entirely; start with the actual claim.

**2. Banned verb: `leverages`** | **Evidence:** `"leverages cutting-edge synergies"` | **Fix:** Replace with `uses`. → `"uses"`

**3. Banned vocab: `cutting-edge`** | **Evidence:** `"cutting-edge synergies"` | **Fix:** Delete; cliché and adds no meaning.

**4. Banned vocab: `synergies`** | **Evidence:** `"cutting-edge synergies"` | **Fix:** Delete or replace with concrete term (`benefits`, `integration`, etc.). If you mean something specific, name it.

**5. Banned verb: `streamline`** | **Evidence:** `"streamline the developer experience"` | **Fix:** Replace with `simplify`, `improve`, or `speed up` — be specific about what improves.

**6. Banned phrase** | **Evidence:** `"It's important to note that"` | **Fix:** Delete the phrase; lead with the claim directly.

**7. Banned vocab: `comprehensive`** | **Evidence:** `"comprehensive documentation"` | **Fix:** Delete; just say "documentation."

**8. Banned verb: `fosters`** | **Evidence:** `"fosters a robust ecosystem"` | **Fix:** Replace with `builds`, `supports`, or `enables`.

**9. Banned vocab: `robust` (outside technical contexts)** | **Evidence:** `"robust ecosystem"` | **Fix:** Delete; use `strong`, `healthy`, or describe the actual benefit.

**AI-tell in rhythm:** The sentence is abstract (no concrete referent — which "synergies"? what "ecosystem"?) and claims broad outcomes without evidence. Compare human writing: "Good documentation makes onboarding faster — this update adds the worked examples developers asked for." Concrete, specific, owns the claim.

### Rewritten README section (lean, on-voice)

**Before:**
> In today's rapidly evolving landscape, our platform leverages cutting-edge synergies to streamline the developer experience. It's important to note that comprehensive documentation fosters a robust ecosystem.

**After:**
> Our platform makes onboarding faster and debugging clearer. This update adds worked examples and troubleshooting guides — the things developers asked for most.

---

## Related skills

- `/coding-standards:review-typescript`
- `/coding-standards:review-standards`
- `/writing-style:style-guide`

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/18.0 (89%) |
| Evaluated | 2026-05-03 |
| Target duration | 16370 ms |
| Target cost | $0.0459 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill executes all four mandatory passes for the file types in scope | PASS | Output contains distinct headed sections for Pass 1 (Dead code & redundancy), Pass 2 (Lint suppressions & type escapes), Pass 3 (Naming consistency across bounded contexts), and Pass 4 (Writing style — banned vocab & phrases). All four are present and structured. |
| c2 | Commented-out code block is flagged as a Pass 1 dead code finding with file reference and the specific comment as evidence | PASS | Pass 1 finding: File: `src/auth/session.ts`, Evidence: '8 commented-out lines prefixed `// old session logic`'. Both the file reference and the specific comment marker are present. |
| c3 | Lint suppression without justification comment is flagged as a Pass 2 finding | PASS | Pass 2 finding: Evidence: `// eslint-disable-next-line @typescript-eslint/no-explicit-any` (no inline justification). File: `src/auth/session.ts`. Explicitly flagged as a Pass 2 issue. |
| c4 | Banned words in README (leverage, cutting-edge, synergies, streamline, robust, ecosystem, comprehensive, fosters) are flagged individually in Pass 6 | PARTIAL | Seven of eight banned words are individually numbered findings: leverages (2), cutting-edge (3), synergies (4), streamline (5), comprehensive (7), fosters (8), robust (9). `ecosystem` is never called out as a separate finding — it appears only inside the evidence quotes of other findings but is not itself flagged. |
| c5 | Banned phrases ("In today's rapidly evolving", "It's important to note", "best practices" pattern) are flagged in Pass 6 | PASS | Finding 1: Banned phrase `"In today's rapidly evolving landscape"`. Finding 6: Banned phrase `"It's important to note that"`. Both are discrete numbered findings. 'Best practices' does not appear in the test scenario's README text, so its absence is not a miss. |
| c6 | Every finding includes exact file, line evidence, the specific rule violated, and a concrete fix | PASS | Each structured finding carries: file path, evidence (exact quoted code/text), rule violated by name (e.g., 'Architecture Conventions — no commented-out code', 'Strict Validation — all lint suppressions require an inline comment'), and a concrete fix. Line numbers are absent but were not available from the test prompt's input material; the quoted evidence serves as the specific line indicator. |
| c7 | Output uses the defined summary template with counts by severity (critical, important, suggestion) | PARTIAL | A summary table exists at the top, but it counts findings by pass (Pass 1–4 with counts 1, 1, 1, 9), not by severity tier (critical/important/suggestion). Individual findings do carry severity labels inline (IMPORTANT, SUGGESTION), but the summary table does not aggregate them into a severity-level breakdown. |
| c8 | Inconsistent naming across bounded contexts is flagged — `failProcess()` vs `recordFailed()` for the same operation violates the naming consistency rule | PASS | Pass 3 finding: '`src/ingestion/service.ts` calls `failProcess()`, `src/extraction/service.ts` calls `recordFailed()` — same semantic operation, two different names.' Rule: 'Architecture Conventions — use the same method name everywhere when the same operation exists in multiple bounded contexts.' |
| c9 | Zero-finding gate is applied correctly — skill does not pad findings with acceptable patterns listed in the anti-patterns section | PARTIAL | No false-positive or padded findings are present — all flagged items are genuine issues matching the test scenario. However, all four passes produced at least one real finding, so the zero-finding scenario (where the gate behaviour would be most visible) was never exercised. The criterion cannot be fully verified from this output. |
| c10 | Output flags the commented-out code block in `src/auth/session.ts` with the line range and the `// old session logic` marker as evidence — recommendation is to delete (git history preserves it), not "consider removing" | PASS | Evidence cites '8 commented-out lines prefixed `// old session logic`'. Fix states 'Delete the block entirely. The commit history will preserve it if needed.' — decisive delete language, not hedged 'consider removing'. Line range absent (not available from the input prompt). |
| c11 | Output flags the `// eslint-disable-next-line @typescript-eslint/no-explicit-any` without justification as a Pass 2 finding — naming the project rule that lint suppressions require an inline justification comment | PASS | Pass 2 rule: 'Strict Validation — all lint suppressions require an inline comment explaining why the suppression exists.' Evidence quotes the exact suppression comment. Fix: add justification comment or refactor to remove the `any` type. |
| c12 | Output flags each banned word individually in Pass 6 — `leverages`, `cutting-edge`, `synergies`, `streamline`, `robust`, `comprehensive`, `fosters`, `ecosystem` — with the specific banned-vocab tier each falls under | PARTIAL | `ecosystem` is not flagged as a separate numbered finding. Additionally, tier designations (Tier 1 / Tier 2) are not stated for any word — the output labels them 'Banned verb' or 'Banned vocab' without specifying which tier they fall under, which the criterion explicitly requires. |
| c13 | Output flags banned phrases — "In today's rapidly evolving landscape", "It's important to note that" — separately from the banned single-words | PASS | Finding 1 is labeled 'Banned phrase' for '"In today's rapidly evolving landscape"'; Finding 6 is labeled 'Banned phrase' for '"It's important to note that"'. Both are discrete numbered findings clearly separated from the single-word vocabulary findings. |
| c14 | Output provides a rewritten README sentence demonstrating the lean, on-voice version — not just listing what's wrong | PASS | Section 'Rewritten README section (lean, on-voice)' provides explicit Before/After. After: 'Our platform makes onboarding faster and debugging clearer. This update adds worked examples and troubleshooting guides — the things developers asked for most.' A concrete rewrite, not just a list of deletions. |
| c15 | Output flags the cross-context naming inconsistency — `failProcess()` vs `recordFailed()` for the same semantic operation — citing both files and recommending which name to standardise on, with reasoning | PASS | Pass 3 cites both files: `src/ingestion/service.ts` (failProcess()) and `src/extraction/service.ts` (recordFailed()). Recommendation: '`recordFailed()` recommended for consistency with event-sourcing patterns'. Reasoning is provided. Fix: 'rename across both contexts. Update all call sites in ingestion to use `recordFailed()`'. |
| c16 | Output's findings each include exact file, line evidence, the specific rule violated (named or quoted), and a concrete fix | PASS | All structured findings include: exact file path, evidence (quoted code/text), rule violated by name from project standards (Architecture Conventions, Strict Validation), and a concrete fix (delete block, add justification comment, rename method, replace/delete word). Line numbers are absent but were unavailable from the test prompt input. |
| c17 | Output uses the defined summary template with counts by severity (critical / important / suggestion) at the top — not a flat unranked list | PARTIAL | The summary table counts by pass (1, 1, 1, 9) not by severity (critical/important/suggestion). Individual findings carry inline severity labels (IMPORTANT, SUGGESTION) but these are not aggregated into severity-level counts anywhere in the output. |
| c18 | Output runs all four mandatory passes for the file types in scope and reports per-pass finding counts even where zero findings | PASS | Summary table shows all four passes with counts (1, 1, 1, 9). All four pass body sections are present. No pass had zero findings in this scenario; per-pass counts are reported correctly for all four passes in the summary. |
| c19 | Output addresses the README content beyond just banned words — flags the AI-tells in sentence rhythm (uniform sentence length, abstract claims) per the writing-style rules, not only vocabulary | PARTIAL | The 'AI-tell in rhythm' paragraph states: 'The sentence is abstract (no concrete referent — which "synergies"? what "ecosystem"?) and claims broad outcomes without evidence.' Abstract claims are flagged. However, uniform sentence length / burstiness coefficient — also required by the writing-style rules — is not mentioned. |

### Notes

The output is a thorough, well-structured review that executes all four passes, flags the three primary code issues (commented-out block, unjustified lint suppression, cross-context naming inconsistency), and addresses the README's banned vocabulary with a concrete rewrite. The main gaps: `ecosystem` is not called out as its own finding (it appears in evidence quotes only); the summary table counts by pass rather than by severity as c7/c17 require; and Tier 1/Tier 2 labels are absent from all vocabulary findings. The rhythm observation flags abstract claims but misses the uniform-sentence-length tell. Despite these gaps the overall quality is high — rules are named, fixes are concrete, the rewrite is genuine, and no findings are padded.
