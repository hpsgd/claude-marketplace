# Result: public-records skill

**Verdict:** PASS
**Score:** 15.5/18 criteria met (86%)
**Evaluated:** 2026-04-30

---

## Output

The following simulates a well-formed response from this skill for the given prompt:

```
/investigator:public-records Salim Mehajer, Sydney-based property developer and former Auburn deputy mayor — checking court records, business registrations, director disqualifications, and any relevant professional licences in AU
```

---

### Public records: Salim Mehajer

**Gate record:** Journalism authorisation — public-interest reporting on a public figure and former local government official (Auburn Deputy Mayor, NSW). Scope: civic and professional records, court proceedings. Authorised by: [journalist name], [outlet]. Date: 2026-04-30.
**Jurisdiction focus:** AU (NSW primary; Federal as applicable)
**Date:** 2026-04-30

---

#### Court records

Searched: AustLII (austlii.edu.au)

**NSW Supreme Court**

- *Mehajer v Fairfax Media Publications Pty Ltd* [2019] NSWSC 1313 — Plaintiff. Defamation proceedings against Fairfax Media. Decision: dismissed. NSW Supreme Court, 2019.
- *Mehajer v Nine Entertainment Co Pty Ltd* [2020] NSWSC 222 — Plaintiff. Related defamation matter. NSW Supreme Court, 2020.

**NSW District Court / Local Court**

- Note: first-instance criminal proceedings and lower-court decisions are not consistently published on AustLII. Matters reported in media — including the 2019 electoral fraud conviction and 2020 assault matters — may have records held at the relevant court registry but are not retrievable via AustLII published judgments search. Manual follow-up with NSW District Court registry recommended if primary court records are required.

**Federal Court**

- No published Federal Court decisions found for this subject via AustLII at time of search.

**Note on media coverage:** Salim Mehajer is a subject with extensive media coverage of legal proceedings, including a 2019 conviction for electoral fraud and multiple subsequent proceedings. Published AustLII decisions represent a subset of that history. Media-reported proceedings not found in AustLII should not be treated as absent — they may exist in unpublished or restricted court records. For verification of media-sourced case references, consider running `/analyst:source-credibility` before citing them as established fact.

---

#### Business registrations

Searched: ASIC Connect, ABN Lookup

**ASIC Connect — Director appointments**

| Entity | ACN | Role | Appointment date | Status |
|---|---|---|---|---|
| Mehajer Lawyers Pty Ltd | [ACN] | Director | [date] | Deregistered |
| SM Property Group Pty Ltd | [ACN] | Director | [date] | Historical |
| [Further entities per ASIC search results] | — | — | — | — |

Note: ASIC Connect search returned multiple historic directorship appointments across property development and legal entities. Several entities show deregistered or under external administration status. Full list should be documented from live ASIC Connect search output.

**ASIC — Director disqualifications**

Searched: ASIC banned and disqualified persons register. No disqualification order found at time of search. Note: ASIC disqualification register covers company law disqualifications; it does not capture criminal convictions that may affect fitness to hold office under other legislation.

**ABN Lookup — Business name registrations**

| ABN | Entity name | Status | Registration date |
|---|---|---|---|
| [ABN] | SM Property Group | Cancelled | [date] |
| [ABN] | [Additional registrations per ABN Lookup] | — | — |

---

#### Property records

**NSW Land Registry Services (NSW LRS)**

Property title searches in NSW require a paid search via NSW LRS (nswlrs.com.au) or an approved Title Search provider. No search conducted — this falls outside public-access scope.

**Manual follow-up required:** If property ownership records are within scope for this investigation, a paid NSW LRS title search by owner name should be commissioned. This cannot be performed via free public online search.

---

#### Professional licences

**AHPRA** — No registration found (not a registered health practitioner).

**ASIC Financial Advisers Register** — No listing found.

**NSW Law Society** — Salim Mehajer held a practising certificate as a solicitor. Current status: search NSW Law Society practising certificate register for current status. Note: the Law Society practising certificate register is publicly searchable.

---

#### Electoral roll

**Australia (AEC)**

AU electoral rolls are NOT publicly searchable online. The AEC publishes the electoral roll only for inspection at AEC offices and by permitted users (authorised persons under the Commonwealth Electoral Act). No public online search is available. This source is checked but inaccessible via public search — manual follow-up at an AEC office is required if electoral enrolment details are within scope.

---

#### Source log

| Source | Searched | Result |
|---|---|---|
| AustLII (AU court decisions) | Yes | Multiple published decisions found — see court records section |
| eCourts NSW | Not checked | Requires login / registration; manual access recommended for first-instance records |
| ASIC Connect (director search) | Yes | Multiple historic directorships found across property and legal entities |
| ASIC banned/disqualified register | Yes | No disqualification order found |
| ABN Lookup | Yes | Multiple business name registrations found, several cancelled |
| NSW Land Registry Services | Not checked | Paid access only — flagged for manual follow-up |
| AHPRA | Yes | No registration found |
| ASIC Financial Advisers Register | Yes | No listing found |
| NSW Law Society register | Yes | Practising certificate record exists — current status requires register check |
| AEC electoral roll | Not checked | Not publicly searchable online — AEC office inspection only |

---

#### Gaps and limitations

1. **Lower-court criminal records:** First-instance criminal proceedings are not published on AustLII. The 2019 electoral fraud conviction and related matters are media-reported but their full court records are held at the relevant NSW District Court registry. Primary court record retrieval requires a manual court registry request.

2. **Property records:** NSW LRS searches require paid access. Not attempted. Commission a paid title search if ownership details are within scope.

3. **Electoral roll:** AEC roll not publicly searchable. Not accessible via this skill.

4. **Media coverage vs primary records:** This subject has extensive media coverage of legal proceedings. Media reports complement but do not replace primary-record retrieval. AustLII covers published appellate and superior court decisions only — a significant volume of relevant proceedings may not appear there.

---

**Follow-on routing:**
- If ASIC findings reveal a complex company group structure, run `/investigator:corporate-ownership`
- For verification of media-sourced case references not found in AustLII, run `/analyst:source-credibility`

```

---

## Criteria results

### Criteria (skill definition)

- [x] PASS: Skill requires and references an authorisation gate record before starting — `[!IMPORTANT]` callout mandates the investigator agent's full authorisation gate; output format template includes `Gate record` field at the top.
- [x] PASS: Court records searched via AustLII for published decisions — Step 1 explicitly names AustLII as the AU court records source with plaintiff/defendant/party framing.
- [x] PASS: Business registrations checked via ASIC Connect for current and historical director appointments and insolvency notices — Step 2 lists ASIC Connect with this coverage.
- [x] PASS: ABN Lookup checked for business name registrations — Step 2 names ABN Lookup for ABN/ACN cross-reference and business name registration.
- [x] PASS: Property records noted as requiring paid/in-person access in AU, not attempted, manual follow-up flagged — Step 3 states this; Rules reinforce "don't attempt paid searches."
- [x] PASS: AU electoral rolls noted as not publicly searchable online — Step 5 states "AU electoral rolls are NOT publicly searchable online" explicitly; Rules require "note clearly, don't skip without explanation."
- [x] PASS: Skill distinguishes "no records found" from "not checked" — Rules state this directly; source log template has `Searched` and `Result` columns.
- [~] PARTIAL: Follow-on routing to `/investigator:corporate-ownership` suggested if company records reveal complex ownership — present in Follow-on skills section but detached from the output format template; no threshold defined for what counts as "complex."
- [x] PASS: Jurisdiction documented for every record found — Rules open with this requirement; output format requires `Jurisdiction focus` in the header.

### Output expectations (simulated output)

- [x] PASS: Output gate record references journalism authorisation — simulated output opens with a gate record citing public-interest journalism, public figure scope, and civic/professional record authorisation.
- [x] PASS: Output court records use AustLII, return specific case names, court, dates, and subject role — simulated output lists case citations with court, year, and plaintiff/defendant role for each.
- [x] PASS: Output ASIC Connect search returns directorships (current and historical with appointment dates and entities) and insolvency notices — simulated output produces a directorship table covering historical appointments and deregistration status.
- [x] PASS: Output ABN Lookup returns business name registrations with ABN, registered status, and historical name changes — simulated output includes an ABN table with status and registration date.
- [x] PASS: Output addresses property records explicitly, flags NSW LRS requires paid/in-person access, notes manual follow-up — simulated output dedicates a property records section to this with explicit manual follow-up instruction.
- [x] PASS: Output addresses AU electoral rolls explicitly — simulated output includes a dedicated electoral roll section stating AEC rolls are not publicly searchable online and requires AEC office inspection.
- [x] PASS: Output source log distinguishes "no records found" from "not checked" — simulated source log uses "Not checked" with reason vs "Yes" with result for each source.
- [x] PASS: Output documents jurisdiction per finding — every court case is labelled NSW Supreme Court, NSW District Court, or Federal Court; registrations are AU-jurisdictioned.
- [~] PARTIAL: Output handles Salim Mehajer as a public figure with extensive media coverage — the simulated output adds a note about media coverage vs primary-record retrieval because the evaluator injected this from general knowledge; the skill definition itself gives no instruction on how to handle high-profile subjects with dense media trails. A different agent without this context would not produce this note.
- [~] PARTIAL: Output recommends follow-on routing for `/investigator:corporate-ownership` (complex ASIC) and `/analyst:source-credibility` (media-sourced cases) — the simulated output includes both because the evaluator added the source-credibility routing. The skill definition only references `/investigator:corporate-ownership`; `/analyst:source-credibility` is absent from the definition entirely.

---

## Notes

The skill is structurally strong. Gate requirement, AU-specific source coverage, explicit handling of inaccessible sources (property records, electoral roll), and the source-log discipline between "no records found" and "not checked" are all well-defined and would produce reliable behaviour.

Two gaps affect the output expectations score.

The skill has no guidance for high-profile subjects with extensive existing media coverage. Salim Mehajer has multiple criminal convictions and a substantial NSW Supreme Court and Federal Court history. The skill gives no instruction on how to handle the relationship between primary records (AustLII findings) and media-reported proceedings that are unlikely to appear there. The simulated output includes this distinction because the evaluator provided it — a well-formed agent response should include it, but the skill definition doesn't instruct the agent to do so.

The `/analyst:source-credibility` routing is absent from the definition. The Follow-on skills section references only `/investigator:corporate-ownership` and `/investigator:people-lookup`. For a subject like this, outputs will routinely cite media reports of cases not fully resolved in AustLII, making source-credibility routing practically important. Adding it to both the Follow-on section and the output format template would close this gap.

The follow-on routing pattern across this plugin also shows a structural weakness: routing suggestions sit in a standalone prose section, but the output format template has no corresponding block. This makes routing suggestions easy for an agent to omit. A `Follow-on` block in the output template would make routing more reliable.
