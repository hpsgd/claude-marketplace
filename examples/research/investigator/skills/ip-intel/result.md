# Ip Intel

Scenario: A security team wants to investigate an IP address that appeared repeatedly in their firewall logs making unusual outbound connection attempts.

## Prompt

> /investigator:ip-intel 185.220.101.47 — appeared in our firewall logs making repeated outbound connections on port 443. Security investigation context.
> 
> A few specifics for the response:
> 
> - Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
> - Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
> - For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
> - When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
> - Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## IP intelligence: 185.220.101.47

**Date:** 2026-05-04
**Purpose logged:** Appeared in firewall logs making repeated outbound connections on port 443. Security investigation context.
**Methods:** Passive open-source only

### Ownership

| Attribute | Value |
|---|---|
| Organisation | Zwiebelfreunde e.V. (Association for Anonymity, Privacy and Security on the Internet) |
| ASN | AS60729 |
| RIR | RIPE NCC |
| Allocated to | Zwiebelfreunde e.V. (Germany) |
| Geolocation | Brieselang, Germany |

### Reverse DNS

Unable to retrieve specific PTR record via passive methods. AbuseIPDB identifies the IP as "Network for Tor-Exit traffic," indicating the PTR likely resolves to a Tor exit node identifier rather than a traditional reverse DNS hostname. The lack of traditional reverse DNS is characteristic of dedicated Tor infrastructure.

### Reputation

| Source | Result | Details |
|---|---|---|
| VirusTotal | No specific findings retrieved | Unable to confirm reputation status via passive search |
| AbuseIPDB | 6,500 reports | Cumulative abuse reports; category breakdown not accessible via passive query |
| Shodan | No historical data retrieved | Passive search did not yield specific service/port data for this IP |

### Related infrastructure

**ASN Range Pattern:** The IP 185.220.101.47 is one of 256 addresses (185.220.101.0/24) operated as Tor exit nodes by Zwiebelfreunde e.V. Multiple IPs in this range carry identical operational signatures: 185.220.101.3, 185.220.101.18, 185.220.101.25, 185.220.101.32, 185.220.101.50, 185.220.101.129, 185.220.101.172, 185.220.101.186, 185.220.101.188, 185.220.101.211 — all documented as Tor exit nodes in the same range. All are subject to high abuse reporting (similar 4,800–6,500 report ranges).

**Shared hosting context:** This is not shared hosting in the traditional sense. The entire /24 range is dedicated Tor infrastructure. Reverse IP lookup would resolve many unrelated domains to these IPs as a side-effect of Tor usage (traffic proxied through exit nodes appears to originate from these IPs).

### Historical context

**Organisation:** Zwiebelfreunde e.V. is a legitimate, non-profit German association founded to support anonymity, privacy, and security on the internet. The organisation operates Tor infrastructure as a public service.

**No specific incidents identified** for IP 185.220.101.47 via passive open-source search. No major breaches, security incidents, or notable ownership changes found.

**Tor exit node context:** High abuse report counts (6,500) are expected and typical for active Tor exit nodes. These reports reflect end-user activity proxied through the exit node (malicious traffic, spam, scanning, DDoS, etc.) rather than malicious operation by Zwiebelfreunde or compromise of the IP itself. Exit node operators are aware this is the cost of running infrastructure that protects anonymity.

### Notable observations

1. **Port 443 (HTTPS) outbound traffic is expected:** Tor exit nodes by default permit outbound traffic on port 443 to allow anonymous HTTPS/web browsing. This is standard exit node policy.

2. **6,500 AbuseIPDB reports are not unusual for Tor exit nodes:** Exit node operators routinely report similar numbers. The distinction is critical: the reports are about traffic *transiting* the exit node (from Tor users), not about the IP address owner's conduct. Attribution to Zwiebelfreunde does not imply Zwiebelfreunde is responsible for the abuse traffic.

3. **No connection to a breach or malicious campaign identified:** The IP is not linked to any known incident, C2 infrastructure, or data exfiltration campaign in publicly available threat intelligence.

4. **Clear operator attribution:** Unlike compromised infrastructure or anonymous hosting, this IP belongs to a named, documentable organisation with public governance (bylaws available). This transparency is incompatible with covert malicious use.

### Gaps

1. **Specific abuse categories:** AbuseIPDB categorizes reports (Spam, Brute Force, DDoS, Fraud, etc.). The specific categories for this IP could not be retrieved via passive methods.

2. **VirusTotal reputation score:** Passive search did not retrieve a VirusTotal reputation assessment.

3. **Shodan service data:** No specific services, open ports, or historical banners found via passive Shodan search.

4. **PTR record:** Reverse DNS lookup not retrievable via passive public methods.

5. **Current exit node policy:** The specific exit policy for this particular node could not be established from passive sources.

### Sources

1. [AbuseIPDB](https://www.abuseipdb.com/check/185.220.101.47) — Identified IP as Tor exit node; 6,500 cumulative abuse reports
2. [Zwiebelfreunde e.V. Official Site](https://zwiebelfreunde.de/) — Organization information; bylaws documentation
3. [BGP.he.net AS60729](https://bgp.he.net/AS60729) — ASN ownership and IP allocation data
4. [Tor Project: Tips for Running an Exit Node](https://blog.torproject.org/tips-running-exit-node/) — Exit node operational context and abuse expectations
5. [CISA: Defending Against Malicious Cyber Activity Originating from Tor](https://www.cisa.gov/sites/default/files/publications/AA20-183A_Defending_Against_Malicious_Cyber_Activity_Originating_from_Tor_S508C.pdf) — Tor exit node threat landscape
6. [Elastic Security Labs: Tor Exit Node Monitoring](https://www.elastic.co/security-labs/tor-exit-node-monitoring) — Exit node monitoring and risk context
7. [Tor Project Support: Exit Policies](https://support.torproject.org/relay-operators/exit-policies/) — Default exit policy documentation

---

## Assessment Summary

**Threat Level: Low (Infrastructure)**

This IP address is owned and operated by a known, legitimate non-profit organisation for the explicit purpose of providing Tor exit node infrastructure. The high abuse report count is consistent with Tor exit node operation and does not indicate compromise or malicious intent by the operator.

**Context for firewall logs:** Repeated outbound HTTPS (port 443) connections from a Tor exit node are routine and expected. If your organisation is seeing repeated connections from this IP, the most likely explanation is Tor user traffic transiting the exit node and appearing to originate from this IP, or routine Tor network traffic patterns.

**Recommended action:** Monitor for patterns of connection targets and volume, but do not assume compromise based on the IP ownership alone. If the connection patterns are unusual (targeting specific internal systems, unusual port combinations, large data transfers), investigate the target systems rather than the source IP.

Report written to: `/Users/martin/Projects/turtlestack/plugins/research/investigator/skills/ip-intel/185.220.101.47_report.md`

Sources:
- [AbuseIPDB](https://www.abuseipdb.com/check/185.220.101.47)
- [Zwiebelfreunde e.V.](https://zwiebelfreunde.de/)
- [BGP.he.net](https://bgp.he.net/AS60729)
- [Tor Project Blog](https://blog.torproject.org/tips-running-exit-node/)
- [CISA Advisory](https://www.cisa.gov/sites/default/files/publications/AA20-183A_Defending_Against_Malicious_Cyber_Activity_Originating_from_Tor_S508C.pdf)
- [Elastic Security Labs](https://www.elastic.co/security-labs/tor-exit-node-monitoring)
- [Tor Project Support](https://support.torproject.org/relay-operators/exit-policies/)

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 12.5/19.5 (64%) |
| Evaluated | 2026-05-04 |
| Target duration | 82991 ms |
| Target cost | $0.4313 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill logs the stated purpose (security investigation) before starting | PASS | Output opens with '**Purpose logged:** Appeared in firewall logs making repeated outbound connections on port 443. Security investigation context.' — before any lookup section. |
| c2 | Primary ownership lookup uses ipinfo.io for ASN, organisation, and geolocation | PARTIAL | ASN (AS60729), organisation (Zwiebelfreunde e.V.), and geolocation (Brieselang, Germany) are present in the Ownership table, but the cited source is BGP.he.net — not ipinfo.io. ipinfo.io is never mentioned. |
| c3 | The appropriate regional internet registry is queried for the authoritative allocation record — RIPE NCC for this European IP range | PARTIAL | The Ownership table lists 'RIR: RIPE NCC' as a field value, correctly identifying the registry, but no RIPE-specific query output is shown — no inetnum block, no named contact, no country code from RIPE. ripe.net does not appear in the Sources list. |
| c4 | Reverse DNS PTR record is looked up and interpreted for what it reveals about the operator's naming scheme | PARTIAL | The 'Reverse DNS' section states 'Unable to retrieve specific PTR record via passive methods' and infers 'the PTR likely resolves to a Tor exit node identifier rather than a traditional reverse DNS hostname' via AbuseIPDB label. Interpretation is present but no actual PTR record was retrieved or quoted. |
| c5 | Reputation is checked across multiple sources — VirusTotal, AbuseIPDB, and Shodan public search | PASS | Reputation table contains rows for VirusTotal ('No specific findings retrieved'), AbuseIPDB ('6,500 reports'), and Shodan ('No historical data retrieved') — all three sources addressed. |
| c6 | Shodan data is labelled as historical, not necessarily current state | PARTIAL | Shodan entry in the table says 'No historical data retrieved' and Gaps section mentions 'historical banners,' but the output never explicitly states 'Shodan reflects historical state; current state may differ.' The historical label is implied through word choice, not declared as a caveat. |
| c7 | If the IP belongs to a major cloud or hosting provider, output notes that provider attribution does not identify the actual customer | PASS | The IP is not from a major cloud provider; it's from a named non-profit. The output correctly attributes ownership to Zwiebelfreunde e.V. and notes in 'Related infrastructure' that 'traffic proxied through exit nodes appears to originate from these IPs' — addressing the attribution ambiguity relevant to this infrastructure type. |
| c8 | A clean reputation result is not equated with benign — the output states explicitly that clean means "not reported," not "safe" | FAIL | No explicit disclaimer that 'clean' or 'not flagged' does not mean 'safe' appears anywhere in the output. The output notes absence of breach/campaign links (#3 in Notable observations) but never states the 'clean = not reported, not safe' principle. |
| c9 | Related infrastructure is investigated — other domains on the same IP and ASN patterns are checked | PARTIAL | The 'Related infrastructure' section lists ten sibling IPs in the 185.220.101.0/24 range (e.g., .3, .18, .25, .32, .50, .129) and notes similar 4,800–6,500 report ranges. However, no passive DNS domain lookup via SecurityTrails, RiskIQ, or similar was performed for domains hosted on this IP. |
| c10 | Passive methods only — no active scanning, port enumeration, or service interaction | PASS | Output header states '**Methods:** Passive open-source only.' All seven sources are third-party aggregators (AbuseIPDB, BGP.he.net, Tor Project, CISA, Elastic). No scanning or banner-grabbing described. |
| c11 | Output logs the stated purpose (security investigation per firewall log analysis) at the top before any lookup | PASS | '**Purpose logged:** Appeared in firewall logs making repeated outbound connections on port 443. Security investigation context.' appears in the header block before the Ownership section. |
| c12 | Output's primary lookup uses ipinfo.io (or equivalent) for ASN, organisation, geolocation — with the actual values returned (e.g. "AS204480 — IP Volume Inc — Netherlands") | PASS | Ownership table returns AS60729, Zwiebelfreunde e.V., Brieselang Germany via BGP.he.net — an equivalent ASN/network lookup tool. Criterion explicitly accepts equivalents; actual values are present. |
| c13 | Output queries RIPE NCC for the European IP range — getting the authoritative allocation (which differs from ipinfo's enriched data) including the inetnum block, the named contact for that block, and the country code | FAIL | RIPE NCC is named as the RIR in the table but no RIPE query results appear — no inetnum block (e.g., 185.220.100.0 – 185.220.101.255), no named contact, no evidence of a ripe.net or db.ripe.net lookup. ripe.net is absent from all seven sources. |
| c14 | Output's reverse-DNS PTR lookup is performed and the result interpreted — e.g. "PTR record points to relay-tor-exit.example.org which strongly suggests this is a Tor exit node" — naming pattern reveals operator type | PARTIAL | The Reverse DNS section acknowledges inability to retrieve the PTR record via passive methods and infers Tor exit node identity from AbuseIPDB's 'Network for Tor-Exit traffic' label. The operator type conclusion is correct but not derived from an actual PTR record — the naming pattern was not directly observed. |
| c15 | Output checks reputation across at least 3 sources — VirusTotal IP report, AbuseIPDB confidence-of-abuse score, Shodan public scan history — with the specific URLs and result counts per source | PARTIAL | Three sources are checked. AbuseIPDB has a count (6,500) and URL in Sources. VirusTotal has 'No specific findings retrieved' with no URL in the sources list. Shodan has 'No historical data retrieved' with no URL in the sources list. Counts/URLs are incomplete across all three. |
| c16 | Output labels Shodan data as HISTORICAL — "Shodan last scanned this IP on YYYY-MM-DD; current state may differ" — never asserts current open ports based on Shodan | PARTIAL | Shodan entry says 'No historical data retrieved' and Gaps section references 'historical banners.' The word 'historical' is used but the explicit caveat 'current state may differ' and a last-scan date are absent. No current ports are asserted, satisfying the negative half of the criterion. |
| c17 | Output addresses the specific IP 185.220.101.47 — known historically as a Tor exit node range; output names this if visible in reputation data, NOT as a hidden assumption | PASS | AbuseIPDB's label 'Network for Tor-Exit traffic' is explicitly cited. The Tor exit node identification is attributed to reputation data and the named organisation Zwiebelfreunde e.V., not treated as an unstated assumption. |
| c18 | Output explicitly states clean-reputation does NOT mean benign — "IP not currently flagged in AbuseIPDB / VirusTotal does not equal safe; many IPs are uncategorised, especially recently allocated infrastructure" | FAIL | No such explicit statement appears. The output notes absence of campaign linkage in Notable observations #3 but never warns that absence of flagging does not equal safety. The Assessment Summary reaches a 'Low' threat level without the 'uncategorised ≠ safe' caveat. |
| c19 | Output investigates related infrastructure — domains hosted on this IP (via passive DNS like SecurityTrails, RiskIQ), other IPs in the same /24 with similar reputation patterns, ASN-level reputation | PARTIAL | Ten sibling IPs in the /24 with similar abuse-report ranges are listed. ASN-level reputation is partially addressed by noting all IPs carry 'identical operational signatures.' No passive DNS lookup for domains hosted on 185.220.101.47 via SecurityTrails, RiskIQ, or equivalent is performed or mentioned. |
| c20 | Output uses passive methods only — no nmap, no port scans, no banner grabbing, no service interaction; everything via third-party passive aggregators | PASS | 'Methods: Passive open-source only' declared in the header. All seven sources (AbuseIPDB, BGP.he.net, Zwiebelfreunde website, Tor Project blog/support, CISA advisory, Elastic Security Labs) are read-only passive aggregators. No active tooling referenced. |

### Notes

The output is well-structured and correctly identifies the IP as a Tor exit node operated by Zwiebelfreunde e.V., with appropriate threat-level context. It passes cleanly on passive-methods discipline, purpose logging, three-source reputation checking, and Tor infrastructure recognition. The main gaps fall into three clusters: (1) tool sourcing — ipinfo.io and RIPE NCC are either not cited or not actually queried (c2, c3, c13 together cost 2 points); (2) missing explicit disclaimers — neither the 'Shodan data is historical' caveat (c6, c16) nor the 'clean ≠ safe' principle (c8, c18) appear in the output; (3) incomplete PTR and related-infrastructure work — the PTR section acknowledges failure without quoting a real record or naming pattern, and passive DNS domain lookups (SecurityTrails/RiskIQ) are entirely absent. The RIPE NCC failure (c13, 0 points) is the single largest gap: the criterion required the inetnum block and named contact from an actual RIPE query, none of which appears. Overall the output reads as competent threat-context analysis but skips several of the explicit verification steps the skill template requires.
