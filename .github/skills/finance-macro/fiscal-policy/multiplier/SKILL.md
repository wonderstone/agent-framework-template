---
name: multiplier
description: Fiscal multiplier estimation by spending type, economic regime, and country characteristics. Estimates GDP impact of government spending changes and tax policy adjustments.
category: finance-macro
domain: fiscal-policy
allowed-tools: Bash(python3:*) Read(*)
---

# Fiscal Multiplier Estimation

## Purpose

Estimate fiscal multipliers — how much GDP changes per unit of government spending or tax change. Multipliers are the critical link between fiscal policy decisions and macro outcomes, but they vary enormously by context: a multiplier that is 1.5 in a recession may be 0.3 in an expansion, and infrastructure spending may have 3x the multiplier of corporate tax cuts.

## When to Use

- "What's the fiscal multiplier for [spending type]?"
- "GDP impact of [policy change]?"
- "Infrastructure spending multiplier?"
- "Tax cut effectiveness?"
- "Which stimulus is most effective?"

## Multiplier Estimates by Type

### Spending Multipliers

| Spending Type | Expansion | Recession | Notes |
|--------------|-----------|-----------|-------|
| Infrastructure Investment | 0.8-1.5 | 1.5-2.5 | Highest multiplier, but slow to deploy |
| Transfers to Low-Income Households | 0.8-1.2 | 1.2-2.0 | Fast, high MPC recipients |
| General Government Consumption | 0.5-1.0 | 1.0-1.5 | Depends on composition |
| Defense Spending | 0.6-1.0 | 1.0-1.8 | Military Keynesianism |
| Transfers to All Households | 0.3-0.7 | 0.7-1.2 | Lower MPC for higher incomes |
| Aid to State/Local Governments | 0.4-0.8 | 0.8-1.3 | Prevents pro-cyclical state cuts |

### Tax Multipliers

| Tax Change | Expansion | Recession | Notes |
|-----------|-----------|-----------|-------|
| Payroll Tax Cut (employee) | 0.5-0.8 | 0.8-1.3 | Directly boosts take-home pay |
| Income Tax Cut (low/middle) | 0.4-0.7 | 0.7-1.1 | | 
| Income Tax Cut (high income) | 0.1-0.4 | 0.3-0.6 | Low MPC = low multiplier |
| Corporate Tax Cut | 0.2-0.4 | 0.3-0.5 | Mostly share buybacks/dividends |
| Investment Tax Incentives | 0.5-0.8 | 0.6-1.0 | Accelerates capex timing |
| VAT Cut (temporary) | 0.3-0.5 | 0.5-0.8 | Brings forward spending |

### Transfer Payments (Targeted)

| Transfer Type | Multiplier | Rationale |
|--------------|-----------|-----------|
| Unemployment Benefit Extension | 1.0-1.5 | Highest MPC — constrained households |
| Food Stamps / SNAP | 1.2-1.7 | Very high MPC |
| Child Tax Credit / Family Benefits | 0.8-1.2 | High MPC for families |
| One-Time Stimulus Checks | 0.3-0.6 | Lower MPC — often saved |
| Pension Increases | 0.3-0.5 | Moderate MPC |

## Context Adjustments to Multiplier

### State-Dependent Multipliers

| Context | Multiplier Adjustment | Reason |
|---------|---------------------|--------|
| Deep Recession (U > 8%) | × 1.5-2.0 | Slack resources, no crowding out |
| Moderate Recession | × 1.2-1.5 | Some slack, monetary accommodation |
| Expansion (at potential) | × 0.5-0.8 | Crowding out, monetary offset |
| Overheating (above potential) | × 0-0.3 | Full crowding out, inflation |
| Zero Lower Bound (ZLB) | × 1.3-1.8 | Monetary policy can't offset |
| High Debt (>100% GDP) | × 0.5-0.7 | Ricardian offset, risk premium |
| Open Economy (trade/GDP > 50%) | × 0.6-0.8 | Leakage through imports |
| Fixed Exchange Rate | × 1.2-1.5 | No monetary offset via FX |
| Floating Exchange Rate | × 0.7-0.9 | FX appreciation offsets stimulus |

### Country-Specific Factors

| Factor | Impact on Multiplier |
|--------|---------------------|
| High household debt | Lower (pay down debt, not spend) |
| Low labor share | Lower (profits saved, wages spent) |
| High inequality | Higher (transfers to low-income have high MPC) |
| Large automatic stabilizers | Lower (already providing stimulus) |
| CB independence | Lower (monetary offset stronger) |
| Fiscal credibility | Higher (less Ricardian offset) |

## Multiplier Decay Over Time

```
Year 1: Full multiplier effect
Year 2: 50-70% of Year 1 (some crowding out, monetary response)
Year 3: 20-40% (most effects dissipated)
Year 4+: 0-10% (supply-side effects may dominate)
```

## Output Template

```markdown
## Fiscal Multiplier Analysis: [Country] — [Policy Proposal]

### Policy Description
- Type: [Infrastructure / Transfers / Tax Cut / ...]
- Size: $XX billion (X.X% of GDP)
- Duration: [One-time / Multi-year / Permanent]

### Multiplier Estimates
| Scenario | Base Multiplier | Adjusted | GDP Impact (Year 1) | GDP Impact (Year 3) |
|----------|---------------|----------|--------------------|--------------------|
| Baseline | X.X | X.X | ±$XXB (±X.X%) | ±$XXB (±X.X%) |
| Optimistic | X.X | X.X | ±$XXB | ±$XXB |
| Conservative | X.X | X.X | ±$XXB | ±$XXB |

### Context Adjustments Applied
- Economic Cycle: [Recession/Expansion] → Multiplier × X.X
- Monetary Stance: [ZLB/Normal/Tightening] → × X.X
- Openness: Trade/GDP = XX% → × X.X
- Debt Level: XX% GDP → × X.X
- FX Regime: [Fixed/Floating] → × X.X

### Assessment
- Most Likely Range: X.X to X.X multiplier
- GDP Impact: ±X.X% over [period]
- Cost per Job Created (if applicable): $XX,XXX
- Key Uncertainty: [Which assumption most affects the estimate]
```

## Red Flags
- Multiplier estimates from IMF/OECD systematically differ by 2-3x — there is no consensus
- "Shovel-ready" infrastructure usually isn't — spending lags explain low short-term multipliers
- Open economy multipliers are MUCH lower — small countries can't stimulate domestically
- Multiplier estimates are from historical data — if the current situation is unprecedented, they're less reliable
- Fiscal multipliers near zero in countries with loss of market access (EM crisis)
