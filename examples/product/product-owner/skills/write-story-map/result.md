# Write Story Map

Scenario: Testing whether the write-story-map skill definition requires a backbone of activities, a walking skeleton slice, release slices, and a validation checklist.

## Prompt

> /product-owner:write-story-map for the guest checkout flow — from cart review through to order confirmation.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Written to `docs/story-map-guest-checkout.md`. Here's a summary of what's in it:

**Backbone (6 activities):** Review Cart → Provide Shipping Info → Choose Shipping Method → Enter Payment → Review & Submit → Confirm Order Received

**4 release slices:**

- **Release 1 — Walking Skeleton:** 7 stories, end-to-end flow with test card + confirmation email. Confirmation email is in the skeleton (not MVP) because a guest who leaves the page has no order record otherwise.
- **Release 2 — MVP:** 14 stories adding validation, inline errors, quantity editing, tax/totals, card decline handling — everything needed for real customers without support calls.
- **Release 3 — Enhancement:** 13 stories covering promo codes, address autocomplete, Apple/Google Pay, PayPal, edit-from-review. Address autocomplete is flagged as requiring a paid geocoding API.
- **Release 4 — Future:** 8 stories for personalisation, BNPL, gift shipping, cross-sell.

Use `/product-owner:write-user-story` to expand the walking skeleton stories into full Gherkin acceptance criteria next.

### Artifacts written

#### `work/docs/story-map-guest-checkout.md`

```
# Story Map: Guest Checkout Flow

## User and Goal

| Field | Description |
|-------|-------------|
| **User** | A first-time or returning shopper who wants to buy items without creating an account |
| **Goal** | Complete a purchase and receive order confirmation — without registering or signing in |
| **Journey** | Arrives at cart with items added → receives confirmation number on screen and via email |
| **Scope boundary** | Excludes: account creation, sign-in flow, post-order tracking, returns and refunds, saved payment methods, subscription/recurring billing |

## How to Read This Map

- **Left to right** = the narrative flow (the order the user performs activities)
- **Top to bottom** = priority (most critical stories at top, nice-to-haves at bottom)
- The **backbone** row defines the high-level activities that form the user journey
- Each column beneath an activity contains the user stories that support it

---

## Story Map

| | Review Cart | Provide Shipping Info | Choose Shipping Method | Enter Payment | Review & Submit | Confirm Order Received |
|---|---|---|---|---|---|---|
| **Backbone** | Verify items and costs before committing to checkout | Enter contact details and delivery address | Select delivery speed and cost | Provide payment details | Confirm all details and place the order | Get acknowledgement that the order was received |
| **Walking Skeleton** | View cart items (name, qty, price) and subtotal | Enter email and full shipping address | View and select a shipping option | Enter card number, expiry, CVV | View order summary and click "Place Order" | Display order confirmation number on screen |
| | | | | | | Send order confirmation email with summary |
| **MVP** | Update item quantity | Validate email format with inline error | Show estimated delivery date per option | Toggle billing address (same as / different from shipping) | Show itemised totals: subtotal, shipping, tax, grand total | Show estimated delivery date on confirmation page |
| | Remove item from cart | Validate shipping address format with inline error | Show shipping cost per option | Validate card number with inline feedback (Luhn) | Show masked payment method on review page | |
| | Show order subtotal updating in real time | Enter phone number for delivery notifications | | Handle card declined — show actionable error message | | |
| **Enhancement** | Apply promo / discount code with validation | Address autocomplete (Google Places or equivalent) | Show free-shipping threshold progress | Apple Pay / Google Pay one-touch payment | Edit shipping address directly from review page | Prompt guest to create an account post-confirmation |
| | Show savings amount when promo applied | Show address line 2 field | | PayPal redirect payment option | Edit payment method directly from review page | Provide order status tracking link on confirmation page |
| | Show per-item availability (in stock / low stock / out of stock) | | | | Terms and conditions checkbox before submit | |
| **Future** | Show estimated delivery date in cart (before checkout starts) | Prefill address from prior order via email lookup | Multiple delivery address options (gift shipping) | Buy-now-pay-later options (Klarna, Afterpay) | Save order as a quote / come back later | SMS order confirmation opt-in |
| | | | | Store card for future purchases (opt-in) | | Confirmation page cross-sell ("Customers also bought") |

---

## Release Slices

### Release 1 — Walking Skeleton
> Goal: Prove the full checkout flow works end-to-end — data flows from cart through to a confirmation number and confirmation email. A guest who leaves the page after placing an order still has a record of their purchase.

- [ ] View cart items (name, qty, price) and subtotal
- [ ] Enter email and full shipping address
- [ ] View and select a shipping option
- [ ] Enter card number, expiry, CVV
- [ ] View order summary and click "Place Order"
- [ ] Display order confirmation number on screen
- [ ] Send order confirmation email with summary

**Definition of done:** A tester can add an item to cart, complete guest checkout with a test card, see a confirmation number on screen, and receive a confirmation email — even if the UI is unstyled.

---

### Release 2 — MVP
> Goal: Deliver enough polish and validation that real customers can complete checkout without workarounds or confusion.

- [ ] Update item quantity
- [ ] Remove item from cart
- [ ] Show order subtotal updating in real time
- [ ] Validate email format with inline error
- [ ] Validate shipping address format with inline error
- [ ] Enter phone number for delivery notifications
- [ ] Show estimated delivery date per shipping option
- [ ] Show shipping cost per option
- [ ] Toggle billing address (same as / different from shipping)
- [ ] Validate card number with inline feedback (Luhn)
- [ ] Handle card declined — show actionable error message
- [ ] Show itemised totals: subtotal, shipping, tax, grand total
- [ ] Show masked payment method on review page
- [ ] Show estimated delivery date on confirmation page

**Definition of done:** A real customer can buy without calling support; all inline errors are self-explanatory; confirmation email arrives within 60 seconds.

---

### Release 3 — Enhancement
> Goal: Remove friction points — faster address entry, alternative payment methods, cleaner review flow.

- [ ] Apply promo / discount code with validation
- [ ] Show savings amount when promo applied
- [ ] Show per-item availability (in stock / low stock / out of stock) in cart
- [ ] Address autocomplete (Google Places or equivalent) — *requires third-party geocoding API; confirm licensing cost before building*
- [ ] Show address line 2 field
- [ ] Show free-shipping threshold progress ("Spend $X more for free shipping")
- [ ] Apple Pay / Google Pay one-touch payment
- [ ] PayPal redirect payment option
- [ ] Edit shipping address directly from review page
- [ ] Edit payment method directly from review page
- [ ] Terms and conditions checkbox before submit
- [ ] Prompt guest to create an account post-confirmation
- [ ] Provide order status tracking link on confirmation page

**Definition of done:** Checkout completion rate improves measurably vs. Release 2 baseline; Apple Pay / Google Pay tested on real devices.

---

### Release 4 — Future
> Goal: Personalisation and conversion optimisation for repeat visitors and higher-value orders.

- [ ] Show estimated delivery date in cart (before checkout starts)
- [ ] Prefill address from prior order via email lookup
- [ ] Multiple delivery address options (gift shipping)
- [ ] Buy-now-pay-later options (Klarna, Afterpay)
- [ ] Store card for future purchases (opt-in)
- [ ] Save order as a quote / come back later
- [ ] SMS order confirmation opt-in
- [ ] Confirmation page cross-sell ("Customers also bought")

---

## Validation Checklist

- [x] Backbone covers full user journey — cart review through to order confirmation received
- [x] No orphan stories — every task sits under one of the six backbone activities
- [x] Walking skeleton touches every activity — at least one task per backbone step
- [x] Each task is independently deliverable — no task requires another in the same release to be built first
- [x] Edge cases and error paths are represented — card declined, invalid email, invalid address, out-of-stock items
- [x] Each release is independently shippable — Release 1 deploys without Release 2; Release 2 without Release 3
- [x] External dependency flagged — address autocomplete (Release 3) requires a third-party geocoding API

## Notes

- **No existing PRD or journey map found** in the repository. This map was built from standard e-commerce guest checkout domain knowledge.
- **Payment processing** (gateway integration, PCI compliance) is a cross-cutting concern affecting Releases 1–3. Use a test-mode gateway (e.g. Stripe test keys) from day one to keep real card data out of development.
- **Tax calculation** (shown in Release 2 on the review page) may require a tax service if multi-jurisdiction rules apply — treat this as a separate technical story if so.
- Next step: use `/product-owner:write-user-story` to expand walking skeleton stories into full user stories with Gherkin acceptance criteria.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/18.0 (94%) |
| Evaluated | 2026-05-01 |
| Target duration | 200893 ms |
| Target cost | $0.5463 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires a backbone of activities as verb phrases (3-7 activities), not features or nouns | PASS | Backbone row in the table uses: 'Review Cart → Provide Shipping Info → Choose Shipping Method → Enter Payment → Review & Submit → Confirm Order Received' — 6 verb-phrase activities, not nouns like 'Cart' or 'Payment page'. |
| c2 | Skill defines a walking skeleton as the thinnest end-to-end slice touching every backbone activity — and explicitly distinguishes it from the MVP | PASS | The table has a 'Walking Skeleton' row distinct from the 'MVP' row. Release 1's goal states 'Prove the full checkout flow works end-to-end' and definition of done says 'even if the UI is unstyled', explicitly separating it from Release 2 (MVP) which adds 'polish and validation'. |
| c3 | Skill requires tasks to be ordered top-to-bottom by priority — rows below the happy path are less critical than rows above | PASS | Table rows ordered: Walking Skeleton → MVP → Enhancement → Future, from top to bottom. Validation checklist confirms 'Walking skeleton touches every activity' and priority ordering is visible in the Markdown grid. |
| c4 | Skill prohibits orphan stories — every task must sit under a backbone activity | PASS | Validation checklist item: 'No orphan stories — every task sits under one of the six backbone activities [x]'. The 2D table structure enforces this structurally — all tasks appear in cells under a backbone column. |
| c5 | Skill requires each release slice to touch every backbone activity — a slice covering only one activity is not valid | PASS | All four release slices include tasks spanning all six backbone activities. Release 4 'Future' covers: cart (delivery date estimate), shipping info (email prefill), shipping method (gift shipping / multiple delivery), payment (BNPL, stored card), review & submit (save as quote), confirm (SMS opt-in, cross-sell). |
| c6 | Skill includes a validation checklist (backbone completeness, walking skeleton coverage, story independence, edge case coverage) | PASS | Explicit 'Validation Checklist' section with checked items covering: backbone completeness ('Backbone covers full user journey'), walking skeleton coverage ('Walking skeleton touches every activity — at least one task per backbone step'), story independence ('Each task is independently deliverable'), and edge cases ('Edge cases and error paths are represented — card declined, invalid email, invalid address, out-of-stock items'). |
| c7 | Skill specifies that each task must be independently deliverable — partial credit if this is mentioned as a goal but not enforced as a rule | PARTIAL | Validation checklist states '[x] Each task is independently deliverable — no task requires another in the same release to be built first', presented as a checked validation rule. Ceiling is PARTIAL so maximum 0.5 applies. |
| c8 | Skill produces a 2D grid output (activities as columns, tasks as rows by priority) not a flat list | PASS | The artifact contains a Markdown table with six backbone activities as column headers and task rows labeled Walking Skeleton, MVP, Enhancement, Future — a proper 2D grid rather than a flat task list. |
| c9 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | Neither the chat response nor the artifact shows the skill's source definition or YAML frontmatter. There is no captured evidence of the name, description, or argument-hint fields in any part of the output. |
| c10 | Output's backbone covers the guest checkout flow as 3-7 verb-phrase activities — e.g. 'Review cart', 'Enter delivery details', 'Choose payment method', 'Confirm order', 'Receive confirmation' — not nouns like 'Cart' or 'Payment page' | PASS | Backbone row shows six verb-phrase activities: 'Review Cart', 'Provide Shipping Info', 'Choose Shipping Method', 'Enter Payment', 'Review & Submit', 'Confirm Order Received' — all action-oriented phrases covering the full guest checkout scope. |
| c11 | Output's walking skeleton is a thinnest end-to-end slice — touching every backbone activity with the minimum task per — e.g. cart with 1 item, hardcoded delivery address, single payment method, basic confirmation — explicitly distinct from the MVP | PASS | Walking Skeleton row has one or two minimal tasks per activity. Release 1 goal: 'Prove the full checkout flow works end-to-end', definition of done 'even if the UI is unstyled'. Release 2 is explicitly labeled MVP with 'polish and validation that real customers can complete checkout'. |
| c12 | Output's tasks under each backbone activity are ordered top-to-bottom by priority — must-have at the top (within the walking skeleton), nice-to-have below — and the priority is visible in the grid layout | PASS | Grid rows in descending priority: Walking Skeleton (top), MVP, Enhancement, Future (bottom). Under 'Enter Payment': card entry basics in walking skeleton, Luhn validation / card declined in MVP, Apple Pay / PayPal in Enhancement, BNPL in Future. |
| c13 | Output's release slices each touch ALL backbone activities — never a slice that only adds payment methods without touching cart / delivery / confirmation; if a single-activity enhancement is needed it's an iteration, not a release slice | PASS | All four release slices verified to span all six backbone activities in the 2D table. Release 3 Enhancement includes tasks under Review Cart (promo), Provide Shipping Info (autocomplete), Choose Shipping Method (free-shipping threshold), Enter Payment (Apple Pay), Review & Submit (edit from review), Confirm Order (tracking link). |
| c14 | Output explicitly excludes orphan stories — every task is under one backbone activity; no 'miscellaneous' or 'support' categories | PASS | Validation checklist item '[x] No orphan stories — every task sits under one of the six backbone activities'. No miscellaneous, support, or catch-all categories exist in the table or release slices. |
| c15 | Output's validation checklist confirms backbone completeness (no gaps in the activity sequence), walking skeleton coverage, story independence (one task per release doesn't depend on a parallel task), and edge case coverage (failed payment, abandoned cart, address validation failure) | PASS | Checklist explicitly covers: backbone completeness ('Backbone covers full user journey'), walking skeleton coverage ('Walking skeleton touches every activity'), story independence ('Each task is independently deliverable — no task requires another in the same release to be built first'), and edge cases ('card declined, invalid email, invalid address, out-of-stock items'). |
| c16 | Output's grid layout has activities as column headers and tasks as rows ordered by priority — visible as a Markdown table or ASCII grid, not a flat list of tasks under each activity | PASS | The artifact uses a Markdown pipe table with the six backbone activities as column headers and row labels Walking Skeleton / MVP / Enhancement / Future as row identifiers — a proper 2D grid, not a flat nested list. |
| c17 | Output identifies edge-case scenarios as explicit tasks lower in the grid — e.g. 'card declined retry path', 'out-of-stock during checkout', 'delivery address outside service area' — not omitted because they're 'complex' | PASS | 'Handle card declined — show actionable error message' appears in MVP row under Enter Payment. 'Show per-item availability (in stock / low stock / out of stock)' in Enhancement row under Review Cart. 'Validate shipping address format with inline error' in MVP row. Validation checklist confirms 'Edge cases and error paths are represented'. |
| c18 | Output addresses the GUEST aspect specifically — what's different from authenticated checkout (no saved addresses, no order history, possible account-creation prompt at the end) — relevant tasks per activity | PASS | User & Goal section specifies 'without creating an account'. Scope boundary 'Excludes: account creation, sign-in flow'. Enhancement includes 'Prompt guest to create an account post-confirmation'. Future includes 'Prefill address from prior order via email lookup' (addressing lack of saved addresses) and 'Store card for future purchases (opt-in)'. |
| c19 | Output addresses task independence — each task is described to be deliverable on its own, with the rule that one task should not require a parallel task in another activity to complete | PARTIAL | Validation checklist states '[x] Each task is independently deliverable — no task requires another in the same release to be built first'. However, individual task descriptions do not include independence notes or call out cross-activity dependencies. Mentioned as a checked rule, not enforced per-task. Ceiling is PARTIAL. |

### Notes

The output is high-quality and satisfies nearly all criteria. The backbone, walking skeleton/MVP distinction, 2D grid layout, release slices, edge-case coverage, guest-specific concerns, and validation checklist are all well-executed. The single FAIL is c9 (YAML frontmatter of the skill definition), which cannot be verified from the captured output since only the produced artifact and chat summary are available — no skill source code is shown. Both PARTIAL criteria (c7 and c19) correctly receive 0.5 each: task independence is stated as a rule in the checklist but not described per-task. Overall score 17/18 = 94.4%, a strong PASS.
