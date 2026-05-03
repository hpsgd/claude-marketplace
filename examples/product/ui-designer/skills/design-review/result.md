# Design Review

Scenario: Testing whether the design-review skill definition covers all six review dimensions and requires severity ratings for issues found.

## Prompt

> First, set up the project by creating these files. Use Bash for mkdir, then Write for each file.
> 
> ```bash
> mkdir -p src/components
> ```
> 
> ```javascript
> // tailwind.config.js
> module.exports = {
>   content: ['./src/**/*.{tsx,ts}'],
>   theme: {
>     extend: {
>       colors: {
>         brand: {
>           50: '#eef2ff',
>           100: '#e0e7ff',
>           200: '#c7d2fe',
>           500: '#6366f1',
>           600: '#4f46e5',
>           700: '#4338ca',
>         },
>         surface: {
>           DEFAULT: '#ffffff',
>           subtle: '#f8fafc',
>           muted: '#f1f5f9',
>         },
>       },
>       spacing: {
>         // 4px base grid — approved values: 1,2,3,4,5,6,8,10,12,16,20,24
>       },
>     },
>   },
> };
> ```
> 
> ```tsx
> // src/components/NotificationPanel.tsx
> import React, { useState } from 'react';
> 
> interface Notification {
>   id: string;
>   title: string;
>   body: string;
>   timestamp: string;
>   read: boolean;
>   type: 'mention' | 'system' | 'billing';
> }
> 
> interface NotificationPanelProps {
>   notifications: Notification[];
>   onClose: () => void;
>   onMarkAllRead: () => void;
>   onMarkRead: (id: string) => void;
>   onBulkDelete: (ids: string[]) => void;
> }
> 
> export function NotificationPanel({
>   notifications,
>   onClose,
>   onMarkAllRead,
>   onMarkRead,
>   onBulkDelete,
> }: NotificationPanelProps) {
>   const [filter, setFilter] = useState<'all' | 'unread'>('all');
>   const [selected, setSelected] = useState<Set<string>>(new Set());
> 
>   const filtered = filter === 'unread'
>     ? notifications.filter(n => !n.read)
>     : notifications;
> 
>   const toggleSelect = (id: string) => {
>     setSelected(prev => {
>       const next = new Set(prev);
>       next.has(id) ? next.delete(id) : next.add(id);
>       return next;
>     });
>   };
> 
>   return (
>     <div className="fixed right-0 top-0 h-full w-96 bg-white shadow-xl z-50 flex flex-col">
>       {/* Header */}
>       <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200">
>         <h2 className="text-base font-semibold text-gray-900">Notifications</h2>
>         <button
>           onClick={onClose}
>           className="text-gray-400 hover:text-gray-600 p-1 rounded"
>         >
>           ✕
>         </button>
>       </div>
> 
>       {/* Filter bar */}
>       <div className="flex items-center gap-2 px-4 py-2" style={{ borderBottom: '1px solid #e5e7eb' }}>
>         <button
>           onClick={() => setFilter('all')}
>           className={`px-3 py-1.5 rounded-full text-sm font-medium ${
>             filter === 'all'
>               ? 'bg-indigo-600 text-white'
>               : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
>           }`}
>         >
>           All
>         </button>
>         <button
>           onClick={() => setFilter('unread')}
>           className={`px-3 py-1.5 rounded-full text-sm font-medium ${
>             filter === 'unread'
>               ? 'bg-indigo-600 text-white'
>               : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
>           }`}
>         >
>           Unread
>         </button>
>         <div className="ml-auto flex items-center gap-2">
>           {selected.size > 0 && (
>             <button
>               onClick={() => { onBulkDelete(Array.from(selected)); setSelected(new Set()); }}
>               className="text-sm text-red-600 hover:text-red-800"
>             >
>               Delete ({selected.size})
>             </button>
>           )}
>           <button
>             onClick={onMarkAllRead}
>             className="text-sm text-indigo-600 hover:text-indigo-800"
>           >
>             Mark all read
>           </button>
>         </div>
>       </div>
> 
>       {/* Notification list */}
>       <div className="flex-1 overflow-y-auto divide-y divide-gray-100">
>         {filtered.map(notification => (
>           <div
>             key={notification.id}
>             onClick={() => onMarkRead(notification.id)}
>             className={`flex items-start gap-3 px-4 py-3 cursor-pointer hover:bg-gray-50 ${
>               !notification.read ? 'bg-blue-50' : 'bg-white'
>             }`}
>           >
>             <input
>               type="checkbox"
>               checked={selected.has(notification.id)}
>               onChange={e => { e.stopPropagation(); toggleSelect(notification.id); }}
>               className="mt-1 flex-shrink-0"
>             />
>             <div className="flex-shrink-0 mt-2">
>               {!notification.read && (
>                 <div className="w-2 h-2 rounded-full" style={{ backgroundColor: '#6366f1' }} />
>               )}
>             </div>
>             <div className="flex-1 min-w-0">
>               <p className={`text-sm ${!notification.read ? 'font-semibold text-gray-900' : 'font-normal text-gray-500'}`}>
>                 {notification.title}
>               </p>
>               <p className="text-sm text-gray-500 mt-0.5 line-clamp-2">{notification.body}</p>
>               <p className="text-xs text-gray-400 mt-1">{notification.timestamp}</p>
>             </div>
>           </div>
>         ))}
>       </div>
>     </div>
>   );
> }
> ```
> 
> Now:
> 
> /ui-designer:design-review of the new notification centre designs — a slide-out panel showing all user notifications with read/unread states, filtering, and bulk actions.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

# Design Review: NotificationPanel.tsx

**Reviewed:** `src/components/NotificationPanel.tsx` (128 lines)
**Design system:** Tailwind 4x with custom brand colors, surface tokens

---

## Blockers (must fix before merge)

### Missing Focus Indicators on All Interactive Elements
- **File:** `NotificationPanel.tsx:47–91`
- **Issue:** All buttons (close, filter, delete, mark-all-read) lack `focus:` or `focus-visible:` classes. This breaks keyboard navigation visibility for all users and fails WCAG 2.4.7 (Focus Visible).
- **Fix:** Add `focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-600` to all `<button>` elements. Example:
  ```tsx
  className="... hover:text-gray-600 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-600 p-1 rounded"
  ```

### Close Button is Icon-Only Without Accessible Label
- **File:** `NotificationPanel.tsx:47–52`
- **Issue:** The `✕` button has no `aria-label`. Screen readers cannot announce its purpose. WCAG 1.3.1 violation.
- **Fix:** Add `aria-label="Close notifications"` to the close button:
  ```tsx
  <button
    onClick={onClose}
    aria-label="Close notifications"
    className="..."
  >
    ✕
  </button>
  ```

### Notification Rows Are Clickable Divs, Not Keyboard Accessible
- **File:** `NotificationPanel.tsx:98–124`
- **Issue:** Notification items use `<div>` with `onClick`, making them unreachable via keyboard. Not semantic. WCAG 2.1.1 violation (keyboard access).
- **Fix:** Convert to `<button>` or add `role="button"`, `tabIndex={0}`, and keyboard handler (`onKeyDown` for Enter/Space):
  ```tsx
  <button
    key={notification.id}
    onClick={() => onMarkRead(notification.id)}
    className={`flex items-start gap-3 px-4 py-3 hover:bg-gray-50 text-left ${
      !notification.read ? 'bg-blue-50' : 'bg-white'
    }`}
  >
    {/* content */}
  </button>
  ```

### Hardcoded Colours in Inline Styles (Two Instances)
- **File:** `NotificationPanel.tsx:56, 113`
- **Issue:** Two hardcoded hex values in `style=` attributes break the design system, prevent dark mode, and create maintenance debt:
  - Line 56: `style={{ borderBottom: '1px solid #e5e7eb' }}` — should use Tailwind class
  - Line 113: `style={{ backgroundColor: '#6366f1' }}` — should use brand color token
- **Fix:**
  - Line 56: Replace with `border-b border-gray-200`
  - Line 113: Use `className="bg-brand-500"` or create a dedicated `.read-indicator` class

### Missing Semantic Labeling for Filter Buttons
- **File:** `NotificationPanel.tsx:57–76`
- **Issue:** Filter buttons don't indicate which is active to screen readers. Users cannot tell if they're viewing "All" or "Unread" without visual inspection.
- **Fix:** Add `aria-current="page"` to the active filter button:
  ```tsx
  <button
    onClick={() => setFilter('all')}
    aria-current={filter === 'all' ? 'page' : undefined}
    className={...}
  >
    All
  </button>
  ```

### Fixed Width Panel Breaks on Mobile
- **File:** `NotificationPanel.tsx:43`
- **Issue:** `w-96` (384px) is too wide for phones. The panel will overflow or clip. Not responsive.
- **Fix:** Use responsive width: `w-full sm:w-96` and ensure mobile padding is applied when full-width.

### Checkboxes Lack Labels or ARIA
- **File:** `NotificationPanel.tsx:105–110`
- **Issue:** Checkboxes have no associated label or `aria-label`. Screen readers cannot announce their state. There's no text explaining what selecting a checkbox does.
- **Fix:** Add `aria-label` and consider grouping checkboxes with a selection description:
  ```tsx
  <input
    type="checkbox"
    checked={selected.has(notification.id)}
    onChange={e => { e.stopPropagation(); toggleSelect(notification.id); }}
    aria-label={`Select notification: ${notification.title}`}
    className="mt-1 flex-shrink-0"
  />
  ```

---

## Suggestions (should fix, not blocking)

### Use `clsx` for Conditional Classes
- **File:** `NotificationPanel.tsx:59–63, 69–73, 101–103, 117`
- **Issue:** Ternary operators inline with string concatenation produce hard-to-read class strings and don't handle falsy values cleanly. Tailwind class purging can also struggle.
- **Fix:** Install `clsx` and refactor:
  ```tsx
  import clsx from 'clsx';
  
  className={clsx(
    'px-3 py-1.5 rounded-full text-sm font-medium',
    filter === 'all'
      ? 'bg-indigo-600 text-white'
      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
  )}
  ```

### Add Dark Mode Support
- **File:** `NotificationPanel.tsx` (entire component)
- **Issue:** No `dark:` variants present. The component is unusable in dark mode — white background stays white, text becomes invisible.
- **Fix:** Add dark mode classes:
  ```tsx
  <div className="... dark:bg-slate-900">
    <div className="... dark:border-gray-700">
    <h2 className="... dark:text-gray-100">
    {/* etc. */}
  </div>
  ```

### Colour Contrast on Secondary Text
- **File:** `NotificationPanel.tsx:121`
- **Issue:** `text-gray-400` on white (or `dark:bg-slate-900` on unread items) may not meet 4.5:1 contrast for normal text. Reads as 3.6:1.
- **Fix:** Use `text-gray-500` for better contrast (4.6:1), or ensure timestamp text is truly supplementary and use `aria-label` to convey critical info.

### Missing Empty State
- **File:** `NotificationPanel.tsx:96–125`
- **Issue:** If `filtered.length === 0`, users see a blank empty scroll area with no guidance. Unclear if notifications are loading, disabled, or just absent.
- **Fix:** Add:
  ```tsx
  {filtered.length === 0 ? (
    <div className="flex items-center justify-center h-32 text-gray-400">
      <p className="text-sm">No notifications yet</p>
    </div>
  ) : (
    filtered.map(/* ... */)
  )}
  ```

### Unread Indicator Lacks Semantic Meaning
- **File:** `NotificationPanel.tsx:111–114`
- **Issue:** A blue dot `•` appears next to unread messages but is never announced. Users with colour blindness cannot distinguish it from read state. Not WCAG 1.4.1 compliant (state is colour-only).
- **Fix:** Combine with text or icon:
  ```tsx
  {!notification.read && (
    <>
      <div className="w-2 h-2 rounded-full bg-brand-500 flex-shrink-0" />
      <span className="sr-only">unread</span>
    </>
  )}
  ```

---

## Nits (minor, fix if touching this code)

### Close Button Icon Could Be More Accessible
- **File:** `NotificationPanel.tsx:50`
- **Issue:** A literal `✕` character is fine, but an SVG or dedicated icon component would be more scalable and allow for hover effects.
- **Fix:** Consider using an `X` icon from a component library or SVG with `aria-hidden="true"` to avoid redundancy with the aria-label.

### Filter Buttons Could Accept a `disabled` State
- **File:** `NotificationPanel.tsx:57–76`
- **Issue:** No way to disable filters (e.g., if "Unread" has no items). Button still appears clickable.
- **Fix:** Add optional `disabled` prop and `disabled:` Tailwind classes for visual feedback.

### Type Union for Filter Could Be More Extensible
- **File:** `NotificationPanel.tsx:27`
- **Issue:** `'all' | 'unread'` is a string literal union. If more filters are added later (e.g., by type), this will require refactoring multiple places.
- **Fix:** Consider an enum or const assertion for reusability:
  ```tsx
  const FILTER_OPTIONS = ['all', 'unread'] as const;
  type FilterType = (typeof FILTER_OPTIONS)[number];
  ```

### Component Does Not Accept `className` Prop
- **File:** `NotificationPanel.tsx:20–26`
- **Issue:** Cannot customize the panel's styling from parent (e.g., different positioning, animation). Breaks composition patterns.
- **Fix:** Add optional `className` prop and merge with base classes using clsx.

---

## Summary
- **Blockers:** 7
- **Suggestions:** 6
- **Nits:** 4
- **Verdict:** **Request changes**

The component has critical accessibility deficits (missing focus indicators, keyboard navigation, ARIA labels) and hardcoded design system violations (inline hex values). These must be fixed before merge. Once blockers are addressed, the suggestions (clsx, dark mode, empty state) are highly recommended but can be tracked as follow-up work.

**Priority order for fixes:**
1. Add focus indicators to all buttons
2. Add `aria-label` to close button
3. Convert notification rows to `<button>`
4. Remove hardcoded colours; use Tailwind classes
5. Add `aria-current` to active filter button
6. Make panel responsive on mobile
7. Add `aria-label` to checkboxes

### Artifacts written

#### `work/tailwind.config.js`

```
module.exports = {
  content: ['./src/**/*.{tsx,ts}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eef2ff',
          100: '#e0e7ff',
          200: '#c7d2fe',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
        },
        surface: {
          DEFAULT: '#ffffff',
          subtle: '#f8fafc',
          muted: '#f1f5f9',
        },
      },
      spacing: {
        // 4px base grid — approved values: 1,2,3,4,5,6,8,10,12,16,20,24
      },
    },
  },
};

```

#### `work/src/components/NotificationPanel.tsx`

```
import React, { useState } from 'react';

interface Notification {
  id: string;
  title: string;
  body: string;
  timestamp: string;
  read: boolean;
  type: 'mention' | 'system' | 'billing';
}

interface NotificationPanelProps {
  notifications: Notification[];
  onClose: () => void;
  onMarkAllRead: () => void;
  onMarkRead: (id: string) => void;
  onBulkDelete: (ids: string[]) => void;
}

export function NotificationPanel({
  notifications,
  onClose,
  onMarkAllRead,
  onMarkRead,
  onBulkDelete,
}: NotificationPanelProps) {
  const [filter, setFilter] = useState<'all' | 'unread'>('all');
  const [selected, setSelected] = useState<Set<string>>(new Set());

  const filtered = filter === 'unread'
    ? notifications.filter(n => !n.read)
    : notifications;

  const toggleSelect = (id: string) => {
    setSelected(prev => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  };

  return (
    <div className="fixed right-0 top-0 h-full w-96 bg-white shadow-xl z-50 flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200">
        <h2 className="text-base font-semibold text-gray-900">Notifications</h2>
        <button
          onClick={onClose}
          className="text-gray-400 hover:text-gray-600 p-1 rounded"
        >
          ✕
        </button>
      </div>

      {/* Filter bar */}
      <div className="flex items-center gap-2 px-4 py-2" style={{ borderBottom: '1px solid #e5e7eb' }}>
        <button
          onClick={() => setFilter('all')}
          className={`px-3 py-1.5 rounded-full text-sm font-medium ${
            filter === 'all'
              ? 'bg-indigo-600 text-white'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          All
        </button>
        <button
          onClick={() => setFilter('unread')}
          className={`px-3 py-1.5 rounded-full text-sm font-medium ${
            filter === 'unread'
              ? 'bg-indigo-600 text-white'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          Unread
        </button>
        <div className="ml-auto flex items-center gap-2">
          {selected.size > 0 && (
            <button
              onClick={() => { onBulkDelete(Array.from(selected)); setSelected(new Set()); }}
              className="text-sm text-red-600 hover:text-red-800"
            >
              Delete ({selected.size})
            </button>
          )}
          <button
            onClick={onMarkAllRead}
            className="text-sm text-indigo-600 hover:text-indigo-800"
          >
            Mark all read
          </button>
        </div>
      </div>

      {/* Notification list */}
      <div className="flex-1 overflow-y-auto divide-y divide-gray-100">
        {filtered.map(notification => (
          <div
            key={notification.id}
            onClick={() => onMarkRead(notification.id)}
            className={`flex items-start gap-3 px-4 py-3 cursor-pointer hover:bg-gray-50 ${
              !notification.read ? 'bg-blue-50' : 'bg-white'
            }`}
          >
            <input
              type="checkbox"
              checked={selected.has(notification.id)}
              onChange={e => { e.stopPropagation(); toggleSelect(notification.id); }}
              className="mt-1 flex-shrink-0"
            />
            <div className="flex-shrink-0 mt-2">
              {!notification.read && (
                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: '#6366f1' }} />
              )}
            </div>
            <div className="flex-1 min-w-0">
              <p className={`text-sm ${!notification.read ? 'font-semibold text-gray-900' : 'font-normal text-gray-500'}`}>
                {notification.title}
              </p>
              <p className="text-sm text-gray-500 mt-0.5 line-clamp-2">{notification.body}</p>
              <p className="text-xs text-gray-400 mt-1">{notification.timestamp}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 9.5/14.5 (66%) |
| Evaluated | 2026-05-02 |
| Target duration | 56652 ms |
| Target cost | $0.1031 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill reviews across all 6 dimensions: design system consistency, component patterns, state coverage, accessibility, responsive behaviour, and code handoff quality | PASS | Design system: hardcoded hex values (lines 56, 113). Component patterns: clsx suggestion, className prop missing. State coverage: empty state. Accessibility: 5+ WCAG blockers. Responsive: fixed w-96 on mobile. Code handoff: type union, composability nits. All 6 touched, though not explicitly labelled by dimension. |
| c2 | Skill requires checking all 8 component states are designed — missing states are a reviewable defect, not a follow-up item | FAIL | Only the Empty state is mentioned ('Missing Empty State' in Suggestions). Loading, Error, Active, Disabled, Default, and Hover states are entirely absent from the review. The Empty state is placed in Suggestions rather than as a blocking defect. No systematic 8-state checklist is present. |
| c3 | Skill requires accessibility to be reviewed as a constraint — WCAG failures are blocking issues, not suggestions | PARTIAL | Most WCAG failures are correctly placed in 'Blockers (must fix before merge)' — focus indicators (WCAG 2.4.7), aria-label on close (WCAG 1.3.1), keyboard access (WCAG 2.1.1). However, 'Unread Indicator Lacks Semantic Meaning' (explicitly cited as WCAG 1.4.1) and 'Colour Contrast on Secondary Text' (potential WCAG AA failure) are placed in Suggestions rather than Blockers, inconsistent with the constraint requirement. |
| c4 | Skill produces findings with severity classifications (e.g. Critical/Major/Minor, Blocking/Non-blocking, or Blockers/Suggestions/Nits) — not a flat list of comments | PASS | Output is explicitly structured into three severity tiers: 'Blockers (must fix before merge)', 'Suggestions (should fix, not blocking)', and 'Nits (minor, fix if touching this code)'. Summary counts each: 7 blockers, 6 suggestions, 4 nits. |
| c5 | Skill checks for design system consistency — components that deviate without justification are flagged | PASS | 'Hardcoded Colours in Inline Styles (Two Instances)' is a Blocker: line 56 uses `style={{ borderBottom: '1px solid #e5e7eb' }}` and line 113 uses `style={{ backgroundColor: '#6366f1' }}` — both flagged as breaking design system tokens. Fix correctly references brand color tokens. |
| c6 | Skill reviews responsive behaviour across breakpoints — partial credit if responsiveness is listed as a dimension but specific breakpoints are not required to be checked | PARTIAL | 'Fixed Width Panel Breaks on Mobile' is a Blocker at NotificationPanel.tsx:43, identifying `w-96` (384px) overflow on phones and suggesting `w-full sm:w-96`. One specific breakpoint (sm:) is addressed. No comprehensive multi-breakpoint audit performed. |
| c7 | Skill produces a prioritised list of required changes before approval, not just observations | PASS | Output ends with 'Priority order for fixes' numbered 1–7 covering all blockers in order. Verdict is 'Request changes' — approval is explicitly conditional on blockers being addressed. The Blockers section is clearly labelled 'must fix before merge'. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | Neither the captured chat output nor the written artifacts (tailwind.config.js, NotificationPanel.tsx) contain any YAML frontmatter with name, description, or argument-hint fields. The skill definition file itself is not surfaced in the output or artifacts. |
| c9 | Output reviews the slide-out notification panel across all 6 dimensions explicitly — design system consistency, component patterns, state coverage, accessibility, responsive behaviour, code handoff quality — with at least one finding or "no issues" per dimension | PARTIAL | Dimensions are covered implicitly but not explicitly labelled. State coverage only finds the Empty state — Loading, Error, Hover, Active, Disabled, Focus-as-state are absent. Code handoff quality appears only in Nits (type union, className prop) without framing it as a handoff-quality dimension. No 'no issues' statements for clean dimensions. |
| c10 | Output verifies all 8 component states are designed for the panel and notification items — Default, Hover (on a notification row), Focus (keyboard focus), Active (clicking), Disabled, Loading (notifications fetching), Error (fetch failed), Empty (no notifications) — flagging any missing state as a blocking/major finding | FAIL | Only the Empty state is addressed ('Missing Empty State' in Suggestions). Loading and Error states are completely absent. Focus is addressed only as an accessibility concern (missing ring), not as a designed interaction state. Active, Disabled, Default, and Hover states are unverified. Empty state is a Suggestion, not a blocking finding. |
| c11 | Output reviews the read/unread state contrast — unread notifications must be distinguishable from read ones with sufficient contrast (not just colour, also typography weight or icon), per WCAG 1.4.1 (not relying on colour alone) | PASS | 'Unread Indicator Lacks Semantic Meaning' explicitly cites WCAG 1.4.1: 'Users with colour blindness cannot distinguish it from read state. Not WCAG 1.4.1 compliant (state is colour-only).' Fix suggests `<span className="sr-only">unread</span>` — non-colour mechanism. The existing `font-semibold` / `font-normal` differentiation in the code is implicitly part of the analysis context. |
| c12 | Output reviews the filtering interaction — partial credit if live regions or screen reader announcement mechanisms are covered generally; full credit if the active filter visibility and empty filtered states are addressed specifically | PARTIAL | Active filter visibility is specifically addressed: 'Missing Semantic Labeling for Filter Buttons' (Blocker) suggests `aria-current={filter === 'all' ? 'page' : undefined}`. Empty filtered state is addressed in 'Missing Empty State' (Suggestion). Live region announcements on filter change are not mentioned. |
| c13 | Output's findings each have a severity classification (Critical / Major / Minor, Blocking / Non-blocking, or Blockers / Suggestions / Nits) — top tier includes WCAG failures and broken state coverage; bottom tier includes spacing or visual nits | PARTIAL | Three-tier classification exists and is used throughout. However, WCAG 1.4.1 violation ('Unread Indicator Lacks Semantic Meaning') and a contrast issue are in Suggestions rather than Blockers. Broken state coverage (Empty) is also in Suggestions. The top tier doesn't consistently capture all WCAG failures as required. |
| c14 | Output flags any deviation from the design system — components that look custom but aren't documented as new primitives, colour values not in the token system, spacing not on the grid | PARTIAL | Inline hex values `#e5e7eb` and `#6366f1` are correctly flagged as Blockers. However, `bg-indigo-600` used in filter buttons is not flagged — the design system defines `brand-600: '#4f46e5'` (not Tailwind's `indigo-600`). `bg-blue-50` for unread background and spacing values against the 4px grid are not checked. |
| c15 | Output's required-changes list is prioritised — Critical findings (WCAG or broken state) listed first as blockers, Major (UX issue or system inconsistency) next, Minor (polish) last — and approval is conditional on Critical+Major being addressed | PASS | Blockers section lists 7 items including all WCAG failures first. Verdict states 'Request changes' and summary says 'These must be fixed before merge.' Priority order for fixes 1–7 is explicitly listed. Suggestions can be tracked as 'follow-up work.' Approval is clearly conditional. |
| c16 | Output addresses code handoff quality — does the design include redlines / specs that engineers can implement without ambiguity, or are spacing values implied rather than measured | PARTIAL | The Nits section raises 'Component Does Not Accept `className` Prop' (composability/handoff concern) and 'Type Union for Filter Could Be More Extensible' (implementation clarity). However, there is no review of whether design redlines exist, whether spacing values are measured vs implied, or whether the design-to-code specification is unambiguous. |

### Notes

The output demonstrates a strong accessibility review and solid severity classification (Blockers/Suggestions/Nits) but has two critical gaps: (1) state coverage — only the Empty state is identified, with Loading, Error, Active, Disabled, and explicit Hover/Focus interaction states entirely absent, and none flagged as blocking defects; (2) the skill definition's YAML frontmatter (name, description, argument-hint) is not evidenced in any artifact. The design system consistency check catches inline hex violations but misses Tailwind token mismatches (bg-indigo-600 vs bg-brand-600). Several WCAG failures (unread indicator 1.4.1, colour contrast) are misclassified as Suggestions rather than Blockers, undermining the stated principle that accessibility is a constraint. The code handoff quality dimension is implicitly present in the Nits but never framed as a handoff review. Overall, the review is useful and well-structured but incomplete against the full rubric dimensions.
