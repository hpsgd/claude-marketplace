# Output: company-lookup skill

**Verdict:** FAIL
**Score:** 11.5/18 criteria met (64%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill defines a clear trigger or usage context — met: frontmatter description and `user-invocable: true` with `argument-hint` make usage context explicit
- [x] PASS: Skill specifies what sources to check — met: Step 1 maps sources by jurisdiction/listing (ASIC, ABN Lookup, NZ Companies Office, SEC EDGAR, Companies House, Crunchbase, LinkedIn); Steps 2-5 name specific sources per research area
- [x] PASS: Skill defines an output structure with named sections — met: output format template defines seven named sections
- [x] PASS: Output structure includes business model or "what they do" section — met: Overview table has explicit "Business model" and "Revenue model" rows; Step 2 captures business model
- [x] PASS: Output structure includes financials or funding section — met: "Financials" is a named section; Step 4 specifies revenue/growth/funding data with mandatory source and date
- [x] PASS: Output structure includes recent news or developments section — met: "Recent news" is a named section; Step 5 defines search method and priority topics
- [~] PARTIAL: Skill includes guidance on assessing source credibility or recency — partially met: 18-month staleness flag and mandatory two-source cross-reference are present; recency handled well. Explicit source authority ranking (primary registry vs press) is absent. Score: 0.5
- [-] SKIP: Skill references collaboration with other agents — skipped: standalone skill definition with no agent routing logic

### Output expectations

- [ ] FAIL: Output covers Palantir Technologies specifically — not met: the skill is a structural definition with placeholder templates, not a live execution. No Palantir-specific content is produced by the definition itself.
- [ ] FAIL: Output's "What they do" section names Gotham, Foundry, and AIP — not met: skill contains no Palantir-specific product content
- [ ] FAIL: Output's business model section explains government vs commercial split, contract structures, AI push — not met: skill contains no Palantir-specific content
- [ ] FAIL: Output's financials section includes recent quarterly revenue with source date — not met: skill contains no Palantir-specific financial data
- [ ] FAIL: Output's recent news covers last 6-12 months of Palantir developments — not met: skill contains no Palantir-specific news
- [ ] FAIL: Output cites specific sources per claim — not met: template shows source format but produces no Palantir-specific citations
- [ ] FAIL: Output addresses Palantir's controversies (surveillance, immigration, military contracts) — not met: the skill has no controversy or reputational risk step. The definition would not instruct the model to surface this material.
- [x] PASS: Output's structure has named sections — met: template defines Overview, Products/services, Team, Financials, Recent news, Strategic direction, Sources
- [ ] FAIL: Output flags any source >12 months old as potentially stale — not met: the skill's Rules flag sources older than 18 months, not 12 months. The criterion requires a 12-month threshold; the skill uses a looser 18-month threshold.
- [~] PARTIAL: Output addresses meeting-prep angles — partially met: "Strategic direction" covers executive statements and job posting signals that could inform meeting prep, but there is no explicit instruction to surface likely conversation topics or meeting-framing angles. Score: 0.5

## Notes

The Criteria section (structural) passes cleanly at 6.5/7. The skill is well-structured with typed source routing, output sections, and sourcing rules.

The failure is concentrated entirely in the Output expectations section. Seven of the ten output criteria require company-specific populated content that a skill definition cannot supply — only a live execution can. Those criteria are effectively unevaluable against a SKILL.md and would only be measurable against an agent run.

Two structural gaps are genuine and affect meeting-prep fitness: (1) no controversy or reputational-risk step — the skill would not instruct the model to surface Palantir's surveillance/military record; (2) the recency threshold is 18 months vs the 12 months the test requires, a real mismatch for fast-moving public companies.
