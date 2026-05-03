# Test: Design tokens

Scenario: Testing whether the design-tokens skill definition requires primitive tokens, semantic tokens, contrast validation, and proper documentation structure.

## Prompt

First, create CSS files with the hardcoded values scattered across the product:

```bash
mkdir -p src/styles src/components
```

Write to `src/styles/global.css`:

```css
/* Global styles — hardcoded values everywhere */
body {
  font-family: Inter, -apple-system, sans-serif;
  font-size: 16px;
  color: #1a1a2e;
  background: #ffffff;
}

a { color: #3b82f6; }
a:hover { color: #2563eb; }

.btn-primary {
  background: #3b82f6;
  color: #ffffff;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
  padding: 8px 16px;
  border-radius: 6px;
}

.btn-danger {
  background: #ef4444;
  color: #ffffff;
  padding: 8px 16px;
  border-radius: 6px;
}

h1 { font-size: 32px; font-weight: 700; color: #111827; margin-bottom: 24px; }
h2 { font-size: 24px; font-weight: 600; color: #111827; margin-bottom: 16px; }
h3 { font-size: 20px; font-weight: 600; color: #374151; margin-bottom: 12px; }
```

Write to `src/styles/sidebar.css`:

```css
.sidebar {
  width: 240px;
  background: #1e293b;
  padding: 24px 0;
}

.sidebar-item {
  padding: 10px 20px;
  color: #94a3b8;
  font-size: 14px;
}

.sidebar-item:hover { background: #334155; color: #ffffff; }
.sidebar-item.active { background: #3b82f6; color: #ffffff; }

.sidebar-badge {
  background: #ef4444;
  color: #ffffff;
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 10px;
}
```

Write to `src/components/card.css`:

```css
.card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.card-header {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e5e7eb;
}

.card-footer {
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid #e5e7eb;
  color: #6b7280;
  font-size: 13px;
}

.status-badge-success { background: #dcfce7; color: #166534; padding: 4px 8px; border-radius: 4px; font-size: 12px; }
.status-badge-warning { background: #fef9c3; color: #854d0e; padding: 4px 8px; border-radius: 4px; font-size: 12px; }
.status-badge-error   { background: #fee2e2; color: #991b1b; padding: 4px 8px; border-radius: 4px; font-size: 12px; }
```

Then run:

/ui-designer:design-tokens for our product — we currently have hardcoded hex values and pixel values scattered across our Figma files and CSS, with no token system.

## Criteria


- [ ] PASS: Skill distinguishes between primitive tokens (raw values: color-blue-500) and semantic tokens (purpose-named: color-action-primary) as separate layers
- [ ] PASS: Skill requires an inventory step — cataloguing existing values before defining tokens
- [ ] PASS: Skill requires contrast ratio validation for colour tokens against WCAG AA thresholds (4.5:1 for normal text, 3:1 for large text)
- [ ] PASS: Skill requires token documentation that specifies the intended use case, not just the value
- [ ] PASS: Skill covers at minimum colour, typography, and spacing token categories
- [ ] PARTIAL: Skill specifies a naming convention for tokens — partial credit if naming is mentioned as important but no specific convention is required
- [ ] PASS: Skill produces output that is usable by both designers (Figma) and developers (CSS custom properties or equivalent) — not just one audience
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output's inventory step lists existing hardcoded values catalogued from Figma + CSS — at least colour values, spacing values, font families, font sizes — so the team sees the scope before designing the token layer
- [ ] PASS: Output structures tokens in two layers — primitive tokens (raw values: `color-blue-500: #3b82f6`, `space-4: 16px`) AND semantic tokens (purpose-named: `color-action-primary: {color-blue-500}`, `space-stack-md: {space-4}`) — and explains why both layers exist
- [ ] PASS: Output's colour tokens include contrast-ratio validation — every text-on-background pair tested against WCAG AA (4.5:1 normal text, 3:1 large text), with the actual ratio shown and any failing pairs flagged
- [ ] PASS: Output covers at minimum colour, typography (font families, sizes, line heights, weights), and spacing token categories — and ideally radius, shadow, and motion durations
- [ ] PASS: Output's token names follow a consistent naming convention — e.g. `<category>-<role>-<scale>` like `color-action-primary` or `space-stack-md` — with the convention stated explicitly, not arbitrary mixing
- [ ] PASS: Output's documentation per token includes intended use case — "use `color-action-primary` for primary CTA buttons; do NOT use for secondary actions" — not just the value
- [ ] PASS: Output is dual-format — Figma library structure (collections, modes for light/dark if applicable) AND code (CSS custom properties, SCSS variables, or design-tokens-spec JSON / Tokens Studio) — usable by both audiences
- [ ] PASS: Output addresses dark mode or theming — semantic tokens enable theme switching by remapping their primitive references; the tokens are theme-aware even if only one theme is built initially
- [ ] PASS: Output's migration plan covers rolling out tokens to existing Figma files and CSS — incrementally replacing hex values with token references, not a big-bang switch
- [ ] PARTIAL: Output addresses tokens for state changes (hover, focus, active, disabled) — these are typically derived from the base colour token via opacity or contrast adjustments, with the relationship documented
