---
name: fiscal-policy
description: Fiscal policy analysis — debt sustainability (DSA), fiscal multipliers, budget structure, tax policy. Connects fiscal stance to macro outcomes and sovereign credit risk.
category: finance-macro
domain: fiscal-policy
allowed-tools: Bash(python3:*) Read(*)
---

# Fiscal Policy Analyzer

## Purpose

Analyze government fiscal positions and debt sustainability. Fiscal policy has become increasingly important post-GFC and COVID era demonstrated its power — and the constraints of high debt levels.

## How to Use

```bash
python3 fiscal-policy/scripts/debt_dynamics.py --debt 140 --growth 2.0 --interest 3.5 --primary-balance -2.1
```

## The Most Important Equation

**Δd = (r - g) × d - pb**

Where d = Debt/GDP, r = effective interest rate, g = nominal GDP growth, pb = primary balance (% GDP).

**If g > r**: debt/GDP can fall even with primary deficits (Japan: r=0.8%, g=1.5%, debt sustainable despite 250% debt/GDP).

**If r > g**: primary surpluses needed just to stabilize debt (Italy: r=3.5%, g=2.0%, needs 2.1% primary surplus).

**r - g** is the single most important metric in fiscal analysis.

## Fiscal Multipliers

Multipliers are larger in recessions (slack resources) and smaller in expansions (crowding out):
- Infrastructure: 0.8-1.5× (expansion) → 1.5-2.5× (recession)
- Tax cuts (low/middle income): 0.5-0.8× → 0.8-1.2×
- Corporate tax cuts: 0.2-0.4× → 0.3-0.5×

## Red Flags
- Official debt figures exclude contingent liabilities (SOEs, pension obligations, guarantees)
- Currency composition matters — EM FX debt is much riskier than domestic currency debt
- Fiscal multipliers are highly uncertain — treat as rough guides, not precise inputs
- Market access can vanish suddenly — don't assume rollover is always possible
- r - g has been favorable for decades (financial repression); rising rates change the calculus
