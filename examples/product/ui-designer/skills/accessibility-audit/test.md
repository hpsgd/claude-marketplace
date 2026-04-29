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

## Output expectations

- [ ] PASS: Output evaluates against WCAG 2.1 AA explicitly (and notes 2.2 deltas where relevant) — referencing the specific success criteria (e.g. SC 1.4.3 Contrast (Minimum), SC 2.1.1 Keyboard) per finding, not generic "accessibility issues"
- [ ] PASS: Output's findings are organised under the four WCAG principles — Perceivable, Operable, Understandable, Robust — with at least one finding category per principle (or "no issues found" stated explicitly)
- [ ] PASS: Output runs concrete automated checks — contrast ratios via tooling (axe-core / Lighthouse output), missing alt text, missing form labels, heading hierarchy, landmark regions — with the tool and command shown
- [ ] PASS: Output runs manual checks — keyboard-only navigation through the page (Tab order, focus visibility, no keyboard traps), screen reader behaviour (likely VoiceOver on macOS, NVDA on Windows), zoom-to-200% layout integrity
- [ ] PASS: Output's findings each have a severity (Critical / Major / Minor) AND a WCAG SC reference AND a specific location (selector, page section) — not a flat list
- [ ] PASS: Output's remediation list is prioritised — Critical findings (block compliance, e.g. images without alt text, contrast failures on body copy) before Major (impair usability, e.g. focus indicators not visible enough) before Minor
- [ ] PASS: Output distinguishes compliance-blocking findings from usability improvements — only the former blocks the enterprise procurement review; the latter are recommendations
- [ ] PASS: Output addresses the procurement context — generates a "compliance status" summary suitable for sharing with the customer's procurement team (e.g. "Currently failing: 3 Critical SC. Pass after these fixes: WCAG 2.1 AA conformance achievable")
- [ ] PASS: Output's keyboard navigation testing shows the actual tab order observed and flags any out-of-sequence focus or keyboard traps with the specific selector / element
- [ ] PARTIAL: Output addresses dynamic content (any client-side updates, modal dialogs) for ARIA live regions and focus management — these are common WCAG 2.1 AA failure points
