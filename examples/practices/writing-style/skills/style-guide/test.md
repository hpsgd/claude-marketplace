# Test: style-guide review of documentation with multiple violations

Scenario: A developer asks for a style review of a newly written API documentation section before publishing. The text contains banned words, passive voice, overly long sentences, and missing Oxford commas.

## Prompt

/style-guide Review this API documentation section: "The endpoint leverages a comprehensive authentication paradigm that facilitates robust access control. It's important to note that the request payload is validated by the middleware layer prior to being processed. Tokens are utilized to ensure that only authorized, authenticated and verified users can access the endpoint. Moving forward, we will be adding support for OAuth 2.0, SAML and API key authentication mechanisms."

## Criteria

- [ ] PASS: Step 2 identifies all banned words present — leverage, comprehensive, paradigm, facilitates, robust, utilized — each flagged with the exact occurrence
- [ ] PASS: Each banned word finding includes the exact original text and a specific rewrite, not just identification
- [ ] PASS: "It's important to note that" is flagged as a banned phrase and removed in the rewrite
- [ ] PASS: Passive voice constructions ("is validated by", "are utilized") are identified in Step 3 and rewritten to active voice
- [ ] PASS: "Moving forward" is flagged as a banned phrase with a suggested rewrite ("From [date]," or "Next,")
- [ ] PASS: Missing Oxford commas ("authorized, authenticated and verified", "OAuth 2.0, SAML and API key") are flagged in Step 4
- [ ] PASS: Output uses the defined findings table format with rule violated, original text, and specific rewrite for each finding
- [ ] PARTIAL: Overall assessment states whether the text is ready to publish or needs a revision pass — not left implicit

## Output expectations

- [ ] PASS: Output begins with a "## Style Review:" heading naming what was reviewed (the API documentation snippet), not generic prose
- [ ] PASS: Output's findings table uses exactly four columns in order: number, rule violated, original text, rewrite — matching the format defined in the skill
- [ ] PASS: Each rewrite preserves the technical meaning of the original (authentication, validation, token use, future protocol support) without inventing new requirements
- [ ] PASS: Rewrites for banned-word substitutions follow the skill's substitution table (leverage→use, comprehensive→complete/thorough/full, facilitate→help/enable, robust→strong/reliable/solid, utilized→used)
- [ ] PASS: At least one rewrite turns a passive construction into a clear active-voice sentence with an explicit subject (e.g., "the middleware validates the request payload")
- [ ] PASS: Output produces a Summary block with numeric counts for total findings, banned words, structure issues, formatting issues, and context-specific issues — counts are consistent with the findings table
- [ ] PASS: Findings include specific line/quote anchors (the exact original text in quotes) so a reader can locate each issue in the source without re-reading the whole snippet
- [ ] PASS: Output does not introduce any new banned words from the skill's hard-stop list in its own rewrites or commentary
- [ ] PARTIAL: Output groups or orders findings by step (Step 2 banned words, Step 3 structure, Step 4 formatting) rather than mixing them randomly
- [ ] PARTIAL: Output flags the API-documentation context (this is API docs) and notes whether the rewritten version meets the README/API doc context-specific rules from Step 5
