---
name: threat-model
description: Create a threat model using STRIDE — identify threats, attack surfaces, and mitigations for a system or feature.
argument-hint: "[system, feature, or architecture to model]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Create a threat model for $ARGUMENTS using STRIDE.

## Process

1. **Scope** — what system/feature is being modelled? What are the trust boundaries?
2. **Data flows** — how does data enter, move through, and leave the system?
3. **STRIDE analysis** — for each component and data flow:

| Threat | Question |
|---|---|
| **Spoofing** | Can someone pretend to be another user/service? |
| **Tampering** | Can someone modify data in transit or at rest? |
| **Repudiation** | Can someone deny performing an action? |
| **Information Disclosure** | Can someone access data they shouldn't? |
| **Denial of Service** | Can someone make the system unavailable? |
| **Elevation of Privilege** | Can someone gain access beyond their role? |

4. **Risk assessment** — likelihood × impact for each threat
5. **Mitigations** — what controls address each threat?

## Output

A threat model document with: scope diagram, threat table (STRIDE category, threat, risk, mitigation, status), and prioritised action items.
