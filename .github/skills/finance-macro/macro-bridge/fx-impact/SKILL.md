---
name: fx-impact
description: Exchange rate transmission to exporters, importers, multinational earnings, and country competitiveness. Analyzes FX moves through translation, transaction, and competitive channels.
category: finance-macro
domain: macro-bridge
allowed-tools: Bash(python3:*) Read(*)
---

# FX Impact — Exchange Rate Transmission

## Purpose

Analyze how exchange rate movements impact companies, sectors, and countries. FX is the most direct macro-to-micro transmission channel — every 1% move in a currency pair has calculable impacts on corporate earnings, trade flows, and capital allocation.

## When to Use

- "How does a stronger USD affect S&P 500 earnings?"
- "Which NZX companies benefit from a weaker NZD?"
- "CNY devaluation — winners and losers?"
- "EUR/USD parity implications?"
- "Yen weakness — who benefits?"

## Transmission Channels

### 1. Translation Effect (Accounting)
```
Foreign subsidiary earnings translated back to reporting currency.
Stronger reporting currency → Reported earnings mechanically lower.
~40% of S&P 500 revenues are foreign.
Every 1% USD appreciation = ~-0.5% hit to S&P 500 EPS.
```

### 2. Transaction Effect (Cash Flow)
```
Exporters: Sell in foreign currency, convert to domestic → benefit from weaker home currency
Importers: Buy in foreign currency → benefit from stronger home currency
```

### 3. Competitive Effect (Market Share)
```
Weaker currency → Export prices more competitive → Market share gain (with lag)
Persistent misalignment → Structural shift in industry competitiveness
```

## Currency Sensitivity by Country

### Commodity Currencies (AUD, NZD, CAD, NOK, BRL, ZAR, CLP)
| Country | Key Export | Currency Driver | 10% FX Move Impact |
|---------|-----------|----------------|-------------------|
| Australia | Iron ore, coal, LNG | Commodity prices, China demand | AUD ↓10% → ASX +5% (exporters), import inflation +2% |
| New Zealand | Dairy, meat, tourism | Commodity prices, RBNZ policy | NZD ↓10% → Fonterra payout +NZ$1.50/kg, tourism boost |
| Canada | Oil, gas, lumber | WTI, US growth | CAD ↓10% → TSX +4%, manufacturing boost |
| Norway | Oil, gas, seafood | Brent, sovereign fund flows | NOK ↓10% → Export boost, already wealthy |
| Brazil | Iron ore, soy, oil | Commodities, political risk | BRL ↓10% → Exporters +15%, import inflation +5% |

### Manufacturing Currencies (CNY, KRW, TWD, JPY, EUR, CHF)
| Country | Key Export | Currency Driver | 10% FX Move Impact |
|---------|-----------|----------------|-------------------|
| China | Electronics, machinery, textiles | PBOC management, trade surplus | CNY ↓10% → Export competitiveness +8%, global deflationary impulse |
| Japan | Autos, electronics, machinery | BOJ policy, carry trade | JPY ↓10% → Nikkei +3% (exporters), inflation import |
| Germany | Autos, machinery, chemicals | EUR/USD, global trade | EUR ↓10% → DAX +5%, export orders +3% |
| South Korea | Semiconductors, ships, autos | KRW/USD, tech cycle | KRW ↓10% → KOSPI +4%, chip export boost |

### Safe Haven / Reserve Currencies (USD, CHF, JPY — flight-to-quality)
| Currency | Behavior During Risk-Off | Impact on Domestic Market |
|----------|--------------------------|--------------------------|
| USD | Strengthens (global tightening) | S&P 500 earnings hit from translation |
| CHF | Strengthens (safe haven) | Swiss exporters suffer, SNB may intervene |
| JPY | Strengthens historically, weaker if BOJ holds | Nikkei sensitive to JPY direction |

## Process

```bash
# Check current FX levels
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"DEXUSUK","limit":30}'
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"DEXJPUS","limit":30}'
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"DEXCHUS","limit":30}'
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"DEXUSEU","limit":30}'
```

## Output Template

```markdown
## FX Impact Analysis — [Currency Pair / Move]

### FX Move
- Pair: [XXX/YYY]
- Move: ±X.X% over [period]
- Reason: [Driver — rate differential, commodity, risk-off, intervention]

### Sector Impact (for [Country])
| Sector | FX Sensitivity | Impact | Key Companies |
|--------|---------------|--------|--------------|
| Exporters | High Positive | +X% earnings | |
| Importers | High Negative | -X% costs | |
| Tourism | High Positive | +X% visitors | |
| Domestic | Low | Neutral | |

### Translation Impact (Multinationals)
- % Revenue Foreign: XX%
- Estimated EPS Impact: ±X.X%

### Competitive Impact
- Export price competitiveness: ±X%
- Import substitution incentive: [Higher/Lower]

### Capital Flow Implications
- Carry trade attractiveness: [Higher/Lower]
- Foreign investor sentiment: [Positive/Negative]
- Central bank response risk: [Intervention likely/unlikely]
```

## Red Flags
- Translation impact is accounting-only — doesn't affect cash flow
- FX moves driven by rate differentials have different sector impact than commodity-driven moves
- Central banks can intervene (BOJ, PBOC, SNB) — sudden reversals possible
- Currency hedging by corporates mutes short-term impact (most hedge 12 months)
- Competitive effect takes 6-18 months to fully materialize in trade data
