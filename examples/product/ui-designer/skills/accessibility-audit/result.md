# Output: Accessibility audit

**Verdict:** PARTIAL
**Score:** 12/14 criteria met (86%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill evaluates against WCAG 2.1 AA (and ideally 2.2) — met. Frontmatter and body target WCAG 2.2 AA explicitly, noting it supersedes 2.1. Exceeds the minimum standard.
- [x] PASS: Skill distinguishes automated from manual checks — met. Step 1 is grep-based automated pattern detection mapped to specific WCAG criteria; Step 2 is an explicit manual checklist. Both are required, clearly separated.
- [x] PASS: Skill classifies findings by severity with WCAG criterion referenced — met. Step 3 defines Critical / Major / Minor / Best Practice. Step 4 and the output template require a WCAG criterion number per finding.
- [x] PASS: Skill covers all four WCAG principles — met. Step 2 manual checklist is organised under Perceivable, Operable, Understandable, Robust with specific success criteria mapped to each row.
- [x] PASS: Skill produces a prioritised remediation list — met. The output format orders sections Critical → Major → Minor → Best Practice. The severity matrix includes response timelines (block deployment, fix this sprint, fix next cycle, backlog).
- [x] PASS: Skill includes keyboard navigation as a specific required check with a defined test pattern — met. Step 1 has grep patterns for onClick without onKeyDown, div/span with onClick, outline suppression, and modal focus traps. Step 2 has O1 (tab through entire interface, activate every control), O2 (verify escape from every component), O5 (focus order), O9 (focus indicator visible). Specific patterns are defined, not a vague mention. This criterion is fully met; PARTIAL is not warranted.
- [x] PASS: Skill distinguishes must-fix from should-fix — met. Critical is defined as "Users with disabilities cannot complete core tasks. Legal risk." with "Block deployment." Best Practice is explicitly "Not a WCAG violation but improves the experience" with "Add to backlog." The boundary is clear.
- [x] PASS: Valid YAML frontmatter with name, description, argument-hint — met. All three fields present and well-formed.

### Output expectations

- [x] PASS: Output references specific WCAG success criteria per finding — met. The output template requires `**WCAG:** [criterion number] — [criterion name]` for every issue.
- [~] PARTIAL: Output findings organised under the four WCAG principles — partially met. Step 2 (the manual checklist) is structured by POUR principle, but the output format sections are ordered by severity (Critical / Major / Minor / Best Practice), not by principle. There is no requirement in the output format to group findings by POUR, and no "no issues found" placeholder per principle. A reader would need to cross-reference Steps 2 and 4 to reconstruct the POUR view.
- [x] PASS: Output findings each have severity, WCAG SC reference, and specific location — met. The output template mandates Location (`file:line`), WCAG criterion number, and Impact for each finding. The severity heading groups provide the severity level.
- [x] PASS: Output remediation list is prioritised Critical before Major before Minor — met. Output format sections enforce this order explicitly.
- [x] PASS: Output distinguishes compliance-blocking from usability improvements — met. The Best Practice Recommendations section is separate from Critical/Major/Minor and the severity matrix defines it as "not a WCAG violation."
- [~] PARTIAL: Output addresses dynamic content for ARIA live regions and focus management — partially met. Step 1 automated checks include patterns for missing aria-live on toast/notification/alert elements (WCAG 4.1.3) and modals without focus traps. Step 2 R3 covers status messages. However, the output format template has no dedicated section for dynamic/ARIA concerns — findings would appear in Critical/Major sections only if detected. There is no explicit prompt to surface ARIA live region findings for dynamic content as a distinct output category.

## Notes

The skill is thorough and well-structured for its intended purpose: static code analysis of a React/Next.js codebase. Against a codebase test it would meet all criteria.

There is a scope gap with the test prompt, which invokes the skill against a live URL (`https://hps.gd`). The skill explicitly scopes itself to code analysis ("This audit uses code analysis to find violations") and its allowed-tools are Read, Bash, Glob, Grep — no browser or HTTP tools. It cannot evaluate rendered contrast ratios, trace live tab order, or test screen reader behaviour against a URL. This is worth noting but does not affect the structural criteria score, which evaluates the skill definition on its own terms.

If the intent is to support live-URL audits, a separate skill using axe-core CLI or Playwright would be needed. The current skill's quality for code auditing is high.
