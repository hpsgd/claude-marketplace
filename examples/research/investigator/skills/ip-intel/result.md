# Ip Intel

Scenario: A security team wants to investigate an IP address that appeared repeatedly in their firewall logs making unusual outbound connection attempts.

## Prompt

> /investigator:ip-intel 185.220.101.47 — appeared in our firewall logs making repeated outbound connections on port 443. Security investigation context.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## IP intelligence: 185.220.101.47

**Date:** 2026-05-01
**Purpose logged:** Repeated outbound connections on port 443 in firewall logs
**Methods:** Passive open-source only

---

### Ownership

| Attribute | Value |
|---|---|
| Organisation | Stiftung Erneuerbare Freiheit (Foundation for Renewable Freedom) |
| ASN | AS60729 — TORSERVERS-NET |
| RIR | RIPE NCC |
| Allocated block | 185.220.101.32/27 (netname: **TOR-EXIT**) |
| Geolocation | Berlin, Germany |
| Abuse contact | abuse@for-privacy.net |

RIPE record (created 2021-08-31) carries netname "TOR-EXIT" with the remark: *"This network is used for Tor Exits. We do not have any logs at all."* The /24 is subdivided into multiple /27 blocks all designated TOR-EXIT. RPKI valid on all announced prefixes.

---

### Reverse DNS

PTR: **`tor-exit-47.for-privacy.net`**

Operator-assigned, explicit. The naming convention (`tor-exit-[N].for-privacy.net`) identifies every exit node in the /24. Fully consistent with WHOIS — this is not a spoofed PTR. Any IDS doing PTR-based Tor detection fires immediately on this label.

---

### Reputation

| Source | Result | Details |
|---|---|---|
| VirusTotal | Not retrieved | JS-gated — check manually at virustotal.com/gui/ip-address/185.220.101.47 |
| AbuseIPDB | **100% confidence — 6,500 reports** | 570 distinct sources. First report 2021-09-22. Categories: brute force, web attacks, port scanning, hacking. Most recent: within hours of this report |
| Shodan | Port 80/TCP — Tor built-in httpd | "This is a Tor Exit Router" notice page. Tagged: Tor exit node. Last seen: 2026-05-01 |
| GreyNoise | Login-gated | Adjacent IPs in the /27 classified Malicious / Tor Exit Node. Cannot confirm .47 label without API access |
| Cleantalk | **Blacklisted** | 4,022 sites attacked. Active as of 2026-05-01. AS60729 carries 85.97% network-wide spam rate |
| Tor Project Exit List | **Confirmed active exit node** | Fingerprint: 2390B303058F5EC1E1BEAAEECE3AAF2CF97B71F4. Published 2026-04-30. ExitAddress confirmed 2026-05-01 09:27:36 |

---

### Related infrastructure

AS60729 operates **321 total relays** (260 exit, 61 middle) under the `for-privacy.net` and `relayon.org` operator families, collectively handling ~69 Gbps of exit capacity. This is one of the larger dedicated Tor exit ASes in the RIPE region. All IPs in the .32–.63 range resolve to `tor-exit-[N].for-privacy.net` with identical AbuseIPDB 100% ratings. The AS peers through Deutsche Telekom (AS3320), RETN (AS9002), and IN-Berlin e.V. (AS29670) — purpose-built anonymity infrastructure, not general-purpose hosting.

ViewDNS returned 403 (bot-blocked). Only two domain names appear across the entire /24 in Cleantalk — both likely arriving as traffic through the exit rather than hosted there.

---

### Historical context

Cleantalk activity detected from 2018-09-14 (predates the current RIPE record from 2021). AbuseIPDB first report 2021-09-22 aligns with when the node went live in its current form.

**CISA Advisory AA20-183A** (joint FBI/CISA, July 2020) explicitly addresses malicious activity routed through Tor exits — covering reconnaissance, credential stuffing, C2, and data exfiltration — and recommends blocking or granular monitoring of all connections to known Tor exits.

Operator's published policy: no logging, no traffic inspection, abuse complaints about specific destination ports may result in exit policy adjustments.

---

### Notable observations

**This is a confirmed, intentionally operated Tor exit node — not a compromised host.** Operationally significant distinctions:

1. **Traffic source is opaque by design.** Connections from this IP do not originate from this host — they originate from anonymous Tor circuit users. The operator has no logs and cannot identify the source. Attribution to a specific threat actor via this IP alone is not possible.

2. **Port 443 is within standard Tor exit policy.** Repeated 443 connections are consistent with normal Tor exit traffic volume (which is high), not necessarily targeted activity.

3. **High AbuseIPDB score reflects cumulative global reports** across many environments, not confirmed targeting of your organisation specifically. The brute force and web attack categories are worth correlating against your application logs.

4. **The key question** is whether these connections are (a) generic Tor exit noise hitting an internet-facing service you expose, or (b) directed probing/credential attacks against authenticated endpoints. That distinction requires application-layer log correlation — not determinable from OSINT.

---

### Gaps

- **VirusTotal** — JS-gated; check manually for passive DNS history and vendor detection count
- **GreyNoise exact label for .47** — login-gated; adjacent IPs suggest Malicious/Tor Exit Node but unconfirmed for this specific IP
- **Shodan full port history** — only port 80 confirmed; full data requires account
- **ThreatFox** — CAPTCHA-blocked; no IOC result, but absence cannot be asserted
- **ViewDNS** — 403 returned; domain co-tenancy could not be mapped
- **Application-layer correlation** — what's being targeted on port 443 in your environment requires your firewall destination field and application logs

---

### Sources

1. [ipinfo.io](https://ipinfo.io/185.220.101.47/json) — ASN, organisation, hostname, geolocation
2. [RIPE WHOIS via stat.ripe.net](https://stat.ripe.net/data/whois/data.json?resource=185.220.101.47) — inetnum TOR-EXIT, no-logging remark
3. [AbuseIPDB](https://www.abuseipdb.com/check/185.220.101.47) — 100% confidence, 6,500 reports
4. [Cleantalk](https://cleantalk.org/blacklists/185.220.101.47) — 4,022 sites attacked, active 2026-05-01
5. [Tor Project Exit List](https://check.torproject.org/exit-addresses) — confirmed exit fingerprint, active 2026-05-01
6. [bgp.tools AS60729](https://bgp.tools/as/60729) — prefix count, peers, RPKI
7. [OrNetStats AS60729](https://nusenu.github.io/OrNetStats/w/as_number/AS60729) — 321 relays, ~69 Gbps capacity
8. [Shodan](https://www.shodan.io/host/185.220.101.47) — port 80 Tor httpd, last seen 2026-05-01
9. [CISA AA20-183A](https://www.cisa.gov/news-events/cybersecurity-advisories/aa20-183a) — Tor exit detection and blocking guidance

---

**Bottom line:** 185.220.101.47 is a high-volume, intentionally operated Tor exit node run by a German privacy foundation. The repeated port 443 connections are consistent with normal Tor exit traffic patterns. The critical next step is application-layer correlation: check what endpoint is being hit and whether authentication failures, scanning patterns, or anomalous request rates align with these source connections.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.5/19.5 (85%) |
| Evaluated | 2026-05-01 |
| Target duration | 280060 ms |
| Target cost | $0.9211 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill logs the stated purpose (security investigation) before starting | PASS | Header block at top of output: '**Purpose logged:** Repeated outbound connections on port 443 in firewall logs' and '**Methods:** Passive open-source only' appear before any lookup data. |
| c2 | Primary ownership lookup uses ipinfo.io for ASN, organisation, and geolocation | PASS | Sources list item 1: 'ipinfo.io — ASN, organisation, hostname, geolocation'. Ownership table populated with AS60729, Stiftung Erneuerbare Freiheit, and Berlin/Germany from this source. |
| c3 | The appropriate regional internet registry is queried for the authoritative allocation record — RIPE NCC for this European IP range | PASS | Sources item 2: 'RIPE WHOIS via stat.ripe.net'. Output includes inetnum block 185.220.101.32/27, netname TOR-EXIT, remark about no-logging, and record creation date 2021-08-31 from RIPE. |
| c4 | Reverse DNS PTR record is looked up and interpreted for what it reveals about the operator's naming scheme | PASS | Dedicated 'Reverse DNS' section: PTR is 'tor-exit-47.for-privacy.net'. Output then interprets: 'The naming convention (tor-exit-[N].for-privacy.net) identifies every exit node in the /24. Fully consistent with WHOIS — this is not a spoofed PTR.' |
| c5 | Reputation is checked across multiple sources — VirusTotal, AbuseIPDB, and Shodan public search | PASS | Reputation table covers VirusTotal (JS-gated, check manually), AbuseIPDB (100% confidence, 6,500 reports, 570 distinct sources), Shodan (port 80 Tor httpd, last seen 2026-05-01), plus GreyNoise, Cleantalk, and Tor Project Exit List. |
| c6 | Shodan data is labelled as historical, not necessarily current state | PARTIAL | Shodan row includes 'Last seen: 2026-05-01' and Gaps section notes 'Shodan full port history — only port 80 confirmed; full data requires account.' The last-seen date implies historical scan data, but no explicit disclaimer that 'current state may differ' is present. |
| c7 | If the IP belongs to a major cloud or hosting provider, output notes that provider attribution does not identify the actual customer | PASS | IP is a Tor exit, not a cloud provider; however, the output provides the directly analogous caveat: 'Connections from this IP do not originate from this host — they originate from anonymous Tor circuit users. The operator has no logs and cannot identify the source. Attribution to a specific threat actor via this IP alone is not possible.' |
| c8 | A clean reputation result is not equated with benign — the output states explicitly that clean means "not reported," not "safe" | FAIL | This IP has a terrible reputation (100% AbuseIPDB) so no clean result arises. The output never includes the general caveat that 'clean = not reported, not safe.' Observation #3 caveats high scores not equaling targeted attacks, but that is a different point. |
| c9 | Related infrastructure is investigated — other domains on the same IP and ASN patterns are checked | PARTIAL | AS60729 investigated (321 relays, ~69 Gbps, BGP peers). /24 pattern documented (all resolve to tor-exit-[N].for-privacy.net with identical AbuseIPDB 100% ratings). ViewDNS attempted but returned 403. Cleantalk mentions only two domain names across /24. No SecurityTrails/RiskIQ passive DNS used; ceiling is PARTIAL. |
| c10 | Passive methods only — no active scanning, port enumeration, or service interaction; everything via third-party passive aggregators | PASS | 'Methods: Passive open-source only' stated at top. All nine sources are third-party passive aggregators. Gaps section documents where data was unavailable due to JS-gating, CAPTCHAs, and login requirements — no attempt to work around with active methods. |
| c11 | Output logs the stated purpose (security investigation per firewall log analysis) at the top before any lookup | PASS | Second line of output: '**Purpose logged:** Repeated outbound connections on port 443 in firewall logs' — appears in the header metadata block before the Ownership section. |
| c12 | Output's primary lookup uses ipinfo.io (or equivalent) for ASN, organisation, geolocation — with the actual values returned (e.g. "AS204480 — IP Volume Inc — Netherlands") | PASS | Ownership table: 'Organisation: Stiftung Erneuerbare Freiheit', 'ASN: AS60729 — TORSERVERS-NET', 'Geolocation: Berlin, Germany'. Source attributed to ipinfo.io. |
| c13 | Output queries RIPE NCC for the European IP range — getting the authoritative allocation (which differs from ipinfo's enriched data) including the inetnum block, the named contact for that block, and the country code | PASS | RIPE record cited with inetnum block '185.220.101.32/27', netname 'TOR-EXIT', abuse contact 'abuse@for-privacy.net', record created 2021-08-31. Country implicit in Berlin/Germany geolocation. Source is stat.ripe.net. |
| c14 | Output's reverse-DNS PTR lookup is performed and the result interpreted — e.g. naming pattern reveals operator type | PASS | PTR 'tor-exit-47.for-privacy.net' resolved; interpreted: 'naming convention (tor-exit-[N].for-privacy.net) identifies every exit node in the /24… Any IDS doing PTR-based Tor detection fires immediately on this label.' |
| c15 | Output checks reputation across at least 3 sources — VirusTotal IP report, AbuseIPDB confidence-of-abuse score, Shodan public scan history — with the specific URLs and result counts per source | PASS | AbuseIPDB: '100% confidence — 6,500 reports, 570 distinct sources'. Shodan: 'Port 80/TCP — Tor built-in httpd, Last seen 2026-05-01'. VirusTotal: 'JS-gated — check manually at virustotal.com/gui/ip-address/185.220.101.47'. Specific URLs provided in Sources section. |
| c16 | Output labels Shodan data as HISTORICAL — "Shodan last scanned this IP on YYYY-MM-DD; current state may differ" — never asserts current open ports based on Shodan | PARTIAL | Shodan row shows 'Last seen: 2026-05-01'. Gaps section: 'Shodan full port history — only port 80 confirmed; full data requires account.' The last-seen date is provided, but no explicit 'current state may differ' disclaimer is present. Output does not assert current open ports beyond what Shodan returned. |
| c17 | Output addresses the specific IP 185.220.101.47 — known historically as a Tor exit node range; output names this if visible in reputation data, NOT as a hidden assumption | PASS | Notable Observations: 'This is a confirmed, intentionally operated Tor exit node — not a compromised host.' PTR confirms 'tor-exit-47.for-privacy.net'. Tor Project Exit List entry with fingerprint '2390B303058F5EC1E1BEAAEECE3AAF2CF97B71F4' and ExitAddress confirmed 2026-05-01 09:27:36 cited as evidence. |
| c18 | Output explicitly states clean-reputation does NOT mean benign — "IP not currently flagged in AbuseIPDB / VirusTotal does not equal safe; many IPs are uncategorised, especially recently allocated infrastructure" | FAIL | IP has 100% AbuseIPDB confidence so no 'clean' result exists; the specific disclaimer that 'clean = not reported, not safe' is never stated. The closest text is Observation #3 cautioning that high AbuseIPDB scores reflect global cumulative reports rather than targeted attacks — a different point entirely. |
| c19 | Output investigates related infrastructure — domains hosted on this IP (via passive DNS like SecurityTrails, RiskIQ), other IPs in the same /24 with similar reputation patterns, ASN-level reputation | PASS | ASN-level: AS60729 with 321 relays, ~69 Gbps, BGP peers via bgp.tools and OrNetStats. /24 reputation: 'All IPs in the .32–.63 range resolve to tor-exit-[N].for-privacy.net with identical AbuseIPDB 100% ratings.' Cleantalk domain count and ViewDNS (returned 403) attempted for domain co-tenancy. |
| c20 | Output uses passive methods only — no nmap, no port scans, no banner grabbing, no service interaction; everything via third-party passive aggregators | PASS | 'Methods: Passive open-source only' stated at top. All sources (ipinfo, RIPE, AbuseIPDB, Cleantalk, Tor Project, bgp.tools, OrNetStats, Shodan, CISA) are passive third-party aggregators. No active probing attempted or described. |

### Notes

The output is thorough and well-structured, correctly identifying 185.220.101.47 as an intentional Tor exit node with strong multi-source corroboration. The two FAIL scores both stem from the same gap: the 'clean reputation ≠ safe' caveat (c8/c18) is absent, which is understandable given the IP has terrible reputation, but the criteria require it as a standing disclaimer regardless. The two PARTIAL scores both concern Shodan historical labeling (c6/c16): the output provides a 'Last seen' date but never adds the explicit 'current state may differ' disclaimer. The PARTIAL ceiling on c9 (related infrastructure) was correctly earned — ViewDNS was attempted but blocked, and passive DNS via SecurityTrails/RiskIQ was not used. The Tor exit attribution caveat (traffic not from this host) effectively substitutes for the cloud-provider customer-attribution caveat. Overall the investigation is operationally useful and appropriately scoped.
