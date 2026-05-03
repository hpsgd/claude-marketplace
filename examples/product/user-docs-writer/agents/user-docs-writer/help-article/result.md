# Help Article

Scenario: A user-facing help article is needed explaining how to set up two-factor authentication for end users of a SaaS product.

## Prompt

> Write a help article for setting up two-factor authentication in Clearpath. Users can set up 2FA using:
> 1. Authenticator app (Google Authenticator, Authy, or any TOTP app)
> 2. SMS to their phone number
> 
> After enabling 2FA, they'll need to enter a code every time they log in. If they lose access to their 2FA method, they can use backup codes (generated at setup) or contact support.
> 
> Our users are non-technical — mostly project managers and team leads at mid-market companies. Some are on mobile, most are on desktop.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Here's the article, saved to `how-do-i-set-up-two-factor-authentication.md`:

---

# How do I set up two-factor authentication (2FA) in Clearpath?

## Short answer

Go to **Settings** > **Security** > **Two-factor authentication** and choose either an authenticator app or SMS verification. Once set up, you'll be asked for a short code each time you log in — which keeps your account safe even if your password is ever compromised.

---

## Prerequisites

No special requirements. Any Clearpath user can enable 2FA on their own account.

---

## Why bother with 2FA?

Your password alone can be stolen — through phishing emails, data breaches at other sites, or someone looking over your shoulder. Two-factor authentication adds a second check: even if someone has your password, they still can't get in without the code from your phone. It takes about two minutes to set up and significantly reduces the risk of unauthorised access to your projects and team data.

---

## Step-by-step: Set up an authenticator app (recommended)

An authenticator app generates a fresh 6-digit code every 30 seconds. It works without mobile signal or Wi-Fi. Google Authenticator, Authy, and Microsoft Authenticator all work with Clearpath.

1. **Download an authenticator app on your phone**
   If you don't already have one, install Google Authenticator or Authy from the App Store (iPhone) or Google Play (Android).

   Expected result: The app opens to an empty screen ready to add accounts.

2. **Open your Clearpath security settings**
   Click your profile picture or initials in the top-right corner of Clearpath, then select **Account settings**. Choose **Security** from the left-hand menu.

   Expected result: You'll see a "Two-factor authentication" section showing your current status as **Off**.

3. **Start the setup**
   Click **Enable two-factor authentication**, then select **Authenticator app** and click **Continue**.

   Expected result: A QR code appears on screen, along with a text code underneath it.

4. **Scan the QR code**
   Open your authenticator app and tap the **+** button (or **Add account**). Point your phone camera at the QR code on screen. If scanning doesn't work, tap **Enter code manually** in the app and type the text code shown in Clearpath instead.

   Expected result: Clearpath appears as a new entry in your authenticator app, showing a 6-digit code that refreshes every 30 seconds.

5. **Enter the 6-digit code to confirm**
   Type the current 6-digit code shown in your authenticator app into the **Verification code** field in Clearpath, then click **Verify**.

   Expected result: Clearpath confirms setup is complete and displays your backup codes. **Do not close this screen until you have saved your backup codes** (see step 6).

6. **Save your backup codes**
   Click **Download backup codes** to save them as a file, or copy them somewhere safe (a password manager, a printed sheet in a secure place). You get 10 single-use codes.

   Expected result: Your backup codes are saved and the setup screen shows "Two-factor authentication is now enabled."

---

## Step-by-step: Set up SMS verification

SMS sends a code to your mobile number each time you log in. It requires mobile signal at login time.

*(Steps follow the same pattern — enter number, verify, save backup codes.)*

---

## What happens next?

Every time you log in, after entering your email and password, you'll see a **"Enter your verification code"** screen. Enter the 6-digit code from your app or text message. The code is only valid for 30 seconds, so enter it promptly.

---

## If you lose access to your 2FA method

- **Use a backup code** — on the login screen, click **Use a backup code** and enter one of the 10 codes saved during setup. Each can only be used once.
- **Contact support** — if you don't have backup codes, reach the Clearpath team via support@clearpath.com or the chat icon on the login page.

---

## Troubleshooting (highlights)

| Problem | Fix |
|---|---|
| Code is rejected | Sync your phone's clock to automatic in date/time settings |
| No SMS received | Wait 1 min, click **Resend code**, check the country code is correct |
| QR code won't scan | Hold phone 15–30 cm away; use the manual text code as a fallback |
| Not prompted for code after setup | Log out and back in to start a fresh session |
| Screen looks different | Use a desktop browser for setup — mobile layout varies |

---

A few decisions worth flagging if you want to adjust before publishing:

- **Navigation paths** (`Settings > Security > Two-factor authentication`) are assumed — verify these match the actual Clearpath UI.
- **Backup code count** (10 codes) is a common default — confirm if Clearpath uses a different number.
- **Related articles** are all marked *To be created* since no existing help content was found.

### Artifacts written

#### `work/how-do-i-set-up-two-factor-authentication.md`

```
# How do I set up two-factor authentication (2FA) in Clearpath?

## Short answer

Go to **Settings** > **Security** > **Two-factor authentication** and choose either an authenticator app or SMS verification. Once set up, you'll be asked for a short code each time you log in — which keeps your account safe even if your password is ever compromised.

---

## Prerequisites

No special requirements. Any Clearpath user can enable 2FA on their own account.

---

## Why bother with 2FA?

Your password alone can be stolen — through phishing emails, data breaches at other sites, or someone looking over your shoulder. Two-factor authentication adds a second check: even if someone has your password, they still can't get in without the code from your phone. It takes about two minutes to set up and significantly reduces the risk of unauthorised access to your projects and team data.

---

## Step-by-step: Set up an authenticator app (recommended)

An authenticator app generates a fresh 6-digit code every 30 seconds. It works without mobile signal or Wi-Fi. Google Authenticator, Authy, and Microsoft Authenticator all work with Clearpath.

1. **Download an authenticator app on your phone**
   If you don't already have one, install Google Authenticator or Authy from the App Store (iPhone) or Google Play (Android).

   Expected result: The app opens to an empty screen ready to add accounts.

2. **Open your Clearpath security settings**
   Click your profile picture or initials in the top-right corner of Clearpath, then select **Account settings**. Choose **Security** from the left-hand menu.

   Expected result: You'll see a "Two-factor authentication" section showing your current status as **Off**.

3. **Start the setup**
   Click **Enable two-factor authentication**, then select **Authenticator app** and click **Continue**.

   Expected result: A QR code appears on screen, along with a text code underneath it.

4. **Scan the QR code**
   Open your authenticator app and tap the **+** button (or **Add account**). Point your phone camera at the QR code on screen. If scanning doesn't work, tap **Enter code manually** in the app and type the text code shown in Clearpath instead.

   Expected result: Clearpath appears as a new entry in your authenticator app, showing a 6-digit code that refreshes every 30 seconds.

5. **Enter the 6-digit code to confirm**
   Type the current 6-digit code shown in your authenticator app into the **Verification code** field in Clearpath, then click **Verify**.

   Expected result: Clearpath confirms setup is complete and displays your backup codes. **Do not close this screen until you have saved your backup codes** (see step 6).

6. **Save your backup codes**
   Click **Download backup codes** to save them as a file, or copy them somewhere safe (a password manager, a printed sheet in a secure place). You get 10 single-use codes.

   Expected result: Your backup codes are saved and the setup screen shows "Two-factor authentication is now enabled."

---

## Step-by-step: Set up SMS verification

SMS sends a code to your mobile number each time you log in. It requires mobile signal at login time.

1. **Open your Clearpath security settings**
   Click your profile picture or initials in the top-right corner of Clearpath, then select **Account settings**. Choose **Security** from the left-hand menu.

   Expected result: You'll see a "Two-factor authentication" section showing your current status as **Off**.

2. **Start the setup**
   Click **Enable two-factor authentication**, then select **Text message (SMS)** and click **Continue**.

   Expected result: A phone number entry field appears.

3. **Enter your mobile number**
   Type your mobile number including country code (e.g. +1 for the US, +44 for the UK), then click **Send code**.

   Expected result: Clearpath sends a text message to your number within one minute. If you don't receive it, check the number is correct and click **Resend code**.

4. **Enter the code from the text message**
   Type the 6-digit code from the text message into the **Verification code** field in Clearpath, then click **Verify**.

   Expected result: Clearpath confirms setup is complete and displays your backup codes. **Do not close this screen until you have saved your backup codes** (see step 5).

5. **Save your backup codes**
   Click **Download backup codes** to save them as a file, or copy them somewhere safe (a password manager, a printed sheet in a secure place). You get 10 single-use codes.

   Expected result: Your backup codes are saved and the setup screen shows "Two-factor authentication is now enabled."

---

## What happens next?

Every time you log in to Clearpath, after entering your email and password, you'll see a **"Enter your verification code"** screen. Open your authenticator app (or check your texts) and enter the current 6-digit code. The code is only valid for 30 seconds, so enter it promptly.

---

## If you lose access to your 2FA method

**Use a backup code**
On the login screen, click **Use a backup code** instead of entering the 6-digit code. Enter one of the 10 codes you saved during setup. Each backup code can only be used once.

Once you're logged in, go to **Settings** > **Security** > **Two-factor authentication** and set up 2FA again with your new phone or number.

**Contact support**
If you don't have your backup codes, contact the Clearpath support team. They'll verify your identity and help you regain access. You can reach them at support@clearpath.com or via the chat icon in the bottom-right corner of the login page.

---

## Troubleshooting

**Problem**: The 6-digit code from the authenticator app is rejected.
**Cause**: Your phone's clock may be out of sync, causing codes to be generated at the wrong time.
**Solution**: On iPhone, go to **Settings** > **General** > **Date & Time** and enable **Set Automatically**. On Android, go to **Settings** > **General management** > **Date and time** and enable **Automatic date and time**. Then try the code again.

---

**Problem**: You didn't receive an SMS code.
**Cause**: The number may have been entered incorrectly, or there may be a temporary delay with your carrier.
**Solution**: Wait one minute, then click **Resend code** on the Clearpath screen. Check that the number shown matches your mobile number exactly, including the country code. If the number is wrong, click **Change number** to re-enter it.

---

**Problem**: The QR code won't scan.
**Cause**: Poor lighting, screen glare, or the camera being too close or far.
**Solution**: Hold your phone 15–30 cm from the screen in a well-lit room. If it still won't scan, use the text code shown beneath the QR code — tap **Enter code manually** in your authenticator app and type it in.

---

**Problem**: You've set up 2FA but aren't being asked for a code at login.
**Cause**: You may still have an active session from before 2FA was enabled.
**Solution**: Log out of Clearpath and log back in. You should see the code prompt on your next login.

---

**Problem**: Setup steps look different on your screen.
**Cause**: Clearpath's interface may look slightly different on mobile browsers compared to desktop.
**Solution**: For the smoothest setup experience, use a desktop browser. The steps are the same, but the layout and button positions may vary on smaller screens.

---

## Related articles

**Next steps**
- How do I generate new backup codes? *(To be created)*
- How do I turn off two-factor authentication? *(To be created)*

**Related topics**
- How do I change my password in Clearpath? *(To be created)*
- How do I manage team member access and permissions? *(To be created)*

**Background**
- Keeping your Clearpath account secure — best practices *(To be created)*

---

```
Last verified: 2026-05-01
Product area: Account security
Applies to: All plans
Tags: 2FA, two-factor authentication, security, login, authenticator app, SMS
```

---

**Maintenance notes**

- **Update trigger**: Review this article whenever the 2FA setup flow changes in a Clearpath release.
- **Staleness check**: If this article has not been verified in 90 days, flag it for review.
- **Helpfulness tracking**: Monitor article views against support tickets about 2FA setup. High traffic with ongoing tickets means the article isn't solving the problem — revisit the troubleshooting section first.
- **Retirement criteria**: Archive this article if the 2FA feature is replaced, and redirect to the successor article.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 11.5/11.5 (100%) |
| Evaluated | 2026-05-01 |
| Target duration | 90779 ms |
| Target cost | $0.1489 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Uses only product language — no jargon like "TOTP", "OTP", or technical acronyms without plain-language explanation | PASS | The article never uses 'TOTP' or 'OTP'. '2FA' is introduced in the title as 'two-factor authentication (2FA)'. Codes are referred to throughout as '6-digit code' rather than OTP. Authenticator apps are described functionally: 'generates a fresh 6-digit code every 30 seconds'. |
| c2 | Every step includes what the user should see or expect after completing it — not just the action, but the confirmation | PASS | Every numbered step in both setup paths includes an 'Expected result:' line. For example, Step 4 (scan QR code): 'Expected result: Clearpath appears as a new entry in your authenticator app, showing a 6-digit code that refreshes every 30 seconds.' All 6 authenticator steps and all 5 SMS steps follow this pattern. |
| c3 | Covers both setup methods (authenticator app and SMS) as separate, clearly labelled paths | PASS | The file contains two distinct H2 sections: 'Step-by-step: Set up an authenticator app (recommended)' with 6 numbered steps and 'Step-by-step: Set up SMS verification' with 5 numbered steps, each fully detailed in the artifact. |
| c4 | Explains what to do if the user loses access to their 2FA method — backup codes and support contact path are both documented | PASS | 'If you lose access to your 2FA method' section covers both paths: backup codes ('click Use a backup code... Enter one of the 10 codes you saved during setup') and support contact ('contact the Clearpath support team... support@clearpath.com or via the chat icon in the bottom-right corner of the login page'). |
| c5 | Title is written as a task or outcome the user is trying to accomplish, not a feature description | PASS | Title is 'How do I set up two-factor authentication (2FA) in Clearpath?' — phrased as a user question/task, not a feature label like '2FA Configuration Guide'. |
| c6 | Addresses the mobile user path — partial credit if desktop is fully covered but mobile considerations are mentioned but not detailed | PARTIAL | Mobile is mentioned in multiple places: app download links specify 'App Store (iPhone) or Google Play (Android)', clock sync troubleshooting covers both iPhone and Android settings paths, and a troubleshooting entry notes 'for the smoothest setup experience, use a desktop browser' because 'layout and button positions may vary on smaller screens.' However, there is no dedicated mobile setup walkthrough — the main steps assume desktop. |
| c7 | Does not assume the user knows why 2FA matters — briefly explains the benefit without lecturing | PASS | 'Why bother with 2FA?' section states: 'Your password alone can be stolen... Two-factor authentication adds a second check: even if someone has your password, they still can't get in without the code from your phone. It takes about two minutes to set up.' Concise, practical, no security treatise. |
| c8 | Includes a troubleshooting section or FAQ covering common problems (wrong code, code expired, lost phone) | PASS | Troubleshooting section covers: rejected authenticator code (clock sync fix), no SMS received (resend + country code check), QR code won't scan (distance + manual fallback), not prompted for code (session logout fix), and different screen layout on mobile. Lost phone/access is addressed in the dedicated 'If you lose access' section above. |
| c9 | Output's title is a task / outcome the user is trying to accomplish — e.g. "How to set up two-factor authentication" or "Turn on extra security for your account" — not "2FA Configuration" or "TOTP Setup Guide" | PASS | File title is 'How do I set up two-factor authentication (2FA) in Clearpath?' — a direct user task question, not a feature/technical label. |
| c10 | Output covers BOTH setup methods as separate, clearly labelled paths — "Option 1: Authenticator app" and "Option 2: SMS to your phone" — with a brief recommendation (authenticator app preferred for security) but not blocking the SMS path | PASS | Authenticator app section is labelled '(recommended)' in its heading. SMS section has its own complete 5-step path. The recommendation is a label, not a gate — SMS steps are fully detailed without discouragement language. |
| c11 | Output's steps each describe what the user SHOULD SEE after — e.g. "Step 3: Scan the QR code. You'll see 'Connected' appear next to the app name." — not just the action | PASS | Every numbered step in the file includes an 'Expected result:' line. Example from SMS path Step 3: 'Expected result: Clearpath sends a text message to your number within one minute. If you don't receive it, check the number is correct and click Resend code.' All 11 steps across both paths follow this structure. |
| c12 | Output explains WHY 2FA matters in 1-2 sentences without lecturing — "Even if someone gets your password, they can't sign in without your phone" — not a security treatise | PASS | 'Why bother with 2FA?' delivers the core message concisely: 'even if someone has your password, they still can't get in without the code from your phone.' The section is one short paragraph and moves on — no extended security lecture. |

### Notes

The article is exceptionally well-executed across all criteria. Every step in both setup paths has an 'Expected result:' confirmation, both methods are fully detailed with distinct labelled sections, the title is task-framed, no jargon slips through, and recovery paths (backup codes + support) are both covered with actionable detail. The only ceiling-limited criterion (c6, mobile) earns its PARTIAL: mobile is thoughtfully woven in (platform-specific clock sync steps, app store links, a troubleshooting entry) but there is no dedicated mobile walkthrough — the article actively recommends desktop for setup. One minor gap is that the chat response showed the SMS section as a placeholder ('Steps follow the same pattern'), but the actual artifact file contains full SMS steps, so criteria judged against the file content are well satisfied. The article also adds genuinely useful maintenance metadata (staleness check, helpfulness tracking, update triggers) that wasn't required but adds professional quality.
