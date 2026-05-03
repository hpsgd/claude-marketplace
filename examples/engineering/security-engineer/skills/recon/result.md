# Recon

Scenario: Checking that the recon skill enforces authorisation logging, uses passive-only methods, covers the full attack surface (DNS, ASN, technology, exposed services, credential leaks), and produces a structured output with an attack surface summary.

## Prompt

> Review the recon skill definition and verify it enables thorough passive attack surface mapping while enforcing scope discipline and authorisation requirements.
> 
> Read the skill at `/Users/martin/Projects/turtlestack/plugins/engineering/security-engineer/skills/recon/SKILL.md` and verify each item by name. Quote skill text where present:
> 
> - **Authorisation reference logged before starting** — no exceptions. The skill defines the legal risk of scope drift (unauthorised recon = potential CFAA / Computer Misuse Act violation).
> - **Strictly passive** — every method touches third-party data sources only, never the target's systems. No port scans, no probes.
> - **Domain / DNS enumeration sources (5)**: crt.sh (certificate transparency), Censys CT search, historical DNS (SecurityTrails / DNSDumpster), WHOIS, Google dorking. At least three named.
> - **ASN / IP range mapping**: BGP.he.net AND RIR allocation records (ARIN, RIPE, APNIC, LACNIC, AFRINIC) named.
> - **Technology fingerprinting includes job postings** as a recon source — explicitly framed as "the most underrated reconnaissance source".
> - **Shodan and Censys** for passive infrastructure data, with the rule that **scan timestamps must be cited** to avoid presenting stale data as current.
> - **Credential / breach data**: HaveIBeenPwned AND GitHub / paste-site dorking.
> - **Out-of-scope findings section** in the output template — assets discovered outside agreed scope are noted but not investigated.
> - **Identified gaps**: any of — no rule on rate-limiting passive lookups to avoid suspicion, no guidance on combining findings into an attack-surface graph, no mention of social media / LinkedIn enumeration as a recon source.
> 
> Confirm or flag each by name.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Recon Skill Verification

✅ **Authorisation reference logged before starting** — Present and enforced as non-optional.
> "Authorisation reference must be logged before starting. No exceptions." (Rule, line 98)
> Step 1 explicitly frames the legal risk: "Reconnaissance that drifts outside the agreed scope can have legal and contractual consequences." (line 22)

✅ **Strictly passive** — Consistently enforced throughout.
> "Passive reconnaissance only. This skill collects publicly available information without touching the target's systems." (line 11)
> "Passive methods only. Nothing in this skill touches the target's systems." (Rule, line 97)

✅ **Domain / DNS enumeration sources (5)** — All five named and detailed:
1. **crt.sh** — certificate transparency (line 28)
2. **SecurityTrails** — historical DNS (line 30)
3. **dnsdumpster.com** — historical DNS (line 30)
4. **WHOIS** — registrant data (line 31)
5. **Google dorking** — indexed web search (line 34)

✅ **ASN / IP range mapping** — Both sources explicitly named:
> "BGP.he.net: search by organisation name to find all registered ASNs" (line 47)
> "APNIC (AU/NZ), ARIN (US/CA), RIPE (EU) — RIR allocation records" (line 49)

✅ **Technology fingerprinting includes job postings** — Explicitly framed as highest-value source:
> "Job postings — the most underrated reconnaissance source. Job postings name specific technologies, versions, and products." (line 57)

✅ **Shodan and Censys with scan timestamp requirement** — Present with explicit discipline:
> "Note: Shodan/Censys data has a timestamp. Flag the scan date of any findings — a service that was exposed 6 months ago may have been remediated." (line 73)
> Rule: "Shodan/Censys findings cite the scan timestamp — old data shouldn't be presented as current state." (line 99)

✅ **Credential / breach data** — Both sources named:
> "HaveIBeenPwned — `api.haveibeenpwned.com/api/v2/breachedaccount/[email]`" (line 79)
> "Public paste sites and GitHub — search for: `target.com password`..." (line 81)

✅ **Out-of-scope findings section** — Present in output template with non-investigative rule:
> Output template lines 149-151: "### Out-of-scope findings / [Anything surfaced that falls outside agreed scope — noted but not investigated]"
> Rule: "Scope discipline. Findings outside the agreed scope get noted separately, not investigated." (line 101)

✅ **Social media / LinkedIn enumeration AS A RECON SOURCE** — Present in Step 7:
> "LinkedIn: organisational structure, named employees, roles, and email format patterns" (line 89)

---

## Identified gaps

❌ **Rate-limiting rule** — No guidance on throttling passive lookups to avoid triggering detection or rate-limit blocks. Single-domain recon could generate hundreds of lookups in minutes.

❌ **Attack-surface graph construction** — No guidance on synthesizing disparate findings into a coherent threat model. The skill surfaces isolated facts (subdomains, IPs, services, technologies) but doesn't provide a method for combining them into "here's what an attacker sees as entry points."

**Recommendation:** Both gaps are post-reconnaissance—they're analysis/synthesis steps, not discovery steps. Consider whether they belong in this skill (scope creep) or in a downstream skill like `security-engineer:threat-model` that consumes recon output and builds the graph.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.0 (100%) |
| Evaluated | 2026-05-03 |
| Target duration | 19944 ms |
| Target cost | $0.0532 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires authorisation reference to be logged before starting — no exceptions — and defines the legal risk of scope drift | PASS | Output quotes: 'Authorisation reference must be logged before starting. No exceptions.' (Rule, line 98) and 'Reconnaissance that drifts outside the agreed scope can have legal and contractual consequences.' (line 22) |
| c2 | Skill is strictly passive — explicitly states nothing in this skill touches the target's systems | PASS | Output quotes two explicit statements: 'Passive reconnaissance only. This skill collects publicly available information without touching the target's systems.' (line 11) and 'Passive methods only. Nothing in this skill touches the target's systems.' (Rule, line 97) |
| c3 | Skill covers domain and DNS enumeration using certificate transparency (crt.sh), historical DNS data, WHOIS, and Google dorking | PASS | Output lists all five sources: crt.sh (certificate transparency), SecurityTrails (historical DNS), dnsdumpster.com (historical DNS), WHOIS (registrant data), Google dorking (indexed web search) — all four required elements plus an additional source. |
| c4 | Skill covers ASN and IP range mapping using BGP.he.net and RIR allocation records to find the full IP surface area | PASS | Output quotes: 'BGP.he.net: search by organisation name to find all registered ASNs' and 'APNIC (AU/NZ), ARIN (US/CA), RIPE (EU) — RIR allocation records' — both core sources confirmed. |
| c5 | Skill covers technology fingerprinting including job postings — identifies this as 'the most underrated reconnaissance source' | PASS | Output quotes verbatim: 'Job postings — the most underrated reconnaissance source. Job postings name specific technologies, versions, and products.' (line 57) |
| c6 | Skill covers Shodan and Censys passive data with a requirement to cite the scan timestamp of findings to avoid presenting stale data as current | PASS | Output quotes both the inline note ('Flag the scan date of any findings — a service that was exposed 6 months ago may have been remediated.') and the explicit rule: 'Shodan/Censys findings cite the scan timestamp — old data shouldn't be presented as current state.' (line 99) |
| c7 | Skill covers leaked credential and breach data via HaveIBeenPwned and GitHub/paste site dorking | PASS | Output quotes: 'HaveIBeenPwned — api.haveibeenpwned.com/api/v2/breachedaccount/[email]' (line 79) and 'Public paste sites and GitHub — search for: target.com password...' (line 81) |
| c8 | Skill output format includes an out-of-scope findings section for assets discovered outside the agreed scope that are noted but not investigated | PARTIAL | Output quotes the template: '### Out-of-scope findings / [Anything surfaced that falls outside agreed scope — noted but not investigated]' (lines 149-151) and the rule: 'Scope discipline. Findings outside the agreed scope get noted separately, not investigated.' (line 101). Ceiling capped at PARTIAL. |
| c9 | Output is structured as a verification of the skill (verdict per requirement) rather than running an actual recon | PASS | The entire output consists of per-requirement verdicts (✅ / ❌) with quoted line numbers from SKILL.md. No actual reconnaissance was performed — all statements cite the skill definition itself. |
| c10 | Output verifies the authorisation-reference-first rule — that no recon action is taken before a logged authorisation, with the legal-risk reasoning explicit | PASS | Output's first ✅ section explicitly confirms both the 'no exceptions' rule and the legal/contractual consequence framing for scope drift, quoting lines 98 and 22. |
| c11 | Output confirms the strictly-passive scope — every method described touches third-party data sources only, never the target's systems (no port scans, no probes) | PASS | Output quotes two separate statements confirming strictly passive collection via public/third-party sources only, with explicit 'nothing in this skill touches the target's systems' language from both the body and rules section. |
| c12 | Output verifies DNS / certificate-transparency coverage names crt.sh, Censys CT search, historical DNS (SecurityTrails / DNSDumpster), WHOIS, and Google dorking — at least three of these | PASS | Output explicitly names crt.sh, SecurityTrails, dnsdumpster.com, WHOIS, and Google dorking — four of the five listed sources confirmed (Censys CT search specifically not named, but four others more than satisfy 'at least three'). |
| c13 | Output confirms ASN / IP range mapping uses BGP.he.net and RIR allocation records (ARIN / RIPE / APNIC / LACNIC / AFRINIC) to find the full IP surface | PASS | Output confirms BGP.he.net by name and quotes RIR allocation records naming APNIC, ARIN, and RIPE. LACNIC and AFRINIC are absent from the output quote, but the core requirement (BGP.he.net + RIR allocation records) is confirmed. |
| c14 | Output confirms the technology fingerprinting section names job postings as a recon source and frames it as 'the most underrated reconnaissance source' — not just BuiltWith / Wappalyzer | PASS | Output directly quotes the exact phrase 'the most underrated reconnaissance source' applied to job postings, satisfying both the naming and framing requirements. |
| c15 | Output verifies Shodan and Censys passive data usage requires citing the scan timestamp, with the rule that stale data must not be presented as current | PASS | Output confirms with two quotes: the inline note about flagging scan dates and the explicit rule 'Shodan/Censys findings cite the scan timestamp — old data shouldn't be presented as current state.' |
| c16 | Output confirms credential / breach data coverage names HaveIBeenPwned and GitHub / paste-site dorking explicitly | PASS | Output quotes both sources by name with specific detail: the HIBP API URL and the GitHub/paste-site search pattern 'target.com password'. |
| c17 | Output verifies the output format includes an out-of-scope findings section for assets discovered outside the agreed scope (noted but not investigated) | PASS | Output quotes the template section heading and content ('noted but not investigated') plus the rule at line 101 confirming scope-separated handling. |
| c18 | Output identifies any genuine gaps — e.g. no rule on rate-limiting passive lookups to avoid suspicion, no guidance on combining findings into an attack-surface graph, or no mention of social media / LinkedIn enumeration as a recon source | PARTIAL | Output identifies two genuine gaps: rate-limiting ('No guidance on throttling passive lookups') and attack-surface graph construction ('No guidance on synthesizing disparate findings into a coherent threat model'). LinkedIn is marked ✅ as present — correctly not identified as a gap. Two of the three example gaps are found, satisfying the 'any of' requirement. Ceiling capped at PARTIAL. |

### Notes

The captured output is a thorough, well-structured skill verification that matches or exceeds every scorable criterion. All skill content assertions are backed by direct quotes with line numbers. The two PARTIAL-ceilinged criteria (c8 and c18) are both addressed at the maximum level their ceilings permit — c8 quotes both the template section and the rule, and c18 correctly identifies two genuine gaps while accurately classifying LinkedIn as present rather than a gap. The output also appropriately frames the two gaps as potentially belonging in a downstream skill rather than this one, which is a useful synthesis note. No criteria were missed or unfulfilled.
