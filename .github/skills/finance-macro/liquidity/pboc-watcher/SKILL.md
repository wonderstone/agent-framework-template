---
name: pboc-watcher
description: Monitor People's Bank of China liquidity operations including MLF rate, LPR, aggregate financing, credit impulse, and social financing scale. Track China's unique multi-rate framework and its implications for global liquidity.
category: finance-macro
domain: liquidity
allowed-tools: Bash(python3:*) Read(*)
---

# PBOC Watcher — People's Bank of China Liquidity Analysis

## Purpose

Track PBOC monetary policy and liquidity operations. China uses a multi-rate, multi-tool framework that differs significantly from Western central banks. Key instruments include the Medium-term Lending Facility (MLF), Loan Prime Rate (LPR), Reserve Requirement Ratio (RRR), and various short-term liquidity tools (OMO, SLF, PSL). The PBOC credit impulse is a leading global economic indicator.

## When to Use

- "What's PBOC doing?"
- "China credit impulse trend?"
- "Is PBOC easing or tightening?"
- "MLF/LPR changes?"
- "China liquidity impact on global markets?"

## Key Instruments

### Policy Rates

| Instrument | What It Is | Signal |
|-----------|------------|--------|
| **MLF Rate** (1-year) | Medium-term lending to banks — key policy rate | Cut = easing signal |
| **7-Day Reverse Repo** | Short-term OMO rate — daily liquidity management | Operational stance |
| **LPR (1-year)** | Benchmark for corporate loans (MLF + bank spread) | Credit cost signal |
| **LPR (5-year)** | Mortgage reference rate | Property policy signal |
| **Standing Lending Facility (SLF)** | Emergency overnight lending — ceiling rate | Rarely changed |

### Quantity Tools

| Instrument | What It Is | Signal |
|-----------|------------|--------|
| **RRR (Reserve Requirement Ratio)** | % of deposits banks must hold at PBOC | Cut = liquidity injection |
| **Aggregate Financing** | Total credit to real economy (loans + bonds + equity + shadow) | Broader than M2 |
| **Social Financing Scale (TSF)** | Flow of credit to non-financial sectors | Monthly flow |
| **Credit Impulse** | ΔCredit as % of GDP — change in new credit flow | Leading global indicator |
| **PSL (Pledged Supplementary Lending)** | Directed lending for infrastructure/housing | Fiscal-monetary hybrid |

## Credit Impulse — The Global Leading Indicator

```
Credit_Impulse(t) = (ΔCredit(t) / GDP(t)) - (ΔCredit(t-1) / GDP(t-1))

Where ΔCredit = change in aggregate financing (TSF flow)
```

Credit impulse typically leads:
- Global PMI by 3-6 months
- Commodity prices (copper, iron ore) by 3-6 months
- EM equity performance by 6-12 months
- AUD, NZD, and commodity FX by 3-6 months

### Credit Impulse Regime

| Value | Regime | Global Implication |
|-------|--------|-------------------|
| > +3% | Strong expansion | Commodities, EM, cyclical assets bullish |
| 0 to +3% | Moderate expansion | Supportive but not driving |
| -3% to 0 | Contraction | Headwind for commodities, EM |
| < -3% | Strong contraction | Risk-off signal, commodity bear |

## PBOC Monetary Framework (vs Fed)

| Dimension | Fed | PBOC |
|-----------|-----|------|
| Single Rate | Fed Funds Rate corridor | Multiple rates (MLF, LPR, OMO, SLF) |
| Transmission | Market-based | Quantity + price-based, directed lending |
| FX Regime | Floating | Managed float (CFETS basket) |
| Independence | High | Moderate (State Council oversight) |
| Data Transparency | High | Limited — aggregate financing opaque |
| Mandate | Dual (price + employment) | Multiple (growth, employment, prices, FX, financial stability) |

## Output Template

```markdown
## PBOC Liquidity Dashboard — [Date]

### Key Rates
| Rate | Current | Last Change | Direction |
|------|---------|-------------|-----------|
| MLF (1Y) | X.XX% | [Date] | |
| 7D Reverse Repo | X.XX% | [Date] | |
| LPR (1Y) | X.XX% | [Date] | |
| LPR (5Y+) | X.XX% | [Date] | |
| RRR (large banks) | X.X% | [Date] | |

### Credit Aggregates
| Metric | Latest | YoY Change | Trend |
|--------|--------|------------|-------|
| Aggregate Financing (TSF) | ¥XX.XT | +X.X% | |
| M2 Money Supply | ¥XXX.XT | +X.X% | |
| New RMB Loans (monthly) | ¥X.XXT | | |

### Credit Impulse
- Current: +X.X
- 3-Month Trend: Rising / Falling
- Regime: Expansion / Contraction
- Global Signal: [Bullish / Neutral / Bearish] for commodities, EM, AUD, NZD

### Assessment
- Policy Stance: [Easing / Neutral / Tightening]
- FX Constraint: [PBOC defending CNY = less room for easing / CNY stable = easing room]
- Key Risk: [Capital outflow pressure / Property sector drag / Deflation risk]
```

## Red Flags
- PBOC data lags and is subject to revision — treat as approximate
- Aggregate financing includes shadow banking — composition matters, not just headline
- PBOC often uses "window guidance" (informal lending quotas) not captured in data
- China's capital controls mean domestic liquidity ≠ global spillover (but credit impulse still transmits via trade)
- Property sector is ~25-30% of GDP — property credit demand is a key transmission channel
