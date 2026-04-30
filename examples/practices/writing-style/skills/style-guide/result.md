# Result: style-guide review of documentation with multiple violations

**Verdict:** PASS
**Score:** 15.5/18.5 criteria met (84%)
**Evaluated:** 2026-04-30

## Output

The following is a simulated invocation of `/style-guide` against the API documentation snippet from the prompt.

---

## Style Review: API documentation snippet

### Findings

| # | Rule violated | Original text | Rewrite |
|---|---|---|---|
| 1 | Banned word — `leverage` | "The endpoint leverages a comprehensive authentication paradigm" | "The endpoint uses a full authentication model" |
| 2 | Banned word — `comprehensive` | "a comprehensive authentication paradigm" | "a full authentication model" (already covered in #1 rewrite) |
| 3 | Banned word — `paradigm` | "authentication paradigm" | "authentication model" |
| 4 | Banned word — `facilitates` | "that facilitates robust access control" | "that provides strong access control" |
| 5 | Banned word — `robust` | "robust access control" | "strong access control" |
| 6 | Banned phrase — "It's important to note that" | "It's important to note that the request payload is validated" | "The middleware validates the request payload before processing." |
| 7 | Passive voice | "the request payload is validated by the middleware layer" | "The middleware layer validates the request payload" |
| 8 | Passive voice + banned word | "Tokens are utilized to ensure that" | "Tokens restrict access to authorized users." |
| 9 | Banned word — `utilized` | "are utilized" | "are used" |
| 10 | Missing Oxford comma | "authorized, authenticated and verified users" | "authorized, authenticated, and verified users" |
| 11 | Banned phrase — "Moving forward" | "Moving forward, we will be adding support for" | "Next, we will add support for" |
| 12 | Missing Oxford comma | "OAuth 2.0, SAML and API key authentication mechanisms" | "OAuth 2.0, SAML, and API key authentication mechanisms" |

### Summary

- Total findings: 12
- Banned words: 5 (leverage, comprehensive, paradigm, facilitates/facilitate, robust, utilized)
- Structure issues: 2 (passive voice × 2)
- Formatting issues: 2 (missing Oxford commas × 2)
- Context-specific: 1 (API docs: endpoint description buries lead; no parameters, example request, or example response present)

### Overall assessment

This text needs a revision pass before publishing — it contains six banned word violations, two passive constructions, two missing Oxford commas, and a banned phrase, and the API documentation context requires additions (parameters table, example request/response) that are entirely absent.

---

**Cleaned rewrite for reference:**

> The endpoint uses a full authentication model that provides strong access control. The middleware layer validates the request payload before processing it. Tokens restrict access to authorized, authenticated, and verified users. Next, we will add support for OAuth 2.0, SAML, and API key authentication mechanisms.

---

## Evaluation

### Criteria (skill definition)

- [x] PASS: Step 2 identifies all banned words present — leverage, comprehensive, paradigm, facilitates, robust, utilized — each flagged with the exact occurrence. All six map directly to the substitution table; Step 2 is mandatory with instruction to flag exact locations.
- [x] PASS: Each banned word finding includes the exact original text and a specific rewrite. The skill states "Every finding needs the exact text, the violated rule, and a specific rewrite. No exceptions."
- [x] PASS: "It's important to note that" is flagged as a banned phrase and removed in the rewrite. Explicitly listed under Banned phrases — hard stops.
- [x] PASS: Passive voice constructions ("is validated by", "are utilized") are identified in Step 3 and rewritten to active voice. Step 3 mandates active voice checking with the pattern "The service loads the configuration."
- [x] PASS: "Moving forward" is flagged as a banned phrase. "going forward / moving forward → from now on, next" is in the substitution table.
- [x] PASS: Missing Oxford commas flagged in Step 4. Oxford comma is listed as a mandatory rule under Step 4 with explicit wrong/right examples.
- [x] PASS: Output uses the defined findings table format with rule violated, original text, and specific rewrite for each finding. Output Format specifies `| # | Rule violated | Original text | Rewrite |` exactly.
- [~] PARTIAL: Overall assessment states whether text is ready to publish or needs revision. The Output Format mandates a `### Overall assessment` block, so the verdict will appear, but the skill defines no threshold for what finding count or severity tips the verdict — the assessment is produced but its content is under-specified.

### Output expectations (simulated output)

- [x] PASS: Output begins with `## Style Review:` heading naming what was reviewed. Mandated verbatim by the Output Format section.
- [x] PASS: Findings table uses exactly four columns in order: number, rule violated, original text, rewrite. The format template is unambiguous.
- [x] PASS: Each rewrite preserves technical meaning. The skill instructs "Preserve the author's voice. Fix violations without rewriting the entire personality out of the text." Substitution table provides meaning-equivalent replacements.
- [x] PASS: Rewrites follow the skill's substitution table. leverage→use, comprehensive→complete/thorough/full, facilitate→help/enable, robust→strong/reliable/solid, utilize→use are all mapped directly.
- [x] PASS: At least one rewrite turns a passive construction into an active-voice sentence with an explicit subject. "the request payload is validated by the middleware layer" → "The middleware layer validates the request payload."
- [x] PASS: Output produces a Summary block with numeric counts for all five categories. The Output Format specifies all five count lines by name.
- [x] PASS: Findings include specific quote anchors. The "Original text" column holds the exact quoted text from the source.
- [x] PASS: Output does not introduce any new banned words in its own rewrites or commentary. The substitution table and core principles apply to all text the skill produces.
- [~] PARTIAL: Output groups findings by step rather than mixing randomly. The skill defines three distinct mandatory steps each with an "Output:" instruction, but the Output Format collapses everything into one undivided findings table with no grouping sub-headings. Findings in the simulated output are ordered by source position, not step — conforming responses will likely vary.
- [~] PARTIAL: Output flags the API-documentation context and notes whether rewritten version meets Step 5 rules. Step 5 is mandatory and covers API docs ("Start with what the endpoint does"), and "Context-specific: [count]" appears in the Summary. However the Output Format provides no dedicated block for a context-type declaration or a pass/fail verdict on context rules — the context finding (missing parameters, example request/response) appears only as a count and note, not a structured verdict.

## Notes

The skill is well-constructed. The substitution table covers every banned word in the prompt directly, and the Output Format template is specific enough that a conforming response would satisfy most criteria.

Two genuine gaps: the Output Format collapses all findings into a single table with no step grouping, so there is no structural guarantee that banned-word findings appear before structure findings before formatting findings. And Step 5 (context-specific rules) produces findings that land in the same table as everything else, with "Context-specific: [count]" in the Summary as the only marker — there is no block that explicitly identifies the content type and delivers a context verdict.

One minor tension: each step ends with its own "Output:" instruction that implies step-level output, but the Output Format assumes a single consolidated pass. A reviewer following step instructions literally would produce four intermediate outputs before rolling up; one following the template would produce one output. This ambiguity could produce inconsistent structure across invocations.

The `comprehensive` and `paradigm` violations share their rewrite row in row 1, which is a minor presentation quirk — the skill does not prohibit this but also does not endorse combined rows.
