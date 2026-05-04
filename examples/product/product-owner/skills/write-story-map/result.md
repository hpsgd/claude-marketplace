# Write Story Map

Scenario: Testing whether the write-story-map skill definition requires a backbone of activities, a walking skeleton slice, release slices, and a validation checklist.

## Prompt

> /product-owner:write-story-map for the guest checkout flow — from cart review through to order confirmation.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I've created a guest checkout story map with **5 main activities** spanning from cart review to order confirmation.

**Key structure:**

- **Backbone:** Review Cart → Provide Shipping → Provide Payment → Confirm & Pay → Receive Confirmation
- **Walking Skeleton** (Slice 1): Minimal end-to-end flow — guest can checkout without account and receive confirmation
- **MVP** (Slice 2): Add error handling, address validation, itemized breakdown, proper error messages
- **Slice 3+:** Progressive enhancements — discounts, faster entry (postcode auto-fill), digital wallets, international shipping

**Release slicing philosophy:**
- Slice 1 is **thin but complete** — every activity is touched, flow end-to-end, but minimal features
- Slice 2 adds **confidence & reliability** — validation, error recovery, detailed confirmation
- Slices 3+ add **convenience & choice** — discounts, smart features, alternative payment methods

Each slice is independently shippable, and the map calls out key risks (payment failures, address validation, PCI compliance) that need design upfront.

The map is in `docs/story-map-guest-checkout.md`. Next step: use `/product-owner:write-user-story` to detail individual stories from the map with Gherkin acceptance criteria.

### Artifacts written

#### `work/docs/story-map-guest-checkout.md`

```
# Story Map: Guest Checkout Flow

## User and Goal

| Field | Description |
|-------|-------------|
| **User** | A guest shopper with items in their cart who wants to purchase without creating an account |
| **Goal** | Complete a purchase quickly and receive order confirmation with tracking information |
| **Journey** | Starts: reviewing items in cart → Ends: order confirmation received and displayed |
| **Scope boundary** | Excludes account creation, wishlists, gift messaging, and post-purchase order management (returns, refunds). Includes guest-only checkout path |

## Story Map

| | Review Cart | Provide Shipping | Provide Payment | Confirm & Pay | Receive Confirmation |
|---|---|---|---|---|---|
| **Backbone** | Review items, quantities, prices | Enter delivery address and shipping method | Enter payment details | Review order total | Process payment and confirm |
| **Walking Skeleton** | View cart items and total | Enter shipping address | Enter card details | Display order summary | Show confirmation page |
| | | | | | |
| **MVP** | Remove item from cart | Validate address | Validate card | Review items and total | Display order number and email |
| | See subtotal and taxes | Select shipping method | Select payment method | See breakdown (subtotal, tax, shipping, total) | Send confirmation email |
| | See shipping cost estimate | Calculate shipping cost | Enter billing address | Accept terms | Provide tracking link |
| | | | | | |
| **Enhancement** | Apply discount code | Auto-fill address from postcode | Save payment method (optional) | Edit items before confirming | Show estimated delivery date |
| | View item details (SKU, options) | Select delivery instructions | Show payment method icon | Apply final discount | Suggest related products |
| | Inventory status per item | Show address confirmation | Tokenize card securely | Show security badges | Provide downloadable receipt |
| | | | | | |
| **Future** | Compare with wishlist | Handle international shipping | Support digital wallets (Apple Pay, Google Pay) | Handle promo code redemption | Post-purchase survey |
| | Bulk pricing | Save address for future orders | Split payment across methods | Collect marketing consent | Subscription offer |
| | | | | | |

## Release Slices

### Slice 1: Walking Skeleton
**Goal:** Prove the end-to-end guest checkout flow works without account creation.

**Stories:**
- View cart items and total price
- Enter shipping address (street, city, state, zip)
- Select shipping method from available options
- Enter card details (number, expiry, CVV)
- Display order summary with all costs
- Process payment and show confirmation page with order number
- Send confirmation email to guest

**Definition of done:**
- A guest can complete checkout from cart review to confirmation
- System accepts guest email without account creation
- Payment processes and order is confirmed
- No manual interventions or workarounds needed

---

### Slice 2: MVP
**Goal:** Deliver a complete, usable checkout experience that prevents common errors and provides confidence.

**Stories:**
- Remove items from cart mid-checkout
- Validate shipping address format and offer corrections
- Calculate and display accurate shipping costs per method
- Validate card details (format, expiry, CVC)
- Distinguish between shipping and billing addresses
- Display itemized order summary (items, subtotal, taxes, shipping, total)
- Handle basic payment failures with clear error messages
- Send detailed confirmation email with order number, items, total, tracking link
- Show estimated delivery date range
- Accept terms and conditions before payment

**Definition of done:**
- Guest can complete checkout with confidence
- Common errors (bad address, invalid card) are caught with helpful guidance
- Confirmation email contains all needed order information
- Tracking information is available immediately after confirmation

---

### Slice 3: Frictionless Entry
**Goal:** Reduce friction in the Provide Shipping and Provide Payment activities.

**Stories:**
- Auto-fill city/state when postcode is entered
- Show address confirmation dialog before accepting
- Offer delivery instructions input (doorbell, signature, etc.)
- Display payment method icons/logos
- Validate card details in real-time
- Option to use billing address same as shipping
- Securely tokenize card (PCI compliance)
- Show security badges and trust signals before payment

**Definition of done:**
- Checkout time reduced by 30% for typical guest
- Address validation prevents misdeliveries
- Payment entry is clearly secure

---

### Slice 4: Smart & Contextual
**Goal:** Add intelligence and convenience features to key activities.

**Stories:**
- Apply discount/coupon codes with validation and error handling
- Show inventory status (in stock, limited stock, backordered) during review
- Allow guest to edit cart items (quantity, options) without restarting checkout
- Display estimated delivery date based on address and shipping method
- Collect marketing consent with clear opt-in/opt-out options
- Show related product recommendations on confirmation page
- Generate downloadable receipt/invoice
- Provide downloadable order summary (PDF)

**Definition of done:**
- Discount codes work reliably and show savings
- Guests can make changes without losing progress
- Confirmation provides all information needed for fulfillment and customer service

---

### Slice 5: Digital Wallets & Advanced Methods
**Goal:** Support faster payment methods and international checkout.

**Stories:**
- Support Apple Pay / Google Pay / payment buttons
- Handle international shipping with country selection
- Support PayPal or similar third-party payment methods
- Offer split payment across multiple payment methods
- Store payment method securely for return guests (with explicit consent)
- Calculate international taxes and duties estimates

**Definition of done:**
- Guests can pay with preferred methods
- International guests can enter shipping address and calculate costs
- Stored payment methods work for returning guests

---

## Validation Checklist

- [x] **Backbone completeness** — covers full journey: Review Cart → Shipping → Payment → Confirm → Complete → Confirmation
- [x] **No orphan stories** — every story sits under an activity
- [x] **Walking skeleton coverage** — one story per activity in the skeleton
- [x] **Story independence** — each story can be built and deployed without dependencies (except foundation stories)
- [x] **Edge cases represented** — address validation, payment failures, discount codes, shipping methods all included
- [x] **Each slice is independently shippable** — walking skeleton works end-to-end; MVP adds completeness; enhancements improve specific areas
- [x] **Priority reflects vertical position** — happy path at top; edge cases and nice-to-haves below

## Notes

**Key Risks:**
- Payment failures must be handled gracefully (Slice 2, not Slice 1)
- Address validation is critical to prevent shipping failures (Slice 2, not Slice 1)
- PCI compliance constraints tokenization and data handling (design upfront in Slice 2)

**Dependencies:**
- Walking skeleton assumes inventory system exists and can provide item details
- Shipping calculations depend on rates API or configuration
- Email sending system must be available before Slice 1 ships
- Payment processor integration must be complete before Slice 1

**Out of Scope:**
- Account creation (guest stays guest)
- Order modifications after confirmation (separate returns/customer service flow)
- Gift messaging, gift wrapping, or special options
- Subscription or recurring checkout

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.0/18.0 (83%) |
| Evaluated | 2026-05-04 |
| Target duration | 35510 ms |
| Target cost | $0.0609 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires a backbone of activities as verb phrases (3-7 activities), not features or nouns | PASS | Backbone row in the grid and chat response list: 'Review Cart → Provide Shipping → Provide Payment → Confirm & Pay → Receive Confirmation' — five verb-phrase activities, not nouns like 'Cart' or 'Payment Page'. |
| c2 | Skill defines a walking skeleton as the thinnest end-to-end slice touching every backbone activity — and explicitly distinguishes it from the MVP | PASS | Artifact has 'Slice 1: Walking Skeleton' and 'Slice 2: MVP' as separately named and described release slices. Chat response explicitly states 'Slice 1 is thin but complete — every activity is touched, flow end-to-end, but minimal features'. |
| c3 | Skill requires tasks to be ordered top-to-bottom by priority — rows below the happy path are less critical than rows above | PASS | Grid rows are ordered Backbone → Walking Skeleton → MVP → Enhancement → Future, with validation checklist item: 'Priority reflects vertical position — happy path at top; edge cases and nice-to-haves below'. |
| c4 | Skill prohibits orphan stories — every task must sit under a backbone activity | PASS | Validation checklist includes: 'No orphan stories — every story sits under an activity'. The Markdown table structure enforces all tasks to be placed under a column headed by a backbone activity. |
| c5 | Skill requires each release slice to touch every backbone activity — a slice covering only one activity is not valid | FAIL | Slice 3 goal explicitly says 'Reduce friction in the Provide Shipping and Provide Payment activities' with no stories for Review Cart, Confirm & Pay, or Receive Confirmation. Slice 5 ('Digital Wallets & Advanced Methods') similarly focuses on Payment and Shipping with no coverage of Review Cart or Receive Confirmation. The skill does not enforce this rule. |
| c6 | Skill includes a validation checklist (backbone completeness, walking skeleton coverage, story independence, edge case coverage) | PASS | Artifact has a '## Validation Checklist' section with checked items for backbone completeness, no orphan stories, walking skeleton coverage, story independence, edge cases represented, independently shippable slices, and priority ordering. |
| c7 | Skill specifies that each task must be independently deliverable — partial credit if this is mentioned as a goal but not enforced as a rule | PARTIAL | Validation checklist states 'Story independence — each story can be built and deployed without dependencies (except foundation stories)' — the caveat '(except foundation stories)' and a separate Notes section listing explicit dependencies (inventory system, payment processor, email system) indicate this is a goal with acknowledged exceptions rather than a strict rule. |
| c8 | Skill produces a 2D grid output (activities as columns, tasks as rows by priority) not a flat list | PASS | Artifact contains a Markdown table under '## Story Map' with backbone activities as column headers (Review Cart, Provide Shipping, Provide Payment, Confirm & Pay, Receive Confirmation) and rows ordered by priority (Backbone, Walking Skeleton, MVP, Enhancement, Future). |
| c9 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output includes only a chat response and the output artifact (story-map-guest-checkout.md). Neither contains the skill definition file or its YAML frontmatter. No explicit evidence of name, description, or argument-hint fields is present. |
| c10 | Output's backbone covers the guest checkout flow as 3-7 verb-phrase activities — e.g. "Review cart", "Enter delivery details", "Choose payment method", "Confirm order", "Receive confirmation" — not nouns like "Cart" or "Payment page" | PASS | Backbone activities in the grid and chat: 'Review Cart \| Provide Shipping \| Provide Payment \| Confirm & Pay \| Receive Confirmation' — five verb-phrase activities covering the full flow, none are bare nouns. |
| c11 | Output's walking skeleton is a thinnest end-to-end slice — touching every backbone activity with the minimum task per — e.g. cart with 1 item, hardcoded delivery address, single payment method, basic confirmation — explicitly distinct from the MVP | PASS | Walking Skeleton row touches all five activities with one minimal task each: 'View cart items and total', 'Enter shipping address', 'Enter card details', 'Display order summary with all costs', 'Show confirmation page'. Slice 1 definition of done states 'A guest can complete checkout from cart review to confirmation' and is explicitly a separate named slice from 'Slice 2: MVP'. |
| c12 | Output's tasks under each backbone activity are ordered top-to-bottom by priority — must-have at the top (within the walking skeleton), nice-to-have below — and the priority is visible in the grid layout | PASS | Grid rows progress from Walking Skeleton (must-have, top) → MVP → Enhancement → Future (nice-to-have, bottom). Validation checklist item confirms: 'Priority reflects vertical position — happy path at top; edge cases and nice-to-haves below'. |
| c13 | Output's release slices each touch ALL backbone activities — never a slice that only adds payment methods without touching cart / delivery / confirmation; if a single-activity enhancement is needed it's an iteration, not a release slice | FAIL | Slice 3 ('Frictionless Entry') goal states 'Reduce friction in the Provide Shipping and Provide Payment activities' — stories only cover address auto-fill, delivery instructions, card validation, billing address, and security badges with no stories for Review Cart, Confirm & Pay, or Receive Confirmation. Slice 5 ('Digital Wallets') similarly omits Review Cart, Confirm & Pay, and Receive Confirmation activities. |
| c14 | Output explicitly excludes orphan stories — every task is under one backbone activity; no "miscellaneous" or "support" categories | PASS | All tasks in the artifact are placed under one of the five backbone activity columns in the grid table. There is no 'miscellaneous' or 'support' category. Validation checklist explicitly confirms 'No orphan stories — every story sits under an activity'. |
| c15 | Output's validation checklist confirms backbone completeness (no gaps in the activity sequence), walking skeleton coverage, story independence (one task per release doesn't depend on a parallel task), and edge case coverage (failed payment, abandoned cart, address validation failure) | PASS | Checklist contains: 'Backbone completeness — covers full journey: Review Cart → Shipping → Payment → Confirm → Complete → Confirmation', 'Walking skeleton coverage — one story per activity in the skeleton', 'Story independence — each story can be built and deployed without dependencies', 'Edge cases represented — address validation, payment failures, discount codes, shipping methods all included'. |
| c16 | Output's grid layout has activities as column headers and tasks as rows ordered by priority — visible as a Markdown table or ASCII grid, not a flat list of tasks under each activity | PASS | The artifact's '## Story Map' section is a Markdown table with five activity column headers and rows labeled Backbone, Walking Skeleton, MVP, Enhancement, Future — a clear 2D grid, not a flat list. |
| c17 | Output identifies edge-case scenarios as explicit tasks lower in the grid — e.g. "card declined retry path", "out-of-stock during checkout", "delivery address outside service area" — not omitted because they're complex | PASS | MVP row includes 'Validate address' (Provide Shipping) and 'Validate card' (Provide Payment); Enhancement row includes 'Inventory status per item' (Review Cart); Slice 2 stories include 'Handle basic payment failures with clear error messages'. Notes section also flags payment failures and address validation as key risks. Edge cases are present in lower rows, not omitted. |
| c18 | Output addresses the GUEST aspect specifically — what's different from authenticated checkout (no saved addresses, no order history, possible account-creation prompt at the end) — relevant tasks per activity | PASS | User framing specifies 'purchase without creating an account'. Scope boundary 'Excludes account creation'. Slice 1 definition of done: 'System accepts guest email without account creation'. 'Save address for future orders' placed in Future slice, acknowledging guests have no saved addresses. Out of Scope lists 'Account creation (guest stays guest)'. The guest-specific path is woven throughout. |
| c19 | Output addresses task independence — each task is described to be deliverable on its own, with the rule that one task should not require a parallel task in another activity to complete | PARTIAL | Validation checklist states 'Story independence — each story can be built and deployed without dependencies (except foundation stories)' — explicitly mentioned as a goal. However, the caveat and a separate Dependencies section listing 'Walking skeleton assumes inventory system exists', 'Payment processor integration must be complete before Slice 1', 'Email sending system must be available' indicate it is a stated goal, not an enforced rule. |

### Notes

The output is a strong story map artifact that correctly implements the backbone as verb phrases, clearly distinguishes the walking skeleton from the MVP, produces a proper 2D Markdown grid, and includes a complete validation checklist. The main failure points are: (1) release slices 3 and 5 explicitly scope to only one or two backbone activities rather than spanning all five, violating the 'each slice touches every activity' rule (both c5 and c13 fail on the same evidence); (2) the skill definition's YAML frontmatter cannot be confirmed from the captured output. The guest-specific framing is well handled throughout. Task independence is mentioned but caveated, earning partial credit on both c7 and c19. Overall the artifact demonstrates strong story mapping practice with the notable structural gap in later release slices not spanning the full activity backbone.
