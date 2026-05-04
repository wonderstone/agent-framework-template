---
name: commodity-macro
description: Commodity-macro linkage — energy, metals, agricultural commodities. Supercycle detection (5-factor model), macro transmission to inflation, currencies, producer economies.
category: finance-macro
domain: commodity-macro
allowed-tools: Bash(python3:*) Read(*)
---

# Commodity Macro Link

## Purpose

Analyze commodity markets through a macroeconomic lens. Connects commodity supply-demand fundamentals to macro variables (inflation, currencies, trade balances, fiscal positions) and detects commodity supercycle phases.

## How to Use

```bash
# Supercycle detection
python3 commodity-macro/scripts/supercycle_scorer.py
python3 commodity-macro/scripts/supercycle_scorer.py --capex-gdp 3.5 --inventory 50 --ev-penetration 25
```

## Supercycle Framework

A commodity supercycle is a multi-decade, demand-driven upswing triggered by industrialization of a large economy. The 5-factor model scores:

1. **Industrialization** — Is a major economy industrializing/urbanizing? (India, SE Asia)
2. **Supply underinvestment** — Mining capex/GDP at multi-decade lows?
3. **Structural demand shift** — Energy transition = electrification = copper/lithium/nickel
4. **Inventories** — At cycle lows? Limited buffer against disruptions
5. **Producer discipline** — OPEC+ compliance, mining consolidation, buybacks over capex

**Score ≥ 60 + ≥ 3/5 checks = Supercycle Likely | ≥ 80 + ≥ 4/5 = Confirmed**

## Historical Context
- 1st: 1890s-1910s — US industrialization (coal, steel, copper)
- 2nd: 1940s-1970s — Post-war reconstruction (oil, steel, copper)
- 3rd: 2000s-2014 — China industrialization (everything)
- 4th candidate: 2020s-? — Energy transition + electrification

## Red Flags
- Commodity prices are the most cyclical asset class — mean reversion is powerful
- High prices cure high prices (demand destruction, substitution, new supply)
- Supercycles can have 30-50% drawdowns within them — don't confuse correction with end
- Oil is uniquely geopolitical — supply disruptions can override demand fundamentals
- China's commodity intensity declining as it shifts from investment to consumption
