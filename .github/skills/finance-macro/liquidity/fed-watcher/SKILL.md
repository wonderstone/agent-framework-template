---
name: fed-watcher
description: Monitor Federal Reserve balance sheet, track quantitative tightening/easing, Treasury General Account, Reverse Repo facility, M2 money supply, and bank reserves. Calculate net liquidity and detect policy regime shifts.
category: finance-macro
domain: liquidity
allowed-tools: Bash(python3:*) Read(*)
---

# Fed Watcher — Federal Reserve Liquidity Analysis

## Purpose

Real-time analysis of Federal Reserve liquidity operations. Monitors the Fed's balance sheet (WALCL), Treasury General Account (TGA), Overnight Reverse Repo facility (RRP), M2 money supply, and bank reserves. Calculates net liquidity injected into the financial system and identifies QT/QE regime changes.

## When to Use

- "What is the Fed's balance sheet at?"
- "Is QT still running? How much has been drained?"
- "What's the TGA balance and what does it mean for liquidity?"
- "Are bank reserves declining?"
- "How fast is M2 contracting/expanding?"
- "What's the net liquidity picture?"

## Key Indicators

| Indicator | FRED Series | Frequency | What It Tells Us |
|-----------|-------------|-----------|------------------|
| Fed Total Assets | WALCL | Weekly (Thu) | Size of Fed balance sheet — QE increases, QT decreases |
| Treasury General Account | TGA | Daily | Government's checking account — rising drains liquidity |
| Overnight Reverse Repo | RRPONTSYD | Daily | MMF cash parked at Fed — absorbs excess liquidity |
| M2 Money Supply | M2SL | Monthly | Broad money — leading indicator for inflation/assets |
| Bank Reserves | TOTRESNS | Monthly | Excess reserves in banking system — lending capacity |
| Securities Held Outright | WSHOSHO | Weekly | Fed's bond portfolio — primary QT/QE metric |
| Reserve Bank Credit | WALCL component | Weekly | Total credit extended by Fed |

## Process

### Step 1: Fetch Raw Data
```bash
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"WALCL","limit":24,"sort_order":"desc"}'
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"TGA","limit":24,"sort_order":"desc"}'
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"RRPONTSYD","limit":24,"sort_order":"desc"}'
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"M2SL","limit":12,"sort_order":"desc"}'
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"TOTRESNS","limit":12,"sort_order":"desc"}'
```

### Step 2: Calculate Net Liquidity
```bash
python3 liquidity/scripts/net_liquidity.py --latest
```

Output includes: WALCL, TGA, RRP, Net Liquidity, weekly change, 3-month trend.

### Step 3: Analyze QT/QE Pace
- QT: WSHOSHO declining ~$60B/month (Treasuries) + $35B/month (MBS) = ~$95B/month runoff cap
- Check if actual runoff matches cap (Treasury runoff often below cap due to low coupon maturities)
- TGA rebuild = additional liquidity drain
- RRP decline = partially offsets QT (RRP → reserves conversion)

### Step 4: Assess Regime
- **QE Regime**: WALCL rising, reserves rising, M2 expanding
- **QT Regime**: WALCL falling, reserves falling, M2 contracting
- **Transition**: QT slowing/ending signs → WALCL stabilizes, RRP near zero
- **Emergency**: WALCL spiking, discount window usage

## Net Liquidity Framework

```
Components:
  Fed Assets (WALCL)         = Securities held + discount window + other assets
  - TGA                      = Treasury's cash balance (drains when rising)
  - RRP (RRPONTSYD)         = Money market funds parked at Fed
  ─────────────────────────────────────────────────────────
  = Net Liquidity            = Effective money in financial system

Additional drain (optional):
  - Foreign repo pool        = Smaller, less tracked

Key relationships:
  Net Liquidity ↑ → risk assets tend to rise
  Net Liquidity ↓ → tighter financial conditions
  RRP → 0      → QT starts to bite (reserves directly drained)
```

## Output Template

```markdown
## Fed Liquidity Dashboard

### Balance Sheet (Latest Week: YYYY-MM-DD)
| Metric | Value | Weekly Change | 3-Month Trend |
|--------|-------|---------------|---------------|
| Fed Assets (WALCL) | $X.XXT | -$XX.XB | ↓ |
| Securities Held | $X.XXT | -$XX.XB | ↓ |
| TGA Balance | $XXXB | +$XXB | → |
| RRP Facility | $XXXB | -$XXB | ↓ |
| **Net Liquidity** | **$X.XXT** | **+$XXB** | **↑/↓/→** |

### Money Supply
| Metric | Value | YoY Change |
|--------|-------|------------|
| M2 | $X.XXT | +X.X% |
| Bank Reserves | $X.XXT | -X.X% |

### QT Progress
- Total QT since peak: $X.XXT
- Monthly runoff rate: $XXB (vs $95B cap)
- Estimated QT remaining at current pace: X months
- RRP exhaustion projected: QX 20XX

### Assessment
- Regime: QT / QE / Transition
- Financial conditions: Tightening / Neutral / Easing
- Key risk: [TGA rebuild / RRP exhaustion / reserves scarcity]
```

## Red Flags
- WALCL data is Thursday close, released Friday — not real-time
- TGA can swing ±$100B in a single day around tax dates
- RRP at zero = QT starts directly draining reserves = potential volatility
- M2 data lags 1 month
- Ignoring Treasury debt issuance = incomplete liquidity picture
