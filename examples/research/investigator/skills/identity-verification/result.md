# Identity verification skill

**Scenario:** A law firm is verifying that a consultant claiming to be a registered financial adviser with ASIC is who they say they are, before engaging them.

> /investigator:identity-verification Dr Priya Narayanan claims to be a licensed financial adviser registered with ASIC, previously at Macquarie Wealth Management, based in Sydney

Routed to `plugins/research/investigator/skills/identity-verification/SKILL.md` — skill test, structural evaluation only.

## Output

> [!IMPORTANT]
> This skill requires the investigator agent's full authorisation gate before invocation. The gate record must be logged before any verification steps begin.

**Gate record (assumed complete from the investigator agent):**

```
Authorisation:  Legal counsel — law firm engaging a consultant.
Purpose:        Pre-engagement credential verification for financial adviser.
Scope:          Professional credentials (ASIC registration, Macquarie employment),
                location (Sydney, professional context only). Personal life out of scope.
Subject aware:  Yes — standard pre-engagement due diligence.
```

---

#### Identity verification: Dr Priya Narayanan

**Gate record:** Logged above.

**Claims to verify:**
1. Licensed financial adviser registered with ASIC
2. Previously at Macquarie Wealth Management
3. Based in Sydney

---

##### Verification results

| Claim | Status | Evidence | Source |
|---|---|---|---|
| ASIC financial adviser registration | TBD — registry checked | Search result from ASIC Financial Advisers Register | [ASIC Financial Advisers Register](https://moneysmart.gov.au/financial-advice/financial-advisers-register), accessed 2026-04-16 |
| Previously at Macquarie Wealth Management | TBD — LinkedIn and Macquarie website checked | LinkedIn profile consistency; Macquarie employee list | [LinkedIn search](https://linkedin.com), accessed 2026-04-16; [Macquarie Group website](https://macquarie.com), accessed 2026-04-16 |
| Sydney-based (professional context) | TBD | LinkedIn profile location; professional registry address | LinkedIn; ASIC register |

**Key verification note — ASIC register:** The ASIC Financial Advisers Register is publicly searchable by name. If a person is a current or former licensed financial adviser, they must appear in this register under the Corporations Act 2001 (AU). "Not found in registry" is not the same as "invalid credential" — the person may be authorised through a licensee rather than holding their own AFS licence. The skill's disambiguation approach distinguishes these cases.

**Key verification note — Macquarie employment:** Macquarie does not maintain a public ex-employee directory. Verification relies on LinkedIn profile consistency (employer history claimed on their profile matching what Macquarie's public team pages or press mentions show) and whether the ASIC register lists Macquarie as a former licensing entity for the adviser.

##### Cross-reference consistency

Photo consistency across LinkedIn and any professional conference or media appearances is noted as a visual observation only — no speculation beyond what can be observed.

Timeline consistency: ASIC register would show the periods of financial adviser registration; LinkedIn employment history would need to align with those periods. Gaps would be flagged.

##### Disambiguation

"Dr Priya Narayanan" combined with "Macquarie Wealth Management" and "Sydney" provides sufficient context anchors to disambiguate in the ASIC register and LinkedIn search. If multiple matches found after three attempts with context anchors: stop, report ambiguity, ask for additional context (e.g., employee number, specialisation, specific years at Macquarie).

##### Inconsistencies

Any discrepancy between what the subject claims and what the ASIC register and LinkedIn sources show would be noted here, with explicit distinction between "unverifiable" (no evidence either way) and "contradicted" (evidence actively contradicts the claim).

##### Confidence assessment

**Overall confidence:** High / Medium / Low — determined by:
- Whether ASIC registration found and current/lapsed status confirmed
- Whether Macquarie employment is consistent across at least two independent sources
- Whether photo and location consistency is noted

---

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 9/9 (100%) | 2026-04-16 |

- [x] PASS: Skill requires and references an authorisation gate record before proceeding — the `[!IMPORTANT]` callout at the top of the skill: "This skill requires the investigator agent's full authorisation gate before invocation. Do not run without a logged gate record." The gate record is a hard precondition.
- [x] PASS: Skill starts from the subject's specific claims, not an open-ended search — Step 1: "Start with what the subject has claimed — not with a general search... List each claim explicitly before verifying any of them. Unanchored searches produce noise; anchored searches produce evidence." Output format has `Claims to verify` as a named section.
- [x] PASS: ASIC Financial Advisers Register checked for the adviser licence claim — Step 2 "Credential verification" lists: "AU financial advisers: ASIC Financial Advisers Register" with the specific URL. This is an explicit named registry for this claim type.
- [x] PASS: Employer verification searches Macquarie's own website and LinkedIn for consistency — Step 2 "Employer verification" requires searching "the company's own website for the person (team pages, leadership, press releases, bylines)" and "LinkedIn for consistency between the person's profile and the company's employee list."
- [x] PASS: Photo consistency checked and described as visual observation, no speculation — Step 3 "Cross-reference identifiers" includes "Photo consistency — does the same face appear on LinkedIn, company site, conference appearances?" Rules: "Photo comparison is visual only — note photo consistency across sources; don't speculate beyond what you can observe."
- [x] PASS: Skill distinguishes "unverifiable" from "contradicted" — Step 5 "Flag inconsistencies": "Distinguish clearly between 'unverifiable' (no public evidence either way) and 'contradicted' (evidence that the claim is false)." This distinction is explicit and named in the skill. Output format includes it as a named sub-field under Inconsistencies.
- [x] PASS: Name disambiguation documented, investigation stops if ambiguity persists after three attempts — Step 4: three-step disambiguation with context anchors. "Failure condition: after 3 attempts with different context anchors, ambiguity persists. Stop and ask for additional context rather than guessing."
- [x] PASS: Output uses structured format with verification results table, cross-reference consistency section, and overall confidence rating — output format template has all three: `Verification results` table, `Cross-reference consistency` section, and `Confidence assessment` section.
- [x] PASS: Skill does not expand into personal life details beyond professional claims — Rules: "Start from the subject's claims, not from an open search. You're verifying, not profiling." Scope is limited to the professional claims in the gate record.

## Notes

The identity-verification skill is one of the most precisely defined skills in the collection. The explicit distinction between "unverifiable" and "contradicted" is important and often missed in less careful implementations. The three-attempt disambiguation failure condition is a good structural safeguard against reporting on the wrong person. The ASIC Financial Advisers Register is the right primary source for this claim type and it's correctly named.
