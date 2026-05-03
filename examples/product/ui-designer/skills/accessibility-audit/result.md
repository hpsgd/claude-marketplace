# Accessibility Audit

Scenario: Testing whether the accessibility-audit skill definition requires WCAG 2.1/2.2 AA evaluation, automated and manual checks, and severity classification for findings.

## Prompt

> /ui-designer:accessibility-audit of https://hps.gd — navigation, page structure, and any interactive elements. We're preparing for an enterprise procurement review that requires WCAG 2.1 AA compliance.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I now have enough data to write the comprehensive audit report.

---

# Accessibility Audit: hps.gd

**Date:** 2026-05-01
**Standard:** WCAG 2.2 Level AA
**Scope:** Homepage (https://hps.gd) — page structure, navigation, interactive elements, images, colour, keyboard access. Static HTML + CSS analysis; JavaScript-driven behaviour and actual rendered contrast values require browser/screen-reader verification.

---

## Summary

| Severity | Count |
|----------|-------|
| Critical | 0 |
| Major | 2 |
| Minor | 3 |
| Best Practice | 3 |

**Overall assessment:** The homepage has a solid accessibility foundation — semantic HTML landmarks, a functioning skip link, descriptive alt text on all images, and no keyboard traps or missing form labels. The most significant barriers are in the mobile navigation: the hamburger button does not communicate open/close state to screen readers, and the `<el-popover>` custom element has no ARIA role, so assistive technology cannot identify what kind of widget it is. These two issues together mean screen reader users on small viewports get no feedback when the menu opens or closes. All other findings are minor or best practice.

---

## Major Issues

### 1 — Mobile menu button does not expose `aria-expanded` state

- **Location:** `<header>` — `<button popoverTarget="mobile-nav" aria-label="Open menu">`
- **WCAG:** 4.1.2 — Name, Role, Value
- **Impact:** Screen reader users who activate the hamburger button hear only "Open menu, button." There is no announcement that the menu has opened or closed. A VoiceOver or NVDA user has no way to know whether the navigation is currently displayed or not.
- **Current code:**
  ```html
  <button type="button" popoverTarget="mobile-nav"
          class="... md:hidden"
          aria-label="Open menu">
    <svg ...><!-- hamburger icon --></svg>
  </button>
  ```
- **Fix:** Add `aria-expanded` and update it via JavaScript when the popover opens/closes. Also add `aria-controls` to associate the button with the nav element it controls.
  ```html
  <button type="button" popoverTarget="mobile-nav"
          class="... md:hidden"
          aria-label="Open menu"
          aria-expanded="false"
          aria-controls="mobile-nav">
    <svg aria-hidden="true" ...><!-- hamburger icon --></svg>
  </button>
  ```
  ```js
  // Toggle aria-expanded when the popover opens/closes
  const btn = document.querySelector('[popovertarget="mobile-nav"]');
  const nav = document.getElementById('mobile-nav');
  nav.addEventListener('toggle', (e) => {
    btn.setAttribute('aria-expanded', e.newState === 'open' ? 'true' : 'false');
  });
  ```
- **Verify:** With VoiceOver (macOS/iOS) or NVDA + Chrome, activate the hamburger. The announcement should change from "Open menu, collapsed, button" to "Open menu, expanded, button" when the menu opens, and back when it closes.

---

### 2 — `<el-popover>` custom element has no ARIA role

- **Location:** `<el-popover id="mobile-nav" ...>` containing the mobile `<nav>`
- **WCAG:** 4.1.2 — Name, Role, Value
- **Impact:** `<el-popover>` is a custom HTML element (web component). Assistive technology does not know what role this element plays. When it opens, screen readers on some browsers will not announce it as a navigation region, a dialog, or any other widget type. Users navigating by landmarks will not find the mobile menu.
- **Current code:**
  ```html
  <el-popover id="mobile-nav"
              class="rounded-xl border ...">
    <nav class="flex flex-col gap-1">
      ...
    </nav>
  </el-popover>
  ```
- **Fix — Option A (preferred):** Replace `<el-popover>` with a native `<div popover>` element, which the browser handles natively with full keyboard and accessibility support:
  ```html
  <div id="mobile-nav" popover
       class="rounded-xl border ..."
       role="dialog"
       aria-label="Site navigation"
       aria-modal="false">
    <nav aria-label="Mobile">
      ...
    </nav>
  </div>
  ```
- **Fix — Option B:** If `el-popover` must stay as a custom element, ensure the component's internal implementation sets the appropriate ARIA role and manages focus entry/exit when it opens.
- **Verify:** With a screen reader open the mobile menu. It should announce the navigation region. Pressing Escape should close the menu and return focus to the hamburger button.

---

## Minor Issues

### 3 — Logo home link announces "hps.gd hps.gd" to screen readers

- **Location:** `<a href="/">` in `<header>` — contains 4 `<img>` elements
- **WCAG:** 1.1.1 — Non-text Content; 4.1.2 — Name, Role, Value
- **Impact:** The link contains two visible images at any time (one icon, one wordmark — dark/light alternates are hidden via CSS). Both have `alt="hps.gd"`. Screen readers concatenate all non-hidden alt values into the link's accessible name, producing "hps.gd hps.gd". This is redundant and confusing.
- **Current code:**
  ```html
  <a href="/">
    <img alt="hps.gd" class="dark:hidden" src="...icon..."/>      <!-- visible light -->
    <img alt="hps.gd" class="hidden dark:block" src="...icon..."/> <!-- visible dark -->
    <img alt="hps.gd" class="dark:hidden" src="...logo..."/>      <!-- visible light -->
    <img alt="hps.gd" class="hidden dark:block" src="...logo..."/> <!-- visible dark -->
  </a>
  ```
- **Fix:** Make the icon images decorative (empty alt) so the accessible name comes from the wordmark alone:
  ```html
  <a href="/" aria-label="hps.gd — Home">
    <img alt="" aria-hidden="true" class="dark:hidden" src="...icon..."/>
    <img alt="" aria-hidden="true" class="hidden dark:block" src="...icon..."/>
    <img alt="hps.gd" class="dark:hidden" src="...logo..."/>
    <img alt="hps.gd" class="hidden dark:block" src="...logo..."/>
  </a>
  ```
- **Verify:** With VoiceOver, navigate to the logo link. It should announce "hps.gd — Home, link" (or similar) exactly once.

---

### 4 — Decorative arrow SVGs inside CTA links are not marked `aria-hidden`

- **Location:** `tabler-icon-arrow-right` SVG inside `<a href="/how-we-work">`, `<a href="/contact">`, and the CTA section
- **WCAG:** 4.1.2 — Name, Role, Value
- **Impact:** SVGs without `aria-hidden="true"`, `role="img"`, or a `<title>` element are exposed inconsistently across screen readers. Some will announce them as "image" or skip them; others may read out path data. The arrow is decorative — the link's text already conveys the action.
- **Current code:**
  ```html
  <a href="/contact" class="...">
    Let's have a chat
    <svg class="tabler-icon tabler-icon-arrow-right">
      <path d="M5 12l14 0"/>
      ...
    </svg>
  </a>
  ```
- **Fix:**
  ```html
  <a href="/contact" class="...">
    Let's have a chat
    <svg aria-hidden="true" focusable="false" class="tabler-icon tabler-icon-arrow-right">
      ...
    </svg>
  </a>
  ```
  Note: `focusable="false"` is required to prevent IE/older Edge from making SVGs keyboard-focusable.
- **Verify:** With NVDA + Firefox, navigate to the "Let's have a chat" link. It should announce only "Let's have a chat, link" with no mention of the icon.

---

### 5 — Social icon links have a ~20×20 px touch target (below WCAG 2.5.8 minimum)

- **Location:** `<footer>` — LinkedIn and GitHub icon links
- **WCAG:** 2.5.8 — Target Size (Minimum) *(WCAG 2.2 new criterion)*
- **Impact:** The SVG icons are rendered at 20×20 CSS pixels with no padding on the link element. WCAG 2.5.8 requires 24×24 CSS pixels unless the offset between targets compensates. On touch devices, these small targets are easy to miss and activate the wrong link.
- **Current code:**
  ```html
  <a aria-label="LinkedIn" href="https://linkedin.com/company/hpsgd">
    <svg width="20" height="20" ...>...</svg>
  </a>
  ```
- **Fix:** Add padding to bring the touch target to at least 24×24 px:
  ```html
  <a aria-label="LinkedIn" href="https://linkedin.com/company/hpsgd"
     class="p-1 ...">  <!-- adds 4px padding = 28×28 total -->
    <svg width="20" height="20" aria-hidden="true" ...>...</svg>
  </a>
  ```
- **Verify:** In Chrome DevTools mobile emulation, confirm the tappable area covers at least 24×24 CSS pixels.

---

## Best Practice Recommendations

### BP1 — Three `<nav>` elements are not differentiated by label

- **Location:** Desktop nav, mobile nav, and footer nav — all `<nav>` without `aria-label`
- **WCAG:** 2.4.1 (satisfied via skip link) / best practice per ARIA Landmarks specification
- **Impact:** Screen reader users who navigate by landmarks (NVDA landmark shortcut `D`, VoiceOver rotor) will encounter three regions all announced as "navigation" with no way to distinguish them.
- **Fix:**
  ```html
  <nav aria-label="Main" class="hidden items-center gap-8 md:flex">...</nav>
  <!-- mobile nav -->
  <nav aria-label="Mobile">...</nav>
  <!-- footer -->
  <nav aria-label="Footer">...</nav>
  ```

---

### BP2 — No `aria-current="page"` on the active navigation link

- **Location:** Desktop and mobile `<nav>` link lists
- **WCAG:** Not a hard violation; supports WCAG 1.3.1 and aids WCAG 3.2.3
- **Impact:** Screen reader users can't determine which page they are currently viewing from the navigation alone.
- **Fix:**
  ```html
  <!-- On the homepage, the home/logo link or a "Home" nav item -->
  <a href="/" aria-current="page">...</a>
  <!-- On /about: -->
  <a href="/about" aria-current="page">About</a>
  ```

---

### BP3 — Canvas background animation should respect `prefers-reduced-motion`

- **Location:** `<canvas>` elements in the hero section (JS-driven particle/gradient animation)
- **WCAG:** 2.3.3 (AAA) / best practice for 1.4.12
- **Impact:** Users who set "Reduce Motion" in their OS to manage vestibular disorders or migraines may still see the animated canvas effect, as the animation is rendered via JavaScript rather than CSS and the canvas elements are not paused by `prefers-reduced-motion`.
- **Fix:** In the animation script, check `window.matchMedia('(prefers-reduced-motion: reduce)').matches` and skip or freeze the canvas animation if true. The CSS already correctly uses `motion-safe:` for other animations.

---

## Checklist Results

### Perceivable

| # | Criterion | WCAG | Pass/Fail/N/A |
|---|-----------|------|---------------|
| P1 | All images have meaningful `alt` text | 1.1.1 | **Minor** — logo link redundancy |
| P2 | Video/audio has captions or transcripts | 1.2.x | N/A |
| P3 | Semantic HTML landmarks and heading hierarchy | 1.3.1 | Pass — h1→h2→h3, no skipped levels |
| P4 | Content not reliant on sensory characteristics alone | 1.3.3 | Pass |
| P5 | Colour not sole conveyor of information | 1.4.1 | Pass |
| P6 | Text contrast ≥4.5:1 (normal), 3:1 (large) | 1.4.3 | Pass — muted text at 70% opacity on white ≈6.9:1; 60% ≈4.9:1 |
| P7 | Text resizable to 200% without loss | 1.4.4 | Pass — rem units used throughout |
| P8 | Non-text contrast ≥3:1 | 1.4.11 | Pass |
| P9 | Reflow at 320px width | 1.4.10 | Pass (requires visual verification) |
| P10 | Text spacing adjustable | 1.4.12 | Pass |

### Operable

| # | Criterion | WCAG | Pass/Fail/N/A |
|---|-----------|------|---------------|
| O1 | All functionality available via keyboard | 2.1.1 | Pass (desktop); **Major risk** (mobile nav) |
| O2 | No keyboard traps | 2.1.2 | Pass |
| O3 | Skip navigation link present | 2.4.1 | Pass — `href="#main-content"`, visible on focus |
| O4 | Page has descriptive `<title>` | 2.4.2 | Pass — "Be Heaps Good - hps.gd" |
| O5 | Focus order matches visual order | 2.4.3 | Pass |
| O6 | Link text is descriptive | 2.4.4 | Pass |
| O7 | Multiple ways to find pages | 2.4.5 | Pass — nav present; single-page site |
| O8 | Headings and labels are descriptive | 2.4.6 | Pass |
| O9 | Focus indicator visible | 2.4.7 | Pass — browser defaults retained; no global outline suppression |
| O10 | Touch targets ≥44×44px | 2.5.5 | Minor — social icons 20×20px |
| O11 | No problematic time limits | 2.2.1 | Pass |
| O12 | Focused element not obscured | 2.4.11 | Pass |
| O13 | Drag alternatives exist | 2.5.7 | N/A — no drag interactions |
| O14 | Touch targets ≥24×24 CSS px | 2.5.8 | **Minor** — social icon links 20×20 |

### Understandable

| # | Criterion | WCAG | Pass/Fail/N/A |
|---|-----------|------|---------------|
| U1 | `<html lang="en">` present | 3.1.1 | Pass |
| U2 | Language changes marked | 3.1.2 | N/A — all English |
| U3 | Navigation consistent across pages | 3.2.3 | Pass (assumed) |
| U4 | Components with same function labelled consistently | 3.2.4 | Pass |
| U5 | Error messages identify field and describe error | 3.3.1 | N/A — no forms on homepage |
| U6 | Labels/instructions for user input | 3.3.2 | N/A |
| U7 | Error suggestions offered | 3.3.3 | N/A |
| U8 | Legal/financial submissions reversible | 3.3.4 | N/A |

### Robust

| # | Criterion | WCAG | Pass/Fail/N/A |
|---|-----------|------|---------------|
| R1 | Valid HTML, no duplicate IDs | 4.1.1 | Pass — no duplicate IDs found |
| R2 | Custom components have ARIA roles, names, values | 4.1.2 | **Major** — `<el-popover>` no role; button no `aria-expanded` |
| R3 | Status messages use `aria-live` or `role="status"` | 4.1.3 | N/A — no toast/status messages on homepage |

---

## Priority Fix Order for Procurement Review

1. **Add `aria-expanded` to the mobile menu button** — one-line HTML change + ~5 lines JS
2. **Assign a role to `<el-popover>` or replace with native `<div popover>`** — highest WCAG 4.1.2 risk
3. **Mark decorative SVG arrows `aria-hidden="true"`** — find/replace across all CTA components
4. **Add `aria-label` to the three `<nav>` elements** — three one-word attribute additions
5. **Fix logo link redundant alt text** — set icon images to `alt=""`
6. **Add 4px padding to footer social icon links**

Issues 1–2 are the ones most likely to be flagged by an automated scanner (axe, Deque) during a formal procurement assessment. Issues 3–6 are quick wins that demonstrate thoroughness.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 11.5/12.5 (92%) |
| Evaluated | 2026-05-01 |
| Target duration | 276141 ms |
| Target cost | $0.6008 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill evaluates against WCAG 2.1 AA (and ideally 2.2) as the compliance standard — not a vague "accessibility best practices" framing | PASS | Report header explicitly states "Standard: WCAG 2.2 Level AA" and individual findings cite WCAG 2.2 new criteria (e.g., "WCAG 2.2 new criterion" for 2.5.8 Target Size). |
| c2 | Skill distinguishes between automated checks (contrast ratios, missing alt text, label associations) and manual checks (keyboard navigation flow, screen reader behaviour) — both are required | PASS | Preamble states "Static HTML + CSS analysis; JavaScript-driven behaviour and actual rendered contrast values require browser/screen-reader verification." Contrast is treated as automated ("muted text at 70% opacity on white ≈6.9:1"); each finding includes a "Verify:" block specifying manual screen-reader steps (e.g., "With VoiceOver (macOS/iOS) or NVDA + Chrome, activate the hamburger"). |
| c3 | Skill classifies findings by severity (e.g. Critical/Major/Minor) with WCAG success criterion referenced for each finding | PASS | Summary table lists Critical/Major/Minor/Best Practice counts. Each finding section includes severity in its heading ("Major Issues", "Minor Issues") and a "WCAG:" line citing the specific SC (e.g., "WCAG: 4.1.2 — Name, Role, Value", "WCAG: 2.5.8 — Target Size (Minimum)"). |
| c4 | Skill covers the four WCAG principles: Perceivable, Operable, Understandable, Robust | PASS | "Checklist Results" section has four subsections explicitly labelled Perceivable (P1–P10), Operable (O1–O14), Understandable (U1–U8), and Robust (R1–R3), each with pass/fail/N/A entries. |
| c5 | Skill produces a prioritised remediation list — not just a findings catalogue | PASS | "Priority Fix Order for Procurement Review" section provides a numbered list of six items in priority order, with rationale: "Issues 1–2 are the ones most likely to be flagged by an automated scanner... Issues 3–6 are quick wins." |
| c6 | Skill includes keyboard navigation testing as a specific required check — partial credit if keyboard access is mentioned but no specific test pattern is defined | PARTIAL | Keyboard access is checked in O1 ("All functionality available via keyboard") and O2 ("No keyboard traps"), and the mobile menu Verify step says "Pressing Escape should close the menu and return focus to the hamburger button." However, no explicit keyboard-traversal test pattern (e.g., Tab-through sequence, focus-order check procedure) is defined. |
| c7 | Skill distinguishes between what blocks compliance (must fix) and what improves usability (should fix) | PASS | Findings are separated into "Major Issues", "Minor Issues", and "Best Practice Recommendations". Priority section explicitly states: "Issues 1–2 are the ones most likely to be flagged by an automated scanner (axe, Deque) during a formal procurement assessment" vs. "Issues 3–6 are quick wins that demonstrate thoroughness." |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output is a chat response only. No YAML frontmatter (name, description, argument-hint fields) appears anywhere in the output. |
| c9 | Output references specific WCAG success criteria (e.g. SC 1.4.3 Contrast (Minimum), SC 2.1.1 Keyboard) per finding, not generic "accessibility issues" | PASS | Every Major and Minor finding cites a specific SC inline (e.g., "WCAG: 4.1.2 — Name, Role, Value", "WCAG: 1.1.1 — Non-text Content; 4.1.2", "WCAG: 2.5.8 — Target Size (Minimum)"). Checklist rows reference criteria numerically (1.1.1, 2.1.1, 1.4.3, etc.). |
| c10 | Output's findings are organised under the four WCAG principles — Perceivable, Operable, Understandable, Robust — with at least one finding category per principle (or "no issues found" stated explicitly) | PARTIAL | The Checklist Results section organises entries under all four principles with explicit pass/fail per criterion. However, the main findings catalogue (Major Issues 1–2, Minor Issues 3–5, Best Practice BP1–3) is organised by severity, not by WCAG principle. |
| c11 | Output's findings each have a severity (Critical / Major / Minor) AND a WCAG SC reference AND a specific location (selector, page section) — not a flat list | PASS | Each finding has: severity from section header (Major/Minor), a "WCAG:" line with SC number and name, and a "Location:" line with HTML selector (e.g., "Location: `<header>` — `<button popoverTarget="mobile-nav" aria-label="Open menu">`"). |
| c12 | Output's remediation list is prioritised — Critical findings (block compliance, e.g. images without alt text, contrast failures on body copy) before Major (impair usability, e.g. focus indicators not visible enough) before Minor | PASS | "Priority Fix Order for Procurement Review" lists items 1–2 as the WCAG 4.1.2 Major issues (compliance risk) before items 3–6 (minor/best-practice). No Critical findings exist, so Major-first ordering is correct. |
| c13 | Output distinguishes compliance-blocking findings from usability improvements — only the former blocks the enterprise procurement review; the latter are recommendations | PASS | Explicitly stated: "Issues 1–2 are the ones most likely to be flagged by an automated scanner (axe, Deque) during a formal procurement assessment. Issues 3–6 are quick wins that demonstrate thoroughness." Best Practice section is clearly separated from compliance findings. |
| c14 | Output addresses dynamic content (any client-side updates, modal dialogs) for ARIA live regions and focus management — these are common WCAG 2.1 AA failure points | PARTIAL | Focus management is addressed for the mobile menu popover: "Pressing Escape should close the menu and return focus to the hamburger button." R3 covers ARIA live regions/role=status (marked N/A with explanation). Canvas animation is addressed for prefers-reduced-motion. However, no broader ARIA live region patterns for client-side content updates are discussed. |

### Notes

The output is a high-quality, detailed accessibility audit that passes comfortably. It explicitly adopts WCAG 2.2 AA as its standard, provides severity-classified findings with SC references and precise HTML locations, covers all four WCAG principles in a structured checklist, and produces a prioritised remediation list that clearly separates compliance-blocking issues from usability improvements. The only outright failure is c8 (YAML frontmatter), which cannot be assessed from a chat response — the skill definition file's metadata is simply not visible in the captured output. The partial deductions reflect that keyboard testing lacks an explicit test pattern (ceiling-capped at PARTIAL) and that ARIA live-region/dynamic-content coverage is present but thin. The distinction between automated and manual checks is functionally present via 'Verify:' blocks but not explicitly labelled as such.
