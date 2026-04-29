# Test: Write integration guide

Scenario: Testing whether the write-integration-guide skill requires numbered steps with expected output, a complete runnable example, and a troubleshooting section.

## Prompt


/developer-docs-writer:write-integration-guide for connecting Clearpath to Salesforce — syncing deal status from Salesforce opportunities to Clearpath projects automatically.

## Criteria


- [ ] PASS: Skill requires numbered steps — not bullet points — so developers can follow sequentially and know exactly where they are
- [ ] PASS: Each step includes the expected output or visible result after completion, not just the action
- [ ] PASS: Skill requires a complete runnable end-to-end example that exercises the full integration
- [ ] PASS: Skill requires a troubleshooting section covering common failure modes with specific fixes
- [ ] PASS: Skill requires a prerequisites section before the integration steps begin
- [ ] PASS: Skill requires a research step — understanding both systems before writing the guide
- [ ] PARTIAL: Skill covers how to verify the integration is working correctly — partial credit if verification is embedded in steps but not a dedicated section
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output's prerequisites section names what the developer needs before starting — Salesforce admin access (with required permissions like API enabled, Connected App permission), Clearpath admin role, OAuth credentials (Salesforce Connected App client_id/client_secret) — explicit, not assumed
- [ ] PASS: Output's steps are numbered (1, 2, 3...) — not bullet points — so the developer can follow sequentially and report which step failed
- [ ] PASS: Output's steps each include expected output / visible result — e.g. "Step 4 expected: you should see 'Connection verified ✓' in the Clearpath integrations panel" — not just the action to perform
- [ ] PASS: Output's mapping step covers the field-level mapping — Salesforce Opportunity stage → Clearpath project status — with a worked example for at least 3 stages (Prospecting → Backlog, Closed Won → Active, Closed Lost → Archived)
- [ ] PASS: Output's complete runnable example covers an end-to-end deal-status sync — creating or updating a Salesforce opportunity, observing the Clearpath project status update — with the full flow demonstrable in a sandbox
- [ ] PASS: Output's troubleshooting section covers at least 4 common failure modes — auth token expired, field mapping mismatch, rate-limit hit, webhook delivery failure — each with the symptom, the cause, and a specific fix
- [ ] PASS: Output addresses sync direction explicitly — is this a one-way sync (Salesforce → Clearpath only) or bidirectional? Conflict resolution if changes happen on both sides
- [ ] PASS: Output's verification section (or embedded verification per step) explains how the developer confirms the integration is working — specific test data, expected behaviour, what to check
- [ ] PASS: Output addresses the initial historical sync vs ongoing sync — does the integration backfill existing opportunities, or only sync from this point forward
- [ ] PARTIAL: Output addresses how to disable / pause the integration safely — necessary for incident response or migration scenarios
