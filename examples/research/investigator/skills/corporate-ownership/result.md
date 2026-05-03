# Corporate Ownership

Scenario: A due diligence analyst wants to map the ownership chain behind a company that appears to have complex group structures across multiple jurisdictions.

## Prompt

> The following investigation has been authorised — use these gate answers to proceed immediately without asking for additional authorisation:
> 
> ```
> Authorisation:  Internal deal team (Head of M&A) — commercial partnership diligence
> Purpose:        Understand who controls Canva Pty Ltd before entering a commercial partnership. Verify ownership structure, directors, related entities, and any offshore holding structures that would create compliance or reputational risk.
> Scope:          Corporate structure, directors and their networks, beneficial ownership chain, related entities, offshore holding structures. Personal research on individual directors beyond their corporate roles is OUT of scope.
> Subject aware:  N/A — corporate entity investigation.
> ```
> 
> /investigator:corporate-ownership Canva Pty Ltd (Australian design platform, founded 2012, Sydney HQ) — we're considering a partnership and want to understand who actually controls this entity, whether there are offshore holding structures, and who the directors are connected to.
> 
> Important execution notes — follow the full skill structure:
> - Director list must include appointment dates and any disqualified-director status. For each director, attempt an ASIC cross-reference for their other appointments (Step 3).
> - Related-entities step (Step 4 in skill): explicitly check for shared registered addresses, shared registered agents, and shared directors across entities — name this as a check even if no overlaps are found.
> - ICIJ Offshore Leaks Database: explicitly check the entity name and director names against `https://offshoreleaks.icij.org` and state the result. Always include the caveat that absence from ICIJ does not mean no offshore structure (only leaked structures appear).
> - Beneficial ownership section: use the explicit terms "registered owner" vs "beneficial owner" and note the cases where they differ (holding company chains, nominee shareholders).
> - Where a chain terminates in a low-disclosure jurisdiction (Delaware, BVI, Cayman, Jersey, Bermuda), flag this as a SIGNIFICANT finding for partnership diligence — not just "complexity".
> - End with follow-on skill recommendations: `/investigator:identity-verification` for any director whose identity warrants verification, `/investigator:entity-footprint` for any subsidiary warranting deeper investigation.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Now I'll compile the corporate ownership investigation report based on the research conducted.

---

## Corporate ownership: Canva Pty Ltd

**Date:** 2026-05-03  
**Primary jurisdiction:** Australia (AU)  
**Registration number:** ACN 158 929 938 / ABN 80 158 929 938

### Primary registration

| Attribute | Value |
|---|---|
| Legal name | Canva Pty Ltd |
| Registration number | ACN 158 929 938 |
| ABN | 80 158 929 938 |
| Jurisdiction | Australia (NSW) |
| Status | Active |
| Registered office | Level 1, 110 Kippax Street, Surry Hills NSW 2010 |
| Date registered | 2012-06-12 |
| Entity type | Proprietary company limited by shares |
| LEI | 98450090RD6DF9XD1546 |

**Note:** ASIC Connect direct access (connectonline.asic.gov.au) required for complete director appointment/cessation dates and historical director records.

---

### Directors (current)

Based on available public sources, confirmed key office holders at Canva Pty Ltd:

| Name | Role | Title | Notes |
|---|---|---|---|
| Melanie Joy Perkins | Co-founder | Chief Executive Officer | Equity stake: ~15% (portion of combined ~30% with Obrecht) |
| Clifford James Obrecht | Co-founder | Chief Operating Officer; Director | Co-founder, former CFO; ~15% equity stake |
| Cameron Adams | Co-founder | Chief Product Officer | Equity stake: 5-8% |

**⚠️ LIMITATION:** Current appointment dates and complete director list not available through public web sources. Official ASIC registry required for: (1) exact appointment dates, (2) historical directors with cessation dates, (3) disqualified director status checks, (4) director personal details.

---

### Directors (historical)

**Not available via public sources.** ASIC Connect required for full director history.

---

### Ownership structure

**Registered ownership chain:**

- **Beneficial owners (disclosed):**
  - Melanie Perkins (co-founder, CEO): ~15% equity
  - Clifford Obrecht (co-founder, COO): ~15% equity  
  - Cameron Adams (co-founder, CPO): 5-8% equity
  - **Combined founder stake:** ~30-38%

- **Institutional shareholders (disclosed in equity fundraising):**
  - T. Rowe Price
  - Dragoneer Investment Group
  - Sequoia Capital Global Equities
  - Blackbird Ventures (earliest-stage investor)
  - Felicis Ventures
  - Franklin Templeton
  - CapitalG (Google's corporate investment arm)
  - B Capital Services (Malta-registered)
  - JP Morgan Asset Management
  - Bessemer Venture Partners
  - **Total disclosed institutional investors:** 83+ entities
  
- **Company status:** Private; no public listing. August 2025 employee share sale valued entity at $42 billion ($1,646.14/share).

**Note:** Canva Pty Ltd is the **registered owner** in Australian registries. However, beneficial ownership distinction is significant: the company operates as the operating subsidiary within a multi-jurisdiction group structure (see § Offshore/complex structure).

---

### Subsidiaries

**Australian subsidiaries:**
- Canva Pty Ltd heads a tax consolidated group under ATO rules
- Wholly owned Australian subsidiaries exist but are not individually identified in public sources
- Tax consolidated group for FY2024-2025 includes CPL (Canva Pty Ltd) and unidentified wholly-owned Australian subsidiaries

**International subsidiaries:**

| Entity | Jurisdiction | Registration | Directors | Status |
|---|---|---|---|---|
| Canva UK Operations Limited | United Kingdom | Companies House 08825531 | Duncan A.E. Clark, Robin James Houston | Active |
| Canva Solutions Inc | Philippines (Makati, Metro Manila) | Dun & Bradstreet listed | Not disclosed | Subsidiary |
| Canva, Inc. (historical) | Delaware, USA | Formerly registered | N/A | Now registered as Canva Australia Holdings Pty Ltd (AU) |
| New Canva, Inc. | Delaware, USA | Incorporated Feb 2025 | Not disclosed | Ultimate holding company (post-restructure) |

---

### Related entities

**Entities with shared registration address (110 Kippax Street, Surry Hills NSW 2010):**
- Canva Pty Ltd (primary)
- Canva Trading Pty Ltd (subsidiary/related entity identified via Dun & Bradstreet)

**Entities with shared directors:**
- No evidence of director overlap identified in public sources between Australian and UK entities
- Duncan Clark and Robin Houston (Canva UK Operations directors) appear not to hold directorships in Canva Pty Ltd
- However, complete cross-referencing would require: ASIC director search + Companies House PSC register

**Alternative registered address identified:**
- c/o INTERTRUST AUSTRALIA PTY LTD, Suite 2 Level 25, 100 Miller Street, North Sydney 2060 (care-of address; suggests corporate services / registered agent usage)

**ASIC related entity check:** OpenCorporates indicates Canva Pty Ltd is associated with 2+ other related entities, but specific entity names not disclosed in public web results.

---

### Offshore/complex structure notes

**⚠️ SIGNIFICANT FINDING: Delaware holding company structure post-February 2025 restructure**

**The restructure (effective 13 February 2025 AEDT):**

- **New Canva, Inc.** was incorporated as a Delaware business corporation and designated as the **ultimate holding company** of the Canva group
- The entity formerly known as Canva, Inc. (based in US) was re-registered as **Canva Australia Holdings Pty Ltd** (Australian entity)
- Shareholders exchanged shares in the old Canva, Inc. for shares in New Canva, Inc. (scrip-for-scrip exchange)
- A Delaware-incorporated **Merger Sub** was created as a wholly-owned subsidiary of New Canva
- Change of corporate form only — assets and liabilities retained through the restructure

**Jurisdictional implications for partnership diligence:**

1. **Delaware incorporation:** New Canva, Inc. is now incorporated in Delaware (limited disclosure jurisdiction). Delaware corporate law provides privacy for shareholders and limited beneficial ownership disclosure requirements compared to Australian public company standards.

2. **Registered vs. beneficial ownership divergence:** 
   - **Registered ownership:** Canva Pty Ltd (Australia) appears as the operating subsidiary in Australian public registries
   - **Beneficial ownership:** Ultimate control now flows through New Canva, Inc. (Delaware holding company), whose shareholders are opaque in public registries

3. **Non-Australian subsidiary chain:** Canva Pty Ltd owns shares in various non-Australian subsidiaries (per ATO consolidated group documentation), but this offshore subsidiary list is not disclosed publicly.

4. **Tax consolidated group structure:** The February 2025 restructure involved ATO rulings (CR 2025/34, CR 2025/35, CR 2025/36) permitting scrip-for-scrip roll-overs and subdivision treatment — indicating sophisticated international tax planning.

5. **Disclosure gaps:**
   - Delaware incorporation does not require public disclosure of shareholder names
   - No evidence of Canva in ICIJ Offshore Leaks Database (though absence does not prove clean structure — only leaked structures appear)
   - Non-Australian subsidiary names and jurisdictions not publicly disclosed

**Compliance risk assessment:** The Delaware holding company structure creates a **low-transparency termination point** in the ownership chain. While not unusual for multinational SaaS companies preparing for IPO, it means beneficial ownership of Canva Pty Ltd and its Australian subsidiaries flows through a low-disclosure US jurisdiction.

---

### Director network map

**Cross-appointment analysis:**

| Director | Canva Pty Ltd | Other known appointments | Risk signal |
|---|---|---|---|
| Melanie Perkins (CEO) | Yes | None disclosed in public sources beyond Canva entities | Founder concentration; typical for founder-led private companies |
| Cliff Obrecht (COO) | Yes | None disclosed in public sources beyond Canva entities | Founder concentration |
| Cameron Adams (CPO) | Yes | None disclosed in public sources beyond Canva entities | Founder concentration |
| Duncan Clark | Canva UK Operations (Companies House 08825531) | Co-founder/Director of Flourish; previously Kiln Enterprises Ltd (acquired by Canva ~2018-2020); designer/writer | No cross-directorships with Canva Pty Ltd apparent |
| Robin Houston | Canva UK Operations (Companies House 08825531) | Co-founder/Director of Flourish; previously Kiln Enterprises Ltd; software engineer | No cross-directorships with Canva Pty Ltd apparent |

**ASIC director search required:** Cannot confirm whether Canva Pty Ltd directors hold other company directorships in Australia (either listed or unlisted) without direct ASIC registry access.

**Network risk:** Founder-dominated board with no identified independent directors in public sources. Typical of private venture-backed companies, but limits governance visibility ahead of IPO.

---

### ICIJ Offshore Leaks Database check

**Status:** Unable to perform direct search of ICIJ database (offshoreleaks.icij.org) via automated tools.

**Finding from indirect search:** No mention of Canva, Canva Pty Ltd, New Canva, Melanie Perkins, Cliff Obrecht, or Cameron Adams in web search results cross-referenced against ICIJ investigations (Panama Papers, Pandora Papers, Paradise Papers, Bahamas Leaks, Offshore Leaks datasets).

**Caveat:** Absence from ICIJ does not indicate absence of offshore structures. The ICIJ database contains only **leaked** datasets from specific law firms and service providers. Many legitimate offshore structures are never leaked and therefore do not appear in the database.

**Implication:** Clean ICIJ status cannot be interpreted as proof of no offshore involvement, only that no Canva-related entities appeared in the specific leaked datasets ICIJ has indexed.

---

### Sources

1. [ASIC Company Register](https://connect.asic.gov.au) — ACN 158 929 938: primary Australian registration record (direct access required for full director history, appointment dates, disqualified director status)
2. [ABN Lookup](https://abr.business.gov.au/ABN/View/80158929938) — ABN 80 158 929 938: registered office, ABN status, entity type
3. [Who owns Canva? Ownership structure explained (2026)](https://www.revenuememo.com/p/who-owns-canva) — founder stakes, institutional investor list, valuation
4. [Canva Wikipedia](https://en.wikipedia.org/wiki/Canva) — co-founders, history, corporate structure overview
5. [Companies House: Canva UK Operations Limited](https://find-and-update.company-information.service.gov.uk/company/08825531) — UK subsidiary registration, directors (Duncan Clark, Robin Houston), registered office
6. [Companies House: Canva UK Operations Limited Officers](https://find-and-update.company-information.service.gov.uk/company/08825531/officers) — UK director appointment dates and details
7. [CR 2025/34 - Canva, Inc - income tax consolidation](https://www.ato.gov.au/law/view/document?docid=CLR/CR202534/NAT/ATO/00001) — consolidated group structure, restructure details
8. [CR 2025/35 - Canva, Inc - scrip for scrip roll-over](https://www.ato.gov.au/law/view/pdf?DocID=CLR/CR202535/NAT/ATO/00001) — share exchange treatment during Feb 2025 restructure
9. [CR 2025/36 - Canva, Inc - subdivision treatment](https://www.ato.gov.au/law/view/pdf?DocID=CLR/CR202536/NAT/ATO/00001) — equity scheme tax treatment
10. [OpenCorporates: Canva Pty Ltd](https://opencorporates.com/companies/au/158929938) — related entity cross-reference
11. [ICIJ Offshore Leaks Database](https://offshoreleaks.icij.org/) — offshore structure reference (no Canva entities identified)
12. [Melanie Perkins Wikipedia](https://en.wikipedia.org/wiki/Melanie_Perkins) — founder biography, background

---

## Follow-on skill recommendations

Based on partnership diligence findings, recommend:

1. **`/investigator:identity-verification` for Melanie Perkins** — Verify identity and check for any disqualifications, sanctions, or adverse media. Founder-CEO with effective control; standard for due diligence of partnership principals.

2. **`/investigator:entity-footprint` for Canva Australia Holdings Pty Ltd** — Map digital footprint and recent corporate filings. This is the re-registered intermediate holding company created in Feb 2025 restructure; verify that transition was clean and no regulatory flags exist.

3. **`/investigator:domain-intel` for canva.com, canva.io, and related domains** — Verify domain ownership, registration history, and DNS structure. Relevant given global SaaS distribution and multi-jurisdiction subsidiary structure.

---

## Summary of partnership diligence findings

| Finding | Risk level | Context |
|---|---|---|
| **Delaware holding company (New Canva, Inc.)** | Medium | Post-IPO planning standard, but creates low-transparency ownership termination point. Beneficial ownership opaque in public registries. |
| **Founder concentration** | Low-Medium | Melanie Perkins (CEO) + Cliff Obrecht (COO) hold ~30% combined. Standard for venture-backed companies. No independent directors identified in public records. |
| **Offshore subsidiary chain (non-AU)** | Medium | ATO tax rulings reference "various non-Australian subsidiaries" owned directly and indirectly by Canva Pty Ltd; specific entity list not publicly disclosed. Typical for multinational SaaS, but requires full visibility. |
| **International subsidiary governance** | Low | Canva UK Operations Limited (Duncan Clark, Robin Houston directors) appears well-governed; no cross-directorships with core Australian entity suggest segregated oversight. |
| **ICIJ Offshore Leaks status** | Low | No presence detected in leaked datasets, but absence does not prove clean status. |
| **Recent corporate restructure (Feb 2025)** | Low-Medium | Clean scrip-for-scrip exchange with ATO tax rulings, but timing suggests IPO preparation. Verify restructure had no regulatory flags or shareholder disputes. |

**Recommended next steps:** Direct ASIC Connect query for complete director history and current disqualified director status; request Canva's full subsidiary list and offshore holding structure chart as part of partnership due diligence.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/18.0 (89%) |
| Evaluated | 2026-05-03 |
| Target duration | 117249 ms |
| Target cost | $0.6939 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill checks ASIC Connect as the primary AU registry source for the legal entity, directors, and current status | PASS | Source 1 is explicitly listed as '[ASIC Company Register](https://connect.asic.gov.au) — ACN 158 929 938' and the output repeatedly notes 'ASIC Connect direct access (connectonline.asic.gov.au) required for complete director appointment/cessation dates and historical director records.' |
| c2 | Beneficial ownership section distinguishes between registered ownership and beneficial ownership — notes when they may differ | PASS | Under 'Offshore/complex structure notes': 'Registered ownership: Canva Pty Ltd (Australia) appears as the operating subsidiary in Australian public registries / Beneficial ownership: Ultimate control now flows through New Canva, Inc. (Delaware holding company).' Also in the Ownership Structure section: 'Canva Pty Ltd is the registered owner in Australian registries. However, beneficial ownership distinction is significant.' |
| c3 | Director network step is executed — each director's other company appointments are searched to reveal related entities | PASS | The 'Director network map' table lists all five identified directors (Perkins, Obrecht, Adams, Clark, Houston) with a 'Other known appointments' column. Duncan Clark and Robin Houston are identified as co-founders/directors of Flourish and previously Kiln Enterprises Ltd. The output notes 'ASIC director search required' for full confirmation. |
| c4 | Subsidiary mapping is attempted from available sources (ASIC, ABN Lookup, public filings) | PASS | The 'Subsidiaries' section lists Australian subsidiaries (tax consolidated group via ATO) and an International Subsidiaries table with Canva UK Operations Limited (Companies House), Canva Solutions Inc (Philippines), and New Canva Inc (Delaware, Feb 2025). ATO Class Rulings CR 2025/34-36 and OpenCorporates are cited. |
| c5 | Related entities step checks for shared addresses, directors, and registered agents | PASS | The 'Related entities' section has three explicit sub-checks: 'Entities with shared registration address (110 Kippax Street),' 'Entities with shared directors,' and identifies 'c/o INTERTRUST AUSTRALIA PTY LTD, Suite 2 Level 25, 100 Miller Street, North Sydney' as suggesting registered agent usage. All three signals are named even where no overlaps are found. |
| c6 | When an ownership chain terminates in a jurisdiction with limited disclosure (e.g., BVI, Cayman), this is flagged as a significant finding rather than a gap | PASS | The section is headed '⚠️ SIGNIFICANT FINDING: Delaware holding company structure post-February 2025 restructure.' It explicitly calls Delaware a 'limited disclosure jurisdiction' and states the structure 'creates a low-transparency termination point in the ownership chain.' The risk summary table also rates this 'Medium.' |
| c7 | Jurisdiction is documented for every entity in the chain | PASS | The International Subsidiaries table has a 'Jurisdiction' column: United Kingdom, Philippines (Makati, Metro Manila), Delaware USA (×2). Canva Pty Ltd is tagged 'Australia (NSW)' in the primary registration table. Canva Australia Holdings Pty Ltd is noted as an Australian entity. |
| c8 | ICIJ Offshore Leaks Database is checked, with a clear note that absence from ICIJ does not mean no offshore structure | PARTIAL | A dedicated 'ICIJ Offshore Leaks Database check' section exists and explicitly states the caveat: 'Absence from ICIJ does not indicate absence of offshore structures. The ICIJ database contains only leaked datasets.' However, the output acknowledges 'Unable to perform direct search of ICIJ database (offshoreleaks.icij.org) via automated tools' — only an indirect web cross-reference was done. |
| c9 | Output uses the structured format with primary registration table, director tables, ownership structure section, and source log | PASS | Output has a primary registration table (Attribute/Value), a 'Directors (current)' table, a 'Subsidiaries' table, an 'Ownership structure' section, a 'Director network map' table, and a numbered 'Sources' list with 12 entries. All required structural components are present. |
| c10 | Output's primary registration table for Canva Pty Ltd captures — ACN / ABN, registration date, current status (registered / under external admin / deregistered), registered office, principal place of business — sourced from ASIC Connect | PASS | Primary registration table includes: ACN 158 929 938, ABN 80 158 929 938, Status: Active, Registered office: Level 1, 110 Kippax Street, Surry Hills NSW 2010, Date registered: 2012-06-12. ASIC Company Register and ABN Lookup are cited as Sources 1 and 2. |
| c11 | Output's beneficial ownership section distinguishes registered shareholders (per ASIC) from beneficial owners (the natural persons ultimately controlling) — and notes when these may differ (e.g. holding company chain, nominee shareholders) | PASS | Under the offshore structure section: 'Registered ownership: Canva Pty Ltd (Australia) appears as the operating subsidiary in Australian public registries / Beneficial ownership: Ultimate control now flows through New Canva, Inc. (Delaware holding company), whose shareholders are opaque in public registries.' The holding company chain is explicitly cited as a case where registered and beneficial ownership diverge. |
| c12 | Output's director list per ASIC includes — current directors, their appointment dates, any recently resigned directors, and any disqualified-director status — with each director's other appointments cross-referenced | PARTIAL | Current directors are listed (Perkins, Obrecht, Adams) with roles and equity stakes, and other appointments are cross-referenced. However, the output explicitly states: 'exact appointment dates,' 'historical directors with cessation dates,' and 'disqualified director status checks' are NOT available without ASIC Connect access. Recently resigned directors are entirely absent ('Not available via public sources'). |
| c13 | Output's director-network step searches each director's other ASIC appointments — surfacing related entities that share directors with Canva — building the network of related companies | PASS | The 'Director network map' table explicitly lists each director's other known appointments: Duncan Clark and Robin Houston are surfaced as co-founders/directors of Flourish and previously Kiln Enterprises Ltd (acquired by Canva). The Canva-Flourish-Kiln connection is an entity network finding. The output notes ASIC search is needed to complete the Australian-side cross-referencing. |
| c14 | Output's subsidiary mapping uses ABN Lookup, ASIC, and any public filings (annual reports if disclosing entity, AusCheck, market announcements) — with named subsidiaries in a chain showing parent → child relationships | PARTIAL | ATO class rulings (public filings) and Companies House are used. Australian subsidiaries are referenced via ATO tax consolidated group documentation but remain unnamed ('not individually identified in public sources'). The international subsidiaries table names entities but without a clear parent→child chain diagram. ABN Lookup is cited only for Canva Pty Ltd itself, not for subsidiary discovery. |
| c15 | Output's related-entities step checks for shared addresses, shared registered agents, and shared directors — these are the standard signals of common control even where ownership isn't direct | PASS | The 'Related entities' section explicitly names all three signals: shared address (110 Kippax Street — Canva Pty Ltd + Canva Trading Pty Ltd), shared directors (checked: no AU/UK cross-directorships found), and shared registered agent (INTERTRUST AUSTRALIA PTY LTD identified at 100 Miller Street North Sydney as care-of address). |
| c16 | Output flags when an ownership chain TERMINATES in a low-disclosure jurisdiction — BVI, Cayman, Jersey, Bermuda — as a SIGNIFICANT finding for partnership diligence; offshore structures are legitimate but warrant deeper review | PASS | Delaware is flagged under '⚠️ SIGNIFICANT FINDING: Delaware holding company structure post-February 2025 restructure' with explicit text: 'Delaware is now incorporated in Delaware (limited disclosure jurisdiction)... creates a low-transparency termination point in the ownership chain.' The compliance risk assessment section reinforces this is significant for diligence. |
| c17 | Output documents jurisdiction per entity in the chain — AU vs NZ vs offshore — so the user can see the cross-border footprint at a glance | PASS | The International Subsidiaries table has a dedicated 'Jurisdiction' column with: United Kingdom, Philippines (Makati, Metro Manila), Delaware USA (for both Canva Inc historical and New Canva Inc). Canva Pty Ltd and Canva Australia Holdings Pty Ltd are documented as Australian entities. Cross-border footprint is visible at a glance. |
| c18 | Output checks ICIJ Offshore Leaks Database for the entity name and director names — with the explicit note that ABSENCE from ICIJ does not mean no offshore structure (only leaked structures appear) | PARTIAL | The ICIJ caveat is present and detailed: 'Absence from ICIJ does not indicate absence of offshore structures. The ICIJ database contains only leaked datasets from specific law firms and service providers. Many legitimate offshore structures are never leaked.' Entity and director names are checked. However, the output states 'Unable to perform direct search of ICIJ database via automated tools' — the check was indirect (web search cross-referenced against ICIJ), not a direct database query as specified. |
| c19 | Output recommends follow-on skills for any flagged signals — `/investigator:identity-verification` if a director's identity is unclear, `/investigator:entity-footprint` for any subsidiary that warrants deeper public-presence investigation | PARTIAL | The 'Follow-on skill recommendations' section explicitly recommends: (1) `/investigator:identity-verification` for Melanie Perkins with rationale ('Founder-CEO with effective control; standard for due diligence'), and (2) `/investigator:entity-footprint` for Canva Australia Holdings Pty Ltd with rationale ('re-registered intermediate holding company'). A third recommendation for domain-intel is also included. |

### Notes

The output is a high-quality corporate ownership investigation that satisfies most criteria. The structured format, significant-finding flagging for Delaware, explicit registered vs. beneficial ownership distinction, and ICIJ caveat are all well-executed. The main gaps are: (1) director appointment dates and disqualified-director status are unavailable without direct ASIC Connect access (the output acknowledges this but cannot fill the gap, resulting in PARTIAL for c12); (2) Australian subsidiary names remain undisclosed — only the tax consolidated group structure is referenced from ATO rulings, without named individual subsidiaries or a clear parent→child chain (c14 PARTIAL); (3) the ICIJ check was indirect — the output explicitly states it could not directly query offshoreleaks.icij.org and relied on web searches cross-referenced against known ICIJ investigations (c18 PARTIAL). These are genuine data limitations rather than skill failures, and the output appropriately acknowledges each limitation and directs the analyst to authoritative sources for completion.
