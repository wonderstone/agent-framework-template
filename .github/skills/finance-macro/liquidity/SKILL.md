---
name: liquidity
description: Global central bank liquidity analysis — Fed, ECB, PBOC, BOJ balance sheets, net liquidity, Scissors Factor asset signals.
category: finance-macro
domain: liquidity
allowed-tools: Bash(python3:*) Read(*)
---

# Global Liquidity Monitor

## Purpose

Track central bank liquidity operations and their asset price implications. The Scissors Factor methodology compares liquidity growth rates to asset price growth rates to identify divergences — when liquidity outruns asset prices, it's bullish; when asset prices outrun liquidity, it's a bearish divergence.

## How to Use

```bash
# Full pipeline
python3 scripts/orchestrator.py '{"domain":"liquidity"}'

# Individual models
python3 liquidity/scripts/net_liquidity.py --walcl 7.2 --tga 0.75 --rrp 0.3
python3 liquidity/scripts/scissors_factor.py --liquidity-yoy 3.5 --btc-yoy 45.0 --gold-yoy 15.0
```

## Key Concepts

**Net Liquidity = Fed Assets (WALCL) - TGA - RRP**

The Treasury General Account (TGA) and Reverse Repo (RRP) drain reserves from the banking system. When the TGA builds (tax season) or RRP usage rises (money funds parking cash), net liquidity falls — even if the Fed balance sheet is flat.

**Scissors Factor = ΔLiquidity_YoY% - ΔAssetPrice_YoY%**
- SF > 0 → Liquidity growing faster than asset prices → Bullish divergence
- SF < 0 → Asset prices outrunning liquidity → Bearish divergence

## Red Flags
- WALCL data lags by 1 week — factor into real-time assessment
- TGA spikes during tax season — seasonal adjustment recommended
- RRP declining = liquidity being drained from financial system
- PBOC data transparency is limited — treat aggregate financing data as approximate
- BOJ balance sheet data lags by 10 days
