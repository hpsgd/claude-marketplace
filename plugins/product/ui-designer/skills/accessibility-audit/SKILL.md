---
name: accessibility-audit
description: Audit a component, page, or codebase for WCAG 2.2 AA accessibility compliance. Includes automated pattern detection, severity classification, and remediation recommendations.
argument-hint: "[component, page, or directory to audit]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Audit $ARGUMENTS for accessibility compliance against WCAG 2.2 AA (published October 2023, supersedes 2.1).

This audit uses code analysis to find violations. It is not a substitute for manual testing with screen readers and keyboard, but it catches the most common and highest-impact issues.

---

## Step 1: Automated Pattern Detection

Run these searches against the target files. Each pattern maps to a specific WCAG criterion.

### Images Without Alt Text (WCAG 1.1.1)
```bash
# Find <img> tags without alt attribute
grep -rn '<img' --include="*.tsx" --include="*.jsx" --include="*.html" | grep -v 'alt='
# Find <img> with empty alt on non-decorative images (check manually)
grep -rn 'alt=""' --include="*.tsx" --include="*.jsx"
# Find Image components without alt
grep -rn '<Image' --include="*.tsx" --include="*.jsx" | grep -v 'alt='
```

### Missing Form Labels (WCAG 1.3.1, 4.1.2)
```bash
# Find inputs without associated labels
grep -rn '<input' --include="*.tsx" --include="*.jsx" | grep -v 'aria-label\|aria-labelledby\|id='
# Find select without labels
grep -rn '<select' --include="*.tsx" --include="*.jsx" | grep -v 'aria-label\|aria-labelledby'
# Find textarea without labels
grep -rn '<textarea' --include="*.tsx" --include="*.jsx" | grep -v 'aria-label\|aria-labelledby'
```

### Missing Keyboard Handlers (WCAG 2.1.1)
```bash
# Find onClick without onKeyDown/onKeyUp (non-button/link elements)
grep -rn 'onClick' --include="*.tsx" --include="*.jsx" | grep -v 'button\|Button\|<a \|Link\|onKeyDown\|onKeyUp\|role="button"'
# Find div/span with onClick (should be button or have role="button" + tabIndex)
grep -rn '<div.*onClick\|<span.*onClick' --include="*.tsx" --include="*.jsx"
```

### Missing Focus Management (WCAG 2.4.3, 2.4.7)
```bash
# Find outline:none or outline:0 without replacement focus indicator
grep -rn 'outline: none\|outline:none\|outline: 0\|outline:0\|focus:outline-none' --include="*.tsx" --include="*.jsx" --include="*.css"
# Find modals/dialogs without focus trap
grep -rn 'modal\|dialog\|Dialog\|Modal' --include="*.tsx" --include="*.jsx" | grep -v 'FocusTrap\|focus-trap\|useFocusTrap\|createFocusTrap'
# Find tabIndex values other than 0 or -1 (positive tabIndex is almost always wrong)
grep -rn 'tabIndex=["{][2-9]\|tabIndex=["]{1}[0-9]' --include="*.tsx" --include="*.jsx"
```

### Colour-Only Information (WCAG 1.4.1)
```bash
# Find status indicators that might rely on colour alone
grep -rn 'className=.*red\|className=.*green\|className=.*yellow' --include="*.tsx" --include="*.jsx" | grep -v 'icon\|Icon\|aria-label\|sr-only\|text-'
# Find hardcoded colour values instead of semantic tokens
grep -rn '#[0-9a-fA-F]\{3,6\}\|rgb(' --include="*.tsx" --include="*.jsx" --include="*.css"
```

### Missing Language Attribute (WCAG 3.1.1)
```bash
# Check HTML element for lang attribute
grep -rn '<html' --include="*.html" --include="*.tsx" --include="*.jsx" | grep -v 'lang='
```

### ARIA Misuse (WCAG 4.1.2)
```bash
# Find aria-hidden="true" on focusable elements (dangerous)
grep -rn 'aria-hidden="true"' --include="*.tsx" --include="*.jsx" | grep 'button\|input\|select\|textarea\|href\|tabIndex'
# Find role without required ARIA attributes
grep -rn 'role="tab"' --include="*.tsx" --include="*.jsx" | grep -v 'aria-selected'
grep -rn 'role="checkbox"' --include="*.tsx" --include="*.jsx" | grep -v 'aria-checked'
grep -rn 'role="switch"' --include="*.tsx" --include="*.jsx" | grep -v 'aria-checked'
# Find duplicate IDs (breaks aria-labelledby)
grep -rn 'id="' --include="*.tsx" --include="*.jsx" --include="*.html"
```

### Missing Live Regions (WCAG 4.1.3)
```bash
# Find dynamic content updates that might need announcements
grep -rn 'toast\|Toast\|notification\|Notification\|alert\|Alert\|snackbar' --include="*.tsx" --include="*.jsx" | grep -v 'aria-live\|role="alert"\|role="status"'
```

---

## Step 2: Manual Checklist Audit

After running automated checks, review against the full WCAG 2.2 AA checklist, organised by principle. WCAG 2.2 adds three new AA criteria (2.4.11, 2.5.7, 2.5.8) — these are included in the Operable section below.

### Perceivable

| # | Criterion | WCAG | Check | Pass/Fail/N/A |
|---|-----------|------|-------|---------------|
| P1 | All images have meaningful `alt` text (or `alt=""` for purely decorative) | 1.1.1 | Verified via grep + manual review | |
| P2 | Video/audio has captions or transcripts | 1.2.1-1.2.5 | Check all media elements | |
| P3 | Content structure uses semantic HTML (headings, lists, landmarks) | 1.3.1 | Check heading hierarchy (no skipped levels) | |
| P4 | Content is meaningful without relying on sensory characteristics ("click the red button") | 1.3.3 | Review instructional text | |
| P5 | Colour is not the sole means of conveying information | 1.4.1 | Status indicators, error states, links within text | |
| P6 | Text contrast ratio: 4.5:1 normal, 3:1 large (18px+ / 14px+ bold) | 1.4.3 | Check all text against background colours | |
| P7 | Text can be resized to 200% without content loss or overlap | 1.4.4 | Browser zoom to 200%, check layout | |
| P8 | Non-text contrast: 3:1 for UI components and graphical objects | 1.4.11 | Check icons, borders, form controls, charts | |
| P9 | Content reflows to single column at 320px width without horizontal scroll | 1.4.10 | Test at 320px viewport | |
| P10 | Text spacing can be adjusted without content loss (line height 1.5x, paragraph spacing 2x, letter spacing 0.12em, word spacing 0.16em) | 1.4.12 | Override styles and verify | |

### Operable

| # | Criterion | WCAG | Check | Pass/Fail/N/A |
|---|-----------|------|-------|---------------|
| O1 | All functionality available via keyboard | 2.1.1 | Tab through entire interface, activate every control | |
| O2 | No keyboard traps — user can always Tab away | 2.1.2 | Verify escape from every component | |
| O3 | Skip navigation link present for repeated content blocks | 2.4.1 | Check for "Skip to main content" link | |
| O4 | Page has a descriptive `<title>` | 2.4.2 | Check `<title>` or `<Head>` | |
| O5 | Focus order matches visual/logical reading order | 2.4.3 | Tab through page, compare to visual order | |
| O6 | Link text is descriptive out of context (not "click here", "read more") | 2.4.4 | Review all link text | |
| O7 | Multiple ways to find pages (nav, search, sitemap) | 2.4.5 | Verify navigation mechanisms | |
| O8 | Headings and labels are descriptive | 2.4.6 | Review all headings and form labels | |
| O9 | Focus indicator is visible on all interactive elements | 2.4.7 | Tab through every focusable element | |
| O10 | Touch targets are at least 44x44px | 2.5.5 | Verify button/link sizes on mobile | |
| O11 | No time limits, or user can extend/disable them | 2.2.1 | Check for session timeouts, auto-advancing content | |
| O12 | Focused element is not entirely hidden by author-created content | 2.4.11 | Tab through page, verify focused element is always at least partially visible | |
| O13 | Functionality via dragging can also be achieved with a single pointer without dragging | 2.5.7 | For every drag interaction, verify an alternative (e.g. buttons, tap-to-move) exists | |
| O14 | Touch/click targets are at least 24x24 CSS pixels (with allowed exceptions) | 2.5.8 | Measure interactive element sizes; inline links and browser-default controls are exempt | |

### Understandable

| # | Criterion | WCAG | Check | Pass/Fail/N/A |
|---|-----------|------|-------|---------------|
| U1 | Page language is specified (`<html lang="en">`) | 3.1.1 | Check document root | |
| U2 | Language changes within content are marked (`<span lang="fr">`) | 3.1.2 | Check for foreign text | |
| U3 | Navigation is consistent across pages | 3.2.3 | Compare navigation patterns | |
| U4 | Components with same function have consistent labels | 3.2.4 | Review repeated UI patterns | |
| U5 | Error messages identify the field and describe the error clearly | 3.3.1 | Trigger every validation error | |
| U6 | Labels or instructions provided for user input | 3.3.2 | Check all form fields | |
| U7 | Error suggestions offered when input format is known | 3.3.3 | Check validation messages for helpful suggestions | |
| U8 | Legal/financial submissions can be reviewed, confirmed, or reversed | 3.3.4 | Check destructive/financial actions | |

### Robust

| # | Criterion | WCAG | Check | Pass/Fail/N/A |
|---|-----------|------|-------|---------------|
| R1 | Valid HTML — no duplicate IDs, proper nesting | 4.1.1 | Run HTML validator or check manually | |
| R2 | Custom components have appropriate ARIA roles, names, values | 4.1.2 | Review all custom interactive components | |
| R3 | Status messages use `aria-live` or `role="status"`/`role="alert"` | 4.1.3 | Check toast notifications, form feedback, loading states | |

---

## Step 3: Severity Classification

Classify every finding using this matrix:

| Severity | Definition | Examples | Response |
|----------|-----------|----------|----------|
| **Critical** | Users with disabilities cannot complete core tasks. Legal risk. | Missing form labels on checkout, keyboard trap in modal, no alt text on functional images | Fix before next release. Block deployment if on a new feature. |
| **Major** | Significant barrier but workaround exists, or affects a secondary flow. | Poor contrast on secondary text, missing skip link, focus order confusing but functional | Fix within current sprint. |
| **Minor** | Inconvenience but does not block task completion. | Decorative image missing alt="", non-critical animation lacks reduced-motion support | Fix in next grooming cycle. |
| **Best Practice** | Not a WCAG violation but improves the experience. | Adding `aria-describedby` for extra context, improving focus indicator visibility | Add to backlog for progressive improvement. |

---

## Step 4: Remediation Recommendations

For every finding, provide:

1. **What the violation is** — specific, with file and line reference
2. **Which WCAG criterion it violates** — the number and name
3. **Why it matters** — who is affected and how (do not just cite the spec — describe the real impact)
4. **How to fix it** — specific code change, not just "add alt text." Show the before and after.
5. **How to verify the fix** — what to test and how

---

## Output Format

```markdown
# Accessibility Audit: [Target]

**Date:** [date]
**Standard:** WCAG 2.2 Level AA
**Scope:** [what was audited]

## Summary

| Severity | Count |
|----------|-------|
| Critical | N |
| Major | N |
| Minor | N |
| Best Practice | N |

**Overall assessment:** [One paragraph: is this component/page usable by people with disabilities? What are the biggest barriers?]

## Critical Issues

### [Issue title]
- **Location:** `[file:line]`
- **WCAG:** [criterion number] — [criterion name]
- **Impact:** [who is affected and how]
- **Current code:**
  ```tsx
  // problematic code
  ```
- **Fix:**
  ```tsx
  // corrected code
  ```
- **Verify:** [how to test the fix]

## Major Issues
[Same format]

## Minor Issues
[Same format]

## Best Practice Recommendations
[Same format]

## Checklist Results
[Include the completed checklist from Step 2 with Pass/Fail/N/A filled in]
```

## Related Skills

- `/ui-designer:component-spec` — when accessibility failures require component changes, update the component spec to include the fix.
- `/ui-designer:design-review` — accessibility findings should be included in design reviews.
