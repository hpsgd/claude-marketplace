---
name: corporate-ownership
description: "Map a company's ownership chain, related entities, and director networks. Use for beneficial ownership investigation, M&A research, or understanding complex corporate structures. Full AU/NZ/UK/US registry coverage."
argument-hint: "[company name or registration number]"
user-invocable: true
allowed-tools: WebSearch, WebFetch
---

Map the corporate ownership structure for $ARGUMENTS.

## Step 1: Primary registration

Look up the company's official registration record. This establishes the legal entity, jurisdiction, and current status.

**Australia:**

- [ASIC Connect](https://connect.asic.gov.au) — company extract includes current and historical directors, shareholders for proprietary companies, registered office, date of registration, and current status
- [ABN Lookup](https://abn.business.gov.au) — ABN/ACN cross-reference, business name registration, GST registration status

**New Zealand:**

- [NZ Companies Office](https://companies.govt.nz) — director history, shareholding structure, registered office, annual returns, filing history

**United Kingdom:**

- [Companies House](https://find-and-update.company-information.service.gov.uk) — full filing history, director history, PSC register (persons with significant control = beneficial owners), accounts

**United States:**

- State secretary of state portals for private companies (coverage varies)
- [SEC EDGAR](https://www.sec.gov/cgi-bin/browse-edgar) for public companies — 10-K lists subsidiaries

**Global cross-reference:**

- [OpenCorporates](https://opencorporates.com) — cross-jurisdiction search, links entities across registries

## Step 2: Beneficial ownership

Identify who ultimately controls or owns the company beyond the registered directors.

Sources:

- UK PSC register (Companies House) — requires disclosure of beneficial owners holding 25%+ control
- [ICIJ Offshore Leaks Database](https://offshoreleaks.icij.org) — offshore structures from leaked datasets (Panama Papers, Pandora Papers, etc.). Public data only.
- [ABN Lookup](https://abn.business.gov.au) for AU — parent entity relationships sometimes disclosed
- SEC 13D/13G filings for US public companies — major shareholder disclosures

Note: beneficial ownership disclosure requirements vary by jurisdiction. Absence of disclosed owners doesn't mean there aren't any.

## Step 3: Director networks

Map all director appointments across the entity:

- Identify current and historical directors from the primary registration
- For each director, search their other company appointments:
  - AU: ASIC Connect director search
  - NZ: NZ Companies Office director search
  - UK: Companies House director search
  - Global: OpenCorporates officer search

Director networks often reveal undisclosed relationships between apparently separate entities.

## Step 4: Subsidiary mapping

For the target company, identify subsidiaries and related entities:

- SEC 10-K Exhibit 21 (US public companies) — lists all subsidiaries
- Companies House group structures (UK)
- ASX/NZX annual report subsidiaries note (AU/NZ public companies)
- ASIC Connect — corporate group searches

## Step 5: Related entities

Look for entities that share:

- The same registered address
- The same directors (cross-reference Step 3 results)
- The same registered agent
- Similar naming patterns

OpenCorporates "related companies" and ViewDNS.info reverse WHOIS (for digital footprint overlap) can help here.

## Rules

- Document the jurisdiction for every entity in the ownership chain.
- Distinguish between registered ownership (what the registry shows) and beneficial ownership (who actually controls the entity). These often differ.
- Note when an ownership chain terminates in a jurisdiction with limited disclosure requirements (offshore structures, certain US states) — this is a significant finding, not a gap.
- ICIJ data covers specific leaked datasets — it's a signal, not a comprehensive offshore registry. Absence from ICIJ doesn't mean no offshore structure.

## Output format

```markdown
## Corporate ownership: [Company name]

**Date:** [today]
**Primary jurisdiction:** [AU / NZ / UK / US / other]
**Registration number:** [if known]

### Primary registration

| Attribute | Value |
|---|---|
| Legal name | — |
| Registration number | — |
| Jurisdiction | — |
| Status | Active / Deregistered / other |
| Registered office | — |
| Date registered | — |

### Directors (current)

| Name | Role | Appointed | Other appointments |
|---|---|---|---|

### Directors (historical)

[Notable past directors and tenure periods]

### Ownership structure

[Shareholders / beneficial owners disclosed in registries — with jurisdiction of disclosure]

### Subsidiaries

[Known subsidiaries with jurisdiction]

### Related entities

[Entities sharing directors, address, or registered agent]

### Offshore/complex structure notes

[Any indications of offshore holding structures or jurisdictions with limited disclosure]

### Director network map

[Cross-appointments that link this entity to others]

### Sources

1. [Registry](URL) — [what it contributed]
```
