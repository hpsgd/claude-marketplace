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
