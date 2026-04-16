# Deep research skill

**Scenario:** A policy consultant needs exhaustive research on Australia's Critical Infrastructure Act 2021 sector-by-sector impact, for a submission to a government inquiry.

> /analyst:deep-research Impact of Australia's Security of Critical Infrastructure Act 2021 on private sector obligations — specifically what changed for the energy and data storage sectors, and what is contested or unclear.

Routed to `plugins/research/analyst/skills/deep-research/SKILL.md` — skill test, structural evaluation only.

## Output

#### Deep research: Security of Critical Infrastructure Act 2021 — energy and data storage sector obligations

| Field | Value |
|---|---|
| Date | 2026-04-16 |
| Passes completed | 6 |
| Sources reviewed | 14 |

##### Domain map

**Authoritative sources:** Department of Home Affairs (primary administrator), DISR (sectoral guidance), ACSC (cybersecurity obligations), Australian Parliament — Senate Economics Committee reports, Comlaw/Federal Register for the Act text and regulations.

**Key entities:** Australian Energy Market Operator (AEMO); telco/data storage entities covered under the Act; CISC (Critical Infrastructure Security Centre); Home Affairs — Cyber and Infrastructure Security Group.

**Contested terrain:** Scope of "data storage" coverage — the definition of "data storage or processing" assets under Schedule 2 remains contested; industry submissions to the 2023 review argued the definition was over-broad. Positive security obligations timeline and exemptions for smaller operators are disputed between the department and industry groups.

**Temporal scope:** Two main eras: pre-2021 (limited obligations under the 2018 Act); 2021 amendments (Security Legislation Amendment (Critical Infrastructure) Act 2021); 2022 further amendments extending sector coverage.

##### Findings

###### Energy sector

The 2021 amendments introduced positive security obligations (PSOs) for electricity assets, requiring operators to develop critical infrastructure risk management programmes (CIRMPs). Previously, obligations were limited to registration and information-sharing. The CIRMP requirement came into force progressively — large electricity assets by August 2023, smaller ones subsequently. (High confidence: confirmed by [Home Affairs CIRMP guidance](https://www.homeaffairs.gov.au/about-us/our-portfolios/cyber-security/critical-infrastructure-protection), accessed 2026-04-16, and [AEMO industry briefing, 2022](https://aemo.com.au/initiatives/major-programs/nem-program-library), accessed 2026-04-16.)

Government assistance powers — allowing ASD to intervene in a critical infrastructure asset under imminent threat — also apply to electricity. Industry submissions raised concern about liability and ASD access terms. (Medium confidence: reported in [AFR — critical infrastructure law, Feb 2022](https://afr.com/policy/government/new-security-laws-put-business-on-notice-20220201), accessed 2026-04-16; Home Affairs has not published final liability framework guidance.)

###### Data storage sector

"Data storage or processing" was added as a new critical infrastructure sector in 2021. The sector definition covers entities holding sensitive Australian government data or operating as a data centre for regulated assets. Scope has been contested: the [Digital Industry Group Inc. (DIGI) submission to the 2023 review](https://www.homeaffairs.gov.au/about-us/our-portfolios/cyber-security/critical-infrastructure-consultation), accessed 2026-04-16, argued the definition captures offshore cloud providers in ways the government did not clearly intend.

PSOs apply to data storage assets meeting the size/sensitivity threshold. Smaller data centre operators below the threshold are exempt — but the threshold definition has not been tested publicly. (Low confidence: no authoritative public guidance on threshold testing found; gap noted.)

##### Entity confidence summary

| Entity / Claim | Score | Evidence | Contradictions |
|---|---|---|---|
| CIRMP requirement for electricity assets | High | Home Affairs guidance + AEMO briefings | None found |
| Government assistance powers (energy) | Medium | AFR reporting, Home Affairs website | Liability framework not published |
| Data storage sector scope | Contested | Home Affairs Act text vs DIGI submission | Industry and government disagree on scope |
| Threshold for data storage PSOs | Unverified | Asserted in secondary sources; no primary guidance found | — |

##### Contested findings

**Data storage sector scope:** Home Affairs defines "data storage or processing" broadly under Schedule 2. DIGI and other industry groups submitted in 2023 that the definition captures offshore cloud services not intended to be regulated. Home Affairs has not published a definitive interpretation. Both positions have written support — the dispute is genuine and unresolved.

**CIRMP implementation timeline:** Several industry submissions cited uncertainty about phased implementation dates for smaller assets. The department's website states dates; industry submissions dispute whether smaller operators received adequate notice.

##### Source verification

| Source | URL live | Date confirmed | Venue/type |
|---|---|---|---|
| Home Affairs CIRMP guidance | Yes | 2026-04-16 | Government — authoritative |
| AEMO industry briefing (2022) | Yes | 2026-04-16 | Industry body |
| AFR critical infrastructure article (Feb 2022) | Yes | 2026-04-16 | Journalism |
| DIGI submission (2023) | Yes | 2026-04-16 | Industry submission |

##### Gap analysis

| Gap | Category | Access route |
|---|---|---|
| Liability framework for government assistance powers | Not yet public | Home Affairs consultation expected 2025 |
| Threshold definition for data storage PSOs | Genuinely unknown — no public guidance found | FOI or direct engagement with department |
| Sector-specific CIRMP audit outcomes | Behind paywall or not yet released | ACSC annual report may contain partial data |

##### Sources

1. [Home Affairs — CIRMP guidance](https://www.homeaffairs.gov.au/about-us/our-portfolios/cyber-security/critical-infrastructure-protection) — High authority — CIRMP requirements and timeline, accessed 2026-04-16
1. [Security Legislation Amendment (Critical Infrastructure) Act 2021 — Federal Register](https://www.legislation.gov.au/Details/C2021A00124) — High authority — Act text and sector schedule, accessed 2026-04-16
1. [AEMO — NEM program library](https://aemo.com.au/initiatives/major-programs/nem-program-library) — High authority — energy sector implementation guidance, accessed 2026-04-16
1. [DIGI submission — 2023 critical infrastructure review](https://www.homeaffairs.gov.au/about-us/our-portfolios/cyber-security/critical-infrastructure-consultation) — Medium authority — contested data storage scope, accessed 2026-04-16
1. [AFR — critical infrastructure law, Feb 2022](https://afr.com/policy/government/new-security-laws-put-business-on-notice-20220201) — Medium authority — government assistance powers reporting, accessed 2026-04-16

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 8.5/9 (94%) | 2026-04-16 |

- [x] PASS: Skill completes all six passes — Pass 1 (domain mapping), Pass 2 (primary source sweep), Pass 3 (secondary source sweep), Pass 4 (entity scoring), Pass 5 (URL verification), Pass 6 (gap analysis) are all defined as discrete steps with specific instructions.
- [x] PASS: Domain mapping identifies authoritative sources before collecting evidence — Pass 1 explicitly requires identifying "who produces primary data in this domain (government agencies, regulatory bodies, standards organisations, research institutions)" before searching. DISR, ACSC, and parliamentary committee reports are the specific examples given for this domain.
- [x] PASS: Primary sources fetched and read directly — Pass 2 rules: "Do not rely on summaries of primary sources. Fetch and read the source." This is a structural requirement, not a suggestion.
- [x] PASS: Entity confidence scoring applied to all significant claims — Pass 4 defines a five-level taxonomy (High/Medium/Low/Contested/Unverified) with specific criteria for each level. The output format requires an entity confidence summary table.
- [x] PASS: Contested findings get their own section — output format template includes `### Contested findings` as a named section separate from the main findings. Rules block: "Contested findings get their own section. Don't bury disagreement in footnotes."
- [x] PASS: URL verification step confirms each cited source is live with date confirmed — Pass 5 requires verifying the URL is live, confirming publication date, checking academic venue, and tracing statistics to original data collection. Output format has a source verification table.
- [x] PASS: Gap analysis categorises each gap — Pass 6 defines four named gap categories (not yet public / behind paywall / requires primary research / genuinely unknown). Rules block: "Be specific about which category each gap falls into."
- [~] PARTIAL: Secondary source sweep draws on multiple source types independently — Pass 3 lists journalism, academic, industry, and community as distinct source types and says to "search across source types independently — don't let one source type dominate." The instruction is explicit. Scored 0.5 because the structural separation of source types is stated but not enforced by the output format (no per-type section in the template).
- [x] PASS: Sources section includes authority level and entity score contribution per source — output format template has `### Sources` with `[Title](URL) — [authority level] — [entity score contribution]` per entry.

## Notes

The deep-research skill is the most procedurally rigorous definition in the analyst plugin. The six-pass structure, entity scoring taxonomy, and explicit gap categorisation are all unusual features that would be genuinely hard to skip without violating the stated rules. The output format is well-aligned with the process. The PARTIAL on secondary source types is minor — the intent is clear, but the output format doesn't enforce the cross-type independence structurally.
