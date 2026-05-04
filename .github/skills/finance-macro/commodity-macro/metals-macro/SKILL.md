---
name: metals-macro
description: Industrial and precious metals macro analysis — copper, iron ore, aluminum, gold, silver, lithium. Tracks supply-demand fundamentals, inventory levels, and macro drivers including China demand, electrification, and real rates.
category: finance-macro
domain: commodity-macro
allowed-tools: Bash(python3:*) Read(*)
---

# Metals Macro Analysis

## Purpose

Analyze industrial and precious metals through a macroeconomic lens. Industrial metals (copper, iron ore, aluminum) are the best real-time indicators of global economic activity. Precious metals (gold, silver) are the primary hedge against monetary debasement and real rate collapse.

## When to Use

- "Copper price outlook?"
- "Gold macro drivers?"
- "What's driving iron ore?"
- "Lithium supply-demand"
- "Metals as macro indicators"

## Industrial Metals — The Economic Barometer

### Copper: "Dr. Copper" — PhD in Economics
Copper is used in every sector — wiring, construction, electronics, EVs. Its price is the best single-commodity proxy for global growth.

| Indicator | Source | Frequency |
|-----------|--------|-----------|
| LME Copper Price | LME | Real-time |
| LME Warehouse Inventories | LME | Daily |
| SHFE Inventories | SHFE | Weekly |
| Copper Concentrate TC/RCs | Fastmarkets | Weekly |
| China Copper Imports | China Customs | Monthly |
| Global Mine Supply | ICSG | Monthly |

**Key Macro Relationships:**
- Copper/Gold ratio correlates with 10Y bond yields (both reflect growth expectations)
- Copper price leads PMI by 1-3 months
- China = 55% of global copper demand → China macro = copper

### Iron Ore: China's Property Barometer
Iron ore is almost entirely a China story (70% of seaborne imports).

| Driver | Signal |
|--------|--------|
| China Property Starts | Direct steel demand (rebar) |
| China Infrastructure Spend | Government-driven demand |
| Port Stockpiles (China) | Inventory buffer — rising = weak demand |
| Steel Mill Margins | Profitability → production intention |
| Baltic Capesize Index | Freight cost proxy for iron ore demand |

### Aluminum: The Energy Metal
Aluminum smelting is extremely energy-intensive (electricity = 30-40% of cost).

| Driver | Signal |
|--------|--------|
| European Power Prices | Smelter curtailment risk |
| China Coal Prices | China is 55% of production (coal-powered) |
| LME Inventories | Low inventories + supply constraint = price support |
| Russian Supply Risk | Rusal = 6% of global supply, sanctions risk |

## Precious Metals — Monetary Hedges

### Gold: The Anti-Fiat Asset

**Gold Price = f(Real Rates, USD, Central Bank Buying, Geopolitical Risk)**

| Driver | Relationship | Current Signal |
|--------|------------|---------------|
| US 10Y Real Yield (TIPS) | Inverse — lower real rates = higher gold | |
| USD (DXY) | Inverse — weaker USD = higher gold | |
| Central Bank Purchases | Positive — structural bid (PBOC, RBI, CBs) | |
| Geopolitical Risk | Positive — safe haven demand | |
| ETF Flows | Momentum — retail/institutional demand | |
| Indian/Chinese Consumer Demand | Seasonal (weddings, festivals) | |

**Gold Macro Regimes:**
| Regime | Real Rates | USD | Gold Direction |
|--------|-----------|-----|---------------|
| Fed Easing + Weak USD | ↓ | ↓ | ↑↑ Strong Bull |
| Fed Easing + Strong USD | ↓ | ↑ | ↑ Moderate |
| Fed Tightening + Weak USD | ↑ | ↓ | → Range |
| Fed Tightening + Strong USD | ↑ | ↑ | ↓ Bear |

## Electrification Metals — The Structural Demand Story

| Metal | EV/Battery Use | Supply Concentration | Key Risk |
|-------|---------------|---------------------|----------|
| Lithium | Battery cathode | Australia, Chile, China (processing) | Price volatility, substitution risk |
| Nickel | Battery cathode (Class 1) | Indonesia (60%+ new supply) | Environmental, ore grade decline |
| Cobalt | Battery cathode | DRC (70%) | Child labor, geopolitical |
| Rare Earths | Magnets, electronics | China (60% mining, 90% processing) | Supply chain weaponization |
| Copper | Wiring, motors (4x ICE vehicle) | Chile, Peru | Underinvestment, long mine lead times |

## Output Template

```markdown
## Metals Macro Analysis — [Date]

### Industrial Metals Dashboard
| Metal | Price | YoY | Inventory (weeks) | Macro Signal |
|-------|-------|-----|------------------|-------------|
| Copper | $X,XXX | ±X% | X.X | [Growth strong/moderate/weak] |
| Iron Ore | $XX | ±X% | | [China property: improving/stable/declining] |
| Aluminum | $X,XXX | ±X% | | [Energy cost impact: high/medium/low] |

### Precious Metals
| Metal | Price | Real Rate Signal | Central Bank Buying | Overall |
|-------|-------|-----------------|-------------------|---------|
| Gold | $X,XXX | [Bullish/Neutral/Bearish] | [Strong/Mod/Weak] | |
| Silver | $XX | | | |

### Electrification Monitor
| Metal | Supply Deficit/Surplus | 3Y Price Outlook | Key Risk |
|-------|----------------------|-----------------|----------|
| Lithium | ±XX Kt LCE | | |
| Copper | ±XX Kt | | |

### Assessment
- Industrial Metals Signal: [Global growth accelerating / stable / decelerating]
- Gold Signal: [Real rate + USD + structural demand]
- Key Commodity-Macro Trade: [e.g., Long copper if China stimulus materializes]
```

## Red Flags
- LME inventories can be distorted by dominant position holders and warehouse queues
- China "demand" includes significant speculative inventory building — not all consumption
- Gold can diverge from real rates for extended periods (central bank buying, geopolitical premium)
- Lithium price swings 200%+ in 12 months — extreme volatility, not for macro timing
- Sanctions can create two-tier pricing (Russian aluminum, Iranian oil) — headline price ≠ all-in price
