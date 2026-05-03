# Test: Design review

Scenario: Testing whether the design-review skill definition covers all six review dimensions and requires severity ratings for issues found.

## Prompt


First, set up the project by creating these files. Use Bash for mkdir, then Write for each file.

```bash
mkdir -p src/components
```

```javascript
// tailwind.config.js
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

```tsx
// src/components/NotificationPanel.tsx
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

Now:

/ui-designer:design-review of the new notification centre designs — a slide-out panel showing all user notifications with read/unread states, filtering, and bulk actions.

A few specifics for the response:

- **Six dimensions, each with its own labelled subsection** — even if no issues, write "✓ no issues found" for that dimension:
  1. Design system consistency
  2. Component patterns
  3. State coverage (all 8 states)
  4. Accessibility (WCAG)
  5. Responsive behaviour (breakpoints)
  6. Code handoff quality
- **8 component states** — review EACH explicitly (Default, Hover, Focus, Active, Disabled, Loading, Error, Empty). Missing states are **Blockers**, not Suggestions.
- **All WCAG failures are Blockers** — including 1.4.1 (semantic meaning), 1.4.3 (colour contrast). Move them out of Suggestions if the model placed them there.
- **Responsive behaviour**: review all three breakpoints — mobile (<640px), tablet (640-1024px), desktop (>1024px). Specific findings per breakpoint.
- **Design system token check**: any inline hex value (`#e5e7eb`, `#6366f1`) or non-token Tailwind utility (`bg-indigo-600` when the token is `bg-brand-600`) is a Blocker. Spacing values must be on the 4px grid.
- **Code handoff quality**: review whether spacing/colour values are measured (token-named) or implied, whether component accepts `className`, whether prop types are extensible.

## Criteria


- [ ] PASS: Skill reviews across all 6 dimensions: design system consistency, component patterns, state coverage, accessibility, responsive behaviour, and code handoff quality
- [ ] PASS: Skill requires checking all 8 component states are designed — missing states are a reviewable defect, not a follow-up item
- [ ] PASS: Skill requires accessibility to be reviewed as a constraint — WCAG failures are blocking issues, not suggestions
- [ ] PASS: Skill produces findings with severity classifications (e.g. Critical/Major/Minor, Blocking/Non-blocking, or Blockers/Suggestions/Nits) — not a flat list of comments
- [ ] PASS: Skill checks for design system consistency — components that deviate without justification are flagged
- [ ] PARTIAL: Skill reviews responsive behaviour across breakpoints — partial credit if responsiveness is listed as a dimension but specific breakpoints are not required to be checked
- [ ] PASS: Skill produces a prioritised list of required changes before approval, not just observations
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output reviews the slide-out notification panel across all 6 dimensions explicitly — design system consistency, component patterns, state coverage, accessibility, responsive behaviour, code handoff quality — with at least one finding or "no issues" per dimension
- [ ] PASS: Output verifies all 8 component states are designed for the panel and notification items — Default, Hover (on a notification row), Focus (keyboard focus), Active (clicking), Disabled, Loading (notifications fetching), Error (fetch failed), Empty (no notifications) — flagging any missing state as a blocking/major finding
- [ ] PASS: Output reviews the read/unread state contrast — unread notifications must be distinguishable from read ones with sufficient contrast (not just colour, also typography weight or icon), per WCAG 1.4.1 (not relying on colour alone)
- [ ] PARTIAL: Output reviews the filtering interaction — partial credit if live regions or screen reader announcement mechanisms are covered generally; full credit if the active filter visibility and empty filtered states are addressed specifically
- [ ] PASS: Output's findings each have a severity classification (Critical / Major / Minor, Blocking / Non-blocking, or Blockers / Suggestions / Nits) — top tier includes WCAG failures and broken state coverage; bottom tier includes spacing or visual nits
- [ ] PASS: Output flags any deviation from the design system — components that look custom but aren't documented as new primitives, colour values not in the token system, spacing not on the grid
- [ ] PASS: Output's required-changes list is prioritised — Critical findings (WCAG or broken state) listed first as blockers, Major (UX issue or system inconsistency) next, Minor (polish) last — and approval is conditional on Critical+Major being addressed
- [ ] PARTIAL: Output addresses code handoff quality — does the design include redlines / specs that engineers can implement without ambiguity, or are spacing values implied rather than measured
