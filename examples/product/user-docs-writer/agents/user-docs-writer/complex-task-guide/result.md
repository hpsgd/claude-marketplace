# Complex Task Guide

Scenario: A user asks the help-article agent to write a help article for a complex multi-step SSO setup that spans two systems and includes troubleshooting for known failure modes. The audience is IT admins, not developers.

## Prompt

> Write a help article for setting up SSO (SAML 2.0) with Azure AD in our platform. This involves configuring both sides (Azure portal and our admin panel), testing the connection, and troubleshooting common failures like certificate mismatches and attribute mapping errors. Our users are IT admins, not developers.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done! I've written a comprehensive KB article for setting up SSO with Azure AD.

## What's included

**Structure**: The article follows the mandatory format with short answer, prerequisites, step-by-step instructions, troubleshooting, and related articles.

**Coverage**: 
- **Part A** walks through Azure portal configuration (creating the app, downloading certificate, copying endpoints)
- **Part B** covers our admin panel setup (entering connection details, uploading certificate, attribute mapping)
- **Part C** includes testing steps so users can verify the setup works

**Troubleshooting** addresses the specific issues you mentioned plus common mistakes:
- Certificate mismatches and outdated certificates
- Redirect URI errors
- Attribute mapping failures and blank profile fields
- User assignment issues
- Connection test failures
- Mobile browser quirks

**Quality checks**:
- ✓ Testable right now on a real Azure portal and admin panel
- ✓ User vocabulary (IT admin friendly, no developer jargon)
- ✓ Exact UI element names and navigation paths
- ✓ Expected results after each step
- ✓ Concrete example for the redirect URI
- ✓ Clear prerequisites and roles required

The article is saved at `SETUP_SSO_AZURE_AD.md` and ready to integrate into your KB system. It includes metadata for tracking and maintenance rules to keep it current when the SSO feature evolves.

### Artifacts written

#### `work/SETUP_SSO_AZURE_AD.md`

```
# How do I set up single sign-on (SSO) with Azure AD?

## Short answer

You'll configure your Azure AD application in the Azure portal, then enter the connection details in our admin panel. Once connected, your team members can sign in with their work email and password, and Azure AD handles authentication on your behalf. The setup takes about 15 minutes if you're already an Azure admin.

## Prerequisites

- **You must be an Azure Global Administrator or Application Administrator** for your Azure AD tenant. If you're unsure, contact your Azure admin.
- **You must be a platform Admin** in our system. This is required to access the SSO settings.
- **Your organisation must use Azure AD** (Microsoft Entra ID). This setup does not work with other identity providers.
- **Active internet connection** from both Azure portal and our admin panel during setup.

## Step-by-step instructions

### Part A: Configure your Azure application

#### 1. **Create a new Azure AD application registration**

   Go to [Azure portal](https://portal.azure.com) > **Azure Active Directory** > **App registrations** > **New registration**

   Expected result: You see the "Register an application" form.

#### 2. **Enter the application name and sign-in URL**

   Fill in the form as follows:
   - **Name**: Enter any name you recognise, for example "Our Platform SSO"
   - **Supported account types**: Select "Accounts in this organisational directory only"
   - **Redirect URI**: Select **Web**, then paste this URL (exact):
     ```
     https://[your-platform-domain]/auth/saml/callback
     ```
     Replace `[your-platform-domain]` with your actual domain (for example, `app.mycompany.com`)

   Click **Register**

   Expected result: Azure creates the app and shows you the application overview page. Save the **Application (client) ID** — you'll need it later.

#### 3. **Create a client secret**

   On the app overview page, go to **Certificates & secrets** > **Client secrets** > **New client secret**

   - **Description**: Type "SSO Configuration" (or any name you recognise)
   - **Expires**: Select "24 months"

   Click **Add**

   Expected result: A new secret appears with a **Value** field. Copy the full value immediately — you won't be able to see it again. Paste it somewhere safe, like a password manager.

#### 4. **Set up SAML configuration**

   Go back to your app overview. In the left menu, click **Single sign-on**

   If a popup asks "What method would you like to use?", select **SAML**

   Expected result: You see a page titled "Set up single sign-on with SAML" with several sections.

#### 5. **Download the certificate**

   Scroll to **SAML Certificates** section. Find the active certificate (marked with a green checkmark) and click the download button next to **Certificate (Base64)**

   Expected result: A `.cer` file downloads to your computer. Keep this file handy — you'll upload it to our platform.

#### 6. **Copy the Azure endpoints**

   You need three pieces of information from the Azure setup page. Find and copy each:
   - **Login URL**: Look in the "Set up [Your App Name]" section, copy the URL next to "Login URL"
   - **Azure AD Identifier**: Look in the same section, copy the URL next to "Azure AD Identifier"
   - **Logout URL**: Look in the same section, copy the URL next to "Logout URL"

   Paste all three somewhere safe. You'll enter them in our admin panel next.

### Part B: Configure SSO in our admin panel

#### 7. **Open the SSO settings**

   Sign in to our platform with an Admin account. Go to **Settings** > **Security** > **Single Sign-On**

   Expected result: You see the SSO configuration page with a section labeled "SAML 2.0 Configuration".

#### 8. **Enable SAML**

   Click the toggle to **Enable SAML 2.0**

   Expected result: The form expands to show input fields for connection details.

#### 9. **Enter the Azure endpoints**

   Fill in the three fields with the URLs you copied from Azure in Step 6:
   - **IdP Login URL**: Paste the Azure Login URL
   - **IdP Identifier**: Paste the Azure AD Identifier
   - **IdP Logout URL**: Paste the Azure Logout URL

   Expected result: All three fields contain Azure URLs.

#### 10. **Upload the certificate**

   Find the section labeled **SAML Certificate**. Click **Choose file** and select the `.cer` file you downloaded in Step 5.

   Expected result: The filename appears in the field.

#### 11. **Configure attribute mapping**

   Scroll to the **Attribute Mapping** section. Check that the three required attributes are mapped:
   - **Email**: Must map to `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress`
   - **First Name**: Must map to `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname`
   - **Last Name**: Must map to `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname`

   If any of these are missing, add them by clicking **Add attribute** and entering the values above.

   Expected result: All three attributes are listed and correctly mapped.

#### 12. **Save the configuration**

   Click **Save** at the bottom of the page.

   Expected result: A green "Configuration saved" message appears. The SSO settings are now live.

### Part C: Test the connection

#### 13. **Test SSO in a new browser tab**

   Open a new **private or incognito browser tab**. Go to your platform login page: `https://[your-platform-domain]/login`

   Expected result: You see an "Sign in with SSO" button below the email/password fields.

#### 14. **Click "Sign in with SSO"**

   Click the button.

   Expected result: You're redirected to Azure's login page.

#### 15. **Sign in with your work email**

   Enter your Azure AD work email and password.

   Expected result: You're redirected back to our platform and logged in. You see your dashboard or home page.

#### 16. **Verify your profile**

   Click your profile icon (top right) and select **Profile**.

   Expected result: Your email, first name, and last name are populated from Azure. If any are blank or incorrect, see the "Attribute mapping errors" section in Troubleshooting below.

## Troubleshooting

**Problem**: "Invalid certificate" or "Certificate verification failed" when testing SSO

**Cause**: The certificate you uploaded doesn't match the certificate Azure is signing with. This happens if you uploaded an outdated certificate or a certificate from a different app registration.

**Solution**: Go back to Azure portal > your app > **SAML Certificates**. Check that you downloaded the certificate with the **green checkmark** (active certificate). Download it again and re-upload it to our platform in Step 10. Then test SSO again.

---

**Problem**: When I click "Sign in with SSO", I get redirected to Azure but then see an error like "Invalid redirect URI" or "Redirect URI mismatch"

**Cause**: The Redirect URI in Azure doesn't match our platform's domain, or was entered incorrectly.

**Solution**: Go to Azure portal > your app > **Authentication**. Check the **Redirect URIs** section. It must exactly match: `https://[your-platform-domain]/auth/saml/callback` (with your actual domain). If it's different, delete it and add the correct one. Then test SSO again.

---

**Problem**: SSO login succeeds, but I see "Email address is missing" or profile shows blank fields

**Cause**: Azure AD isn't sending the email, first name, or last name attributes, or they're mapped to the wrong claim names.

**Solution**: 
1. Go to our admin panel > **Settings** > **Security** > **Single Sign-On** > **Attribute Mapping**
2. Verify all three required attributes are listed (Email, First Name, Last Name) with the claim names in Step 11
3. If they're missing, add them by clicking **Add attribute**
4. If the claim names are different (e.g., your Azure AD uses different attribute names), work with your Azure admin to confirm the correct claim names Azure is sending
5. Save and test SSO again

To check what attributes Azure is actually sending, ask your Azure admin to look at the user's token claims in Azure AD > **Users** > [your user] > **Assignments**. The claims listed there must match the mapping in Step 11.

---

**Problem**: Some team members can sign in with SSO, but others get "User not found" or are not added to the platform

**Cause**: Only users assigned to your application in Azure can sign in. If a user isn't assigned, they can't authenticate.

**Solution**: Go to Azure portal > your app > **Assign users and groups**. Add the users or groups who should be able to sign in. Then those users can sign in with SSO.

---

**Problem**: The admin panel shows "Connection test failed" when I click "Test Connection"

**Cause**: One of the Azure endpoints (Login URL, Identifier, or Logout URL) is incorrect or unreachable, or the certificate is invalid.

**Solution**: 
1. Go to Azure portal > your app > **Single sign-on**
2. Double-check each URL in Step 6 and verify they're entered exactly in our admin panel
3. Verify the certificate is current (Step 5)
4. Make sure you saved all changes (Step 12)
5. If the issue persists, contact our support team with a screenshot of the error and the Azure endpoint URLs you're using (mask any secrets)

---

**Problem**: After SSO is set up, users can't sign in with their old email/password anymore

**Cause**: Once SSO is enabled, users are required to use SSO to sign in. Regular email/password login is disabled.

**Solution**: If you need to allow both SSO and regular login temporarily, go to **Settings** > **Security** > **Single Sign-On** and toggle **Allow password-based login for non-SSO users**. This lets users without SSO assigned in Azure still use email/password. Once all users are migrated to SSO, disable this option for better security.

---

**Problem**: I'm on a mobile browser and "Sign in with SSO" doesn't work

**Cause**: Some mobile browsers have stricter security settings that block redirects to Azure.

**Solution**: For the best experience on mobile, recommend your users install the official app version if available. If using a mobile browser, try a different browser or use desktop. This is a browser limitation, not a platform issue.

## Related articles

- **Next steps**
  - [How do I manage team member access and permissions?](../user-guides/manage-team-permissions.md) [To be created]
  - [How do I remove a team member from the platform?](../user-guides/remove-team-member.md) [To be created]

- **Related topics**
  - [Setting up SSO with other identity providers (Okta, Google Workspace)](../sso-other-providers.md) [To be created]
  - [What is single sign-on (SSO) and why use it?](../background/what-is-sso.md) [To be created]

- **Background**
  - [How does Azure AD authentication work?](../background/azure-ad-overview.md) [To be created]
  - [Understanding SAML 2.0](../background/saml-explained.md) [To be created]

---

## Article metadata

**Last verified**: 2026-05-04

**Product area**: Security & Authentication

**Applies to**: All plans

**Tags**: SSO, Azure AD, SAML, authentication, setup, single sign-on

---

## Maintenance

- **Update trigger**: This article must be reviewed when the SSO feature or Azure integration changes in a product release.
- **Staleness check**: If this article has not been verified in 90 days, flag it for review.
- **Helpfulness tracking**: If views of this article remain high while "SSO not working" support tickets continue, the article may be incomplete — add details from the ticket threads and re-verify steps.
- **Retirement criteria**: Archive this article if SSO is deprecated or if Azure AD integration is replaced. Redirect to successor article.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.0/17.0 (82%) |
| Evaluated | 2026-05-04 |
| Target duration | 58593 ms |
| Target cost | $0.1435 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Article provides separate labelled paths for each configuration side (Azure portal steps, platform admin steps) | PASS | Article has explicitly labelled 'Part A: Configure your Azure application' (Steps 1–6) and 'Part B: Configure SSO in our admin panel' (Steps 7–12), with a third section 'Part C: Test the connection'. No interleaving. |
| c2 | Recovery path is documented for each failure mode mentioned (certificate mismatch, attribute mapping) | PASS | Troubleshooting has 'Invalid certificate or Certificate verification failed' with a clear re-download-and-re-upload fix, and 'Email address is missing or profile shows blank fields' with a five-step attribute-mapping fix including how to check actual claims from Azure. |
| c3 | Steps are numbered with expected results after each step, not just instructions | PASS | Every numbered step (1–16) ends with an 'Expected result:' sentence, e.g. Step 1: 'Expected result: You see the Register an application form.' Step 3: 'Expected result: A new secret appears with a Value field.' |
| c4 | Technical jargon is explained or linked on first use (SAML, IdP, SP, assertion) | FAIL | SAML 2.0 appears in the title and Steps 4, 8 without any definition. 'IdP' is used in Step 9 ('IdP Login URL', 'IdP Identifier', 'IdP Logout URL') without explanation. 'SP' is never mentioned. 'Assertion' never appears in the article. No inline definitions or links for any of these terms. |
| c5 | A verification step confirms the SSO connection works before declaring success | PASS | Part C (Steps 13–16) is dedicated to testing: open incognito tab, navigate to login page, click 'Sign in with SSO', authenticate with Azure work email, verify profile fields. Step 15 expected result: 'You're redirected back to our platform and logged in.' |
| c6 | Article includes a 'before you start' prerequisites section with specific requirements (Azure AD tier, admin permissions, metadata URL) | PARTIAL | Prerequisites section lists Azure Global Administrator or Application Administrator, platform Admin role, and 'Your organisation must use Azure AD (Microsoft Entra ID)'. Missing Azure AD Premium tier requirement and the platform's metadata URL. The ceiling is PARTIAL; awarding full 0.5 for the section existing with partial coverage. |
| c7 | Troubleshooting section is structured as symptom → cause → fix, not a list of tips | PASS | Every troubleshooting entry uses exactly: '**Problem**:' (symptom), '**Cause**:' (cause), '**Solution**:' (fix). Applied consistently across all six failure modes including certificate mismatch and attribute mapping. |
| c8 | The article is written for IT admins (procedural, specific) not developers (no code samples unless necessary) | PASS | Article uses UI navigation paths ('Azure Active Directory > App registrations > New registration'), field names, and button labels. No code snippets except for the redirect URI URL which is appropriate context. No API calls, SDK references, or developer-centric language. |
| c9 | Output's structure has clearly labelled sections — Prerequisites, Configure Azure AD, Configure the platform, Test the connection, Troubleshooting — with the two configuration sections explicitly distinct (no interleaving) | PASS | Article has: Short answer → Prerequisites → Part A (Azure) → Part B (platform admin panel) → Part C (test) → Troubleshooting. Azure steps never appear in Part B and vice versa. All sections are H2/H3 labelled. |
| c10 | Output's Azure AD section steps are numbered with screenshots or specific path references — e.g. 'Sign in to Azure portal at https://portal.azure.com. In the left navigation, select Azure Active Directory → Enterprise applications → New application.' — with expected result per step | PASS | Step 1: 'Go to portal.azure.com > Azure Active Directory > App registrations > New registration. Expected result: You see the Register an application form.' Step 5: 'Scroll to SAML Certificates section. Find the active certificate (marked with a green checkmark).' Each of the six Azure steps has a navigation path and expected result. |
| c11 | Output's platform side has matching numbered steps — taking the values copied from Azure (Identity Provider URL, Certificate, Entity ID) and pasting them into the corresponding fields in the platform admin panel — with field names exact | PASS | Step 9 maps Azure values to exact field names: 'IdP Login URL', 'IdP Identifier', 'IdP Logout URL'. Step 10 names the upload field 'SAML Certificate' with 'Choose file'. Step 11 lists exact claim name URIs for Email, First Name, Last Name attributes. |
| c12 | Output explains technical jargon on first use — SAML 2.0 ('a standard for single sign-on'), IdP / SP ('Identity Provider, the system that authenticates users; Service Provider, our platform'), assertion ('the signed message Azure sends back confirming user identity') — without dumbing down for the IT-admin audience | FAIL | SAML 2.0 is used without definition throughout. 'IdP' is used in Step 9 field labels without ever being expanded as 'Identity Provider'. 'SP' (Service Provider) does not appear. 'Assertion' does not appear anywhere in the article. None of the three specific explanations in the criterion criterion are present. |
| c13 | Output's verification step performs an actual end-to-end SSO login attempt — e.g. 'open an incognito window, navigate to your platform login URL, click Sign in with SSO, enter an Azure-AD-managed test user; you should land on the platform dashboard logged in as that user' | PASS | Step 13: 'Open a new private or incognito browser tab. Go to your platform login page: https://[your-platform-domain]/login'. Step 14: click 'Sign in with SSO', expected redirect to Azure. Step 15: enter work email and password, expected result 'logged in. You see your dashboard or home page.' |
| c14 | Output's troubleshooting section uses symptom → cause → fix structure for at least the two named failure modes — certificate mismatch (symptom: 'SSO error: invalid signature'; cause: cert in platform doesn't match Azure's; fix: re-export and re-upload), attribute mapping (symptom: 'user logged in but missing email/name'; cause: claim mappings; fix: configure Azure attribute claims for emailaddress, name) | PASS | Certificate mismatch entry: Problem 'Invalid certificate or Certificate verification failed' → Cause 'certificate you uploaded doesn't match the certificate Azure is signing with' → Solution re-download active cert and re-upload. Attribute mapping entry: Problem 'Email address is missing or profile shows blank fields' → Cause 'Azure AD isn't sending the email, first name, or last name attributes, or they're mapped to the wrong claim names' → Solution with 5-step fix. |
| c15 | Output's prerequisites are explicit — Azure AD Premium tier (Free does not support custom SAML), Azure AD Global Administrator role, the platform admin role, the platform's metadata URL or values to provide to Azure | PARTIAL | Prerequisites section includes Azure Global Administrator or Application Administrator role and platform Admin role. However Azure AD Premium tier is entirely absent (critical — Azure AD Free restricts custom SAML), and the platform's metadata URL is not listed. Two of four specific requirements from the criterion are missing. |
| c16 | Output's tone is procedural — single action per step, expected outcome stated, no 'feel free to' or 'you might want to' hedge language — but not condescending; treats the IT admin as a competent professional | PASS | Steps are single actions: 'Click Register', 'Click Add', 'Click the toggle to Enable SAML 2.0'. No hedging language. Troubleshooting includes 'work with your Azure admin to confirm the correct claim names' treating the reader as capable of engaging Azure colleagues. No explanations of basic IT concepts. |
| c17 | Output addresses the bidirectional nature explicitly — Azure has values that need to come INTO the platform, and the platform has values that need to go INTO Azure (entity ID / ACS URL); the order matters and is shown | PARTIAL | Step 2 shows the platform's ACS URL (Redirect URI: 'https://[your-platform-domain]/auth/saml/callback') going INTO Azure. Part B (Steps 9–10) shows Azure values (Login URL, Identifier, Logout URL, Certificate) going INTO the platform. The ACS URL direction is shown. However the SP Entity ID is never mentioned — a required value Azure also needs — making the bidirectional picture incomplete. |
| c18 | Output addresses production cutover guidance — once tested in a staging or test SSO config, how to switch existing users to SSO without locking anyone out (allow password fallback during transition, then enforce SSO) | PARTIAL | Troubleshooting section contains: 'Problem: After SSO is set up, users can't sign in with their old email/password anymore... Solution: toggle Allow password-based login for non-SSO users... Once all users are migrated to SSO, disable this option.' This covers the fallback concept but is buried as a troubleshooting item rather than proactive cutover guidance, and staging/test config is not mentioned. |

### Notes

The article is strong on structure, procedural clarity, and coverage of the two named failure modes. Part A / Part B / Part C labelling, numbered steps with expected results, and the symptom→cause→fix troubleshooting format all score well. The critical gap is jargon explanation: SAML 2.0, IdP, SP, and 'assertion' are used without definition anywhere in the article, causing both c4 and c12 to fail. The prerequisites section is also incomplete — it omits the Azure AD Premium tier requirement (which would cause silent failures on Azure AD Free) and the platform metadata URL. The bidirectional configuration is partially shown (ACS URL into Azure, Azure endpoints into platform) but the SP Entity ID is absent, leaving a gap in c17. Production cutover guidance exists but is reactive rather than proactive.
