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

## Output expectations

- [ ] PASS: Output's scope at the top is explicit — investment-consideration diligence, public data only, with the caveat that Theranos has been the subject of extensive published reporting (WSJ Carreyrou, books, court cases) so the public record is unusually deep
- [ ] PASS: Output's business fundamentals section flags the gap between Theranos's claims (revolutionary blood testing from finger-prick) and the independent verification record (no peer-reviewed validation, regulatory inspections finding the technology did not work as claimed)
- [ ] PASS: Output's team section notes the executive departures and governance concerns — board composition (high-profile but technology-naive members like Kissinger / Mattis / Shultz), CEO/founder removal, COO Sunny Balwani charged
- [ ] PASS: Output's signal summary lists multiple RED signals — gap between claims and evidence (red), legal action (red — SEC charges and criminal trial), executive criminal liability (red — Holmes and Balwani both convicted), governance concerns (red — board lacked technical expertise)
- [ ] PASS: Output's verdict is DO NOT PROCEED (or DECLINE) — red signals are decisive; positive signals (high valuation, prestigious investors) do NOT override the substantive concerns
- [ ] PASS: Output routes to follow-on skills — `/investigator:public-records` for court filings (the SEC complaint, criminal trial transcripts), `/investigator:corporate-ownership` for the entity structure / disposition
- [ ] PASS: Output distinguishes "information unavailable" (e.g. private investor return data) from "information contradicts claims" (e.g. WSJ reporting and lab inspection results contradict the technology claims) — both are findings but they're qualitatively different
- [ ] PASS: Output flags Theranos's revenue and technology claims as UNVERIFIABLE FROM PUBLIC DATA — and notes that the independent verification that DID happen contradicted the claims; this is a CONTRADICTED state, not just unverified
- [ ] PASS: Output uses Theranos as a case where "do not proceed" is unambiguous — the skill demonstrates it can recognise a clear red verdict, not equivocate
- [ ] PARTIAL: Output addresses the timing — when this diligence might have run (pre-Carreyrou-WSJ, post-WSJ, post-trial); the public record changed dramatically over time and that affects the diligence trajectory
