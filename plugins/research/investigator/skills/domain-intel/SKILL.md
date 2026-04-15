---
name: domain-intel
description: "Investigate a domain's registration, DNS, certificates, hosting, and history using passive public sources. Use when mapping a domain's infrastructure or researching who owns/operates it."
argument-hint: "[domain name]"
user-invocable: true
allowed-tools: WebSearch, WebFetch
---

Produce a domain intelligence report for $ARGUMENTS using passive public sources only.

## Step 1: Registration

Look up WHOIS to establish registrant, registrar, creation/expiry dates, and nameservers.

Choose the right registry for the TLD:

- **.com/.net/.org and generic TLDs:** [who.is](https://who.is) or registrar lookup
- **.au domains:** [auDA WHOIS](https://whois.audns.net.au) — the authoritative .au registry
- **.nz domains:** [NZRS WHOIS](https://whois.nic.nz) — InternetNZ
- **.uk domains:** Nominet WHOIS
- **Country TLDs generally:** [IANA WHOIS](https://www.iana.org/whois) redirects to the authoritative registry

Note: many registrations use privacy protection — log this as a finding, not a failure. Proceed with DNS and certificate transparency.

## Step 2: DNS records

Fetch DNS records via [MXToolbox](https://mxtoolbox.com) or [dnsdumpster.com](https://dnsdumpster.com).

Collect: A, AAAA, MX, TXT, NS, CNAME records.

TXT records frequently reveal: email providers (Google Workspace, Microsoft 365), SPF/DKIM configuration, third-party service ownership verification (Stripe, HubSpot, Salesforce), and site verification codes.

## Step 3: Certificate transparency

Search [crt.sh](https://crt.sh) for all certificates issued to the domain and its subdomains.

Certificate transparency reveals:

- All subdomains (including internal-looking names that suggest architecture)
- Naming patterns (environments: dev/staging/prod; regions; services)
- Certificate issuer (Let's Encrypt = self-managed; DigiCert/Sectigo = often enterprise)
- Certificate history (when the domain started using HTTPS; any gaps)

## Step 4: ASN and hosting

Use [ipinfo.io](https://ipinfo.io) or [BGP.he.net](https://bgp.he.net) to identify:

- Hosting provider and ASN
- IP range the domain resolves to
- Geographic location of hosting

Cross-reference with MX records to identify email hosting (separate from web hosting is common).

## Step 5: Reverse WHOIS and related domains

Search [ViewDNS.info](https://viewdns.info) for other domains registered to the same entity (registrant name or email where not privacy-protected).

This can reveal related brands, acquired properties, or shell domains.

## Step 6: Historical data

- [Wayback Machine](https://web.archive.org) — what has the site looked like historically? When was it first indexed? Any major content changes?
- SecurityTrails public tier — DNS history and IP history where available

Historical gaps (domain registered but no Wayback content for a period) can be significant.

## Follow-on skills

Domain intel often surfaces leads worth deeper investigation:

- **Multiple related domains found** → run this skill again per domain, or use `/investigator:entity-footprint` for the full organisational picture
- **IP addresses from A/AAAA records worth investigating** → `/investigator:ip-intel`
- **Organisation behind the domain** → `/investigator:corporate-ownership` for the legal entity structure

## Rules

- Passive methods only. Never attempt active scanning, port enumeration, or authenticated access.
- Log every source used, including those that returned no results.
- Privacy-protected WHOIS is a finding, not a failure — note it and continue with other sources.
- Don't pivot from infrastructure investigation into profiling individuals whose names appear in records. Note the name exists if relevant; don't expand.
- Absence is data. A domain with no Wayback history, a brand-new registration, or no TXT records is telling you something.

## Output format

```markdown
## Domain intelligence: [domain]

**Date:** [today]
**Purpose logged:** [stated purpose]
**Methods:** Passive open-source only

### Registration

| Attribute | Value |
|---|---|
| Registrar | — |
| Registered | — |
| Expires | — |
| Nameservers | — |
| Privacy protection | Yes / No |

### DNS records

[Key records with interpretation — not just raw data]

### Certificate transparency findings

[Subdomains discovered, naming patterns, certificate history]

### Hosting

| Attribute | Value |
|---|---|
| Hosting provider | — |
| ASN | — |
| IP range | — |
| Email hosting | — |

### Related domains

[Domains sharing registration details — or "none found" / "privacy-protected, unable to determine"]

### Historical findings

[Wayback Machine observations, DNS history anomalies]

### Notable observations

[Anything that stands out — unusual configurations, patterns, discrepancies]

### Gaps

[What couldn't be established; what would require deeper access]

### Sources

1. [Tool/Registry](URL) — [what it contributed]
```
