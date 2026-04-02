---
name: churn-analysis
description: "Analyse churn patterns — identify why customers leave, which segments are at risk, and what interventions would have the highest impact on retention."
argument-hint: "[time period, segment, or specific churned accounts to analyse]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Analyse churn for $ARGUMENTS. Identify patterns by segment, tenure, health score at time of churn, last engagement, and common exit reasons. Distinguish voluntary churn (customer chose to leave) from involuntary (payment failure). Recommend top 3 interventions ranked by expected retention impact.
