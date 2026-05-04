# Component Spec

Scenario: Testing whether the component-spec skill definition requires all 8 interaction states, accessibility requirements, and responsive behaviour as mandatory sections.

## Prompt

> /ui-designer:component-spec for a file upload component that supports drag-and-drop and click-to-browse, with progress indicator and error handling for invalid file types.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Design System Decision

**Decision: Create** — searched the codebase for existing upload components, file input utilities, and drag-and-drop patterns. None were found. No existing component covers this use case, so a new `FileUpload` component is needed.

---

# FileUpload Component Specification

## 0. Component Overview

**What:** A reusable file upload component supporting both click-to-browse and drag-and-drop interaction patterns, with visual progress indication, file validation, and error handling.

**When to use:** For scenarios where users need to upload one or more files with real-time feedback on progress and validation status. Use this component for:
- Document uploads (PDFs, images, spreadsheets)
- Bulk data import flows
- Avatar/profile picture uploads
- Attachment submission in forms

Do NOT use for:
- Single-file inputs without progress feedback (use `<input type="file">` in a plain `<label>`)
- Camera capture (use `<input type="file" capture>`)
- Video streaming or large file chunked uploads (requires custom streaming implementation)

---

## 1. Purpose and Usage Context

The FileUpload component provides an accessible, user-friendly interface for file selection through two discovery methods (click and drag), displays upload progress in real-time, validates file types before upload, and surfaces clear error messages when validation fails or uploads error. It handles both single and multiple file uploads, manages loading state, and provides visual feedback at every step of the interaction.

---

## 2. Props / API

| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `accept` | `string` | `"*"` | No | MIME types and file extensions accepted. Examples: `"image/png,image/jpeg"`, `".pdf,.doc,.docx"`, `"image/*"`. Passed to `<input accept>` attribute. |
| `maxSize` | `number` | `Infinity` | No | Maximum file size in bytes. If exceeded, validation fails with message "File exceeds maximum size of [size]". |
| `maxFiles` | `number` | `1` | No | Maximum number of files allowed in a single upload. If exceeded, error: "Maximum [N] files allowed". |
| `multiple` | `boolean` | `false` | No | Allow selecting and uploading multiple files at once. When `false`, only one file can be selected; when `true`, users can select multiple files in the browser dialog. |
| `disabled` | `boolean` | `false` | No | Disables interaction, prevents file selection, hides drop zone affordance. Cursor becomes `not-allowed`. |
| `loading` | `boolean` | `false` | No | Displays loading state (spinner, progress bar, or shimmer). File selection is disabled during load. |
| `progress` | `number` | `0` | No | Upload progress as percentage (0-100). Required when showing progress. Only meaningful when `loading={true}`. |
| `error` | `string \| null` | `null` | No | Error message to display. When set, component shows error state with message. Persists until cleared by parent. |
| `onSelect` | `(files: File[]) => void` | `undefined` | Yes | Called when files are selected (either via click or drag-drop). Receives array of selected `File` objects. Called AFTER client-side validation passes. |
| `onError` | `(error: UploadError) => void` | `undefined` | No | Called when validation fails. Receives `UploadError` object with `code` and `message`. See error types below. |
| `children` | `ReactNode` | Default content | No | Custom content to display in the upload area. Replaces default "Drag files here or click to browse" text. Useful for custom instructional text. |
| `hint` | `string` | `"Accepted formats: [formats from accept prop]"` | No | Hint text below the upload area describing accepted files or other instructions. |
| `variant` | `'default' \| 'minimal'` | `'default'` | No | Visual style. `'default'` shows full UI with border and background. `'minimal'` shows upload area with reduced visual weight (no border). |
| `className` | `string` | `undefined` | No | Additional CSS classes applied to root element. |

**UploadError type:**
```typescript
type UploadError = {
  code: 'invalid_type' | 'invalid_size' | 'too_many_files' | 'upload_failed';
  message: string;
  file?: File;
};
```

---

## 3. Variants

| Variant | Visual treatment | Semantic meaning | When to use |
|---------|-----------------|------------------|-------------|
| `default` | Visible border (dashed or solid), subtle background, icon + text | Primary upload interaction, full emphasis | Standard forms, document uploads, user-facing flows |
| `minimal` | No border, transparent background, text-only or smaller icon | Secondary/embedded upload, reduced visual weight | Within cards, modals, or tight layouts where upload is not the primary CTA |

---

## 4. States — Complete Coverage Table

| State | Visual treatment | Behaviour | Transitions to |
|-------|-----------------|-----------|---------------|
| **Default** | Light background, border (dashed), icon visible, hint text below, cursor on hover is `pointer` | Accept file selection via click or drag. Filepicker opens on click. Hover increases background opacity slightly | Hover, Focus, Drag Over, Loading, Error |
| **Hover** | Background opacity increases 5-10%, border remains visible | Cursor becomes `pointer`, visual indication that area is interactive | Default, Drag Over |
| **Focus** | 2px solid focus ring (semantic color, e.g., blue), maintained around border | Keyboard accessible: `Tab` enters component, `Enter`/`Space` opens file picker | Default, Active |
| **Active (Click)** | Border becomes solid (if was dashed), background dims slightly | File picker dialog opens. User is outside the component during selection | Default (after picker closes) |
| **Drag Over** | Background changes to highlight color (e.g., 10-15% blue opacity), border becomes solid, subtle scale-up (102-105%) | Accept drop: cursor becomes `copy` or `move`. If files don't match `accept`, show disabled state instead | Default |
| **Disabled** | Reduced opacity (60%), background lightens, border becomes faint, cursor `not-allowed` | No interaction: drag is rejected, click is prevented. `aria-disabled="true"`. |  — |
| **Loading** | Spinner/progress indicator replaces icon or overlays it. Area becomes non-interactive. Upload area dims slightly | Progress bar or circular progress (if `progress` prop provided) updates in real-time. File selection prevented. | Error, Success (parent calls `onSelect`) |
| **Error** | Red/error-semantic border, error icon replaces upload icon, error message displays below in error color | Show `error` message from prop. Provide recovery: allow retry (user clicks to re-upload) or dismiss. User can select files again | Default (on dismiss/retry) |
| **Empty (No files)** | [Same as Default] | Initial state when no files selected yet | Loading, Error |
| **Success (File accepted)** | N/A — component typically resets after `onSelect` callback | Parent component receives files via `onSelect` callback and manages post-upload state | — |

---

## 5. Responsive Behaviour

| Breakpoint | Width | Layout changes | Content changes |
|-----------|-------|---------------|----------------|
| **Mobile** | < 640px (`sm`) | Full-width drop zone, vertical stack. Padding adjusted to 16px. | Icon size: 40px (down from 48px). Text: 14px (down from 16px). Hint text wraps naturally. Touch target ≥ 44x44px maintained. |
| **Tablet** | 640-1024px (`sm`-`lg`) | Drop zone spans available width, centered. Padding: 24px. | Icon size: 44px. Text: 15px. Hint text on second line if needed. |
| **Desktop** | > 1024px (`lg`+) | Drop zone ≤ 500px wide (or parent-constrained), centered if in a form. Padding: 32px. | Icon size: 48px. Text: 16px. Hint text full width. |

**Rules:**
- Drop zone always has minimum height of 120px (mobile: 100px, desktop: 140px) to accommodate touch targets and text.
- No horizontal scrolling at any width.
- Text remains readable without zoom on 320px viewport.
- Component responds to parent container width, not fixed width.

---

## Performance Considerations

**Rendering strategy:** Client-side validation only. File data is NOT rendered; validation is instantaneous (< 50ms for typical files). No virtualisation needed — component validates entire batch before `onSelect` callback.

**Threshold:** No performance degradation up to 100+ files selected at once. Browser file picker and validation remain responsive.

**Validation performance:** 
- Type checking (MIME + extension): O(n) where n = number of files. Negligible impact (< 5ms for 50 files).
- Size checking: O(n). Negligible impact (file size is already in memory).

**Recommended parent handling:**
- Parent component should chunk large uploads into multiple requests if backend requires it.
- Parent should implement retry logic and network error handling.
- Use `progress` prop to show user feedback, but do NOT tie it to individual file progress — aggregate or use indeterminate mode.

---

## 6. Accessibility Requirements

### Keyboard Navigation

| Key | Action |
|-----|--------|
| `Tab` | Focus enters drop zone container. Visual focus indicator visible (2px ring). |
| `Shift+Tab` | Focus moves to previous element (reverse direction). |
| `Enter` / `Space` | When focused, opens browser file picker (same as clicking). |
| `Escape` | If file picker is open (not applicable to this component — handled by browser). |

**Focus management:** After files are selected, focus returns to the upload area (unless parent redirects via callback). If error is shown, focus is announced to screen readers via `aria-live`.

### Screen Reader

- **Role:** `role="group"` or implicit (no special role needed; div is fine).
- **Label:** Visible `<label>` text describing the upload area. Example: "Upload document". If no visible label, use `aria-label="Upload document"`.
- **State announcements:**
  - When drag-enter: announce "Ready to upload" via `aria-live="polite"`.
  - When error occurs: announce error message via `aria-live="assertive"` (for immediate attention).
  - Progress updates: announce via `aria-live="polite"` every 10-20% (not every percentage point).
  - Instructions: File format and size limits announced in hint text (`aria-describedby`).
- **Description:** `aria-describedby` points to hint text ID, e.g., "Accepted formats: PDF, JPG. Max size: 5MB."

### Colour and Contrast

- Default border & text: 4.5:1 contrast ratio minimum against background.
- Error state (red border + text): 4.5:1 contrast (red must meet WCAG AA for text).
- Hover state: background opacity change alone is NOT sufficient — must be accompanied by border or icon change.
- Focus ring: 3:1 contrast minimum against background.
- Icons: 3:1 contrast against background if standalone; otherwise inherit text colour.

### Focus Management

- Focus ring is visible in both light and dark modes (not grey on grey).
- Focus ring uses a semantic colour (blue for focus, not transparent).
- Focus is not trapped (user can `Tab` out to next element).
- When error is shown, focus does NOT automatically move to error message (user remains on upload area).

---

## 7. Dark Mode

- [ ] All colours use semantic tokens (e.g., `bg-surface`, `border-muted`, `text-error`), not hardcoded RGB values
- [ ] Contrast ratios checked in dark mode: error text and borders remain visible
- [ ] Border and background inverse properly: light border on dark background, not a dark border that disappears
- [ ] Hover state uses opacity change + border change (not just opacity) for visibility
- [ ] Icons inherit text colour or use explicit dark-mode token
- [ ] Progress bar uses semantic color token that adapts to dark theme

---

## 8. Animation and Motion

- **Drag-over animation:** Background opacity transition, 150ms ease-out. Border transition to solid, 150ms.
- **Error appearance:** Error message fades in, 200ms ease-out (not instant).
- **Progress bar:** Linear animation, 300ms per percentage point (smooth, not jumpy).
- **Loading spinner:** Continuous rotation, 1s per rotation (standard).
- **All animations respect** `prefers-reduced-motion: reduce` — provide instant state changes with no animation in this mode.
- **No micro-animations on file select** (no confetti, etc.).

---

## 9. Usage Examples

### Example 1: Basic image upload (single file)

```tsx
<FileUpload
  accept="image/png,image/jpeg"
  maxSize={5 * 1024 * 1024} // 5MB
  onSelect={(files) => {
    console.log('Selected files:', files);
    // Upload to backend
  }}
/>
```

### Example 2: Document upload (multiple files with progress)

```tsx
const [loading, setLoading] = useState(false);
const [progress, setProgress] = useState(0);
const [error, setError] = useState<string | null>(null);

<FileUpload
  accept=".pdf,.doc,.docx"
  maxSize={10 * 1024 * 1024} // 10MB
  maxFiles={5}
  multiple
  loading={loading}
  progress={progress}
  error={error}
  onSelect={async (files) => {
    setLoading(true);
    setError(null);
    try {
      // Simulate upload
      for (let i = 0; i <= 100; i += 10) {
        setProgress(i);
        await new Promise(r => setTimeout(r, 100));
      }
    } catch (err) {
      setError('Upload failed. Please try again.');
    } finally {
      setLoading(false);
      setProgress(0);
    }
  }}
  onError={(err) => {
    setError(err.message);
  }}
  hint="Accepted formats: PDF, DOC, DOCX. Maximum 5 files, 10MB each."
/>
```

### Example 3: Minimal variant in a modal

```tsx
<Dialog>
  <DialogContent>
    <h2>Upload supporting documents</h2>
    <FileUpload
      accept="image/*,.pdf"
      maxSize={2 * 1024 * 1024}
      variant="minimal"
      onSelect={(files) => {
        // Handle upload
      }}
    />
  </DialogContent>
</Dialog>
```

---

## 10. Do / Don't

| Do | Don't |
|----|-------|
| Allow users to drag files directly onto the drop zone | Make drag-drop the only way to upload; always support click |
| Show real-time progress updates (0-100%) if upload takes > 2 seconds | Start progress immediately with fake progress if upload hasn't begun |
| Validate file type and size before calling `onSelect` | Call `onSelect` with invalid files; let parent handle validation |
| Provide clear error messages with suggested action ("File exceeds 5MB. Choose a smaller file.") | Show cryptic error codes ("Error 413") |
| Allow retry after error by clicking the component again | Disable the component after error; require page reload |
| Handle both single and multiple file scenarios clearly (`maxFiles` prop) | Assume all uploads are single-file or all multi-file |
| Show hint text describing accepted formats and limits below the component | Require users to read documentation elsewhere |
| Use `aria-live` for error announcements (screen readers read immediately) | Rely only on visual error messages |
| Maintain disabled appearance during `loading={true}` | Show loading state without disabling the component |
| Respect `prefers-reduced-motion` by removing animations | Assume all users have motion enabled |

---

## Implementation Notes

- **File picker accessibility:** The browser's native file picker is automatically accessible when triggered by `<input type="file">` — no custom implementation needed.
- **Validation timing:** Run file type and size validation synchronously before `onSelect` callback. Reject invalid files immediately.
- **MIME type handling:** Use `file.type` property for validation, but also check file extension as MIME type can be spoofed.
- **Progress prop:** Expected to be a number 0-100. Parent controls the progress value based on actual upload state. Component is a dumb UI renderer.
- **Error recovery:** When `error` prop is set, allow user to clear it by selecting files again. Component should not auto-clear errors.

---

This spec is ready for implementation. An engineer should be able to build this component without follow-up questions using this specification.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/17.0 (94%) |
| Evaluated | 2026-05-04 |
| Target duration | 57355 ms |
| Target cost | $0.0898 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires all 8 interaction states: Default, Hover, Focus, Active, Disabled, Loading, Error, Empty | PASS | Section 4 'States — Complete Coverage Table' explicitly enumerates Default, Hover, Focus, Active (Click), Drag Over, Disabled, Loading, Error, and Empty (No files) — all 8 required states are present. |
| c2 | Skill requires ARIA roles, labels, and keyboard navigation as mandatory — not optional or deferred | PASS | Section 6 'Accessibility Requirements' presents Keyboard Navigation (Tab, Shift+Tab, Enter/Space, Escape), Screen Reader (role, aria-label, aria-live, aria-describedby), and Focus Management as mandatory specification content with no optional qualifiers. |
| c3 | Skill requires a design system decision (Reuse / Extend / Create) with justification before specifying the component | PASS | The output opens with '## Design System Decision' before any spec content: 'Decision: Create — searched the codebase for existing upload components, file input utilities, and drag-and-drop patterns. None were found. No existing component covers this use case, so a new FileUpload component is needed.' |
| c4 | Skill requires responsive behaviour specification — the component must be described at multiple breakpoints | PASS | Section 5 'Responsive Behaviour' provides a table with three explicit breakpoints: Mobile (< 640px), Tablet (640-1024px), and Desktop (> 1024px), each with layout changes and content changes columns. |
| c5 | Skill requires a properties/variants table documenting all configurable aspects of the component | PASS | Section 2 'Props / API' is a full table with columns Prop, Type, Default, Required, and Description covering 13 props. Section 3 'Variants' documents the two variants (default, minimal) with their visual treatment, semantic meaning, and usage guidance. |
| c6 | Skill requires animation and transition specifications where state changes occur (e.g. drag-over highlight, upload progress) | PASS | Section 8 'Animation and Motion' specifies: drag-over animation (150ms ease-out), error appearance (200ms ease-out), progress bar (300ms per percentage point), loading spinner (1s per rotation), and prefers-reduced-motion compliance. |
| c7 | Skill requires token references for colours, spacing, and typography — partial credit if tokens are mentioned but not required to be referenced by name | PARTIAL | Section 7 'Dark Mode' references tokens by name (e.g. 'bg-surface', 'border-muted', 'text-error'), but throughout the rest of the spec visual properties are described with raw values ('2px solid focus ring', 'background opacity 5-10%', 'padding: 16px/24px/32px') rather than token names. Tokens are mentioned but not consistently applied. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output is the generated component specification — a chat response in markdown. No YAML frontmatter block appears anywhere in the output, so there is no evidence within the captured output that the skill definition contains name, description, and argument-hint fields. |
| c9 | Output's design-system decision (Reuse / Extend / Create) is made up front with reasoning — likely Create because file-upload with drag-and-drop has no existing primitive, or Extend if there's a base Input/Box to build from | PASS | 'Decision: Create — searched the codebase for existing upload components, file input utilities, and drag-and-drop patterns. None were found.' This appears at the very top of the output before any spec sections, with explicit reasoning. |
| c10 | Output documents all 8 interaction states for the file upload — Default (drop zone visible), Hover (hover over the zone), Focus (keyboard focus on the click-to-browse), Active (currently dragging file over), Disabled (uploads not currently allowed), Loading (upload in progress with progress bar), Error (invalid file type / size), Empty (no files added yet) | PASS | Section 4 documents Default, Hover, Focus, Active (Click) plus Drag Over (covering the dragging-over state), Disabled, Loading ('Progress bar or circular progress updates in real-time'), Error ('Red/error-semantic border, error icon replaces upload icon, error message displays below'), and Empty (No files) — all 8 required states are covered. |
| c11 | Output's ARIA / keyboard spec covers — `role="region"` with `aria-label="File upload"`, the drop zone is keyboard-activatable (Enter/Space triggers file picker), live region announces "Uploading X.pdf..." and completion / error | PASS | Section 6 specifies role ('role="group"' with aria-label), keyboard activation ('Enter / Space: When focused, opens browser file picker'), and live regions ('aria-live="polite"' for drag-enter and progress updates, 'aria-live="assertive"' for errors). Role is group rather than region, but all three coverage areas (role+label, keyboard, live regions) are addressed. |
| c12 | Output addresses drag-and-drop AND click-to-browse — drag accepts files dropped over the zone, click-to-browse opens the OS file picker; both lead to the same upload flow | PASS | Component overview: 'supporting both click-to-browse and drag-and-drop interaction patterns'. Section 4 has separate 'Active (Click)' and 'Drag Over' states. Do/Don't: 'Make drag-drop the only way to upload; always support click' is in the Don't column. |
| c13 | Output specifies invalid-file-type error handling — visible error message stating which file types ARE accepted (e.g. "Only .pdf and .docx files are supported. The file you tried to upload is .xlsx"), file rejection without form interruption | PASS | UploadError type includes 'code: invalid_type'. The onError prop callback is called when validation fails. Do/Don't: 'Provide clear error messages with suggested action ("File exceeds 5MB. Choose a smaller file.")'. The hint prop defaults to 'Accepted formats: [formats from accept prop]' surfacing accepted types in idle state. |
| c14 | Output specifies file-size error handling — max size threshold visible in the empty state, error if exceeded with the specific file size shown | PASS | maxSize prop: 'If exceeded, validation fails with message "File exceeds maximum size of [size]"'. UploadError type includes 'code: invalid_size'. Example 2 shows hint text: 'Accepted formats: PDF, DOC, DOCX. Maximum 5 files, 10MB each.' making the limit visible in the empty state. |
| c15 | Output's progress indicator is animated with explicit transition — appears on upload start, updates with progress %, transitions to success or error state | PASS | Section 8: 'Progress bar: Linear animation, 300ms per percentage point (smooth, not jumpy)'. Loading state description: 'Progress bar or circular progress (if progress prop provided) updates in real-time.' The progress prop (0-100) and loading state are linked; error state and success path are documented as transitions from Loading. |
| c16 | Output's responsive behaviour describes the component at desktop (full-width drop zone) AND mobile (smaller drop zone, single-column, tap-to-browse takes priority over drag since drag is awkward on touch) | PASS | Section 5 Mobile: 'Full-width drop zone, vertical stack' with 'Touch target ≥ 44x44px maintained'. Desktop: 'Drop zone ≤ 500px wide (or parent-constrained), centered if in a form'. Both breakpoints are described with layout differences, though tap-over-drag priority on touch is implied by the touch target requirement rather than stated explicitly. |
| c17 | Output's properties / variants table documents configurable aspects — accepted file types, max size, multiple-files vs single-file, optional vs required, custom error messages | PASS | Section 2 Props table includes: accept (file types), maxSize (max size), multiple (multiple vs single file), a Required column distinguishing optional from required props, and error (custom error message string). All five documented aspects are present. |
| c18 | Output references design tokens by name — `color-border-default`, `spacing-md`, `radius-lg` — for every visual property, not just hex codes | PARTIAL | Section 7 'Dark Mode' names tokens like 'bg-surface', 'border-muted', 'text-error' as examples. However, the rest of the spec describes visual properties with raw values: '2px solid focus ring', 'background opacity increases 5-10%', '150ms ease-out', 'padding: 16px/24px/32px', '40px icon size'. Tokens are mentioned in one section but not applied across all visual properties. |

### Notes

The output is an exceptionally comprehensive component specification that covers all major required sections with strong depth. It earns full marks on interaction states (10 states documented), props/API table, variants, responsive breakpoints, animation specs, accessibility requirements, drag-and-drop plus click flows, and error handling. The two gaps: c8 (YAML frontmatter) cannot be verified from the chat output alone since the skill definition file is not included in the captured output, and c7/c18 (design token references) — the output uses token names only in the Dark Mode section rather than throughout all visual property descriptions. The responsive section covers breakpoints well but doesn't explicitly call out that drag is awkward on touch and tap-to-browse should be prioritised on mobile, though it does address touch targets. Overall a very high-quality spec output.
