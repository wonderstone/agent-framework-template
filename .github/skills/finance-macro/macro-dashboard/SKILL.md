---
name: macro-dashboard
description: Macroeconomic indicator dashboard — GDP, CPI, unemployment, yield curve, PMI, recession probability. 4-dimension composite scoring with FRED + WorldBank data.
category: finance-macro
domain: macro-dashboard
allowed-tools: Bash(python3:*) Read(*)
---

# Macroeconomic Dashboard

## Purpose

On-demand macroeconomic snapshot with composite scoring and recession risk assessment. Aggregates 19 indicators across growth, inflation, labor, and financial conditions into a single composite score.

## How to Use

```bash
# Full pipeline
python3 scripts/orchestrator.py '{"domain":"macro-dashboard","country":"USA"}'

# Individual models
python3 macro-dashboard/scripts/indicator_hub.py --gdp 2.8 --unrate 4.1 --spread -0.25 ...
python3 macro-dashboard/scripts/yield_curve.py --dgs2 4.85 --dgs10 4.55 --dtb3 5.30
```

## Key Signals

**Yield curve**: The single most reliable recession indicator. Every US recession since 1950 was preceded by 10Y-3M inversion. But inversion is a leading indicator, not a timing tool — inversion can last 12-24 months before recession.

**Sahm Rule**: When 3-month average unemployment rate rises 0.50pp above its 12-month low, recession is likely underway. Real-time indicator, not a forecast.

**Composite approach**: Single indicators mislead. Always check the composite across all four dimensions (growth, inflation, labor, financial conditions).

## Red Flags
- Seasonal adjustments matter — always use SA data
- PMI is survey-based and noisy — confirm with hard data (IP, retail sales)
- GDP is backward-looking (1-month lag, revised multiple times)
- Full employment doesn't mean no recession — labor market is a lagging indicator
- Financial conditions can turn on a dime — credit spreads lead equities
