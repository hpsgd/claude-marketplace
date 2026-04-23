---
description: "Review workflow conventions: inline decision markers, proposals in the artifact not in chat"
---

# Review Conventions

## Consolidate review in the artifact

When proposing changes to a document or file, write the proposals into the artifact itself with inline markers. Don't split proposals between chat and the file. Chat scrolls away. The artifact persists.

Use decision markers for changes that need approval:

```markdown
<!-- DECISION: Reword this section to focus on outcomes rather than process. ACCEPT / TWEAK / REJECT? -->
```

The reviewer can respond to each marker in place. Once resolved, strip the markers. This keeps the full review context in the artifact where it belongs, not scattered across a conversation that may not survive the session.

This applies when reviewing specs, documentation, config files, or any structured content where multiple changes need individual sign-off. For code reviews, use PR review comments instead (same principle, different medium).
