---
name: rate-path
description: Interest rate transmission to sectors and assets. Analyzes how policy rate changes flow through discount rates, borrowing costs, and bank profitability to impact equity sectors, bonds, real estate, and currencies.
category: finance-macro
domain: macro-bridge
allowed-tools: Bash(python3:*) Read(*)
---

# Rate Path — Interest Rate Transmission

## Purpose

Analyze how interest rate changes transmit to the real economy and financial assets. The rate channel is the primary monetary policy transmission mechanism — understanding its sector-level impact is fundamental to macro-aware investing.

## When to Use

- "How do higher rates affect tech stocks?"
- "Which sectors benefit from rate cuts?"
- "Impact of rising 10Y yields on housing?"
- "What's the rate sensitivity of my portfolio?"
- "How much have financial conditions tightened?"

## Transmission Channels

### 1. Discount Rate Channel
```
Higher rates → Higher discount rate → Lower PV of future cash flows
Impact: LONG-DURATION assets most affected (growth stocks, long bonds, real estate)
```

**Duration Sensitivity by Sector:**
| Sector | Duration (years) | Rate Sensitivity |
|--------|-----------------|-----------------|
| Tech / SaaS | 15-25 | Very High |
| Biotech | 12-20 | Very High |
| Real Estate / REITs | 8-15 | High |
| Utilities | 8-12 | High |
| Consumer Staples | 6-10 | Medium |
| Banks | 2-5 | Low (benefit from higher rates) |
| Energy | 3-6 | Low |

### 2. Borrowing Cost Channel
```
Higher rates → Higher borrowing costs → Lower investment, hiring, M&A
Impact: LEVERAGED sectors most affected (real estate, PE-owned companies, small caps)
```

**Floating Rate Exposure:**
- High: Small caps (~40% floating), PE-owned companies, REITs, leveraged loans
- Medium: Mid-cap industrials, leveraged consumer
- Low: Large cap tech (cash-rich), staples

### 3. Bank Profitability Channel
```
Steeper curve → Higher NIM → Bank profit ↑
Flatter/Inverted curve → NIM compression → Bank profit ↓
```

### 4. Currency Channel
```
Higher rates → Capital inflows → Stronger currency 
→ Exporters hurt, importers benefit
```

## Rate Hike Impact Matrix

| Magnitude | Tech | Banks | REITs | Consumer Disc. | Industrials | Gold |
|-----------|------|-------|-------|---------------|-------------|------|
| +25bp | -1% | +0.5% | -0.5% | -0.5% | -0.5% | -0.5% |
| +50bp | -3% | +1% | -1.5% | -1% | -1% | -1% |
| +100bp | -6% | +2% | -3% | -2% | -2% | -1.5% |
| +200bp | -15% | +3% | -8% | -5% | -5% | -2% |

**Note:** These are first-order directional estimates. Actual impact depends on starting level, speed, and whether the move is expected or surprise.

## Process

1. Identify rate change scenario
2. Map to discount rate impact on each sector based on duration
3. Assess borrowing cost impact for leveraged sectors
4. Evaluate curve steepening/flattening implications for banks
5. Check currency channel for multinationals/exporters
6. Generate sector impact matrix and portfolio implications

## Red Flags
- Markets price expected changes ahead of time — only surprises move prices
- Rate cuts during recession are NOT bullish for equities initially
- The first rate cut often comes AFTER equities have already fallen 20%+
- Sector sensitivity changes with the cycle — banks benefit from rising rates until they cause a recession
- Real rates matter more than nominal rates for gold and growth stocks
