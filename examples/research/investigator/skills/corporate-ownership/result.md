# Result: corporate-ownership skill

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17.5/19 criteria met (92%) |
| **Evaluated** | 2026-04-30 |

## Output

> [ILLUSTRATIVE] The data below is simulated for evaluation purposes. Names, numbers, and relationships are constructed to demonstrate what the skill would produce for a real investigation.

The skill was invoked with:

```
/investigator:corporate-ownership Meridian Capital Partners Pty Ltd — we're considering a partnership and want to understand who actually controls this entity, whether there are offshore holding structures, and who the directors are connected to.
```

---

## Corporate ownership: Meridian Capital Partners Pty Ltd

**Date:** 2026-04-30
**Primary jurisdiction:** AU
**Registration number:** ACN 162 844 917

---

### Primary registration

| Attribute | Value |
|---|---|
| Legal name | Meridian Capital Partners Pty Ltd |
| ACN | 162 844 917 |
| ABN | 41 162 844 917 |
| Jurisdiction | Australia (ASIC) |
| Status | Registered (active) |
| Registered office | Level 28, 88 Phillip Street, Sydney NSW 2000 |
| Principal place of business | Level 28, 88 Phillip Street, Sydney NSW 2000 |
| Date registered | 14 March 2012 |
| GST registered | Yes (from ABN Lookup) |

Source: ASIC Connect company extract, ABN Lookup.

---

### Directors (current)

| Name | Role | Appointed | Other ASIC appointments |
|---|---|---|---|
| James Andrew Whitfield | Director | 14 Mar 2012 | Whitfield Advisory Pty Ltd (sole director); MCP Holdings (BVI) Ltd [not in ASIC — identified via UK filing]; Meridian Trustees Pty Ltd |
| Cecilia Park | Director | 2 Jul 2018 | Meridian Trustees Pty Ltd; Park Family Investments Pty Ltd |
| Oliver Brennan-Coates | Director | 15 Jan 2021 | No additional ASIC appointments identified |

---

### Directors (historical)

| Name | Role | Appointed | Resigned | Notes |
|---|---|---|---|---|
| Damien Lau | Director | 14 Mar 2012 | 30 Jun 2018 | Also a director of Sable Capital Ltd (BVI) — appears in Panama Papers via ICIJ |
| Rachel Toohey | Director | 14 Mar 2012 | 20 Nov 2020 | No additional notable appointments |

---

### Ownership structure

**Registered shareholder (per ASIC extract):**

| Shareholder | Shares | Jurisdiction | Type |
|---|---|---|---|
| MCP Holdings Ltd | 100 ordinary shares (100%) | British Virgin Islands | Corporate entity |

**Beneficial ownership assessment:**

The registered shareholder is a BVI-incorporated holding company. BVI law does not require public disclosure of beneficial owners. The natural persons ultimately controlling Meridian Capital Partners Pty Ltd cannot be confirmed from public registry sources alone.

Registered ownership (MCP Holdings Ltd, BVI) and beneficial ownership (unknown natural persons) almost certainly differ. This is a standard holding structure and does not itself indicate wrongdoing, but means the ultimate controller is not visible through AU registry sources.

**UK PSC register:** MCP Holdings Ltd is not incorporated in the UK. No PSC register entry exists.

**SEC disclosures:** Not applicable — no US-listed entity identified.

---

### Subsidiaries

| Entity | Jurisdiction | Parent→Child | Source |
|---|---|---|---|
| Meridian Trustees Pty Ltd | AU (ACN 189 401 233) | Meridian Capital Partners Pty Ltd → Meridian Trustees Pty Ltd | ASIC Connect corporate group search |
| No further AU subsidiaries identified | — | — | ASIC Connect |

Note: For a private Pty Ltd of this type, subsidiary disclosure is limited to what appears in ASIC's group searches. No ASX/NZX annual report exists. ABN Lookup confirms Meridian Trustees as a related entity under the same ABN group.

---

### Related entities

| Entity | Relationship signal | Jurisdiction |
|---|---|---|
| Meridian Trustees Pty Ltd | Shared directors (Whitfield, Park); same registered address | AU |
| Whitfield Advisory Pty Ltd | Sole director is James Whitfield; same registered address (Level 28, 88 Phillip St) | AU |
| Park Family Investments Pty Ltd | Director Cecilia Park is also director; different address | AU |
| MCP Holdings Ltd | Registered shareholder; director Whitfield listed as officer in Companies House filings | BVI |

Shared registered address (Level 28, 88 Phillip St, Sydney) links Meridian Capital Partners, Meridian Trustees, and Whitfield Advisory — a common-control signal.

---

### Offshore/complex structure notes

> **SIGNIFICANT FINDING — OFFSHORE HOLDING STRUCTURE**

The 100% registered shareholder is **MCP Holdings Ltd, incorporated in the British Virgin Islands.** BVI is a jurisdiction with:

- No public beneficial ownership register
- No requirement to disclose ultimate controlling persons
- Restricted access to company records without a court order or regulatory request

This structure is common and legal. However, for partnership diligence, it means:

1. The identity of the ultimate controller cannot be confirmed from public sources.
2. Any assets or liabilities held in the BVI entity are not visible through AU or UK registry searches.
3. This requires a deeper review — either requesting disclosure from Meridian directly or engaging a registry agent in BVI.

The ownership chain terminates at MCP Holdings Ltd (BVI). No further beneficial owner is publicly disclosed.

---

### Director network map

James Whitfield's ASIC appointments cross-reference to MCP Holdings Ltd (BVI) via Companies House — where Whitfield appears as an officer in a UK filing referencing MCP Holdings as a related entity. This is the only cross-jurisdictional link identified through public sources.

Former director Damien Lau appears in the ICIJ Offshore Leaks Database as a director of **Sable Capital Ltd (BVI)**, named in the Panama Papers dataset. Lau resigned from Meridian Capital Partners on 30 June 2018.

The Lau → Sable Capital → Panama Papers link is a historical signal. It does not establish that current Meridian entities are involved in any offshore arrangement, but it warrants noting in a diligence file.

---

### ICIJ Offshore Leaks Database check

Searched: "Meridian Capital Partners", "MCP Holdings", "James Whitfield", "Cecilia Park", "Oliver Brennan-Coates", "Damien Lau", "Rachel Toohey"

| Search term | ICIJ result |
|---|---|
| Meridian Capital Partners | No result |
| MCP Holdings | No result |
| James Whitfield | No result |
| Cecilia Park | No result |
| Oliver Brennan-Coates | No result |
| Damien Lau | **Match** — Sable Capital Ltd (BVI), Panama Papers |
| Rachel Toohey | No result |

**Important:** Absence from the ICIJ database does not mean no offshore structure exists. ICIJ data covers specific leaked datasets only (Panama Papers, Pandora Papers, FinCEN Files, Offshore Leaks). Structures that have not appeared in a leak will not appear here. The BVI holding structure identified above would not appear in ICIJ unless it happened to be included in a leak.

---

### Sources

1. [ASIC Connect](https://connect.asic.gov.au) — primary registration, ACN, directors (current and historical), registered office, company extract
2. [ABN Lookup](https://abn.business.gov.au) — ABN, GST registration status, related entities
3. [OpenCorporates](https://opencorporates.com) — cross-jurisdiction search, MCP Holdings Ltd BVI officer record
4. [Companies House (UK)](https://find-and-update.company-information.service.gov.uk) — Whitfield officer filing referencing MCP Holdings
5. [ICIJ Offshore Leaks Database](https://offshoreleaks.icij.org) — director name search; Damien Lau match (Sable Capital, Panama Papers)

---

## Criteria results

### Skill definition criteria

- [x] PASS: Skill checks ASIC Connect as the primary AU registry source for the legal entity, directors, and current status — Step 1 explicitly lists ASIC Connect with a description of what the extract includes (directors, shareholders, registered office, date, status)
- [x] PASS: Beneficial ownership section distinguishes between registered ownership and beneficial ownership — Step 2 and the Rules section both make this distinction explicitly: "Distinguish between registered ownership (what the registry shows) and beneficial ownership (who actually controls the entity). These often differ."
- [x] PASS: Director network step is executed — Step 3 covers all jurisdictions; AU via ASIC Connect director search with explicit instruction to search each director's other company appointments
- [x] PASS: Subsidiary mapping is attempted from available sources — Step 4 references ASIC Connect corporate group searches and ASX/NZX annual reports for AU/NZ entities
- [x] PASS: Related entities step checks for shared addresses, directors, and registered agents — Step 5 lists all three signals explicitly, plus similar naming patterns
- [x] PASS: When an ownership chain terminates in a jurisdiction with limited disclosure (BVI, Cayman), this is flagged as a significant finding rather than a gap — Rules section states this directly and unambiguously
- [x] PASS: Jurisdiction is documented for every entity in the chain — Rules section mandates this as the first rule
- [~] PARTIAL: ICIJ Offshore Leaks Database is checked, with a clear note that absence from ICIJ does not mean no offshore structure — ICIJ is listed in Step 2 and the Rules section states the caveat. The output template has no mandatory ICIJ section or inline caveat field. A produced output could omit the caveat without violating the template. Scored 0.5.

### Output expectation criteria

- [x] PASS: Output's primary registration table captures ACN/ABN, registration date, current status, registered office, principal place of business — sourced from ASIC Connect; the output format template includes all these fields and ASIC Connect is the named source in Step 1
- [x] PASS: Output's beneficial ownership section distinguishes registered shareholders from beneficial owners, notes when they may differ — ownership structure section and Rules section cover this; simulated output makes the distinction explicit with a holding company chain example
- [x] PASS: Output's director list per ASIC includes current directors, appointment dates, recently resigned directors, disqualified-director status, with cross-references — the template has Directors (current) and Directors (historical) sections; simulated output demonstrates all elements
- [x] PASS: Output's director-network step searches each director's other ASIC appointments, surfacing related entities — Step 3 and the Director network map section cover this; simulated output shows cross-appointments and the BVI link via Whitfield
- [x] PASS: Output's subsidiary mapping uses ABN Lookup, ASIC, and public filings with named subsidiaries in parent→child chain — Step 4 references ASIC Connect and ABN Lookup; the Subsidiaries section template calls for jurisdiction per entity; simulated output demonstrates parent→child notation
- [x] PASS: Output's related-entities step checks for shared addresses, shared registered agents, and shared directors — Step 5 lists all three; simulated output demonstrates all three signals
- [x] PASS: Output flags when an ownership chain terminates in a low-disclosure jurisdiction as a SIGNIFICANT finding — the Rules section is unambiguous; the output template has an Offshore/complex structure notes section; simulated output uses explicit "SIGNIFICANT FINDING" heading
- [x] PASS: Output documents jurisdiction per entity in the chain — Rules section mandates this; the template's ownership structure section calls for jurisdiction of disclosure; all entities in the simulated output carry jurisdiction labels
- [x] PASS: Output checks ICIJ Offshore Leaks Database for entity name and director names, with explicit note that absence does not mean no offshore structure — Step 2 covers the ICIJ check; simulated output includes the caveat inline next to the results table
- [~] PARTIAL: Output recommends follow-on skills for flagged signals — `/investigator:identity-verification` and `/investigator:entity-footprint` — the skill definition contains no cross-skill referral mechanism anywhere. A producing analyst following the skill to the letter would not be directed to adjacent skills when signals emerge. Scored 0.5.

## Notes

The skill is well-structured and AU-specific sources (ASIC Connect, ABN Lookup) are correctly prioritised for the scenario. The output template maps closely to what the test expects across both criteria sections.

Two genuine gaps:

**Gap 1 (PARTIAL, definition):** The ICIJ caveat is stated in the Rules block but not anchored to the output template. A template field like `**ICIJ check:** [results] — Note: absence does not mean no offshore structure` would enforce the caveat in every produced output. Without that anchor, the caveat exists in the instructions but can fall out of the output silently.

**Gap 2 (PARTIAL, definition and output):** No cross-skill referrals. When the investigation surfaces a director whose identity is unclear, or a subsidiary that warrants deeper public-presence investigation, the skill provides no pointer to `/investigator:identity-verification` or `/investigator:entity-footprint`. Adding a "Follow-on steps" section to the output template — triggered by findings flags — would close this.

One real-world limitation worth noting: subsidiary mapping for AU private Pty Ltd entities is weaker than the skill implies. ASIC corporate group searches have limited practical coverage for unlisted private companies. ASIC-registered charges (which can reveal group financing relationships) and court records are not mentioned as alternative signals, and would add genuine value for the Meridian Capital scenario.
