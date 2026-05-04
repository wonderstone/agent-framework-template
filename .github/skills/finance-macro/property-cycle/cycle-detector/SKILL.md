---
name: cycle-detector
description: Real estate cycle phase detection using price momentum, credit conditions, construction activity, and sentiment indicators. Classifies markets into Recovery, Boom, Bust, or Stabilization phases.
category: finance-macro
domain: property-cycle
allowed-tools: Bash(python3:*) Read(*)
---

# Property Cycle Detector

## Purpose

Detect the current phase of the real estate cycle for any country or city using a multi-indicator framework. The property cycle is one of the most predictable economic cycles (18-year average) — correct phase identification is the foundation of property investment, mortgage risk management, and construction sector analysis.

## When to Use

- "Where are we in the property cycle?"
- "Is it time to buy or sell property?"
- "Property market overheating?"
- "Is the housing correction over?"
- "Which cycle phase is [City/Country] in?"

## Phase Detection Framework

### 7-Indicator Model

| # | Indicator | Weight | Recovery | Boom | Bust | Stabilization |
|---|-----------|--------|----------|------|------|---------------|
| 1 | Real House Price Momentum (12M) | 25% | Flat to +3% | +5 to +15% | -5 to -15% | -3 to +3% |
| 2 | Price-to-Income vs LT Avg | 20% | Below avg | Above avg | Falling to avg | At avg |
| 3 | Housing Credit Growth (YoY) | 15% | Low, turning up | High, accelerating | Contracting | Turning positive |
| 4 | Building Approvals (YoY) | 15% | Low, stabilizing | High, rising | Collapsing | Bottoming |
| 5 | Months of Inventory | 10% | High, declining | Low (<3 months) | Rising rapidly | Peaking, then declining |
| 6 | Auction Clearance Rate | 10% | 50-60% (improving) | > 70% | < 50% | 50-60% (stabilizing) |
| 7 | Investor Activity (% of lending) | 5% | Low, turning up | High (>35%) | Very low | Low |

### Phase Classification

Each indicator is scored -2 (bust signal) to +2 (boom signal). Weighted sum determines phase:

| Score Range | Phase | Signal |
|-------------|-------|--------|
| +8 to +14 | Boom (Late) | Reduce — speculative excess |
| +4 to +7 | Boom (Early-Mid) | Hold — momentum intact |
| -3 to +3 | Transition | Watch — phase change approaching |
| -7 to -4 | Bust (Early-Mid) | Avoid — correction underway |
| -14 to -8 | Bust (Late) / Stabilization | Screen for value — bottom forming |

## Country Data Sources

| Country | House Price Index | Source |
|---------|------------------|--------|
| US | Case-Shiller National | FRED: CSUSHPISA |
| UK | UK HPI / Nationwide | ONS API |
| Australia | CoreLogic HVI | ABS / CoreLogic |
| New Zealand | REINZ HPI | REINZ / RBNZ |
| Canada | Teranet-National Bank HPI | CREA / Teranet |
| China | 70-City Index | NBS |

## Process

```bash
# US example
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"CSUSHPISA","limit":60}'
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"HOUST","limit":60}'
python3 mcp-servers/fred-mcp/server.py get_series '{"series_id":"MORTGAGE30US","limit":24}'

# NZ example  
python3 mcp-servers/stats-mcp/server.py get_series '{"series_id":"house-price-index"}'
```

## Red Flags
- National averages mask city-level divergence — drill down to city for investment decisions
- The cycle can extend — Phase 2 (Boom) has lasted 15+ years in some markets (Australia 1991-2017 with brief interruptions)
- Policy intervention (macroprudential, tax) can accelerate or delay phase transitions
- The 18-year cycle is an empirical observation, not a law — treat as framework, not prediction
