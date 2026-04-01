---
name: write-query
description: Write a SQL query, dbt model, or analytics query to answer a business question.
argument-hint: "[business question to answer, or data to extract]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Write a query to answer: $ARGUMENTS

## Process

1. Clarify the question — what exactly is being measured? What's the time range? What filters apply?
2. Identify the data source — which tables/collections contain the relevant data?
3. Write the query — optimised for readability first, performance second
4. Document assumptions — what edge cases are excluded? What constitutes a "user" or "session"?
5. Validate — does the result make sense? Are there sanity checks? (total should roughly equal sum of parts, percentages should add to ~100%, counts should be within expected range)

## Rules

- Define every metric precisely before querying. "Active users" means nothing without specifying window, qualifying action, and bot exclusion
- CTEs over subqueries for readability
- Comment non-obvious joins and filters
- Include the business question as a comment at the top of the query
