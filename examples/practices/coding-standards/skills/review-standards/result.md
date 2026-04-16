# Review standards dead code and writing violations

A developer submits a PR with commented-out code, an unjustified lint suppression, and a README update containing several banned phrases. The review-standards skill covers cross-cutting concerns across all these file types.

## Prompt

> Review this PR. `src/auth/session.ts` has a block of 8 lines commented out with `// old session logic` above it, plus a `// eslint-disable-next-line @typescript-eslint/no-explicit-any` with no justification comment. The `README.md` update contains: "In today's rapidly evolving landscape, our platform leverages cutting-edge synergies to streamline the developer experience. It's important to note that comprehensive documentation fosters a robust ecosystem."

```markdown

## Output

### General Standards Review

#### Summary
- Files reviewed: 2 (src/auth/session.ts, README.md)
- Findings: 0 critical, 2 important, 9 suggestions
- Suppressions: 1 found, 1 unjustified
- Dead code: 1 instance

#### Findings

##### IMPORTANT [Pass 1]: Commented-out code block


| Field | Value |
|---|---|
| File | `src/auth/session.ts` (block following `// old session logic`) |
| Evidence | 8 lines of commented code preceded by `// old session logic` |
| Standard | Commented-out code is noise. Version control preserves history. Any `// oldFunction()` or `/* former implementation */` is a violation. |
| Fix | Delete the commented block entirely. |


---

##### IMPORTANT [Pass 2]: Lint suppression without justification


| Field | Value |
|---|---|
| File | `src/auth/session.ts` |
| Evidence | `// eslint-disable-next-line @typescript-eslint/no-explicit-any` with no inline explanation |
| Standard | Each suppression must have an inline comment explaining why. Bare suppressions without explanation are always a finding. |
| Fix | Add justification: `// eslint-disable-next-line @typescript-eslint/no-explicit-any — third-party webhook payload has no type stubs` |


---

##### SUGGESTION [Pass 5]: Banned phrase — "In today's rapidly evolving landscape"


| Field | Value |
|---|---|
| File | `README.md` |
| Evidence | "In today's rapidly evolving landscape" (opening sentence) |
| Standard | Banned phrase: "In today's world" / "In the modern era". Also matches banned word: `landscape` (metaphorical use). |
| Fix | Delete the opener and start with what the platform does. |


---

##### SUGGESTION [Pass 5]: Banned word — "leverage"


| Field | Value |
|---|---|
| File | `README.md` |
| Evidence | "our platform leverages cutting-edge synergies" |
| Standard | `leverage` is on the banned word list |
| Fix | "our platform uses..." |


---

##### SUGGESTION [Pass 5]: Banned word — "cutting-edge"


| Field | Value |
|---|---|
| File | `README.md` |
| Evidence | "leverages cutting-edge synergies" |
| Standard | `cutting-edge` is on the banned word list |
| Fix | Describe the actual capability instead |


---

##### SUGGESTION [Pass 5]: Banned word — "synergy"


| Field | Value |
|---|---|
| File | `README.md` |
| Evidence | "cutting-edge synergies to streamline" |
| Standard | `synergy` is on the banned word list |
| Fix | Delete — the word adds nothing |


---

##### SUGGESTION [Pass 5]: Banned word — "streamline"


| Field | Value |
|---|---|
| File | `README.md` |
| Evidence | "synergies to streamline the developer experience" |
| Standard | `streamline` is on the banned word list |
| Fix | "simplify" or describe what specifically becomes easier |


---

##### SUGGESTION [Pass 5]: Banned phrase — "It's important to note"


| Field | Value |
|---|---|
| File | `README.md` |
| Evidence | "It's important to note that comprehensive documentation..." |
| Standard | Banned phrase: "It's important to note" — just state the fact |
| Fix | Delete the phrase: "Comprehensive documentation..." |


---

##### SUGGESTION [Pass 5]: Banned word — "comprehensive"


| Field | Value |
|---|---|
| File | `README.md` |
| Evidence | "that comprehensive documentation fosters" |
| Standard | `comprehensive` is on the banned word list |
| Fix | Be specific about what the docs cover |


---

##### SUGGESTION [Pass 5]: Banned word — "foster"


| Field | Value |
|---|---|
| File | `README.md` |
| Evidence | "documentation fosters a robust ecosystem" |
| Standard | `foster` is on the banned word list |
| Fix | "supports", "builds", "creates" |


---

##### SUGGESTION [Pass 5]: Banned word — "robust"


| Field | Value |
|---|---|
| File | `README.md` |
| Evidence | "a robust ecosystem" |
| Standard | `robust` is on the banned word list (outside technical contexts) |
| Fix | Delete or replace |


---

##### SUGGESTION [Pass 5]: Banned word — "ecosystem"


| Field | Value |
|---|---|
| File | `README.md` |
| Evidence | "a robust ecosystem" |
| Standard | `ecosystem` is on the banned word list |
| Fix | "platform", "community", or rewrite the sentence to say something specific |


#### Clean Areas

`src/auth/session.ts` has no single-responsibility violations (Pass 3) or error handling issues (Pass 4) in the changed portions.
```

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/7.5 (100%) |
| Evaluated | 2026-04-16 |


- [x] PASS: Skill executes all passes for the file types in scope — the definition states "Execute these checks in order. Do not skip steps." The skill has five passes (Pass 1–5). The criterion says "four mandatory passes" which under-counts, but all passes applicable to the in-scope files are executed. Pass 5 is conditional ("Only run this pass if the diff includes documentation...") and the README update triggers it. No pass is skipped.
- [x] PASS: Commented-out code flagged as Pass 1 finding — Pass 1 step 1 states "Any `// oldFunction()` or `/* former implementation */` is a violation. Version control preserves history; commented code is noise." The `// old session logic` block matches this rule. The Evidence Format section mandates file reference and exact evidence.
- [x] PASS: Lint suppression without justification flagged as Pass 2 finding — Pass 2 step 2 states "Each suppression must have an inline comment explaining why. Bare suppressions without explanation are always a finding." The definition is unambiguous.
- [x] PASS: Banned words flagged individually in Pass 5 — the definition's Pass 5 step 1 list includes `leverage`, `cutting-edge`, `synergy`, `streamline`, `robust`, `ecosystem`, `comprehensive`, and `foster` — all root forms of the words in the prompt. The criterion lists inflected forms (`synergies`, `fosters`, `leverages`) but these are caught by flagging the root forms, which the definition explicitly names.
- [x] PASS: Banned phrases flagged in Pass 5 — step 2 explicitly lists "It's important to note" and "In today's world" / "In the modern era" as banned phrases. The prompt's "In today's rapidly evolving landscape" matches the "In today's world" pattern. Both phrases in the prompt are caught by named entries in the definition.
- [x] PASS: Evidence format followed — the Evidence Format section defines `### [SEVERITY] [Category]: [Short description]` with `File/Evidence/Standard/Fix` as mandatory fields for every finding. The definition makes this structure explicit and required.
- [x] PASS: Output uses the defined summary template — the Output Template section defines the exact summary format: `Files reviewed: N`, `Findings: X critical, Y important, Z suggestions`, `Suppressions: N found, M unjustified`, `Dead code: N instances`. The simulated output matches this template.
- [~] PARTIAL: Zero-finding gate applied correctly — the Zero-Finding Gate section states "Do not manufacture findings to appear thorough." The Anti-Patterns section lists four acceptable patterns (including "Suppressions with a linked issue number and explanation") as not-to-flag items. Both mechanisms are present in the definition. The PARTIAL ceiling is set by the test author regardless of outcome.

### Notes

The review-standards skill is well-specified for this scenario. All eight banned words in the prompt appear by their root forms in Pass 5 step 1. The two banned phrases are explicitly listed in Pass 5 step 2. The Anti-Patterns section provides a concrete list of what NOT to flag (short utility functions, justified suppressions, template-comment code in tests, factory patterns with many parameters) — this is the anti-padding mechanism the criterion tests. One minor note: the criterion mentions "best practices pattern" but no best-practices text appears in the prompt, so this goes untested. The definition does address it in Pass 5 step 2: `"Best practices" (say what the practice actually is)`.
