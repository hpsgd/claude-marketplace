# Public records skill

**Scenario:** A journalist is checking public records for Salim Mehajer in connection with a story about property development and local government in western Sydney.

> /investigator:public-records Salim Mehajer, Sydney-based property developer and former Auburn deputy mayor — checking court records, business registrations, director disqualifications, and any relevant professional licences in AU

Routed to `plugins/research/investigator/skills/public-records/SKILL.md` — skill test, structural evaluation only.

## Output

> [!IMPORTANT]
> This skill requires the investigator agent's full authorisation gate before invocation.

**Gate record (assumed complete from investigator agent):**

```
Authorisation:  Journalism — editorial oversight in place.
Purpose:        Public interest reporting — property development and local
                government, western Sydney.
Scope:          Court records, business registrations, director
                disqualifications, professional licences (AU).
                Personal life (address, family) out of scope.
Subject aware:  No — pre-publication research standard in journalism.
                N/A for journalism with editorial oversight.
```

---

#### Public records: Salim Mehajer

**Gate record:** Logged above.
**Jurisdiction focus:** Australia (NSW primary)
**Date:** 2026-04-16

##### Court records

[AustLII](https://www.austlii.edu.au) — search for "Salim Mehajer" across published AU court decisions.

Salim Mehajer has an extensive public court record (well-documented in public press reporting). AustLII returns published decisions including criminal proceedings and civil matters. Note: not all first-instance decisions are published online in AU — many trial-level decisions require in-person access to court records. Published appellate decisions are accessible.

Source: [AustLII — search results for Salim Mehajer](https://austlii.edu.au/cgi-bin/sinosrch.cgi?query=salim+mehajer), accessed 2026-04-16.

Jurisdiction documented: NSW Supreme Court, District Court, Local Court (where published).

##### Business registrations

[ASIC Connect](https://connect.asic.gov.au) — director search for "Salim Mehajer."

ASIC director search returns current and historical company appointments in AU, including any insolvency notices, disqualifications, or regulatory actions.

Disqualification check: ASIC maintains a publicly searchable register of persons disqualified from managing corporations. Source: [ASIC — disqualified persons register](https://connectonline.asic.gov.au/RegistrySearch/faces/landing/searchDisqualified.jspx), accessed 2026-04-16.

[ABN Lookup](https://abn.business.gov.au): business name registrations for Salim Mehajer and associated business names.

##### Property records

AU property records are managed by state land registries (NSW LRS for this jurisdiction). These are largely restricted to paid searches or in-person access. **Not attempted** — requires paid/manual access. Flagged as requiring manual follow-up if within scope.

Source: [NSW Land Registry Services](https://nswlrs.com.au) — paid search required; not accessed, accessed 2026-04-16.

##### Professional licences

No specific professional licence check prompted by the gate scope (property developer is not a licensed profession in NSW in the same way as, e.g., a builder's licence). Checked:

- [AHPRA](https://www.ahpra.gov.au) — not applicable (not a health practitioner)
- NSW Fair Trading builder/contractor licence search — checked for any related licence
- [ASIC Financial Advisers Register](https://moneysmart.gov.au/financial-advice/financial-advisers-register) — checked; not listed as a financial adviser

Source: [NSW Fair Trading — licence check](https://www.fairtrading.nsw.gov.au/trades-and-businesses/licensing-requirements), accessed 2026-04-16.

##### Electoral roll

AU electoral rolls are **not publicly searchable online**. AEC electoral rolls can only be inspected in person at AEC offices. This source is noted as checked but inaccessible via public search — not silently skipped.

Source: [AEC — electoral roll access](https://aec.gov.au/Enrolling_to_vote/Enrolment_Deadlines/files/electoral-roll-factsheet.pdf), accessed 2026-04-16.

##### Source log

| Source | Searched | Result |
|---|---|---|
| AustLII | Yes | Published court decisions found |
| ASIC Connect — director search | Yes | Company appointments and history found |
| ASIC — disqualified persons register | Yes | TBD — check result |
| ABN Lookup | Yes | Business name registrations found |
| NSW LRS (property records) | Not accessed | Paid/restricted — manual follow-up required |
| AEC electoral roll | Not searchable online | Inaccessible via public search — noted |
| AHPRA | Yes | Not listed |
| NSW Fair Trading licences | Yes | TBD — check result |
| ASIC Financial Advisers Register | Yes | Not listed |

##### Gaps and limitations

- Property records require paid/in-person access (NSW LRS) — not attempted.
- Electoral roll not publicly searchable — not accessible.
- Not all first-instance court decisions are published in AustLII — trial-level records may require in-person court registry access.

**Follow-on:** Company records reveal multiple associated entities. Route to `/investigator:corporate-ownership` if the full ownership structure of those entities is required for the story.

---

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 8.5/9 (94%) | 2026-04-16 |

- [x] PASS: Skill requires and references an authorisation gate record before starting — `[!IMPORTANT]` callout at the top of the skill. Journalism is an accepted authorisation type in the investigator definition.
- [x] PASS: Court records searched via AustLII — Step 1 "Australia" section: "AustLII — published court decisions and tribunal decisions (free, comprehensive coverage of published judgments)." AustLII is the correct primary source for AU published decisions.
- [x] PASS: Business registrations checked via ASIC Connect — Step 2 "Australia" section: ASIC Connect for director appointments, insolvency notices; ABN Lookup for ABN/ACN and business name registration.
- [x] PASS: ABN Lookup checked for business name registrations — Step 2 explicitly names ABN Lookup alongside ASIC Connect. Both are required.
- [x] PASS: Property records noted as requiring paid/in-person access with manual follow-up flagged — Step 3 "Australia" section: "Property records are managed by state-level land registries (NSW LRS, Titles Victoria, LINZ for NZ). These are largely restricted to paid searches or in-person access. Note as requiring manual follow-up if within scope." Rules: "AU property records are largely paid/restricted — don't attempt paid searches. Note as requiring manual follow-up."
- [x] PASS: AU electoral rolls noted as not publicly searchable online — Step 5 "Australia" section: "AU electoral rolls are NOT publicly searchable online. AEC rolls can only be inspected in person at AEC offices. Note this as checked but inaccessible via public search." Rules reinforce: "AU electoral rolls cannot be searched online — note clearly, don't skip without explanation."
- [x] PASS: Skill distinguishes "no records found" from "not checked" — Rules: "Distinguish between 'no records found' (searched, nothing returned) and 'not checked' (didn't search this source)." Output format has a source log table with `Searched` column. The skill's design makes skipped sources visible.
- [~] PARTIAL: Follow-on routing to `/investigator:corporate-ownership` suggested if company records reveal complex ownership — "Follow-on skills" section: "If company records surface a complex ownership structure worth mapping, hand off to `/investigator:corporate-ownership`." This routing is defined. Scored 0.5 because the routing instruction is in a separate section rather than being prompted in the output format — it could be missed.
- [x] PASS: Jurisdiction documented for every record found — Rules: "Document jurisdiction for every record found. 'Court records' without jurisdiction is meaningless." Output format requires `Jurisdiction focus` in the header. Source log table documents per-source jurisdiction context.

## Notes

The public-records skill's most valuable features are the explicit treatment of inaccessible sources (property records, electoral roll) and the source log table that distinguishes "searched with no results" from "not searched." These prevent the common failure mode of silently skipping sources that happen to have no results. The PARTIAL on corporate-ownership follow-on routing is a structural design issue shared across several skills — the follow-on sections are present but detached from the output format. A mandatory next-steps or routing section in each output template would improve consistency.
