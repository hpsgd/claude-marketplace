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
> 
> A few specifics for the response:
> 
> - Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
> - Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
> - For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
> - When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
> - Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Based on my search of the codebase, I found **no existing wizard or multi-step form components**. I'll proceed with a **Create decision** and write a comprehensive specification for a new Wizard component that composes the existing Input, Button, Avatar, and Card components.

---

# Onboarding Wizard Component Specification

## 0. Design System Decision

**Decision: Create** — No existing wizard, stepper, or multi-step form component found in the design system. The existing Input, Button, Avatar, and Card components will be composed into a new Wizard component. This is a compound component that orchestrates form steps, progress tracking, and navigation.

---

## 1. Purpose and Usage Context

**What:** A guided multi-step form that walks users through configuration tasks sequentially, with progress indication, validation, and navigation controls.

**When to use:** For onboarding flows where users must complete sequential setup tasks (workspace configuration, team setup, integrations). Each step has distinct validation and dependencies. Do NOT use for: simple linear questionnaires (use a single-page form with sections), confirmation dialogs (use Modal), or non-sequential processes (use tabbed interface).

---

## 2. Props / API

| Prop | Type | Default | Required | Description |
|---|---|---|---|---|
| `steps` | `WizardStep[]` | — | Yes | Array of step definitions. Each step must have `id`, `title`, `subtitle`, and `render` function |
| `initialStep` | `string` | First step's ID | No | ID of the step to show on mount |
| `onComplete` | `(data: Record<string, any>) => void` | — | Yes | Called when user completes all steps. Receives all step data |
| `onCancel` | `() => void` | — | No | Called when user clicks Cancel. If omitted, Cancel button is hidden |
| `canSkipSteps` | `boolean` | `false` | No | Whether user can skip forward to later steps without completing earlier ones |
| `showProgress` | `boolean` | `true` | No | Whether to display progress indicator (step counter, progress bar) |
| `variant` | `'modal' \| 'fullpage'` | `'modal'` | No | Modal displays in a centered dialog; fullpage spans the viewport |
| `title` | `string` | — | No | Wizard title shown at the top (optional override for header) |

**Step Configuration:**

```typescript
interface WizardStep {
  id: string;                                    // Unique identifier for the step
  title: string;                                 // Step heading (e.g., "Set up your workspace")
  subtitle?: string;                             // Optional secondary text or description
  render: (data: Record<string, any>, 
           setData: (updates: Partial<Record<string, any>>) => void) => ReactNode;  // Render function
  validate?: (data: Record<string, any>) => boolean | string;  // Validation; return true if valid, string if invalid (error message)
  allowSkip?: boolean;                           // If true, user can skip this step (shows "Skip" button alongside "Next")
  onEnter?: (data: Record<string, any>) => void; // Called when step becomes active
  onExit?: (data: Record<string, any>) => void;  // Called when step is left
}
```

---

## 3. Variants

| Variant | Visual treatment | When to use |
|---------|-----------------|-------------|
| **Modal** (default) | Dialog centered on screen, dark overlay, fixed width (600px desktop, 90vw tablet) | Onboarding flows where the user should focus solely on setup. Standard for B2B tools. |
| **Fullpage** | Steps fill the viewport, no dialog container. Header bar with branding/logo space | Multi-step setup processes where users may need to reference external info (email clients for invites, browser tabs for integrations). Rare. |

---

## 4. States — Complete Coverage Table

| State | Visual treatment | Behaviour | Transitions to |
|-------|-----------------|-----------|---------------|
| **Step loading** | Skeleton loaders for form fields; spinner if `onEnter` is async | Form fields disabled, Next/Skip buttons disabled | Step ready |
| **Step ready** | All form fields interactive, visible | User can interact with form, focus management active | Step validating |
| **Step validating** | Form maintains appearance, Next button shows spinner | User cannot submit while validation runs | Step valid or Step invalid |
| **Step valid** | Next button enabled with checkmark icon (brief), then standard appearance | User can proceed or remain on step | Next step active |
| **Step invalid** | Red error text below the first invalid field; error icon; field border highlight in error colour | User cannot proceed. Error message guides correction | Step valid (after user corrects) |
| **Step skipped** | Checkmark + "Skipped" label in progress indicator | Data for this step is not collected | Next step active |
| **Completion screen** | Success icon, confirmation message, CTA button ("Go to workspace", "View settings") | No further wizard interaction; user is guided toward next action | — |

**Sub-step states (within a form step):**
- **Field focus:** Field has focus ring (dark mode: lighter ring; light mode: standard ring)
- **Field error:** Red border, error icon, error message text below
- **Field filled:** Input has content, visual indicator subtle (text colour change, no outline colour change to avoid confusion with focus)

**Compound states:**
- **Validating + error:** Validation runs; if it fails, error state shows immediately
- **Skipped step + next step validation depends on it:** If step B depends on data from step A (which was skipped), the dependency is noted. Step B's validation accounts for missing data.

---

## 5. Responsive Behaviour

| Breakpoint | Width | Layout changes | Content changes |
|-----------|-------|---------------|----------------|
| **Tablet** | 640-1024px | Modal width: 90vw, max 600px; form fields stack vertically; button group spans full width; `gap: 12px` | All form labels visible; validation text may wrap |
| **Desktop** | >1024px | Modal width: 600px fixed; form fields in grid (2-col where appropriate); button group: Next/Skip left, Cancel right | Full-width form labels; validation text on single line |

**Specific responsive rules:**
- Touch targets (inputs, buttons) minimum 44x44px at all breakpoints
- No horizontal scroll at 640px viewport width
- Form fields must remain usable at 320px width (mobile, but not primary target)
- Progress indicator (step counter) must fit in header without wrapping
- Modal overlay visible on both breakpoints

---

## 6. Accessibility Requirements

### Keyboard Navigation

| Key | Action |
|-----|--------|
| `Tab` | Move focus to next interactive element (form field → Next button → Cancel button). Focus order: top-to-bottom, left-to-right |
| `Shift+Tab` | Move focus backward through interactive elements |
| `Enter` | Submit focused button (Next, Skip, Cancel, Complete) |
| `Space` | Activate focused button (same as Enter for buttons; for checkboxes/radios within a step, toggle selection) |
| `Escape` | Close wizard, call `onCancel`. Modal only — fullpage variant ignores Escape |

**Focus management:**
- On step entry: focus moves to the first form field (or to the "Next" button if all fields are pre-filled)
- After step completion: focus moves to the header of the next step
- On wizard completion: focus moves to the completion screen's primary CTA button

### Screen Reader

- **Role:** `role="dialog"` (modal variant) or `role="main"` (fullpage variant)
- **Label:** `aria-label="Clearpath onboarding wizard"` or `aria-labelledby` pointing to the wizard title
- **Progress announcement:** Progress indicator region uses `aria-live="polite"` and announces "Step 2 of 4: Invite team members"
- **Step heading:** Each step heading uses `<h2>` or `aria-level="2"` with `aria-current="step"` attribute
- **Form validation:** Error messages use `aria-invalid="true"` on the field and `aria-describedby` pointing to the error text
- **Button states:** Next button has `aria-disabled="true"` when validation fails, preventing screen reader activation

### Colour and Contrast

- Text-to-background contrast: 4.5:1 minimum (normal text, form labels)
- Error text (red) against background: 4.5:1 minimum
- Progress indicator bar: 3:1 minimum contrast against background
- Focus ring: 3:1 minimum contrast against all adjacent colours (light mode: dark ring; dark mode: light ring)
- Icons alone do not convey state — always pair with text (error icon + error message, success icon + checkmark text)

### Focus Management (Modal variant)

- Focus trap enabled: `Tab` within the modal cycles through form fields and buttons without leaving the modal
- `Escape` key closes the modal and returns focus to the trigger element (if applicable; in this case, focus returns to the page's main content area)
- Initial focus: first form field on step load, or first interactive button if all fields are disabled

---

## 7. Dark Mode

- [ ] All colours use semantic tokens (e.g., `color-text-primary`, `color-bg-surface`, `color-border-default`), not hardcoded values
- [ ] Error state (red) uses dark-mode-safe error token — verify 4.5:1 contrast against dark background
- [ ] Focus ring colour adjusted for dark background (lighter ring, not darker)
- [ ] Modal backdrop uses semi-transparent overlay that works in both modes (dark mode: lighter overlay, light mode: darker overlay)
- [ ] Form input backgrounds: light mode uses white or light grey; dark mode uses darker grey (not black, to maintain hierarchy)
- [ ] Shadows on modal: dark mode uses subtle shadows (less aggressive than light mode)

---

## 8. Animation and Motion

**Transition between steps:**
- Fade duration: 200ms (ease: `ease-in-out`)
- On "Next": current step fades out, next step fades in
- Loading spinners: smooth rotation at 1 rotation per 2 seconds
- Success checkmark: quick bounce/scale (100ms, cubic-bezier(0.68, -0.55, 0.265, 1.55)) on completion

**Entry/exit animations:**
- Modal entry: fade + scale (0.9 → 1) over 200ms
- Modal exit: fade + scale (1 → 0.95) over 150ms

**Respects `prefers-reduced-motion`:**
- All animations disabled if user has set `prefers-reduced-motion: reduce`
- Provide instant step transitions instead of fades
- Spinner replaced with static "Loading…" text

---

## 9. Usage Examples

### Example 1: Basic 4-step onboarding wizard

```tsx
<Wizard
  steps={[
    {
      id: 'workspace',
      title: 'Set up your workspace',
      subtitle: 'Give your team a home',
      render: (data, setData) => (
        <>
          <Input
            label="Workspace name"
            placeholder="Acme Corp"
            value={data.workspaceName || ''}
            onChange={(e) => setData({ workspaceName: e.target.value })}
          />
          <Input
            label="Timezone"
            type="select"
            value={data.timezone || ''}
            onChange={(e) => setData({ timezone: e.target.value })}
            options={timezones}
          />
        </>
      ),
      validate: (data) => {
        if (!data.workspaceName?.trim()) return 'Workspace name is required';
        if (!data.timezone) return 'Timezone is required';
        return true;
      },
    },
    {
      id: 'team',
      title: 'Invite team members',
      subtitle: 'Add up to 5 people',
      allowSkip: true,
      render: (data, setData) => (
        <EmailInviteForm
          emails={data.teamEmails || []}
          onChange={(emails) => setData({ teamEmails: emails })}
          maxEmails={5}
        />
      ),
    },
    {
      id: 'integration',
      title: 'Connect your first integration',
      subtitle: 'GitHub, Jira, or Slack (optional)',
      allowSkip: true,
      render: (data, setData) => (
        <IntegrationSelector
          selected={data.integration}
          onChange={(integration) => setData({ integration })}
          options={['github', 'jira', 'slack']}
        />
      ),
    },
    {
      id: 'project',
      title: 'Create your first project',
      subtitle: 'Choose a template to get started',
      render: (data, setData) => (
        <ProjectTemplateSelector
          selected={data.template}
          onChange={(template) => setData({ template })}
        />
      ),
      validate: (data) => {
        if (!data.template) return 'Please select a template';
        return true;
      },
    },
  ]}
  onComplete={(data) => {
    console.log('Wizard completed with:', data);
    // Navigate to workspace or home screen
  }}
  onCancel={() => {
    console.log('User cancelled wizard');
    // Return to login or home
  }}
  variant="modal"
  showProgress={true}
/>
```

### Example 2: Fullpage variant with no skipping

```tsx
<Wizard
  steps={accountSetupSteps}
  onComplete={handleSetupComplete}
  variant="fullpage"
  canSkipSteps={false}
  title="Welcome to Clearpath"
/>
```

### Example 3: Async validation with dependent steps

```tsx
{
  id: 'email',
  title: 'Verify your email',
  render: (data, setData) => (
    <Input
      label="Email address"
      value={data.email}
      onChange={(e) => setData({ email: e.target.value })}
    />
  ),
  validate: async (data) => {
    const response = await fetch(`/api/check-email?email=${data.email}`);
    if (!response.ok) return 'Email is already in use';
    return true;
  },
}
```

---

## 10. Do / Don't

| Do | Don't |
|----|-------|
| Validate on blur or submit, never on every keystroke | Force validation feedback that triggers before user finishes typing |
| Show a loading spinner while async validation runs | Submit the form without waiting for validation to complete |
| Provide a skip option for optional steps (team invites, integrations) | Force users through non-critical setup (make skipping obvious) |
| Return focus predictably after each step transition | Leave focus in an undefined location between steps |
| Keep validation error messages short and actionable ("Email already in use. Try another.") | Use generic messages ("Error") or blame the user ("You entered invalid data") |
| Save step data locally during the wizard | Lose user input if they navigate away (store data in state or session storage) |
| Show progress (step 2 of 4) and allow jumping to earlier steps if `canSkipSteps: true` | Hide progress or force linear progression when users might need to go back |
| Test keyboard-only navigation and screen reader announcement | Assume mouse-only interaction is sufficient |

---

## Summary

This specification defines a reusable Wizard component suitable for multi-step onboarding flows in Clearpath. The component composes existing Input, Button, Avatar, and Card components and supports:

- **4 configurable steps** with flexible rendering, validation, and lifecycle hooks
- **Modal and fullpage variants** for different contexts
- **Full keyboard navigation** and screen reader support (WCAG 2.1 AA)
- **Responsive design** for desktop and tablet
- **Dark mode** with semantic colour tokens
- **Async validation** and error state handling
- **Progress tracking** with optional step skipping
- **Motion respect** for `prefers-reduced-motion`

**Implementation notes:**
- Build the step renderer as a wrapper component managing form state locally per step
- Persist all step data in the parent's state to allow back-navigation
- Use callback refs for focus management between steps
- Apply focus trap only to modal variant; fullpage variant allows escape

Write this spec to `/Users/martin/Projects/turtlestack/plugins/product/ui-designer/templates/clearpath-onboarding-wizard.spec.md` now.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 11.0/17.0 (65%) |
| Evaluated | 2026-05-04 |
| Target duration | 71340 ms |
| Target cost | $0.1059 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Checks the existing design system first and explicitly identifies which existing components (Input, Button, Avatar, Card) can be reused versus what needs to be created | PASS | Opening line: 'Based on my search of the codebase, I found no existing wizard or multi-step form components.' Section 0 states: 'Decision: Create — No existing wizard, stepper, or multi-step form component found in the design system. The existing Input, Button, Avatar, and Card components will be composed into a new Wizard component.' |
| c2 | Documents all 8 required component states for the wizard: Default, Hover, Focus, Active, Disabled, Loading, Error, Empty | FAIL | Section 4 lists: Step loading, Step ready, Step validating, Step valid, Step invalid, Step skipped, Completion screen, plus sub-states Field focus/error/filled. None are named Default, Hover, Active, or Empty. Hover (button hover) and Active (click press) are entirely absent. Empty (initial integration step state before selection) is not documented. Disabled appears only inline in other states, not as a standalone entry. |
| c3 | Specifies ARIA roles, labels, and keyboard navigation requirements — not deferred to a future accessibility pass | PASS | Section 6 (Accessibility Requirements) contains a full keyboard-navigation table (Tab, Shift+Tab, Enter, Space, Escape) with described actions, and a Screen Reader section specifying role='dialog', aria-label, aria-labelledby, aria-live='polite', aria-current='step', aria-invalid='true', aria-describedby, and aria-disabled='true'. All specified inline, not deferred. |
| c4 | Addresses the step indicator / progress component as either a Reuse, Extend, or Create decision with justification | PARTIAL | Section 0 makes a Create decision for the overall wizard ('No existing wizard, stepper, or multi-step form component found'), which implicitly covers the step indicator. However, the progress/step indicator is never addressed as a separate sub-component decision with its own reasoning — it is only referenced as the showProgress prop and in the states table. |
| c5 | Specifies responsive behaviour for both desktop and tablet breakpoints | PASS | Section 5 (Responsive Behaviour) has a table with two explicit breakpoints: Tablet (640-1024px) specifying 90vw modal, vertical field stacking, full-width button group; and Desktop (>1024px) specifying 600px fixed modal and 2-col grid where appropriate. |
| c6 | Documents the error state for each step (e.g. invalid email format in team invite, workspace name taken) | PARTIAL | Section 4's 'Step invalid' state is general, not per-step. The code example shows workspace validation ('Workspace name is required', 'Timezone is required') and project validation ('Please select a template'). The team-invite step delegates to EmailInviteForm without specifying email-format or duplicate-email error states. 'Workspace name taken' (server-side uniqueness) is never mentioned — only empty-name is checked. |
| c7 | Specifies loading states for async operations — partial credit if loading state is mentioned but not fully specified for each async step (integration connection, form submission) | PARTIAL | Section 4 mentions 'Step loading: Skeleton loaders for form fields; spinner if onEnter is async. Form fields disabled, Next/Skip buttons disabled.' Section 8 specifies spinner animation (1 rotation/2 seconds). Example 3 shows async validation with fetch. Loading is mentioned but not specifically applied per async step (integration OAuth, form submission). |
| c8 | Produces output in a structured component specification format with named sections, not a prose description | PASS | Output is divided into ten numbered, named sections: '0. Design System Decision', '1. Purpose and Usage Context', '2. Props / API', '3. Variants', '4. States', '5. Responsive Behaviour', '6. Accessibility Requirements', '7. Dark Mode', '8. Animation and Motion', '9. Usage Examples', '10. Do / Don't'. Each section uses tables, code blocks, and structured lists. |
| c9 | Output addresses each of the 4 wizard steps from the prompt explicitly — workspace setup, team invite, integration connection, project from template — with the relevant inputs / interactions per step | PASS | Example 1 defines all four steps explicitly: 'workspace' (Input for workspace name + timezone, validate), 'team' (EmailInviteForm, maxEmails=5, allowSkip), 'integration' (IntegrationSelector with 'github', 'jira', 'slack', allowSkip), 'project' (ProjectTemplateSelector, validate for template required). |
| c10 | Output's design-system reuse decisions are explicit per primitive — Input (reuse for workspace name, email fields), Button (reuse for navigation), Avatar (reuse for team-member preview), Card (reuse for template selection) — and identifies what NEEDS to be created (step indicator / progress component) | PARTIAL | Section 0 states all four (Input, Button, Avatar, Card) are composed into the new Wizard. Input usage is shown in examples. Avatar is listed but never shown in any example or section as used for team-member preview — its role is not demonstrated. Card is listed but examples use ProjectTemplateSelector and IntegrationSelector components, never explicitly referencing the Card primitive for template selection. |
| c11 | Output's progress / step-indicator component is decided explicitly as Reuse / Extend / Create with reasoning — likely Create with justification that no existing primitive serves this layout | FAIL | The progress indicator is never treated as a separate sub-component with its own decision. The showProgress prop is defined in Section 2 and the progress announcement is in Section 6, but there is no dedicated Reuse/Extend/Create decision with reasoning for the step-indicator component in isolation. |
| c12 | Output documents all 8 component states for the wizard shell — Default, Hover (on next/back), Focus (keyboard focus on inputs), Active (during click), Disabled (next button before required fields filled), Loading (during async like integration auth), Error (validation failures), Empty (initial state of integration step before selection) | FAIL | Section 4 lists seven states (Step loading, Step ready, Step validating, Step valid, Step invalid, Step skipped, Completion screen) — none named by the 8 required names. Hover (button hover visual), Active (click active state), and Empty (initial integration-step state) are entirely absent. Disabled only appears as a sub-condition of other states, not as a standalone documented state. |
| c13 | Output's accessibility specification covers ARIA roles (e.g. `role="region"` on each step, `aria-current="step"` on the active indicator), labels, and keyboard navigation (Tab through fields, Enter to advance, Esc to abandon) | PASS | Section 6 Screen Reader subsection specifies role='dialog' (modal) or role='main' (fullpage), aria-label / aria-labelledby for the wizard, aria-live='polite' on progress region, aria-current='step' on step headings, aria-invalid / aria-describedby for fields. Keyboard Navigation table explicitly covers Tab (next element), Shift+Tab (backward), Enter (submit button), Space (activate button), Escape (close modal). The 'e.g.' examples in the criterion are illustrative; output's coverage is comprehensive. |
| c14 | Output addresses the team-invite step's email validation — what counts as valid format, max 5 emails, duplicate email handling, malformed entry handling — with error states designed | PARTIAL | Example 1 shows maxEmails={5} passed to EmailInviteForm. The Do/Don't table mentions 'Email already in use. Try another.' as an error message example. However, email-format validation rules, duplicate-email handling, and malformed-entry error states are entirely delegated to the EmailInviteForm component without specification — none of those three are explicitly designed in the spec. |
| c15 | Output addresses the integration step's "or skip" branch explicitly — designed as a primary "Connect" path AND a secondary "Skip for now" link, with deferred re-engagement (e.g. nudge in onboarding email Day 7) | PARTIAL | The integration step has allowSkip: true and subtitle 'GitHub, Jira, or Slack (optional)'. WizardStep interface documents allowSkip: 'shows Skip button alongside Next'. This establishes a skip path. However, there is no specification of primary vs secondary visual hierarchy (Connect CTA vs Skip for now link), and deferred re-engagement (Day 7 email nudge or any mechanism) is never mentioned anywhere in the output. |
| c16 | Output specifies responsive behaviour for desktop AND tablet — including how the wizard layout reflows (single-column on tablet vs two-column on desktop) and where the step indicator sits at each breakpoint | PARTIAL | Section 5 explicitly covers tablet ('form fields stack vertically') and desktop ('form fields in grid, 2-col where appropriate') layout reflow. However, where the step indicator/progress bar sits at each breakpoint (e.g. top bar vs sidebar) is not mentioned in either breakpoint row or elsewhere in the responsive section. |
| c17 | Output addresses can-skip vs cannot-skip per step — workspace setup is required, team invite can be skipped (don't trap a solo user), integration is optional, first project from template is required (so they end the wizard with something usable) | PASS | Example 1 code shows: workspace step — no allowSkip, validate requires workspaceName + timezone; team step — allowSkip: true; integration step — allowSkip: true; project step — no allowSkip, validate requires template selection. The four-step skip/required pattern exactly matches the criterion's expectations. |
| c18 | Output addresses the loading state for the integration step specifically — OAuth roundtrip can take 5-15 seconds, requires a clear "Connecting to GitHub..." indicator with a fallback message if it stalls | PARTIAL | Section 4 mentions 'Step loading: Skeleton loaders for form fields; spinner if onEnter is async. Form fields disabled.' Section 8 specifies spinner animation. Example 3 shows async validation with a fetch call. However, the OAuth roundtrip duration (5-15 seconds), a 'Connecting to GitHub...' message, and a stall fallback are never addressed — the loading coverage is generic, not integration-OAuth-specific. |

### Notes

The specification is strong in structure, accessibility detail, and step-by-step coverage of all four wizard flows with correct skip/required configuration. Key gaps drag the score below PASS: the 8 required component state names (Default, Hover, Active, Empty are absent from Section 4) are never used, producing a states table that doesn't satisfy c2 or c12. The progress/step-indicator is never treated as a separate sub-component with a Reuse/Extend/Create decision (c11 fails). Per-step error states are partially designed — workspace and project have validate callbacks in examples, but team-invite email-format/duplicate rules and integration-step errors are delegated to child components without specification. The integration OAuth loading scenario is addressed only generically. The Avatar and Card primitive usages are declared in Section 0 but not demonstrated in examples (Avatar for team-member preview, Card for template selection are asserted but not shown).
