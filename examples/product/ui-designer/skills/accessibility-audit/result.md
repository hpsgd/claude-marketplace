# Result: Accessibility audit

**Verdict:** PASS
**Score:** 13.5/14 criteria met (96%)
**Evaluated:** 2026-04-30

---

## Output

Simulated output for the prompt: `/ui-designer:accessibility-audit of https://hps.gd — navigation, page structure, and any interactive elements. We're preparing for an enterprise procurement review that requires WCAG 2.1 AA compliance.`

> Note: The skill is scoped to code analysis (allowed-tools: Read, Bash, Glob, Grep). The prompt targets a live URL. The output below reflects what the skill would produce when run against the hps.gd source repository. If only the live URL is available, a browser-based tool or axe-core CLI would be needed to supplement this skill.

---

# Accessibility Audit: hps.gd — Navigation, Page Structure, Interactive Elements

**Date:** 2026-04-30
**Standard:** WCAG 2.2 Level AA (supersedes WCAG 2.1 AA — all 2.1 AA criteria are covered)
**Scope:** Navigation components, page structure (landmarks, headings), and interactive elements across the hps.gd codebase

## Summary

| Severity | Count |
|----------|-------|
| Critical | 2 |
| Major | 3 |
| Minor | 2 |
| Best Practice | 2 |

**Overall assessment:** The site has a functional visual structure but presents barriers for keyboard-only users and screen reader users. Two critical issues — a missing keyboard handler on the mobile menu toggle and unlabelled icon-only buttons in the navigation — would block WCAG 2.1 AA compliance for an enterprise procurement review. These must be fixed before submission. The remaining major issues (focus indicator suppression, missing skip link, colour-only state on the active nav item) impair usability for assistive technology users but have workarounds. Minor issues are cosmetic and low risk.

---

## Critical Issues

### 1. Mobile nav toggle — onClick without keyboard handler

- **Location:** `components/Nav.tsx:47`
- **WCAG:** 2.1.1 — Keyboard
- **Impact:** Keyboard-only users cannot open the mobile navigation menu. The entire site navigation is inaccessible without a mouse on small viewports.
- **Current code:**
  ```tsx
  <div className="menu-toggle" onClick={handleMenuOpen}>
    <MenuIcon />
  </div>
  ```
- **Fix:**
  ```tsx
  <button
    className="menu-toggle"
    onClick={handleMenuOpen}
    aria-expanded={menuOpen}
    aria-controls="primary-nav"
    aria-label="Open navigation menu"
  >
    <MenuIcon aria-hidden="true" />
  </button>
  ```
- **Verify:** Tab to the menu toggle. Press Enter and Space — menu should open. Confirm `aria-expanded` updates to `true`. Close with Escape.

### 2. Icon-only buttons — no accessible name

- **Location:** `components/SocialLinks.tsx:12-28`
- **WCAG:** 4.1.2 — Name, Role, Value
- **Impact:** Screen reader users hear "button" with no name for each social link. They cannot determine where the link goes.
- **Current code:**
  ```tsx
  <a href="https://linkedin.com/in/martin-lau">
    <LinkedInIcon />
  </a>
  ```
- **Fix:**
  ```tsx
  <a href="https://linkedin.com/in/martin-lau" aria-label="Martin Lau on LinkedIn">
    <LinkedInIcon aria-hidden="true" />
  </a>
  ```
- **Verify:** Navigate to links with a screen reader (VoiceOver / NVDA). Each link should announce its destination.

---

## Major Issues

### 3. Focus indicator suppressed globally

- **Location:** `styles/globals.css:14`
- **WCAG:** 2.4.7 — Focus Visible
- **Impact:** Keyboard-only users lose visual location on the page. Affects all interactive elements.
- **Current code:**
  ```css
  * {
    outline: none;
  }
  ```
- **Fix:**
  ```css
  /* Remove the global suppression. Add focus styles per component: */
  :focus-visible {
    outline: 2px solid #005fcc;
    outline-offset: 2px;
    border-radius: 2px;
  }
  ```
- **Verify:** Tab through every interactive element. Each must have a visible focus indicator with at least 3:1 contrast against the surrounding background (WCAG 2.4.11).

### 4. No skip navigation link

- **Location:** `components/Layout.tsx` — not present
- **WCAG:** 2.4.1 — Bypass Blocks
- **Impact:** Keyboard users must tab through the full navigation (8 links) on every page before reaching main content.
- **Fix:**
  ```tsx
  // Insert as the first child of <body>
  <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4">
    Skip to main content
  </a>
  ```
- **Verify:** Press Tab on page load. First focusable element should be the skip link. Activating it should move focus to `#main-content`.

### 5. Active navigation item conveyed by colour only

- **Location:** `components/Nav.tsx:31`
- **WCAG:** 1.4.1 — Use of Colour
- **Impact:** Colour-blind users cannot identify which navigation item is the current page.
- **Current code:**
  ```tsx
  <NavLink className={isActive ? 'text-blue-600' : 'text-gray-700'}>
  ```
- **Fix:**
  ```tsx
  <NavLink
    className={isActive ? 'text-blue-600 font-semibold' : 'text-gray-700'}
    aria-current={isActive ? 'page' : undefined}
  >
  ```
- **Verify:** View nav with a greyscale filter — active item must remain distinguishable. Confirm screen reader announces "current" for the active link.

---

## Minor Issues

### 6. Decorative hero image — missing `alt=""`

- **Location:** `components/Hero.tsx:8`
- **WCAG:** 1.1.1 — Non-text Content
- **Impact:** Screen readers announce the filename or a garbled description for a purely decorative image.
- **Fix:** Add `alt=""` to suppress the announcement for decorative images.
- **Verify:** VoiceOver should skip the image entirely.

### 7. Heading hierarchy skips from H1 to H3

- **Location:** `pages/index.tsx:34`
- **WCAG:** 1.3.1 — Info and Relationships
- **Impact:** Screen reader users navigating by heading encounter an unexpected jump. Structural meaning is lost.
- **Fix:** Change the H3 to H2, or insert an H2 section heading above it.
- **Verify:** Use a heading outline tool (e.g. HeadingsMap) to confirm a sequential hierarchy.

---

## Best Practice Recommendations

### 8. Contact form — inline error messages lack `aria-describedby`

Not a WCAG violation, but associating error messages with their fields via `aria-describedby` gives screen reader users immediate context without needing to navigate back to the field.

### 9. Social links — add `rel="noopener noreferrer"` for external links

Not a WCAG issue. Improves security for links opening in new tabs, and pairing with a visually hidden "(opens in new tab)" notice reduces surprise for screen reader users.

---

## Checklist Results

### Perceivable

| # | Criterion | WCAG | Pass/Fail/N/A |
|---|-----------|------|---------------|
| P1 | Images have meaningful `alt` text | 1.1.1 | Fail — hero image missing `alt=""` (Minor #6) |
| P2 | Video/audio has captions/transcripts | 1.2.1–1.2.5 | N/A — no media elements |
| P3 | Semantic HTML structure (headings, landmarks) | 1.3.1 | Fail — heading hierarchy skips H2 (Minor #7) |
| P4 | Content not conveyed by sensory characteristics alone | 1.3.3 | Pass |
| P5 | Colour not the sole means of conveying information | 1.4.1 | Fail — active nav item colour-only (Major #5) |
| P6 | Text contrast 4.5:1 normal / 3:1 large | 1.4.3 | Pass — all sampled text meets threshold |
| P7 | Text resizes to 200% without loss | 1.4.4 | Pass |
| P8 | Non-text contrast 3:1 for UI components | 1.4.11 | Pass |
| P9 | Reflows to 320px without horizontal scroll | 1.4.10 | Pass |
| P10 | Text spacing adjustable without content loss | 1.4.12 | Pass |

### Operable

| # | Criterion | WCAG | Pass/Fail/N/A |
|---|-----------|------|---------------|
| O1 | All functionality via keyboard | 2.1.1 | Fail — mobile nav toggle not keyboard accessible (Critical #1) |
| O2 | No keyboard traps | 2.1.2 | Pass |
| O3 | Skip navigation link present | 2.4.1 | Fail — not present (Major #4) |
| O4 | Page has descriptive `<title>` | 2.4.2 | Pass |
| O5 | Focus order matches visual/logical order | 2.4.3 | Pass |
| O6 | Link text descriptive out of context | 2.4.4 | Pass |
| O7 | Multiple ways to find pages | 2.4.5 | Pass — nav + contact info |
| O8 | Headings and labels are descriptive | 2.4.6 | Pass |
| O9 | Focus indicator visible on all interactive elements | 2.4.7 | Fail — outline suppressed globally (Major #3) |
| O10 | Touch targets at least 44x44px | 2.5.5 | Pass |
| O11 | No problematic time limits | 2.2.1 | N/A |
| O12 | Focused element not hidden by author-created content | 2.4.11 | Pass |
| O13 | Drag functionality has single-pointer alternative | 2.5.7 | N/A — no drag interactions |
| O14 | Touch/click targets at least 24x24 CSS px | 2.5.8 | Pass |

### Understandable

| # | Criterion | WCAG | Pass/Fail/N/A |
|---|-----------|------|---------------|
| U1 | Page language specified | 3.1.1 | Pass — `<html lang="en">` present |
| U2 | Language changes marked | 3.1.2 | N/A |
| U3 | Navigation consistent across pages | 3.2.3 | Pass |
| U4 | Components with same function have consistent labels | 3.2.4 | Pass |
| U5 | Error messages identify field and error | 3.3.1 | Pass |
| U6 | Labels/instructions for user input | 3.3.2 | Pass |
| U7 | Error suggestions offered | 3.3.3 | Pass |
| U8 | Legal/financial actions can be reviewed | 3.3.4 | N/A |

### Robust

| # | Criterion | WCAG | Pass/Fail/N/A |
|---|-----------|------|---------------|
| R1 | Valid HTML — no duplicate IDs, proper nesting | 4.1.1 | Pass |
| R2 | Custom components have ARIA roles, names, values | 4.1.2 | Fail — icon-only buttons unlabelled (Critical #2) |
| R3 | Status messages use `aria-live` or `role="status"` | 4.1.3 | Pass — toast uses `role="status"` |

---

## Compliance verdict for enterprise procurement review

Two Critical issues block WCAG 2.1 AA compliance sign-off:

1. Mobile nav toggle inaccessible by keyboard (2.1.1)
2. Icon-only social links lack accessible names (4.1.2)

Fix these before submitting. The three Major issues should be resolved in the same sprint — they would be noted by any independent auditor and may trigger follow-up questions during procurement review.

---

## Related Skills

- `/ui-designer:component-spec` — update the NavLink and SocialLinks component specs to include the accessibility fixes.
- `/ui-designer:design-review` — include these findings in the next design review before the procurement submission.

---

## Evaluation

### Criteria

- [x] PASS: Skill evaluates against WCAG 2.1 AA (and ideally 2.2) — met. Frontmatter and body target WCAG 2.2 AA explicitly, with a note that it supersedes 2.1. The enterprise procurement review's WCAG 2.1 requirement is fully covered.
- [x] PASS: Skill distinguishes automated from manual checks — met. Step 1 is explicit grep-pattern automated detection mapped to specific WCAG criteria. Step 2 is a structured manual checklist. Both are required and clearly separated.
- [x] PASS: Skill classifies findings by severity with WCAG criterion referenced — met. Step 3 defines Critical / Major / Minor / Best Practice with definitions, examples, and response timelines. Step 4 and the output template mandate a WCAG criterion number per finding.
- [x] PASS: Skill covers all four WCAG principles — met. Step 2 manual checklist is explicitly organised under Perceivable, Operable, Understandable, Robust with criterion numbers mapped to each row.
- [x] PASS: Skill produces a prioritised remediation list — met. Output format enforces Critical → Major → Minor → Best Practice order. Severity matrix includes response timelines (block deployment, fix this sprint, fix next cycle, backlog).
- [x] PASS: Skill includes keyboard navigation as a specific required check with a defined test pattern — met. Step 1 includes grep patterns for onClick without onKeyDown, div/span with onClick, outline suppression, and modal focus traps. Step 2 has O1 (tab through entire interface, activate every control), O2 (keyboard escape), O5 (focus order), O9 (focus indicator). Patterns are specific, not a vague mention. Full credit; PARTIAL is not warranted.
- [x] PASS: Skill distinguishes must-fix from should-fix — met. Critical is defined as "Users with disabilities cannot complete core tasks. Legal risk." with "Block deployment." Best Practice is "Not a WCAG violation" with "Add to backlog." The boundary is unambiguous.
- [x] PASS: Valid YAML frontmatter with name, description, argument-hint — met. All three fields present and well-formed.

### Output expectations

- [x] PASS: Output references specific WCAG success criteria per finding — met. Every finding in the simulated output includes the criterion number and name (e.g. "2.1.1 — Keyboard", "4.1.2 — Name, Role, Value").
- [~] PARTIAL: Output findings organised under the four WCAG principles — partially met. Step 2's manual checklist is structured by POUR principle and the simulated output's checklist section covers all four principles with explicit Pass/Fail/N/A per criterion. However, the main findings sections (Critical / Major / Minor) are ordered by severity, not grouped by principle. There is no requirement in the output format to group findings by POUR in the issues sections, and no "no issues found" placeholder per principle in the issues (only in the checklist). The POUR structure is present in the checklist, not in the findings body.
- [x] PASS: Output findings each have severity, WCAG SC reference, and specific location — met. Every finding in the simulated output includes a Location (file:line), WCAG criterion number, severity (via section heading), and Impact.
- [x] PASS: Output remediation list is prioritised Critical before Major before Minor — met. Output sections enforce this order, and the compliance verdict section restates what must be fixed before procurement submission.
- [x] PASS: Output distinguishes compliance-blocking from usability improvements — met. The simulated output's compliance verdict section explicitly separates the two Critical issues (block compliance sign-off) from Major and Minor findings (should-fix, not blockers).
- [~] PARTIAL: Output addresses dynamic content for ARIA live regions and focus management — partially met. The simulated output includes a checklist entry for R3 (aria-live / role="status") and notes the toast notification uses `role="status"` (Pass). The skill's Step 1 includes automated detection for missing live regions on toast/notification/alert elements (WCAG 4.1.3). However, the output format template has no dedicated section for dynamic content concerns — findings surface under Critical/Major only if violations are detected. There is no explicit prompt to surface ARIA live region or focus management findings for dynamic content as a distinct output category, and modal focus trap findings appear only if the grep patterns match.

**Score detail:**

| Group | Criteria | Met | Score |
|---|---|---|---|
| Skill criteria (8) | 8 PASS | 8 | 8/8 |
| Output expectations (6) | 4 PASS, 2 PARTIAL | 4 + 1 | 5.5/6 |
| **Total** | **14** | | **13.5/14** |

**Combined score: 13.5/14 = 96%**

## Notes

The skill is well-designed for static code analysis of a React/Next.js codebase. It covers WCAG 2.2 AA (exceeding the 2.1 requirement in the prompt), provides specific grep patterns for the most common failure modes, and the output format produces an audit artefact that would satisfy an enterprise procurement review.

One scope gap worth flagging: the prompt targets a live URL (`https://hps.gd`) but the skill's allowed-tools are Read, Bash, Glob, Grep — no browser or HTTP tools. It cannot evaluate rendered contrast ratios against live page styles, trace live tab order in a rendered browser, or test screen reader behaviour at runtime. The simulated output assumes source code access. For live-URL-only audits, axe-core CLI (`npx axe https://hps.gd`) or Playwright with axe-playwright would complement this skill.

The PARTIAL on output criterion 2 (POUR grouping in findings) is a design choice that is defensible — severity-first ordering is more actionable for developers than principle-first — but it means a reader cannot immediately answer "are we failing any Operable criteria?" without scanning the full findings body. Adding a POUR summary table to the output format would resolve this with minimal added complexity.
