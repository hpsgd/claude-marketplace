# Output: user-docs-writer — complex task guide

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 14/17 criteria met (82%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Article provides separate labelled paths for each configuration side (Azure portal steps, platform admin steps) — met: the definition explicitly mandates "Part 1: Configure Azure AD / Part 2: Configure [Platform] / Part 3: Test the connection" for multi-system tasks
- [x] PASS: Recovery path is documented for each failure mode mentioned (certificate mismatch, attribute mapping) — met: KB article structure mandates "Recovery paths" and troubleshooting structured as symptom → cause → fix
- [x] PASS: Steps are numbered with expected results after each step, not just instructions — met: "Every step has an expected result" is a non-negotiable principle; User Guide rules state expected result after each step
- [x] PASS: Technical jargon is explained or linked on first use (SAML, IdP, SP, assertion) — met: "No acronyms without definition. First use: 'Single Sign-On (SSO)'" is an explicit voice rule
- [x] PASS: A verification step confirms the SSO connection works before declaring success — met: multi-system task guidance specifies "The verification step at the end confirms both sides work together"
- [~] PARTIAL: Article includes a "before you start" prerequisites section with specific requirements (Azure AD tier, admin permissions, metadata URL) — partially met: prerequisites section is required by User Guide structure; the definition covers generic "account type, permissions, data" but does not drive the specific Azure AD Premium tier or metadata URL requirements; an agent would produce a prerequisites section but content specificity depends on domain knowledge not the definition
- [x] PASS: Troubleshooting section is structured as symptom → cause → fix, not a list of tips — met: KB article structure explicitly mandates symptom → cause → fix with a certificate mismatch example matching the test scenario
- [x] PASS: The article is written for IT admins (procedural, specific) not developers (no code samples unless necessary) — met: procedural User Guide format; "What You Don't Do" excludes developer-oriented docs and jargon

### Output expectations

- [x] PASS: Output's structure has clearly labelled sections — Prerequisites, Configure Azure AD, Configure the platform, Test the connection, Troubleshooting — with the two configuration sections explicitly distinct — met: Part 1/Part 2/Part 3 labelled sections are mandated by the multi-system task rule
- [x] PASS: Output's Azure AD section steps are numbered with specific path references and expected result per step — met: "One action per step" and "Expected result after each step" are explicit rules; procedural numbered structure would produce path references
- [~] PARTIAL: Output's platform side has matching numbered steps taking values from Azure and mapping to exact platform field names — partially met: numbered steps per section are mandated; however, the definition does not specify that field names must be exact or that cross-system value mapping must be made explicit; an agent may produce this from context but it is not rule-driven
- [x] PASS: Output explains technical jargon on first use (SAML 2.0, IdP/SP, assertion) without dumbing down for IT-admin audience — met: "No acronyms without definition" rule covers this; IT-admin audience preserved by procedural User Guide format
- [x] PASS: Output's verification step performs an actual end-to-end SSO login attempt — met: "The verification step at the end confirms both sides work together" is explicit in the multi-system guidance; Verification Protocol mandates following every step from scratch
- [x] PASS: Output's troubleshooting section uses symptom → cause → fix for at least the two named failure modes — met: symptom → cause → fix is explicitly mandated; certificate mismatch example in the definition matches the test scenario exactly
- [~] PARTIAL: Output's prerequisites are explicit — Azure AD Premium tier, Global Administrator role, platform admin role, metadata URL — partially met: prerequisites structure is required but the definition's "account type, permissions, data" does not guarantee the specific tier, role, and metadata URL items; specificity depends on domain knowledge not definition rules
- [x] PASS: Output's tone is procedural — single action per step, expected outcome stated, no hedge language — met: "One action per step" and active voice rules are enforced; "feel free to" language conflicts with active voice and writing-style rules
- [x] PASS: Output addresses the bidirectional nature explicitly — Azure values go into platform, platform values go into Azure — met: Part 1/Part 2 self-contained sections handle this; the agent definition's multi-system guidance explicitly addresses this exchange pattern
- [~] PARTIAL: Output addresses production cutover guidance — transitioning existing users to SSO without lockout — partially met: the definition covers "Recovery paths" for access-control scenarios including lost-access recovery, but production cutover (staged rollout, password fallback during transition, enforcing SSO) is not explicitly prompted; an agent might include it under "Next steps" but no rule drives it

## Notes

The agent definition is well-matched to this scenario. The multi-system SSO/Azure AD case is used as the worked example in both the multi-system task guidance and the troubleshooting rules, suggesting the definition was written with this kind of scenario in mind. Criteria gap areas are in output specificity: prerequisites content (Azure AD tier, metadata URL) depends on domain knowledge rather than definition rules; exact field name mapping across systems is not explicitly required; and production cutover guidance has no mechanism driving it. These are genuine gaps, not definition failures — the agent would produce a high-quality article but some of the most specific output expectations exceed what the definition mandates.
