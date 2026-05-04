---
name: macro-bridge
description: Macro-to-micro transmission — rates, FX, commodities, liquidity → sector/asset impact. Pre-built scenarios, parametric stress testing, ETF allocation mapping.
category: finance-macro
domain: macro-bridge
allowed-tools: Bash(python3:*) Read(*)
---

# Macro-Bridge — Macro-to-Micro Transmission

## Purpose

The bridge between macroeconomic conditions and investable outcomes. Connects macro drivers (rates, FX, commodities, liquidity) to sector-level and asset-level implications. Answers: "The Fed just hiked 50bp — what does that mean for my portfolio?"

## How to Use

```bash
# Pre-built scenarios
python3 macro-bridge/scripts/stress_test.py --scenario fed-tightening --country NZL
python3 macro-bridge/scripts/stress_test.py --scenario global-recession

# Custom scenarios
python3 macro-bridge/scripts/stress_test.py --custom "rate=+2.0,oil=+3.0,liquidity=-2.0"

# ETF allocation from scenario
python3 macro-bridge/scripts/asset_mapper.py --scenario fed-tightening
```

## Transmission Channels

Four channels map macro events to sector/asset outcomes:
1. **Rate**: duration effect on growth stocks/REITs, NIM effect on banks, borrowing costs
2. **FX**: exporter competitiveness, importer costs, multinational earnings translation
3. **Commodity**: input costs, terms of trade, inflation passthrough
4. **Liquidity**: risk appetite, funding stress, asset price correlation regime

The sector sensitivity matrix is in `sector_mapper.py`. Each sector has a [-5, +5] sensitivity to each channel.

## Red Flags
- Transmission mechanisms are regime-dependent — what works in expansion may reverse in recession
- Correlation ≠ causation — commodity prices and EM equities can both be driven by global demand
- Second-order effects often dominate: rate hike → USD strength → EM stress → contagion
- Policy responses can override transmission: fiscal stimulus can offset monetary tightening
- Market pricing embeds transmission assumptions — watch for "priced in" risk
