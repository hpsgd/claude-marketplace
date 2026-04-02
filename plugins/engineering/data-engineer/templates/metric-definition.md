# Metric Definition Template

Based on the Metrics Layer pattern used by dbt, Airbnb's Minerva, and the OpenTelemetry Semantic Conventions.

---

## Metric: {metric_name}

### Definition
- **Description:** {One sentence — what this metric measures}
- **Business question:** {What decision does this metric inform?}
- **Owner:** {Who is accountable for the definition — name or role}
- **Status:** Draft | Reviewed | Approved | Deprecated

### Calculation
- **Formula:** {Exact calculation, e.g., `COUNT(DISTINCT user_id WHERE event = 'session_started' AND event_date BETWEEN start AND end)`}
- **Numerator:** {If a ratio — what's on top}
- **Denominator:** {If a ratio — what's on the bottom}
- **Aggregation:** {SUM / COUNT / COUNT DISTINCT / AVG / PERCENTILE}
- **Grain:** {Per user / per session / per day / per cohort}
- **Time window:** {Rolling 7-day / calendar month / since signup / trailing 30 days}

### Filters
- **Included:** {What's counted — e.g., "All users with at least one session"}
- **Excluded:** {What's NOT counted — e.g., "Test accounts, internal users, bots"}
- **Segmentation:** {How this metric can be sliced — by plan, by region, by cohort}

### Data Source
- **Source system:** {Production database / event stream / third-party API}
- **Source table(s):** {Exact table or event names}
- **Freshness:** {Real-time / hourly / daily batch}
- **Lineage:** {Source → transform → destination path}

### Targets and Thresholds
- **Current baseline:** {What the metric is today — with date}
- **Target:** {What we're aiming for — with timeframe}
- **Alert threshold:** {When to flag — e.g., ">20% deviation from 7-day average"}
- **Direction:** {Higher is better / Lower is better / Target range}

### Caveats
- {What could make this number misleading — e.g., "Includes free trial users who may not convert"}
- {Seasonal effects — e.g., "Drops during holiday periods"}
- {Known data quality issues — e.g., "Mobile events may be delayed by up to 24h"}

### History
| Date | Change | Reason |
|---|---|---|
| {YYYY-MM-DD} | {What changed in the definition} | {Why it changed} |
