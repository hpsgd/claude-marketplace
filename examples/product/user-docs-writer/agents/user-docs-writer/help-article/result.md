# Output: Help article

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 11.5/12 criteria met (96%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Uses only product language — met. The Non-negotiable section states "Product language only — no jargon, no technical terms, no internal terminology." Voice and Language adds "No acronyms without definition." The definition would prohibit bare "TOTP" or "OTP."
- [x] PASS: Every step includes what the user should see after completing it — met. The Non-negotiable section states "Every step has an expected result so the reader knows they're on track." The Principles section gives a direct example showing the difference between "Click Save" (incomplete) and "Click Save. You should see a green confirmation banner…" (correct).
- [x] PASS: Covers both setup methods as separate, clearly labelled paths — met. KB article Rules state: "When multiple methods exist for the same task (e.g., SMS vs authenticator app for 2FA, GUI vs CLI for configuration), document each as a separate labelled path. Don't interleave steps from different methods."
- [x] PASS: Explains what to do if the user loses access — met. KB article structure explicitly includes "Recovery paths (when applicable)" and names the exact scenario: "2FA setup needs both 'troubleshoot setup' and 'lost my authenticator device' paths." Both backup codes and support contact are implied by "lost my authenticator device" path.
- [x] PASS: Title is written as a task or outcome — met. KB article Rules require "Title is the question the user would type into search — 'How do I reset my password?' not 'Password Reset Functionality'."
- [~] PARTIAL: Addresses the mobile user path — partially met. The Audience section instructs the agent to "call out where steps differ between form factors (e.g., a step that assumes a second device, gestures specific to small screens)." This would produce mentions of mobile considerations, but the definition does not prescribe a dedicated mobile path with its own steps.
- [x] PASS: Does not assume the user knows why 2FA matters — met. The audience framing requires assuming nothing about skill level, and the KB article structure requires a "Short answer — 1-2 sentences for scanners." These combine to produce a brief benefit statement rather than a lecture.
- [x] PASS: Includes a troubleshooting section covering common problems — met. KB article structure requires troubleshooting "structured as symptom → cause → fix." The definition mandates this for every KB article.

### Output expectations

- [x] PASS: Output title is a task / outcome — met. KB Rules explicitly require this and give "How do I reset my password?" as the model form. An agent following this definition would produce a task-oriented title, not "2FA Configuration" or "TOTP Setup Guide."
- [x] PASS: Output covers both setup methods as separate labelled paths with a brief recommendation — met. The definition requires separate labelled paths and "recommend one without blocking the other — let the user choose with context." This directly maps to preferring the authenticator app while keeping the SMS path available.
- [x] PASS: Output steps each describe what the user should see after — met. This is a non-negotiable principle stated twice in the definition with an explicit worked example.
- [x] PASS: Output explains WHY 2FA matters in 1-2 sentences without lecturing — met. KB article short-answer-first structure combined with non-technical audience framing produces the expected brief benefit statement. The definition instructs: "Short answer — 1-2 sentences for scanners who just need the answer."

## Notes

The agent definition handles this test case well. The KB article rules cite the 2FA lost-device scenario verbatim as an example use case, which is unusually specific and directly matches the test. The "recommend one without blocking the other" rule maps cleanly to the authenticator-preferred-but-SMS-available output expectation. The one partial is the mobile path: the instruction exists in the Audience section but is general guidance rather than a procedural rule, so an agent might mention mobile considerations without producing a fully detailed separate mobile path. All other criteria are covered by explicit, prescriptive rules in the definition.
