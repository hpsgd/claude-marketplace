# Test: Accessibility audit

Scenario: Testing whether the accessibility-audit skill definition requires WCAG 2.1/2.2 AA evaluation, automated and manual checks, and severity classification for findings.

## Prompt


/ui-designer:accessibility-audit of https://hps.gd — navigation, page structure, and any interactive elements. We're preparing for an enterprise procurement review that requires WCAG 2.1 AA compliance.

## Criteria


- [ ] PASS: Skill evaluates against WCAG 2.1 AA (and ideally 2.2) as the compliance standard — not a vague "accessibility best practices" framing
- [ ] PASS: Skill distinguishes between automated checks (contrast ratios, missing alt text, label associations) and manual checks (keyboard navigation flow, screen reader behaviour) — both are required
- [ ] PASS: Skill classifies findings by severity (e.g. Critical/Major/Minor) with WCAG success criterion referenced for each finding
- [ ] PASS: Skill covers the four WCAG principles: Perceivable, Operable, Understandable, Robust
- [ ] PASS: Skill produces a prioritised remediation list — not just a findings catalogue
- [ ] PARTIAL: Skill includes keyboard navigation testing as a specific required check — partial credit if keyboard access is mentioned but no specific test pattern is defined
- [ ] PASS: Skill distinguishes between what blocks compliance (must fix) and what improves usability (should fix)
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
