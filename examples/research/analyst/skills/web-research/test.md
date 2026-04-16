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
