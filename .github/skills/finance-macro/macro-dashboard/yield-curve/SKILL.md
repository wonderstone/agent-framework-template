---
name: yield-curve
description: Treasury yield curve analysis with recession probability estimation. Tracks 2Y/10Y/30Y yields, 10Y-2Y and 10Y-3M spreads, TIPS real yields, breakeven inflation, and credit spreads.
category: finance-macro
domain: macro-dashboard
allowed-tools: Bash(python3:*) Read(*)
---

# Yield Curve Analyzer

## Purpose

Comprehensive Treasury yield curve analysis. The yield curve is the single most reliable leading indicator of recessions — every US recession since 1950 was preceded by a 10Y-3M inversion. This skill tracks the curve's level, slope, and curvature, plus real yields, inflation breakevens, and credit spreads.

## When to Use

- "Is the yield curve inverted?"
- "What's the recession probability from the yield curve?"
- "What are 10-year yields doing?"
- "How wide are credit spreads?"
- "What does the real yield tell us?"
- "Analyze the yield curve"

## Key Indicators

| Indicator | FRED Code | What It Tells Us |
|-----------|-----------|-----------------|
| 2-Year Treasury | DGS2 | Near-term rate expectations |
| 5-Year Treasury | DGS5 | Medium-term expectations |
| 10-Year Treasury | DGS10 | Benchmark long rate — discount rate for all assets |
| 30-Year Treasury | DGS30 | Long-term growth/inflation expectations |
| 3-Month T-Bill | DTB3 | Short-term rate (Fed-controlled) |
| 10Y-2Y Spread | T10Y2Y | Classic recession signal |
| 10Y-3M Spread | T10Y3M | Fed's preferred recession indicator |
| 10-Year TIPS Real Yield | DFII10 | Real rate — true cost of capital |
| 5-Year Breakeven | T5YIFR | 5-year inflation expectations |
| 10-Year Breakeven | T10YIE | 10-year inflation expectations |
| Fed Funds Rate | FEDFUNDS | Policy rate |
| BBB-10Y Spread | BAA10Y | Corporate credit stress |

## Yield Curve Shapes

| Shape | Configuration | Macro Signal |
|-------|--------------|-------------|
| **Normal (Steep)** | Long rates >> Short rates | Recovery/early expansion — growth expected |
| **Normal (Flat)** | Long rates ≈ Short rates | Late cycle — market pricing rate cuts ahead |
| **Inverted** | Short rates > Long rates | Recession signal — market expects rate cuts |
| **Bear Steepening** | Long rates rising faster | Inflation fears, fiscal risk premium |
| **Bull Steepening** | Short rates falling faster | Aggressive easing expectations |
| **Bear Flattening** | Short rates rising faster | Tightening cycle underway |
| **Bull Flattening** | Long rates falling faster | Flight to safety, recession fear |

## Recession Probability Model

Based on the NY Fed model using 10Y-3M spread:

```
Recession_Prob = f(10Y-3M spread)
```

| 10Y-3M Spread | Recession Probability (12mo) |
|---------------|------------------------------|
| > 1.0% | < 5% — Very low |
| 0.5% to 1.0% | 5-10% — Low |
| 0% to 0.5% | 10-25% — Elevated |
| -0.5% to 0% | 25-40% — High |
| -1.0% to -0.5% | 40-60% — Very high |
| < -1.0% | > 60% — Extreme |

**Important caveats:**
- Inversion typically leads recession by 12-24 months
- False positives exist (1966 — inversion, no recession within 2 years)
- The curve can steepen BEFORE a recession starts (bear steepening as cuts are priced)
- Post-GFC structural factors (QE, global savings glut) may have flattened the curve structurally

## Process

```bash
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"DGS2","limit":30}'
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"DGS10","limit":30}'
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"DGS30","limit":30}'
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"DTB3","limit":30}'
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"T10Y2Y","limit":30}'
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"T10Y3M","limit":30}'
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"DFII10","limit":30}'
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"T5YIFR","limit":30}'
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"BAA10Y","limit":30}'
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"FEDFUNDS","limit":30}'
```

## Output Template

```markdown
## Yield Curve Analysis — [Date]

### Current Rates
| Maturity | Yield | Weekly Change |
|----------|-------|---------------|
| 3-Month | X.XX% | ±X bp |
| 2-Year | X.XX% | ±X bp |
| 10-Year | X.XX% | ±X bp |
| 30-Year | X.XX% | ±X bp |

### Key Spreads
| Spread | Current | 1M Ago | 1Y Ago | Signal |
|--------|---------|--------|--------|--------|
| 10Y-2Y | X.XX% | X.XX% | X.XX% | Inverted/Normal |
| 10Y-3M | X.XX% | X.XX% | X.XX% | Inverted/Normal |
| 2Y-Fed Funds | X.XX% | X.XX% | X.XX% | |
| BBB-10Y | X.XX% | X.XX% | X.XX% | |

### Real Rates & Breakevens
| Metric | Current | Signal |
|--------|---------|--------|
| 10Y Real Yield | X.XX% | Restrictive/Neutral/Accommodative |
| 5Y Breakeven | X.XX% | |
| 10Y Breakeven | X.XX% | |

### Assessment
- Curve Shape: [Normal/Flat/Inverted/Bear Steepening/etc.]
- Recession Probability: XX% (12-month)
- Policy Rate Expectations: [cuts/hikes/hold priced in]
- Real Rate Stance: [Restrictive/Neutral/Accommodative]
```

## Red Flags
- 10Y-3M is more reliable than 10Y-2Y for recession prediction
- Inversion duration matters — 1-day inversion is noise, 1-month inversion is signal
- Post-QE world: curve may be structurally flatter due to Fed's bond holdings
- Credit spreads often blow out BEFORE the curve un-inverts
- Real yields above 2% = genuinely restrictive financial conditions
