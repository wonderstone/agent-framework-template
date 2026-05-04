---
name: macro-health
description: Composite macroeconomic health scoring across 7 dimensions — growth, inflation, external, fiscal, financial, labor, and structural. Generates a 0-100 score for any country with radar chart output and peer benchmarking.
category: finance-macro
domain: country-intel
allowed-tools: Bash(python3:*) Read(*)
---

# Macro Health Score

## Purpose

Composite macroeconomic health assessment scored 0-100 across 7 dimensions. Standardized scoring enables cross-country comparison, time-series tracking, and early warning signal detection. Each dimension is scored using 3-5 indicators weighted by relevance to the country's economic structure.

## When to Use

- "How healthy is the [Country] economy?"
- "Macro health score for [Country]?"
- "Compare [Country A] vs [Country B] macro health"
- "Is [Country]'s macro situation improving or deteriorating?"
- Early warning system for economic stress

## 7-Dimension Framework

### 1. Growth (weight: 20%)
| Indicator | Source | Weight |
|-----------|--------|--------|
| Real GDP Growth (3Y avg) | World Bank | 35% |
| GDP per Capita Growth | World Bank | 25% |
| Output Gap Estimate | IMF WEO | 20% |
| PMI Composite | National sources / Markit | 20% |

**Scoring**: > 3% GDP growth = 80-100 | 1-3% = 40-80 | < 1% = 0-40

### 2. Inflation (weight: 15%)
| Indicator | Source | Weight |
|-----------|--------|--------|
| CPI YoY (deviation from target) | National statistics | 40% |
| Core CPI trend (3M ann.) | National statistics | 30% |
| Inflation Expectations (survey/breakeven) | Central bank surveys | 30% |

**Scoring**: At target ±0.5% = 80-100 | ±1-2% off target = 40-80 | > 2% off = 0-40

### 3. External Balance (weight: 15%)
| Indicator | Source | Weight |
|-----------|--------|--------|
| Current Account (% GDP) | IMF IFS | 35% |
| FX Reserves (months of imports) | IMF IFS | 25% |
| NIIP (% GDP) | IMF IFS | 20% |
| REER vs 10Y average | BIS | 20% |

### 4. Fiscal Position (weight: 15%)
| Indicator | Source | Weight |
|-----------|--------|--------|
| Government Debt / GDP | IMF WEO | 30% |
| Fiscal Balance (% GDP) | IMF WEO | 30% |
| Interest Payments / Revenue | IMF WEO | 25% |
| Debt Maturity Profile (avg maturity) | National debt office | 15% |

### 5. Financial Stability (weight: 15%)
| Indicator | Source | Weight |
|-----------|--------|--------|
| Credit / GDP Gap | BIS | 30% |
| Bank NPL Ratio | IMF FSI | 25% |
| Bank Capital Adequacy | IMF FSI | 20% |
| Real House Price Growth | BIS / national | 15% |
| Private Sector Debt / GDP | BIS | 10% |

### 6. Labor Market (weight: 10%)
| Indicator | Source | Weight |
|-----------|--------|--------|
| Unemployment Rate (vs NAIRU est.) | National / IMF | 40% |
| Labor Force Participation | World Bank | 25% |
| Youth Unemployment | World Bank | 20% |
| Real Wage Growth | National / ILO | 15% |

### 7. Structural / Institutional (weight: 10%)
| Indicator | Source | Weight |
|-----------|--------|--------|
| Ease of Doing Business / B-READY | World Bank | 25% |
| Governance Indicators | WGI (World Bank) | 25% |
| Infrastructure Quality | WEF / national | 20% |
| Demographic Outlook (dependency ratio) | UN Population | 20% |
| R&D Spending (% GDP) | UNESCO | 10% |

## Composite Score Interpretation

| Score | Classification | Meaning |
|-------|---------------|---------|
| 80-100 | Excellent | Strong across most dimensions, resilient to shocks |
| 65-80 | Good | Generally healthy, some areas of concern |
| 50-65 | Fair | Mixed picture, significant vulnerabilities |
| 35-50 | Weak | Multiple stress areas, shock-prone |
| 20-35 | Poor | Crisis risk elevated, urgent policy action needed |
| 0-20 | Critical | Active crisis or imminent |

## Output Template

```markdown
## Macro Health Score: [Country] — [Date]

### Overall Score: XX/100 — [Classification]

### Dimension Scores
| Dimension | Score | Weight | Weighted | Trend |
|-----------|-------|--------|----------|-------|
| Growth | XX/100 | 20% | XX.X | ↑/↓/→ |
| Inflation | XX/100 | 15% | XX.X | |
| External | XX/100 | 15% | XX.X | |
| Fiscal | XX/100 | 15% | XX.X | |
| Financial | XX/100 | 15% | XX.X | |
| Labor | XX/100 | 10% | XX.X | |
| Structural | XX/100 | 10% | XX.X | |
| **TOTAL** | | **100%** | **XX.X** | |

### Strengths (Top 2)
1. [Strength 1]
2. [Strength 2]

### Weaknesses (Bottom 2)
1. [Weakness 1]
2. [Weakness 2]

### Key Risk
[Most acute near-term risk and trigger level]
```

## Red Flags
- Scores are relative — adjust thresholds for country's development level
- Data lags: official figures can be 6-12 months old for some indicators
- Structural dimension changes slowly — use for long-term comparison, not monthly tracking
- Composite scores hide distribution — always check individual dimensions
- One weak dimension (e.g., external) can override all other strengths in a crisis
