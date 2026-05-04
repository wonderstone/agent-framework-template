---
name: policy-stance
description: Monetary and fiscal policy stance assessment for any country. Combines central bank rate analysis with fiscal impulse measurement to determine whether policy is expansionary, neutral, or contractionary.
category: finance-macro
domain: country-intel
allowed-tools: Bash(python3:*) Read(*)
---

# Policy Stance Assessment

## Purpose

Unified monetary + fiscal policy stance assessment. Determines whether a country's combined policy mix is expansionary (supporting growth), neutral, or contractionary (restraining growth). Critical for understanding the macro outlook — policy stance is often the most important near-term macro variable.

## When to Use

- "What's the policy stance in [Country]?"
- "Is monetary policy restrictive right now?"
- "Fiscal impulse direction?"
- "Policy mix analysis?"
- "Are fiscal and monetary policy working together or against each other?"

## Monetary Policy Stance

### Real Rate Assessment
```
Real Policy Rate = Nominal Policy Rate - Core Inflation (YoY)

Real Rate > Neutral Rate → Restrictive (tightening)
Real Rate ≈ Neutral Rate → Neutral
Real Rate < Neutral Rate → Accommodative (easing)
```

### Neutral Rate Estimation
| Country | Estimated Neutral Rate | Rationale |
|---------|----------------------|-----------|
| US | 2.5-3.0% (r-star) | Fed SEP long-run dot |
| Eurozone | 1.5-2.0% | ECB staff estimates |
| Japan | 0.5-1.5% | Wide range, structural uncertainty |
| UK | 2.0-2.5% | BOE estimates |
| Australia | 2.5-3.0% | RBA estimates |
| New Zealand | 2.5-3.0% | RBNZ estimates (OCR neutral) |
| Canada | 2.0-2.5% | BOC estimates |

### Monetary Stance Classification
| Real Rate - Neutral | Stance | Macro Impact |
|--------------------|--------|-------------|
| > +1% | Tight / Restrictive | Growth headwind, inflation falling |
| +0.5% to +1% | Moderately Tight | Gradual demand restraint |
| -0.5% to +0.5% | Neutral | Policy neither helping nor hurting |
| -1% to -0.5% | Moderately Loose | Gradual demand support |
| < -1% | Loose / Accommodative | Growth tailwind, inflation risk |

### Financial Conditions Index
Complements real rate assessment by incorporating credit spreads, equity prices, and FX:
```
FCI = β1 × Real_Rate + β2 × HY_Spread + β3 × Equity_Change + β4 × Trade_Weighted_FX + β5 × VIX
```
- Rising FCI = tighter conditions
- Falling FCI = easier conditions

## Fiscal Policy Stance

### Fiscal Impulse
```
Fiscal Impulse = -(Δ Cyclically-Adjusted Primary Balance / Potential GDP)
```
- Positive fiscal impulse (> +0.5% GDP) = expansionary
- Neutral (±0.5% GDP) = neutral
- Negative fiscal impulse (< -0.5% GDP) = contractionary

### Government Consumption + Investment
```
Govt C+I Growth > GDP Growth → Fiscal expansion (direct demand contribution)
Govt C+I Growth ≈ GDP Growth → Neutral
Govt C+I Growth < GDP Growth → Fiscal contraction
```

## Policy Mix Matrix

```
              | Fiscal Expansionary | Fiscal Neutral | Fiscal Contractionary
Monetary Tight| Conflict (STAG)     | Tight-only     | Double Tight (hard landing risk)
Monetary Neutral| Ease-only        | Neutral        | Tight-only
Monetary Loose | Double Ease (reflation) | Ease-only | Conflict (fiscal drag)
```

**Key Insight**: When monetary and fiscal policy conflict, monetary usually wins in the short run; fiscal dominance happens when debt is in local currency and the central bank is not independent.

## Output Template

```markdown
## Policy Stance: [Country] — [Date]

### Monetary Policy
- Policy Rate: X.XX% | Neutral Estimate: X.X%
- Core Inflation: X.X%
- Real Policy Rate: +X.XX%
- Real Rate - Neutral: ±X.XXpp → [Tight/Neutral/Loose]
- Financial Conditions: [Tightening / Stable / Easing]

### Fiscal Policy
- Fiscal Balance: -X.X% of GDP
- Cyclically-Adjusted Primary Balance: ±X.X% of GDP
- Fiscal Impulse: ±X.X% of potential GDP → [Expansionary/Neutral/Contractionary]
- Govt C+I Growth: +X.X% vs GDP Growth +X.X%

### Policy Mix
- Monetary Stance: [Tight / Neutral / Loose]
- Fiscal Stance: [Expansionary / Neutral / Contractionary]
- Mix Assessment: [Double Tight / Conflict / Neutral / Double Ease]
- Near-term Outlook: [Policy likely to tighten/ease/hold]

### Key Risks
- [Risk 1: e.g., "If inflation stays above 3%, central bank can't ease"]
- [Risk 2: e.g., "Fiscal consolidation required if spreads widen"]
```

## Red Flags
- Neutral rate (r-star) is unobservable — large uncertainty bands around estimates
- Policy works with "long and variable lags" (Friedman) — stance today affects economy in 6-18 months
- Financial conditions can ease even as policy rate rises (risk-on rally, weaker USD)
- Fiscal impulse calculation is sensitive to output gap estimates — which are also uncertain
- In EM, the relevant policy rate may not be the official rate but the market rate (if credit rationed)
