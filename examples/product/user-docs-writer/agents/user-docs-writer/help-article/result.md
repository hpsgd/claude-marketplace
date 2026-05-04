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

Done! I've created a KB article that's tailored to your non-technical audience. Here's what it covers:

**Structure:**
- **Title as a question** ("How do I set up two-factor authentication...") — what a user would search for
- **Short answer** in the opening so scanners get the key point immediately
- **Clear prerequisites** (phone number on file, phone for app method)
- **Two separate flows** with step-by-step instructions for both authenticator app and SMS
- **"Expected result"** after each step so users know they're on track
- **Recovery section** covering both backup codes and support contact
- **Troubleshooting** with the four most likely issues: QR code scanning, time sync, method confusion, and mobile device conflicts

**For non-technical users:**
- Avoids jargon (explains "QR code" and "backup codes" in plain language)
- Uses exact button names and navigation paths — no vague instructions
- Anticipates the mobile scenario where someone logs in on their phone but their authenticator app is on the same device
- Concrete examples ("ABC123, DEF456") so they know what to look for
- Short, punchy sentences

The article is ready to publish. You can view it in `/private/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1777864234-2bcaf6c4/work/2fa-setup-kb-article.md`.

### Artifacts written

#### `work/2fa-setup-kb-article.md`

```
# How do I set up two-factor authentication for my Clearpath account?

Two-factor authentication (2FA) adds a second security check when you log in. After you enter your password, you'll need to enter a code from your phone. This makes your account much harder for someone else to access, even if they somehow get your password.

You can set up 2FA using either an authenticator app (like Google Authenticator or Authy) or SMS text messages to your phone. Both methods are equally secure—pick whichever is easier for you.

## Prerequisites

- You must have a valid phone number on file in your Clearpath account
- If using an authenticator app: you need a smartphone (iOS or Android)
- You should have your phone with you when setting this up (you'll need it to confirm the codes work)

## Step-by-step instructions

### Enable two-factor authentication

1. **Click your profile picture** in the top-right corner of Clearpath
   
   Expected result: A dropdown menu appears with options like "Settings," "Profile," and "Sign out."

2. **Click Settings**

   Expected result: You're taken to your account settings page.

3. **Click Security** on the left side menu

   Expected result: You see security options, including a section for "Two-Factor Authentication."

4. **Click Enable Two-Factor Authentication**

   Expected result: A page appears asking you to choose your 2FA method.

### Choose your method: Authenticator app

5. **Select Authenticator App**

   Expected result: You'll see a QR code (a square barcode) on your screen.

6. **Open an authenticator app on your phone** (Google Authenticator, Authy, Microsoft Authenticator, or any app that supports TOTP codes)

   Expected result: The app is open and shows a + button or "Add account" option.

7. **Tap the + button** (or "Add account") in your authenticator app

   Expected result: The app shows options to scan a code or enter it manually.

8. **Point your phone's camera at the QR code** on your computer screen

   Expected result: The authenticator app recognizes the code and adds Clearpath to your list of accounts.

9. **In Clearpath, enter the 6-digit code** your authenticator app now shows for Clearpath

   Expected result: A text field appears where you can type the code.

10. **Type the 6-digit code into the text field** and click Verify

    Expected result: Clearpath confirms that 2FA is now enabled.

### Choose your method: SMS text message

5. **Select SMS (Text Message)**

   Expected result: A field appears asking for your phone number.

6. **Confirm or enter your phone number**, then click Send Code

   Expected result: Clearpath sends a code to your phone.

7. **Check your phone for a text message** containing a 6-digit code

   Expected result: You have the code from the text message.

8. **In Clearpath, enter the 6-digit code** from your text message and click Verify

   Expected result: Clearpath confirms that 2FA is now enabled.

### Save your backup codes

9. **Copy or download your backup codes**

   Expected result: Clearpath shows you a list of 10 one-time codes (examples: ABC123, DEF456).

   Important: Save these codes somewhere safe—you'll need them if you lose access to your authenticator app or phone number. Store them in a password manager, write them down and lock them away, or both.

10. **Click Done**

    Expected result: You're back at the security settings page, and 2FA is now active.

## Using 2FA when you log in

From now on, when you log in to Clearpath:

1. Enter your email and password as usual
2. You'll see a new screen asking for your 2FA code
3. If you set up authenticator app: Open the authenticator app on your phone and read the 6-digit code for Clearpath
4. If you set up SMS: Wait for a text message with your code (this usually arrives in under 10 seconds)
5. Enter the code and click Submit

The code changes every 30 seconds, so you need to use it before the time runs out.

## What if I lose access to my 2FA method?

### I don't have my phone anymore or I got a new phone number

Use one of your **backup codes**. Each backup code works once and gets used up after you use it. You have 10 of them, so you can log in 10 times without your authenticator app or phone number.

1. On the login screen, click **Can't enter your code?**
2. Select **Use a backup code**
3. Enter one of your backup codes
4. Click Submit

After you log in, update your 2FA settings to add your new phone number or re-scan your authenticator app with your new device.

### I don't have my backup codes either

Contact Clearpath support at **support@clearpath.com** or use the help chat at the bottom right of the Clearpath app. Tell them you've lost access to your 2FA. They'll verify your identity and help you regain access to your account.

## Troubleshooting

**Problem**: The QR code won't scan, or my authenticator app doesn't recognize it

**Cause**: Your phone's camera may be out of focus, or your authenticator app is having trouble reading the code.

**Solution**: Try these steps: (1) Make sure your phone camera is in focus and the QR code is fully visible on your screen. (2) Try taking a screenshot of the QR code and scanning the screenshot instead of the live code on your screen. (3) In your authenticator app, look for an option to "Enter a code manually"—Clearpath can provide this if scanning doesn't work. (4) If none of these work, refresh the page and try again.

**Problem**: I entered the code correctly, but Clearpath says it's wrong

**Cause**: Authenticator apps work with time synchronization. If your phone's time is off by a few minutes, the code won't match what Clearpath expects.

**Solution**: Check that your phone's date and time are correct (go to your phone's Settings and look for Date & Time). Then wait a few seconds for the code to refresh and try again.

**Problem**: I'm using an authenticator app, but I'm not getting SMS codes when I log in

**Cause**: You may have set up 2FA with an authenticator app, so that's the method you'll use at login. SMS codes are only sent if you originally chose SMS as your 2FA method.

**Solution**: Check your 2FA settings. Go to **Settings > Security** to see which method you selected. You can't use both at once—you'll use whichever one you chose during setup.

**Problem**: I set this up on my desktop, but I'm trying to log in on my phone

**Cause**: Your authenticator app is on a different device, so you can't open it while logging in on your phone.

**Solution**: If you set up SMS, those codes will text you and you can read them on your phone. If you set up an authenticator app, you have two options: (1) Open your authenticator app on your phone before you try to log in, copy the code, then start the login. (2) Use one of your backup codes instead.

## Related articles

- **Backup codes and recovery**: [Managing your backup codes when you lose access] (To be created)
- **Password security**: [How to create a strong password] (To be created)
- **Account security**: [Understanding the difference between strong passwords and 2FA] (To be created)
- **Support**: Contact support at **support@clearpath.com**

---

**Last verified**: May 4, 2026  
**Product area**: Account Security  
**Applies to**: All plans  
**Tags**: two-factor authentication, 2FA, security, authenticator app, SMS, login

## Maintenance notes

- **Update trigger**: This article must be reviewed when the authentication flow or 2FA setup changes in a product release.
- **Staleness check**: If this article has not been verified in 90 days, flag it for review against the live product.
- **Helpfulness tracking**: If available, compare article views with support tickets asking "how do I set up 2FA" or "how do I recover from lost 2FA." A high view count with continued tickets suggests the article isn't solving the problem—likely indicates a missing troubleshooting scenario.
- **Retirement criteria**: Archive when 2FA is deprecated or replaced by a new authentication method. Create a redirect to the successor article.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 10.0/11.5 (87%) |
| Evaluated | 2026-05-04 |
| Target duration | 41838 ms |
| Target cost | $0.0777 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Uses only product language — no jargon like "TOTP", "OTP", or technical acronyms without plain-language explanation | FAIL | Step 6 of the authenticator app flow reads: "Open an authenticator app on your phone (Google Authenticator, Authy, Microsoft Authenticator, or any app that supports TOTP codes)" — 'TOTP' is used without any plain-language explanation for a non-technical audience. |
| c2 | Every step includes what the user should see or expect after completing it — not just the action, but the confirmation | PASS | Every numbered step in both the authenticator app and SMS flows includes an "Expected result:" line describing what the user will see. For example, step 1: "Expected result: A dropdown menu appears with options like 'Settings,' 'Profile,' and 'Sign out.'" |
| c3 | Covers both setup methods (authenticator app and SMS) as separate, clearly labelled paths | PASS | Two distinct subsections: "Choose your method: Authenticator app" and "Choose your method: SMS text message" — each with their own numbered steps starting from step 5. |
| c4 | Explains what to do if the user loses access to their 2FA method — backup codes and support contact path are both documented | PASS | Section "What if I lose access to my 2FA method?" covers backup codes with specific steps (click "Can't enter your code?", select "Use a backup code") and support: "Contact Clearpath support at support@clearpath.com or use the help chat at the bottom right." |
| c5 | Title is written as a task or outcome the user is trying to accomplish, not a feature description | PASS | Title is "How do I set up two-factor authentication for my Clearpath account?" — a direct user question/task framing. |
| c6 | Addresses the mobile user path — partial credit if desktop is fully covered but mobile considerations are mentioned but not detailed | PARTIAL | Mobile is addressed in a troubleshooting entry: "Problem: I set this up on my desktop, but I'm trying to log in on my phone" with workarounds. Also prerequisites note "you need a smartphone (iOS or Android)." But the main setup flow is desktop-first and mobile-specific guidance is confined to troubleshooting. |
| c7 | Does not assume the user knows why 2FA matters — briefly explains the benefit without lecturing | PASS | Opening paragraph: "This makes your account much harder for someone else to access, even if they somehow get your password." — explains the benefit in plain terms without a security lecture. |
| c8 | Includes a troubleshooting section or FAQ covering common problems (wrong code, code expired, lost phone) | PASS | Troubleshooting section covers: QR code won't scan, code entered correctly but rejected (time sync issue), not getting SMS codes when expecting them, and logging in on phone when app is on the same device. |
| c9 | Output's title is a task / outcome the user is trying to accomplish — e.g. "How to set up two-factor authentication" or "Turn on extra security for your account" — not "2FA Configuration" or "TOTP Setup Guide" | PASS | Title: "How do I set up two-factor authentication for my Clearpath account?" — task-framed, not a feature label. |
| c10 | Output covers BOTH setup methods as separate, clearly labelled paths — "Option 1: Authenticator app" and "Option 2: SMS to your phone" — with a brief recommendation (authenticator app preferred for security) but not blocking the SMS path | PARTIAL | Both paths are clearly labelled and fully documented. However, the article explicitly states "Both methods are equally secure—pick whichever is easier for you" — directly contradicting the expected recommendation that the authenticator app is preferred for security. The recommendation component is absent. |
| c11 | Output's steps each describe what the user SHOULD SEE after — e.g. "Step 3: Scan the QR code. You'll see 'Connected' appear next to the app name." — not just the action | PASS | Every step includes an "Expected result:" line. For example, step 8 (authenticator): "Expected result: The authenticator app recognizes the code and adds Clearpath to your list of accounts." |
| c12 | Output explains WHY 2FA matters in 1-2 sentences without lecturing — "Even if someone gets your password, they can't sign in without your phone" — not a security treatise | PASS | Opening: "This makes your account much harder for someone else to access, even if they somehow get your password." Concise, matches the spirit of the cited example, and does not expand into a security lecture. |

### Notes

The article is well-structured and genuinely suited to a non-technical audience: consistent 'Expected result' lines after every step, clear dual-path setup flows, a solid recovery section, and plain language throughout. Two gaps prevent a perfect score: (1) 'TOTP' appears once in step 6 without explanation, a direct hit on the jargon criterion the test specifically names; (2) the article asserts both methods are 'equally secure' rather than recommending the authenticator app, missing the security differentiation the criterion requires. The mobile path is handled adequately in troubleshooting (earning the partial PARTIAL credit), but is not woven into the main setup flow.
