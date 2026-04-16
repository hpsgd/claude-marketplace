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
