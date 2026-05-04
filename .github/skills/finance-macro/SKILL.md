---
name: finance-macro
description: Multi-domain macroeconomic analysis engine. 8 sub-domains, 5 live MCP data servers, 15+ quantitative models, orchestrator pipeline, scenario stress-testing, chart generation.
category: finance-macro
allowed-tools: Bash(python3:*) Read(*)
---

# Finance-Macro — Macroeconomic Analysis Engine

## Purpose

Comprehensive macroeconomic analysis combining live data (WorldBank, FRED, BIS, IMF, Stats NZ), quantitative models, and scenario stress-testing. Covers global liquidity, country intelligence, central banks, macro-to-asset transmission, commodities, property cycles, and fiscal policy.

## How to Use

Every analysis follows the same pattern:

```bash
# 1. Pipeline mode — one command
python3 scripts/orchestrator.py '{"domain":"country-intel","country":"JPN"}'
python3 scripts/orchestrator.py '{"domain":"property-cycle","country":"AUS","params":{"rate":"6.2"}}'

# 2. Individual model mode
python3 country-intel/scripts/macro_score.py --growth 1.8 --inflation 0.2 --cagdp -4.5 ...

# 3. Scenario stress-testing
python3 macro-bridge/scripts/stress_test.py --scenario fed-tightening --country NZL
python3 macro-bridge/scripts/stress_test.py --custom "rate=+2.0,oil=+3.0,liquidity=-2.0"
```

## Domain Map

| Query Trigger | Domain | Key Scripts |
|--------------|--------|-------------|
| GDP, CPI, unemployment, PMI, yield curve, recession risk | `macro-dashboard` | `indicator_hub.py`, `yield_curve.py` |
| Liquidity, Fed balance sheet, TGA, RRP, M2, scissors factor | `liquidity` | `net_liquidity.py`, `scissors_factor.py` |
| FOMC, ECB, hawkish/dovish, rate path, policy divergence | `central-bank` | `hawk_dove_scorer.py` |
| Rates → sectors, FX impact, commodity shock, stress test | `macro-bridge` | `stress_test.py`, `sector_mapper.py`, `asset_mapper.py` |
| Country economy, macro health score, risk radar | `country-intel` | `macro_score.py` |
| Oil/copper/gold, supercycle, commodity-macro linkage | `commodity-macro` | `supercycle_scorer.py` |
| Housing cycle, affordability, mortgage stress, cross-country | `property-cycle` | `cycle_score.py`, `affordability_calc.py` |
| Government debt, fiscal sustainability, multipliers | `fiscal-policy` | `debt_dynamics.py` |

## Data Layer

5 MCP servers provide live data. Two work without any API key:

| Server | Auth | Coverage |
|--------|------|----------|
| `worldbank` | **None** | 200+ countries, GDP/CPI/trade/debt/employment |
| `bis` | **None** | Credit-to-GDP, property prices, debt service ratios |
| `fred` | Free key | US economic data (GDP, CPI, employment, M2, Fed tools) |
| `imf` | Registration | WEO projections, IFS exchange rates, BoP |
| `stats` | Free key | Stats NZ, ABS (Australia), ONS (UK) |

Set keys in `.env` (copy from `.env.example`).

## Pipeline Architecture

```
Query → Orchestrator → MCP Fetch → Cache (SQLite) → Transform (yoy/avg/deviation)
       → Model Execution → Output (JSON) → Chart (PNG) / Markdown
```

Cross-domain linking: `schemas.py` enables automatic data flow between domains (e.g., liquidity conditions → macro-bridge asset signals, property cycle → country-intel financial stability dimension).

## Red Flags (Global)

- Single indicators never tell the full story — always check composite scores
- Data lags: official figures can be 2-6 months behind, use transaction/listing data for real-time
- Exchange rate effects distort USD-denominated cross-country comparisons
- Commodity prices are the most cyclical asset class — mean reversion is powerful
- Property cycles last years, not months — don't overtrade phase signals
- The 18-year property cycle is an empirical observation, not a law — treat as framework

## Sub-Domains

Each sub-domain has its own `SKILL.md` with domain-specific guidance, Red Flags, and interpretation context. Scripts handle the computation; SKILL.md provides the judgment layer.
