# Public Records

Scenario: A journalist is checking public records for Salim Mehajer in connection with a story about property development and local government in western Sydney.

## Prompt

> /investigator:public-records Salim Mehajer, Sydney-based property developer and former Auburn deputy mayor — checking court records, business registrations, director disqualifications, and any relevant professional licences in AU

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

### Public records: Salim Mehajer

**Gate record:** Public figure — former Auburn City Council deputy mayor, property developer. Extensive public court record and media coverage.
**Jurisdiction focus:** AU (NSW primary)
**Date:** 2026-05-01

---

#### Court records

> **Note on AustLII access:** AustLII returned HTTP 403 on automated requests. Cases below are confirmed via ASIC media releases, CDPP publications, Federal Court secondary analysis, and cross-referenced sources. Full judgment text for all decisions requires manual AustLII/NSW Caselaw retrieval.

**Federal Court**
- *Mehajer v Weston* [2019] FCA 1713 — Bankruptcy annulment application dismissed. Justice Lee found Mehajer "hopelessly insolvent" with ~$24 million in total debts, including ~$8.6 million to the ATO.

**NSW Court of Criminal Appeal**
- *Mehajer v R* [2024] NSWCCA 226 (Kirk JA, Rothman J, Yehia J) — Bail application dismissed pending appeal; court found assertions of innocence lacked detail.
- *Mehajer v R* [2026] NSWCCA 14 — Court of Criminal Appeal granted leave to appeal. Confirmed via NSW Supreme Court announcement. Full orders not yet accessible in open sources; requires manual follow-up.

**NSW Supreme Court**
- *R v Mehajer* [2018] NSWSC 1687 (cited in secondary sources) — Bail refusal; justice found Mehajer showed "an arrogant disregard for the law."
- **Vexatious litigant declaration**, 27 May 2022, Justice Lindsay — Court found Mehajer "intended to, and did indeed, harass and annoy his opponents." Stayed his $52 million claim against 17 defendants (Lidcombe development dispute). Prohibited from commencing further NSW civil proceedings without leave. Neutral citation not confirmed from primary source; verify at NSW Supreme Court vexatious proceedings register.

**NSW District / Local Court (criminal)**

| Matter | Court | Year | Outcome |
|---|---|---|---|
| Electoral fraud (77 offences) — joint enterprise with sister Fatima to rig 2012 Auburn Council election via false AEC enrolment applications | Local Court (Mag. Schurr) | 2018 | Convicted; 21 months, NPP 11 months. CDPP prosecution. |
| Perverting the course of justice (×2) + perjury — false statements to secure relaxed 2017 bail conditions | District Court (Judge Zahra) | 2021 | Convicted; 3 years 6 months total |
| Domestic violence (intimidation, suffocation, assault ×3) + fraud (false docs to reclaim $6,530 seized by police) | District Court | 2023 | Convicted by jury; 7 years 9 months, NPP 3.5 years. Released on parole 18 July 2025 with conditions: DV programs, drug/alcohol testing, no contact with victim or OMCG members. |

**Minor matters (plea/conviction confirmed; no published citation):**
- Star Casino assault (2017): guilty plea; $600+ compensation, 3-year good behaviour bond
- Journalist assault (2017): guilty (2018); conviction without penalty
- Ex-wife intimidation via 400+ messages (2018): guilty; 18-month good behaviour bond
- Drug possession — Endone, Xanax (2020): guilty; 12-month conditional release order

---

#### Business registrations

**ABN Lookup (confirmed):**
- ABN 50 388 412 508 — Sole trader: MEHAJER, SALIM (NSW 2141), active from 15 June 2015. Business name: **SM Engineering & Constructions**, registered 27 March 2008.

**ASIC-confirmed companies (via ASIC media releases and court records):**

| Company | Role | Outcome |
|---|---|---|
| SM Property Development Pty Ltd (ACN 130 968 811) | Director/controller | Liquidated; ~$886,701 owed to ATO |
| SM Engineering and Constructions Pty Ltd (ACN 132 853 153) | Director | Wound up; ~$159,206 owed to ATO |
| Sydney Project Group Pty Ltd | Sole shareholder; director 2012–2013, 2014–2015 | Failed; Lidcombe Skypoint Towers project; combined SPG/SET debts >$7 million |
| S.E.T Services Pty Ltd | Sole shareholder; director 2014–2015 | Failed; see above |

**ASIC director disqualification:**
- **5 November 2015**: ASIC disqualified under s.206F Corporations Act for **3 years** (to 5 November 2018). Findings: failed to maintain adequate financial records; ATO debts ~$1.045 million; failed to lodge returns; collected $315,192 GST and failed to remit.
- **19 August 2016**: AAT affirmed disqualification on review. Found management "fell far short of what is reasonably expected of a director" and showed "a cavalier approach."
- Three-year period expired 5 November 2018. No further confirmed ASIC disqualification identified from primary sources — check ASIC Banned and Disqualified register at data.gov.au for current status.

**Bankruptcy:**
- Declared bankrupt 20 March 2018. Annulment rejected ([2019] FCA 1713). Standard 3-year period would have concluded ~March 2021, unless extended by trustee. Current discharge status unconfirmed — requires AFSA NPII search.

---

#### Property records

NSW LRS title searches are a paid service, not publicly queryable. Mehajer's declared bankruptcy (March 2018) would have passed property held at that time to trustee Weston. His publicised portfolio (Million Dollar Point house, Lidcombe townhouses, Skypoint Towers development) is documented in media but title history requires a paid NSW LRS search. **Flagged for paid manual follow-up.**

---

#### Professional licences

- **NSW Fair Trading licence register**: Portal requires a JavaScript-rendered browser session; not accessible via automated fetch. No public media identifies a current or historical building/contractor licence in Mehajer's personal name. Recommend manual check at verify.licence.nsw.gov.au — the register shows current, expired, and cancelled licences under the *Home Building Act 1989*.
- **ASIC Financial Advisers Register**: Inaccessible via automated fetch. No evidence in any source of a financial adviser registration. Consistent with his profile; finding: no evidence of any registration.

---

#### Electoral roll

AEC electoral rolls are not publicly searchable online. Roll status cannot be ascertained through open sources. Not applicable to this records check.

---

#### Source log

| Source | Searched | Result |
|---|---|---|
| AustLII | Yes — HTTP 403 blocked | Cases identified via secondary/cross-referenced sources; manual follow-up required |
| NSW Caselaw | Yes — JS-rendered, inaccessible | Manual browser search required |
| Federal Court (via secondary) | Yes | *Mehajer v Weston* [2019] FCA 1713 confirmed |
| CDPP website | Yes | Electoral fraud sentencing confirmed |
| ASIC media releases | Yes — fetched directly | 16-290MR and 19-310MR confirmed |
| ABN Lookup | Yes — fetched directly | ABN 50 388 412 508 confirmed |
| ASIC Connect (director register) | Yes — JS-rendered, inaccessible | Manual search required for full directorship history |
| NSW Fair Trading licence register | Yes — JS-rendered, inaccessible | No personal licence found in public media |
| ASIC Financial Advisers Register | Yes — JS-rendered, inaccessible | No evidence of registration in any source |
| AFSA (bankruptcy/NPII) | Not searched directly | Bankruptcy confirmed via FCA; discharge status unconfirmed |
| AEC electoral roll | Not applicable | Not publicly searchable online in AU |

---

#### Gaps and limitations

1. **AustLII full search** — blocked (HTTP 403). Manual search at austlii.edu.au or caselaw.nsw.gov.au required to retrieve full list of published decisions, including NCAT/tribunal matters and all bail decisions.

2. **Mehajer v R [2026] NSWCCA 14** — confirmed decided but full orders/judgment text not yet in open sources. Retrieve from NSW Caselaw once indexed.

3. **ASIC Banned and Disqualified register — current status** — the confirmed 2015–2018 disqualification has expired. Whether any subsequent disqualification was imposed is unconfirmed. Check ASIC's downloadable dataset at data.gov.au or the ASIC Connect banned register.

4. **ASIC Connect — full directorship history** — JS-rendered portal. ACN numbers for Sydney Project Group and S.E.T Services not confirmed. Complete entity list requires manual ASIC Connect search or paid company extract.

5. **NSW Fair Trading licence register** — requires manual browser session at verify.licence.nsw.gov.au. Recommended given property developer profile.

6. **NSW LRS property records** — paid service. Post-bankruptcy property position unclear. Manual paid search recommended.

7. **AFSA NPII (bankruptcy discharge status)** — standard 3-year period from March 2018 would have concluded ~March 2021. Whether extended or objections lodged is unconfirmed. Search AFSA NPII for current status.

8. **Vexatious litigant order (May 2022)** — neutral citation not confirmed from primary source. Verify at NSW Supreme Court vexatious proceedings register: supremecourt.nsw.gov.au/practice-procedure/vexatious-proceedings.html

9. **Local Court criminal matters** — not systematically published on AustLII. The minor matters listed above are confirmed via media but this list is not exhaustive of all proceedings.

---

*Sources: ASIC media releases 16-290MR and 19-310MR; CDPP sentencing announcement; ABN Lookup ABN 50 388 412 508; Mehajer v Weston [2019] FCA 1713; [2024] NSWCCA 226; [2026] NSWCCA 14 (NSW Supreme Court announcement); Wikipedia (cross-referenced); McCabes Lawyers; Coutts Legal; Government News; SBS News.*

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/18.0 (94%) |
| Evaluated | 2026-05-01 |
| Target duration | 527731 ms |
| Target cost | $1.7978 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires and references an authorisation gate record before starting | PASS | Output opens with '**Gate record:** Public figure — former Auburn City Council deputy mayor, property developer. Extensive public court record and media coverage.' — explicitly labelled gate record at the top before any findings. |
| c2 | Court records are searched via AustLII for published decisions involving the subject as plaintiff, defendant, or party | PASS | Source log entry: 'AustLII — Yes — HTTP 403 blocked — Cases identified via secondary/cross-referenced sources; manual follow-up required.' Attempt documented; note on access failure with alternative sourcing explained. |
| c3 | Business registrations are checked via ASIC Connect for current and historical director appointments and any insolvency notices | PASS | Source log: 'ASIC Connect (director register) — Yes — JS-rendered, inaccessible.' Company table lists four entities with roles (director/shareholder) and outcomes (Liquidated, Wound up). ASIC disqualification s.206F detailed. Insolvency notices (ATO debts, wind-up outcomes) present. |
| c4 | ABN Lookup is checked for business name registrations | PASS | Source log: 'ABN Lookup — Yes — fetched directly.' Output confirms 'ABN 50 388 412 508 — Sole trader: MEHAJER, SALIM (NSW 2141), active from 15 June 2015. Business name: SM Engineering & Constructions, registered 27 March 2008.' |
| c5 | Property records are noted as requiring paid/in-person access in AU — skill does not attempt paid searches and flags this clearly as requiring manual follow-up | PASS | 'NSW LRS title searches are a paid service, not publicly queryable... **Flagged for paid manual follow-up.**' Also listed in Gaps section item 6: 'NSW LRS property records — paid service. Manual paid search recommended.' |
| c6 | AU electoral rolls are noted as not publicly searchable online — this is stated explicitly, not silently skipped | PASS | 'AEC electoral rolls are not publicly searchable online. Roll status cannot be ascertained through open sources. Not applicable to this records check.' Source log also shows 'AEC electoral roll — Not applicable — Not publicly searchable online in AU.' |
| c7 | Skill distinguishes between 'no records found' (searched, nothing returned) and 'not checked' (didn't search this source) — source log table documents both | PASS | Source log table explicitly differentiates: 'Yes — fetched directly' (searched, returned data), 'Yes — HTTP 403 blocked' / 'Yes — JS-rendered, inaccessible' (searched, could not retrieve), 'Not searched directly' for AFSA, and 'Not applicable' for AEC — all distinct states. |
| c8 | Follow-on routing to `/investigator:corporate-ownership` is suggested if company records reveal a complex ownership structure | FAIL | No mention of `/investigator:corporate-ownership` anywhere in the output. The gaps and limitations section and conclusion contain no skill routing recommendations despite the complex multi-entity structure surfaced by ASIC findings. |
| c9 | Jurisdiction is documented for every record found | PASS | Court records are grouped by jurisdiction: 'Federal Court', 'NSW Court of Criminal Appeal', 'NSW Supreme Court', 'NSW District / Local Court (criminal)'. Electoral fraud noted as 'CDPP prosecution' (Commonwealth). ASIC disqualification is Commonwealth (Corporations Act s.206F). |
| c10 | Output's gate record at the top references journalism authorisation — public-interest reporting on a public figure / former local government official, professional / civic-record scope | PASS | Gate record: 'Public figure — former Auburn City Council deputy mayor, property developer. Extensive public court record and media coverage.' Establishes public figure / former local government official status as authorisation basis; civic-record scope confirmed. |
| c11 | Output's court records search uses AustLII (austlii.edu.au) for published decisions — returns specific case names, court (NSW Supreme Court / Federal Court / etc.), dates, and the role of the subject in each (plaintiff / defendant / appellant) | PASS | Specific citations: '*Mehajer v Weston* [2019] FCA 1713' (Federal Court, appellant); '*Mehajer v R* [2024] NSWCCA 226' (NSWCCA, appellant); '*R v Mehajer* [2018] NSWSC 1687' (NSW Supreme Court, defendant). Courts, years, roles all documented. |
| c12 | Output's ASIC Connect search returns directorships — current and historical, with appointment dates and the entities involved — and any insolvency / external administration notices | PASS | Company table shows entities (SM Property Development, SM Engineering, Sydney Project Group, S.E.T Services) with role (Director, Sole shareholder) and date ranges (e.g., '2012–2013, 2014–2015'). Outcomes include 'Liquidated', 'Wound up', ATO debts quantified. Sourced via ASIC media releases when Connect was inaccessible. |
| c13 | Output's ABN Lookup returns business name registrations — with the ABN, registered status, and any historical name changes | PASS | 'ABN 50 388 412 508 — Sole trader: MEHAJER, SALIM (NSW 2141), active from 15 June 2015. Business name: SM Engineering & Constructions, registered 27 March 2008.' ABN, registered status ('active'), and registration date all present. |
| c14 | Output addresses property records explicitly — flagging that AU Land Registry searches (NSW Land Registry Services) require paid / in-person access; the skill does NOT attempt unauthorised access to those records and clearly notes this as a manual follow-up step | PASS | 'NSW LRS title searches are a paid service, not publicly queryable... Flagged for paid manual follow-up.' Gap item 6 repeats: 'NSW LRS property records — paid service... Manual paid search recommended.' No attempt to access paid records. |
| c15 | Output addresses AU electoral rolls — the AEC publishes the electoral roll only at libraries / for permitted users; not searchable online by the public; this is stated explicitly rather than silently skipped | PASS | 'AEC electoral rolls are not publicly searchable online. Roll status cannot be ascertained through open sources.' Dedicated Electoral roll section present; not silently omitted. |
| c16 | Output's source log distinguishes 'no records found' (the search ran, returned nothing) from 'not checked' (didn't search this source) — never collapsing absence-of-evidence with absence-of-search | PASS | Source log uses distinct status descriptors: 'Yes — fetched directly' (success), 'Yes — HTTP 403 blocked' (searched, failed), 'Yes — JS-rendered, inaccessible' (searched, inaccessible), 'Not searched directly' (AFSA), 'Not applicable' (AEC). Each state is labelled separately. |
| c17 | Output documents jurisdiction per finding — NSW vs Federal vs Commonwealth — for every court case and registration | PASS | Court findings grouped by Federal Court / NSWCCA / NSW Supreme Court / NSW District/Local Court. Electoral fraud described as 'CDPP prosecution' (Commonwealth). ASIC disqualification under 'Corporations Act' (Commonwealth). Bankruptcy under Federal Court. All findings jurisdiction-tagged. |
| c18 | Output handles that Salim Mehajer is a public figure with extensive media coverage — the public-records search complements but doesn't replace media archive search; output notes the major media-reported cases but does NOT replace them with primary-record retrieval beyond AustLII | PASS | Gate record flags 'Extensive public court record and media coverage.' Sources cite Wikipedia, SBS News, Government News as cross-references, not primary records. Minor matters are 'confirmed via media but this list is not exhaustive.' Media-reported cases supplement rather than replace primary-record retrieval. |
| c19 | Output recommends follow-on routing — `/investigator:corporate-ownership` for any complex group structure surfaced through ASIC findings, `/analyst:source-credibility` if the user is citing media reports of cases that aren't in AustLII | FAIL | Neither `/investigator:corporate-ownership` nor `/analyst:source-credibility` appears anywhere in the output. The gaps section lists manual follow-up actions for humans but contains zero skill routing recommendations. |

### Notes

The output is exceptionally thorough and well-structured, passing 17 of 17 PASS-ceiling criteria. It correctly handles AustLII access failure by documenting the attempt and sourcing from ASIC media releases/secondary court documents; it clearly labels property records and electoral rolls as requiring paid/manual access; and its source log table meaningfully distinguishes searched-but-blocked from not-searched-at-all. The two failures are both on PARTIAL-ceiling criteria (c8, c19) — neither `/investigator:corporate-ownership` nor `/analyst:source-credibility` skill routing is suggested anywhere in the output, despite a complex multi-entity corporate structure being surfaced and multiple findings coming from media rather than AustLII primary sources. These omissions cost only 1.0 point from the maximum of 18.0, yielding 94.4%.
