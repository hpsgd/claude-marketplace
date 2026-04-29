# Output: Help article

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 13.0/16.5 criteria met (79%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Uses only product language — the Non-negotiable section states "Product language only — no jargon, no technical terms, no internal terminology." Voice and Language adds "No acronyms without definition. First use: 'Single Sign-On (SSO)'." The definition would prohibit bare "TOTP" or "OTP." Met.
- [x] PASS: Every step includes what the user should see after completing it — the Non-negotiable section states "Every step has an expected result so the reader knows they're on track." The Principles section gives a direct example: "'Click Save' is incomplete. 'Click Save. You should see a green confirmation banner…' tells the user they are on track." Met.
- [x] PASS: Both setup methods as separate, clearly labelled paths — the KB article Rules state: "When multiple methods exist for the same task (e.g., SMS vs authenticator app for 2FA, GUI vs CLI for configuration), document each as a separate labelled path. Don't interleave steps from different methods." Met.
- [x] PASS: Explains what to do if the user loses access — the KB article structure includes a "Recovery paths" section with explicit guidance: "if the feature involves access control, authentication, or destructive actions, document what to do when the user loses access or needs to undo." The definition names the exact scenario: "2FA setup needs both 'troubleshoot setup' and 'lost my authenticator device' paths." Met.
- [x] PASS: Title written as a task or outcome — KB article Rules state: "Title is the question the user would type into search — 'How do I reset my password?' not 'Password Reset Functionality'." Met.
- [~] PARTIAL: Addresses the mobile user path — the definition has no mobile-specific guidance. Desktop is covered by the general steps structure, but no mobile considerations appear anywhere in the definition. Partially met: 0.5.
- [x] PASS: Does not assume the user knows why 2FA matters — KB article structure requires a "Short answer — 1-2 sentences for scanners." Combined with the agent's non-technical audience framing ("assume nothing about their skill level"), a brief benefit statement is the expected output pattern. Met.
- [x] PASS: Troubleshooting section covering common problems — KB article structure requires troubleshooting "structured as symptom → cause → fix." The definition mandates this for every KB article. Met.

**Criteria subtotal: 7.0 + 0.5 = 7.5 / 8.0**

### Output expectations

- [x] PASS: Output title is a task or outcome — KB Rules explicitly require this and give "How do I reset my password?" as the model form. An agent following this definition would produce a task-oriented title. Met.
- [~] PARTIAL: Output covers both methods with brief recommendation (authenticator preferred, SMS not blocked) — the definition requires separate labelled paths but does not include any guidance on recommending one method over another. The paths would be present; the recommendation framing is not governed. Partially met: 0.5.
- [ ] FAIL: Output's authenticator section names example apps from the prompt and defines "TOTP" before using it — the "no acronyms without definition" rule would produce a definition before use. However, the definition does not instruct the agent to include specific app examples from the brief. Whether Google Authenticator and Authy appear depends on the agent reading the prompt, not on standing instructions. Not met.
- [ ] FAIL: Output's SMS section addresses inherent risks (SIM swap, roaming phone unavailable) — the definition has no guidance on surfacing method-level security risks within setup paths. An agent following this definition would document the setup steps but would not be directed to include SIM-swap warnings. Not met.
- [x] PASS: Output's steps each describe what the user should see after — governed by "Every step has an expected result" as a non-negotiable. Met.
- [~] PARTIAL: Output addresses backup codes explicitly with save recommendation — the definition covers recovery paths generically but does not mention backup codes, the recommendation to save them (print or password manager), or their one-time-use nature. The recovery section would exist; these specifics are not governed. Partially met: 0.5.
- [ ] FAIL: Output's recovery section includes honest acknowledgment that account recovery may take time and require identity verification — the definition documents the existence of a recovery path but gives no guidance on tone or setting user expectations about support turnaround. Not met.
- [x] PASS: Output explains WHY 2FA matters in 1-2 sentences — KB article structure requires a "Short answer" first, and audience framing requires assuming nothing about the user's prior knowledge. The agent would produce a brief benefit statement. Met.
- [~] PARTIAL: Output's troubleshooting covers specific items (clock drift, re-enrolment after phone restore, SMS not arriving, carrier delay) — the definition requires a troubleshooting section with symptom → cause → fix structure, which covers the form. The specific items enumerated in the criterion are not listed in the definition. Some common items would appear; full coverage of this list is not guaranteed. Partially met: 0.5.
- [ ] FAIL: Output addresses mobile user path — no mobile-specific guidance exists in the definition for any document type. Not met.

**Output expectations subtotal: 4.0 + 1.5 = 5.5 / 8.5**

## Notes

The agent definition handles structural and voice requirements well — the 2FA example is cited verbatim in the KB article rules, and the recovery paths section shows clear awareness of authentication-specific documentation needs. Where it falls short is output depth: the Output expectations criteria probe specifics (SIM-swap risks, backup code save instructions, recovery time acknowledgment, named app examples, mobile workaround) that require prescriptive guidance the definition does not provide. The definition tells the agent to write recovery paths and troubleshooting sections but not what those sections must contain for a 2FA scenario. A stronger definition would include a worked example or a content checklist for authentication-related articles.

**Score:** Criteria 7.5/8.0 + Output expectations 5.5/8.5 = 13.0/16.5 = 79% → PARTIAL.
