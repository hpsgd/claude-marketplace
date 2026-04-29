# Test: corporate-ownership skill

Scenario: A due diligence analyst wants to map the ownership chain behind a company that appears to have complex group structures across multiple jurisdictions.

## Prompt

/investigator:corporate-ownership Meridian Capital Partners Pty Ltd — we're considering a partnership and want to understand who actually controls this entity, whether there are offshore holding structures, and who the directors are connected to.

## Criteria

- [ ] PASS: Skill checks ASIC Connect as the primary AU registry source for the legal entity, directors, and current status
- [ ] PASS: Beneficial ownership section distinguishes between registered ownership and beneficial ownership — notes when they may differ
- [ ] PASS: Director network step is executed — each director's other company appointments are searched to reveal related entities
- [ ] PASS: Subsidiary mapping is attempted from available sources (ASIC, ABN Lookup, public filings)
- [ ] PASS: Related entities step checks for shared addresses, directors, and registered agents
- [ ] PASS: When an ownership chain terminates in a jurisdiction with limited disclosure (e.g., BVI, Cayman), this is flagged as a significant finding rather than a gap
- [ ] PASS: Jurisdiction is documented for every entity in the chain
- [ ] PARTIAL: ICIJ Offshore Leaks Database is checked, with a clear note that absence from ICIJ does not mean no offshore structure
- [ ] PASS: Output uses the structured format with primary registration table, director tables, ownership structure section, and source log

## Output expectations

- [ ] PASS: Output's primary registration table for Meridian Capital Partners Pty Ltd captures — ACN / ABN, registration date, current status (registered / under external admin / deregistered), registered office, principal place of business — sourced from ASIC Connect
- [ ] PASS: Output's beneficial ownership section distinguishes registered shareholders (per ASIC) from beneficial owners (the natural persons ultimately controlling) — and notes when these may differ (e.g. holding company chain, nominee shareholders)
- [ ] PASS: Output's director list per ASIC includes — current directors, their appointment dates, any recently resigned directors, and any disqualified-director status — with each director's other appointments cross-referenced
- [ ] PASS: Output's director-network step searches each director's other ASIC appointments — surfacing related entities that share directors with Meridian — building the network of related companies
- [ ] PASS: Output's subsidiary mapping uses ABN Lookup, ASIC, and any public filings (annual reports if disclosing entity, AusCheck, market announcements) — with named subsidiaries in a chain showing parent → child relationships
- [ ] PASS: Output's related-entities step checks for shared addresses, shared registered agents, and shared directors — these are the standard signals of common control even where ownership isn't direct
- [ ] PASS: Output flags when an ownership chain TERMINATES in a low-disclosure jurisdiction — BVI, Cayman, Jersey, Bermuda — as a SIGNIFICANT finding for partnership diligence; offshore structures are legitimate but warrant deeper review
- [ ] PASS: Output documents jurisdiction per entity in the chain — AU vs NZ vs offshore — so the user can see the cross-border footprint at a glance
- [ ] PASS: Output checks ICIJ Offshore Leaks Database for the entity name and director names — with the explicit note that ABSENCE from ICIJ does not mean no offshore structure (only leaked structures appear)
- [ ] PARTIAL: Output recommends follow-on skills for any flagged signals — `/investigator:identity-verification` if a director's identity is unclear, `/investigator:entity-footprint` for any subsidiary that warrants deeper public-presence investigation
