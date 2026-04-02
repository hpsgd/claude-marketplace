# Test Strategy: [Project / Feature Name]

| Field | Value |
|---|---|
| **Author** | [Name] |
| **Version** | [e.g. 1.0] |
| **Date** | [YYYY-MM-DD] |
| **Status** | Draft / In Review / Approved |

## Scope & Objectives

### What is Being Tested

[One-paragraph description of the feature, service, or system under test]

### Quality Goals

- [e.g. Zero critical/high defects at release]
- [e.g. 80%+ code coverage on changed code]
- [e.g. All critical user flows pass E2E tests]
- [e.g. No P1/P2 accessibility violations]

## Risk Assessment

### Risk Matrix

| Risk | Likelihood | Impact | Risk Level | Test Priority |
|---|---|---|---|---|
| [e.g. Payment processing fails] | [H/M/L] | [H/M/L] | [Critical/High/Medium/Low] | [Test first / thorough / basic / defer] |
| [e.g. Data loss on concurrent writes] | [H/M/L] | [H/M/L] | [Critical/High/Medium/Low] | [Test first / thorough / basic / defer] |

### Risk-Based Test Prioritisation

1. [Highest-risk area — describe what to test most thoroughly and why]
2. [Second-highest risk area]
3. [Lower-risk areas that still need coverage]

## Test Levels

| Level | Scope | Tools | Coverage Target | Entry Criteria | Exit Criteria |
|---|---|---|---|---|---|
| **Unit** | Functions, business logic, transformations | [e.g. Vitest, xUnit, pytest] | [e.g. 80%+ changed code] | Code compiles, tests written | All pass, coverage met |
| **Integration** | Component boundaries, API contracts, DB queries | [e.g. Testcontainers, MSW, httpx] | [e.g. All API endpoints] | Unit tests pass | All contract tests pass |
| **E2E** | Critical user flows, cross-service workflows | [e.g. Playwright, Cypress] | [e.g. Top 5 user journeys] | Integration tests pass, env deployed | All critical flows pass |
| **Contract** | API compatibility between services | [e.g. Pact, Specmatic] | [e.g. All inter-service APIs] | Schemas defined | No breaking changes |
| **Performance** | Latency, throughput, resource usage | [e.g. k6, Locust, Artillery] | [e.g. p95 < 200ms] | Functional tests pass | Budgets met |
| **Security** | Vulnerabilities, auth, injection | [e.g. OWASP ZAP, Snyk, manual review] | [e.g. OWASP Top 10] | Feature complete | No critical/high findings |

## Test Types

- **Functional:** Verify features work as specified against acceptance criteria
- **Regression:** Ensure existing functionality is not broken by changes
- **Smoke:** Quick sanity check after deployment — critical path only
- **Exploratory:** Time-boxed manual testing focused on risk areas and edge cases
- **Accessibility:** Automated and manual checks against [WCAG 2.1 AA](https://www.w3.org/WAI/WCAG21/quickref/)
- **Security:** Vulnerability scanning and manual review per security-review skill

## Environment Requirements

| Environment | Purpose | Data | Service Dependencies |
|---|---|---|---|
| Local | Unit + integration tests | Fixtures / in-memory | [Mocked / containerised] |
| CI | Automated test suite | Seeded test data | [Containerised / stubs] |
| Staging | E2E, performance, exploratory | Production-like (anonymised) | [Live dependencies / sandboxes] |
| Production | Smoke tests, monitoring | Real data | [Live] |

## Defect Management

| Severity | Definition | Response Time | Examples |
|---|---|---|---|
| **Critical** | System unusable, data loss, security breach | [e.g. Immediate fix, hotfix release] | [e.g. Auth bypass, data corruption] |
| **High** | Major feature broken, no workaround | [e.g. Fix within current sprint] | [e.g. Checkout fails, API 500s] |
| **Medium** | Feature impaired, workaround exists | [e.g. Fix within next sprint] | [e.g. Incorrect calculation, UI glitch] |
| **Low** | Cosmetic, minor inconvenience | [e.g. Backlog] | [e.g. Typo, alignment issue] |

**Lifecycle:** New → Triaged → In Progress → Fixed → Verified → Closed

## Quality Gates

### Pre-Merge (Pull Request)

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Code coverage meets target on changed files
- [ ] No new critical/high static analysis findings
- [ ] Security scan passes (no critical/high vulnerabilities)

### Pre-Release

- [ ] All E2E tests pass on staging
- [ ] Performance budgets met
- [ ] Exploratory testing session completed
- [ ] Accessibility audit passes
- [ ] No open critical/high defects

## Metrics & Reporting

| Metric | Target | Reporting Cadence |
|---|---|---|
| Test pass rate | [e.g. 100% on main] | [Per CI run] |
| Code coverage (changed code) | [e.g. 80%+] | [Per PR] |
| Defect escape rate | [e.g. < 5% to production] | [Per release] |
| Mean time to detect (MTTD) | [e.g. < 1 hour for critical] | [Weekly] |
| Flaky test rate | [e.g. < 2%] | [Weekly] |

## Tool Stack

| Test Level | Tool | Version | Configuration |
|---|---|---|---|
| Unit | [e.g. Vitest / xUnit / pytest] | [Version] | [Config file path or key settings] |
| Integration | [e.g. Testcontainers / MSW] | [Version] | [Config file path or key settings] |
| E2E | [e.g. Playwright / Cypress] | [Version] | [Config file path or key settings] |
| Performance | [e.g. k6 / Locust] | [Version] | [Config file path or key settings] |
| Security | [e.g. Snyk / OWASP ZAP] | [Version] | [Config file path or key settings] |
| Accessibility | [e.g. axe-core / Lighthouse] | [Version] | [Config file path or key settings] |
