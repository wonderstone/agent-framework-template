---
name: liquidity-to-assets
description: Global liquidity conditions mapped to asset class performance. Analyzes how central bank liquidity expansion/contraction drives risk appetite, correlation regimes, and cross-asset returns using historical relationships.
category: finance-macro
domain: macro-bridge
allowed-tools: Bash(python3:*) Read(*)
---

# Liquidity-to-Assets — Liquidity Transmission

## Purpose

Map global liquidity conditions to asset class performance. Central bank liquidity is the single most powerful driver of cross-asset returns — this skill quantifies the historical relationships and generates forward-looking signals based on current liquidity conditions.

## When to Use

- "How will QT ending affect crypto?"
- "What does current liquidity mean for my asset allocation?"
- "Liquidity cycle phase and asset implications?"
- "RRP drain = bullish for what?"
- "Global liquidity contraction — what to avoid?"

## Liquidity → Asset Sensitivity Map

Historical beta to changes in global net liquidity:

| Asset Class | Liquidity Beta | R² | Regime Dependence |
|------------|---------------|-----|-------------------|
| Bitcoin / Crypto | 1.8-2.5 | 0.65 | Highest in expansion |
| Emerging Market Equities | 1.2-1.8 | 0.55 | Consistent |
| Nasdaq / Growth Stocks | 1.0-1.5 | 0.50 | Higher when rates low |
| High Yield Credit | 0.8-1.2 | 0.45 | Consistent |
| S&P 500 | 0.6-1.0 | 0.40 | Lower in earnings-driven markets |
| Gold | 0.5-0.8 | 0.30 | Highest during real rate declines |
| Investment Grade Credit | 0.3-0.6 | 0.25 | Consistent |
| US Dollar (DXY) | -0.5 to -1.0 | 0.35 | Inverse relationship |
| Government Bonds | -0.2 to 0.3 | 0.10 | More driven by rates/inflation |
| Commodities (broad) | 0.3-0.7 | 0.20 | More driven by demand/supply |

## Liquidity Regime → Asset Allocation

| Regime | Liquidity Direction | Overweight | Underweight |
|--------|-------------------|-----------|-------------|
| **QE + Rate Cuts** | Strong expansion | Crypto, EM, Growth, Gold | Cash, USD, IG bonds |
| **QE + Hold** | Moderate expansion | Equities, HY, Gold | Cash, Short bonds |
| **QT + Hold** | Moderate contraction | Quality, DM equities, Cash | Crypto, EM, HY |
| **QT + Rate Hikes** | Strong contraction | Cash, USD, Defensive, Gold | Crypto, Growth, EM, HY |
| **Transition (QT end signal)** | Inflection | Growth, Crypto, HY | Cash, USD |

## Liquidity Correlation Regimes

```
High Liquidity (QE): "Risk-on" correlation — everything up, low vol
                     Crypto leads, EM follows, USD down
                     Correlation across assets ↑

Low Liquidity (QT):  "Risk-off" correlation — everything down, vol spikes
                     USD up, crypto crushed, EM sells off
                     Correlation across assets ↑ (all sell off)

Transition:          Divergence — quality/duration differentiated
                     Correlation ↓ — stock-picking matters
```

## Process

1. Calculate current global net liquidity (use `liquidity/cross-border-liquidity`)
2. Determine liquidity regime (Expansion / Peak / Contraction / Trough)
3. Map regime to asset allocation tilt
4. Check Scissors Factor for specific assets
5. Generate allocation recommendations

## Output Template

```markdown
## Liquidity-to-Assets Analysis — [Date]

### Liquidity Status
- Global Net Liquidity: $X.XT equivalent
- YoY Change: +X.X%
- Regime: [Phase 1/2/3/4]
- 3-Month Trend: [Expanding / Contracting]

### Asset Allocation Tilt
| Asset Class | Current Weight | Liquidity Signal | Recommended Tilt |
|------------|---------------|-----------------|-----------------|
| Bitcoin/Crypto | X% | Strong Buy | Overweight |
| EM Equities | X% | Buy | Overweight |
| Nasdaq | X% | Hold | Market Weight |
| S&P 500 | X% | Hold | Market Weight |
| Gold | X% | Buy | Overweight |
| HY Credit | X% | Hold | Market Weight |
| IG Credit | X% | Hold | Market Weight |
| Cash | X% | Avoid | Underweight |
| Government Bonds | X% | Hold | Market Weight |

### Key Risks
- [Risk 1: e.g., RRP exhaustion causing temporary tightness]
- [Risk 2: e.g., TGA rebuild draining reserves]
- [Risk 3: e.g., PBOC not easing enough to offset Fed]

### Confidence
- High: [Relationship name]
- Medium: [Relationship name]
- Low: [Relationship name]
```

## Red Flags
- Liquidity-asset relationships are strongest at extremes, noisy in between
- "Don't fight the Fed" works until it doesn't (earnings can overpower liquidity)
- Crypto is the purest liquidity play — highest beta in both directions
- Liquidity drives CORRELATION more than DIRECTION — assets can rise together or fall together
- R² values are moderate — liquidity is one factor among many (earnings, geopolitics, positioning)
