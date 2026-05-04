---
name: commodity-shock
description: Commodity price shock transmission to sectors, countries, and inflation. Analyzes input cost passthrough, terms of trade effects, and identifies which industries and countries are most exposed to commodity moves.
category: finance-macro
domain: macro-bridge
allowed-tools: Bash(python3:*) Read(*)
---

# Commodity Shock — Price Transmission

## Purpose

Analyze how commodity price shocks transmit through the economy. Commodity prices are both a macro signal (demand strength, supply constraints) and a micro cost driver. This skill maps commodity price changes to sector input costs, profit margins, country terms of trade, and inflation expectations.

## When to Use

- "What happens if oil hits $100?"
- "Which sectors benefit from lower copper prices?"
- "Impact of rising food prices on EM?"
- "Natural gas spike — who's exposed?"
- "Commodity price shock scenario"

## Commodity Coverage

### Energy
| Commodity | Key Use | Price Driver | Sensitive Sectors |
|-----------|---------|-------------|------------------|
| Crude Oil (WTI/Brent) | Transportation, petrochemicals | OPEC+, geopolitics, demand | Airlines, shipping, chemicals, consumers |
| Natural Gas | Heating, electricity, fertilizer | Weather, storage, LNG | Utilities, chemicals, industrials (EU) |
| Coal | Power generation, steel | China/India demand, policy | Utilities (APAC), steel |

### Industrial Metals
| Commodity | Key Use | Price Driver | Sensitive Sectors |
|-----------|---------|-------------|------------------|
| Copper | Wiring, electronics, construction | China demand, electrification | Construction, EVs, electronics |
| Iron Ore | Steel production | China property, infrastructure | Steel, construction |
| Aluminum | Packaging, aerospace, construction | Energy costs (smelting) | Aerospace, packaging, autos |
| Nickel / Lithium | EV batteries | EV adoption, mining supply | EV makers, battery producers |

### Agricultural
| Commodity | Key Use | Price Driver | Sensitive Sectors |
|-----------|---------|-------------|------------------|
| Corn | Feed, ethanol, food | Weather, ethanol policy | Food producers, livestock, biofuels |
| Wheat | Food staple | Weather, Russia/Ukraine | Food producers, EM consumers |
| Soybeans | Feed, oil, food | China demand, weather | Livestock, food, biodiesel |
| Coffee / Cocoa | Consumer goods | Weather, demand | Consumer staples, restaurants |

## Input Cost Passthrough Matrix

| Sector | Energy % of Costs | Metals % of Costs | Agri % of Costs | Total Commodity Exposure |
|--------|------------------|------------------|----------------|-------------------------|
| Airlines | 25-35% | 0% | 0% | Very High (Energy) |
| Chemicals | 40-60% | 0% | 5-10% | Very High (Energy) |
| Shipping | 30-40% | 0% | 0% | Very High (Energy) |
| Steel | 15-20% | 30-40% | 0% | Very High (Metals + Energy) |
| Construction | 10-15% | 20-30% | 0% | High |
| Autos | 5-10% | 15-20% | 0% | High (Metals) |
| Food & Beverage | 5-10% | 0% | 30-50% | High (Agri) |
| Electronics | 5-10% | 10-15% | 0% | Medium |
| Apparel | 5-10% | 0% | 10-20% | Medium |
| Software | 0-5% | 0% | 0% | None |

## Country Terms of Trade Impact

| Country Type | Oil ↑ 20% | Copper ↑ 20% | Food ↑ 20% |
|-------------|----------|-------------|-----------|
| Oil Exporter (SA, UAE, NO) | ✅ Large gain | Neutral | Neutral |
| Oil Importer (IN, JP, KR) | ❌ Large loss | Neutral | ❌ Loss |
| Copper Exporter (CL, PE, ZM) | Neutral | ✅ Large gain | Neutral |
| Food Exporter (NZ, BR, AU) | Neutral | Neutral | ✅ Gain |
| Food Importer (EG, NG, PH) | Neutral | Neutral | ❌ Loss |
| Diversified (US, CN, RU) | Mixed | Mixed | Mixed |

## Process

1. Identify commodity shock (type, magnitude, persistence)
2. Map to sector input cost exposure
3. Estimate margin impact (% of costs × price change × passthrough rate)
4. Assess country terms of trade impact
5. Evaluate second-round effects (inflation, monetary policy response)

## Red Flags
- Energy is the most macro-relevant commodity — oil shocks have caused most post-WWII recessions
- Food price spikes disproportionately affect EM (food is 30-50% of CPI vs 10-15% in DM)
- Futures prices ≠ spot impact — many corporates hedge 6-12 months forward
- Second-round effects (wage demands, policy response) often larger than direct impact
- Supply-driven shocks (OPEC cut) are more stagflationary than demand-driven (strong growth)
