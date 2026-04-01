---
name: accessibility-audit
description: Audit a component, page, or codebase for WCAG 2.1 AA accessibility compliance.
argument-hint: "[component, page, or directory to audit]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Audit $ARGUMENTS for accessibility compliance against WCAG 2.1 AA.

## Checklist

### Perceivable
- [ ] Images have meaningful alt text (or `alt=""` for decorative)
- [ ] Colour is not the sole means of conveying information
- [ ] Colour contrast meets 4.5:1 for text, 3:1 for large text and UI components
- [ ] Text can be resized to 200% without loss of content
- [ ] Content is readable without CSS

### Operable
- [ ] All interactive elements are keyboard accessible
- [ ] Tab order is logical and follows visual order
- [ ] Focus is visible on all interactive elements
- [ ] No keyboard traps
- [ ] Skip navigation link for repeated content
- [ ] No time limits (or adjustable/extendable)

### Understandable
- [ ] Language is set on the `<html>` element
- [ ] Form labels are associated with inputs
- [ ] Error messages identify the field and describe the error
- [ ] Instructions don't rely solely on sensory characteristics

### Robust
- [ ] Valid HTML (no duplicate IDs, proper nesting)
- [ ] ARIA attributes used correctly (roles, states, properties)
- [ ] Custom components expose appropriate ARIA roles
- [ ] Dynamic content updates announced via live regions

## Output

Present findings as a table: issue, WCAG criterion, severity (critical/major/minor), location, and fix recommendation.
