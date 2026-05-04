---
name: inflation-tracker
description: Multi-dimensional inflation analysis tracking CPI, Core CPI, PCE, Core PCE, PPI, breakeven rates, wage growth, and rent inflation. Detects disinflation trends, sticky components, and inflation regime shifts.
category: finance-macro
domain: macro-dashboard
allowed-tools: Bash(python3:*) Read(*)
---

# Inflation Tracker

## Purpose

Multi-dimensional inflation monitoring. Goes beyond headline CPI to analyze core measures, sticky vs. flexible components, shelter/lag indicators, wage-price spiral risks, and market-implied expectations. Detects whether inflation is truly trending back to target or is structurally elevated.

## When to Use

- "What's the latest inflation reading?"
- "Is inflation coming down?"
- "What's the Fed's preferred inflation measure showing?"
- "Are we seeing wage-price spiral?"
- "What are breakevens pricing?"
- "Is disinflation stalling?"

## Inflation Dimensions

### 1. Headline Measures
| Indicator | FRED Code | Frequency | Notes |
|-----------|-----------|-----------|-------|
| CPI (YoY) | CPIAUCSL | Monthly | Most cited, widest coverage |
| PCE (YoY) | PCEPI | Monthly | Fed's preferred measure |
| GDP Deflator | GDPDEF | Quarterly | Broadest price measure |

### 2. Core Measures (ex. Food & Energy)
| Indicator | FRED Code | Frequency | Notes |
|-----------|-----------|-----------|-------|
| Core CPI | CPILFESL | Monthly | Shelter is ~33% weight |
| Core PCE | PCEPILFE | Monthly | Fed's 2% target metric |
| Sticky CPI (Atlanta Fed) | STICKCPIM157SFRBATL | Monthly | Items that change price slowly |
| Flexible CPI | FLEXCPIM159SFRBATL | Monthly | Items that change price frequently |
| Trimmed Mean PCE (Dallas Fed) | PCETRIM12M159SFRBDAL | Monthly | Excludes outliers |
| Median CPI (Cleveland Fed) | MEDCPIM158SFRBCLE | Monthly | Median price change |

### 3. Pipeline / Leading
| Indicator | FRED Code | Frequency | Notes |
|-----------|-----------|-----------|-------|
| PPI (Final Demand) | PPIACO | Monthly | Wholesale prices → CPI with ~1-3mo lag |
| ISM Prices Paid | NAPMPRI | Monthly | Manufacturing input costs |
| Import Prices | IR | Monthly | Exchange rate pass-through |
| CRB Commodity Index | — | Daily | Raw material prices |
| NY Fed Global Supply Chain Pressure | GSCPI | Monthly | Supply chain inflation driver |

### 4. Services / Shelter (Sticky Component)
| Indicator | FRED Code | Frequency | Notes |
|-----------|-----------|-----------|-------|
| CPI Shelter | CUSR0000SAH1 | Monthly | ~33% of CPI, lags market rents by 12mo |
| CPI Services ex. Shelter | CUSR0000SASLE | Monthly | "Supercore" — Fed focus area |
| Zillow Observed Rent Index | — | Monthly | Leading shelter indicator by ~12 months |
| Average Hourly Earnings | CES0500000003 | Monthly | Wage inflation |

### 5. Expectations
| Indicator | FRED Code | Frequency | Notes |
|-----------|-----------|-----------|-------|
| 5-Year Breakeven | T5YIFR | Daily | Market-implied 5y inflation |
| 10-Year Breakeven | T10YIE | Daily | Market-implied 10y inflation |
| 5y5y Forward | T5YIFR (derived) | Daily | Long-term expectations |
| Michigan 5-10Y Survey | MICH | Monthly | Consumer expectations |

## Inflation Regime Classification

| Regime | CPI Range | Core PCE Range | Policy Implication |
|--------|----------|---------------|-------------------|
| **Deflation** | < 0% | < 0% | Aggressive easing |
| **Below Target** | 0-2% | 0-1.5% | Easing bias |
| **At Target** | 2-2.5% | 1.8-2.2% | Hold / neutral |
| **Above Target / Transitory** | 2.5-4% | 2.2-3% | Watchful waiting |
| **Elevated / Sticky** | 4-6% | 3-4% | Tightening |
| **High / Entrenched** | > 6% | > 4% | Aggressive tightening |

## Disinflation Checklist

Is disinflation genuine? Check:

1. [ ] Core PCE declining for 3+ consecutive months?
2. [ ] Shelter inflation rolling over? (Check Zillow lag ~12 months)
3. [ ] Wage growth decelerating toward 3.5%?
4. [ ] Supply chain pressures normalized? (GSCPI near zero)
5. [ ] Inflation expectations anchored near 2-2.5%?
6. [ ] PPI not signaling re-acceleration?

**If 4/6: disinflation likely sustainable**
**If 2/6: sticky inflation risk — Fed may need to hold tighter for longer**

## Output Template

```markdown
## Inflation Dashboard — [Month YYYY]

### Headline & Core
| Measure | Latest | Prior | 3-Mo Avg | 6-Mo Trend |
|---------|--------|-------|----------|------------|
| CPI (YoY) | X.X% | X.X% | X.X% | ↓/↑/→ |
| Core CPI (YoY) | X.X% | X.X% | X.X% | |
| PCE (YoY) | X.X% | X.X% | X.X% | |
| Core PCE (YoY) | X.X% | X.X% | X.X% | |

### Sticky vs Flexible
| Component | YoY | 3-Mo Ann. |
|-----------|-----|-----------|
| Sticky CPI | X.X% | X.X% |
| Flexible CPI | X.X% | X.X% |
| CPI Shelter | X.X% | X.X% |
| CPI Services ex-Shelter | X.X% | X.X% |

### Pipeline
| Indicator | Latest | Signal |
|-----------|--------|--------|
| PPI | X.X% | |
| ISM Prices Paid | XX.X | |
| Import Prices | X.X% | |

### Expectations
| Horizon | Rate | Assessment |
|---------|------|------------|
| 5-Year Breakeven | X.XX% | Anchored/Drifting |
| 5y5y Forward | X.XX% | Anchored/Drifting |

### Assessment
- Regime: [At Target / Above Target / Elevated]
- Trend: [Disinflation / Stable / Re-accelerating]
- Disinflation Checklist: X/6
- Fed Implications: [On track for cuts / Need more evidence / Holds needed]
```

## Red Flags
- Shelter is ~33% of CPI but lags market rents by ~12 months — use Zillow/Apartment List as leading indicators
- Core PCE is the Fed's metric — not CPI. Always reference both.
- Insurance, healthcare, and education inflation are structural and less rate-sensitive
- Breakevens can be distorted by liquidity premiums in TIPS market
- Base effects can create misleading YoY comparisons (use 3-month or 6-month annualized for trend)
