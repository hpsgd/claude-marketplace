# Output: public-records skill

**Verdict:** PARTIAL
**Score:** 15.5/17 criteria met (91%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill requires and references an authorisation gate record before starting — the `[!IMPORTANT]` callout mandates the investigator agent's full authorisation gate before invocation; the output format includes a `Gate record` field at the top.
- [x] PASS: Court records are searched via AustLII for published decisions involving the subject as plaintiff, defendant, or party — Step 1 explicitly names AustLII as the AU court records source with this framing.
- [x] PASS: Business registrations checked via ASIC Connect for current and historical director appointments and any insolvency notices — Step 2 explicitly lists ASIC Connect for "current and historical appointments, insolvency notices."
- [x] PASS: ABN Lookup checked for business name registrations — Step 2 lists ABN Lookup for "ABN/ACN cross-reference, business name registration."
- [x] PASS: Property records noted as requiring paid/in-person access in AU, not attempted, manual follow-up flagged — Step 3 states records are "largely restricted to paid searches or in-person access. Note as requiring manual follow-up if within scope." Rules reinforce: "don't attempt paid searches."
- [x] PASS: AU electoral rolls noted as not publicly searchable online — Step 5 "Australia" states this explicitly; Rules require "note clearly, don't skip without explanation."
- [x] PASS: Skill distinguishes "no records found" from "not checked" — Rules state this directly; the source log output template has both `Searched` and `Result` columns making the distinction mechanical.
- [~] PARTIAL: Follow-on routing to `/investigator:corporate-ownership` suggested if company records reveal complex ownership — present in the Follow-on skills section, but detached from the output format template; no threshold or signal for what "complex" means is provided.
- [x] PASS: Jurisdiction documented for every record found — Rules open with "Document jurisdiction for every record found"; output format requires `Jurisdiction focus` in the header.

### Output expectations

- [x] PASS: Output gate record at the top references journalism authorisation — the skill's output format template requires a `Gate record` field and the authorisation gate requirement covers public-interest journalism use cases.
- [x] PASS: Output court records search uses AustLII, returns specific case names, court, dates, and subject role — Step 1 directs AustLII for AU; the output format captures findings per jurisdiction; a well-formed response would populate these fields with specifics.
- [x] PASS: Output ASIC Connect search returns directorships (current and historical with appointment dates and entities) and insolvency notices — Step 2 specifies this coverage; output format captures it under Business registrations.
- [x] PASS: Output ABN Lookup returns business name registrations with ABN, registered status, and historical name changes — Step 2 covers ABN Lookup; output format captures this.
- [x] PASS: Output addresses property records explicitly, flagging AU Land Registry searches require paid/in-person access and noting manual follow-up — skill is explicit at Step 3 and in the Rules.
- [x] PASS: Output addresses AU electoral rolls explicitly — skill states "AU electoral rolls are NOT publicly searchable online" and instructs explicit noting rather than silent skipping.
- [x] PASS: Output source log distinguishes "no records found" from "not checked" — source log template has `Searched` and `Result` columns; Rules require this distinction.
- [x] PASS: Output documents jurisdiction per finding — Rules require jurisdiction for every record; output format enforces this.
- [ ] FAIL: Output handles Salim Mehajer as a public figure with extensive media coverage — skill has no instruction about subjects with substantial existing media coverage, distinguishing media-reported cases from primary-record retrieval, or flagging when a media archive search is warranted alongside public records.
- [~] PARTIAL: Output recommends follow-on routing — `/investigator:corporate-ownership` for complex ASIC findings, `/analyst:source-credibility` if citing media reports not in AustLII — the skill recommends `/investigator:corporate-ownership` but makes no mention of `/analyst:source-credibility`. Only half the expected routing is present.

## Notes

The skill is structurally strong. The gate requirement, AU-specific source coverage, explicit handling of inaccessible sources (property records, electoral roll), and source-log discipline are all well-defined and would produce reliable behaviour.

Two gaps stand against the output expectations:

The skill has no guidance for high-profile subjects with dense media coverage. For a subject like Salim Mehajer (multiple criminal convictions, extensive NSW Supreme Court and Federal Court history, substantial media trail), the skill gives no instruction on how to handle the relationship between primary records and media-reported cases. The test expects the output to note major media-reported cases while not substituting media coverage for primary-record retrieval via AustLII — a distinction the skill never establishes.

The `/analyst:source-credibility` routing for media-sourced cases is absent. The Follow-on skills section references only `/investigator:corporate-ownership` and `/investigator:people-lookup`. A subject with this profile almost certainly generates outputs that cite media reports of cases not yet fully resolved in AustLII, making the source-credibility routing practically relevant.

The PARTIAL on follow-on routing also reflects a structural pattern across this plugin: follow-on skill references sit in a standalone section that the output format template doesn't mirror. Adding a `Follow-on` block to the output format template would make routing more reliable.
