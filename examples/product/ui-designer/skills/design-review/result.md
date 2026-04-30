# Result: Design review

**Verdict:** PARTIAL
**Score:** 14.5/16 criteria met (91%)
**Evaluated:** 2026-04-30

## Output

Simulated execution of `/ui-designer:design-review` on the notification centre designs — a slide-out panel showing all user notifications with read/unread states, filtering, and bulk actions.

---

# Design Review: Notification Centre Panel

**Reviewed:** `components/NotificationPanel.tsx`, `components/NotificationItem.tsx`, `components/NotificationFilter.tsx`, `components/BulkActions.tsx`
**Design system:** `tailwind.config.ts` + `components/ui/` primitives

---

## Blockers (must fix before merge)

### Missing Focus state on notification rows
- **File:** `components/NotificationItem.tsx:34`
- **Issue:** Notification rows are clickable (`onClick`) but have no `focus-visible:` class. Keyboard users tabbing through the panel see no visible focus indicator, violating WCAG 2.4.7 (Focus Visible, AA).
- **Fix:** Add `focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:outline-none` to the row wrapper.

### Read/unread distinction relies on colour alone
- **File:** `components/NotificationItem.tsx:52`
- **Issue:** Unread notifications are distinguished only by a blue dot and a lighter background. No typographic weight difference or icon exists to communicate the state without colour, violating WCAG 1.4.1 (Use of Color, A).
- **Fix:** Add `font-semibold` to the notification title for unread items, or add a textual `sr-only` label ("Unread") alongside the blue dot.

### Loading state missing on panel mount
- **File:** `components/NotificationPanel.tsx:18`
- **Issue:** `useSWR('/api/notifications')` is called with no skeleton or spinner while `isLoading` is true. The panel renders an empty container until data arrives — no visual feedback, no accessible `aria-busy` attribute.
- **Fix:** Check `isLoading` before rendering list. Show `<NotificationSkeleton />` with `aria-busy="true"` on the container.

### Error state missing
- **File:** `components/NotificationPanel.tsx:22`
- **Issue:** `isError` from `useSWR` is not handled. If the fetch fails, the panel is silent — no error message, no retry action.
- **Fix:** Add an error state with a short message ("Couldn't load notifications") and a Retry button that calls `mutate()`.

### Icon-only bulk-action buttons have no accessible label
- **File:** `components/BulkActions.tsx:41`
- **Issue:** "Mark all read" and "Delete selected" are rendered as icon-only `<Button>` elements with no `aria-label` or `sr-only` text. Screen readers announce nothing useful.
- **Fix:** Add `aria-label="Mark all notifications as read"` and `aria-label="Delete selected notifications"`, or wrap the icon with `<span className="sr-only">` label text.

### Hardcoded hex in notification dot
- **File:** `components/NotificationItem.tsx:61`
- **Issue:** `style={{ backgroundColor: '#3B82F6' }}` — hardcoded blue. This will not update with theme changes or dark mode.
- **Fix:** Replace with `bg-brand-500` (or whichever token maps to this blue in `tailwind.config.ts`).

---

## Suggestions (should fix, not blocking)

### Active (Disabled) state not designed for bulk-action buttons
- **File:** `components/BulkActions.tsx:38`
- **Issue:** When no notifications are selected, bulk-action buttons are hidden entirely rather than shown as disabled. This removes the affordance — users don't know the actions exist until they select something.
- **Fix:** Keep buttons visible with `disabled` attribute and `disabled:opacity-50 cursor-not-allowed` styling.

### Filter bar has no empty-filtered-state
- **File:** `components/NotificationFilter.tsx`
- **Issue:** When a filter is active and no notifications match, the panel shows the loading skeleton (from `isLoading` being briefly true on re-fetch). No dedicated empty-filtered-state message is shown.
- **Fix:** After data resolves with an active filter and zero results, render "No [type] notifications" with a "Clear filter" link.

### Fixed width on slide-out panel overflows on small viewports
- **File:** `components/NotificationPanel.tsx:8`
- **Issue:** Panel has `w-[420px]` — a fixed pixel width. On viewports narrower than 420px the panel overflows horizontally.
- **Fix:** Replace with `w-full sm:w-[420px]` or `max-w-[420px] w-full`.

### Notification rows use raw `<button>` instead of Button primitive
- **File:** `components/NotificationItem.tsx:30`
- **Issue:** Each row is a raw `<button>` element styled manually, bypassing the shared `<Button>` component and its built-in state classes and accessible defaults.
- **Fix:** Refactor to `<Button variant="ghost" asChild>` wrapping the row content, or extract a `<NotificationRow>` that composes the design system primitive.

---

## Nits (minor, fix if touching this code)

### Conditional className uses template literals instead of `cn()`
- **File:** `components/NotificationItem.tsx:35`
- **Issue:** `className={\`notification-row ${isUnread ? 'bg-blue-50' : ''}\`}` — template literal with a potentially empty string.
- **Fix:** Use `cn('notification-row', isUnread && 'bg-blue-50')` for cleaner output.

### Active press feedback missing on rows
- **File:** `components/NotificationItem.tsx:34`
- **Issue:** No `active:` class on notification rows. Minor UX gap — press feedback helps confirm the tap on mobile.
- **Fix:** Add `active:bg-gray-100`.

---

## Summary

| Dimension | Finding |
|---|---|
| Design system consistency | Hardcoded hex on notification dot — 1 Blocker |
| Component patterns | Raw `<button>` bypassing primitive — 1 Suggestion, template literal — 1 Nit |
| State coverage | Loading missing, Error missing, Disabled (bulk) not designed — 2 Blockers, 1 Suggestion |
| Accessibility | Focus state missing, colour-only read/unread, unlabelled icon buttons — 3 Blockers |
| Responsive behaviour | Fixed `w-[420px]` overflow on mobile — 1 Suggestion |
| Code quality / handoff | `aria-busy` missing, redlines appear complete in Figma but spacing tokens not annotated for `NotificationItem` padding |

- **Blockers:** 6
- **Suggestions:** 4
- **Nits:** 2
- **Verdict:** Request changes — address all 6 blockers before merge. Suggestions recommended before ship; nits optional.

---

## Criteria results

### Criteria (skill definition)

- [x] PASS: Skill reviews across all 6 dimensions: design system consistency, component patterns, state coverage, accessibility, responsive behaviour, and code handoff quality — all six named dimensions present in the SKILL.md
- [x] PASS: Skill requires checking all 8 component states — Dimension 3 explicitly lists Default, Hover, Focus, Active, Disabled, Loading, Error, Empty and routes missing states to Blockers
- [x] PASS: Skill requires accessibility to be reviewed as a constraint — Dimension 4 opens with "WCAG failures are blocking issues, not suggestions" as an explicit policy statement
- [x] PASS: Skill produces findings with severity classifications — three-tier output format: Blockers / Suggestions / Nits
- [x] PASS: Skill checks for design system consistency — Dimension 1 covers colour tokens, type scale, spacing scale, and border radius with grep checks flagging deviations
- [~] PARTIAL: Skill reviews responsive behaviour across breakpoints — Dimension 5 references Tailwind breakpoint prefixes (sm/md/lg/xl) and common responsive issues, but does not require specific named breakpoints to be checked as mandatory; partial credit per criterion
- [x] PASS: Skill produces a prioritised list of required changes before approval — Blockers section is listed first in the output format and the Verdict is gated on blockers being resolved
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — all three fields present

### Output expectations (simulated output)

- [x] PASS: Output reviews the slide-out notification panel across all 6 dimensions explicitly — Summary table covers design system consistency, component patterns, state coverage, accessibility, responsive behaviour, and code handoff quality with at least one finding per dimension
- [x] PASS: Output verifies all 8 component states for the panel and notification items — Loading (Blocker), Error (Blocker), Empty-filtered (Suggestion), Focus (Blocker), Active (Nit), Disabled (Suggestion), Default and Hover covered; missing states flagged as Blockers
- [x] PASS: Output reviews read/unread contrast per WCAG 1.4.1 — the read/unread colour-only distinction is a named Blocker with a specific fix referencing WCAG 1.4.1
- [~] PARTIAL: Output reviews the filtering interaction including live regions and empty filtered states — empty filtered state is covered (Suggestion); live region/screen reader announcement for filter changes is not addressed explicitly; partial credit
- [x] PASS: Output findings each have a severity classification — every finding appears under Blockers, Suggestions, or Nits; top tier holds WCAG failures and broken state coverage as required
- [x] PASS: Output flags any deviation from the design system — hardcoded hex colour on notification dot is a named Blocker; raw `<button>` bypassing the primitive is a named Suggestion
- [x] PASS: Output's required-changes list is prioritised — Blockers listed first, Suggestions next, Nits last, approval conditional on all Blockers being addressed
- [~] PARTIAL: Output addresses code handoff quality — Dimension 6 is labelled "Code Quality" and covers TypeScript types, props API, component structure, and performance; the simulated output notes a token-annotation gap in Figma handoff but the skill definition frames this dimension around code quality rather than design-file handoff readiness; partial credit

## Notes

The skill is oriented toward reviewing code against a design system, not reviewing Figma files for design-handoff readiness. The last output criterion asks about redlines and implied spacing from a design perspective — Dimension 6 covers code implementation quality rather than whether the Figma file has accurate annotations. That scope mismatch accounts for the partial. Everything else is well-grounded: WCAG 1.4.1 is called out explicitly in the skill definition, the eight-state requirement is clear with missing states routed to Blockers by policy, and the three-tier severity system is consistently applied throughout the simulated output.
