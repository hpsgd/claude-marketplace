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
