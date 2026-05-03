# Style Guide

Scenario: A developer asks for a style review of a newly written API documentation section before publishing. The text contains banned words, passive voice, overly long sentences, and missing Oxford commas.

## Prompt

> /style-guide Review this API documentation section: "The endpoint leverages a comprehensive authentication paradigm that facilitates robust access control. It's important to note that the request payload is validated by the middleware layer prior to being processed. Tokens are utilized to ensure that only authorized, authenticated and verified users can access the endpoint. Moving forward, we will be adding support for OAuth 2.0, SAML and API key authentication mechanisms."

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Style Review: API documentation section

### Findings

| # | Rule violated | Original text | Rewrite |
|---|---|---|---|
| 1 | Banned word: `leverage` | "The endpoint leverages" | "The endpoint uses" |
| 2 | Banned word: `comprehensive` | "a comprehensive authentication paradigm" | "an authentication model" |
| 3 | Banned word: `paradigm` | "authentication paradigm" | "authentication model" |
| 4 | Banned word: `facilitate` | "that facilitates robust access control" | "for access control" |
| 5 | Banned word: `robust` | "robust access control" | "reliable access control" (or just "access control") |
| 6 | Banned phrase: "It's important to note" | "It's important to note that the request payload..." | Cut the preamble: "The middleware validates the request payload before processing it." |
| 7 | Banned word: `utilize` | "Tokens are utilized" | "Tokens verify" |
| 8 | Passive voice | "the request payload is validated by the middleware layer" | "The middleware validates the request payload" |
| 9 | Redundant list | "authorized, authenticated and verified users" | "authenticated users" — these three words mean the same thing |
| 10 | Banned phrase: "Moving forward" | "Moving forward, we will be adding" | "OAuth 2.0, SAML, and API key authentication are planned." |
| 11 | Missing Oxford comma | "OAuth 2.0, SAML and API key" | "OAuth 2.0, SAML, and API key" |
| 12 | Context-specific (API docs) | Entire section | Missing: what the endpoint actually does, parameter names/types, example request/response |

**Proposed rewrite:**

> This endpoint authenticates requests using token-based access control. The middleware validates the request payload before processing. Only authenticated users can access it.
>
> OAuth 2.0, SAML, and API key authentication are planned.

---

### Summary
- **Total findings:** 12
- **Banned words:** 5 (`leverage`, `comprehensive`, `paradigm`, `facilitate`, `robust`, `utilize`)
- **Structure issues:** 3 (passive voice, redundant list, "Moving forward")
- **Formatting issues:** 1 (missing Oxford comma)
- **Context-specific:** 1 (API docs missing required elements)

### Overall assessment
Needs a revision pass — dense with banned words and passive voice, and missing the structural elements required for API documentation (parameters, example request/response).

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/16.5 (88%) |
| Evaluated | 2026-05-01 |
| Target duration | 9977 ms |
| Target cost | $0.0525 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 2 identifies all banned words present — leverage, comprehensive, paradigm, facilitates, robust, utilized — each flagged with the exact occurrence | PASS | Rows 1–5 and 7 in the findings table explicitly flag leverage, comprehensive, paradigm, facilitate, robust, and utilize (as 'Banned word: leverage', 'Banned word: comprehensive', etc.) with exact occurrences quoted. |
| c2 | Each banned word finding includes the exact original text and a specific rewrite, not just identification | PASS | All six banned-word rows include an 'Original text' column with exact quoted phrases and a 'Rewrite' column with specific substitutions (e.g., 'The endpoint leverages' → 'The endpoint uses'). |
| c3 | "It's important to note that" is flagged as a banned phrase and removed in the rewrite | PASS | Row 6: rule 'Banned phrase: "It's important to note"', original text quoted in full, rewrite: 'Cut the preamble: "The middleware validates the request payload before processing it."' |
| c4 | Passive voice constructions ("is validated by", "are utilized") are identified in Step 3 and rewritten to active voice | PASS | Row 8 explicitly labels 'Passive voice' and rewrites 'the request payload is validated by the middleware layer' → 'The middleware validates the request payload'. Row 7 identifies 'Tokens are utilized' as a banned-word issue and rewrites to active 'Tokens verify'. Both passive constructions end up rewritten to active voice. |
| c5 | "Moving forward" is flagged as a banned phrase with a suggested rewrite ("From [date]," or "Next,") | PARTIAL | Row 10 correctly flags 'Banned phrase: "Moving forward"'. However the rewrite is 'OAuth 2.0, SAML, and API key authentication are planned.' — it does not use the prescribed substitutions 'From [date],' or 'Next,'; instead it restructures the sentence entirely. |
| c6 | Missing Oxford commas ("authorized, authenticated and verified", "OAuth 2.0, SAML and API key") are flagged in Step 4 | PARTIAL | Row 11 explicitly flags the Oxford comma in 'OAuth 2.0, SAML and API key'. However 'authorized, authenticated and verified' is addressed only as 'Redundant list' in row 9 (collapsed to 'authenticated users'), not explicitly flagged as a missing Oxford comma. |
| c7 | Output uses the defined findings table format with rule violated, original text, and specific rewrite for each finding | PASS | Table header is '\| # \| Rule violated \| Original text \| Rewrite \|' with all 12 rows populated across all four columns. |
| c8 | Overall assessment states whether the text is ready to publish or needs a revision pass — not left implicit | PARTIAL | '### Overall assessment' section explicitly states 'Needs a revision pass — dense with banned words and passive voice, and missing the structural elements required for API documentation.' |
| c9 | Output begins with a "## Style Review:" heading naming what was reviewed (the API documentation snippet), not generic prose | PASS | Opening heading is '## Style Review: API documentation section' — matches the required format exactly. |
| c10 | Output's findings table uses exactly four columns in order: number, rule violated, original text, rewrite — matching the format defined in the skill | PASS | Table header '\| # \| Rule violated \| Original text \| Rewrite \|' is exactly four columns in the specified order. |
| c11 | Each rewrite preserves the technical meaning of the original (authentication, validation, token use, future protocol support) without inventing new requirements | PASS | Proposed rewrite retains: token-based auth, middleware validation, access restriction to authenticated users, and planned OAuth 2.0/SAML/API key support. No new technical requirements introduced. |
| c12 | Rewrites for banned-word substitutions follow the skill's substitution table (leverage→use, comprehensive→complete/thorough/full, facilitate→help/enable, robust→strong/reliable/solid, utilized→used) | PARTIAL | leverage→'uses' ✓; robust→'reliable' ✓; but comprehensive→'an authentication model' (not complete/thorough/full); facilitate→removed entirely ('for access control', not help/enable); utilized→'verify' (not 'used'). Three of five substitutions deviate from the prescribed table. |
| c13 | At least one rewrite turns a passive construction into a clear active-voice sentence with an explicit subject (e.g., "the middleware validates the request payload") | PASS | Row 8 rewrite: 'The middleware validates the request payload' — explicit subject 'The middleware', active verb 'validates'. |
| c14 | Output produces a Summary block with numeric counts for total findings, banned words, structure issues, formatting issues, and context-specific issues — counts are consistent with the findings table | PARTIAL | Summary block exists with all required categories. However counts are inconsistent: 'Banned words: 5' but six words are listed in parentheses and six rows cover banned words in the table; category subtotals (5+3+1+1=10) do not sum to the stated total of 12. |
| c15 | Findings include specific line/quote anchors (the exact original text in quotes) so a reader can locate each issue in the source without re-reading the whole snippet | PASS | Every row in the 'Original text' column contains an exact verbatim quote from the source (e.g., '"The endpoint leverages"', '"that facilitates robust access control"', '"OAuth 2.0, SAML and API key"'). |
| c16 | Output does not introduce any new banned words from the skill's hard-stop list in its own rewrites or commentary | PASS | Rewrites and proposed rewrite block use plain language: 'uses', 'authentication model', 'validates', 'reliable access control', 'authenticated users', 'are planned'. No banned words (leverage, utilize, paradigm, facilitate, robust, comprehensive, etc.) appear in the output's own prose. |
| c17 | Output groups or orders findings by step (Step 2 banned words, Step 3 structure, Step 4 formatting) rather than mixing them randomly | PARTIAL | Findings are in a single flat table with no explicit step grouping or section headers separating banned words, structure, and formatting. There is rough ordering (banned words/phrases at rows 1–7, passive at 8, structure at 9–10, formatting at 11, context at 12) but no explicit step labels or group headings. |
| c18 | Output flags the API-documentation context (this is API docs) and notes whether the rewritten version meets the README/API doc context-specific rules from Step 5 | PARTIAL | Row 12 labels 'Context-specific (API docs)' and lists missing elements: 'what the endpoint actually does, parameter names/types, example request/response'. This flags the context and identifies gaps against API doc standards. |

### Notes

The output is a strong style review that correctly identifies all six banned words, the two banned phrases, passive voice, Oxford comma, and API-doc context gaps in a well-formatted four-column table. Its main weaknesses are: (1) three banned-word substitutions deviate from the prescribed substitution table (comprehensive, facilitate, utilize); (2) 'Moving forward' is correctly flagged but the prescribed replacement pattern ('From [date],' or 'Next,') is not used; (3) only one of the two Oxford-comma instances is explicitly labeled as such; (4) the Summary block has an arithmetic inconsistency (5 banned words listed but 6 enumerated, subtotals don't sum to total 12); and (5) findings are not grouped by skill step. Despite these gaps, coverage is broad and the core deliverables — findings table, proposed rewrite, and overall verdict — are all present and accurate.
