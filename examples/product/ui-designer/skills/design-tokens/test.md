# Test: Design tokens

Scenario: Testing whether the design-tokens skill definition requires primitive tokens, semantic tokens, contrast validation, and proper documentation structure.

## Prompt


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
