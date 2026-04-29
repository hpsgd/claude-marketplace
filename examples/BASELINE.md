# Baseline evaluation report (post-augmentation)

Captured for caveman-spike comparison. Each `result.md` has the full evaluation; this file aggregates verdicts and scores against the new `## Output expectations` rubric.

| Field | Value |
|---|---|
| Run date | 2026-04-29 |
| Total | 172 tests |
| PASS | 76 |
| PARTIAL | 86 |
| FAIL | 10 |
| Score range | 56%-100% |
| Average | 88.0% |
| Median | 91% |

## Results

| Test | Type | Verdict | Score |
|---|---|---|---|
| engineering/ai-engineer/agents/ai-engineer/rag-design | agent | PARTIAL | 13/18 (72%) |
| engineering/ai-engineer/skills/model-evaluation | skill | PARTIAL | 15.5/18 (86%) |
| engineering/ai-engineer/skills/prompt-design | skill | PARTIAL | 14.5/18 (81%) |
| engineering/ai-engineer/skills/rag-pipeline | skill | PARTIAL | 17/19 (90%) |
| engineering/architect/agents/architect/system-design-request | agent | PARTIAL | 16/19 (84%) |
| engineering/architect/skills/api-design | skill | PASS | 18.5/19 (97%) |
| engineering/architect/skills/evaluate-technology | skill | PASS | 16.5/17 (97%) |
| engineering/architect/skills/system-design | skill | PARTIAL | 17/18 (94%) |
| engineering/architect/skills/write-adr | skill | PASS | 16.5/17 (97%) |
| engineering/code-reviewer/agents/code-reviewer/review-with-issues | agent | PARTIAL | 14.0/17 (82%) |
| engineering/code-reviewer/skills/code-review | skill | PASS | 16.5/17 (97%) |
| engineering/code-reviewer/skills/pr-create | skill | PASS | 16.5/17 (97%) |
| engineering/data-engineer/agents/data-engineer/pipeline-design | agent | PARTIAL | 16.5/19 (87%) |
| engineering/data-engineer/skills/data-model | skill | PARTIAL | 14.5/19 (76%) |
| engineering/data-engineer/skills/event-tracking-plan | skill | PARTIAL | 17/19 (90%) |
| engineering/data-engineer/skills/write-query | skill | PARTIAL | 17/19 (89%) |
| engineering/devops/agents/devops/deployment-strategy | agent | PARTIAL | 14/18 (78%) |
| engineering/devops/skills/incident-response | skill | PASS | 19.5/20 (98%) |
| engineering/devops/skills/write-dockerfile | skill | PASS | 17.5/18 (97%) |
| engineering/devops/skills/write-iac | skill | PASS | 17.5/18 (97%) |
| engineering/devops/skills/write-pipeline | skill | PASS | 17.5/18 (97%) |
| engineering/devops/skills/write-slo | skill | PASS | 16.5/17 (97%) |
| engineering/dotnet-developer/agents/dotnet-developer/endpoint-implementation | agent | PARTIAL | 14.5/19 (76%) |
| engineering/dotnet-developer/skills/write-endpoint | skill | PARTIAL | 14.5/19 (76%) |
| engineering/dotnet-developer/skills/write-handler | skill | PARTIAL | 14.5/19 (76%) |
| engineering/performance-engineer/agents/performance-engineer/bottleneck-investigation | agent | PASS | 18.5/19 (97%) |
| engineering/performance-engineer/skills/capacity-plan | skill | PARTIAL | 16.5/19 (87%) |
| engineering/performance-engineer/skills/load-test-plan | skill | PARTIAL | 14.5/18.5 (78%) |
| engineering/performance-engineer/skills/performance-profile | skill | PARTIAL | 15.5/18 (86%) |
| engineering/python-developer/agents/python-developer/feature-implementation | agent | PARTIAL | 15/19 (79%) |
| engineering/python-developer/skills/write-feature-spec | skill | PASS | 17/18 (94%) |
| engineering/python-developer/skills/write-schema | skill | PARTIAL | 17.5/19 (92%) |
| engineering/qa-engineer/agents/qa-engineer/test-planning | agent | PASS | 18.5/19 (97%) |
| engineering/qa-engineer/skills/generate-tests | skill | PARTIAL | 18/19 (95%) |
| engineering/qa-engineer/skills/write-bug-report | skill | PASS | 16.5/17 (97%) |
| engineering/qa-lead/agents/qa-lead/strategy-review | agent | PARTIAL | 14.5/19 (76%) |
| engineering/qa-lead/skills/test-strategy | skill | PARTIAL | 14.5/19 (76%) |
| engineering/qa-lead/skills/write-acceptance-criteria | skill | PARTIAL | 17.5/19 (92%) |
| engineering/react-developer/agents/react-developer/component-implementation | agent | PASS | 17.5/19 (92%) |
| engineering/react-developer/skills/component-from-spec | skill | PARTIAL | 16/18 (89%) |
| engineering/react-developer/skills/performance-audit | skill | PASS | 14.5/15 (97%) |
| engineering/release-manager/agents/release-manager/release-coordination | agent | PARTIAL | 16.5/19 (87%) |
| engineering/release-manager/skills/release-plan | skill | PASS | 18/18.5 (97%) |
| engineering/release-manager/skills/rollback-assessment | skill | PARTIAL | 16/19 (84%) |
| engineering/security-engineer/agents/prompt-injection-tester/test-llm-endpoint | agent | PASS | 17/18 (94%) |
| engineering/security-engineer/agents/security-engineer/vulnerability-assessment | agent | PASS | 17/17.5 (97%) |
| engineering/security-engineer/skills/dependency-audit | skill | PASS | 16/16.5 (97%) |
| engineering/security-engineer/skills/recon | skill | PASS | 17.5/18 (97%) |
| engineering/security-engineer/skills/security-review | skill | PASS | 15.5/16 (97%) |
| engineering/security-engineer/skills/supply-chain-audit | skill | PASS | 17.5/18 (97%) |
| engineering/security-engineer/skills/threat-model | skill | PARTIAL | 15.5/18 (86%) |
| engineering/security-engineer/skills/web-assessment | skill | PARTIAL | 16.5/18 (92%) |
| engineering/workflow-tools/skills/content-retrieval | skill | PARTIAL | 14/18 (78%) |
| leadership/coordinator/agents/coordinator/cross-domain-conflict | agent | PARTIAL | 12.5/16 (78%) |
| leadership/coordinator/agents/coordinator/cross-domain-dispatch | agent | PARTIAL | 18.5/20 (92%) |
| leadership/coordinator/agents/coordinator/initiative-decomposition | agent | PASS | 17/18 (94%) |
| leadership/coordinator/skills/decompose-initiative | skill | PARTIAL | 15/17 (88%) |
| leadership/coordinator/skills/define-okrs | skill | PASS | 18/18.5 (97%) |
| leadership/coordinator/skills/write-spec | skill | PARTIAL | 17/20 (85%) |
| leadership/cpo/agents/cpo/product-prioritisation | agent | PASS | 16.5/17.5 (94%) |
| leadership/cto/agents/cto/ambiguous-routing | agent | PARTIAL | 10.5/15 (70%) |
| leadership/cto/agents/cto/incident-coordination | agent | PASS | 14.5/16 (91%) |
| leadership/cto/agents/cto/technical-decision | agent | PARTIAL | 16.5/18.5 (89%) |
| leadership/grc-lead/agents/grc-lead/compliance-scope | agent | PARTIAL | 14.5/18 (81%) |
| leadership/grc-lead/skills/ai-governance-review | skill | PASS | 19/20 (95%) |
| leadership/grc-lead/skills/compliance-audit | skill | PARTIAL | 17/20 (85%) |
| leadership/grc-lead/skills/risk-assessment | skill | PASS | 19/20 (95%) |
| leadership/grc-lead/skills/write-dpia | skill | PASS | 19.5/20 (98%) |
| practices/coding-standards/skills/review-dotnet | skill | PASS | 18.5/19 (97%) |
| practices/coding-standards/skills/review-git | skill | PASS | 16/16.5 (97%) |
| practices/coding-standards/skills/review-python | skill | PASS | 16.5/17 (97%) |
| practices/coding-standards/skills/review-standards | skill | PARTIAL | 14.5/17 (85%) |
| practices/coding-standards/skills/review-typescript | skill | PASS | 17/18 (94%) |
| practices/plugin-curator/agents/plugin-curator/audit-request | agent | PASS | 16.5/17 (97%) |
| practices/plugin-curator/skills/audit-agent | skill | PASS | 16.5/17 (97%) |
| practices/plugin-curator/skills/audit-skill | skill | PASS | 16/18 (89%) |
| practices/plugin-curator/skills/create-agent | skill | PARTIAL | 16.5/17.5 (94%) |
| practices/plugin-curator/skills/create-skill | skill | PARTIAL | 16/17 (94%) |
| practices/security-compliance/skills/security-audit | skill | PASS | 16.5/17 (97%) |
| practices/thinking/skills/algorithm | skill | PASS | 17/17.5 (97%) |
| practices/thinking/skills/council | skill | PASS | 17/17.5 (97%) |
| practices/thinking/skills/creative | skill | PASS | 13.5/14 (96%) |
| practices/thinking/skills/first-principles | skill | PASS | 15.5/17 (91%) |
| practices/thinking/skills/health-check | skill | PASS | 16/18 (89%) |
| practices/thinking/skills/isc | skill | PARTIAL | 13.5/18 (75%) |
| practices/thinking/skills/iterative-depth | skill | PASS | 17.5/18 (97%) |
| practices/thinking/skills/learning | skill | PARTIAL | 13.5/16 (84%) |
| practices/thinking/skills/propose-improvement | skill | PASS | 16.5/17 (97%) |
| practices/thinking/skills/reconcile-rules | skill | PASS | 17/17 (100%) |
| practices/thinking/skills/red-team | skill | PASS | 17.5/18 (97%) |
| practices/thinking/skills/retrospective | skill | PASS | 17.5/18 (97%) |
| practices/thinking/skills/review-settings | skill | PASS | 17/17 (100%) |
| practices/thinking/skills/scientific-method | skill | PARTIAL | 16.5/18 (92%) |
| practices/thinking/skills/wisdom | skill | PARTIAL | 12.5/15.5 (81%) |
| practices/writing-style/skills/style-guide | skill | PARTIAL | 15.5/18 (86%) |
| product/customer-success/agents/customer-success/account-review | agent | PASS | 16.5/17 (97%) |
| product/customer-success/skills/churn-analysis | skill | PARTIAL | 12.5/14 (89%) |
| product/customer-success/skills/expansion-plan | skill | PARTIAL | 12.5/17 (74%) |
| product/customer-success/skills/expansion-plan-healthy | skill | FAIL | 9.5/17 (56%) |
| product/customer-success/skills/health-assessment | skill | FAIL | 11.5/18 (64%) |
| product/customer-success/skills/write-onboarding-playbook | skill | PASS | 18/18.5 (97%) |
| product/customer-success/skills/write-qbr | skill | PARTIAL | 16/18 (89%) |
| product/developer-docs-writer/agents/developer-docs-writer/api-documentation | agent | PASS | 17.5/18 (97%) |
| product/developer-docs-writer/skills/write-api-docs | skill | FAIL | 12.5/18 (69%) |
| product/developer-docs-writer/skills/write-integration-guide | skill | PARTIAL | 11.5/18 (64%) |
| product/developer-docs-writer/skills/write-migration-guide | skill | PASS | 17.5/19 (92%) |
| product/developer-docs-writer/skills/write-sdk-guide | skill | PARTIAL | 14.5/18 (81%) |
| product/gtm/agents/gtm/launch-strategy | agent | PASS | 16.5/17 (97%) |
| product/gtm/skills/competitive-analysis | skill | PARTIAL | 16/18 (89%) |
| product/gtm/skills/launch-plan | skill | PARTIAL | 13.5/18 (75%) |
| product/gtm/skills/positioning | skill | PASS | 17.5/18 (97%) |
| product/gtm/skills/write-battle-card | skill | PARTIAL | 14/17 (82%) |
| product/gtm/skills/write-battle-card-enterprise | skill | PARTIAL | 15.5/18 (86%) |
| product/internal-docs-writer/agents/internal-docs-writer/runbook-creation | agent | PARTIAL | 14/18 (78%) |
| product/internal-docs-writer/skills/write-architecture-doc | skill | PARTIAL | 16/19 (84%) |
| product/internal-docs-writer/skills/write-changelog | skill | PARTIAL | 14.5/17 (85%) |
| product/internal-docs-writer/skills/write-runbook | skill | FAIL | 11.5/18 (64%) |
| product/product-owner/agents/product-owner/backlog-prioritisation | agent | PASS | 17.5/18 (97%) |
| product/product-owner/skills/groom-backlog | skill | FAIL | 11.5/17 (68%) |
| product/product-owner/skills/write-jtbd | skill | PARTIAL | 15.5/18 (86%) |
| product/product-owner/skills/write-prd | skill | PARTIAL | 17/19 (89%) |
| product/product-owner/skills/write-story-map | skill | PASS | 18/19 (95%) |
| product/product-owner/skills/write-user-story | skill | PASS | 17/18 (94%) |
| product/support/agents/support/ticket-handling | agent | PARTIAL | 16/17.5 (91%) |
| product/support/skills/feedback-synthesis | skill | PARTIAL | 14.5/18 (81%) |
| product/support/skills/triage-tickets | skill | PARTIAL | 15.5/18 (86%) |
| product/support/skills/write-kb-article | skill | PARTIAL | 14/18 (78%) |
| product/ui-designer/agents/designer/component-design | agent | PASS | 17.5/18 (97%) |
| product/ui-designer/skills/accessibility-audit | skill | FAIL | 12.5/18 (69%) |
| product/ui-designer/skills/component-spec | skill | PASS | 17/18 (94%) |
| product/ui-designer/skills/component-spec-complex | skill | PASS | 17/18 (94%) |
| product/ui-designer/skills/design-review | skill | FAIL | 12/18 (67%) |
| product/ui-designer/skills/design-tokens | skill | PASS | 16.5/17 (97%) |
| product/ui-designer/skills/design-tokens-audit | skill | FAIL | 12.5/18 (69%) |
| product/user-docs-writer/agents/user-docs-writer/complex-task-guide | agent | PARTIAL | 14/17 (82%) |
| product/user-docs-writer/agents/user-docs-writer/help-article | agent | PARTIAL | 13.0/16.5 (79%) |
| product/user-docs-writer/skills/content-strategy | skill | PARTIAL | 14/18 (78%) |
| product/user-docs-writer/skills/write-kb-article | skill | PASS | 16/17 (94%) |
| product/user-docs-writer/skills/write-onboarding | skill | PARTIAL | 12.5/18 (69%) |
| product/user-docs-writer/skills/write-onboarding-technical | skill | PARTIAL | 14/18 (78%) |
| product/user-docs-writer/skills/write-user-guide | skill | PARTIAL | 12.5/17 (74%) |
| product/ux-researcher/agents/ux-researcher/research-plan | agent | PARTIAL | 13.5/16 (84%) |
| product/ux-researcher/skills/journey-map | skill | PARTIAL | 14/18 (78%) |
| product/ux-researcher/skills/persona-definition | skill | PASS | 17/18 (94%) |
| product/ux-researcher/skills/service-blueprint | skill | PARTIAL | 17.5/19 (92%) |
| product/ux-researcher/skills/usability-review | skill | PARTIAL | 14.5/17 (85%) |
| product/ux-researcher/skills/usability-test-plan | skill | PASS | 16.5/17 (97%) |
| research/analyst/agents/business-analyst/boundary-individual | agent | FAIL | 9.5/17 (56%) |
| research/analyst/agents/content-analyst/content-evaluation | agent | PASS | 17.5/18 (97%) |
| research/analyst/agents/content-analyst/multi-source-comparison | agent | PASS | 17/17.5 (97%) |
| research/analyst/agents/open-source-researcher/topic-research | agent | PARTIAL | 12.5/17 (74%) |
| research/analyst/skills/company-lookup | skill | FAIL | 11.5/18 (64%) |
| research/analyst/skills/competitive-analysis | skill | PARTIAL | 16.5/19 (87%) |
| research/analyst/skills/content-analysis | skill | PASS | 16.5/17 (97%) |
| research/analyst/skills/deep-research | skill | PASS | 17/17 (100%) |
| research/analyst/skills/due-diligence | skill | PARTIAL | 16/18 (89%) |
| research/analyst/skills/due-diligence-red-signals | skill | PASS | 14.5/15 (97%) |
| research/analyst/skills/market-sizing | skill | PARTIAL | 13/18 (72%) |
| research/analyst/skills/source-credibility | skill | PASS | 19/19 (100%) |
| research/analyst/skills/web-research | skill | PASS | 16.5/16.5 (100%) |
| research/investigator/agents/investigator/gate-enforcement | agent | PASS | 16.5/17 (97%) |
| research/investigator/agents/investigator/legitimate-investigation | agent | PARTIAL | 13.5/17 (79%) |
| research/investigator/agents/osint-analyst/domain-investigation | agent | PARTIAL | 14.5/18 (81%) |
| research/investigator/skills/corporate-ownership | skill | PARTIAL | 17/19 (89%) |
| research/investigator/skills/domain-intel | skill | PARTIAL | 16.5/19 (87%) |
| research/investigator/skills/entity-footprint | skill | PASS | 18/18 (100%) |
| research/investigator/skills/identity-verification | skill | PARTIAL | 16.5/19 (87%) |
| research/investigator/skills/identity-verification-positive | skill | PASS | 18.5/19 (97%) |
| research/investigator/skills/ip-intel | skill | PARTIAL | 17.5/20 (88%) |
| research/investigator/skills/people-lookup | skill | PASS | 18.5/19 (97%) |
| research/investigator/skills/public-records | skill | PARTIAL | 15.5/17 (91%) |
| research/investigator/skills/social-media-footprint | skill | PARTIAL | 16.5/19 (87%) |
