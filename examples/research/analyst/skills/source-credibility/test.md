# Test: source-credibility skill

Scenario: A journalist wants to assess whether the Australian Strategic Policy Institute (ASPI) is a reliable source to cite in a piece on defence procurement.

## Prompt

/analyst:source-credibility Australian Strategic Policy Institute (ASPI)

## Criteria

- [ ] PASS: Skill identifies the source type (think tank / research organisation) and applies the appropriate credibility framework
- [ ] PASS: Ownership and funding section covers who funds ASPI, transparency of disclosure, and any implications for systematic bias
- [ ] PASS: Editorial standards section assesses whether ASPI has a corrections policy, peer review, and named accountable authors
- [ ] PASS: Track record section draws on specific examples (corrections, retractions, or a strong reliability record) — not a generic statement
- [ ] PASS: Declared mission vs output pattern is assessed — does ASPI's stated purpose match what it publishes?
- [ ] PASS: Credibility assessment table is produced with ratings across ownership transparency, editorial accountability, accuracy track record, and bias transparency
- [ ] PASS: Output distinguishes between bias (systematic pattern) and error (specific inaccuracy) — treats them as separate dimensions
- [ ] PASS: "Appropriate use" section states what ASPI is and isn't reliable for — credibility is not treated as binary
- [ ] PASS: Skill does not assess whether ASPI's conclusions are correct — only whether the source is credible
