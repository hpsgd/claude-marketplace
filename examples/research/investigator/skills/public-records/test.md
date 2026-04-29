# Test: public-records skill

Scenario: A journalist is checking public records for Salim Mehajer in connection with a story about property development and local government in western Sydney.

## Prompt

/investigator:public-records Salim Mehajer, Sydney-based property developer and former Auburn deputy mayor — checking court records, business registrations, director disqualifications, and any relevant professional licences in AU

## Criteria

- [ ] PASS: Skill requires and references an authorisation gate record before starting
- [ ] PASS: Court records are searched via AustLII for published decisions involving the subject as plaintiff, defendant, or party
- [ ] PASS: Business registrations are checked via ASIC Connect for current and historical director appointments and any insolvency notices
- [ ] PASS: ABN Lookup is checked for business name registrations
- [ ] PASS: Property records are noted as requiring paid/in-person access in AU — skill does not attempt paid searches and flags this clearly as requiring manual follow-up
- [ ] PASS: AU electoral rolls are noted as not publicly searchable online — this is stated explicitly, not silently skipped
- [ ] PASS: Skill distinguishes between "no records found" (searched, nothing returned) and "not checked" (didn't search this source) — source log table documents both
- [ ] PARTIAL: Follow-on routing to `/investigator:corporate-ownership` is suggested if company records reveal a complex ownership structure
- [ ] PASS: Jurisdiction is documented for every record found

## Output expectations

- [ ] PASS: Output's gate record at the top references journalism authorisation — public-interest reporting on a public figure / former local government official, professional / civic-record scope
- [ ] PASS: Output's court records search uses AustLII (austlii.edu.au) for published decisions — returns specific case names, court (NSW Supreme Court / Federal Court / etc.), dates, and the role of the subject in each (plaintiff / defendant / appellant)
- [ ] PASS: Output's ASIC Connect search returns directorships — current and historical, with appointment dates and the entities involved — and any insolvency / external administration notices
- [ ] PASS: Output's ABN Lookup returns business name registrations — with the ABN, registered status, and any historical name changes
- [ ] PASS: Output addresses property records explicitly — flagging that AU Land Registry searches (NSW Land Registry Services) require paid / in-person access; the skill does NOT attempt unauthorised access to those records and clearly notes this as a manual follow-up step
- [ ] PASS: Output addresses AU electoral rolls — the AEC publishes the electoral roll only at libraries / for permitted users; not searchable online by the public; this is stated explicitly rather than silently skipped
- [ ] PASS: Output's source log distinguishes "no records found" (the search ran, returned nothing) from "not checked" (didn't search this source) — never collapsing absence-of-evidence with absence-of-search
- [ ] PASS: Output documents jurisdiction per finding — NSW vs Federal vs Commonwealth — for every court case and registration
- [ ] PASS: Output handles that Salim Mehajer is a public figure with extensive media coverage — the public-records search complements but doesn't replace media archive search; output notes the major media-reported cases but does NOT replace them with primary-record retrieval beyond AustLII
- [ ] PARTIAL: Output recommends follow-on routing — `/investigator:corporate-ownership` for any complex group structure surfaced through ASIC findings, `/analyst:source-credibility` if the user is citing media reports of cases that aren't in AustLII
