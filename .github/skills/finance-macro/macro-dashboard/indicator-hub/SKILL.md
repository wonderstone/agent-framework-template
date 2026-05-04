---
name: indicator-hub
description: Multi-indicator macroeconomic snapshot with composite recession risk scoring. Fetches GDP growth, CPI inflation, unemployment rate, PMI, retail sales, industrial production, and leading indicators from FRED.
category: finance-macro
domain: macro-dashboard
allowed-tools: Bash(python3:*) Read(*)
---

# Indicator Hub — Macroeconomic Snapshot

## Purpose

Generate a multi-indicator macroeconomic snapshot with composite scoring. Combines growth, inflation, labor, and financial condition indicators into a unified assessment with a recession probability score based on leading indicator convergence.

## When to Use

- Quick macro health check
- Recession probability assessment
- Dashboard-style summary for a specific country (default: US)
- Before any deeper macro analysis — always start here

## Key Indicator Dashboard

### Growth Signals (6 indicators)

| Indicator | FRED Code | Frequency | Expansion Signal | Recession Signal |
|-----------|-----------|-----------|-----------------|-----------------|
| Real GDP (QoQ annualized) | GDPC1 | Quarterly | >2% | <0% |
| Industrial Production (YoY) | INDPRO | Monthly | >2% | <0% |
| Retail Sales (YoY) | RSAFS | Monthly | >3% | <0% |
| ISM Manufacturing PMI | NAPM | Monthly | >50 | <45 |
| Capacity Utilization | TCU | Monthly | >78% | <75% |
| Real Personal Income | DSPIC96 | Monthly | >2% | <0% |

### Inflation Signals (4 indicators)

| Indicator | FRED Code | Frequency | Low Risk | High Risk |
|-----------|-----------|-----------|---------|-----------|
| Core PCE (YoY) | PCEPILFE | Monthly | <2.5% | >3.5% |
| Core CPI (YoY) | CPILFESL | Monthly | <3% | >4% |
| PPI (YoY) | PPIACO | Monthly | <3% | >5% |
| 5y5y Inflation Swap | T5YIFR | Daily | <2.5% | >3% |

### Labor Signals (5 indicators)

| Indicator | FRED Code | Frequency | Strong | Weak |
|-----------|-----------|-----------|--------|------|
| Unemployment Rate | UNRATE | Monthly | <4.5% | >6% |
| Nonfarm Payrolls (3-mo avg) | PAYEMS | Monthly | >150K | <50K |
| Initial Claims (4-wk avg) | ICSA | Weekly | <250K | >300K |
| JOLTS Openings | JTSJOL | Monthly | >8M | <6M |
| Wage Growth (YoY) | CES0500000003 | Monthly | <4% | >5% or <2% |

### Financial Conditions (4 indicators)

| Indicator | FRED Code | Frequency | Easy | Tight |
|-----------|-----------|-----------|------|-------|
| Fed Funds Rate | FEDFUNDS | Daily | — | — |
| 10Y-2Y Spread | T10Y2Y | Daily | >0.5% | <0% |
| BBB Spread | BAA10Y | Daily | <2% | >3% |
| VIX | VIXCLS | Daily | <20 | >30 |

## Composite Scoring

Each indicator is scored -1 (recessionary), 0 (neutral), or +1 (expansionary).

```
Recession_Probability = f(
  Growth_Score (0-6 scaled to 0-100 inverted),
  Labor_Score (0-5 scaled to 0-100 inverted),
  Financial_Score (0-4 scaled to 0-100 inverted),
  Leading_Index_Score (0-3 scaled to 0-100 inverted)
)
```

- **<20%**: Low recession risk — expansion intact
- **20-40%**: Elevated risk — monitor closely
- **40-60%**: High risk — prepare for downturn
- **>60%**: Recession likely within 6-12 months

## Process

```bash
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"GDPC1","limit":8,"frequency":"q"}'
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"UNRATE","limit":12}'
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"PCEPILFE","limit":12}'
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"T10Y2Y","limit":30}'
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"PAYEMS","limit":12}'
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"ICSA","limit":12}'
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"BAA10Y","limit":12}'
```

## Red Flags
- GDP is revised 3 times — initial release is least reliable
- PMI ≠ actual output, it's sentiment (can be wrong at turning points)
- Wage growth is a lagging indicator, not leading
- VIX can spike without triggering recession (1987, 2010, 2018)
- No single indicator has a perfect track record — composite matters
