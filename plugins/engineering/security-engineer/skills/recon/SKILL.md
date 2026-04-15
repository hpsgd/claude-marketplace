---
name: recon
description: "Passive reconnaissance on a target domain or organisation using open-source intelligence. Maps the attack surface from publicly available sources only. Use at the start of a penetration test or security assessment to understand what's exposed before active testing begins."
argument-hint: "[target domain or organisation name] for [engagement name or authorisation reference]"
user-invocable: true
allowed-tools: WebSearch, WebFetch
---

Conduct passive reconnaissance on $ARGUMENTS.

> [!IMPORTANT]
> Passive reconnaissance only. This skill collects publicly available information without touching the target's systems. Active scanning (nmap, Burp, nikto, etc.) is outside this skill's scope. Authorisation for subsequent active testing does NOT come from this skill — confirm scope and rules of engagement before proceeding to any active phase.

## Step 1: Scope definition

Before starting, confirm and log:

- **Target:** the domain(s), IP ranges, or organisation in scope
- **Authorisation reference:** engagement name, statement of work reference, or authorisation letter
- **Out of scope:** any explicitly excluded assets, subdomains, or IP ranges

Reconnaissance that drifts outside the agreed scope can have legal and contractual consequences. When uncertain, check with the client before proceeding.

## Step 2: Domain and DNS enumeration

Using only passive sources (no active DNS queries to the target):

**Certificate transparency** — [crt.sh](https://crt.sh): search for all certificates issued to `%.target.com`. This is the single most reliable passive subdomain discovery method.

**DNS records** — [SecurityTrails](https://securitytrails.com) public search or [dnsdumpster.com](https://dnsdumpster.com) for historical DNS data including subdomains, MX records, and past IP associations.

**WHOIS** — registrant, nameservers, registration date. See `/investigator:domain-intel` for the full WHOIS methodology including AU/NZ registries.

**Google dorking** — passive web search queries to discover indexed content and exposed resources:

```
site:target.com -www          # Subdomains indexed by Google
site:target.com filetype:pdf  # Exposed documents
site:target.com inurl:admin   # Admin interfaces
site:target.com "index of"    # Directory listings
```

## Step 3: ASN and IP range mapping

Find all IP ranges associated with the organisation:

- [BGP.he.net](https://bgp.he.net): search by organisation name to find all registered ASNs and associated IP blocks
- [ipinfo.io](https://ipinfo.io): validate specific IPs
- APNIC (AU/NZ), ARIN (US/CA), RIPE (EU) — RIR allocation records for the organisation

This establishes the full IP surface area, including ranges that may not be surfaced by DNS alone.

## Step 4: Technology fingerprinting

Identify technologies in use from passive indicators:

**Job postings** — the most underrated reconnaissance source. Job postings name specific technologies, versions, and products. A job ad for a "Senior AWS security engineer with experience in Terraform and Kubernetes" tells you the cloud platform, IaC tool, and container orchestration.

Search: LinkedIn Jobs, Seek (AU/NZ), the company careers page.

**Web technologies** — [Wappalyzer](https://www.wappalyzer.com) public lookup, BuiltWith (for public data tier). Reveals CMS, CDN, analytics, and framework choices.

**Email headers** — publicly available email headers (in press releases, newsletters) reveal mail server software, delivery infrastructure, and SPF/DKIM configuration.

**TXT record analysis** — from DNS step: third-party services declared in TXT records (HubSpot, Salesforce, SendGrid, Google Workspace, Microsoft 365) map the SaaS surface area.

## Step 5: Shodan and Censys passive search

[Shodan](https://shodan.io) and [Censys](https://search.censys.io) index internet-connected services from their own scanning activity — looking at their data is passive from your perspective.

Search by: organisation name, ASN, IP range, domain name.

Note: Shodan/Censys data has a timestamp. Flag the scan date of any findings — a service that was exposed 6 months ago may have been remediated.

Key findings to surface: exposed management interfaces, non-standard ports with service banners, TLS certificate details, HTTP response headers.

## Step 6: Leaked credential and breach data

**HaveIBeenPwned** — `api.haveibeenpwned.com/api/v2/breachedaccount/[email]` or domain search to identify breaches affecting corporate email addresses.

**Public paste sites and GitHub** — search for: `target.com password`, `target.com api_key`, `target.com secret`. GitHub dork: `"target.com" filename:.env` or `"target.com" api_key`.

Finding leaked credentials doesn't mean they're still valid — but it confirms the credential class was exposed and should be flagged for the client to investigate.

## Step 7: Social engineering surface

What information could an attacker use for social engineering or phishing?

- LinkedIn: organisational structure, named employees, roles, and email format patterns
- Conference talks and papers: technical details disclosed by engineers in public presentations
- Job postings: internal tool names, team structures, process details

This section informs the social engineering risk assessment, not active attacks.

## Rules

- Passive methods only. Nothing in this skill touches the target's systems.
- Authorisation reference must be logged before starting. No exceptions.
- Shodan/Censys findings cite the scan timestamp — old data shouldn't be presented as current state.
- GitHub and paste site findings are leads, not confirmed exposures. They require client validation.
- Scope discipline. Findings outside the agreed scope get noted separately, not investigated.

## Output format

```markdown
## Reconnaissance: [Target]

**Engagement:** [authorisation reference]
**Date:** [today]
**Scope:** [domains / IP ranges in scope]
**Out of scope:** [exclusions]
**Method:** Passive OSINT only

### Domain and subdomain inventory

[Subdomains found via cert transparency, DNS, Google dorking]

### IP ranges and ASN

[Registered ASNs and IP blocks]

### Technology fingerprint

| Category | Technology | Source | Confidence |
|---|---|---|---|
| Web framework | — | Wappalyzer | High / Medium |
| Email | — | MX record | High |
| Cloud | — | Job postings | Medium |

### Exposed services (Shodan/Censys)

| Service | IP:Port | Shodan scan date | Notes |
|---|---|---|---|

### Credential exposure

[Breach data findings — with breach names and dates, not plaintext credentials]

[GitHub/paste findings — with URLs to the specific commits/pastes]

### Social engineering surface

[LinkedIn structure, email format pattern, notable disclosures]

### Attack surface summary

[High-level assessment: what stands out, what warrants active testing focus]

### Out-of-scope findings

[Anything surfaced that falls outside agreed scope — noted but not investigated]
```
