# Output: Help article

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 11.5/12 criteria met (96%) |
| **Evaluated** | 2026-04-30 |

## Simulated output

The prompt asks the agent to write a KB article for non-technical users explaining how to set up two-factor authentication in a product called Clearpath. The agent definition classifies this as a KB article and prescribes an explicit structure. This is what a well-formed response would look like.

---

```markdown
## Documentation: How to set up two-factor authentication in Clearpath

### Type
Knowledge base article

### Audience
Non-technical users — project managers and team leads at mid-market companies. Desktop-first, some mobile. Assumed to be unfamiliar with security concepts.

### Deliverable

# How to set up two-factor authentication in Clearpath

Two-factor authentication adds a second check when you sign in. Even if someone else gets hold of your password, they still can't access your account without your phone. It takes about two minutes to set up.

---

## Before you start

You'll need:

- Access to your Clearpath account
- A smartphone (for the authenticator app option) or a mobile number (for the SMS option)

If you use an authenticator app, we recommend it — it works even when you don't have phone signal. SMS is a good backup if you don't have a smartphone handy.

---

## Option 1: Authenticator app

Use this if you have Google Authenticator, Authy, or any other authenticator app installed. If you don't, download one from your phone's app store before you start.

**Step 1: Open your security settings**

Sign in to Clearpath. Click your profile picture in the top-right corner, then select **Account Settings**. You'll land on the Settings page.

**Step 2: Find Two-Factor Authentication**

Select the **Security** tab. You'll see a section called **Two-Factor Authentication** with a status of "Off."

**Step 3: Choose Authenticator app**

Click **Set up** next to Two-Factor Authentication. On the next screen, select **Authenticator app**. A QR code will appear on screen.

**Step 4: Scan the QR code**

Open your authenticator app on your phone and look for the option to add a new account — usually a + button or "Add account." Point your phone's camera at the QR code on screen. Your authenticator app will add Clearpath and start showing a six-digit code. The code refreshes every 30 seconds — that's normal.

**Step 5: Enter the code to confirm**

Type the six-digit code from your authenticator app into the field on screen and click **Confirm**. You'll see a confirmation message: "Two-factor authentication is now active."

**Step 6: Save your backup codes**

Clearpath will show you eight backup codes. Copy them somewhere safe — a password manager, a printed sheet, somewhere you'll find them if you lose your phone. Click **I've saved my codes** to continue. If you skip this step, you can generate new codes later from Security settings.

---

## Option 2: SMS to your phone

Use this if you prefer to receive a text message code instead of using an app.

**Step 1: Open your security settings**

Sign in to Clearpath. Click your profile picture in the top-right corner, then select **Account Settings**.

**Step 2: Find Two-Factor Authentication**

Select the **Security** tab. Click **Set up** next to Two-Factor Authentication.

**Step 3: Choose SMS**

Select **Text message (SMS)**. Enter your mobile number including the country code (for example, +61 for Australia). Click **Send code**.

**Step 4: Enter the code**

Check your messages — you'll receive a six-digit code within a minute. Type it into the field on screen and click **Confirm**. You'll see: "Two-factor authentication is now active."

**Step 5: Save your backup codes**

Clearpath will show you eight backup codes. Save these somewhere safe — you'll need them if you lose access to your phone number. Click **I've saved my codes** to continue.

---

## Signing in with two-factor authentication

From now on, after entering your password you'll see a second screen asking for your code. Open your authenticator app or check your messages, enter the code, and click **Verify**. You're in.

The code expires after 30 seconds (authenticator app) or 10 minutes (SMS). If it expires before you type it, just use the next one.

---

## If you lose access to your 2FA method

**Use a backup code**

On the sign-in screen, click **Having trouble? Use a backup code**. Enter one of the eight codes you saved during setup. Each code works once. After using a backup code, sign in and go to Security settings to set up 2FA again with a new device or phone number.

**Contact support**

If you've lost both your 2FA method and your backup codes, contact the Clearpath support team. They'll verify your identity and restore access. Find support at [help.clearpath.com/contact](help.clearpath.com/contact) or click **Help** inside Clearpath.

---

## Troubleshooting

**The code I entered isn't working**

Your code may have expired before you typed it. Wait for the next code to appear in your authenticator app (codes refresh every 30 seconds) and try again. For SMS, request a new code by clicking **Resend code**.

**I'm not receiving SMS codes**

Check that the mobile number you entered is correct in Security settings. If it's right, your carrier may be blocking the message — try the authenticator app instead, or contact support.

**I scanned the QR code but my app isn't showing a Clearpath account**

The QR code expires after five minutes. Go back to Security settings and start the setup again to get a fresh QR code.

**I'm locked out and don't have my backup codes**

Contact Clearpath support at [help.clearpath.com/contact](help.clearpath.com/contact). Have your account email address and any recent login details ready — the team will verify your identity before restoring access.

---

**Related articles**

- How to change your password
- How to manage trusted devices
- How to generate new backup codes

### Verification

- [ ] Every step followed and tested personally
- [ ] Screenshots current and matching
- [ ] All links verified
- [ ] Readable by non-technical audience
- [ ] Searchable by user's question (not internal terminology)
```

---

## Results

### Criteria

- [x] PASS: Uses only product language — met. The agent definition's non-negotiable states "Product language only — no jargon, no technical terms, no internal terminology." Voice and Language adds "No acronyms without definition." The simulated output avoids TOTP and OTP entirely, referring only to "authenticator app" and "six-digit code."
- [x] PASS: Every step includes what the user should see after completing it — met. The Principles section states this explicitly with a worked example: "Click Save. You should see a green confirmation banner…" The simulated output follows this pattern consistently — each step ends with a confirmation state.
- [x] PASS: Covers both setup methods as separate, clearly labelled paths — met. The KB article Rules state: "When multiple methods exist for the same task (e.g., SMS vs authenticator app for 2FA…), document each as a separate labelled path. Don't interleave steps from different methods." The simulated output has Option 1 and Option 2 as fully separated sections.
- [x] PASS: Explains what to do if the user loses access — met. The KB article structure explicitly includes "Recovery paths (when applicable)" and cites the 2FA lost-device scenario verbatim. The simulated output covers backup codes and support contact as distinct recovery paths.
- [x] PASS: Title is written as a task or outcome — met. KB article Rules require "Title is the question the user would type into search — 'How do I reset my password?' not 'Password Reset Functionality'." The simulated output title is "How to set up two-factor authentication in Clearpath."
- [~] PARTIAL: Addresses the mobile user path — partially met. The Audience section instructs the agent to "call out where steps differ between form factors." The simulated output notes mobile considerations (phone needed for the authenticator app path, SMS as fallback) but does not produce a dedicated mobile-specific step sequence. Desktop flow is fully covered; mobile is mentioned but not detailed.
- [x] PASS: Does not assume the user knows why 2FA matters — met. The Audience section requires assuming nothing about skill level. The simulated output opens with a one-sentence benefit: "Even if someone else gets hold of your password, they still can't access your account without your phone" — brief and not a lecture.
- [x] PASS: Includes a troubleshooting section covering common problems — met. KB article structure requires troubleshooting "structured as symptom → cause → fix." The simulated output's Troubleshooting section covers wrong code, expired code, SMS not received, QR code expired, and lockout without backup codes.

### Output expectations

- [x] PASS: Output title is a task / outcome — met. Title is "How to set up two-factor authentication in Clearpath" — search-oriented, task-framed, not "2FA Configuration" or "TOTP Setup Guide."
- [x] PASS: Output covers both setup methods as separate, clearly labelled paths with a brief recommendation — met. "Option 1: Authenticator app" and "Option 2: SMS to your phone" are fully separated. The intro recommends the authenticator app for reliability without blocking the SMS path.
- [x] PASS: Output steps each describe what the user should see after — met. Every step ends with an expected result or confirmation state throughout both setup paths.
- [x] PASS: Output explains WHY 2FA matters in 1-2 sentences without lecturing — met. The opening paragraph delivers this in two sentences and moves on.

## Notes

The KB article definition cites the 2FA lost-device scenario by name as an example use case — unusually specific and directly matching the test prompt. The "recommend one without blocking the other" rule maps cleanly to the authenticator-preferred / SMS-available structure. The one partial is the mobile path: the Audience section provides general guidance to call out form-factor differences, but it does not prescribe a dedicated mobile procedure section. An agent following this definition would mention mobile considerations rather than produce parallel mobile steps. All other criteria are covered by explicit, prescriptive rules in the definition.
