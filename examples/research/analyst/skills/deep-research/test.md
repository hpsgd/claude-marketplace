# Test: deep-research skill

Scenario: A policy consultant needs exhaustive research on Australia's Critical Infrastructure Act 2021 sector-by-sector impact, for a submission to a government inquiry.

## Prompt

/analyst:deep-research Impact of Australia's Security of Critical Infrastructure Act 2021 on private sector obligations — specifically what changed for the energy and data storage sectors, and what is contested or unclear.

A few specifics for the response:

- Domain map MUST name these AU sources by name even if not all are reachable: Department of Home Affairs (CISC), ACSC/ASD, PJCIS, **AER (Australian Energy Regulator)**, **OAIC (for data)**, AEMO (energy), and the **Federal Register of Legislation** (for the Act itself and the CIRMP Rules). Include a Federal Register URL for the Act in the source list.
- Confidence taxonomy: use ALL of `HIGH`, `MEDIUM`, `LOW`, `CONTESTED`, `UNVERIFIED` as inline tags on claims (not just High/Medium/Low). At minimum, tag the industry compliance-cost claim as CONTESTED and any claim that has no traceable source as UNVERIFIED.
- Source-type diversity: include at least one journalism source (e.g. AFR, ABC, The Guardian Australia) and at least one academic / think-tank source (e.g. ASPI, Lowy Institute, university law review) alongside the law-firm analyses, so no single source type dominates. Note any source-type gaps in the Gap Analysis section.
- Sources section MUST map each source to the specific claims it supported (cross-reference the entity confidence table by claim ID or short label) — not just authority level alone.
- End with a "Submission-readiness" subsection mapping findings to what an inquiry-submission drafter would need: primary regulatory text, parliamentary record, balanced industry submissions. Flag which gaps are submission-critical vs background.

## Criteria

- [ ] PASS: Skill completes all six passes — domain mapping, primary source sweep, secondary source sweep, entity scoring, URL verification, and gap analysis
- [ ] PASS: Domain mapping identifies the authoritative sources (DISR, ACSC, parliamentary committee reports) before beginning evidence collection
- [ ] PASS: Primary sources are fetched and read directly — not cited via summaries or secondary references
- [ ] PASS: Entity confidence scoring is applied to all significant claims — High/Medium/Low/Contested/Unverified
- [ ] PASS: Contested findings get their own section and present each position with its evidence — not buried in footnotes
- [ ] PASS: URL verification step confirms each cited source is live and the date is confirmed
- [ ] PASS: Gap analysis categorises each gap (not yet public / paywall / primary research needed / genuinely unknown) — not just "information unavailable"
- [ ] PARTIAL: Secondary source sweep draws on multiple source types independently — journalism, academic, industry — without one type dominating
- [ ] PASS: Sources section includes authority level and entity score contribution per source

## Output expectations

- [ ] PASS: Output addresses Australia's Security of Critical Infrastructure Act 2021 specifically — covering the 2018 original Act and the 2021 amendments (SOCI Act amendments), not just generic "critical infrastructure law"
- [ ] PASS: Output's sector coverage explicitly addresses BOTH energy AND data storage / processing — separately, with sector-specific obligations (e.g. positive security obligation, mandatory cyber incident reporting) per sector
- [ ] PASS: Output's domain-mapping step names authoritative AU sources — Department of Home Affairs (CISC, formerly DCO), ACSC, Parliamentary Joint Committee on Intelligence and Security (PJCIS) reports, Federal Register of Legislation, sector-specific regulators (AER for energy, OAIC for data) — before evidence collection
- [ ] PASS: Output's primary sources are fetched and read — the Act itself (federal register URL), the Risk Management Program rules, sector-specific guidance documents, parliamentary committee reports — not cited via summaries
- [ ] PASS: Output's entity confidence per significant claim uses High / Medium / Low / Contested / Unverified — e.g. "Mandatory cyber incident reporting within 12 hours: HIGH (legislated in s30BC); Industry's compliance cost claims: CONTESTED (varies widely by source)"
- [ ] PASS: Output's contested findings get their own section — presenting industry's view (high cost, low net benefit) alongside government's view (national security imperative) with evidence per position, not buried as footnotes
- [ ] PASS: Output's URL verification confirms each cited source is live — checking publication date, version (e.g. specific compilation of the Act), and that the link still resolves
- [ ] PASS: Output's gap analysis classifies each gap — "not yet public" (regulations under development), "paywall" (industry analyst reports), "primary research needed" (operational impact data is held by individual entities), "genuinely unknown" (long-term effectiveness)
- [ ] PASS: Output's sources section includes per-source authority level (government legislation = high authority, parliamentary committee = high, industry submission = medium with conflict-of-interest noted, news = medium with date sensitivity) and what each source contributed
- [ ] PARTIAL: Output addresses what would be needed for a strong inquiry submission — primary regulatory text + parliamentary record + a balanced selection of industry submissions — the requester is preparing one, so the deep-research output should map to that artifact
