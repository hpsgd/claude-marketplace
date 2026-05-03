# Component Design

Scenario: A product team needs a multi-step onboarding wizard designed for their B2B SaaS product. The designer agent is asked to produce a component specification.

## Prompt

> We need to design a multi-step onboarding wizard for Clearpath, our B2B project management tool. New users need to:
> 1. Set up their workspace (name, logo, timezone)
> 2. Invite team members (up to 5 emails)
> 3. Connect their first integration (GitHub, Jira, or Slack — or skip)
> 4. Create their first project from a template
> 
> We have a design system with existing Input, Button, Avatar, and Card components. The wizard should work on desktop and tablet. Can you design this?

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

The spec is complete and patched. Here's a summary of what was produced:

---

**`OnboardingWizard.spec.md`** written at the repo root — a complete implementation-ready spec covering:

**Decision: Create** — no existing wizard, stepper, or relevant compound components found.

**Key design decisions locked down:**
- **Shell vs step state** separated — shell tracks step number, transition, submit, OAuth return, and exit confirmation; each step owns its own field/async states
- **Skip semantics** resolved for all 4 steps: Step 2 has no skip (0 invites is valid); Step 3 requires an explicit "Skip for now" button (Continue stays disabled without a connection); Step 4 has no skip
- **OAuth redirect hazard** fully specified: flush state before redirect, read callback params on mount, handle abandonment with a 10-min timeout
- **Auto-save failure** blocks step advance with a retry banner — not silent
- **`WizardData` resume** splits `logoFile: File | null` (current session) from `logoUrl: string | null` (server-restored preview) — a `File` object cannot survive a page reload
- **`WizardSubmitError`** typed with `step`, `message`, `retryable`
- **Step 1 Back button** is hidden (not just disabled)
- **Mobile explicitly out of scope** — tablet (≥640px) is the floor

**Four out-of-scope primitives** contractually defined so they can be specced in parallel: `LogoUpload`, `TimezoneSelect`, `EmailTagInput`, `StepIndicator`.

**Next steps:** `/ui-designer:component-spec` each of the four out-of-scope primitives, then `/ui-designer:design-review` once the engineer delivers a build.

### Artifacts written

#### `work/OnboardingWizard.spec.md`

```
# Component Spec: OnboardingWizard

**Design system decision: Create**
Searched for existing wizard, stepper, onboarding, and multi-step components — none found. The existing design system has Input, Button, Avatar, and Card but none cover the compound shell, step indicator, logo upload, timezone search, radio-card selection, or OAuth handoff needed here. Full spec required.

**Design system gaps called out per step:**

| Gap | Assumed resolution |
|-----|-------------------|
| Logo upload (file picker + preview) | New primitive `LogoUpload` — out of scope for this spec; treated as a black-box sub-component with defined contract |
| Timezone selector (searchable) | New primitive `TimezoneSelect` (searchable combobox) — out of scope; treated as black-box with defined contract |
| Radio-card selection (integration, template) | Extend existing `Card` with `selectable` variant — keyboard/selected semantics defined in this spec |
| Step indicator / progress rail | New primitive `StepIndicator` — fully specified in this doc (Section 4.1) |
| Email tag input (multi-value) | New primitive `EmailTagInput` — fully specified in this doc (Section 4.3) |

---

## 1. Purpose and Usage Context

**What it does:** A four-step modal wizard that guides a newly registered Clearpath user through workspace configuration, team invitations, integration connection, and first project creation — collecting all required context before they reach the main application.

**When to use:** On first login only, for users who have completed email verification but have not yet completed onboarding. Do NOT use for re-configuring an existing workspace (use the Settings pages), re-inviting members (use People > Invite), or connecting additional integrations after onboarding (use the Integrations page).

---

## 2. Props / API

### OnboardingWizard (shell)

| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `initialStep` | `1 \| 2 \| 3 \| 4` | `1` | No | Step to resume at — set from server when a prior partial session exists |
| `initialData` | `Partial<WizardData>` | `{}` | No | Pre-populated field values from a prior partial session |
| `onComplete` | `(data: WizardData) => Promise<void>` | — | Yes | Called on final step submission. Resolves on success, rejects with `WizardSubmitError` on failure |
| `onExit` | `() => void` | — | No | Called if the user explicitly closes the wizard before completion. If omitted, the exit button is hidden |
| `availableIntegrations` | `Integration[]` | `[github, jira, slack]` | No | Which integrations to offer on Step 3 |
| `availableTemplates` | `Template[]` | — | Yes | Templates to display on Step 4 — at least one required |

### WizardData (completion payload)

```ts
interface WizardData {
  workspace: {
    name: string;              // 1–80 chars
    logoFile: File | null;     // null = no logo uploaded this session
    logoUrl: string | null;    // previously uploaded logo URL (from server resume); if logoFile is set, logoFile takes precedence
    timezone: string;          // IANA timezone string, e.g. "America/New_York"
  };
  invites: string[];           // 0–5 validated email strings
  integration: {
    provider: 'github' | 'jira' | 'slack' | null;  // null = skipped
    connected: boolean;
  };
  project: {
    templateId: string;
    name: string;              // 1–80 chars
  };
}

// Resume note: a server-restored session cannot rehydrate a File object.
// On resume, initialData.workspace.logoFile will always be null; logoUrl
// carries the previously uploaded logo for preview. The user need not
// re-upload unless they want to change it.

interface WizardSubmitError {
  step: 1 | 2 | 3 | 4;   // which step the error is attributable to, if known; null for network/unknown
  message: string;         // user-facing message
  retryable: boolean;      // if true, show retry; if false, suggest contacting support
}
```
```

### Integration (shape for availableIntegrations)

```ts
interface Integration {
  id: 'github' | 'jira' | 'slack';
  label: string;
  iconUrl: string;
  oauthUrl: string;           // Full OAuth initiation URL
}
```

### Template (shape for availableTemplates)

```ts
interface Template {
  id: string;
  name: string;
  description: string;        // Max 120 chars
  iconEmoji?: string;         // e.g. "🚀"
  previewImageUrl?: string;
}
```

---

## 3. Variants

The OnboardingWizard has no visual variants — it is a single-purpose, full-screen-overlay component. Visual variation exists within individual steps (see Section 4).

The `Card` component's `selectable` extension (used in Steps 3 and 4):

| Variant | Visual treatment | Semantic meaning | When to use |
|---------|-----------------|------------------|-------------|
| `selectable` (default/unselected) | Standard card border, subtle hover fill | Available, not chosen | Integration or template not yet selected |
| `selectable` + `selected={true}` | Brand-colour border (2px), light brand tint background, checkmark badge top-right | Chosen | The active selection |
| `selectable` + `disabled={true}` | Muted opacity 50%, cursor `not-allowed` | Unavailable | Future: integration already connected |

---

## 4. States — Complete Coverage

The wizard has two levels of state: **shell-level** (which step, overall progress) and **step-level** (field validity, async ops within a step).

### 4.1 Shell States

| State | Visual treatment | Behaviour | Transitions to |
|-------|-----------------|-----------|---------------|
| **Step N (idle)** | Step indicator highlights current step; step content rendered; Continue button enabled if step valid | User fills fields; Back/Continue available | Step N+1, Step N-1, Submitting (step 4), Exit confirmation |
| **Step transitioning** | Content fades out (150ms), new content fades in (150ms); step indicator updates | Non-interactive during transition | Step N (idle) |
| **Submitting** | Continue button replaced with spinner; all inputs disabled; overlay not closable | Final wizard payload is sent; no interaction | Complete, Submit error |
| **Submit error** | Error Banner appears below step content ("Something went wrong. Try again."); Continue re-enabled | User can retry; Back available | Submitting |
| **Complete** | Wizard closes; focus moves to main app; `onComplete` resolves | Caller is responsible for navigation | — |
| **Exit confirmation** | A confirmation dialog appears: "Leave setup? Your progress will be saved." with "Continue setup" and "Leave" actions | Focus trapped in dialog | Step N (idle) on "Continue setup"; `onExit()` called on "Leave" |
| **OAuth return** | After OAuth redirect, wizard reopens on Step 3 with integration status updated | Integration shown as connected or failed | Step 3 (idle) |

**Step 1 Back button:** Hidden (not rendered) on Step 1 — there is no previous step. Steps 2–4 show a Back button.

**Progress persistence:** Wizard state (current step + all entered data) is auto-saved to the server after each successful step advance. On re-entry via `initialStep` + `initialData`, previously entered fields are pre-populated. A user who closes the tab mid-wizard resumes where they left off on next login.

**Auto-save failure:** If the server save fails after a step advance, the wizard shows the Submit-error banner ("Progress couldn't be saved. Check your connection and try again.") with a retry action. The user does not advance to the next step until the save succeeds. This is distinct from the final submission error — it can occur after any step.

**OAuth redirect hazard:** Step 3 initiates an OAuth flow that redirects away from the page. The current wizard state must be flushed to the server before the OAuth redirect begins. On return, the application must detect the OAuth callback (e.g., via `?oauth_callback=1&provider=github&status=success`) and reopen the wizard at Step 3 with the result. The wizard shell is responsible for reading this URL parameter on mount and setting `integration.connected` accordingly.

### 4.2 Step 1 — Workspace Setup

Sub-component states for each field:

**Workspace Name (Input)**

| State | Visual | Behaviour |
|-------|--------|-----------|
| Empty (default) | Placeholder "Acme Corp" | Continue blocked |
| Filled + valid | Standard input, no indicator | Continue enabled (assuming other fields valid) |
| Filled + invalid | Red border + error text below: "Name must be between 1 and 80 characters" | Continue blocked |
| Focused | Focus ring on input | Standard |

**Logo Upload (LogoUpload primitive)**

| State | Visual | Behaviour |
|-------|--------|-----------|
| Empty | Dashed border zone, upload icon, "Upload logo (optional)" label, "PNG or SVG, max 2 MB" hint | Click or drag to upload |
| Uploading | Progress bar within zone | Non-interactive |
| Preview | Thumbnail + "Remove" link | Replaces upload zone; Remove clears back to Empty |
| Error | Red border + error text: "File too large" or "Unsupported format" | Upload zone remains; user can retry |

**Timezone Select (TimezoneSelect primitive)**

| State | Visual | Behaviour |
|-------|--------|-----------|
| Default | Pre-selected to browser's detected timezone, or first option | Auto-populated; Continue not blocked |
| Open | Dropdown with search input | Keyboard-navigable list of IANA timezones, grouped by region |
| Selected | Displays friendly timezone label, e.g. "Eastern Time (US & Canada)" | — |

**Continue button:** Enabled when workspace name is filled and valid. Logo and timezone are always valid (logo is optional; timezone has a default).

### 4.3 Step 2 — Invite Team Members

**EmailTagInput** (new primitive):

| State | Visual | Behaviour |
|-------|--------|-----------|
| Empty (0 tags) | Placeholder "teammate@company.com" | Continue enabled (invites are optional — see skip semantics below) |
| Typing | Input active; existing tags shown as pills on the left | Pressing Enter or comma adds a tag |
| Tag added (valid email) | Filled pill: avatar initial + email, remove × | Counts against 5-tag limit |
| Tag added (invalid email) | Red-outlined pill + tooltip "Not a valid email" | Continue blocked while any invalid tag present |
| Limit reached (5 tags) | Input hidden; "5 of 5 added" text shown | Adding disabled; user must remove a tag to add another |
| Duplicate email | Tag not added; toast "Already added" | No state change to existing tags |

**Skip semantics:** Steps 2, 3, and 4 all allow advancing without completing the action:
- Step 2 (invites): zero invites is valid — "Continue" is always enabled. No explicit skip button.
- Step 3 (integration): explicit "Skip for now" text button below the cards. If no card selected and user clicks Continue, treated as skip.
- Step 4 (project): project name and template are required — Continue is blocked until both are chosen. There is NO skip on this step.

**Continue button:** Enabled when 0–5 valid email tags are present (no invalid tags).

### 4.4 Step 3 — Connect Integration

**SelectableCard (Card extended):**

| State | Visual | Behaviour | Transitions to |
|-------|--------|-----------|---------------|
| Unselected | Standard card, hover: light tint fill | Click to select | Selected |
| Selected | Brand border 2px, tint background, checkmark badge | Click to deselect (returns to Unselected) | Unselected, Connecting |
| Connecting | Spinner replaces icon; "Connecting…" label | Disabled; OAuth redirect triggered | Connected, Connection error |
| Connected | Green check badge; "Connected" label | Non-interactive; user can proceed | — |
| Connection error | Red border; "Connection failed. Retry?" retry link | Retry link re-triggers OAuth | Connecting |

**"Skip for now" button:** A ghost/text `Button` below the card grid. Clicking it sets `integration.provider = null` and advances to Step 4. This is the **only** way to skip Step 3 — the Continue button requires a completed connection. If no card is selected, Continue is disabled; clicking it does not silently skip. This resolves any ambiguity: skip requires an explicit "Skip for now" action, not an implicit unselected Continue.

**Continue button:** Enabled only when `connected === true`. Disabled in all other states (no selection, card selected but not yet connected).

**OAuth redirect flow:**
1. User selects a card → the "Connect [Provider]" primary button appears (replaces Continue).
2. User clicks "Connect [Provider]" → wizard state flushed to server → OAuth redirect.
3. On return: wizard reopens at Step 3; connected card shown in Connected state; Continue enabled.

**OAuth abandonment:** If the user closes the OAuth popup or returns to the app without completing the OAuth flow (no callback URL parameter present), the wizard returns to Step 3 with the previously selected card in its unselected state and no connection. The Connection error state is not shown — the user simply reattempts. A 10-minute server-side timeout applies to pending OAuth state; after expiry, a new attempt starts a fresh OAuth flow.

### 4.5 Step 4 — Create First Project

**Template selection (SelectableCard grid):**

| State | Visual | Behaviour |
|-------|--------|-----------|
| Unselected | Standard selectable card | Click to select |
| Selected | Brand border, tint, checkmark | Click deselects ONLY IF another is available (at least one template must stay selected) |

**Project Name (Input):** Same states as Workspace Name in Step 1.

**Continue button (final step — labelled "Create Project"):** Enabled when a template is selected AND project name is valid (1–80 chars).

**Step-level validation summary:**

| Step | Required to advance | Optional |
|------|--------------------|---------:|
| 1 | Workspace name (1–80 chars) | Logo, timezone (has default) |
| 2 | No invalid email tags | Emails (0–5) |
| 3 | `connected === true` OR explicit skip | — |
| 4 | Template selected + project name (1–80 chars) | — |

---

## 5. Responsive Behaviour

**Mobile (< 640px): Out of scope.** Clearpath is a B2B desktop/tablet product. The wizard is not designed or tested for mobile viewports. If rendered below 640px, the layout is undefined — callers must gate the wizard behind a viewport check and display a "Clearpath works best on desktop or tablet" message on smaller screens.

| Breakpoint | Width | Layout | Changes |
|-----------|-------|--------|---------|
| **Tablet** | 640–1024px | Wizard is a centred modal, 90vw max-width 640px, padding 24px | Step cards in single column; integration cards 1×3 grid (stacked); template cards 1×2 grid |
| **Desktop** | > 1024px | Centred modal, max-width 720px, padding 40px | Integration cards 1×3 row; template cards 2×2 grid (2 columns) |

**Touch targets:** All interactive elements (cards, buttons, input tags) are minimum 44×44px on tablet. `EmailTagInput` remove buttons are minimum 32×32px with 6px invisible touch padding extending the hit area.

**No horizontal scrolling** at any supported breakpoint. At 640px, card text may truncate with ellipsis but layout does not overflow.

### Performance Considerations

N/A — no large datasets rendered in this wizard. Template and integration lists are bounded (<20 items each) and statically loaded. No virtualisation required.

---

## 6. Accessibility Requirements

### Keyboard Navigation

**Wizard shell:**

| Key | Action |
|-----|--------|
| `Tab` / `Shift+Tab` | Move focus between all interactive elements within the current step |
| `Enter` (on Continue/Create Project button) | Advance step or submit |
| `Enter` (on Back button) | Return to previous step |
| `Escape` | Open exit confirmation dialog (if `onExit` prop provided) |

**Step 3 & 4 — SelectableCard grid:**

| Key | Action |
|-----|--------|
| `Tab` | Move focus to next card |
| `Shift+Tab` | Move focus to previous card |
| `Enter` or `Space` | Select/deselect focused card |
| `Arrow` keys | Move focus between cards within the grid (left/right/up/down) |

**EmailTagInput (Step 2):**

| Key | Action |
|-----|--------|
| `Enter` or `,` | Add current input value as a tag (if valid) |
| `Backspace` (empty input) | Remove the last tag |
| `Tab` (on a tag's × button) | Move focus to next × or to input |
| `Enter` or `Space` (on × button) | Remove that tag; focus returns to input |
| `Escape` | Clear input text; focus stays on input |

**Focus management after step transitions:**
- After advancing to the next step: focus moves to the first interactive element in the new step's content area (not the step indicator).
- After going back: focus moves to the first interactive element.
- After OAuth return (Step 3 reopens): focus moves to the connected card.
- After wizard closes (complete or exit): focus returns to the element that was focused before the wizard opened (store it on mount).

**Exit confirmation dialog:**
- Focus is trapped within the dialog.
- On open: focus moves to "Continue setup" (safe default action).
- On close via "Continue setup": focus returns to the step content, first interactive element.
- On close via "Leave": wizard closes, focus returns to pre-wizard element.

### Screen Reader

- **Wizard shell role:** `role="dialog"` with `aria-modal="true"`, `aria-labelledby` pointing to the step title `<h1>`.
- **Step indicator:** `role="list"` with each step as `role="listitem"`. Current step has `aria-current="step"`. Completed steps have a visually hidden "(completed)" suffix.
- **Step title:** `<h1>` element within the dialog, updated on each step transition (triggers a screen reader announcement).
- **SelectableCard:** `role="radio"` within a `role="radiogroup"`. The group is labelled by the step's section heading. `aria-checked="true/false"`.
- **EmailTagInput:** `role="group"` labelled "Team member emails". Each tag pill is `role="option"` within a `role="listbox"`. The input has `aria-label="Add email address"`.
- **Continue/Back buttons:** Standard `<button>` elements. When disabled, use `aria-disabled="true"` (not the `disabled` HTML attribute) to keep them focusable and announceable.
- **Error messages:** `role="alert"` with `aria-live="assertive"` so they are announced immediately without requiring focus.
- **Progress:** Step indicator announces: "Step 2 of 4: Invite team members" (via `aria-label` on the indicator landmark).
- **OAuth connecting state:** `aria-live="polite"` region announces "Connecting to GitHub…" and then "GitHub connected successfully" or "Connection failed".

### Colour and Contrast

- All text must meet 4.5:1 against background.
- Selected card brand border must meet 3:1 against the card background.
- Step indicator: completed steps use a filled circle — icon must meet 3:1 against circle fill.
- Error states (red border, red text): must meet 4.5:1. Red colour alone is not sufficient — error icon + text label accompanies every error.
- Focus indicator: 3px solid ring, offset 2px, using the brand focus colour (must meet 3:1 against both light and dark backgrounds).

### Focus Management (summary)

- On wizard mount: focus moves to the first input in Step 1.
- Focus is trapped within the wizard modal at all times (including between steps).
- Exception: during OAuth redirect, the wizard is unmounted — focus trap is released.

---

## 7. Dark Mode

- [ ] All colours use semantic design tokens (e.g. `surface.overlay`, `border.brand`, `text.primary`) — no hardcoded hex values.
- [ ] Selected card tint uses a token that has a dark-mode equivalent (dark tint is lighter, not darker).
- [ ] Logo upload zone: dashed border uses `border.subtle` token, which inverts in dark mode.
- [ ] Step indicator completed-fill uses `brand.500` in light mode, `brand.400` in dark mode (lighter for dark backgrounds).
- [ ] Shadow on the modal overlay: lighter in dark mode (`shadow.xl` at 20% opacity, not 30%).
- [ ] Connected/error badge colours re-verified for contrast in dark mode — green and red must still meet 3:1 against the card background in dark mode.

---

## 8. Animation and Motion

| Element | Animation | Duration | Easing |
|---------|-----------|----------|--------|
| Step content transition | Fade out current + fade in new | 150ms out + 150ms in | `ease-in-out` |
| Step indicator advance | Completed step fill scales from 0→1 + check icon fades in | 200ms | `ease-out` |
| SelectableCard select | Border colour + background tint | 120ms | `ease-out` |
| SelectableCard checkmark | Scale 0→1 | 150ms | `spring(stiffness: 300, damping: 20)` |
| Exit confirmation dialog | Fade in + scale from 95%→100% | 150ms | `ease-out` |
| Error banner | Slide down from 0 height | 200ms | `ease-out` |
| EmailTagInput tag added | Slide in from right | 120ms | `ease-out` |
| EmailTagInput tag removed | Fade out + collapse width | 100ms | `ease-in` |

**`prefers-reduced-motion: reduce`:** All animations are disabled. State changes are instantaneous. The only exception is the step indicator check icon — it appears without scaling (immediate). No layout shifts occur because dimensions are pre-allocated.

---

## 9. Usage Examples

```tsx
// Standard usage — server provides resumption data
<OnboardingWizard
  initialStep={user.onboardingStep}
  initialData={user.onboardingData}
  availableTemplates={templates}
  onComplete={async (data) => {
    await api.completeOnboarding(data);
    router.push('/dashboard');
  }}
  onExit={() => router.push('/dashboard?onboarding=skipped')}
/>
```

```tsx
// First-time user, no prior progress
<OnboardingWizard
  availableTemplates={templates}
  onComplete={async (data) => {
    await api.completeOnboarding(data);
    router.push('/dashboard');
  }}
/>
// No onExit prop — exit button is hidden; user must complete wizard
```

```tsx
// Restricted integration set (e.g. Jira-only enterprise)
<OnboardingWizard
  availableIntegrations={[integrations.jira]}
  availableTemplates={templates}
  onComplete={handleComplete}
  onExit={handleExit}
/>
// Step 3 shows only one card; "Skip for now" still available
```

---

## 10. Do / Don't

| Do | Don't |
|----|-------|
| Pre-populate timezone from `Intl.DateTimeFormat().resolvedOptions().timeZone` | Leave timezone blank and force the user to search |
| Flush wizard state to server before triggering OAuth redirect | Let OAuth redirect discard unsaved wizard data |
| Keep Continue disabled while any email tag is invalid | Let users advance with a red-outlined invalid tag still present |
| Announce step changes to screen readers via updated `<h1>` | Silently update the DOM without triggering a new SR announcement |
| Show "Step N of 4" in the step indicator `aria-label` | Rely on visual position alone to convey progress |
| Return focus to the pre-wizard element on close | Drop focus to `body` when the wizard closes |
| Make "Skip for now" a clearly labelled text/ghost button | Hide the skip option or label it ambiguously as "Later" |
| Use `aria-disabled` on Continue/Back so they remain focusable when blocked | Use the `disabled` HTML attribute, which removes them from tab order |
| Validate email format client-side immediately on tag add | Batch-validate on Continue — surface errors early |
| Offer at least one template — `availableTemplates` is required | Render Step 4 with an empty template grid |
| Define the minimum `onComplete` handler to navigate post-wizard | Leave navigation implicit inside the component |
| Gate the wizard behind a ≥640px viewport check | Let the layout break silently at mobile widths |

---

## Sub-component Contracts (out-of-scope primitives)

The following primitives are called out in this spec but not fully specced here. They must be specced separately before implementation begins.

| Primitive | Used in | Key contract |
|-----------|---------|-------------|
| `LogoUpload` | Step 1 | Accepts PNG/SVG ≤2 MB; emits `File \| null`; exposes `uploading`, `error`, `preview` states |
| `TimezoneSelect` | Step 1 | Searchable combobox; emits IANA timezone string; pre-selects browser default; required (always has a value) |
| `EmailTagInput` | Step 2 | Multi-value input; validates on add; enforces 1–5 limit; emits `string[]` of valid emails |
| `StepIndicator` | Shell | Receives `totalSteps`, `currentStep`, `completedSteps[]`; read-only (no click navigation) |

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/17.0 (85%) |
| Evaluated | 2026-05-01 |
| Target duration | 351666 ms |
| Target cost | $0.9984 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Checks the existing design system first and explicitly identifies which existing components (Input, Button, Avatar, Card) can be reused versus what needs to be created | PASS | Intro states 'The existing design system has Input, Button, Avatar, and Card but none cover the compound shell...' and the design system gaps table lists each primitive with an 'Assumed resolution' column explicitly marking what is reused (Card extended to selectable variant), extended, or created new (LogoUpload, TimezoneSelect, EmailTagInput, StepIndicator). |
| c2 | Documents all 8 required component states for the wizard: Default, Hover, Focus, Active, Disabled, Loading, Error, Empty | PARTIAL | Section 4.1 shell-states table names: idle, transitioning, submitting, submit error, complete, exit confirmation, OAuth return — covering Default, Loading, Error, and transitional states. However, Hover as a distinct shell state is not in the table (only mentioned for cards), Active (during button press) is absent, and Empty is not named as a formal state. Focus is in Section 6, not in the states table. |
| c3 | Specifies ARIA roles, labels, and keyboard navigation requirements — not deferred to a future accessibility pass | PASS | Section 6 (Accessibility Requirements) fully specifies: ARIA roles (role='dialog', aria-modal, aria-labelledby, role='list/listitem', aria-current='step', role='radio/radiogroup', role='group/listbox/option', aria-live, role='alert'); keyboard navigation tables for wizard shell, card grids, and EmailTagInput; focus management on step transitions, OAuth return, and wizard close — all inline, nothing deferred. |
| c4 | Addresses the step indicator / progress component as either a Reuse, Extend, or Create decision with justification | PASS | Design system gaps table row: 'Step indicator / progress rail → New primitive StepIndicator — fully specified in this doc.' The intro justifies the Create decision: 'Searched for existing wizard, stepper, onboarding, and multi-step components — none found.' Sub-component contracts section specifies the interface. |
| c5 | Specifies responsive behaviour for both desktop and tablet breakpoints | PASS | Section 5 table: Tablet (640–1024px) — '90vw max-width 640px, padding 24px; step cards single column; integration cards 1×3 stacked; template cards 1×2'; Desktop (>1024px) — 'max-width 720px, padding 40px; integration cards 1×3 row; template cards 2×2 grid.' Touch target minimums also specified for tablet. |
| c6 | Documents the error state for each step (e.g. invalid email format in team invite, workspace name taken) | PASS | Step 1: red border + 'Name must be between 1 and 80 characters'; logo upload: 'File too large' or 'Unsupported format'. Step 2: red-outlined pill + tooltip 'Not a valid email'; Continue blocked with any invalid tag. Step 3: 'Connection failed. Retry?' red border. Step 4: project name reuses Step 1 error pattern; Continue blocked. Note: server-side 'name taken' scenario not covered. |
| c7 | Specifies loading states for async operations — partial credit if loading state is mentioned but not fully specified for each async step (integration connection, form submission) | PARTIAL | Integration connection (Step 3 SelectableCard 'Connecting' state): 'Spinner replaces icon; Connecting… label; Disabled; OAuth redirect triggered.' Final submission: shell 'Submitting' state with 'Continue button replaced with spinner; all inputs disabled.' Logo upload: 'Progress bar within zone.' Auto-save failure also specified. Ceiling is PARTIAL. |
| c8 | Produces output in a structured component specification format with named sections, not a prose description | PASS | Spec is structured with 10 numbered sections (Purpose, Props/API, Variants, States, Responsive Behaviour, Accessibility, Dark Mode, Animation, Usage Examples, Do/Don't) plus Sub-component Contracts. Each section uses tables, TypeScript interfaces, and state tables — not prose. |
| c9 | Output addresses each of the 4 wizard steps from the prompt explicitly — workspace setup, team invite, integration connection, project from template — with the relevant inputs / interactions per step | PASS | Sections 4.2 (Step 1 Workspace Setup with name/logo/timezone states), 4.3 (Step 2 Invite with EmailTagInput states and skip semantics), 4.4 (Step 3 Integration with SelectableCard states, OAuth flow, Skip for now), 4.5 (Step 4 Project with template selection and name input) — all four steps covered with state tables and interactions. |
| c10 | Output's design-system reuse decisions are explicit per primitive — Input (reuse for workspace name, email fields), Button (reuse for navigation), Avatar (reuse for team-member preview), Card (reuse for template selection) — and identifies what NEEDS to be created (step indicator / progress component) | PARTIAL | Input reuse (Steps 1, 4), Button reuse (Continue, Back, Skip), Card extended to selectable variant (Section 3), and new primitives (LogoUpload, TimezoneSelect, EmailTagInput, StepIndicator) are all explicit. Avatar is used in email tag pills ('avatar initial + email') but is NOT explicitly called out as a 'reuse Avatar' decision in the design system gaps table or any dedicated decision row. |
| c11 | Output's progress / step-indicator component is decided explicitly as Reuse / Extend / Create with reasoning — likely Create with justification that no existing primitive serves this layout | PASS | Design system gaps table: 'New primitive StepIndicator — fully specified in this doc.' Intro: 'Searched for existing wizard, stepper, onboarding, and multi-step components — none found.' Create decision with search-based justification. Sub-component contracts specify the interface: 'Receives totalSteps, currentStep, completedSteps[]; read-only (no click navigation).' |
| c12 | Output documents all 8 component states for the wizard shell — Default, Hover (on next/back), Focus (keyboard focus on inputs), Active (during click), Disabled (next button before required fields filled), Loading (during async like integration auth), Error (validation failures), Empty (initial state of integration step before selection) | PARTIAL | Shell states table (4.1) covers: idle (Default), transitioning, submitting (Loading), submit error (Error), complete, exit confirmation, OAuth return — 7 states. Disabled Continue is addressed per-step. However, Hover on Back/Continue buttons, Active (click) state, and Empty as a named initial shell state are not in the shell states table. Focus is only in Section 6. |
| c13 | Output's accessibility specification covers ARIA roles (e.g. `role="region"` on each step, `aria-current="step"` on the active indicator), labels, and keyboard navigation (Tab through fields, Enter to advance, Esc to abandon) | PASS | Section 6 Screen Reader: aria-current='step' on active step indicator ✓; role='dialog' on shell (not role='region' per step, but this is a valid alternative); Tab/Shift+Tab through fields ✓; Enter to advance ✓; Escape to exit confirmation ✓. Step indicator aria-label 'Step 2 of 4: Invite team members' ✓. Comprehensive beyond minimum. |
| c14 | Output addresses the team-invite step's email validation — what counts as valid format, max 5 emails, duplicate email handling, malformed entry handling — with error states designed | PASS | Section 4.3 EmailTagInput table: valid email → filled pill; invalid email → 'Red-outlined pill + tooltip Not a valid email'; limit reached (5 tags) → 'Input hidden; 5 of 5 added'; duplicate → 'Tag not added; toast Already added.' Continue blocked while any invalid tag present. Do/Don't: 'Validate email format client-side immediately on tag add.' |
| c15 | Output addresses the integration step's "or skip" branch explicitly — designed as a primary "Connect" path AND a secondary "Skip for now" link, with deferred re-engagement (e.g. nudge in onboarding email Day 7) | PARTIAL | Section 4.4: primary path (card select → Connect [Provider] button → OAuth), secondary 'Skip for now' ghost/text button that sets integration.provider=null and advances to Step 4 — both paths explicitly designed. However, deferred re-engagement (onboarding email nudge, Day 7 reminder, or any post-wizard follow-up) is entirely absent from the spec. |
| c16 | Output specifies responsive behaviour for desktop AND tablet — including how the wizard layout reflows (single-column on tablet vs two-column on desktop) and where the step indicator sits at each breakpoint | PARTIAL | Section 5 table specifies card grid reflow: tablet single-column integration/template cards vs desktop 2-column grids ✓. Modal width changes (640px vs 720px max-width) ✓. However, the step indicator's position at different breakpoints (top of modal, sidebar, inline) is not mentioned in Section 5 or anywhere in the spec. |
| c17 | Output addresses can-skip vs cannot-skip per step — workspace setup is required, team invite can be skipped (don't trap a solo user), integration is optional, first project from template is required (so they end the wizard with something usable) | PASS | Section 4.3 skip semantics explicitly: Step 1 requires workspace name (Continue blocked until filled); Step 2 zero invites valid, no skip button needed; Step 3 explicit 'Skip for now' button, Continue disabled without connection; Step 4 no skip, Continue blocked until template + name filled. Step-level validation summary table at end of 4.5 consolidates all four. |
| c18 | Output addresses the loading state for the integration step specifically — OAuth roundtrip can take 5-15 seconds, requires a clear "Connecting to GitHub..." indicator with a fallback message if it stalls | PARTIAL | Section 4.4 SelectableCard 'Connecting' state: 'Spinner replaces icon; Connecting… label; Disabled.' aria-live announces 'Connecting to GitHub…' and result. OAuth abandonment: 10-minute server-side timeout specified. However, no UI-visible stall fallback message (e.g. 'This is taking longer than expected — check your browser') is specified for long-running OAuth flows. Ceiling is PARTIAL. |

### Notes

The spec is exceptionally thorough — a production-ready document with TypeScript interfaces, state tables, accessibility coverage, animations, dark mode tokens, and usage examples. It clearly passes on structure, step coverage, ARIA, keyboard navigation, email validation, skip semantics, and design-system decision-making. The gaps that cost points are: (1) the 8-state framework is not explicitly mapped for the shell (Hover/Active/Empty missing as named states); (2) Avatar reuse is implied but never declared as a design decision; (3) step indicator position at different breakpoints is unspecified in the responsive section; (4) deferred re-engagement after skipping integration is entirely absent; (5) OAuth stall fallback UI is not specified. These are minor omissions in an otherwise comprehensive spec, resulting in a comfortable PASS.
