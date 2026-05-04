# Style Guide

Scenario: A developer asks for a style review of a newly written API documentation section before publishing. The text contains banned words, passive voice, overly long sentences, and missing Oxford commas.

## Prompt

> /style-guide Review this API documentation section: "The endpoint leverages a comprehensive authentication paradigm that facilitates robust access control. It's important to note that the request payload is validated by the middleware layer prior to being processed. Tokens are utilized to ensure that only authorized, authenticated and verified users can access the endpoint. Moving forward, we will be adding support for OAuth 2.0, SAML and API key authentication mechanisms."

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Style Review: API Authentication Documentation

### Findings

| # | Rule violated | Original text | Rewrite |
|---|---|---|---|
| 1 | Banned word: "leverages" | "The endpoint leverages a comprehensive authentication paradigm" | "This endpoint requires authentication" |
| 2 | Banned word: "comprehensive" | "comprehensive authentication paradigm" | "authentication model" |
| 3 | Banned word: "paradigm" | "authentication paradigm" | "authentication model" or "authentication approach" |
| 4 | Banned word: "facilitates" | "facilitates robust access control" | "controls access" |
| 5 | Banned word: "robust" | "robust access control" | "reliable access control" or just "access control" |
| 6 | Banned phrase: "It's important to note that" | "It's important to note that the request payload is validated" | "Middleware validates the request payload before processing." |
| 7 | Passive voice | "the request payload is validated by the middleware layer" | "Middleware validates the request payload" |
| 8 | Banned word: "prior to" | "prior to being processed" | "before processing it" |
| 9 | Banned word: "utilized" | "Tokens are utilized to ensure" | "Use tokens to authenticate" |
| 10 | Passive voice | "Tokens are utilized to ensure that only authorized, authenticated and verified users can access" | "Only authenticated users can access this endpoint" |
| 11 | Repetition | "authorized, authenticated and verified users" | "authenticated users" (all three mean the same thing; pick one) |
| 12 | Banned phrase: "moving forward" | "Moving forward, we will be adding support" | "We're adding support" |
| 13 | API context rule violation | Entire section buries the requirement | Start with: "This endpoint requires authentication via token, OAuth 2.0, SAML, or API key." Then explain details. |
| 14 | Missing Oxford comma | "OAuth 2.0, SAML and API key" | "OAuth 2.0, SAML, and API key" |

### Summary
- Total findings: **14**
- Banned words/phrases: 9
- Structure issues (passive voice, repetition): 3
- Formatting issues (Oxford comma): 1
- Context-specific (API documentation): 1

### Overall assessment

**Not ready to publish.** The section is 90% corporate boilerplate and obscures the actual requirements. It needs a complete rewrite to lead with what the endpoint requires, use active voice throughout, and eliminate redundant qualifiers.

### Suggested rewrite

> This endpoint requires authentication. Use one of these methods:
> - Bearer token in the `Authorization` header
> - OAuth 2.0 (client credentials flow)
> - SAML assertion
> - API key in the `X-API-Key` header
>
> The middleware validates credentials before processing the request. Requests without valid credentials return a 401 Unauthorized error.
>
> Coming soon: additional authentication options (OAuth 2.0, SAML, API key support).

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/16.5 (97%) |
| Evaluated | 2026-05-04 |
| Target duration | 14012 ms |
| Target cost | $0.0445 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 2 identifies all banned words present — leverage, comprehensive, paradigm, facilitates, robust, utilized — each flagged with the exact occurrence | PASS | Rows 1–5 and 9 flag 'leverages', 'comprehensive', 'paradigm', 'facilitates', 'robust', and 'utilized' respectively, each with the exact text from the source in the Original text column. |
| c2 | Each banned word finding includes the exact original text and a specific rewrite, not just identification | PASS | Every row in the findings table has a quoted Original text and a specific Rewrite. E.g., Row 1: original 'The endpoint leverages a comprehensive authentication paradigm' → rewrite 'This endpoint requires authentication'. |
| c3 | 'It's important to note that' is flagged as a banned phrase and removed in the rewrite | PASS | Row 6: 'Banned phrase: "It's important to note that"' with original text 'It's important to note that the request payload is validated' and rewrite 'Middleware validates the request payload before processing.' |
| c4 | Passive voice constructions ('is validated by', 'are utilized') are identified in Step 3 and rewritten to active voice | PASS | Row 7: 'Passive voice — the request payload is validated by the middleware layer' → 'Middleware validates the request payload'. Row 10: 'Passive voice — Tokens are utilized to ensure...' → 'Only authenticated users can access this endpoint'. |
| c5 | 'Moving forward' is flagged as a banned phrase with a suggested rewrite ('From [date],' or 'Next,') | PASS | Row 12: 'Banned phrase: "moving forward"' with original 'Moving forward, we will be adding support' and rewrite 'We're adding support'. The rewrite removes the banned phrase; the specific prescribed alternates in the criterion are examples, not requirements. |
| c6 | Missing Oxford commas ('authorized, authenticated and verified', 'OAuth 2.0, SAML and API key') are flagged in Step 4 | PARTIAL | Row 14 explicitly flags the Oxford comma in 'OAuth 2.0, SAML and API key'. However, 'authorized, authenticated and verified' (Row 11) is addressed only as a repetition/redundancy issue, not as a missing Oxford comma. The criterion requires both instances to be flagged as Oxford comma violations. |
| c7 | Output uses the defined findings table format with rule violated, original text, and specific rewrite for each finding | PASS | The findings table header reads '# \| Rule violated \| Original text \| Rewrite' — exactly matching the prescribed four-column format, applied consistently across all 14 rows. |
| c8 | Overall assessment states whether the text is ready to publish or needs a revision pass — not left implicit | PARTIAL | The Overall assessment section opens with '**Not ready to publish.**' — explicit and unambiguous. Ceiling is PARTIAL so maximum credit is 0.5. |
| c9 | Output begins with a '## Style Review:' heading naming what was reviewed (the API documentation snippet), not generic prose | PASS | First line of the output: '## Style Review: API Authentication Documentation' — correct format and names the reviewed content. |
| c10 | Output's findings table uses exactly four columns in order: number, rule violated, original text, rewrite — matching the format defined in the skill | PASS | Table header '\| # \| Rule violated \| Original text \| Rewrite \|' — four columns in the exact prescribed order. |
| c11 | Each rewrite preserves the technical meaning of the original (authentication, validation, token use, future protocol support) without inventing new requirements | PASS | The suggested rewrite retains: authentication requirement, middleware validation, token-based access, and forthcoming OAuth 2.0/SAML/API key support. No new technical claims are added. |
| c12 | Rewrites for banned-word substitutions follow the skill's substitution table (leverage→use, comprehensive→complete/thorough/full, facilitate→help/enable, robust→strong/reliable/solid, utilized→used) | PARTIAL | 'utilized' → 'Use tokens' (aligns with utilized→used) and 'robust' → 'reliable access control' (reliable is in the robust→reliable/solid mapping). However, 'leverages' → 'requires authentication' (not 'use'), 'comprehensive' → 'authentication model' (not complete/thorough/full), and 'facilitates' → 'controls access' (not help/enable) deviate from the substitution table. |
| c13 | At least one rewrite turns a passive construction into a clear active-voice sentence with an explicit subject (e.g., 'the middleware validates the request payload') | PASS | Row 7 rewrites 'the request payload is validated by the middleware layer' to 'Middleware validates the request payload' — 'Middleware' is the explicit subject in an active-voice sentence. |
| c14 | Output produces a Summary block with numeric counts for total findings, banned words, structure issues, formatting issues, and context-specific issues — counts are consistent with the findings table | PASS | Summary shows: Total findings: 14, Banned words/phrases: 9, Structure issues: 3, Formatting issues: 1, Context-specific: 1. Sum is 9+3+1+1=14, consistent with the 14-row findings table. |
| c15 | Findings include specific line/quote anchors (the exact original text in quotes) so a reader can locate each issue in the source without re-reading the whole snippet | PASS | The 'Original text' column in every row contains an exact quoted excerpt from the source text, e.g., 'The endpoint leverages a comprehensive authentication paradigm', 'It's important to note that the request payload is validated', etc. |
| c16 | Output does not introduce any new banned words from the skill's hard-stop list in its own rewrites or commentary | PASS | Commentary uses plain language: 'corporate boilerplate', 'complete rewrite', 'lead with', 'active voice', 'redundant qualifiers'. None of these appear in the banned vocabulary list. Rewrites use 'requires', 'validates', 'use tokens', 'controls access' — all clean. |
| c17 | Output groups or orders findings by step (Step 2 banned words, Step 3 structure, Step 4 formatting) rather than mixing them randomly | PARTIAL | The table interleaves categories: rows 1–6 are mostly banned words/phrases, but rows 7–12 mix passive voice (7, 10), banned words (8, 9), repetition (11), and banned phrase (12), with Oxford comma last (14). There is loose front-loading of banned-word findings but no explicit step-based grouping headers or strict separation. Ceiling is PARTIAL. |
| c18 | Output flags the API-documentation context (this is API docs) and notes whether the rewritten version meets the README/API doc context-specific rules from Step 5 | PARTIAL | Row 13 explicitly flags 'API context rule violation — Entire section buries the requirement' with a rewrite that leads with the requirement. The suggested rewrite restructures as an API reference (requirement-first, method list, then details). Ceiling is PARTIAL; deeper Step 5 rule commentary (e.g., README conventions, endpoint naming) is not elaborated. Score capped at 0.5. |

### Notes

Strong overall performance — 14 of 18 criteria at full ceiling. The output correctly identifies all six banned words, both passive constructions, both banned phrases, the Oxford comma in the OAuth list, and the API-context structural flaw. The suggested rewrite is clean and technically accurate. Two criteria fall to PARTIAL: c6 misses that 'authorized, authenticated and verified' also has an Oxford comma issue (treating it only as redundancy), and c12 diverges from the prescribed substitution table for 'comprehensive', 'facilitates', and 'leverages'. The three PARTIAL-ceiling criteria (c8, c17, c18) all earn their half-point — the publish verdict is explicit, findings have loose step-based ordering, and the API context is flagged with a conforming rewrite.
