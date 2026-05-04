---
name: debt-sustainability
description: Debt sustainability analysis (DSA) framework. Projects debt/GDP paths under baseline, optimistic, and stress scenarios. Calculates debt-stabilizing primary balance, fiscal gap, and rollover risk indicators.
category: finance-macro
domain: fiscal-policy
allowed-tools: Bash(python3:*) Read(*)
---

# Debt Sustainability Analysis (DSA)

## Purpose

IMF/World Bank-style debt sustainability analysis for any country. The core question: can a country service its debt without an unrealistic adjustment or default? Uses the debt dynamics equation to project debt/GDP under multiple scenarios and identifies the fiscal gap — the adjustment needed to stabilize debt.

## When to Use

- "Is [Country]'s debt sustainable?"
- "Debt sustainability analysis for [Country]"
- "What happens if rates stay high for [Country]?"
- "Fiscal gap calculation"
- "Debt projection under different scenarios"

## The Debt Dynamics Model

```
dt = dt-1 × (1 + r) / (1 + g) - pbt + SFt

Where:
  dt   = Debt/GDP at time t
  r    = Effective nominal interest rate on debt
  g    = Nominal GDP growth rate
  pbt  = Primary balance (% GDP) at time t
  SFt  = Stock-flow adjustment (residual: privatization, valuation, contingent liabilities)
```

### Key Derived Metrics

**Debt-Stabilizing Primary Balance:**
```
pb* = (r - g) / (1 + g) × d ≈ (r - g) × d
```

**Fiscal Gap:**
```
Gap = pb* - pb_actual
Positive gap = adjustment needed (tightening required)
Negative gap = fiscal space available (can ease)
```

**Snowball Effect:**
```
Snowball = (r - g) × dt-1
Positive snowball = debt rising automatically (r > g — unfavorable)
Negative snowball = debt falling automatically (g > r — favorable)
```

## Scenario Design

### Baseline
- GDP growth: Consensus / IMF WEO forecast
- Interest rate: Forward curve + term premium
- Primary balance: Current policy, adjusted for cycle

### Optimistic
- GDP growth: Baseline + 1pp
- Interest rate: Baseline - 50bp
- Primary balance: Baseline + 0.5pp (growth dividend, consolidation)

### Stress (Interest Rate Shock)
- GDP growth: Baseline - 1pp
- Interest rate: Baseline + 200bp
- Primary balance: Baseline - 0.5pp (automatic stabilizers)

### Stress (Growth Shock / Recession)
- GDP growth: 0% or negative
- Interest rate: Baseline + 100bp (spreads widen)
- Primary balance: Deficit widens by 2-3pp of GDP

### Combined Shock
- Worst of all scenarios simultaneously
- Tests extreme but plausible tail risk

## Sustainability Assessment

| Indicator | Sustainable | Borderline | Unsustainable |
|-----------|-----------|------------|---------------|
| Debt/GDP trajectory (5Y projection) | Falling or stable | Rising slowly | Rising rapidly |
| r - g | Negative | Near zero | Significantly positive |
| Fiscal gap | < 1% of GDP | 1-3% of GDP | > 3% of GDP |
| Gross financing needs (% GDP) | < 15% | 15-25% | > 25% |
| Foreign currency debt share | < 20% | 20-50% | > 50% |
| Market access (sovereign spread) | < 300bp | 300-700bp | > 700bp |

## Process

1. Gather: debt stock, maturity profile, currency composition, interest cost
2. Establish baseline macro projections (g, r, primary balance)
3. Project debt/GDP forward 5 years (baseline)
4. Apply stress scenarios
5. Calculate debt-stabilizing primary balance and fiscal gap
6. Assess rollover/refinancing risk (debt maturing within 12 months)
7. Generate heat map: probability of debt exceeding thresholds

## Output Template

```markdown
## DSA: [Country] — [Date]

### Baseline Assumptions
| Variable | 20XX | 20XX+1 | ... | 20XX+5 |
|----------|------|--------|-----|--------|
| Real GDP Growth | X.X% | | | |
| Inflation (GDP Deflator) | X.X% | | | |
| Effective Interest Rate | X.X% | | | |
| Primary Balance (% GDP) | -X.X% | | | |

### Debt Projection
| Scenario | Year 1 | Year 3 | Year 5 | Direction |
|----------|--------|--------|--------|-----------|
| Baseline | XX% | XX% | XX% | ↑ Stable ↓ |
| Optimistic | XX% | XX% | XX% | ↓ |
| Interest Rate Shock | XX% | XX% | XX% | ↑ |
| Growth Shock | XX% | XX% | XX% | ↑↑ |
| Combined Shock | XX% | XX% | XX% | ↑↑↑ |

### Debt Stabilization
- r - g: ±X.X%
- Debt-Stabilizing Primary Balance: ±X.X% of GDP
- Actual Primary Balance: -X.X% of GDP
- Fiscal Gap: X.X% of GDP

### Assessment
- Debt Sustainability: [Sustainable / Borderline / At Risk / Unsustainable]
- Key Vulnerability: [r-g dynamics / FX debt / rollover risk / contingent liabilities]
- Required Adjustment: [None / Moderate fiscal consolidation / Significant / Urgent]
```

## Red Flags
- DSA is highly sensitive to r and g assumptions — small changes produce large debt path differences
- The model doesn't capture non-linearities: market access can vanish (cliff effect), not gradually tighten
- Contingent liabilities (SOEs, PPPs, pension systems, bank bailouts) are NOT in standard debt figures
- DSA is backward-looking: it asks if current policies can continue, not if they should
- IMF DSAs systematically underestimate debt accumulation in stress periods (GFC, COVID)
