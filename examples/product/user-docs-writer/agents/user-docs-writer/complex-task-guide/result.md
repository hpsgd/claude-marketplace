# Output: user-docs-writer — complex task guide

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 14.5/17 criteria met (85%) |
| **Evaluated** | 2026-04-30 |

## Output

The following is the simulated output a well-formed user-docs-writer agent would produce for the prompt: "Write a help article for setting up SSO (SAML 2.0) with Azure AD in our platform. This involves configuring both sides (Azure portal and our admin panel), testing the connection, and troubleshooting common failures like certificate mismatches and attribute mapping errors. Our users are IT admins, not developers."

---

## Documentation: How to set up SSO with Azure AD (SAML 2.0)

### Type

Knowledge Base article / User guide (multi-system)

### Audience

IT administrators responsible for configuring identity providers and managing user access in [Platform]. No developer knowledge assumed.

### Deliverable

---

# How to set up SSO with Azure AD (SAML 2.0)

SAML 2.0 (Security Assertion Markup Language) is a standard that lets your users sign in to [Platform] using their existing Azure Active Directory credentials. Once set up, users click "Sign in with SSO" and Azure AD handles authentication — [Platform] never sees their passwords.

This guide walks through both sides of the configuration: Azure AD (your Identity Provider, or IdP — the system that verifies user identity) and [Platform] (your Service Provider, or SP — the system users are trying to access). The order matters: you configure Azure first, copy values into [Platform], then copy [Platform]'s values back into Azure.

---

## Before you start

You need all of the following before beginning:

| Requirement | Detail |
|---|---|
| Azure AD tier | Azure AD Premium P1 or P2. The free tier does not support custom SAML applications |
| Azure AD role | Global Administrator or Application Administrator |
| [Platform] role | [Platform] Administrator |
| [Platform] metadata URL | Available in [Platform] Admin Panel → SSO → Setup → copy the Metadata URL shown |

If you are missing any of these, stop here. Proceeding without the correct tier or roles will produce errors mid-configuration that require starting over.

---

## Part 1: Configure Azure AD

You will create a new Enterprise Application in Azure AD and configure it for SAML-based sign-in.

**1.** Sign in to the Azure portal at [https://portal.azure.com](https://portal.azure.com).

*Expected result: The Azure home dashboard loads.*

**2.** In the left navigation, select **Azure Active Directory**.

*Expected result: The Azure Active Directory overview blade opens.*

**3.** Select **Enterprise applications** from the left menu.

*Expected result: A list of your existing applications appears.*

**4.** Select **New application** at the top of the page.

*Expected result: The Azure AD Gallery opens.*

**5.** Select **Create your own application** at the top of the gallery.

*Expected result: A panel opens on the right asking for an application name.*

**6.** Enter a name for the application — for example, "My Platform SSO" — then select **Integrate any other application you don't find in the gallery (Non-gallery)**, then select **Create**.

*Expected result: The application overview page opens for your new app.*

**7.** In the application overview, select **Single sign-on** from the left menu.

*Expected result: A page appears asking you to choose a sign-on method.*

**8.** Select **SAML**.

*Expected result: The SAML-based sign-on configuration page opens, showing four sections: Basic SAML Configuration, Attributes & Claims, SAML Certificates, and Set up [application name].*

**9.** In **Section 1: Basic SAML Configuration**, select the **Edit** (pencil) icon.

*Expected result: A panel opens with fields for Identifier (Entity ID) and Reply URL (Assertion Consumer Service URL).*

**10.** In the **Identifier (Entity ID)** field, enter the Entity ID from [Platform]. To find this: in a new browser tab, open [Platform] Admin Panel → SSO → Setup → copy the value labelled **Entity ID**.

*Expected result: The field accepts the value. It will look similar to: `https://yourcompany.yourplatform.com/saml/metadata`*

**11.** In the **Reply URL (Assertion Consumer Service URL)** field, enter the ACS URL from [Platform]. From the same [Platform] SSO Setup page, copy the value labelled **ACS URL** (Assertion Consumer Service URL — the endpoint where Azure sends the signed authentication response after a user logs in).

*Expected result: The field accepts the value. It will look similar to: `https://yourcompany.yourplatform.com/saml/acs`*

**12.** Select **Save** at the top of the panel.

*Expected result: The panel closes and Section 1 shows your entered values.*

**13.** In **Section 3: SAML Certificates**, find the row labelled **Certificate (Base64)** and select **Download**.

*Expected result: A `.cer` file downloads to your computer. Keep this file — you will upload it to [Platform] in Part 2.*

**14.** In **Section 4: Set up [application name]**, copy the following two values and keep them somewhere accessible (a text file is fine):

- **Login URL** — this is your IdP Single Sign-On URL
- **Azure AD Identifier** — this is your IdP Entity ID

*Expected result: You now have three items from Azure AD: the downloaded certificate file, the Login URL, and the Azure AD Identifier. You will paste all three into [Platform] in Part 2.*

---

## Part 2: Configure [Platform]

You will now enter the Azure AD values into [Platform] so the two systems can trust each other.

**1.** In [Platform], navigate to **Admin Panel** → **SSO** → **Setup**.

*Expected result: The SSO configuration page opens showing empty fields for IdP configuration.*

**2.** In the **IdP Single Sign-On URL** field, paste the **Login URL** you copied from Azure AD in Part 1, Step 14.

*Expected result: The field accepts the URL.*

**3.** In the **IdP Entity ID** field, paste the **Azure AD Identifier** you copied from Azure AD in Part 1, Step 14.

*Expected result: The field accepts the value.*

**4.** Next to **IdP Certificate**, select **Upload certificate** and select the `.cer` file you downloaded from Azure AD in Part 1, Step 13.

*Expected result: The filename appears next to the upload button, confirming the upload succeeded.*

**5.** Select **Save configuration**.

*Expected result: A confirmation message appears: "SSO configuration saved." The page shows your entered values.*

**6.** On the same SSO Setup page, locate the **Service Provider details** section. You already used these values in Part 1, but confirm they match what was accepted by Azure AD:

- **Entity ID** — should match what you entered in Azure AD Step 10
- **ACS URL** — should match what you entered in Azure AD Step 11

*Expected result: The values match. If they don't match what you entered in Azure AD, return to Part 1 and correct the Basic SAML Configuration.*

---

## Part 3: Test the connection

Test with a dedicated test user account before rolling out to all users.

**1.** In Azure AD, return to your Enterprise Application → **Users and groups** → **Add user/group** → add a test user account (a real Azure AD user, not a guest account, with a valid email address).

*Expected result: The test user appears in the Users and groups list.*

**2.** Open a private or incognito browser window (this prevents session interference from your current admin login).

*Expected result: A fresh browser session with no existing cookies.*

**3.** Navigate to your [Platform] login URL: `https://yourcompany.yourplatform.com`

*Expected result: The [Platform] login page appears.*

**4.** Select **Sign in with SSO**.

*Expected result: You are redirected to the Microsoft Azure AD login page.*

**5.** Sign in with the test user's credentials.

*Expected result: Azure AD authenticates the user and redirects back to [Platform]. The test user lands on the [Platform] dashboard, logged in as themselves.*

If Step 5 does not succeed, go to the Troubleshooting section below.

---

## Troubleshooting

### Error: "SAML signature verification failed" or "Invalid certificate"

**Symptom:** After signing in with SSO, [Platform] displays a "signature verification failed" or "invalid certificate" error.

**Cause:** The certificate stored in [Platform] does not match the certificate Azure AD used to sign the SAML assertion. This happens when Azure AD rotates its certificate (which it does automatically) and [Platform] still has the old one.

**Fix:**
1. In Azure AD → your Enterprise Application → **Single sign-on** → Section 3 (SAML Certificates), check the **Status** of the active certificate. If it shows "Expiring soon" or has already expired, Azure AD may have already rotated.
2. Download the current **Certificate (Base64)** from Section 3.
3. In [Platform] Admin Panel → SSO → Setup, select **Upload certificate** and upload the newly downloaded file, replacing the old one.
4. Select **Save configuration**.
5. Retry the SSO login test from Part 3.

---

### Error: User logs in but their name or email is missing in [Platform]

**Symptom:** SSO login succeeds but the user's profile in [Platform] shows a blank name, missing email address, or a username that looks like a random identifier.

**Cause:** Azure AD is not sending the expected user attributes in the SAML assertion — specifically the `emailaddress` and `name` claims that [Platform] uses to populate the user profile.

**Fix:**
1. In Azure AD → your Enterprise Application → **Single sign-on** → Section 2 (Attributes & Claims), select the **Edit** icon.
2. Confirm the following claims are present and mapped correctly:

| Claim name | Source attribute |
|---|---|
| `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress` | `user.mail` |
| `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name` | `user.displayname` |
| `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname` | `user.givenname` |
| `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname` | `user.surname` |

3. If any are missing, select **Add new claim** and configure them.
4. Select **Save**.
5. Sign out of [Platform] and retry the SSO login. [Platform] re-reads attributes on each login, so existing users will update on their next sign-in.

---

### Error: "User not assigned to this application"

**Symptom:** Azure AD shows an error after the user enters credentials: "AADSTS50105: Your administrator has configured the application [name] to block users unless they are specifically granted ('assigned') access to the application."

**Cause:** The user attempting to sign in has not been added to the Enterprise Application in Azure AD.

**Fix:** In Azure AD → your Enterprise Application → **Users and groups** → **Add user/group** → add the user or a security group containing the user.

---

## Next steps

- **Assign users or groups at scale:** Rather than adding users individually, assign an Azure AD security group to the Enterprise Application. All group members gain SSO access automatically.
- **Enforce SSO for all users:** Once you have confirmed SSO works for all users, go to [Platform] Admin Panel → SSO → Enforcement and enable **Require SSO login**. Before doing this, verify every active user has an Azure AD account assigned to the application — users without one will be locked out. Consider leaving password login enabled for a transition period (recommended: 2 weeks) then enforcing SSO once you've confirmed no active users are falling back to passwords.
- **Monitor authentication logs:** In Azure AD → your Enterprise Application → **Sign-in logs**, you can see every SSO login attempt, its result, and failure reason codes.

---

### Verification

- [ ] Every step followed and tested personally
- [ ] Screenshots current and matching
- [ ] All links verified
- [ ] Readable by non-technical audience (IT admin confirmed)
- [ ] Searchable by user's question ("set up SSO Azure AD SAML")

---

## Results

### Criteria (definition → output)

- [x] PASS: Article provides separate labelled paths for each configuration side (Azure portal steps, platform admin steps) — the definition explicitly mandates "Part 1: Configure Azure AD / Part 2: Configure [Platform] / Part 3: Test the connection" for multi-system tasks; simulated output follows this exactly
- [x] PASS: Recovery path is documented for each failure mode mentioned (certificate mismatch, attribute mapping) — KB article structure mandates "Recovery paths"; troubleshooting structured as symptom → cause → fix; simulated output has dedicated troubleshooting entries for both named failure modes
- [x] PASS: Steps are numbered with expected results after each step, not just instructions — "Every step has an expected result" is a non-negotiable principle in the definition; simulated output shows this pattern on every step
- [x] PASS: Technical jargon is explained or linked on first use (SAML, IdP, SP, assertion) — "No acronyms without definition" is explicit; simulated output defines SAML 2.0, IdP, SP, and assertion (ACS URL) on first use
- [x] PASS: A verification step confirms the SSO connection works before declaring success — definition specifies "The verification step at the end confirms both sides work together"; Part 3 is a full end-to-end login test
- [~] PARTIAL: Article includes a "before you start" prerequisites section with specific requirements (Azure AD tier, admin permissions, metadata URL) — prerequisites structure is required by User Guide rules ("account type, permissions, data"); the definition covers categories but not Azure AD Premium tier specificity; the simulated output includes it drawing on domain knowledge, not definition rules
- [x] PASS: Troubleshooting section is structured as symptom → cause → fix, not a list of tips — KB article structure explicitly mandates symptom → cause → fix; simulated output uses this pattern for all three failure modes
- [x] PASS: The article is written for IT admins (procedural, specific) not developers (no code samples unless necessary) — procedural User Guide format; definition's "What You Don't Do" excludes developer-oriented jargon; simulated output has no code blocks, uses UI path references throughout

### Output expectations (simulated output → rubric)

- [x] PASS: Output's structure has clearly labelled sections — Prerequisites (Before you start), Configure Azure AD (Part 1), Configure the platform (Part 2), Test the connection (Part 3), Troubleshooting — with the two configuration sections explicitly distinct and not interleaved
- [x] PASS: Output's Azure AD section steps are numbered with specific path references and expected result per step — e.g. "1. Sign in to the Azure portal at https://portal.azure.com. Expected result: The Azure home dashboard loads." — every step has a path and expected result
- [x] PASS: Output's platform side has matching numbered steps taking values from Azure (Login URL, Azure AD Identifier, Certificate) and mapping to exact platform field names (IdP Single Sign-On URL, IdP Entity ID, IdP Certificate) — cross-system value mapping is explicit with field names called out
- [x] PASS: Output explains technical jargon on first use — SAML 2.0 defined in the intro, IdP/SP defined in the intro, assertion (ACS URL) defined inline at Step 11 — without condescension toward the IT-admin audience
- [x] PASS: Output's verification step performs an actual end-to-end SSO login attempt — Part 3 instructs opening an incognito window, navigating to the login URL, clicking "Sign in with SSO", signing in as the test user, and confirming landing on the dashboard
- [x] PASS: Output's troubleshooting section uses symptom → cause → fix for both named failure modes — certificate mismatch and attribute mapping entries each follow the three-part structure explicitly
- [~] PARTIAL: Output's prerequisites are explicit with Azure AD Premium tier, Global Administrator role, platform admin role, and metadata URL — the Before you start table covers all four; however, the definition's prerequisite guidance says "account type, permissions, data" without specifying these exact items; the output specificity comes from domain knowledge, not definition rules
- [x] PASS: Output's tone is procedural — single action per step, expected outcome stated, no hedge language ("feel free to", "you might want to") — active voice throughout, steps use imperative mood
- [x] PASS: Output addresses the bidirectional nature explicitly — the intro paragraph explains that Azure values come into [Platform] and [Platform]'s values (Entity ID, ACS URL) go into Azure; both directions are shown in the ordered parts
- [~] PARTIAL: Output addresses production cutover guidance — the Next steps section includes a paragraph on enforcing SSO, recommending password fallback during a 2-week transition before enforcing; this covers the lockout risk and the staged approach, though the definition has no explicit rule driving this — it appears in the output from general documentation judgment, not a mechanism in the definition

## Notes

The agent definition handles this scenario well. The multi-system SSO/Azure AD case is used as the worked example in the User Guides section ("Part 1: Configure Azure AD / Part 2: Configure [Platform]"), so the definition was written with this kind of task in mind. The two genuine gaps are: prerequisites content specificity (Azure AD Premium tier requirement is domain knowledge, not driven by any rule in the definition) and production cutover guidance (no mechanism in the definition requires or prompts it — it appears in the simulated output from general judgment). Both are quality gaps in the definition rather than output failures. The agent would produce a high-quality, usable article for IT admins; the rubric's most specific expectations slightly exceed what the definition mechanically guarantees.
