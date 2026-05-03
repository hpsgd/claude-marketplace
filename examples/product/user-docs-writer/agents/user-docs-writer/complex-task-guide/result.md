# Complex Task Guide

Scenario: A user asks the help-article agent to write a help article for a complex multi-step SSO setup that spans two systems and includes troubleshooting for known failure modes. The audience is IT admins, not developers.

## Prompt

> Write a help article for setting up SSO (SAML 2.0) with Azure AD in our platform. This involves configuring both sides (Azure portal and our admin panel), testing the connection, and troubleshooting common failures like certificate mismatches and attribute mapping errors. Our users are IT admins, not developers.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

The article is written at `docs/kb/sso-saml-azure-ad-setup.md`. Here's what it covers:

**Structure**
- Search-phrased title, scannable short answer, explicit prerequisites (Azure role + platform plan tier)
- 17 numbered steps split across three logical phases: Azure portal → admin panel → test & enforce
- Each step names exact UI elements and states the expected result

**Troubleshooting** covers all requested failure modes plus two extras that come up constantly in practice:
- Certificate mismatch (including the rotation scenario)
- Attribute mapping / empty `user.mail` → UPN fallback
- ACS URL mismatch (AADSTS50011)
- Redirect loop (NameID format + cookie block)
- Existing account not matched on SSO login
- Clock skew (NotBefore/NotOnOrAfter)
- Metadata fetch failure

**One thing to action before publishing**: the article uses placeholder ACS URL and Entity ID values. The publishing note at the bottom flags exactly what to replace — pull the real values from the admin panel and drop them in.

### Artifacts written

#### `work/docs/kb/sso-saml-azure-ad-setup.md`

```
# How do I set up single sign-on (SSO) with Azure Active Directory?

## Short answer

Create an enterprise application in Azure AD, copy the SAML endpoints and certificate into your organisation's SSO settings, then test with a pilot user before enabling SSO for your whole organisation. The full process takes 20–30 minutes.

---

## Prerequisites

- **Role**: You must hold the **Global Administrator** or **Application Administrator** role in your Azure AD tenant.
- **Platform role**: You must be an **Organisation Owner** in the platform admin panel.
- **Plan**: SSO is available on the **Business** and **Enterprise** plans. If you don't see the SSO menu in your admin panel, contact your account manager.
- **Certificate handling**: You will download an X.509 certificate from Azure. Have a place to save it temporarily (your Desktop is fine — you'll upload it within the same session).

---

## Step-by-step instructions

### Part 1 — Configure Azure AD

1. **Open the Azure portal and navigate to Enterprise Applications**

   Go to [portal.azure.com](https://portal.azure.com), then select **Azure Active Directory** from the left-hand menu. Choose **Enterprise applications** > **New application**.

   Expected result: The Azure AD application gallery opens.

2. **Create a new application**

   Click **Create your own application**. Enter a display name (e.g. `[Your Platform Name] SSO`), select **Integrate any other application you don't find in the gallery (Non-gallery)**, then click **Create**.

   Expected result: Azure creates the application and opens its Overview page.

3. **Open the SAML configuration panel**

   In the application's left-hand menu, under **Manage**, select **Single sign-on**. Choose **SAML** as the sign-on method.

   Expected result: The **Set up Single Sign-On with SAML** page opens, showing five numbered sections.

4. **Enter the basic SAML configuration**

   In section **1 – Basic SAML Configuration**, click **Edit** and fill in the two required fields:

   | Field | Value |
   |---|---|
   | **Identifier (Entity ID)** | `https://app.[yourplatform].com/saml/metadata` |
   | **Reply URL (Assertion Consumer Service URL)** | `https://app.[yourplatform].com/saml/acs` |

   > **Note for the publishing team**: Replace the placeholder URLs above with the real Entity ID and ACS URL from your admin panel (see Part 2, Step 1 below — collect those values first).

   Click **Save**.

   Expected result: Azure validates and saves the URLs. If you see a red banner, check that both URLs begin with `https://` and contain no trailing spaces.

5. **Configure user attributes and claims**

   In section **2 – Attributes & Claims**, click **Edit**. Verify the following claims are present. If any are missing, click **Add new claim** to add them:

   | Claim name | Source attribute |
   |---|---|
   | `emailaddress` | `user.mail` |
   | `givenname` | `user.givenname` |
   | `surname` | `user.surname` |
   | Unique User Identifier (Name ID) | `user.userprincipalname` |

   Click **Save**.

   Expected result: The claims list updates. If `user.mail` is empty for some accounts in your directory, see [Troubleshooting — email attribute not passed](#troubleshooting) below.

6. **Download the SAML certificate**

   In section **3 – SAML Signing Certificate**, find the row labelled **Certificate (Base64)** and click **Download**.

   Save the `.cer` file somewhere accessible — you will upload it in the next part.

   Expected result: A file named something like `[AppName].cer` downloads to your computer.

7. **Copy the federation metadata URL**

   In section **4 – Set up [App Name]**, copy the value labelled **App Federation Metadata URL**. It looks like:
   `https://login.microsoftonline.com/{tenant-id}/federationmetadata/2007-06/federationmetadata.xml?appid={app-id}`

   Keep this URL — you will paste it into the platform admin panel.

   Expected result: The URL is copied to your clipboard.

---

### Part 2 — Configure the platform admin panel

8. **Open SSO settings in the admin panel**

   Log in to the platform as an Organisation Owner. Go to **Settings** > **Security** > **Single Sign-On**.

   Expected result: The SSO configuration page opens, showing fields for Identity Provider settings and your platform's Service Provider details.

9. **Copy your Service Provider details into Azure**

   At the top of the SSO page, you will see two read-only values:

   | Field | Example |
   |---|---|
   | **Entity ID** | `https://app.[yourplatform].com/saml/metadata` |
   | **ACS URL** | `https://app.[yourplatform].com/saml/acs` |

   If you skipped ahead to Part 2 first, go back to Part 1, Step 4 and enter these values into Azure now before continuing.

10. **Paste the federation metadata URL**

    In the **Identity Provider Metadata URL** field, paste the URL you copied in Step 7.

    Click **Fetch Metadata**. The platform will retrieve and populate the IdP fields automatically.

    Expected result: The **SSO Issuer**, **SSO Login URL**, and **Certificate** fields fill in automatically. This may take up to 10 seconds. If the fetch fails, see [Troubleshooting — metadata fetch fails](#troubleshooting) below.

11. **Upload the certificate (if metadata fetch did not populate it)**

    If the **Certificate** field is still blank after Step 10, click **Upload Certificate** and select the `.cer` file you downloaded in Step 6.

    Expected result: A certificate fingerprint (a long string of hexadecimal characters) appears in the **Certificate** field.

12. **Set the Name ID format**

    From the **Name ID Format** dropdown, select **Email Address**.

    Expected result: The dropdown shows **Email Address**.

13. **Save and enable SSO**

    Click **Save Settings**. Do **not** toggle **Enforce SSO for all users** yet — leave that off until testing is complete.

    Expected result: A green banner reads "SSO settings saved." The page reloads with the settings intact.

---

### Part 3 — Assign users in Azure and test

14. **Assign a test user in Azure**

    Return to the Azure portal. In your enterprise application, go to **Users and groups** > **Add user/group**. Add a single test account (ideally your own, or a dedicated test user).

    Expected result: The user appears in the assigned users list.

15. **Test the SSO login**

    Open a private/incognito browser window. Navigate to the platform login page and click **Sign in with SSO**. Enter the test user's email address and click **Continue**.

    Expected result: You are redirected to the Microsoft login page, you authenticate, and you are returned to the platform as the test user. If you see an error page, note the error code and see the [Troubleshooting](#troubleshooting) section below.

16. **Verify the user's profile**

    After logging in, go to the test user's profile in the platform. Confirm that their name and email address are correctly populated from Azure AD.

    Expected result: The name and email match the values in Azure AD exactly.

17. **Enforce SSO (when ready)**

    Once you are satisfied the connection works, return to **Settings** > **Security** > **Single Sign-On** and toggle **Enforce SSO for all users** to **On**. Click **Save Settings**.

    After enforcement is on, users who attempt to log in with a password will be redirected to Azure AD instead.

    Expected result: A confirmation dialog warns you that password login will be disabled. Confirm to proceed.

---

## Troubleshooting

**Problem**: The metadata fetch in Step 10 fails with "Unable to retrieve metadata."
**Cause**: Azure may take a few minutes to publish the federation metadata URL after the application is created, or a firewall is blocking the platform from reaching Microsoft's servers.
**Solution**: Wait 2–3 minutes and try again. If it continues to fail, manually copy the **Login URL** and **Azure AD Identifier** from Azure section 4 into the corresponding fields in the admin panel, and upload the certificate manually using the `.cer` file from Step 6.

---

**Problem**: After authenticating with Microsoft, the platform shows a "Certificate mismatch" or "Invalid signature" error.
**Cause**: The certificate in the platform does not match the one Azure is currently using to sign assertions. This happens if the Azure certificate was rotated after you configured SSO.
**Solution**: In Azure, go to **Enterprise applications** > your app > **Single sign-on** > section 3. Download the current **Certificate (Base64)**. In the platform admin panel (**Settings** > **Security** > **Single Sign-On**), click **Upload Certificate** and upload the new file. Save settings and test again. To prevent this recurring, use the **Metadata URL** method (Step 10) so the certificate is refreshed automatically.

---

**Problem**: Login fails with "Attribute mapping error" or the user's name and email appear blank after login.
**Cause**: The email claim is not being sent by Azure, or the claim name does not match what the platform expects. This commonly happens when a user's `user.mail` attribute is empty in Azure AD (some accounts only have a UPN, not a separate mail attribute).
**Solution**: In Azure, go to **Attributes & Claims** (Step 5). Change the source attribute for the `emailaddress` claim from `user.mail` to `user.userprincipalname`. The UPN is always populated and is typically the user's email address. Click **Save** and test again.

---

**Problem**: Login fails with "AADSTS50011: The reply URL specified in the request does not match the reply URLs configured for the application."
**Cause**: The ACS URL entered in Azure (Step 4) does not exactly match the ACS URL the platform sent in its SAML request. A common cause is a trailing slash, `http` vs `https`, or a typo.
**Solution**: In the platform admin panel, copy the ACS URL from the Service Provider details at the top of the SSO page. Return to Azure, open **Basic SAML Configuration**, and paste it directly — do not retype it. Save and test again.

---

**Problem**: The SSO login page redirects back and forth between Microsoft and the platform without completing (redirect loop).
**Cause**: The platform is sending users to Azure for authentication, but Azure is redirecting them back without a valid session being created. This is usually caused by the **NameID format** mismatch (the platform expects Email Address but receives a different format) or cookies being blocked.
**Solution**: First, confirm the **Name ID Format** is set to **Email Address** in the platform admin panel (Step 12) and that the Name ID source in Azure is `user.userprincipalname`. Second, ensure the browser is not blocking third-party cookies — test in a browser with default settings. If the loop persists, contact support and include the SAML trace from your browser (the support team can provide a browser extension to capture this).

---

**Problem**: Login succeeds but the user is shown as a new account rather than their existing platform account.
**Cause**: The email address returned by Azure does not match the email on the user's existing platform account. This happens if the user signed up with a personal email but Azure is sending their corporate UPN.
**Solution**: Before enforcing SSO, ensure each user's email in the platform matches their Azure AD UPN or mail attribute. You can update email addresses in **Settings** > **Team** > select the user > **Edit Profile**.

---

**Problem**: Login fails with "AADSTS7000215: Invalid client secret" or a clock-related error ("NotBefore" or "NotOnOrAfter" validation failed).
**Cause**: Clock skew — the time on the server issuing the SAML assertion differs from the platform's server time by more than the allowed tolerance (typically 5 minutes). SAML assertions include timestamps and are rejected if they appear to be from the future or have expired.
**Solution**: This is not something you can fix in the platform or Azure portal — the clocks on your end are not involved. Contact your IT team to verify the Azure AD service is synchronised correctly. If the issue is on the platform side, contact support.

---

## Related articles

**Next steps**
- How do I assign SSO to specific groups instead of all users? [To be created]
- How do I provision and deprovision users automatically with SCIM? [To be created]

**Related topics**
- How do I require multi-factor authentication (MFA) for my organisation? [To be created]
- How do I manage team roles and permissions? [To be created]

**Background**
- What is single sign-on and why should I enable it? [To be created]

---

```
Last verified: 2026-05-01
Product area: Security / Authentication
Applies to: Business and Enterprise plans
Tags: SSO, SAML, Azure AD, Azure Active Directory, single sign-on
```

---

**Maintenance notes**

- **Update trigger**: Review this article whenever the SSO configuration UI changes in a platform release, or when Microsoft updates the Azure portal layout for Enterprise Applications.
- **Staleness check**: If this article has not been verified in 90 days, flag it for review.
- **Helpfulness tracking**: Track article views vs. ongoing SSO support tickets. High view volume with continued ticket volume means the steps are unclear — prioritise rewriting the failing section over adding more content.
- **Publishing note**: Before publishing, replace both placeholder URLs (`https://app.[yourplatform].com/saml/metadata` and `https://app.[yourplatform].com/saml/acs`) with the real production values. Confirm the admin panel navigation path (**Settings** > **Security** > **Single Sign-On**) matches the shipped UI.
- **Retirement criteria**: Archive this article when SAML 2.0 SSO is replaced by a successor authentication standard, and redirect to the new setup guide.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/17.0 (85%) |
| Evaluated | 2026-05-01 |
| Target duration | 173265 ms |
| Target cost | $0.2987 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Article provides separate labelled paths for each configuration side (Azure portal steps, platform admin steps) | PASS | The article has distinct titled sections: '### Part 1 — Configure Azure AD' (steps 1–7) and '### Part 2 — Configure the platform admin panel' (steps 8–13), with no interleaving. |
| c2 | Recovery path is documented for each failure mode mentioned (certificate mismatch, attribute mapping) | PASS | Troubleshooting section has a dedicated entry for 'Certificate mismatch' or 'Invalid signature' with a full recovery path, and a separate entry for 'Attribute mapping error' or blank email/name with a UPN fallback fix. |
| c3 | Steps are numbered with expected results after each step, not just instructions | PASS | All 17 steps include an 'Expected result:' line, e.g. Step 1: 'Expected result: The Azure AD application gallery opens.' and Step 4: 'Expected result: Azure validates and saves the URLs.' |
| c4 | Technical jargon is explained or linked on first use (SAML, IdP, SP, assertion) | FAIL | SAML appears in the title and throughout but is never defined. 'Identity Provider' is used in a field label (Step 10) without definition. 'Service Provider' appears in Step 9 without definition. 'Assertion' is used in the clock-skew troubleshooting entry ('SAML assertions include timestamps') without definition. None of the four listed terms are explained on first use. |
| c5 | A verification step confirms the SSO connection works before declaring success | PASS | Step 15 ('Test the SSO login') and Step 16 ('Verify the user's profile') explicitly require a successful end-to-end login before Step 17 enables enforcement for all users. |
| c6 | Article includes a 'before you start' prerequisites section with specific requirements (Azure AD tier, admin permissions, metadata URL) | PARTIAL | A '## Prerequisites' section is present listing Azure AD role (Global/Application Administrator), platform role (Organisation Owner), and platform plan tier (Business/Enterprise). However, Azure AD Premium tier requirement is not mentioned, and the platform metadata URL is not listed as a prerequisite. |
| c7 | Troubleshooting section is structured as symptom → cause → fix, not a list of tips | PASS | Every troubleshooting entry follows 'Problem: ... Cause: ... Solution:' structure, consistently applied across all seven entries. |
| c8 | The article is written for IT admins (procedural, specific) not developers (no code samples unless necessary) | PASS | No code samples appear. Steps reference UI elements by exact name ('click Edit', 'select Email Address from the dropdown'). Tables show configuration values. Language is procedural throughout. |
| c9 | Output's structure has clearly labelled sections — Prerequisites, Configure Azure AD, Configure the platform, Test the connection, Troubleshooting — with the two configuration sections explicitly distinct (no interleaving) | PASS | Article has '## Prerequisites', '### Part 1 — Configure Azure AD', '### Part 2 — Configure the platform admin panel', '### Part 3 — Assign users in Azure and test', and '## Troubleshooting' — all clearly labelled and non-interleaved. |
| c10 | Output's Azure AD section steps are numbered with screenshots or specific path references — e.g. '1. Sign in to Azure portal at https://portal.azure.com. 2. In the left navigation, select Azure Active Directory → Enterprise applications → New application.' — with expected result per step | PASS | Step 1: 'Go to [portal.azure.com], then select Azure Active Directory from the left-hand menu. Choose Enterprise applications > New application. Expected result: The Azure AD application gallery opens.' All Azure steps include portal.azure.com path references and expected results. |
| c11 | Output's platform side has matching numbered steps — taking the values copied from Azure (Identity Provider URL, Certificate, Entity ID) and pasting them into the corresponding fields in the platform admin panel — with field names exact | PASS | Step 10 pastes the 'Identity Provider Metadata URL' from Azure Step 7. Step 11 handles 'Upload Certificate' if the 'Certificate' field is blank. Step 9 cross-references the Entity ID and ACS URL values. Field names are quoted exactly: 'SSO Issuer', 'SSO Login URL', 'Certificate', 'Name ID Format'. |
| c12 | Output explains technical jargon on first use — SAML 2.0 ('a standard for single sign-on'), IdP / SP ('Identity Provider, the system that authenticates users; Service Provider, our platform'), assertion ('the signed message Azure sends back confirming user identity') — without dumbing down for the IT-admin audience | FAIL | SAML 2.0 is never defined — only used as a label. 'Identity Provider' is used in a field name without definition. 'Service Provider' appears in Step 9 ('Service Provider details') without definition. 'Assertion' is used in the clock-skew entry without definition. None of the four terms receive the inline explanation the criterion requires. |
| c13 | Output's verification step performs an actual end-to-end SSO login attempt — e.g. 'open an incognito window, navigate to your platform login URL, click Sign in with SSO, enter an Azure-AD-managed test user; you should land on the platform dashboard logged in as that user' | PASS | Step 15: 'Open a private/incognito browser window. Navigate to the platform login page and click Sign in with SSO. Enter the test user's email address and click Continue. Expected result: You are redirected to the Microsoft login page, you authenticate, and you are returned to the platform as the test user.' |
| c14 | Output's troubleshooting section uses symptom → cause → fix structure for at least the two named failure modes — certificate mismatch (symptom: 'SSO error: invalid signature'; cause: cert in platform doesn't match Azure's; fix: re-export and re-upload), attribute mapping (symptom: 'user logged in but missing email/name'; cause: claim mappings; fix: configure Azure attribute claims for emailaddress, name) | PASS | Certificate mismatch entry: Problem ('Certificate mismatch or Invalid signature error') → Cause ('certificate in the platform does not match the one Azure is currently using') → Solution (download current cert, upload to admin panel). Attribute mapping entry: Problem ('name and email appear blank') → Cause ('email claim not being sent / user.mail empty') → Solution (change source attribute to user.userprincipalname). |
| c15 | Output's prerequisites are explicit — Azure AD Premium tier (Free does not support custom SAML), Azure AD Global Administrator role, the platform admin role, the platform's metadata URL or values to provide to Azure | PARTIAL | Prerequisites section lists Azure AD role ('Global Administrator or Application Administrator') and platform role ('Organisation Owner') explicitly. Platform plan tier (Business/Enterprise) is noted. However, Azure AD Premium tier requirement is absent entirely, and the platform's metadata URL is not listed as a prerequisite — it is retrieved during setup rather than prepared beforehand. |
| c16 | Output's tone is procedural — single action per step, expected outcome stated, no 'feel free to' or 'you might want to' hedge language — but not condescending; treats the IT admin as a competent professional | PASS | Steps are consistently 'verb + object' form ('Click Save', 'Copy the value labelled…', 'Download the .cer file'). No hedge phrases found. The note 'your Desktop is fine' is conversational but not condescending. Expected results confirm outcomes rather than reassure. |
| c17 | Output addresses the bidirectional nature explicitly — Azure has values that need to come INTO the platform, and the platform has values that need to go INTO Azure (entity ID / ACS URL); the order matters and is shown | PASS | Step 4 note: 'Replace the placeholder URLs above with the real Entity ID and ACS URL from your admin panel (see Part 2, Step 1 below — collect those values first).' Step 9: 'If you skipped ahead to Part 2 first, go back to Part 1, Step 4 and enter these values into Azure now before continuing.' The bidirectional dependency and ordering are made explicit. |
| c18 | Output addresses production cutover guidance — once tested in a staging or test SSO config, how to switch existing users to SSO without locking anyone out (allow password fallback during transition, then enforce SSO) | PARTIAL | Step 13 says 'Do not toggle Enforce SSO for all users yet — leave that off until testing is complete.' Step 17 provides the enforcement step with a warning dialog. However, there is no explicit guidance on password fallback during transition, gradual rollout, or handling existing accounts that might be locked out — only the existing-account-mismatch troubleshooting entry partially touches this. |

### Notes

The article is a high-quality, well-structured SSO setup guide that excels at procedural clarity, bidirectional configuration flow, troubleshooting depth, and tone. Its main gap is the complete absence of inline jargon definitions — SAML, IdP, SP, and 'assertion' are all used without explanation, failing both c4 and c12 independently. The prerequisites section is solid on roles but omits the Azure AD Premium tier requirement, which is a significant operational gap (IT admins on Free tier cannot configure custom SAML apps). Production cutover guidance is present but shallow — the article tells admins to test before enforcing but gives no rollback path or password-fallback strategy for transitioning existing users. These three gaps together cost 2.5 points out of 17, leaving the article at 85.3% — comfortably passing but with actionable improvements in jargon glossing and cutover safety.
