# Output: Accessibility audit

**Verdict:** FAIL
**Score:** 12.5/18 criteria met (69%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill evaluates against WCAG 2.1 AA (and ideally 2.2) — met. Frontmatter and line 9 explicitly target WCAG 2.2 AA, noting it supersedes 2.1. Exceeds the minimum standard.
- [x] PASS: Skill distinguishes automated from manual checks — met. Step 1 is grep-based automated pattern detection mapped to specific WCAG criteria. Step 2 is an explicit manual checklist. Both are required sections, clearly separated.
- [x] PASS: Skill classifies findings by severity with WCAG criterion referenced — met. Step 3 defines a four-level matrix (Critical / Major / Minor / Best Practice). Step 4 requires every finding to identify the specific WCAG criterion number and name.
- [x] PASS: Skill covers all four WCAG principles — met. Step 2 manual checklist is organised under Perceivable, Operable, Understandable, Robust headings with specific success criteria mapped to each item.
- [x] PASS: Skill produces a prioritised remediation list — met. Step 4 requires file/line reference, before/after code, and verification steps per finding. The severity matrix includes response timelines (block deployment, fix this sprint, fix next cycle, backlog), making priority explicit.
- [~] PARTIAL: Skill includes keyboard navigation as a specific required check — partially met (0.5). Step 1 includes grep patterns for onClick without onKeyDown (WCAG 2.1.1) and div/span with onClick. Step 2 has O1 (tab entire interface, activate every control), O2 (no keyboard traps), O5 (focus order), and O9 (focus indicator visible). These are specific test patterns, not a vague mention. Score capped at 0.5 per criterion type, though in substance this is fully met.
- [x] PASS: Skill distinguishes must-fix from should-fix — met. Severity matrix explicitly marks Critical as "Users with disabilities cannot complete core tasks. Legal risk." with "Block deployment" response, separating it from Best Practice ("Not a WCAG violation but improves the experience") with "Add to backlog" response.
- [x] PASS: Valid YAML frontmatter with name, description, argument-hint — met. All three fields present and well-formed.

### Output expectations

- [ ] FAIL: Skill targets WCAG 2.2 AA but is code-analysis-only (grep against source files). The prompt invokes it against a live URL (`https://hps.gd`). The skill cannot run axe-core or Lighthouse against a live URL, produce tool output with commands shown, or evaluate rendered contrast ratios — it explicitly states "This audit uses code analysis to find violations. It is not a substitute for manual testing."
- [ ] FAIL: Findings cannot be organised under four WCAG principles for a live URL because the skill only analyses source files, not a rendered page. The structural categories exist in the skill but cannot be populated from a URL scan.
- [ ] FAIL: Skill has no mechanism for running axe-core or Lighthouse against a live URL. All automated checks are grep patterns against `.tsx`/`.jsx`/`.html` source files. No CLI tool or command for live URL scanning is present.
- [ ] FAIL: Manual checks for keyboard-only navigation, screen reader behaviour, and zoom-to-200% cannot be performed by this skill as invoked — the skill is code-analysis-only and does not adapt its instructions to a live URL scenario.
- [x] PASS: Output template requires severity + WCAG SC reference + location (file:line) per finding. The format satisfies the structured-finding criterion.
- [x] PASS: Remediation list is prioritised Critical → Major → Minor → Best Practice, with distinct sections and response timelines in the output format.
- [x] PASS: Skill distinguishes compliance-blocking (Critical/Major) from usability improvements (Best Practice is explicitly called out as not a WCAG violation).
- [ ] FAIL: Skill has no mechanism for producing a procurement-ready compliance status summary. No output section exists for "currently failing N Critical SC; WCAG 2.1 AA conformance achievable after these fixes" language directed at a procurement team.
- [ ] FAIL: Skill cannot show actual tab order observed against a live URL. It can detect missing keyboard handlers in source code, but cannot trace rendered tab order or flag runtime keyboard traps.
- [~] PARTIAL: Skill includes automated detection for modals without focus traps and missing `aria-live` regions (Steps 1 and 2, WCAG 4.1.3). The pattern is present but applies to source code only, not rendered dynamic content on a live URL. Partial credit for addressing the requirement in the code-audit context.

## Notes

The skill is thorough and well-structured for its intended use case: auditing a React/Next.js codebase via static analysis. Against a codebase test it would score near 100% across all criteria.

The gap is a scope mismatch. The test prompt invokes the skill against a live URL. The skill explicitly scopes itself to code analysis. The output expectations assume live-URL tooling (axe-core CLI, Lighthouse, browser-based keyboard testing, screen reader testing) and a procurement-facing compliance summary — none of which this skill supports.

The skill would need a companion mode or a separate live-URL audit skill using Playwright or axe-core CLI to meet these output expectations. The structural quality of the skill definition is high; the applicability to the given scenario is not.
