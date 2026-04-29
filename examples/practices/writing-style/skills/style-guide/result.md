# Output: style-guide review of documentation with multiple violations

**Verdict:** PARTIAL
**Score:** 15.5/18 criteria met (86%)
**Evaluated:** 2026-04-29

## Results

### Criteria (skill definition)

- [x] PASS: Step 2 identifies all banned words present — leverage, comprehensive, paradigm, facilitates, robust, utilized — each flagged with the exact occurrence — all six appear in the word substitution table; Step 2 is mandatory and instructs flagging with exact locations
- [x] PASS: Each banned word finding includes the exact original text and a specific rewrite, not just identification — the skill states "Every finding needs the exact text, the violated rule, and a specific rewrite. No exceptions."
- [x] PASS: "It's important to note that" is flagged as a banned phrase and removed in the rewrite — explicitly listed under Banned phrases — hard stops
- [x] PASS: Passive voice constructions ("is validated by", "are utilized") are identified in Step 3 and rewritten to active voice — Step 3 mandates active voice checking with the explicit example pattern "The service loads the configuration"
- [x] PASS: "Moving forward" is flagged as a banned phrase with a suggested rewrite — "going forward / moving forward → from now on, next" is in the substitution table
- [x] PASS: Missing Oxford commas are flagged in Step 4 — Oxford comma is listed as a mandatory rule under Step 4 with explicit wrong/right guidance
- [x] PASS: Output uses the defined findings table format with rule violated, original text, and specific rewrite for each finding — Output Format section specifies `| # | Rule violated | Original text | Rewrite |` exactly
- [~] PARTIAL: Overall assessment states whether the text is ready to publish or needs a revision pass — partially met: the Output Format includes a mandatory `### Overall assessment` block defined as "One sentence: is the text ready to publish, or does it need a revision pass?" so it will appear, but the skill provides no criteria for what threshold of findings tips the verdict one way or the other

### Output expectations (simulated output)

- [x] PASS: Output begins with a "## Style Review:" heading naming what was reviewed — mandated verbatim by the Output Format section: `## Style Review: [what was reviewed]`
- [x] PASS: Output's findings table uses exactly four columns in order: number, rule violated, original text, rewrite — the format template is `| # | Rule violated | Original text | Rewrite |`
- [x] PASS: Each rewrite preserves the technical meaning of the original — the skill instructs "Preserve the author's voice. Fix violations without rewriting the entire personality out of the text." The substitution table provides meaning-equivalent replacements (leverage→use, paradigm→model, etc.)
- [x] PASS: Rewrites for banned-word substitutions follow the skill's substitution table — the table explicitly maps leverage→use, comprehensive→complete/thorough/full, facilitate→help/enable, robust→strong/reliable/solid, utilize→use
- [x] PASS: At least one rewrite turns a passive construction into an active-voice sentence with an explicit subject — Step 3 mandates this and the example "The service loads the configuration" makes the pattern unambiguous; "is validated by the middleware layer" would become "The middleware validates the request payload"
- [x] PASS: Output produces a Summary block with numeric counts for total findings, banned words, structure issues, formatting issues, and context-specific issues — the Output Format specifies all five count lines by name
- [x] PASS: Findings include specific line/quote anchors (the exact original text in quotes) — the "Original text" column in the findings table is defined to hold quoted exact text
- [x] PASS: Output does not introduce any new banned words in its own rewrites or commentary — the skill's core principles and substitution table apply to all output the skill produces; a skill that enforces these rules on reviewed text applies them to its own prose as well
- [~] PARTIAL: Output groups or orders findings by step (Step 2 banned words, Step 3 structure, Step 4 formatting) rather than mixing them randomly — partially met: the skill defines three distinct mandatory steps each with a separate "Output:" instruction, but the Output Format template collapses everything into one undivided findings table with no grouping columns or sub-headings by step. A conforming response might naturally order findings step-by-step, but nothing in the format enforces it
- [~] PARTIAL: Output flags the API-documentation context and notes whether the rewritten version meets the README/API doc context-specific rules from Step 5 — partially met: Step 5 is mandatory and covers API documentation ("Start with what the endpoint does (one sentence)"), and the Summary includes a "Context-specific: [count]" line, but the Output Format provides no dedicated block for a context verdict and no explicit instruction to name the context type in the summary

## Notes

The skill is well-constructed. The substitution table covers every banned word in the prompt directly, and the Output Format template is specific enough that a conforming response would satisfy most criteria without ambiguity.

Two genuine gaps: the Output Format collapses all findings into a single table with no step grouping, so there is no structural guarantee that banned-word findings appear before structure findings before formatting findings. And Step 5 (context-specific rules) produces findings that land in the same table as everything else, with "Context-specific: [count]" in the Summary as the only marker — there is no block that explicitly identifies the content type and delivers a context verdict.

One minor tension in the skill: each step ends with an "Output:" instruction ("List of violations found with exact locations and rewrites", "Structure violations with specific rewrites", etc.) that implies step-level output, but the Output Format template assumes a single consolidated pass. A reviewer following the step instructions literally would produce four intermediate outputs before rolling up; one following the template would produce one output. This ambiguity could produce inconsistent structure across invocations.
