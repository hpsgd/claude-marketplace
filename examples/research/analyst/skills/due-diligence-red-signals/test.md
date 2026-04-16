# Test: due-diligence skill with red signals

Scenario: An investor asks for due diligence on a company with well-documented public red flags. The company's claims are contradicted by public reporting, key executives have departed under scrutiny, and independent verification of core technology claims does not exist. The skill should surface red signals and refuse to recommend proceeding.

## Prompt

/analyst:due-diligence Theranos Inc for investment consideration — pre-Series C health tech company claiming revolutionary blood testing technology

## Criteria

- [ ] PASS: Skill states scope explicitly at the top — investment consideration, public data only
- [ ] PASS: Business fundamentals section flags the gap between claims and independently verifiable evidence
- [ ] PASS: Team section notes executive departures or governance concerns from public reporting
- [ ] PASS: Signal summary contains at least two red signals from public sources
- [ ] PASS: When two or more red signals are present, skill routes to follow-on skills (public-records, corporate-ownership)
- [ ] PASS: Verdict does NOT recommend proceeding — red signals override positive indicators
- [ ] PARTIAL: The skill distinguishes between "information unavailable" and "information contradicts claims" in the signal assessment
- [ ] PASS: Revenue and technology claims are flagged as unverifiable from public data when no independent validation exists
