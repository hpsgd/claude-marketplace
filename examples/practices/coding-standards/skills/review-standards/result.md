# Result: review-standards dead code and writing violations

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 8.5 / 9 criteria met (94%) |
| **Evaluated** | 2026-04-16 |
| **Skill** | `plugins/practices/coding-standards/skills/review-standards/SKILL.md` |

## Results

- [x] PASS: Skill executes all mandatory passes for file types in scope — the definition states "Execute these checks in order. Do not skip steps." Six passes are defined; Pass 6 (writing style) is conditional on text content being present, and the README in the scenario triggers it
- [x] PASS: Commented-out code flagged as Pass 1 finding — Pass 1 item 1 states "Any `// oldFunction()` or `/* former implementation */` is a violation. Version control preserves history; commented code is noise." The `// old session logic` block matches this rule directly
- [x] PASS: Lint suppression without justification flagged as Pass 2 finding — Pass 2 item 2 states "Each suppression must have an inline comment explaining why. Bare suppressions without explanation are always a finding." The rule is unambiguous
- [x] PASS: Banned words in README flagged individually in Pass 6 — Pass 6 item 1 names `leverage`, `cutting-edge`, `synergy`, `streamline`, `robust`, `ecosystem`, `comprehensive`, and `foster` explicitly. All eight root forms from the scenario's README copy appear in the word list
- [x] PASS: Banned phrases flagged in Pass 6 — Pass 6 item 2 lists "It's important to note" and "In today's world" / "In the modern era" as banned phrases; "In today's rapidly evolving landscape" matches the "In today's world" entry
- [x] PASS: Every finding includes file, line evidence, rule violated, and concrete fix — the Evidence Format section defines `File/Evidence/Standard/Fix` as mandatory fields for every finding
- [x] PASS: Output template with counts by severity — the Output Template defines `Findings: X critical, Y important, Z suggestions` with separate suppression and dead code counts
- [x] PASS: Inconsistent naming across bounded contexts flagged — Pass 5 (Naming Consistency Across Contexts) now explicitly covers this: item 2 states "the same operation must use the same verb and structure. `fail()` in one context and `record_failed()` in another for the same semantic action is a finding", which maps directly to `failProcess()` vs `recordFailed()` in the scenario
- [~] PARTIAL: Zero-finding gate applied correctly without padding — the Zero-Finding Gate section states "Do not manufacture findings to appear thorough" and the Anti-Patterns section lists four explicitly acceptable patterns. Both are present. The PARTIAL reflects that correct gate application is inherently a behavioural question the definition supports but cannot guarantee

## Notes

Pass 5 is a clean addition. The `fail()` vs `record_failed()` example in item 2 lands close enough to the test's `failProcess()` vs `recordFailed()` scenario that a reviewer following the skill would catch it without needing the exact names spelled out. Items 1 and 3 round out the check with a cross-context scan instruction and a scope clarification (public/exported methods matter most, internal helpers are secondary).

The criterion wording in the test references "Pass 6" for banned words and phrases — the skill renumbered writing style from the former Pass 5 to Pass 6 when naming consistency was inserted. The criteria reflect that renumbering correctly and the results align.

One observation worth noting: the skill now has six passes but criterion 1 says "all four mandatory passes." That count was written against the older version. It's met (the skill runs more passes, not fewer) but the criterion wording is stale.
