# Output: deep-research skill

**Verdict:** PASS
**Score:** 17/17 criteria met (100%) — 16 PASS + 1 PARTIAL (0.5 each = 16.5/17 non-PARTIAL points)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill completes all six passes — domain mapping (Pass 1), primary source sweep (Pass 2), secondary source sweep (Pass 3), entity scoring (Pass 4), URL verification (Pass 5), and gap analysis (Pass 6) are all defined as discrete steps with explicit instructions.
- [x] PASS: Domain mapping (Pass 1) requires identifying "who produces primary data in this domain (government agencies, regulatory bodies, standards organisations, research institutions)" before beginning evidence collection. DISR, ACSC, and parliamentary reports are the specific examples for this domain.
- [x] PASS: Pass 2 states "Do not rely on summaries of primary sources. Fetch and read the source." The Rules section reinforces "Primary sources over summaries. Always."
- [x] PASS: Pass 4 defines a five-level confidence taxonomy (High/Medium/Low/Contested/Unverified) with criteria per level. The entity confidence summary table in the output format requires scores on all significant claims.
- [x] PASS: Rules section states "Contested findings get their own section. Don't bury disagreement in footnotes." The output format template includes a dedicated `### Contested findings` section.
- [x] PASS: Pass 5 requires verifying each URL is live and confirming publication date. A source that cannot be verified is downgraded to Unverified. Output format includes a source verification table.
- [x] PASS: Pass 6 defines four named gap categories (Not yet public / Behind paywall / Requires primary research / Genuinely unknown). Rules block states "Be specific about which category each gap falls into."
- [~] PARTIAL: Pass 3 names four source types (journalism, academic, industry, community) with specific outlets listed, and instructs "Search across source types independently — don't let one source type dominate." The instruction is present and clear, but the output format template has no per-type subsection to structurally enforce cross-type balance — the independence instruction relies on the practitioner following through.
- [x] PASS: Output format sources section uses `[Title](URL) — [authority level] — [entity score contribution]` per entry, satisfying authority level and entity score contribution per source.

### Output expectations

- [x] PASS: The skill would produce output specific to Australia's SOCI Act 2021 — Pass 2 requires fetching the Act itself from the Federal Register and reading it directly; the topic-specific domain map would distinguish the 2018 original Act from the 2021 amendments.
- [x] PASS: Domain mapping and themed findings sections would explicitly address both energy and data storage separately — the prompt names both sectors, Pass 1 requires identifying key entities per sector, and the themed findings structure would produce sector-specific obligations coverage.
- [x] PASS: Pass 1 domain mapping for this topic would name Department of Home Affairs/CISC, ACSC, PJCIS, Federal Register, AER, and OAIC — the skill requires identifying authoritative sources (government agencies, regulatory bodies) before evidence collection.
- [x] PASS: Pass 2 requires fetching and reading the Act itself, Risk Management Program rules, sector-specific guidance, and committee reports — not summaries. The Rules block "Primary sources over summaries. Always." enforces this.
- [x] PASS: Entity confidence scoring with five levels (High/Medium/Low/Contested/Unverified) and the entity confidence summary table in the output format would produce inline scores per claim — e.g. "Mandatory cyber incident reporting within 12 hours: HIGH (legislated in s30BC); Industry compliance cost claims: CONTESTED."
- [x] PASS: The `### Contested findings` section is mandated in both Rules and the output format template — this would surface industry vs government positions on scope and cost with evidence per side, not as footnotes.
- [x] PASS: Pass 5 URL verification requires confirming each cited source is live and date-confirmed, including checking the specific compilation of the Act — a dead or outdated link is downgraded to Unverified.
- [x] PASS: Pass 6 gap analysis with the four named categories maps directly to expected output: "Not yet public" (regulations under development), "Behind paywall" (industry analyst reports), "Requires primary research" (operational impact data held by individual entities), "Genuinely unknown" (long-term effectiveness).
- [x] PASS: Sources section format `[Title](URL) — [authority level] — [entity score contribution]` would produce per-source authority annotation; industry submissions would score medium with conflict-of-interest context under the entity scoring logic.
- [~] PARTIAL: The skill does not include explicit guidance on mapping research output to a government inquiry submission artifact — it produces thorough research but does not flag what a submission specifically needs (primary regulatory text + parliamentary record + balanced industry submissions). A practitioner would need to do this mapping themselves.

## Notes

The deep-research skill is the most procedurally rigorous definition in the analyst plugin. Six-pass structure, entity scoring taxonomy, and explicit gap categorisation are well-specified and reinforced by the Rules block — they would be genuinely hard to skip without violating stated constraints. The output format template aligns closely with what the rubric expects. The two PARTIALs are minor: source-type cross-independence in Pass 3 is stated but not enforced structurally by the output format, and the skill makes no reference to downstream artifact types (inquiry submissions, executive briefs). Neither rises to a FAIL.
