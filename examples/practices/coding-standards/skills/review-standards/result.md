# Result: review-standards dead code and writing violations

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 14.5 / 17 criteria met (85%) |
| **Evaluated** | 2026-04-29 |
| **Skill** | `plugins/practices/coding-standards/skills/review-standards/SKILL.md` |

## Results

### Criteria

- [x] PASS: Skill executes all mandatory passes for file types in scope — the definition states "Execute these checks in order. Do not skip steps." Six passes are defined; Pass 6 (writing style) is conditional on text content being present, and the README in the scenario triggers it.
- [x] PASS: Commented-out code flagged as Pass 1 finding — Pass 1 item 1 states "Any `// oldFunction()` or `/* former implementation */` is a violation. Version control preserves history; commented code is noise." The `// old session logic` block matches directly.
- [x] PASS: Lint suppression without justification flagged as Pass 2 finding — Pass 2 item 2 states "Each suppression must have an inline comment explaining why. Bare suppressions without explanation are always a finding." Unambiguous.
- [x] PASS: Banned words in README flagged individually in Pass 6 — Pass 6 item 1 names `leverage`, `cutting-edge`, `synergy`, `streamline`, `robust`, `ecosystem`, `comprehensive`, and `foster` explicitly. All eight root forms from the scenario's README copy are on the list.
- [x] PASS: Banned phrases flagged in Pass 6 — "It's important to note" is listed verbatim. "In today's world" / "In the modern era" covers "In today's rapidly evolving landscape." "Best practices" is explicitly listed.
- [x] PASS: Every finding includes file, line evidence, rule violated, and concrete fix — the Evidence Format section defines File/Evidence/Standard/Fix as mandatory fields for every finding.
- [x] PASS: Output template with counts by severity — the Output Template defines "X critical, Y important, Z suggestions" with separate suppression and dead code counts.
- [x] PASS: Inconsistent naming across bounded contexts flagged — Pass 5 item 2 states "the same operation must use the same verb and structure. `fail()` in one context and `record_failed()` in another for the same semantic action is a finding," which maps directly to `failProcess()` vs `recordFailed()`.
- [~] PARTIAL: Zero-finding gate applied correctly without padding — the Zero-Finding Gate section says "Do not manufacture findings to appear thorough" and the Anti-Patterns section lists four acceptable patterns. Both present. PARTIAL because gate application is behavioural; the definition supports correct behaviour but does not guarantee it.

### Output expectations

- [x] PASS: Output flags commented-out code block in `src/auth/session.ts` with line range and `// old session logic` as evidence, recommending deletion — met. Pass 1 step 1 establishes this as a violation with evidence required; "Version control preserves history; commented code is noise" implies delete, not "consider removing."
- [x] PASS: Output flags `// eslint-disable-next-line @typescript-eslint/no-explicit-any` without justification as a Pass 2 finding, naming the project rule — met. Pass 2 step 2 is explicit; the evidence format's Standard field would name the violated rule.
- [x] PASS: Output flags each banned word individually in Pass 6 — met. The skill instructs "flag any occurrence" and the evidence format requires individual findings with specific evidence per occurrence.
- [x] PASS: Output flags banned phrases "In today's rapidly evolving landscape" and "It's important to note that" separately from banned single-words — met. Pass 6 separates banned words (step 1) from banned phrases (step 2) explicitly.
- [ ] FAIL: Output provides a rewritten README sentence demonstrating the lean, on-voice version — not met. The Fix field in the evidence format says "concrete code or action to resolve it," but the skill never instructs reviewers to produce a rewritten prose version. A reviewer following the skill could write "remove 'leverages', use a direct verb" and satisfy every required field without producing an actual rewrite.
- [x] PASS: Output flags the cross-context naming inconsistency — `failProcess()` vs `recordFailed()` — citing both files and recommending which name to standardise on — met. Pass 5 requires flagging the inconsistency and the Fix field in the evidence template structurally requires a concrete recommendation. The skill does not mandate reasoning for the chosen name, but the criterion is satisfied at the level of "recommending which name."
- [x] PASS: Output's findings each include exact file, line evidence, the specific rule violated (named or quoted), and a concrete fix — met. The evidence format template enforces this for every finding.
- [x] PASS: Output uses the defined summary template with counts by severity at the top, not a flat unranked list — met. The output template places the summary first with severity-grouped findings below.
- [x] PASS: Output runs all four mandatory passes for the file types in scope — met. The skill defines six passes (more than four), all mandatory, covering the file types in scope. Per-pass finding counts are not explicitly required by the output template, but the criterion is met at the "runs all passes" level.
- [~] PARTIAL: Output addresses README content beyond banned words — flags AI-tells in sentence rhythm per writing-style rules — partially met. Pass 6 step 3 covers "sentences over 30 words — split or tighten" and passive voice, but the skill does not instruct sentence-length variance analysis, burstiness checks, or abstract-claim identification. Some structural tells are caught; rhythm analysis is not mandated.

## Notes

The skill is structurally strong. Pass 5 is a standout — the `fail()` vs `record_failed()` example in item 2 directly mirrors the test scenario, making the naming consistency finding almost guaranteed from a well-formed reviewer following the skill.

The primary gap is the rewritten-prose expectation. The Fix field in the evidence template covers "concrete code or action," but prose rewrites for writing-style violations require explicit instruction to produce a rewritten example rather than a corrective label. Without that instruction, the skill supports but does not enforce the rewrite.

The writing-style pass (Pass 6) is narrower than the full tone-and-voice rules. It catches vocabulary and some structural patterns but stops short of rhythm analysis — the test's PARTIAL criterion on sentence-length variance and abstract claims reflects a genuine gap between what the skill mandates and what the broader writing-style rule requires.

Criterion 1 wording ("all four mandatory passes") predates Pass 5 being added, making the count stale. The skill now defines six passes; the criterion is still met since more is not fewer.
