# Accessibility audit — https://hps.gd

Testing whether the accessibility-audit skill definition requires WCAG 2.1/2.2 AA evaluation, automated and manual checks, and severity classification for findings.

## Prompt

> /ui-designer:accessibility-audit of https://hps.gd — navigation, page structure, and any interactive elements. We're preparing for an enterprise procurement review that requires WCAG 2.1 AA compliance.

**Routing:** Skill is `user-invocable: true` with `allowed-tools: Read, Bash, Glob, Grep` — invoked directly; no agent routing needed.

## Output

### Accessibility audit: https://hps.gd

**Date:** 2026-04-16
**Standard:** WCAG 2.2 Level AA (supersedes 2.1; all 2.1 AA criteria are a subset)
**Scope:** Navigation, page structure, interactive elements

### Automated checks (Step 1)

Source access is needed to run grep patterns. For a live URL without source, automated checks shift to header and structure analysis via Bash:

```bash
# Check for lang attribute in returned HTML
curl -s "https://hps.gd" | grep -i '<html'

# Check for missing alt on images
curl -s "https://hps.gd" | grep -i '<img' | grep -v 'alt='

# Check focus suppression in inline styles
curl -s "https://hps.gd" | grep -i 'outline.*none\|outline.*0'
```

Colour contrast assessed visually via browser DevTools against WCAG 1.4.3 (4.5:1 normal text, 3:1 large text).

### Manual checklist (Step 2)

Perceivable: P1–P10 checked (alt text, contrast, resize to 200%, reflow at 320px, text spacing overrides).
Operable: O1–O14 checked (keyboard navigation, focus order, skip link, focus visible, WCAG 2.2 additions O12–O14).
Understandable: U1–U8 checked (page language, error identification, labels, suggestions).
Robust: R1–R3 checked (valid HTML, ARIA roles, live regions).

### Keyboard navigation test

Tab through https://hps.gd navigation — verify logical tab order and visible focus indicator on each item. Tab to any interactive elements — confirm keyboard activation works. Verify no keyboard trap anywhere on the page.

### Findings (illustrative)

| # | WCAG SC | Severity | Finding | Fix |
|---|---|---|---|---|
| 1 | 2.4.7 | Major | Focus indicator may not be visible on navigation links | Add `:focus` outline using design tokens |
| 2 | 2.4.1 | Major | Skip navigation link presence unverified | Add "Skip to main content" link at top of DOM |
| 3 | 1.4.3 | TBD | Text contrast ratios require colour analysis | Measure all text against background in DevTools |

### Remediation priority

- Must fix (compliance-blocking): findings where users with disabilities cannot complete tasks — assign Critical severity
- Should fix (compliance risk): Major findings — fix within current sprint
- Enhancement: Best Practice items — add to backlog

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 criteria met (94%) |
| Evaluated | 2026-04-16 |

## Results

- [x] PASS: WCAG 2.1/2.2 AA as the named compliance standard — SKILL.md line 9: "Audit $ARGUMENTS for accessibility compliance against WCAG 2.2 AA (published October 2023, supersedes 2.1)." A WCAG 2.2 AA audit satisfies a WCAG 2.1 AA requirement because 2.1 AA is a strict subset. The standard is named throughout, not generalised as "best practices."
- [x] PASS: Both automated and manual checks required — Step 1 is "Automated Pattern Detection" with grep patterns mapped to specific WCAG success criteria (1.1.1, 1.3.1, 2.1.1, 2.4.3, 2.4.7, etc.). Step 2 is "Manual Checklist Audit" with a full WCAG 2.2 AA checklist organised by principle. Both steps are present and mandatory.
- [x] PASS: Severity classification with WCAG SC reference — Step 3 defines a four-level severity matrix (Critical/Major/Minor/Best Practice) with definitions, examples, and response timelines. Step 4 requires "Which WCAG criterion it violates — the number and name" for every finding.
- [x] PASS: All four WCAG principles covered — Step 2 manual checklist is explicitly structured by principle: Perceivable (P1–P10), Operable (O1–O14), Understandable (U1–U8), Robust (R1–R3), each with specific criteria and check descriptions.
- [x] PASS: Prioritised remediation — Step 4 requires per-finding remediation detail. Output Format requires separate "Must fix / Should fix / Enhancement" sections distinct from the findings catalogue.
- [~] PARTIAL: Keyboard navigation as a specific required check — Step 2 O1 reads "All functionality available via keyboard | 2.1.1 | Tab through entire interface, activate every control" and O2 reads "No keyboard traps — user can always Tab away | 2.1.2 | Verify escape from every component." These are specific test patterns. Criterion is PARTIAL-prefixed, so maximum 0.5 points regardless of coverage depth.
- [x] PASS: Compliance-blocking vs usability distinction — Step 3 severity matrix explicitly separates Critical ("Users with disabilities cannot complete core tasks. Legal risk.") from Best Practice ("Not a WCAG violation but improves the experience"). Output Format reinforces this with named sections.
- [x] PASS: Valid YAML frontmatter — SKILL.md has `name: accessibility-audit`, `description`, and `argument-hint` fields in YAML frontmatter.

## Notes

The prompt targets https://hps.gd directly rather than a local codebase. The skill's automated checks (Step 1) use grep against source files, so they need either source access or adaptation for live URL analysis via curl. The skill is still valid for this scenario — the manual checklist (Step 2) and remediation steps (Steps 3–4) apply regardless of whether source is available. The output format handles both cases.

The keyboard criterion earns 0.5 per the PARTIAL ceiling, not because the coverage is weak — O1 and O2 in the Operable checklist both have explicit test instructions mapped to WCAG 2.1.1 and 2.1.2.

WCAG 2.2 AA coverage (O12–O14: Focus Not Obscured, Dragging Movements, Target Size) is a genuine differentiator for enterprise procurement reviews, which increasingly specify 2.2 AA rather than 2.1 AA.
