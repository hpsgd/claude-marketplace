# Web research skill

**Scenario:** A policy analyst needs a structured overview of how OECD countries have implemented mandatory climate risk disclosure for listed companies.

> /analyst:web-research How have OECD countries implemented mandatory climate risk disclosure for listed companies? I need a Standard tier overview — focusing on what's been legislated, what's still voluntary, and where there's significant variation.

Routed to `plugins/research/analyst/skills/web-research/SKILL.md` — skill test, structural evaluation only.

## Output

#### Research: Mandatory climate risk disclosure for listed companies — OECD overview

| Field | Value |
|---|---|
| Date | 2026-04-16 |
| Tier | Standard |
| Sources | 7 |

##### What's been legislated

**European Union:** The Corporate Sustainability Reporting Directive (CSRD) requires large listed companies to disclose climate risks against the European Sustainability Reporting Standards (ESRS) from financial year 2024. Source: [EUR-Lex — CSRD text](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022L2464), accessed 2026-04-16.

**United States:** The SEC's climate risk disclosure rule (finalised March 2024) requires disclosure of material climate risks, Scope 1 and 2 emissions for large accelerated filers, and scenario analysis in certain cases. As of early 2026 the rule is subject to ongoing litigation; implementation is uncertain. Source: [SEC — climate disclosure rule final text](https://sec.gov/rules/final/2024/33-11275.pdf), accessed 2026-04-16.

**United Kingdom:** The Financial Conduct Authority (FCA) mandates Task Force on Climate-related Financial Disclosures (TCFD)-aligned disclosure for premium listed companies since 2021, extended to all listed companies by 2022. Source: [FCA — TCFD disclosure rules](https://www.fca.org.uk/publications/policy-statements/ps21-23-enhancing-climate-related-disclosures-listed-issuers), accessed 2026-04-16.

**Australia:** Treasury released draft mandatory climate-related financial disclosure legislation in 2023; the Australian Accounting Standards Board (AASB) finalised AASB S2 (climate-related disclosures) in 2024. Phased mandatory disclosure begins for large entities (financial year 2025). Source: [Treasury — mandatory climate disclosure consultation](https://treasury.gov.au/consultation/c2023-462886), accessed 2026-04-16.

##### What's still voluntary

Japan, Canada, and most other OECD members rely on TCFD-aligned voluntary frameworks. Some jurisdictions (Canada, New Zealand) have published draft mandatory requirements but not yet legislated them as of April 2026. Source: [ISSB — IFRS S2 adoption tracker](https://www.ifrs.org/groups/international-sustainability-standards-board/ifrs-s2-adoption/), accessed 2026-04-16.

##### Where significant variation exists

The EU and US diverge on scope. CSRD applies to all large companies operating in the EU regardless of where they are listed; the SEC rule applies to US-listed companies only. This creates extraterritorial tension for multinationals listed in both markets.

Scope 3 emissions reporting is the clearest variation point: required under CSRD's ESRS standards for many sectors; omitted from the SEC final rule (delayed indefinitely). Source: [TCFD — 2023 status report](https://www.fsb-tcfd.org/publications/tcfd-2023-status-report/), accessed 2026-04-16.

AU and NZ have broadly aligned with the ISSB (IFRS S2) framework rather than CSRD, meaning their disclosure taxonomies will diverge from EU requirements.

##### Key uncertainties

- SEC rule litigation: multiple US circuit courts are considering stays. The final mandatory scope is uncertain.
- ISSB adoption pace: whether non-EU OECD members (Canada, Japan, Korea) will move to mandatory requirements within a 3-year horizon is genuinely unclear. No public timeline exists.
- Assurance requirements: most jurisdictions are still consulting on whether climate disclosures will require third-party assurance and at what level (limited vs reasonable).

##### Sources

1. [EUR-Lex — CSRD text (Directive 2022/2464)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022L2464) — EU mandatory disclosure requirements, accessed 2026-04-16
1. [SEC — climate disclosure final rule 33-11275](https://sec.gov/rules/final/2024/33-11275.pdf) — US rule scope and Scope 3 position, accessed 2026-04-16
1. [FCA — PS21/23 TCFD disclosure policy statement](https://www.fca.org.uk/publications/policy-statements/ps21-23-enhancing-climate-related-disclosures-listed-issuers) — UK mandatory requirements, accessed 2026-04-16
1. [Treasury AU — mandatory climate disclosure consultation](https://treasury.gov.au/consultation/c2023-462886) — AU phased disclosure timeline, accessed 2026-04-16
1. [IFRS — ISSB S2 adoption tracker](https://www.ifrs.org/groups/international-sustainability-standards-board/ifrs-s2-adoption/) — ISSB adoption status by jurisdiction, accessed 2026-04-16
1. [TCFD — 2023 Status Report](https://www.fsb-tcfd.org/publications/tcfd-2023-status-report/) — voluntary vs mandatory landscape, Scope 3 variation, accessed 2026-04-16
1. [APRA CPG 229 — Climate Change Financial Risks](https://www.apra.gov.au/sites/default/files/2021-11/Final%20Prudential%20Practice%20Guide%20CPG%20229%20Climate%20Change%20Financial%20Risks.pdf) — AU prudential sector guidance, accessed 2026-04-16

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 7.5/8 (94%) | 2026-04-16 |

- [x] PASS: Skill selects Standard tier as requested and does not inflate to Deep — Step 1 defines three tiers with clear criteria. Standard uses 5-8 sources. The prompt explicitly requests Standard; the skill defaults to Standard when not specified and does not upscale without cause.
- [x] PASS: Every source cited has been fetched and read — Rules block: "Never cite a source you haven't read. Fetch the page before including it." This is stated as an absolute rule. The skill's output format requires a sources section listing each source.
- [x] PASS: Authority hierarchy applied — Step 2 defines the authority hierarchy explicitly: government/regulatory above journalism, which is above analyst/company sources. Rules: "Don't cite a blog when a government dataset exists." SEC, FCA, EUR-Lex, Treasury AU, and APRA are all primary regulatory sources.
- [x] PASS: Output organised by theme, not by source — Step 4 Standard instructions: "organise findings by theme, not by source. The reader wants to understand the topic, not to read a list of what each website said." The output format for Standard has named theme sections.
- [x] PASS: Where sources conflict, conflict is explained rather than one version chosen arbitrarily — Step 4: "Where sources conflict, explain the conflict rather than choosing a side arbitrarily. Conflicting findings are often the most useful output." Standard tier output format includes guidance on this.
- [x] PASS: Key uncertainties section present covering thin or contested evidence — Standard tier output format template includes `### Key uncertainties` as a named section.
- [~] PARTIAL: For AU/NZ dimensions, AU/NZ sources used first — Rules block: "For AU/NZ topics, use AU/NZ sources first: ABS, Stats NZ, ABC News, RNZ, ASIC, APRA." The skill names these sources explicitly. Scored 0.5 because this is a global question with an AU/NZ dimension, not a purely AU/NZ question — the criterion is partially applicable and the skill handles this correctly by using APRA and Treasury AU where relevant, but the AU-first rule is a subordinate concern here.
- [x] PASS: Sources section lists each source with URL and what it contributed — output format template has `### Sources` with `[Title](URL) — [what it contributed]` per entry for Standard tier.

## Notes

The three-tier structure with explicit source counts and output format templates per tier is one of the strongest structural features in the analyst plugin. The authority hierarchy table in Step 2 prevents the common failure mode of citing vendor blog posts alongside regulatory guidance at the same level. The PARTIAL on AU/NZ sources is a fair score for a primarily global question with an AU/NZ component — the skill handles it correctly but the criterion is partially applicable.
