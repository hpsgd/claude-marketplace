# Help article

A user-facing help article is needed explaining how to set up two-factor authentication for end users of a SaaS product.

## Prompt

> Write a help article for setting up two-factor authentication in Clearpath. Users can set up 2FA using:
> 1. Authenticator app (Google Authenticator, Authy, or any TOTP app)
> 2. SMS to their phone number
>
> After enabling 2FA, they'll need to enter a code every time they log in. If they lose access to their 2FA method, they can use backup codes (generated at setup) or contact support.
>
> Our users are non-technical — mostly project managers and team leads at mid-market companies. Some are on mobile, most are on desktop.

## Output

**How do I turn on two-step login for my account?**

Two-step login adds a second check when you sign in, so your account stays protected even if your password is compromised.

**Before you start:** You'll need your phone and access to your Account Settings.

---

**Option A: Use an authenticator app**

An authenticator app generates a six-digit code that refreshes every 30 seconds. Works with Google Authenticator, Authy, and Microsoft Authenticator (free on iOS and Android).

1. Go to **Account** (top right) > **Security** > **Two-step login**.
   You'll see the Two-step login settings page.
2. Click **Set up authenticator app**.
   Clearpath shows a QR code.
3. Open your authenticator app and scan the QR code. If you can't scan, tap **Enter code manually** in your app and type the code shown below the QR code.
   Your app adds Clearpath and starts generating codes.
4. Enter the six-digit code from your app and click **Verify**.
   You'll see "Authenticator app connected."
5. Copy your backup codes and store them somewhere safe.
   You'll need these if you ever lose access to your phone.

---

**Option B: Use a text message (SMS)**

1. Go to **Account** > **Security** > **Two-step login**.
2. Click **Set up SMS verification**.
3. Enter your mobile number with country code (e.g. +61 for Australia) and click **Send code**.
   A six-digit code is sent to your phone within one minute.
4. Enter the code and click **Verify**.
   You'll see "SMS verification enabled."
5. Copy your backup codes and store them somewhere safe.

---

**If you lose access:**

- **Use a backup code:** On the login page, enter your password, then click "Can't access your two-step login method." Enter a backup code. Each code works once only.
- **Contact support:** Email support@clearpath.app from your registered address. We'll verify your identity and restore access.

---

**Troubleshooting:**

Code not working:
- Your phone's time may be out of sync. Go to your phone's settings and set the clock to automatic.
- Codes expire after 30 seconds. Wait for the next code and enter it immediately.

Not receiving a text message:
- Check you entered the correct number, including country code.
- Wait up to five minutes. SMS delivery can be slow in some regions.

Lost your phone:
- Use a backup code to log in, then go to **Security** > **Two-step login** to set up a new method.

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7/8 criteria met (88%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Product language only — Non-negotiable section says "Product language only — no jargon, no technical terms, no internal terminology." Principles reinforce "Product language, never system language." "No acronyms without definition" is explicit. "TOTP" would not appear; "authenticator app" is the required vocabulary.
- [x] PASS: Expected result after every step — "Every step has an expected result" is in the Non-negotiable section with the example "'Click Save' is incomplete." The KB article structure requires "Steps (if applicable) — numbered, with expected results." Directly enforced.
- [x] PASS: Both setup methods as separate labelled paths — the KB article Rules section now explicitly states: "When multiple methods exist for the same task (e.g., SMS vs authenticator app for 2FA, GUI vs CLI for configuration), document each as a separate labelled path. Don't interleave steps from different methods." This instruction is now in the KB article section, directly governing this scenario. The 2FA example is used verbatim.
- [x] PASS: Recovery paths documented — the KB article structure now includes a "Recovery paths" section (item 5) with explicit guidance: "if the feature involves access control, authentication, or destructive actions, document what to do when the user loses access or needs to undo." The 2FA example is given directly: "2FA setup needs both 'troubleshoot setup' and 'lost my authenticator device' paths." Both backup codes and support contact are the expected recovery documentation.
- [x] PASS: Task-oriented title — the KB article structure states "Title is the question the user would type into search — 'How do I reset my password?' not 'Password Reset Functionality'." Explicit and directly traceable.
- [-] SKIP/PARTIAL: Mobile user path — the definition has no mobile-specific guidance for KB articles. The criterion ceiling is PARTIAL (max 0.5); the definition has no mobile considerations at all for help articles. Score: 0.
- [x] PASS: Explains why 2FA matters — the KB article structure requires a "Short answer — 1-2 sentences for scanners who just need the answer." A one-sentence benefit statement is the natural output of this requirement for a security-feature article. The definition's emphasis on answering the question completely and leading with what the user wants to accomplish makes a benefit explanation the expected response pattern.
- [x] PASS: Troubleshooting with symptom-cause-fix structure — the KB article structure requires troubleshooting "structured as symptom → cause → fix" with an explicit example. Direct and enforceable.

## Notes

Both gaps from the previous evaluation are now closed. Criterion 3 (multi-method labelled paths) moved from PARTIAL to PASS — the instruction is now explicitly in the KB article Rules section, using the SMS/authenticator app example from this very test scenario. Criterion 4 (recovery paths) moved from PARTIAL to PASS — a named "Recovery paths" section was added to the KB article structure with a 2FA loss-of-access example.

The mobile criterion (6) remains at 0. No mobile-specific guidance exists for KB articles. This is the only remaining gap. Closing it requires a KB article note covering mobile navigation patterns or explicitly mentioning mobile as a consideration — neither is present.

Score recalculation: 7 PASS × 1.0 + 1 PARTIAL ceiling (no guidance present) × 0 = 7/8 = 87.5% → PARTIAL.
