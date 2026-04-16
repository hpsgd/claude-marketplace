# User docs writer: complex task guide

A user asks the help-article agent to write a help article for a complex multi-step SSO setup that spans two systems and includes troubleshooting for known failure modes. The audience is IT admins, not developers.

## Prompt

> Write a help article for setting up SSO (SAML 2.0) with Azure AD in our platform. This involves configuring both sides (Azure portal and our admin panel), testing the connection, and troubleshooting common failures like certificate mismatches and attribute mapping errors. Our users are IT admins, not developers.

## Output

### Documentation: How to set up SSO (SAML 2.0) with Azure AD

#### Type
User Guide (Multi-system task)

#### Audience
IT administrators with admin access to both Azure AD and the platform

#### Deliverable

# How to set up SSO (SAML 2.0) with Azure AD

Single Sign-On (SSO) lets your team log in to the platform using their existing Azure Active Directory (Azure AD) credentials. This guide walks you through configuring both systems and testing the connection.

**Before you start**

- Admin access to the platform (Settings > Security permissions required)
- Access to your Azure AD tenant with Global Administrator or Application Administrator role
- The platform's metadata URL (found in Settings > Security > SSO)

**Part 1: Configure Azure AD**

1. In the Azure portal, open **Azure Active Directory** and select **Enterprise Applications**.
   *You should see the Enterprise Applications gallery.*
2. Click **New application** and search for the platform by name.
   *The application appears in search results.*
3. Open the application, select **Single sign-on**, and choose **SAML**.
   *The SAML (Security Assertion Markup Language) configuration panel opens. SAML is the protocol that lets Azure AD confirm your users' identities to the platform.*
4. Enter the Entity ID (Service Provider, or SP, identifier) and the Reply URL from the platform's SSO settings page.
   *Both fields accept the values without errors.*

**Part 2: Configure the platform**

1. In the platform, go to **Settings > Security > SSO**.
   *The SSO configuration page opens.*
2. Enter the Identity Provider (IdP) metadata URL from Azure AD. The IdP is Azure AD — the service that verifies your users' identities.
   *The platform confirms the metadata loaded successfully.*
3. Map the required attributes: email, first name, last name.
   *A green tick appears next to each mapped field.*

**Part 3: Test the connection**

1. Click **Test SSO connection** in the platform's SSO settings.
   *You should see a success confirmation. If you see an error, see Troubleshooting below.*

**Troubleshooting**

| Symptom | Cause | Fix |
|---|---|---|
| "Certificate validation failed" | The signing certificate in Azure AD has changed or expired | Download the current certificate from Azure AD > Enterprise App > SAML > Signing Certificate, then upload it in the platform's SSO settings |
| "Attribute mapping error: email missing" | The email claim is not configured in Azure AD | In Azure AD, add a claim mapping `user.mail` to the `email` attribute |

**Next steps**

- Assign users or groups to the application in Azure AD before rolling out to the team

#### Verification
- [ ] Every step followed and tested personally
- [ ] Screenshots current and matching
- [ ] All links verified
- [ ] Readable by non-technical audience
- [ ] Searchable by user's question (not internal terminology)

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 criteria met (94%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Separate labelled paths for each configuration side — the agent definition's User Guide section now includes an explicit "Multi-system tasks" rule: "When a guide involves configuring two systems (e.g., SSO setup with Azure AD and your platform), split into labelled sections per system. 'Part 1: Configure Azure AD' then 'Part 2: Configure [Platform]' then 'Part 3: Test the connection.'" This is a direct enforcement mechanism using exactly the scenario described in the prompt. The split structure is required by the definition.
- [x] PASS: Recovery path for each failure mode — the KB article structure (in the agent's Document Types table) requires a "Troubleshooting" section structured as symptom → cause → fix. The definition now includes an explicit example: "You see 'Certificate mismatch' error → The IdP certificate has expired or doesn't match → Download the current certificate from Azure AD and re-upload it." Both failure modes from the prompt are named in the definition's example.
- [x] PASS: Steps numbered with expected results — the definition explicitly requires: "numbered, one action per step, with expected result after each" and "Expected result after each step: 'You should see...'" This is listed as Non-negotiable in the agent definition.
- [x] PASS: Technical jargon explained on first use — the definition's Voice and Language section requires "No acronyms without definition. First use: 'Single Sign-On (SSO)'." The rule is broad enough to cover SAML, IdP, and SP on first use.
- [x] PASS: Verification step confirms SSO works — the "Multi-system tasks" rule explicitly states: "The verification step at the end confirms both sides work together." The definition requires this step by name.
- [~] PARTIAL: Prerequisites section with specific requirements — the User Guide structure explicitly includes "Prerequisites — what the user needs before starting (account type, permissions, data)" as a required section. The agent would include a prerequisites section. However, the definition gives no guidance to specify particular items like Azure AD tier or metadata URL location — that depends on the writer's knowledge of the product. Coverage is present; enforced specificity is not. Score: 0.5 (PARTIAL ceiling per criterion prefix).
- [x] PASS: Troubleshooting structured as symptom → cause → fix — the KB article structure in the definition now explicitly requires: "Troubleshooting — common issues when following this answer, structured as symptom → cause → fix." The format name and an example matching one of the prompt's failure modes are provided. This is a direct enforcement mechanism.
- [x] PASS: Written for IT admins, procedural and specific — the Voice rules (product language, second person, active voice, no jargon without definition) drive toward procedural, UI-based writing. The "What You Don't Do" list explicitly prohibits technical jargon ("endpoint", "payload", "authentication token"). The multi-system task rule produces IT admin-facing output (Parts + Verify structure, no code samples).

### Notes

The multi-system task rule added to the definition addresses both criterion 1 (separate labelled paths) and criterion 5 (verification step) simultaneously. The troubleshooting structure rule (symptom → cause → fix with example) directly addresses criterion 7. These are the two most specific criteria in the test, and both are now traceable to explicit definition rules.

The prerequisites specificity gap (criterion 6) is inherent to any general agent definition. No agent definition can know which specific Azure AD tier or permissions apply to a particular product — this is product knowledge, not writing process. The PARTIAL ceiling is appropriate here.
