---
name: entity-footprint
description: "Map an organisation's complete public digital presence: domains, web presence, social profiles, apps, code repositories, job postings, and regulatory filings."
argument-hint: "[organisation name]"
user-invocable: true
allowed-tools: WebSearch, WebFetch
---

Map the public digital footprint of $ARGUMENTS.

## Step 1: Owned domains

Establish the primary domain, then discover related ones.

- **Reverse WHOIS:** search [ViewDNS.info](https://viewdns.info) for domains registered to the same entity (by registrant name or email where not privacy-protected)
- **Certificate transparency:** search [crt.sh](https://crt.sh) for the primary domain — wildcard and SANs often reveal subdomain patterns and product domains
- **Search variation:** `"[org name]" site:domain` patterns, regional variants (`.com.au`, `.co.nz`), product-specific domains, acquired brand domains

## Step 2: Web presence

- Primary site and its key sections (products, pricing, about, careers)
- Regional variants or localised sites
- Documentation or developer portals (often `docs.`, `developers.`, `api.`)
- Blog or content properties
- Status page (`status.`)

Use Wayback Machine to understand when properties were established and how they've evolved.

## Step 3: Social profiles

Search each platform:

| Platform | What to look for |
|---|---|
| LinkedIn | Company page, employee count, key executives |
| Twitter/X | Official account, follower count, posting cadence |
| GitHub | Organisation account, public repos, contributor patterns |
| YouTube | Product demos, conference talks, webinar archives |
| Facebook | Company page (often useful for older or B2C companies) |

Note: the absence of a platform presence is itself a signal — a tech company with no GitHub presence is unusual.

## Step 4: App store presence

Search iOS App Store and Google Play for the organisation's name.

Published apps reveal:

- Product scope beyond the website description
- User ratings and review sentiment (public)
- Update frequency (activity signal)
- Tech stack signals from app categories and permissions

## Step 5: Code repositories

[GitHub](https://github.com) organisation search:

- Public repositories — what they've open-sourced
- Tech stack patterns across repos
- Contributor patterns (team size, activity, geography)
- Stars and forks as adoption signal for developer-facing products

Also check [GitLab](https://gitlab.com) for organisations with non-GitHub presence.

## Step 6: Job postings as leading indicator

Current job postings reveal operational reality more reliably than press releases.

- Company careers page
- LinkedIn Jobs
- [Seek](https://www.seek.com.au) / [Seek NZ](https://www.seek.co.nz) for AU/NZ companies

Look for: technology stack requirements, new functional areas being built out, seniority distribution of open roles, hiring volume relative to declared company size.

## Step 7: Press and regulatory filings

- News search for the last 12 months
- Regulatory filings: [ASIC Connect](https://connect.asic.gov.au) (AU), [NZ Companies Office](https://companies.govt.nz) (NZ), Companies House (UK), SEC EDGAR (US public companies)
- AU broadcast/telco entities: [ACMA](https://www.acma.gov.au) register
- Any relevant industry-specific regulatory bodies

## Follow-on skills

This skill maps the surface of an organisation's digital presence. For deeper investigation of specific assets found here:

- **Domains discovered** → `/investigator:domain-intel` for registration, DNS, cert transparency, and hosting detail on any domain worth investigating further
- **IP addresses surfaced** → `/investigator:ip-intel` for ownership, ASN, and reputation
- **Ownership structure questions** → `/investigator:corporate-ownership`

## Rules

- Stay on organisational targets. If investigation reveals individual employee details, note the data exists but don't expand.
- Passive only — no authenticated access, no scraping behind login walls.
- Every claim about the organisation's footprint needs a source.
- A minimal footprint is a finding. A company that's hard to find online is telling you something.

## Output format

```markdown
## Entity footprint: [Organisation]

**Date:** [today]
**Purpose logged:** [stated purpose]
**Methods:** Passive open-source only

### Domain inventory

[Primary domain + related domains with discovery method]

### Web presence

[Primary site, regional variants, product properties, documentation]

### Social profiles

| Platform | Account | Followers/size | Activity |
|---|---|---|---|

### App store

[iOS/Android apps, rating, update frequency — or "none found"]

### Code repositories

[GitHub/GitLab presence, key repos, tech stack signals — or "none found"]

### Hiring signals

[Job posting patterns, technology stack from JDs, growth areas]

### Regulatory and press

[Filing status, recent news, regulatory actions]

### Notable observations

[Anything significant — gaps in presence, unusual patterns, discrepancies]

### Sources

1. [Tool/Source](URL) — [what it contributed]
```
