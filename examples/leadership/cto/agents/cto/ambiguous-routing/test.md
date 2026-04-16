# Test: Ambiguous routing between architect and developer

Scenario: A request that blurs the line between architecture decision and implementation task. The CTO must decide whether to send this to the architect, a developer, or both, and in what order.

## Prompt

We need to add rate limiting to our API. We're getting hammered by a few customers doing bulk imports and it's degrading performance for everyone else. Not sure if this is an architecture decision about how rate limiting should work across our services, or just an implementation task for the backend developer.

## Criteria

- [ ] PASS: CTO reads the request fully before classifying — doesn't jump to delegation
- [ ] PASS: CTO produces a trade-off summary before delegating (architecture-level design vs implementation-level fix)
- [ ] PASS: CTO correctly identifies this as needing BOTH — architect for the rate limiting strategy across services, developer for implementation
- [ ] PASS: Delegation to architect specifies the right skill (system-design for cross-service rate limiting strategy)
- [ ] PASS: Delegation sequence is correct — architect first (strategy), then developer (implementation)
- [ ] PARTIAL: CTO identifies that the immediate performance issue may need a quick fix before the architectural solution
- [ ] PASS: Delegation includes clear scope boundaries — what the architect decides vs what the developer decides
- [ ] PASS: ADR is included as a required deliverable for the rate limiting strategy decision
