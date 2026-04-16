# Test: Design tokens

Scenario: Testing whether the design-tokens skill definition requires primitive tokens, semantic tokens, contrast validation, and proper documentation structure.

## Prompt


/ui-designer:design-tokens for our product — we currently have hardcoded hex values and pixel values scattered across our Figma files and CSS, with no token system.

## Criteria


- [ ] PASS: Skill distinguishes between primitive tokens (raw values: color-blue-500) and semantic tokens (purpose-named: color-action-primary) as separate layers
- [ ] PASS: Skill requires an inventory step — cataloguing existing values before defining tokens
- [ ] PASS: Skill requires contrast ratio validation for colour tokens against WCAG AA thresholds (4.5:1 for normal text, 3:1 for large text)
- [ ] PASS: Skill requires token documentation that specifies the intended use case, not just the value
- [ ] PASS: Skill covers at minimum colour, typography, and spacing token categories
- [ ] PARTIAL: Skill specifies a naming convention for tokens — partial credit if naming is mentioned as important but no specific convention is required
- [ ] PASS: Skill produces output that is usable by both designers (Figma) and developers (CSS custom properties or equivalent) — not just one audience
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
