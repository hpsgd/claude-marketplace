---
name: health-assessment
description: "Assess customer health across product adoption, engagement, relationship, value realisation, and commercial dimensions. Use to identify at-risk accounts or portfolio-level health."
argument-hint: "[customer name, segment, or 'portfolio' for all accounts]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Assess customer health for $ARGUMENTS using the five-dimension health score framework defined in the customer-success agent. Score each dimension 0-100, calculate weighted composite, classify as Healthy/Neutral/At Risk/Critical, and recommend specific interventions for any account below 60.
