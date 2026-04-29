# Result: review-typescript any usage and client component misuse

## Evaluation

| Field | Value |
|---|---|
| **Test** | review-typescript any usage and client component misuse |
| **Type** | Skill |
| **Source** | `plugins/practices/coding-standards/skills/review-typescript/SKILL.md` |
| **Verdict** | PASS |
| **Score** | 17/18 criteria met (94%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Skill executes all six mandatory passes — met. "Execute all six passes. Do not skip." Pass 4 is fully defined and applies because the scenario uses Next.js.
- [x] PASS: Data fetching inside a Client Component is flagged as a Pass 4 finding — met. Pass 4 item 1 states "Data fetching belongs in Server Components. If a Client Component fetches data, that is a finding."
- [x] PASS: `const data: any` is flagged as a Pass 1 type safety finding with the specific line as evidence — met. Pass 1 item 1 lists `: any` as a grep target and the evidence format mandates file path with line number.
- [x] PASS: Missing return type on exported `getUserList` function is flagged as a Pass 1 finding — met. Pass 1 item 2 covers "every exported function and method must have an explicit return type."
- [x] PASS: Non-null assertion (`user!.profile.avatar`) is flagged as a Pass 1 finding with optional chaining or early return suggestion — met. Pass 1 item 4 targets `[a-zA-Z]!\.` and names "optional chaining" and "early returns" as fixes.
- [x] PASS: `"strict": false` in tsconfig is flagged as a critical Pass 1 finding — met. Pass 1 item 5 states "flag it as a critical finding" explicitly.
- [x] PASS: Each finding includes severity, pass label, file path with line reference, and a concrete code fix — met. The Evidence Format template mandates all four elements for every finding.
- [~] PARTIAL: Anti-patterns table references the relevant anti-pattern for each finding type — partially met. The table covers `as any` but has no entries for non-null assertions, missing return types, or `"strict": false`. Three of the four Pass 1 finding types in this scenario are absent from the table.

### Output expectations

- [x] PASS: Output would flag `'use client'` + data fetching as a Pass 4 finding with the server-component fix — met. Pass 4 item 1 directly mandates this; the fix (convert to Server Component or split into server-fetched parent + client-rendered child) is described in the pass instructions.
- [x] PASS: Output would flag `const data: any = response.json()` as a Pass 1 finding with `unknown` + narrowing or typed interface fix — met. Pass 1 item 1 covers `: any` and specifies "use `unknown` and narrow, define a specific type" as the fix.
- [x] PASS: Output would flag missing return type on `getUserList` with a concrete suggested signature — met. Pass 1 item 2 mandates explicit return types on exports and the Evidence Format requires a concrete fix block.
- [x] PASS: Output would flag `user!.profile.avatar` as a Pass 1 non-null-assertion finding with optional chaining fix — met. Pass 1 item 4 names optional chaining and early returns explicitly.
- [x] PASS: Output would flag `"strict": false` as a CRITICAL Pass 1 finding explaining impact — met. Pass 1 item 5 mandates "critical finding"; the skill does not enumerate the specific strict flags but the Evidence Format's `**Fix:**` requirement would prompt an explanation. Partially satisfied on the named-flags detail, but the criterion reads as met.
- [x] PASS: Output findings would include severity, pass label, file path with line reference, and a concrete code fix block — met. The Evidence Format template mandates all four elements.
- [x] PASS: Output would run all six passes and report per-pass finding counts including zeros — met. The Output Template mandates per-pass counts in the Summary section with "N/A" for inapplicable passes.
- [x] PASS: Overall verdict would be REQUEST_CHANGES — met. Four concurrent findings (one critical, three important) cannot produce an APPROVE under the skill's Zero-Finding Gate logic. The skill's severity framework implies REQUEST_CHANGES without ambiguity.
- [~] PARTIAL: Output would include practical impact of fetch-on-client (latency, CSR-only load, no server-side error handling, API exposure) — partially met. Pass 4 identifies client-side data fetching as a finding but does not enumerate these specific performance and security impacts. A well-formed response might include them, but the skill definition does not mandate them.
- [x] PASS: Anti-pattern references would include specific terms from the rules — met. `as any` is in the anti-patterns table; non-null assertion, client-side data fetching, and strict-mode-disabled are named in the pass instructions and would appear in finding output.

## Notes

The skill is well-specified for this scenario. The mandatory-pass structure, grep patterns, evidence format, and output template are all present and sufficient to produce correct findings. Pass 4 coverage is direct — the condition maps to the scenario without interpretation.

Two gaps worth noting. First, the anti-patterns table omits non-null assertions, strict mode, and missing return types — three of the four main Pass 1 finding types. The table also does not appear in the Output Template, so an agent following the template strictly might omit it from review output. Second, the skill does not prompt for practical-impact explanation on client-side data fetching (latency, LCP, API exposure). Reviewers following the skill would identify the violation but might not articulate why it matters beyond "belongs in Server Components."
