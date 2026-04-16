# Test: user-docs-writer — complex task guide

Scenario: A user asks the help-article agent to write a help article for a complex multi-step SSO setup that spans two systems and includes troubleshooting for known failure modes. The audience is IT admins, not developers.

## Prompt

Write a help article for setting up SSO (SAML 2.0) with Azure AD in our platform. This involves configuring both sides (Azure portal and our admin panel), testing the connection, and troubleshooting common failures like certificate mismatches and attribute mapping errors. Our users are IT admins, not developers.

## Criteria

- [ ] PASS: Article provides separate labelled paths for each configuration side (Azure portal steps, platform admin steps)
- [ ] PASS: Recovery path is documented for each failure mode mentioned (certificate mismatch, attribute mapping)
- [ ] PASS: Steps are numbered with expected results after each step, not just instructions
- [ ] PASS: Technical jargon is explained or linked on first use (SAML, IdP, SP, assertion)
- [ ] PASS: A verification step confirms the SSO connection works before declaring success
- [ ] PARTIAL: Article includes a "before you start" prerequisites section with specific requirements (Azure AD tier, admin permissions, metadata URL)
- [ ] PASS: Troubleshooting section is structured as symptom → cause → fix, not a list of tips
- [ ] PASS: The article is written for IT admins (procedural, specific) not developers (no code samples unless necessary)
