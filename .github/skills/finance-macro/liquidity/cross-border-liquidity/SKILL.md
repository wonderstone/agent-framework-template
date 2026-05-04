---
name: cross-border-liquidity
description: Aggregate global liquidity view combining Fed, ECB, PBOC, and BOJ balance sheets. Apply Scissors Factor methodology to generate Buy/Hold/Sell signals for Bitcoin, Gold, Nasdaq, and other macro-sensitive assets.
category: finance-macro
domain: liquidity
allowed-tools: Bash(python3:*) Read(*)
---

# Cross-Border Liquidity — Global View

## Purpose

Aggregate liquidity conditions across the four major central banks (Fed, ECB, PBOC, BOJ) into a unified global liquidity signal. Apply the Scissors Factor methodology (Liquidity YoY% - Asset Price YoY%) to generate asset-level signals. Detect cross-border capital flow regimes and global liquidity cycles.

## When to Use

- "What's the global liquidity picture?"
- "Scissors Factor for Bitcoin/Gold/Nasdaq?"
- "Are we in a global liquidity expansion or contraction?"
- "How does China credit impulse compare to Fed QT?"
- "Cross-border capital flows direction?"
- "Global liquidity cycle phase?"

## Global Liquidity Framework

### Four-Pillar Model

```
Global_Liquidity = 
  US_NetLiquidity (WALCL - TGA - RRP)     × USD_weight
  + ECB_NetLiquidity (Balance Sheet - Govt Deposits) × EUR_weight  
  + BOJ_NetLiquidity (JGB Holdings + ETFs) × JPY_weight
  + PBOC_CreditImpulse (ΔCredit / GDP)     × CNY_weight
```

### Pillar Weights (by global financial influence)

| Central Bank | Weight | Key Metric |
|-------------|--------|------------|
| Federal Reserve | 45% | Net Liquidity (WALCL - TGA - RRP) |
| European Central Bank | 25% | Balance Sheet + TLTRO outstanding |
| Bank of Japan | 15% | JGB holdings + ETF portfolio |
| People's Bank of China | 15% | Credit Impulse (ΔAggregate Financing / GDP) |

## Scissors Factor Signal Engine

### Methodology

For each asset, calculate:
```
SF(Asset) = ΔGlobalLiquidity_YoY% - ΔAssetPrice_YoY%
```

### Three-Component Weighted Signal

1. **Regime (50%)**: Is global liquidity expanding or contracting?
   - Expansion: SF > 0, accelerating
   - Contraction: SF < 0, decelerating

2. **Threshold (30%)**: SF magnitude assessment
   - SF > 10 → Strong bullish
   - -5 < SF < 5 → Neutral
   - SF < -10 → Strong bearish

3. **Momentum (20%)**: SF directional acceleration
   - SF rising → improving conditions
   - SF falling → deteriorating conditions

### Default Asset Basket

| Asset | Symbol | Sensitivity | Why |
|-------|--------|------------|-----|
| Bitcoin | BTC-USD | Very High | Most liquidity-sensitive major asset |
| Gold | GC=F | High | Real rate + liquidity sensitive |
| Nasdaq | ^IXIC | High | Growth stocks = long duration |
| S&P 500 | ^GSPC | Medium | Broader market, less pure liquidity play |
| US Dollar | DX-Y.NYB | Inverse | Liquidity ↑ → USD typically ↓ |
| EM Equities | EEM | Very High | Global liquidity = EM fuel |

## Global Liquidity Cycle Phases

| Phase | Characteristics | Asset Implication |
|-------|---------------|-------------------|
| **Phase 1: Expansion** | Central banks easing, credit growing, net liquidity rising | Risk-on: BTC, EM, commodities ↑ |
| **Phase 2: Peak** | Liquidity growth decelerating, central banks signaling pause | Cautious: reduce risk, gold holds |
| **Phase 3: Contraction** | QT, credit tightening, net liquidity falling | Risk-off: cash, USD, short duration |
| **Phase 4: Trough** | Liquidity contraction slowing, easing signals emerging | Bottom-fishing: prepare for reversal |

## Process

```bash
# 1. Fetch Fed data
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"WALCL","limit":52}'
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"TGA","limit":52}'
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"RRPONTSYD","limit":52}'

# 2. Calculate net liquidity
python3 liquidity/scripts/net_liquidity.py --months 12

# 3. Run Scissors Factor
python3 liquidity/scripts/scissors_factor.py --all --export json
```

## Output Template

```markdown
## Global Liquidity Dashboard — [Date]

### Central Bank Summary
| Central Bank | Policy Rate | Balance Sheet Trend | Liquidity Contribution |
|-------------|-------------|-------------------|----------------------|
| Fed | X.XX% | QT -$XXB/mo | Negative / Neutral |
| ECB | X.XX% | QT -€XXB/mo | Negative / Neutral |
| BOJ | X.XX% | Expanding / Steady | Positive / Neutral |
| PBOC | X.XX% (MLF) | Credit impulse: +X.X% | Positive / Negative |

### Global Liquidity Index
- Current Level: $XX.XT (equivalent)
- YoY Change: +X.X%
- 3-Month Trend: Expanding / Contracting
- Cycle Phase: [Phase 1/2/3/4]

### Scissors Factor Signals
| Asset | Price YoY | Liq YoY | SF | Signal | Score |
|-------|----------|---------|-----|--------|-------|
| Bitcoin | +XX% | +X.X% | +X.X | Buy | 0.XX |
| Gold | +XX% | +X.X% | +X.X | Hold | 0.XX |
| Nasdaq | +XX% | +X.X% | +X.X | Buy | 0.XX |
| S&P 500 | +XX% | +X.X% | +X.X | Hold | 0.XX |
| USD Index | -XX% | +X.X% | +X.X | Sell | 0.XX |

### Regime Assessment
- Primary Regime: [Liquidity Expansion / Transition / Contraction]
- Confidence: [High / Medium / Low]
- Key Risk: [PBOC stimulus insufficient / ECB over-tightening / etc.]
```

## Red Flags
- Global liquidity aggregation is approximate — precise data lags differ across CBs
- PBOC data is less transparent — treat credit impulse as directionally informative
- Scissors Factor works best at extremes — noisy in neutral ranges
- Asset prices can front-run liquidity changes by months (expectations-driven)
- Currency movements affect cross-border liquidity (strong USD = tighter global conditions)
