# Style guide review of documentation with multiple violations

A developer asks for a style review of a newly written API documentation section before publishing. The text contains banned words, passive voice, overly long sentences, and missing Oxford commas.

## Prompt

> /style-guide Review this API documentation section: "The endpoint leverages a comprehensive authentication paradigm that facilitates robust access control. It's important to note that the request payload is validated by the middleware layer prior to being processed. Tokens are utilized to ensure that only authorized, authenticated and verified users can access the endpoint. Moving forward, we will be adding support for OAuth 2.0, SAML and API key authentication mechanisms."

```markdown

## Output

### Style Review: API documentation section

#### Step 1: Core principles check

Text opens with abstract corporate language, contains passive constructions in two sentences, and includes two temporal filler phrases. Proceeding to systematic scan.

#### Step 2: Banned words and phrases scan

**Banned words found:** `leverages`, `comprehensive`, `paradigm`, `facilitates`, `robust`, `utilized`, `prior to`

**Banned phrases found:** "It's important to note that", "Moving forward"

#### Step 3: Sentence structure check

**Passive voice:** "is validated by the middleware layer", "Tokens are utilized"

#### Step 4: Punctuation and formatting

**Missing Oxford commas:** "authorized, authenticated and verified" (missing before "and"), "OAuth 2.0, SAML and API key" (missing before "and")

---

### Style Review: API documentation — authentication endpoint

#### Findings

| # | Rule violated | Original text | Rewrite |
|---|---|---|---|
| 1 | Banned word: `leverages` | "The endpoint leverages a comprehensive authentication paradigm" | "The endpoint uses a full authentication model" |
| 2 | Banned word: `comprehensive` | "a comprehensive authentication paradigm" | "a full authentication model" (combined with #1) |
| 3 | Banned word: `paradigm` | "a comprehensive authentication paradigm" | "a full authentication model" (combined with #1–2) |
| 4 | Banned word: `facilitates` | "that facilitates robust access control" | "that controls access" |
| 5 | Banned word: `robust` | "facilitates robust access control" | "controls access" (combined with #4) |
| 6 | Banned phrase: "It's important to note that" | "It's important to note that the request payload is validated by the middleware layer prior to being processed." | "The middleware validates the request payload before processing." |
| 7 | Passive voice: "is validated by" | "the request payload is validated by the middleware layer prior to being processed" | "The middleware validates the request payload before processing" |
| 8 | Banned word: `prior to` | "prior to being processed" | "before processing" |
| 9 | Banned word: `utilized` | "Tokens are utilized to ensure" | "Tokens ensure" |
| 10 | Passive voice: "are utilized" | "Tokens are utilized to ensure that only..." | "Tokens ensure that only authorized..." |
| 11 | Banned phrase: "Moving forward" | "Moving forward, we will be adding support for OAuth 2.0, SAML and API key authentication mechanisms." | "We're adding support for OAuth 2.0, SAML, and API key authentication." |
| 12 | Oxford comma missing | "authorized, authenticated and verified users" | "authorized, authenticated, and verified users" |
| 13 | Oxford comma missing | "OAuth 2.0, SAML and API key authentication mechanisms" | "OAuth 2.0, SAML, and API key authentication" |

#### Rewritten text

> The endpoint uses a full authentication model that controls access. The middleware validates the request payload before processing. Tokens ensure that only authorized, authenticated, and verified users can access the endpoint. We're adding support for OAuth 2.0, SAML, and API key authentication.

#### Summary
- Total findings: 13
- Banned words: 7 (`leverages`, `comprehensive`, `paradigm`, `facilitates`, `robust`, `utilized`, `prior to`)
- Structure issues: 2 (passive voice)
- Formatting issues: 2 (Oxford comma)
- Banned phrases: 2 ("It's important to note that", "Moving forward")
- Context-specific: 0

#### Overall assessment

This text is not ready to publish. Every sentence contains at least one violation. Use the rewritten version above.
```

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/7.5 (100%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Step 2 identifies all banned words — the skill's word substitutions table lists `leverage → use`, `comprehensive → complete, thorough, full`, `paradigm → model, approach`, `facilitate → help, enable`, `robust → strong, reliable, solid`, and `utilize → use`. The banned words hard stops section also lists additional items. The simulation flags `leverages`, `comprehensive`, `paradigm`, `facilitates`, `robust`, `utilized`, and `prior to`, each quoted from the source text.
- [x] PASS: Each finding includes exact original text and specific rewrite — the skill's Rules section states "Every finding needs the exact text, the violated rule, and a specific rewrite. No exceptions." The findings table uses three columns (Rule violated, Original text, Rewrite) with quoted source text and concrete replacement text for every finding including combined findings.
- [x] PASS: "It's important to note that" flagged and removed — the skill's Banned phrases section lists "'It's important to note' / 'It's worth mentioning' — just state the fact." Finding 6 flags the exact phrase and rewrites the sentence as a direct statement.
- [x] PASS: Passive voice identified in Step 3 and rewritten to active — the skill's Step 3 table defines "Active voice: Subject performs the action" with wrong/right examples. Findings 7 and 10 identify "is validated by the middleware layer" and "Tokens are utilized" as passive constructions and rewrite both to active voice ("The middleware validates..." and "Tokens ensure...").
- [x] PASS: "Moving forward" flagged as banned phrase — the skill's word substitutions table includes `going forward / moving forward → from now on, next`. Finding 11 flags the exact phrase and rewrites to "We're adding support for..." with temporal filler removed.
- [x] PASS: Missing Oxford commas flagged in Step 4 — the skill's Step 4 table defines "Oxford comma: Always — 'Red, white, and blue' not 'Red, white and blue'." Findings 12 and 13 flag both missing commas in "authorized, authenticated and verified" and "OAuth 2.0, SAML and API key" with corrected versions.
- [x] PASS: Output uses defined findings table format — the skill's Output Format section specifies `| # | Rule violated | Original text | Rewrite |`. All 13 findings in the simulation follow this exact column structure.
- [~] PARTIAL: Overall assessment states readiness to publish — the skill's Output Format specifies "Overall assessment: [One sentence: is the text ready to publish, or does it need a revision pass?]." The simulation states "This text is not ready to publish. Every sentence contains at least one violation." This directly answers the required question. PARTIAL ceiling applies regardless — the test author set this ceiling deliberately.

### Notes

The skill's word substitutions table is the core execution mechanism: it is specific enough that the list of violations in the test prompt maps directly to the table. The `prior to` entry in the substitutions table (`prior to → before`) and `going forward / moving forward → from now on, next` both cover test-case violations directly. The banned phrase "It's important to note" is in the Banned phrases section. The passive voice check is in Step 3. The Oxford comma is in Step 4. This skill is well-designed for deterministic mechanical text review: the substitutions table and banned phrases list leave little room for evaluator judgment on whether something should be flagged.
