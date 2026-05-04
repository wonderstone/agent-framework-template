---
name: energy-macro
description: Energy commodity macro analysis — crude oil, natural gas, and coal. Tracks OPEC+ dynamics, inventory levels, supply-demand balance, and macro transmission to inflation, currencies, and fiscal positions of producer/consumer nations.
category: finance-macro
domain: commodity-macro
allowed-tools: Bash(python3:*) Read(*)
---

# Energy Macro Analysis

## Purpose

Analyze energy commodity markets (crude oil, natural gas, coal) through a macroeconomic lens. Energy is the most macro-relevant commodity class — oil price shocks have preceded most post-WWII recessions, natural gas prices determine European industrial competitiveness, and energy transitions are reshaping global capital flows and geopolitics.

## When to Use

- "Oil price outlook?"
- "OPEC+ decision analysis"
- "Energy price impact on inflation?"
- "Natural gas and European industry"
- "Energy supply-demand balance"

## Key Reference Prices

| Commodity | Benchmark | Key Driver | Macro Sensitivity |
|-----------|----------|------------|-------------------|
| Crude Oil | WTI (US), Brent (Global) | OPEC+, geopolitics, global demand | Highest — core CPI, trade balances, fiscal |
| Natural Gas | Henry Hub (US), TTF (EU), JKM (Asia) | Weather, storage, LNG | High — EU industry, inflation |
| Coal | Newcastle (Asia), API2 (EU) | China/India demand, policy | Medium — power prices, steel |
| LNG | JKM (spot), oil-indexed contracts | Winter demand, supply projects | Growing — energy security premium |

## Oil Macro Transmission

### Supply-Side Oil Shock (e.g., OPEC cut, geopolitical disruption)
```
Oil Price ↑ 20%
  → Headline CPI +0.3-0.5pp (direct via gasoline)
  → Core CPI +0.1-0.2pp (indirect via transport costs)
  → Consumer spending shifts from discretionary to fuel → GDP -0.2 to -0.5pp
  → Oil exporters: fiscal surplus, currency appreciation
  → Oil importers: trade deficit widening, currency depreciation
```

### Demand-Side Oil Rally (e.g., strong global growth)
```
Oil Price ↑ driven by demand
  → Positive signal: global growth strong
  → Less stagflationary than supply shock
  → Commodity currencies benefit, EM commodity importers suffer
```

### Oil Price Collapse
```
Oil Price ↓ 30%
  → Headline CPI -0.3 to -0.5pp
  → Consumer relief — discretionary spending boost
  → Oil exporters: fiscal crisis, currency collapse (NGN, RUB, SAR peg pressure)
  → US shale: capex collapse, high-yield energy debt stress
```

## Inventory Monitoring

| Region | Data Source | Frequency | Key Level |
|--------|-----------|----------|-----------|
| US | EIA Weekly Petroleum Status | Weekly (Wed) | Cushing hub critical for WTI |
| OECD | IEA Monthly Oil Market Report | Monthly | Days of forward demand cover |
| Global | Satellite tanker tracking (Vortexa, Kpler) | Real-time | Floating storage = contango signal |
| SPR | US Strategic Petroleum Reserve | Weekly | Release/depletion pace |

## OPEC+ Decision Framework

OPEC+ meetings (scheduled + emergency) are the most important discrete macro events for oil:

### What to Analyze
1. **Quota change**: Baseline adjustment vs. voluntary cuts vs. mandatory cuts
2. **Compliance**: Who is cheating? (Iraq, Kazakhstan historically)
3. **Spare capacity**: Saudi (~2 mbpd), UAE (~1 mbpd) — key buffer
4. **Forward guidance**: "Market stability" vs. "precautionary" language
5. **Political context**: US SPR releases, Russia sanctions, China import quotas

## Natural Gas — The European De-Industrialization Question

European natural gas (TTF) is structurally higher post-Russia:
- TTF > €40/MWh → European energy-intensive industry (chemicals, steel, glass) uncompetitive
- TTF > €80/MWh → De-industrialization accelerates, permanent capacity loss
- TTF < €25/MWh → Industry recovery possible (unlikely without Russian supply return)

## Red Flags
- Oil is simultaneously a commodity, financial asset, and geopolitical weapon — models fail at regime changes
- IEA demand forecasts are systematically revised (usually higher) — treat as baseline, not precision
- SPR releases can suppress prices temporarily but don't add permanent supply
- Energy transition = structural decline for coal, peak uncertainty for oil, structural growth for some metals
- Jevons paradox: energy efficiency can INCREASE total energy consumption
