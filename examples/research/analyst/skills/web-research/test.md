# Test: web-research skill

Scenario: A policy analyst needs a structured overview of how other OECD countries have implemented mandatory climate risk disclosure for listed companies.

## Prompt

/analyst:web-research How have OECD countries implemented mandatory climate risk disclosure for listed companies? I need a Standard tier overview — focusing on what's been legislated, what's still voluntary, and where there's significant variation.

## Criteria

- [ ] PASS: Skill selects Standard tier (5-8 sources, structured sections) and does not default to Quick or inflate to Deep
- [ ] PASS: Every source cited has been fetched and read — no citations added without retrieval
- [ ] PASS: Authority hierarchy is applied — regulatory and government sources (SEC, FCA, ASIC, ISSB) take precedence over journalism for legislative facts
- [ ] PASS: Output is organised by theme (what's legislated, what's voluntary, where variation exists), not by "here's what each source said"
- [ ] PASS: Where sources conflict on what's mandatory vs voluntary in a given jurisdiction, the conflict is explained rather than one version chosen arbitrarily
- [ ] PASS: Key uncertainties section is present — covers where evidence is thin or contested
- [ ] PARTIAL: For AU/NZ dimensions of the question, AU/NZ sources (ASIC, APRA, Treasury) are used first before US/UK equivalents
- [ ] PASS: Sources section lists each source with its URL and what it contributed

## Output expectations

- [ ] PASS: Output uses Standard tier — 5-8 sources fetched and read, structured sections, moderate depth — NOT inflated to Deep with extensive primary-source verification, NOT collapsed to Quick with 2-3 sources
- [ ] PASS: Output addresses MULTIPLE OECD jurisdictions named with specific implementations — at minimum EU (CSRD), UK (TCFD-aligned mandatory disclosure for listed companies), Australia (recently legislated AASB S2), New Zealand (XRB CRD), Japan (TCFD-aligned), USA (SEC final rule, status as of date), Canada — covering enough jurisdictions to support the requester's "OECD" scope
- [ ] PASS: Output's authority hierarchy is shown — regulatory body / government source first (SEC, FCA, ASIC, EU Commission, ISSB) for legislative facts, with journalism / industry analysis used only for context, never substituted for the legal text
- [ ] PASS: Output is organised by THEME — what's legislated (with effective dates per jurisdiction), what's still voluntary or proposed, where significant variation exists (scope of disclosure, assurance requirements, materiality framework — TCFD vs ISSB) — not by jurisdiction-by-jurisdiction
- [ ] PASS: Output's variation section names specific differences — e.g. "EU CSRD covers ~50,000 companies + double materiality; SEC rule covers SEC registrants + financial materiality only; AU AASB S2 phases in by company size FY25-FY28" — not abstract "there is variation"
- [ ] PASS: Output handles conflicts between sources — when one source says "mandatory in 2024" and another says "proposed for 2026", the conflict is explained (e.g. different jurisdictions, different scope, source date) rather than picking one arbitrarily
- [ ] PASS: Output's key-uncertainties section addresses — SEC rule litigation status, individual EU member state transposition delays, alignment between jurisdictional rules and the ISSB / IFRS-S baseline
- [ ] PASS: Output addresses AU/NZ dimensions with AU/NZ-specific sources — ASIC, APRA, Treasury announcements, AASB consultation papers — not relying on US-centric reporting
- [ ] PASS: Output's sources section lists every source with its URL, the date accessed, and what specific information that source contributed to which section
- [ ] PARTIAL: Output addresses the timing dimension — most OECD countries have moved from voluntary TCFD-aligned to mandatory in the past 18 months, so the answer is time-sensitive and the access dates matter
