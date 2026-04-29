# Test: Help article

Scenario: A user-facing help article is needed explaining how to set up two-factor authentication for end users of a SaaS product.

## Prompt


Write a help article for setting up two-factor authentication in Clearpath. Users can set up 2FA using:
1. Authenticator app (Google Authenticator, Authy, or any TOTP app)
2. SMS to their phone number

After enabling 2FA, they'll need to enter a code every time they log in. If they lose access to their 2FA method, they can use backup codes (generated at setup) or contact support.

Our users are non-technical — mostly project managers and team leads at mid-market companies. Some are on mobile, most are on desktop.

## Criteria


- [ ] PASS: Uses only product language — no jargon like "TOTP", "OTP", or technical acronyms without plain-language explanation
- [ ] PASS: Every step includes what the user should see or expect after completing it — not just the action, but the confirmation
- [ ] PASS: Covers both setup methods (authenticator app and SMS) as separate, clearly labelled paths
- [ ] PASS: Explains what to do if the user loses access to their 2FA method — backup codes and support contact path are both documented
- [ ] PASS: Title is written as a task or outcome the user is trying to accomplish, not a feature description
- [ ] PARTIAL: Addresses the mobile user path — partial credit if desktop is fully covered but mobile considerations are mentioned but not detailed
- [ ] PASS: Does not assume the user knows why 2FA matters — briefly explains the benefit without lecturing
- [ ] PASS: Includes a troubleshooting section or FAQ covering common problems (wrong code, code expired, lost phone)

## Output expectations

- [ ] PASS: Output's title is a task / outcome the user is trying to accomplish — e.g. "How to set up two-factor authentication" or "Turn on extra security for your account" — not "2FA Configuration" or "TOTP Setup Guide"
- [ ] PASS: Output covers BOTH setup methods as separate, clearly labelled paths — "Option 1: Authenticator app" and "Option 2: SMS to your phone" — with a brief recommendation (authenticator app preferred for security) but not blocking the SMS path
- [ ] PASS: Output's authenticator app section names example apps from the prompt — Google Authenticator, Authy, "or any TOTP app" — and uses "TOTP" only after defining it ("an app that generates a 6-digit code that changes every 30 seconds")
- [ ] PASS: Output's SMS section addresses the inherent risks (SIM swap, phone unavailable in roaming) without scaremongering — and recommends authenticator app for users with sensitive data
- [ ] PASS: Output's steps each describe what the user SHOULD SEE after — e.g. "Step 3: Scan the QR code. You'll see 'Connected' appear next to the app name." — not just the action
- [ ] PASS: Output addresses backup codes explicitly — generated at setup, recommended to be saved (printed or in password manager), and used as a one-time fallback when 2FA method is unavailable
- [ ] PASS: Output's recovery section is comprehensive — using a backup code, contacting support if backup codes are also lost, with an honest acknowledgment that account recovery may take time and require identity verification
- [ ] PASS: Output explains WHY 2FA matters in 1-2 sentences without lecturing — "Even if someone gets your password, they can't sign in without your phone" — not a security treatise
- [ ] PASS: Output's troubleshooting / FAQ covers — wrong code (timing / clock drift on phone), code expired (re-trigger or use a fresh one), lost phone (use backup codes, then contact support), SMS not arriving (carrier delay, alternative), restored phone (re-enrol the authenticator)
- [ ] PARTIAL: Output addresses the mobile user path — for users on mobile setting up 2FA (e.g. authenticator app on the same device requires a workaround like manual code entry vs QR scan)
