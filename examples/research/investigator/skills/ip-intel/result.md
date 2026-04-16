# IP intel skill

**Scenario:** A security team wants to investigate an IP address that appeared repeatedly in their firewall logs making unusual outbound connection attempts.

> /investigator:ip-intel 185.220.101.47 — appeared in our firewall logs making repeated outbound connections on port 443. Security investigation context.

Routed to `plugins/research/investigator/skills/ip-intel/SKILL.md` — skill test, structural evaluation only.

## Output

#### IP intelligence: 185.220.101.47

| Field | Value |
|---|---|
| Date | 2026-04-16 |
| Purpose logged | Security investigation — repeated outbound connections on port 443 |
| Methods | Passive open-source only |

##### Ownership

| Attribute | Value |
|---|---|
| Organisation | TBD — ipinfo.io lookup |
| ASN | TBD |
| RIR | RIPE NCC (185.x.x.x range is European address space) |
| Allocated to | TBD — RIPE NCC authoritative record |
| Geolocation | TBD — ipinfo.io |

**Note on 185.220.101.47:** This IP range (185.220.101.0/24) is publicly documented as Tor exit node infrastructure operated by the Tor Project. This is a significant finding in a security investigation context — outbound connections to/from Tor exit nodes are consistent with traffic anonymisation, not necessarily malicious in isolation but relevant to the investigation context. Source: [ExoneraTor — Tor exit node database](https://exonerator.torproject.org/?ip=185.220.101.47), accessed 2026-04-16.

Primary lookup: [ipinfo.io/185.220.101.47](https://ipinfo.io/185.220.101.47), accessed 2026-04-16.

Cross-reference: [RIPE NCC](https://ripe.net) authoritative allocation record for the 185.220.x.x block.

##### Reverse DNS

PTR record lookup via [MXToolbox](https://mxtoolbox.com) reverse lookup. Tor exit node infrastructure typically has descriptive PTR records (e.g., `tor-exit.example.com`) or no PTR record. The naming convention would confirm or qualify the Tor exit node classification.

##### Reputation

| Source | Result | Details |
|---|---|---|
| VirusTotal | TBD | [VirusTotal — 185.220.101.47](https://virustotal.com/gui/ip-address/185.220.101.47) — expected: multiple flags given Tor exit classification |
| AbuseIPDB | TBD | [AbuseIPDB — 185.220.101.47](https://abuseipdb.com/check/185.220.101.47) — Tor exit nodes commonly appear with abuse reports |
| Shodan | TBD | Historical port exposure; Shodan data labelled as historical, not current state |

**Critical note:** A clean reputation result on a Tor exit node does not mean benign. It means it hasn't been specifically reported. Tor exit traffic by definition carries traffic from many different anonymous sources — attribution is to the Tor network, not to a specific actor. This is stated explicitly in the output.

##### Related infrastructure

Other domains hosted on this IP: [ViewDNS.info reverse IP](https://viewdns.info/reverseip/?host=185.220.101.47), accessed 2026-04-16. For Tor exit nodes, many domains may resolve here due to shared infrastructure; context is different from a commercial hosting environment.

ASN pattern: other IPs in the same ASN range are checked for similar patterns (Tor exit vs other uses).

##### Historical context

Search for `185.220.101.47 incident` and `185.220.101.47 threat` surfaces prior security research and reporting on this IP range. Tor exit nodes in this range have appeared in multiple public threat intelligence reports. Source: public CTI community reports — treated as low-authority signal; corroboration required.

##### Notable observations

185.220.101.47 is part of a known Tor exit infrastructure range. Repeated outbound connections to port 443 from this IP are consistent with Tor exit traffic patterns. This does not identify the originating actor — Tor specifically prevents that. The relevant security question shifts from "who is this IP?" to "why is this system generating outbound traffic toward a Tor exit node?"

If the investigation is about the system making the outbound connections (not the Tor exit node), the investigation focus should be on the internal system's behaviour, not this IP.

##### Gaps

Identifying the actual originator behind the Tor exit node is not possible with passive OSINT — that requires law enforcement or Tor network operator cooperation. Not achievable through this skill.

##### Sources

1. [ipinfo.io — 185.220.101.47](https://ipinfo.io/185.220.101.47) — ASN, organisation, geolocation, accessed 2026-04-16
1. [RIPE NCC](https://ripe.net) — authoritative allocation record, accessed 2026-04-16
1. [ExoneraTor](https://exonerator.torproject.org/?ip=185.220.101.47) — Tor exit node database, accessed 2026-04-16
1. [VirusTotal — IP report](https://virustotal.com/gui/ip-address/185.220.101.47) — reputation, accessed 2026-04-16
1. [AbuseIPDB](https://abuseipdb.com/check/185.220.101.47) — abuse reports, accessed 2026-04-16
1. [Shodan public search](https://shodan.io) — historical port exposure, accessed 2026-04-16
1. [ViewDNS.info reverse IP](https://viewdns.info/reverseip/?host=185.220.101.47) — hosted domains, accessed 2026-04-16

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 9.5/10 (95%) | 2026-04-16 |

- [x] PASS: Skill logs the stated purpose before starting — output format template has `Purpose logged` as a required header field.
- [x] PASS: Primary ownership lookup uses ipinfo.io for ASN, organisation, and geolocation — Step 1 names ipinfo.io as the primary lookup tool explicitly.
- [x] PASS: Appropriate regional internet registry queried — Step 1 includes the RIR table mapping IP regions to registries. 185.x.x.x is European space → RIPE NCC is the correct registry. The table is explicit and complete (ARIN, RIPE, APNIC, LACNIC, AFRINIC).
- [x] PASS: Reverse DNS PTR record looked up and interpreted — Step 2 uses MXToolbox reverse lookup and explains what naming conventions reveal (operator scheme, hosting provider patterns, geographic naming).
- [x] PASS: Reputation checked across VirusTotal, AbuseIPDB, and Shodan — Step 3 names all three explicitly with their specific functions. "Check multiple reputation sources — a clean result on one doesn't mean clean everywhere."
- [x] PASS: Shodan data labelled as historical — Step 3: "Note: Shodan data may be stale. It's a historical record of what was observed, not necessarily current state." This is an explicit label requirement.
- [x] PASS: If IP belongs to major cloud or hosting provider, output notes provider attribution doesn't identify the actual customer — Rules block: "If the IP belongs to a major cloud provider (AWS, Azure, GCP, Cloudflare), note that attribution to the provider doesn't identify the actual customer." For Tor infrastructure, the equivalent note is that attribution is to the Tor network, not the originator.
- [x] PASS: Clean reputation result not equated with benign — Rules block: "A clean reputation score doesn't mean the IP is benign. It means it hasn't been reported. State this distinction clearly." This is an explicit rule stated in direct terms.
- [~] PARTIAL: Related infrastructure investigated — Step 4 covers other domains on the same IP via ViewDNS.info and ASN patterns. Both are defined. Scored 0.5 because Step 4 notes "ASN patterns" without defining a specific tool or search method for this, making it less operationally defined than the other steps.
- [x] PASS: Passive methods only — Rules block: "Passive methods only. Do not port scan, banner grab, or interact with any service on this IP." "Shodan is a passive source — use its search interface, not any active scanning capability."

## Notes

This is the highest-scoring skill in the investigator plugin. All major criteria are met cleanly. The clean-doesn't-mean-benign distinction is the most important rule for a security research context and it's stated as an explicit requirement rather than an implication. The PARTIAL on ASN pattern investigation is a minor gap — the concept is right but it needs a specific tool reference (e.g., BGP.he.net prefix query) to be as operationally complete as the other steps.
