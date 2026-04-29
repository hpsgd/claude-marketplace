# Test: Write user story

Scenario: Testing whether the write-user-story skill definition produces stories in Gherkin format with proper acceptance criteria and ISC splitting guidance.

## Prompt


/product-owner:write-user-story for allowing users to export their data as a CSV file from the reporting dashboard.

## Criteria


- [ ] PASS: Skill requires Gherkin format (Given/When/Then) for acceptance criteria — not free-form bullet points
- [ ] PASS: Skill requires at least one edge case or error scenario in the acceptance criteria, not just the happy path
- [ ] PASS: Skill includes the ISC splitting test — Independent, Small, Complete — to verify stories are appropriately sized
- [ ] PASS: Skill requires the standard "As a [role], I want [action], so that [outcome]" story format
- [ ] PASS: Skill prohibits solution-specifying stories — acceptance criteria must describe behaviour, not implementation
- [ ] PARTIAL: Skill addresses anti-requirements (things the story explicitly should NOT do) — partial credit if mentioned but not required as a mandatory section
- [ ] PASS: Skill specifies that stories must have a single, clear acceptance condition — not "and/or" compound criteria
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output's user story uses the standard format — "As a [role e.g. report viewer], I want [to export the current dashboard view as a CSV file], so that [I can analyse the data offline / share with stakeholders who don't have access]" — with the role concrete, not "user"
- [ ] PASS: Output's acceptance criteria are in Gherkin format (Given / When / Then) — at least 3 scenarios — not bullet points
- [ ] PASS: Output's happy-path scenario covers the main flow — "Given I'm viewing a dashboard with data, When I click Export → CSV, Then a file downloads with the visible data, named appropriately, in valid CSV format"
- [ ] PASS: Output includes at least one edge case — empty dashboard (export creates a CSV with headers only and an info message), very large dataset (export shows progress indicator and either streams or queues a job), unicode characters in values (escaped correctly)
- [ ] PASS: Output includes at least one error scenario — export endpoint fails (user sees a clear error message and can retry), permissions error (user without dashboard access cannot export), network drop mid-download
- [ ] PASS: Output's acceptance criteria are observable / verifiable — "Then a CSV file is downloaded" is testable; "Then the system handles it correctly" is not, and is rejected
- [ ] PASS: Output passes the ISC test — Independent (this story doesn't depend on a parallel story in flight), Small (deliverable in a single sprint), Complete (covers happy path, edges, and errors)
- [ ] PASS: Output's acceptance criteria describe behaviour, not implementation — "Then the file contains all rows visible in the dashboard" is good; "Then the API endpoint returns a 200 with text/csv content type" is too implementation-specific for a user story
- [ ] PASS: Output addresses what the CSV contains — exactly the data visible in the dashboard at export time, with column headers matching the displayed columns; respects active filters and sorts at export time
- [ ] PARTIAL: Output's anti-requirements section names what the story does NOT include — e.g. "does NOT support Excel format", "does NOT support scheduled exports", "does NOT include pivoted/aggregated data unless visible in the dashboard"
