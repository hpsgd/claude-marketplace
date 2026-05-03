# Recon

Scenario: Checking that the recon skill enforces authorisation logging, uses passive-only methods, covers the full attack surface (DNS, ASN, technology, exposed services, credential leaks), and produces a structured output with an attack surface summary.

## Prompt

> Review the recon skill definition and verify it enables thorough passive attack surface mapping while enforcing scope discipline and authorisation requirements.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Confirmed. The skill references the outdated v2 endpoint. Now I'll write the full assessment.

---

## Review: `security-engineer:recon`

### Verdict

**Scope discipline and authorisation enforcement: strong.** The prominent callout at the top, the mandatory Step 1 log (target, authorisation reference, exclusions), and the Rules section all reinforce the same requirement. Out-of-scope findings are handled in a dedicated output section rather than folded into the main results. This part of the skill is well-designed.

---

### Issues — prioritised

#### 1. HIBP API endpoint is outdated (factual error)

The skill references:
```
api.haveibeenpwned.com/api/v2/breachedaccount/[email]
```

The current version is **v3** (`https://haveibeenpwned.com/api/v3`). More importantly, **domain-level search requires a paid API key** — it's a "Core Pro High RPM" feature. The skill presents it as a straightforward passive lookup without flagging the subscription requirement. Per the global "flag paid services in execution paths" rule, this needs an explicit callout.

Fix: update the endpoint to v3 and note that domain search requires a paid HIBP subscription.

#### 2. Paid services not flagged

Several tools in the execution path have paid tiers that gate the useful functionality — and the skill doesn't distinguish what's free vs. what requires a subscription:

| Tool | Free tier | Paid gate |
|---|---|---|
| HaveIBeenPwned | Pwned Passwords API only | Domain search requires subscription |
| SecurityTrails | Very limited public search | Full historical DNS is paid |
| Shodan | Basic search | API access and deeper queries are paid |
| BuiltWith | Surface-level public lookup | Detailed tech data is paid |

These should be flagged inline, not buried in the tool docs. A practitioner running this skill for the first time will hit paywalls without warning.

#### 3. Major passive sources missing

These are mainline OSINT tools, not nice-to-haves:

- **Wayback Machine / archive.org** — historical snapshots of web content, removed pages, old admin paths, technology version history. Standard passive recon.
- **Passive DNS platforms** — VirusTotal (`virustotal.com/gui/domain/`) and RiskIQ/PassiveTotal provide historical DNS resolution data without touching the target. More thorough than SecurityTrails alone.
- **Reverse WHOIS** — searching other domains registered by the same registrant or organisation surfaces shadow IT and affiliated assets.

#### 4. Wappalyzer browser extension vs. public lookup

Step 4 references "Wappalyzer" without distinguishing between:
- `wappalyzer.com` public lookup — **passive** (queries Wappalyzer's own cached data)
- The browser extension — **active** (the extension fetches and analyses the target's live pages)

Using the extension breaks the passive-only constraint. The skill should specify the public lookup URL explicitly.

#### 5. Passive/active boundary: wordlist-driven subdomain enumeration

The skill correctly excludes active scanning tools (nmap, Burp, nikto). It should also explicitly state that **wordlist-driven subdomain brute forcing is out of scope** — it hits the target's authoritative name servers directly, which is active from a DNS perspective, even though it feels "passive." This is a common grey area that causes practitioner confusion.

---

### Minor omissions (nice-to-have)

- **hunter.io** — email format discovery and employee address enumeration. Useful addition to Step 7.
- **Bug bounty program pages** (HackerOne/Bugcrowd) — if the target has a public programme, it explicitly documents in-scope assets and often flags known-sensitive areas. Passive intelligence.
- **Favicon hash search** on Shodan — identifies additional hosts running the same software fingerprint.

---

### Summary

The skill's authorisation and scope discipline are its strongest features — they're well-enforced and hard to miss. The main gaps are: an outdated HIBP endpoint with an unannounced paywall, three missing mainline OSINT sources (Wayback Machine, passive DNS, reverse WHOIS), the Wappalyzer passive/active ambiguity, and no paid-tier flagging across several tools. The wordlist DNS enumeration boundary is worth one explicit sentence.

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 7.0/17.0 (41%) |
| Evaluated | 2026-05-01 |
| Target duration | 126410 ms |
| Target cost | $0.4043 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires authorisation reference to be logged before starting — no exceptions — and defines the legal risk of scope drift | PARTIAL | Output confirms 'mandatory Step 1 log (target, authorisation reference, exclusions)' and calls scope discipline 'strong,' but never explicitly verifies that the skill defines the legal risk of scope drift. |
| c2 | Skill is strictly passive — explicitly states nothing in this skill touches the target's systems | PASS | Output states 'the skill correctly excludes active scanning tools (nmap, Burp, nikto)' and frames issues #4 and #5 as violations of 'the passive-only constraint,' implying the skill explicitly states this requirement. |
| c3 | Skill covers domain and DNS enumeration using certificate transparency (crt.sh), historical DNS data, WHOIS, and Google dorking | PARTIAL | Output confirms SecurityTrails for historical DNS (and flags it as paid), and mentions WHOIS in the context of reverse WHOIS being a missing capability. crt.sh and Google dorking are not mentioned at all, so only one or two of the four required elements are confirmed. |
| c4 | Skill covers ASN and IP range mapping using BGP.he.net and RIR allocation records to find the full IP surface area | FAIL | No mention of ASN mapping, BGP.he.net, or RIR allocation records (ARIN/RIPE/APNIC/LACNIC/AFRINIC) anywhere in the captured output. |
| c5 | Skill covers technology fingerprinting including job postings — identifies this as "the most underrated reconnaissance source" | FAIL | Output mentions BuiltWith and Wappalyzer for technology fingerprinting but never references job postings as a recon source or the 'most underrated reconnaissance source' framing. |
| c6 | Skill covers Shodan and Censys passive data with a requirement to cite the scan timestamp of findings to avoid presenting stale data as current | FAIL | Shodan appears only in the paid-services table ('API access and deeper queries are paid'). Censys is not mentioned. The scan-timestamp requirement is not confirmed anywhere. |
| c7 | Skill covers leaked credential and breach data via HaveIBeenPwned and GitHub/paste site dorking | PARTIAL | HaveIBeenPwned is explicitly confirmed (issue #1 critiques the outdated v2 endpoint). GitHub/paste-site dorking is not explicitly confirmed; the output only references 'Step 7' indirectly by noting hunter.io as an addition to it. |
| c8 | Skill output format includes an out-of-scope findings section for assets discovered outside the agreed scope that are noted but not investigated | PARTIAL | Output states: 'Out-of-scope findings are handled in a dedicated output section rather than folded into the main results. This part of the skill is well-designed.' Directly confirms the criterion. |
| c9 | Output is structured as a verification of the skill (verdict per requirement) rather than running an actual recon | PASS | The response is explicitly structured as a skill review with a 'Verdict' section, numbered issues, and a summary — no actual recon targets or data are produced. |
| c10 | Output verifies the authorisation-reference-first rule — that no recon action is taken before a logged authorisation, with the legal-risk reasoning explicit | PARTIAL | Output confirms the 'mandatory Step 1 log (target, authorisation reference, exclusions)' and praises 'Scope discipline and authorisation enforcement: strong.' However, the legal-risk reasoning is never made explicit in the verification. |
| c11 | Output confirms the strictly-passive scope — every method described touches third-party data sources only, never the target's systems (no port scans, no probes) | PARTIAL | Output confirms 'the skill correctly excludes active scanning tools (nmap, Burp, nikto)' and identifies Wappalyzer extension as breaking 'the passive-only constraint,' but does not explicitly state every method touches only third-party data sources, never the target. |
| c12 | Output verifies DNS / certificate-transparency coverage names crt.sh, Censys CT search, historical DNS (SecurityTrails / DNSDumpster), WHOIS, and Google dorking — at least three of these | FAIL | Only SecurityTrails (historical DNS) is clearly named. crt.sh, Censys CT search, and Google dorking are absent. WHOIS appears only in the context of 'reverse WHOIS' being a missing feature. Fewer than three of the five required sources are confirmed. |
| c13 | Output confirms ASN / IP range mapping uses BGP.he.net and RIR allocation records (ARIN / RIPE / APNIC / LACNIC / AFRINIC) to find the full IP surface | FAIL | No mention of ASN, BGP.he.net, or any RIR (ARIN/RIPE/APNIC/LACNIC/AFRINIC) anywhere in the captured output. |
| c14 | Output confirms the technology fingerprinting section names job postings as a recon source and frames it as "the most underrated reconnaissance source" — not just BuiltWith / Wappalyzer | FAIL | BuiltWith and Wappalyzer are mentioned for technology fingerprinting. Job postings and the 'most underrated reconnaissance source' framing do not appear anywhere in the output. |
| c15 | Output verifies Shodan and Censys passive data usage requires citing the scan timestamp, with the rule that stale data must not be presented as current | FAIL | Shodan appears in the paid-services table only. Censys is not mentioned. The scan-timestamp rule and stale-data constraint are not referenced at any point. |
| c16 | Output confirms credential / breach data coverage names HaveIBeenPwned and GitHub / paste-site dorking explicitly | PARTIAL | HaveIBeenPwned is explicitly confirmed and extensively discussed (outdated v2 endpoint, paid domain-search requirement). GitHub/paste-site dorking is not explicitly named. |
| c17 | Output verifies the output format includes an out-of-scope findings section for assets discovered outside the agreed scope (noted but not investigated) | PASS | Output explicitly states: 'Out-of-scope findings are handled in a dedicated output section rather than folded into the main results.' |
| c18 | Output identifies any genuine gaps — e.g. no rule on rate-limiting passive lookups to avoid suspicion, no guidance on combining findings into an attack-surface graph, or no mention of social media / LinkedIn enumeration as a recon source | PARTIAL | Output identifies several genuine gaps: outdated HIBP endpoint, unannounced paywalls for SecurityTrails/Shodan/BuiltWith, missing Wayback Machine/passive DNS/reverse WHOIS, Wappalyzer passive/active ambiguity, wordlist subdomain enumeration boundary, hunter.io, bug bounty pages, favicon hash search. None of the three specifically mentioned examples (rate-limiting, attack-surface graph, LinkedIn) appear, but genuine gaps are identified. |

### Notes

The captured output is a competent skill critique that excels in two areas: confirming scope/authorisation discipline and flagging paid-service issues (especially the HIBP v2→v3 endpoint and unannounced paywalls). However, the review is notably shallow on the specific technical verification criteria the test rubric requires. It never mentions ASN mapping, BGP.he.net, RIR records, crt.sh, Google dorking, Censys, scan-timestamp requirements, or job-postings-as-recon-source — all of which the rubric treats as mandatory skill features. The output reads like a general OSINT review rather than a structured verification against the skill's stated requirements. The legal-risk framing is also absent despite being explicitly required by c1 and c10. The result is a 41% score, well below the PASS threshold.
