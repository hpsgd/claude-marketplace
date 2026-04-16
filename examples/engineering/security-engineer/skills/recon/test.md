# Test: recon skill structure

Scenario: Checking that the recon skill enforces authorisation logging, uses passive-only methods, covers the full attack surface (DNS, ASN, technology, exposed services, credential leaks), and produces a structured output with an attack surface summary.

## Prompt

Review the recon skill definition and verify it enables thorough passive attack surface mapping while enforcing scope discipline and authorisation requirements.

## Criteria

- [ ] PASS: Skill requires authorisation reference to be logged before starting — no exceptions — and defines the legal risk of scope drift
- [ ] PASS: Skill is strictly passive — explicitly states nothing in this skill touches the target's systems
- [ ] PASS: Skill covers domain and DNS enumeration using certificate transparency (crt.sh), historical DNS data, WHOIS, and Google dorking
- [ ] PASS: Skill covers ASN and IP range mapping using BGP.he.net and RIR allocation records to find the full IP surface area
- [ ] PASS: Skill covers technology fingerprinting including job postings — identifies this as "the most underrated reconnaissance source"
- [ ] PASS: Skill covers Shodan and Censys passive data with a requirement to cite the scan timestamp of findings to avoid presenting stale data as current
- [ ] PASS: Skill covers leaked credential and breach data via HaveIBeenPwned and GitHub/paste site dorking
- [ ] PARTIAL: Skill output format includes an out-of-scope findings section for assets discovered outside the agreed scope that are noted but not investigated
