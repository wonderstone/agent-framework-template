---
name: boj-watcher
description: Monitor Bank of Japan monetary policy including YCC framework, JGB purchase operations, ETF holdings, and balance sheet. Track BOJ's unique ultra-loose stance and its implications for global carry trade and yen dynamics.
category: finance-macro
domain: liquidity
allowed-tools: Bash(python3:*) Read(*)
---

# BOJ Watcher — Bank of Japan Liquidity Analysis

## Purpose

Track the Bank of Japan's unique monetary policy framework. The BOJ is the last major central bank maintaining ultra-loose policy (negative/zero rates + asset purchases), making it a critical source of global liquidity. The BOJ-JGB yield curve control (YCC) and the yen carry trade are key global macro transmission mechanisms.

## When to Use

- "What is the BOJ doing?"
- "Is BOJ normalizing policy?"
- "YCC changes?"
- "BOJ balance sheet size?"
- "Yen carry trade dynamics?"
- "Japan rate hike implications?"

## Key Framework

### BOJ Policy Tools

| Tool | Current Setting | What It Does |
|------|----------------|-------------|
| Policy Rate (Short-term) | X.XX% | Overnight call rate target |
| YCC (10Y JGB) | ~1.0% reference (flexible) | Caps long-term rates |
| JGB Purchases | ¥X.XT/month | Yield curve control + balance sheet expansion |
| ETF Purchases | Suspended (March 2024) | Equity market support |
| J-REIT Purchases | Suspended | Property market support |
| CP/Corporate Bond Purchases | Winding down | Corporate funding support |

### BOJ Balance Sheet (Unique Features)

```
BOJ Assets:
  - JGB Holdings: ¥XXXT (~50% of all JGBs outstanding)
  - ETFs: ¥XXT (legacy from yield curve control era)
  - J-REITs, CP, Corporate Bonds: ¥XT (winding down)

BOJ Liabilities:
  - Current Account Balances (bank reserves): ¥XXXT
  - Banknotes: ¥XXXT
```

## BOJ Normalization — The Big Global Macro Risk

The BOJ has been the anchor of global low rates for decades. Normalization means:

### Domestic Implications
- JGB yields rise → government debt service costs increase (250%+ debt/GDP)
- Mortgage rates rise → property market pressure
- Bank profitability improves (decades of NIM compression reverses)
- Yen strengthens → export sector headwind

### Global Spillovers
- **Carry trade unwind**: Higher JPY rates = costlier to short JPY for carry
- **JGB repatriation**: Japanese investors (largest foreign holders of US Treasuries) may repatriate
- **Global rate floor rises**: BOJ was the anchor keeping global long-end rates low
- **EUR, AUD, NZD impact**: Carry trade funding currencies shift

## Yen Carry Trade Monitor

```
Carry Trade Attractiveness = 
  Target Currency Yield (e.g., USD 5.25%) 
  - JPY Funding Cost (BOJ rate X.XX%)
  - FX Hedge Cost (swap points)
  - Expected JPY appreciation
```

### Key Indicators
- USD/JPY level and momentum
- JPY speculative positioning (CFTC)
- JPY implied volatility
- Japan-US 2-year yield spread
- Japanese investor net foreign bond purchases

## Output Template

```markdown
## BOJ Liquidity Dashboard — [Date]

### Policy Settings
| Instrument | Current | Last Change | Next Meeting |
|-----------|---------|-------------|--------------|
| Policy Rate | X.XX% | [Date] | [Date] |
| YCC Band | ±X.XX% | [Date] | |
| JGB Purchase Pace | ¥X.XT/mo | [Date] | |

### Balance Sheet
| Metric | Value | YoY Change |
|--------|-------|------------|
| Total Assets | ¥XXXT | +X.X% |
| JGB Holdings | ¥XXXT | |
| ETF Holdings | ¥XXT | |
| Bank Reserves | ¥XXXT | |

### Normalization Progress
- Policy Rate: [Still negative / At zero / Above zero]
- YCC: [Rigid cap / Flexible / Abandoned]
- JGB Purchases: [Full pace / Tapering / Stopped]
- Normalization Phase: [1 (initial) / 2 (gradual) / 3 (accelerating) / Complete]

### Yen & Carry Trade
| Metric | Current | Signal |
|--------|---------|--------|
| USD/JPY | XXX | |
| JP-US 2Y Spread | X.XX% | Carry [attractive / neutral / unattractive] |
| JPY Spec Positioning | [Long / Neutral / Short] | |
| JPY 3M Implied Vol | XX.X% | |

### Global Spillover Assessment
- Liquidity Contribution: [Still adding / Neutral / Withdrawing]
- Carry Trade Risk: [Low — ample spread / Medium / High — repatriation risk]
- Key Scenario: [Gradual normalization / Disruptive rate shock / BOJ capitulates on YCC]
```

## Red Flags
- BOJ communication is deliberately vague — watch actions (purchase amounts), not words
- JGB market is ~50% BOJ-owned — price discovery is impaired
- Japanese banks hold large JGB portfolios — rapid yield rise = unrealized losses
- Yen intervention (MOF) is separate from BOJ — can create contradictory signals
- Japan's debt/GDP (250%+) means BOJ normalization is fundamentally constrained
