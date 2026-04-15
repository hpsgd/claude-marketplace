---
name: ip-intel
description: "Investigate an IP address: ownership, hosting provider, ASN, reputation, and associated infrastructure. Passive sources only — no active scanning."
argument-hint: "[IP address or CIDR range]"
user-invocable: true
allowed-tools: WebSearch, WebFetch
---

Produce an IP intelligence report for $ARGUMENTS using passive public sources only.

## Step 1: Ownership and geolocation

Use [ipinfo.io](https://ipinfo.io) for the primary lookup: ASN, organisation name, and geolocation.

Then cross-reference with the authoritative regional internet registry for the IP's allocation:

| Region | Registry | URL |
|---|---|---|
| North America | ARIN | [arin.net](https://arin.net) |
| Europe, Middle East, Central Asia | RIPE NCC | [ripe.net](https://ripe.net) |
| Asia Pacific (including AU/NZ) | APNIC | [apnic.net](https://apnic.net) |
| Latin America | LACNIC | [lacnic.net](https://lacnic.net) |
| Africa | AFRINIC | [afrinic.net](https://afrinic.net) |

The RIR record gives the authoritative allocation — who IANA assigned the block to, and any sub-allocations.

## Step 2: Reverse DNS

Look up the PTR record via [MXToolbox](https://mxtoolbox.com) reverse lookup.

Reverse DNS naming conventions often reveal:

- The operator's naming scheme (`mail.company.com`, `api-prod-1.cloud.company.com`)
- Hosting provider patterns (`compute.amazonaws.com`, `servers.ovh.net`)
- Geographic or functional naming (`syd01.hosting.example.com` suggests Sydney data centre)

## Step 3: Reputation

Check multiple reputation sources — a clean result on one doesn't mean clean everywhere:

- [VirusTotal](https://www.virustotal.com) — malware associations, URL/file detections tied to this IP
- [AbuseIPDB](https://www.abuseipdb.com) — crowdsourced abuse reports (spam, scanning, brute force)
- [Shodan](https://www.shodan.io) public search — services exposed, banners, historical ports (search only, no active scanning)

Note: Shodan data may be stale. It's a historical record of what was observed, not necessarily current state.

## Step 4: Related infrastructure

- Other IPs in the same ASN range that share patterns with this IP
- Reverse IP lookup on [ViewDNS.info](https://viewdns.info) — other domains hosted on this IP
- Shared hosting detection — if multiple unrelated domains resolve here, it's likely a shared hosting environment

## Step 5: Historical context

Has this IP been notable before? Search:

- `[IP address] incident` / `[IP address] breach` / `[IP address] attack`
- Threat intelligence feeds that have public exposure (GreyNoise, pulsedive)
- Any major ownership changes (ASN transfers, RIPE records)

## Rules

- Passive methods only. Do not port scan, banner grab, or interact with any service on this IP.
- Shodan is a passive source — use its search interface, not any active scanning capability.
- If the IP belongs to a major cloud provider (AWS, Azure, GCP, Cloudflare), note that attribution to the provider doesn't identify the actual customer.
- A clean reputation score doesn't mean the IP is benign. It means it hasn't been reported. State this distinction clearly.

## Output format

```markdown
## IP intelligence: [IP address]

**Date:** [today]
**Purpose logged:** [stated purpose]
**Methods:** Passive open-source only

### Ownership

| Attribute | Value |
|---|---|
| Organisation | — |
| ASN | — |
| RIR | — |
| Allocated to | — |
| Geolocation | — |

### Reverse DNS

[PTR record and what it reveals about the operator]

### Reputation

| Source | Result | Details |
|---|---|---|
| VirusTotal | Clean / [N detections] | — |
| AbuseIPDB | [N reports] | [Types of abuse] |
| Shodan | [Services observed] | [Date of last scan] |

### Related infrastructure

[Other domains on this IP, ASN pattern, shared hosting context]

### Historical context

[Any notable history — incidents, ownership changes, notable associations]

### Notable observations

[Anything significant — unusual patterns, discrepancies between sources]

### Gaps

[What couldn't be established with passive methods]

### Sources

1. [Tool/Registry](URL) — [what it contributed]
```
