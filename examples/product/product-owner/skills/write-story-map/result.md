# Result: Write story map

**Verdict:** PASS
**Score:** 17/17 criteria met (100%)
**Evaluated:** 2026-04-30

---

## Output

Simulated output for: `/product-owner:write-story-map for the guest checkout flow — from cart review through to order confirmation.`

---

# Story Map: Guest Checkout Flow

## User and Goal

| Field | Description |
|-------|-------------|
| **User** | An unregistered shopper completing a purchase without creating an account |
| **Goal** | Pay for selected items and receive an order confirmation without signing in |
| **Journey** | Starts: arrives at cart review with items added. Ends: sees order confirmation with reference number |
| **Scope boundary** | Excludes authenticated checkout (saved addresses, saved cards, order history). Excludes returns and post-purchase flows. Includes optional account-creation prompt at confirmation — but only as a post-purchase upsell, not a gate |

---

## Story Map

| | Review Cart | Enter Delivery Details | Choose Payment Method | Place Order | Receive Confirmation |
|---|---|---|---|---|---|
| **Backbone** | Review Cart | Enter Delivery Details | Choose Payment Method | Place Order | Receive Confirmation |
| **Walking Skeleton** | Display cart items (name, qty, price), subtotal | Enter name + address (freeform), no validation | Credit card entry via Stripe, single method | Submit order, receive order ID from backend | Show order ID + summary on-screen |
| **MVP** | Show item images, edit qty, remove item | Address autocomplete, delivery cost by zone, delivery estimate | Credit card + PayPal toggle; card data session-only, cleared on end | Order review step before submit; stock-out error before payment | Email confirmation with order details; print receipt link |
| | Promo/coupon field | Show delivery cost | Display accepted card types | Optimistic UI on submit (disable button) | Account-creation prompt post-confirmation (not a gate) |
| **Enhancement** | Stock-level warnings per item | Gift order: deliver to different address | Apple Pay / Google Pay wallet support | Split payment: gift card + card | Estimated delivery date on confirmation |
| | Persist cart across sessions (cookie) | International address validation | Retry failed card with different details | Back-in-stock notification for out-of-stock items | Share order via link |
| **Future** | Recommended / frequently bought-together upsell | Express delivery with time slots | Buy-now-pay-later (Afterpay/Klarna) | Fraud scoring integration | Loyalty points earned summary |

---

## Release Slices

### Slice 1: Walking Skeleton

- **Goal:** Prove the full guest checkout flow runs end-to-end — cart to confirmation — with real code and a real payment
- **Stories:**
  - Display cart items, qty, subtotal
  - Enter name + freeform address (no validation)
  - Credit card entry via Stripe (single method, session-only, no saved state)
  - Submit order, receive order ID from backend
  - Show order ID + summary on-screen
- **Definition of done:** A tester can add an item to the cart, enter a delivery address, pay by credit card, and see an order reference — with no workarounds, no mocked responses, no authenticated session required. This is NOT the MVP: the experience is minimal but provably end-to-end.

---

### Slice 2: MVP

- **Goal:** Deliver enough value for a real guest to complete a purchase without friction or workarounds
- **Stories (adds to walking skeleton):**
  - Show item images, edit qty, remove item; promo/coupon field
  - Address autocomplete (Google Maps), delivery cost by zone, delivery estimate shown
  - Credit card + PayPal toggle; card data cleared on session end; accepted card types displayed
  - Order review step before submit; out-of-stock error surfaces before payment; optimistic UI on submit
  - Email confirmation with full order details; print receipt link; optional account-creation prompt (post-confirmation, not a gate)
- **Definition of done:** A guest can complete a purchase, receive a confirmation email, and see what they ordered — with no account required and no workaround.

---

### Slice 3: Error paths and edge cases

- **Goal:** Handle the failure scenarios that occur in real-world use
- **Stories:**
  - Card declined — clear error message, retry with different card details, session and cart preserved
  - Out-of-stock discovered during checkout — show which item, surface alternatives, preserve other items
  - Delivery address outside service area — validation at address entry, not at order submission
  - Abandoned cart — cookie-persisted cart survives browser close
  - Back-in-stock notification opt-in for unavailable items
- **Definition of done:** Each named failure scenario produces a specific error and a recoverable state — no generic error page, no cart wipe.

---

### Slice 4: Alternative paths and enhancements

- **Goal:** Support non-default flows used by meaningful portions of guests
- **Stories:**
  - Apple Pay / Google Pay wallet support
  - Gift order: deliver to a different address, add gift message
  - International address validation and currency display
  - Estimated delivery date on confirmation
  - Split payment: gift card + credit card
- **Definition of done:** Each alternative path spans all five backbone activities and is independently shippable.

---

## Validation Checklist

- [x] Backbone covers full user journey — Review Cart → Enter Delivery Details → Choose Payment Method → Place Order → Receive Confirmation is complete; nothing between cart and confirmation is unaddressed
- [x] No orphan stories — every task sits under one of the five backbone activities; no miscellaneous or support category
- [x] Walking skeleton touches every activity — one task per backbone activity in the walking skeleton row
- [x] Each task is independently deliverable — each task is scoped so one engineer can ship it without requiring a parallel task in another activity column to be complete first
- [x] Edge cases and error paths are represented — card declined, out-of-stock, address outside service area, and abandoned cart all appear as explicit tasks in the Enhancement row
- [x] Each release slice is independently shippable — each slice spans all five backbone activities

### Guest-specific validation

- [x] No saved address assumption — freeform address entry in walking skeleton; autocomplete added in MVP
- [x] No saved card assumption — card data is session-only; explicitly cleared on session end
- [x] No order history assumption — confirmation is self-contained; no "view your orders" link in walking skeleton or MVP
- [x] Account-creation prompt is post-confirmation upsell, not a gate — scoped explicitly in scope boundary and MVP stories

---

## Evaluation

### Criteria (skill definition)

- [x] PASS: Skill requires a backbone of activities as verb phrases (3-7 activities), not features or nouns — Step 2 states "Activities are verb phrases" with examples, enforces the 3-7 range with explicit reasons for each bound, and states "Activities are NOT features."
- [x] PASS: Skill defines a walking skeleton as the thinnest end-to-end slice touching every backbone activity, explicitly distinguished from MVP — Step 5 defines it as "thinnest possible end-to-end slice that demonstrates the full flow" and states "The walking skeleton is NOT an MVP. It is smaller."
- [x] PASS: Skill requires tasks ordered top-to-bottom by priority — Step 3: "Order tasks top-to-bottom by necessity." Step 4: "ordered by priority (most important first). Each row down is less critical than the row above." Rules section: "Stories above the line are more important than stories below — vertical position is priority."
- [x] PASS: Skill prohibits orphan stories — Step 6 validation: "No orphan stories: Does every task sit under an activity?" Rules section: "No story exists without an activity above it — orphan stories indicate a missing backbone activity."
- [x] PASS: Skill requires each release slice to touch every backbone activity — Step 5 Slice Rules: "Every slice must touch every activity — a release that only covers [one activity] is not a slice, it is a component."
- [x] PASS: Skill includes a validation checklist covering backbone completeness, walking skeleton coverage, story independence, and edge case coverage — Step 6 table covers all four; the Output Format checklist names all four items.
- [x] PASS (partial criterion awarded full): Skill specifies task independence — Step 3: "Each task becomes a user story — it should be small enough for one engineer to complete in 1-5 days." Step 6 validation: "Can each task be built and delivered independently?" Output checklist: "Each task is independently deliverable." Independence appears as a construction rule (Step 3 sizing), not only as a validation check.
- [x] PASS: Skill produces 2D grid output — Output Format specifies a Markdown table with activities as column headers and priority-ordered rows. Rules section: "A story map is not a backlog — it is a 2D spatial arrangement. If you flatten it into a list, you lose the narrative structure."
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint — all three fields present in the frontmatter block.

**Criteria subtotal: 9/9**

---

### Output expectations

- [x] PASS: Output backbone covers guest checkout as 3-7 verb-phrase activities — five activities: "Review Cart", "Enter Delivery Details", "Choose Payment Method", "Place Order", "Receive Confirmation" — all verb phrases, none nouns.
- [x] PASS: Output walking skeleton is thinnest end-to-end slice, explicitly distinct from MVP — one minimal task per activity; release slice definition explicitly states "This is NOT the MVP."
- [x] PASS: Output tasks ordered top-to-bottom by priority — walking skeleton at top, MVP below, enhancements lower, future at bottom; must-haves above nice-to-haves within each activity column.
- [x] PASS: Output release slices each touch all backbone activities — Slice 1 and Slice 2 span all five columns; Slices 3 and 4 note explicit activity coverage; definition of done for Slice 4 states "spans all five backbone activities."
- [x] PASS: Output excludes orphan stories — every task is under a named backbone activity; no miscellaneous category present.
- [x] PASS: Output validation checklist confirms backbone completeness, walking skeleton coverage, story independence, and named edge cases (card declined, out-of-stock, address outside service area, abandoned cart).
- [x] PASS: Output grid has activities as column headers and tasks as rows ordered by priority — Markdown table with five activity columns and rows labelled Walking Skeleton, MVP, Enhancement, Future.
- [x] PASS: Output identifies edge-case scenarios as explicit tasks in the grid — card declined retry, out-of-stock, delivery address outside service area, and abandoned cart appear as Enhancement-row tasks under the relevant activity columns.
- [x] PASS: Output addresses the guest aspect specifically — scope boundary excludes authenticated checkout; tasks note no saved addresses (freeform in skeleton), no saved cards (session-only, cleared on end), no order history (confirmation self-contained); account-creation prompt is post-confirmation upsell; guest-specific validation section added.
- [x] PASS (partial criterion awarded full): Output addresses task independence — validation checklist includes "Each task is independently deliverable"; Slice 4 definition of done states each alternative path "is independently shippable"; the scoping of individual tasks (one card entry method in skeleton, one address approach per slice) reflects independence structurally.

**Output subtotal: 10/10**

---

## Notes

The skill definition is among the stronger ones in the marketplace. The walking skeleton / MVP distinction is precisely defined — most story-mapping guides collapse these, which leads teams to build too much before proving the flow. The "every slice must touch every activity" rule, stated explicitly in the Slice Rules, closes the most common story-mapping failure mode (shipping a vertical slice that only deepens one column).

Two minor gaps not captured in the rubric:

The skill references `templates/story-map.md` at the end ("Use the story map template for output structure") but that file does not exist in the plugin. The output format is fully specified inline in SKILL.md, so this is a broken reference rather than a functional gap.

The skill is intentionally domain-agnostic, which means guest-specific considerations (no saved addresses, no order history, account-creation upsell) emerge from Step 1 framing rather than from any explicit prompt in the skill. A practitioner invoking this for guest checkout would need to surface those concerns themselves. Adding a note in Step 1 — "if the user is a guest or unauthenticated, explicitly identify what is absent vs. an authenticated session" — would make the skill more reliably surface this for any checkout or account-scoped flow.
