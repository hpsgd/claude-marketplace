---
name: identity-verification
description: "Verify that a named individual is who they claim to be, or resolve ambiguity between people sharing a name. Anchors on verifiable claims and cross-references independently. Requires authorisation gate."
argument-hint: "[person name] claims to be [role/employer/credential]"
user-invocable: true
allowed-tools: WebSearch, WebFetch
---

Verify the identity of $ARGUMENTS using public sources.

> [!IMPORTANT]
> This skill requires the investigator agent's full authorisation gate before invocation. Do not run without a logged gate record.

## Step 1: Anchor on verifiable claims

Start with what the subject has claimed — not with a general search. Claims to verify might include:

- Current employer and role
- Credentials and qualifications
- Publications or public work
- Location or operational base

List each claim explicitly before verifying any of them. Unanchored searches produce noise; anchored searches produce evidence.

## Step 2: Verify each claim independently

For each claim:

**Employer verification:**
- Search the company's own website for the person (team pages, leadership, press releases, bylines)
- Check LinkedIn for consistency between the person's profile and the company's employee list
- Look for the person mentioned in company announcements or press coverage

**Credential verification:**
- Professional licensing boards (see people-lookup skill for the full AU/NZ/US registry list)
- Academic institutions for degree claims — faculty pages, alumni directories
- For specific accreditations: the issuing body's public registry or verification page
- AU health practitioners: [AHPRA](https://www.ahpra.gov.au) register (publicly searchable)
- AU financial advisers: [ASIC Financial Advisers Register](https://moneysmart.gov.au/financial-advice/financial-advisers-register)

**Publication verification:**
- [Google Scholar](https://scholar.google.com), [ORCID](https://orcid.org), [ResearchGate](https://www.researchgate.net)
- The specific journal or publisher's website for the claimed work
- Conference proceedings for claimed conference presentations

## Step 3: Cross-reference identifiers

Strong identity confirmation comes from consistent identifiers across independent sources:

- **Photo consistency** — does the same face appear on LinkedIn, company site, conference appearances?
- **Location consistency** — do professional history claims place the person in the same locations consistently?
- **Timeline consistency** — do claimed tenures line up? Are there unexplained gaps?
- **Writing style or patterns** — for authors, does the claimed work match a consistent voice or research area?

## Step 4: Name disambiguation

If the name belongs to multiple people:

1. List all distinct individuals found with this name
2. Apply context anchors from the gate record (employer, location, field) to narrow
3. Document which individual you're confirming — and note if disambiguation is uncertain

Failure condition: after 3 attempts with different context anchors, ambiguity persists. Stop and ask for additional context rather than guessing.

## Step 5: Flag inconsistencies

Document any:

- Claims that couldn't be verified (not the same as disproved)
- Gaps in the professional timeline
- Credential claims that don't appear in the issuing body's registry
- Conflicting information across sources (different employers listed on different sites)

Distinguish clearly between "unverifiable" (no public evidence either way) and "contradicted" (evidence that the claim is false).

## Rules

- Start from the subject's claims, not from an open search. You're verifying, not profiling.
- Never assert a claim is false unless you have a source that actively contradicts it. "Not found in registry" is not the same as "invalid credential."
- Disambiguation failures must be surfaced. Reporting on the wrong person is worse than reporting nothing.
- Photo comparison is visual only — note photo consistency across sources; don't speculate beyond what you can observe.

## Output format

```markdown
### Identity verification: [Name]

**Gate record:** [link or copy]
**Claims to verify:** [listed]

#### Verification results

| Claim | Status | Evidence | Source |
|---|---|---|---|
| [Employer] | Verified / Unverifiable / Contradicted | [detail] | [source] |
| [Credential] | Verified / Unverifiable / Contradicted | [detail] | [source] |

#### Cross-reference consistency

[Photo/location/timeline consistency across sources]

#### Disambiguation

[If multiple people share the name — how isolated, confidence level]

#### Inconsistencies

[Any gaps, unverifiable claims, or contradictions — with distinction between unverifiable vs contradicted]

#### Confidence assessment

[Overall: High / Medium / Low — with reasoning]
```
