# Test: ip-intel skill

Scenario: A security team wants to investigate an IP address that appeared repeatedly in their firewall logs making unusual outbound connection attempts.

## Prompt

/investigator:ip-intel 185.220.101.47 — appeared in our firewall logs making repeated outbound connections on port 443. Security investigation context.

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
