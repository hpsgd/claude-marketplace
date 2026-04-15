---
name: public-records
description: "Search public records for a named individual: court records, business registrations, property (where public), professional licences, and electoral roll. Full AU/NZ/UK/US source coverage. Requires authorisation gate."
argument-hint: "[person name, jurisdiction if known]"
user-invocable: true
allowed-tools: WebSearch, WebFetch
---

Search public records for $ARGUMENTS.

> [!IMPORTANT]
> This skill requires the investigator agent's full authorisation gate before invocation. Document the jurisdiction for every record found — public records laws vary significantly.

## Step 1: Court records

Search court records for filings involving the subject as plaintiff, defendant, or party.

**Australia:**

- [AustLII](https://www.austlii.edu.au) — published court decisions and tribunal decisions (free, comprehensive coverage of published judgments)
- eCourts (NSW), VCAT (VIC) — state portals for specific jurisdictions
- Note: not all court records are published online in AU — many first-instance decisions are not publicly accessible

**New Zealand:**

- [NZLII](https://www.nzlii.org) — published court decisions
- [NZ Courts](https://www.courtsofnz.govt.nz) — Supreme Court, Court of Appeal, High Court judgments
- Note: District Court decisions are less consistently published

**United States:**

- [CourtListener](https://www.courtlistener.com) — federal and state courts, free
- [PACER](https://pacer.uscourts.gov) — federal courts public search
- State court online portals (coverage varies by state)

**United Kingdom:**

- [The Gazette](https://www.thegazette.co.uk) — insolvency, bankruptcy, company winding-up notices
- BAILII for published judgments

## Step 2: Business registrations

Has the subject been registered as a director or officer of any company?

**Australia:**

- [ASIC Connect](https://connect.asic.gov.au) — director search across all Australian registered companies; includes current and historical appointments, insolvency notices
- [ABN Lookup](https://abn.business.gov.au) — ABN/ACN cross-reference, business name registration

**New Zealand:**

- [NZ Companies Office](https://companies.govt.nz) — director appointments, shareholding, historical roles, annual returns

**UK:**

- [Companies House](https://find-and-update.company-information.service.gov.uk) — director history, all registered companies

**US:**

- State secretary of state portals — coverage varies
- [OpenCorporates](https://opencorporates.com) — global cross-jurisdiction search

## Step 3: Property records

Check within the scope defined by the gate record only. Property records reveal addresses — handle carefully.

**Australia:**

- Property records are managed by state-level land registries (NSW LRS, Titles Victoria, LINZ for NZ)
- These are largely restricted to paid searches or in-person access. Note as requiring manual follow-up if within scope.

**New Zealand:**

- [LINZ](https://www.linz.govt.nz) — land title searches (paid)

**United Kingdom:**

- [HM Land Registry](https://www.gov.uk/search-property-information-land-registry) — public property search (reveals addresses)

**United States:**

- County assessor public search — coverage and access vary significantly by county

## Step 4: Professional licences

If the gate record covers professional background:

**Australia:**

- [AHPRA](https://www.ahpra.gov.au) — all registered health practitioners (doctors, nurses, pharmacists, dentists, physios, psychologists, optometrists, osteopaths, etc.)
- [ASIC Financial Advisers Register](https://moneysmart.gov.au/financial-advice/financial-advisers-register) — licensed financial advisers
- State law societies for lawyers

**New Zealand:**

- [Medical Council of NZ](https://www.mcnz.org.nz)
- [Nursing Council of NZ](https://www.nursingcouncil.org.nz)
- [NZ Law Society](https://www.lawsociety.org.nz) — practising certificate search
- [FMA Financial Services Register](https://www.fma.govt.nz/compliance/registers-and-warnings/financial-service-providers/)

**United States:**

- State licensing boards for medicine, law, finance, real estate, engineering — check state-level

## Step 5: Electoral roll

**United Kingdom:**

- UK electoral register — public search via local council

**United States:**

- Voter registration is publicly available in many states — availability and access vary

**Australia:**

- AU electoral rolls are NOT publicly searchable online. AEC rolls can only be inspected in person at AEC offices. Note this as checked but inaccessible via public search.

**New Zealand:**

- NZ Electoral Commission has limited public search capability. Note what's accessible.

## Follow-on skills

This skill covers formal records (court, licences, registrations). For professional history, social presence, and people-search aggregators, run `/investigator:people-lookup` alongside this skill — together they constitute a complete background check.

If company records surface a complex ownership structure worth mapping, hand off to `/investigator:corporate-ownership`.

## Rules

- Document jurisdiction for every record found. "Court records" without jurisdiction is meaningless.
- Note when a resource requires account creation or paid access — mark as checked but inaccessible, and suggest manual follow-up.
- AU property records are largely paid/restricted — don't attempt paid searches. Note as requiring manual follow-up.
- AU electoral rolls cannot be searched online — note clearly, don't skip without explanation.
- Distinguish between "no records found" (searched, nothing returned) and "not checked" (didn't search this source).

## Output format

```markdown
### Public records: [Name]

**Gate record:** [link or copy]
**Jurisdiction focus:** [AU / NZ / UK / US / other]
**Date:** [today]

#### Court records

[Findings or "no published decisions found" per jurisdiction searched]

#### Business registrations

[Director/officer appointments found — or "none found"]

#### Property records

[Within scope: findings or "requires manual follow-up (paid/restricted)"]

#### Professional licences

[Licences found — or "none found in checked registries"]

#### Electoral roll

[Result or "not publicly searchable online in [jurisdiction]"]

#### Source log

| Source | Searched | Result |
|---|---|---|
| AustLII | Yes | [result] |
| ASIC Connect | Yes | [result] |
| [etc.] | — | — |

#### Gaps and limitations

[What couldn't be accessed, what would require non-public access or manual follow-up]
```
