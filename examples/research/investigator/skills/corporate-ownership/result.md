# Output: corporate-ownership skill

**Verdict:** PARTIAL
**Score:** 17/19 criteria met (89%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill checks ASIC Connect as the primary AU registry source for the legal entity, directors, and current status — Step 1 explicitly lists ASIC Connect with a description of what the extract includes
- [x] PASS: Beneficial ownership section distinguishes between registered ownership and beneficial ownership — notes when they may differ — Step 2 and the Rules section both make this distinction explicitly
- [x] PASS: Director network step is executed — each director's other company appointments are searched to reveal related entities — Step 3 covers this for all jurisdictions including AU via ASIC Connect director search
- [x] PASS: Subsidiary mapping is attempted from available sources (ASIC, ABN Lookup, public filings) — Step 4 covers ASIC Connect corporate group searches and ASX/NZX annual reports for AU/NZ
- [x] PASS: Related entities step checks for shared addresses, directors, and registered agents — Step 5 lists all three signals explicitly
- [x] PASS: When an ownership chain terminates in a jurisdiction with limited disclosure (e.g., BVI, Cayman), this is flagged as a significant finding rather than a gap — Rules section states this directly
- [x] PASS: Jurisdiction is documented for every entity in the chain — Rules section mandates this
- [~] PARTIAL: ICIJ Offshore Leaks Database is checked, with a clear note that absence from ICIJ does not mean no offshore structure — Step 2 includes ICIJ with the correct caveat in the Rules section. Scored 0.5 because the output template has no mandatory ICIJ section or inline caveat; the note lives in the rules block only, so a produced output could omit it without violating the template structure

### Output expectations

- [x] PASS: Output's primary registration table captures ACN/ABN, registration date, current status, registered office, principal place of business — sourced from ASIC Connect — the output format template includes all these fields; ASIC Connect is the named source in Step 1
- [x] PASS: Output's beneficial ownership section distinguishes registered shareholders from beneficial owners, notes when they may differ — the ownership structure section combined with the Rules section covers this
- [x] PASS: Output's director list per ASIC includes current directors, appointment dates, recently resigned directors, disqualified-director status, with cross-references — Directors (current) and Directors (historical) sections in the template cover this; ASIC Connect is named as the source
- [x] PASS: Output's director-network step searches each director's other ASIC appointments, surfacing related entities — Step 3 and the Director network map section in the output template cover this
- [x] PASS: Output's subsidiary mapping uses ABN Lookup, ASIC, and public filings with named subsidiaries in parent→child relationships — Step 4 references ASIC Connect and ASX annual reports; Subsidiaries section in the template calls for jurisdiction per subsidiary
- [x] PASS: Output's related-entities step checks for shared addresses, shared registered agents, and shared directors — Step 5 lists all three explicitly
- [x] PASS: Output flags when an ownership chain terminates in a low-disclosure jurisdiction as a SIGNIFICANT finding — Rules section is unambiguous; the output template has an Offshore/complex structure notes section
- [x] PASS: Output documents jurisdiction per entity in the chain — Rules section mandates this; the output template's ownership structure section calls for jurisdiction of disclosure
- [x] PASS: Output checks ICIJ Offshore Leaks Database for entity name and director names, with explicit note that absence does not mean no offshore structure — Step 2 covers this with the caveat stated in the Rules section
- [~] PARTIAL: Output recommends follow-on skills for any flagged signals — `/investigator:identity-verification` and `/investigator:entity-footprint` — not met: the skill contains no cross-skill referrals anywhere. There is no mechanism in the definition to recommend adjacent skills when signals emerge

## Notes

The skill is well-structured and covers AU-specific sources (ASIC Connect, ABN Lookup) as the primary path, which is appropriate for the scenario. The output template maps closely to what the test expects across both criteria sections.

The follow-on skill cross-referral gap is the only structural omission worth flagging. A producing analyst following this skill to the letter would complete the investigation without being pointed to `/investigator:identity-verification` or `/investigator:entity-footprint` even when signals warrant them.

The subsidiary mapping section is slightly weaker for AU private Pty Ltd entities — it leans on ASIC corporate group searches, which have limited practical coverage for unlisted private companies. The AU path could usefully mention ASIC-registered charges (which can reveal group financing relationships) or court records. This doesn't fail any criterion but is a real-world limitation.
