---
name: people-lookup
description: "Structured overview of a named individual's public presence: professional history, news coverage, academic work, people search aggregators, and company affiliations. Requires a complete authorisation gate before starting."
argument-hint: "[person name, with context: employer, location, or field]"
user-invocable: true
allowed-tools: WebSearch, WebFetch
---

Produce a structured overview of $ARGUMENTS's public presence.

> [!IMPORTANT]
> This skill requires the investigator agent's full authorisation gate before it can be invoked. Do not run this skill without a logged gate record (authorisation, purpose, scope, subject awareness). The gate is not optional.

## Step 1: Professional history

Search LinkedIn public profile, company website bios, and professional registrations.

For professionals in regulated fields, check licensing boards:

- AU health practitioners: [AHPRA](https://www.ahpra.gov.au) (doctors, nurses, pharmacists, physios, psychologists, allied health)
- AU financial advisers: [ASIC Financial Advisers Register](https://moneysmart.gov.au/financial-advice/financial-advisers-register)
- AU lawyers: state law societies
- NZ health practitioners: [Medical Council NZ](https://www.mcnz.org.nz), [Nursing Council NZ](https://www.nursingcouncil.org.nz)
- NZ lawyers: [NZ Law Society](https://www.lawsociety.org.nz)
- NZ financial services: [FMA Financial Services Register](https://www.fma.govt.nz/compliance/registers-and-warnings/financial-service-providers/)
- US professionals: relevant state licensing boards

## Step 2: News and press

Search Google News (`site:news.google.com "[name]"`) and relevant industry press for the subject's name combined with professional context.

For older coverage: newspaper archives where accessible.

Note: for names with many homonyms, add qualifiers (employer, location, field) to all searches.

## Step 3: Academic and published work

For researchers, academics, or published professionals:

- [Google Scholar](https://scholar.google.com)
- [ResearchGate](https://www.researchgate.net)
- [ORCID](https://orcid.org)
- [Semantic Scholar](https://www.semanticscholar.org)

Note publication count, citation count (very rough proxy for influence in field), and institutional affiliations.

## Step 4: People search aggregators

These aggregate public records — use for confirmation, not as primary source.

**US-based subjects:**

- [TruePeopleSearch](https://www.truepeoplesearch.com)
- [That's Them](https://thatsthem.com)
- [Radaris](https://radaris.com)

**AU-based subjects:**

- [White Pages AU](https://www.whitepages.com.au)
- [Australia411](https://www.australia411.com.au)

Note: AU/NZ have no equivalent of the comprehensive US people-search aggregators. These directories are narrower and less cross-referenced — use for directory-style confirmation only.

**NZ-based subjects:**

- [White Pages NZ](https://www.whitepages.co.nz)

## Step 5: Company affiliations

Check for current and historical directorships or company registrations:

- AU: [ASIC Connect](https://connect.asic.gov.au) — director search across all registered companies
- NZ: [NZ Companies Office](https://companies.govt.nz) — director appointments, historical roles
- UK: [Companies House](https://find-and-update.company-information.service.gov.uk) — director history
- US public companies: [SEC EDGAR](https://www.sec.gov/cgi-bin/browse-edgar) for officer listings
- Global: [OpenCorporates](https://opencorporates.com) for cross-jurisdiction search

## Step 6: Cross-reference

Before including any fact in the output, confirm it across at least two independent sources. A single people search result is a lead, not a finding.

Flag single-source findings explicitly.

## Follow-on skills

A complete background check typically needs both this skill and `/investigator:public-records` — this skill covers professional history and licensing, `public-records` covers court filings and company directorships. Run both unless the gate scope explicitly limits to one.

If a company affiliation is found and the investigation scope includes the organisation, hand off to `/investigator:entity-footprint` (digital presence) or `/investigator:corporate-ownership` (ownership structure).

## Rules

- This skill cannot run without a complete authorisation gate. Stop if the gate record is missing.
- Cross-reference key facts across two independent sources before asserting them.
- Don't pivot from professional background into personal life — addresses, family, daily routine are out of scope unless the gate record explicitly includes them.
- Name disambiguation: if multiple people share the name, use context anchors (location, employer, field) to isolate the correct subject. Document the disambiguation method in the output.
- Absence is a finding. No press, no academic work, minimal professional footprint is a result — not a failed investigation.

## Output format

```markdown
### People lookup: [Name]

**Gate record:** [link or copy of gate record from investigator]
**Context anchors used:** [employer, location, field — what was used to disambiguate]

#### Professional history

[Roles, employers, tenure — sourced]

#### Licensing and registrations

[Any professional registrations found — or "none found in checked registries"]

#### News and press

[Dated list, most recent first — or "no significant press coverage found"]

#### Academic/published work

[Publication summary — or "no published work found"]

#### Company affiliations

[Directorships or company registrations found — or "none found"]

#### Source cross-reference

[Which key facts confirmed across 2+ independent sources; which are single-source only]

#### Gaps and limitations

[What couldn't be confirmed; what is out of scope per gate]
```
