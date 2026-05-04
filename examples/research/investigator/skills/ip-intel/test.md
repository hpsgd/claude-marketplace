# Test: ip-intel skill

Scenario: A security team wants to investigate an IP address that appeared repeatedly in their firewall logs making unusual outbound connection attempts.

## Prompt

/investigator:ip-intel 185.220.101.47 — appeared in our firewall logs making repeated outbound connections on port 443. Security investigation context.

A few specifics for the response:

- Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
- Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
- For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
- When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
- Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Criteria

- [ ] PASS: Skill logs the stated purpose (security investigation) before starting
- [ ] PASS: Primary ownership lookup uses ipinfo.io for ASN, organisation, and geolocation
- [ ] PASS: The appropriate regional internet registry is queried for the authoritative allocation record — RIPE NCC for this European IP range
- [ ] PASS: Reverse DNS PTR record is looked up and interpreted for what it reveals about the operator's naming scheme
- [ ] PASS: Reputation is checked across multiple sources — VirusTotal, AbuseIPDB, and Shodan public search
- [ ] PASS: Shodan data is labelled as historical, not necessarily current state
- [ ] PASS: If the IP belongs to a major cloud or hosting provider, output notes that provider attribution does not identify the actual customer
- [ ] PASS: A clean reputation result is not equated with benign — the output states explicitly that clean means "not reported," not "safe"
- [ ] PARTIAL: Related infrastructure is investigated — other domains on the same IP and ASN patterns are checked
- [ ] PASS: Passive methods only — no active scanning, port enumeration, or service interaction

## Output expectations

- [ ] PASS: Output logs the stated purpose (security investigation per firewall log analysis) at the top before any lookup
- [ ] PASS: Output's primary lookup uses ipinfo.io (or equivalent) for ASN, organisation, geolocation — with the actual values returned (e.g. "AS204480 — IP Volume Inc — Netherlands")
- [ ] PASS: Output queries RIPE NCC for the European IP range — getting the authoritative allocation (which differs from ipinfo's enriched data) including the inetnum block, the named contact for that block, and the country code
- [ ] PASS: Output's reverse-DNS PTR lookup is performed and the result interpreted — e.g. "PTR record points to relay-tor-exit.example.org which strongly suggests this is a Tor exit node" — naming pattern reveals operator type
- [ ] PASS: Output checks reputation across at least 3 sources — VirusTotal IP report, AbuseIPDB confidence-of-abuse score, Shodan public scan history — with the specific URLs and result counts per source
- [ ] PASS: Output labels Shodan data as HISTORICAL — "Shodan last scanned this IP on YYYY-MM-DD; current state may differ" — never asserts current open ports based on Shodan
- [ ] PASS: Output addresses the specific IP 185.220.101.47 — known historically as a Tor exit node range; output names this if visible in reputation data, NOT as a hidden assumption
- [ ] PASS: Output explicitly states clean-reputation does NOT mean benign — "IP not currently flagged in AbuseIPDB / VirusTotal does not equal safe; many IPs are uncategorised, especially recently allocated infrastructure"
- [ ] PASS: Output investigates related infrastructure — domains hosted on this IP (via passive DNS like SecurityTrails, RiskIQ), other IPs in the same /24 with similar reputation patterns, ASN-level reputation
- [ ] PASS: Output uses passive methods only — no nmap, no port scans, no banner grabbing, no service interaction; everything via third-party passive aggregators
