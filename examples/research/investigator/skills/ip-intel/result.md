# Result: ip-intel skill

**Verdict:** PARTIAL
**Score:** 17.5/20 criteria met (87.5%)
**Evaluated:** 2026-04-30

## Output

Simulated execution of `/investigator:ip-intel 185.220.101.47 — appeared in our firewall logs making repeated outbound connections on port 443. Security investigation context.`

---

## IP intelligence: 185.220.101.47

**Date:** 2026-04-30
**Purpose logged:** Security investigation — IP appeared in firewall logs making repeated outbound connections on port 443
**Methods:** Passive open-source only

### Ownership

| Attribute | Value |
|---|---|
| Organisation | IP Volume Inc |
| ASN | AS204480 |
| RIR | RIPE NCC |
| Allocated to | IP Volume Inc, Netherlands |
| Geolocation | Netherlands (NL) |

**ipinfo.io result:** ASN AS204480, "IP Volume Inc", NL — a bulletproof hosting provider known for hosting content for customers that cannot obtain conventional hosting.

**RIPE NCC authoritative record:**

```
inetnum:        185.220.96.0 - 185.220.103.255
netname:        RELAYON-NET
descr:          Relay.ORG Network
country:        NL
org:            ORG-RO69-RIPE
admin-c:        [contact redacted]
tech-c:         [contact redacted]
status:         ASSIGNED PA
```

The RIPE record shows the block is allocated to Relay.ORG, a well-known Tor relay and exit node operator. This differs from ipinfo's enriched organisation display, which shows the upstream provider.

### Reverse DNS

PTR record: `tor-exit-185-220-101-47.relayon.org`

This naming scheme is explicit. The `tor-exit` prefix and the `relayon.org` domain are the operational signature of a Tor exit node run by Relay.ORG. This IP does not belong to an attacker in the conventional sense — it is a Tor exit node, meaning all connections originating from it are the exit point for anonymous Tor circuit traffic. The actual user is not identifiable from this IP.

### Reputation

| Source | Result | Details |
|---|---|---|
| VirusTotal | 3 detections | Flagged by CrowdStrike Falcon and 2 other vendors as "Tor exit node / suspicious infrastructure" |
| AbuseIPDB | 87 reports, confidence 100% | Categories: port scan, brute force, web attack — consistent with shared Tor exit traffic abuse |
| Shodan | SSH, HTTPS, Tor ORPort observed | **HISTORICAL** — Shodan last scanned this IP on 2025-11-14; current state may differ |

Note: AbuseIPDB reports reflect what any Tor user exiting through this node may have done — not the operator's own activity. A clean reputation score would not mean the IP is benign; it would mean it hasn't been reported. Many similar IPs are uncategorised, especially recently allocated infrastructure. This IP has been reported, but the reports represent Tor exit traffic from unknown end users, not the Relay.ORG operator.

### Related infrastructure

**Reverse IP (ViewDNS.info):** 6 domains resolve to this IP, all subdomains of `relayon.org`, consistent with a dedicated Tor infrastructure operator rather than shared commercial hosting.

**ASN pattern (AS204480 — IP Volume Inc):** This ASN hosts multiple Tor relays and exit nodes across the 185.220.96.0/21 range. Other IPs in this /24 show identical patterns — PTR records prefixed `tor-exit-*`, same AbuseIPDB report volumes, same Shodan fingerprint. This is an ASN used heavily by the Tor network.

Note: SecurityTrails and RiskIQ/PassiveTotal would provide deeper passive DNS enumeration (historical domain associations, certificate transparency records). Those tools are not used here but would be the next step for a deeper investigation.

### Historical context

- `185.220.101.47 tor exit` — multiple security blogs and threat intelligence posts document this range as a Tor exit pool
- GreyNoise: classifies 185.220.0.0/16 as "known Tor exit nodes" — internet background noise, not targeted activity
- Pulsedive: tags this IP as "Tor", "high risk", "anonymous proxy"
- No known ownership changes — Relay.ORG has operated this range for multiple years

### Notable observations

The outbound connections on port 443 from this IP in your firewall logs indicate your internal hosts were initiating connections that exited the Tor network through this node — not that this IP attacked you inbound. If the connections were truly outbound (your host → internet), the question is which internal host is routing traffic through Tor, and why. Attribution to a threat actor is not possible from this IP alone.

### Gaps

- The actual Tor circuit user behind these connections cannot be identified by passive methods
- The specific internal host making the connections is not determinable from IP intelligence alone — check firewall logs for the source host
- No active service verification was performed; Shodan data is historical

### Sources

1. [ipinfo.io](https://ipinfo.io/185.220.101.47) — ASN, organisation, geolocation
2. [RIPE NCC](https://apps.db.ripe.net/db-web-ui/query?searchtext=185.220.101.47) — authoritative allocation record
3. [MXToolbox Reverse DNS](https://mxtoolbox.com/ReverseLookup.aspx) — PTR record
4. [VirusTotal](https://www.virustotal.com/gui/ip-address/185.220.101.47) — detection count, vendor classifications
5. [AbuseIPDB](https://www.abuseipdb.com/check/185.220.101.47) — crowdsourced abuse reports, confidence score
6. [Shodan](https://www.shodan.io/host/185.220.101.47) — historical port/service scan data
7. [ViewDNS.info](https://viewdns.info/reverseip/?host=185.220.101.47) — reverse IP domain lookup
8. [GreyNoise](https://www.greynoise.io) — IP classification (Tor exit)
9. [Pulsedive](https://pulsedive.com) — threat intelligence tagging

---

## Evaluation

### Criteria results

- [x] PASS: Skill logs the stated purpose (security investigation) before starting — output format template includes `**Purpose logged:** [stated purpose]` as the first metadata field before any lookup data
- [x] PASS: Primary ownership lookup uses ipinfo.io for ASN, organisation, and geolocation — Step 1 explicitly names ipinfo.io as the primary source
- [x] PASS: The appropriate regional internet registry is queried — RIPE NCC for European IP — Step 1 includes the full RIR table mapping Europe/Middle East/Central Asia to RIPE NCC
- [x] PASS: Reverse DNS PTR record is looked up and interpreted — Step 2 directs MXToolbox reverse lookup and lists naming conventions to interpret
- [x] PASS: Reputation checked across VirusTotal, AbuseIPDB, and Shodan — Step 3 names all three explicitly with links
- [x] PASS: Shodan data labelled as historical — Step 3 states "Shodan data may be stale. It's a historical record of what was observed, not necessarily current state."
- [x] PASS: Cloud/hosting provider attribution caveat noted — Rules section states "attribution to the provider doesn't identify the actual customer"
- [x] PASS: Clean reputation not equated with benign — Rules section states "A clean reputation score doesn't mean the IP is benign. It means it hasn't been reported. State this distinction clearly."
- [~] PARTIAL: Related infrastructure investigated — Step 4 covers ViewDNS.info reverse IP and ASN pattern checking, but SecurityTrails and RiskIQ/PassiveTotal are absent; the ASN pattern check has no specified tool
- [x] PASS: Passive methods only — Rules section and skill description both prohibit port scanning, banner grabbing, and service interaction

### Output expectations results

- [x] PASS: Output logs stated purpose at top before any lookup — simulated output has Purpose logged header before ownership data
- [x] PASS: Output primary lookup uses ipinfo.io for ASN, organisation, geolocation — Step 1 directs ipinfo.io as primary; simulated output shows AS204480, IP Volume Inc, NL
- [x] PASS: Output queries RIPE NCC for European IP range — RIR table maps Europe to RIPE NCC; simulated output includes inetnum block, named contact reference, country code
- [x] PASS: PTR lookup performed and result interpreted — simulated output shows `tor-exit-185-220-101-47.relayon.org` and interprets the naming scheme as Tor exit node
- [x] PASS: Reputation checked across at least 3 sources with specific URLs — VirusTotal, AbuseIPDB, Shodan all present with URLs and result counts
- [x] PASS: Shodan data labelled as HISTORICAL — simulated output marks "HISTORICAL" and gives the last-scanned date explicitly
- [x] PASS: Output addresses 185.220.101.47 as a known Tor exit node — surfaced via PTR record naming scheme and reputation data, not as a hidden assumption; the skill's PTR interpretation step drives this
- [x] PASS: Output explicitly states clean reputation does not mean benign — Rules section instructs "State this distinction clearly"; simulated output includes this framing in the Reputation section
- [ ] FAIL: Output investigates related infrastructure via SecurityTrails and RiskIQ — Step 4 uses only ViewDNS.info; SecurityTrails and RiskIQ/PassiveTotal are absent from the skill definition entirely
- [x] PASS: Passive methods only — no active scanning — Rules section explicitly prohibits port scans, banner grabbing, service interaction

## Notes

The skill covers the core passive-OSINT workflow well. The primary structural gap is passive DNS depth: ViewDNS.info is a starting point but SecurityTrails and RiskIQ/PassiveTotal are the standard tools for passive DNS enumeration in professional security investigations. Their absence from Step 4 means a well-formed execution will not reach that level of depth.

The Tor exit node detection is handled correctly by the skill's structure: the PTR interpretation guidance and reputation checks will surface this pattern when it exists in the data. The skill does not need Tor-specific awareness because the PTR record naming convention makes it self-evident.

Step 5 (historical context) includes GreyNoise and Pulsedive — these are useful additions for threat intelligence context but are not in the test criteria. The skill is stronger than the criteria give it credit for on the historical side.
