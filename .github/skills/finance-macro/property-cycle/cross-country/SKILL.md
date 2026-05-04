---
name: cross-country
description: Cross-country property cycle comparison covering house prices, affordability, credit conditions, and cycle phase synchronization. Identifies global housing cycle convergence/divergence and macro drivers.
category: finance-macro
domain: property-cycle
allowed-tools: Bash(python3:*) Read(*)
---

# Cross-Country Property Cycle Comparison

## Purpose

Compare property cycles across countries to identify synchronization, divergence, and global macro drivers. The 2020-2022 pandemic housing boom was the most synchronized global property upswing in history — this skill tracks whether countries are converging or diverging in their cycles and what macro forces (rates, migration, credit) are driving the differences.

## When to Use

- "Compare housing markets across countries"
- "Which countries are most overvalued?"
- "Global housing cycle synchronization?"
- "Where to invest in property globally?"
- "Relative value across housing markets"

## Global Housing Cycle Synchronization

### The Pandemic Boom (2020-2022)
```
Unprecedented synchronization:
  → All DM house prices rose simultaneously (first time in history)
  → Common drivers: rate cuts, QE, fiscal transfers, WFH space demand
  → Price gains: +20-40% across US, CA, AU, NZ, NL, SE, DK, DE
```

### The Great Divergence (2022-Present)
```
Desynchronization driven by:
  → Mortgage rate structure differences
  → Migration patterns
  → Supply constraints
  → Policy responses (macroprudential, tax)
```

### Current Synchronization Matrix
| Country Pair | Correlation (5Y real house price) | Status |
|-------------|----------------------------------|--------|
| AU-NZ | 0.85 | Highly synchronized |
| US-UK | 0.70 | Synchronized |
| US-CA | 0.75 | Synchronized |
| CN-ROW | -0.20 | Diverging (China property slump) |
| DE-US | 0.45 | Moderate (energy shock divergence) |

## Driver Comparison

### Mortgage Rate Structure — The Key Differentiator

| Country | Typical Mortgage | Rate Reset | Sensitivity to Central Bank |
|---------|-----------------|-----------|---------------------------|
| US | 30Y Fixed | No reset (refinancing option) | Low — existing borrowers insulated |
| Canada | 5Y Fixed (renewal) | Every 5 years | High — rolling reset wall |
| Australia | Variable (~85% share) | Immediate passthrough | Very High — instant transmission |
| New Zealand | 1-2Y Fixed (~70%) | Every 1-2 years | Very High — rapid passthrough |
| UK | 2-5Y Fixed | Every 2-5 years | High |
| Germany | 10Y+ Fixed | Every 10+ years | Low |
| Sweden | Variable (~50%) | Immediate | High |

**Implication**: Australia and New Zealand have the fastest monetary policy transmission through housing — rate changes hit mortgage holders within months. The US has the slowest — most homeowners are insulated from rate changes.

## Cross-Country Valuation Comparison

| Country | Nominal Price from Peak | Real Price from Peak | P/I vs LT Avg | P/R vs LT Avg | Cycle Phase |
|---------|----------------------|--------------------|--------------|-------------|-------------|
| New Zealand | -XX% | -XX% | +XX% | +XX% | [Phase] |
| Australia | -XX% | -XX% | +XX% | +XX% | |
| Canada | -XX% | -XX% | +XX% | +XX% | |
| US | +XX% | +XX% | +XX% | +XX% | |
| UK | -XX% | -XX% | +XX% | +XX% | |
| Germany | -XX% | -XX% | +XX% | +XX% | |
| China | -XX% | -XX% | +XX% | +XX% | |

## Global Housing Cycle Heatmap

```
                        Correction Deepening  |  Recovery Beginning
                        ──────────────────────┼──────────────────────
                        DE •                   |
                        UK •                   |
                        NZ ••                  |
                        CA ••                  |
Price Momentum (YoY)   AU ••                   |  US •
(Negative = correction) SE •                   |
                        NL •                   |
                        CN ••• (structural)    |
                        ──────────────────────┼──────────────────────
                        Bust / Stabilization  |  Boom / Expansion
```

## Macro Drivers of Convergence/Divergence

### Forces Driving Convergence (Synchronization)
- Global central bank rate cycle (2022-2023: synchronized tightening)
- Global bond yields (US 10Y drives global mortgage rates)
- Pandemic common shock (WFH, fiscal transfers)
- Cross-border capital flows

### Forces Driving Divergence
- Mortgage rate structure (fixed vs variable)
- Migration patterns (Canada, Australia seeing record inflows)
- Housing supply (US underbuilding vs Spain overbuilding)
- Tax policy (NZ interest deductibility changes, Canada foreign buyer bans)
- China property structural adjustment

## Red Flags
- Nominal house price indices can be misleading during high inflation — always check real prices
- National averages hide city-level extremes — Auckland, Sydney, Toronto, Vancouver distort national metrics
- Synchronized global housing corrections are rare but dangerous — correlated downside = systemic risk
- Policy responses differ: some countries let housing correct, others intervene (China, Singapore)
- Housing data lags vary by country (2-6 months) — transaction-based data (REINZ, CoreLogic) leads registry data
