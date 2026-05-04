---
name: country-brief
description: One-page country macroeconomic snapshot. Generates standardized country briefs with GDP, inflation, trade, fiscal, and financial indicators using World Bank and IMF data.
category: finance-macro
domain: country-intel
allowed-tools: Bash(python3:*) Read(*)
---

# Country Brief — 1-Page Macro Snapshot

## Purpose

Generate a standardized 1-page macroeconomic snapshot for any country. Pulls data from World Bank, IMF, and national sources to produce a consistent template that enables cross-country comparison and rapid familiarization with any economy.

## When to Use

- "Brief me on [Country X]"
- "Quick snapshot of the NZ economy"
- "How big is [Country X]'s economy?"
- "Key stats for [Country X]"
- First step in any country analysis

## Brief Template Structure

### Section 1: Economy at a Glance
- GDP (nominal USD), GDP per capita, GDP growth (5Y avg)
- Population, median age, urbanization rate
- Currency, exchange rate regime
- Credit rating (S&P / Moody's / Fitch)

### Section 2: Growth & Output
- Real GDP growth (current, 1Y ago, 5Y avg)
- GDP composition (consumption, investment, government, net exports)
- Key growth drivers (consumption-led, export-led, investment-led)
- Output gap estimate

### Section 3: Prices & Monetary
- CPI inflation (headline, core, trend)
- Central bank policy rate
- Real policy rate (nominal - CPI)
- Money supply growth, credit growth

### Section 4: External Sector
- Current account balance (% GDP)
- Trade balance, top exports (3), top imports (3)
- Foreign exchange reserves (months of imports)
- External debt (% GDP), net international investment position

### Section 5: Fiscal Position
- Government budget balance (% GDP)
- Government debt (% GDP)
- Revenue and expenditure (% GDP)
- Fiscal breakeven oil price (for oil exporters)

### Section 6: Financial Sector
- Banking sector assets (% GDP)
- NPL ratio, capital adequacy ratio
- Credit to private sector (% GDP)
- Key financial stability concerns

## Process

```bash
python3 mcp-servers/worldbank-mcp/server.py get_indicator '{"indicator":"NY.GDP.MKTP.CD","country":"NZL","date_range":"2018:2025"}'
python3 mcp-servers/worldbank-mcp/server.py get_indicator '{"indicator":"NY.GDP.MKTP.KD.ZG","country":"NZL","date_range":"2018:2025"}'
python3 mcp-servers/worldbank-mcp/server.py get_indicator '{"indicator":"NY.GDP.PCAP.CD","country":"NZL"}'
python3 mcp-servers/worldbank-mcp/server.py get_indicator '{"indicator":"FP.CPI.TOTL.ZG","country":"NZL"}'
python3 mcp-servers/worldbank-mcp/server.py get_indicator '{"indicator":"BN.CAB.XOKA.GD.ZS","country":"NZL"}'
python3 mcp-servers/worldbank-mcp/server.py get_indicator '{"indicator":"GC.DOD.TOTL.GD.ZS","country":"NZL"}'
```

Use `scripts/data_formatters.py` to produce standardized JSON and Markdown output.

## Country Profiles

For deep-dive data, see `references/country-profiles/` for pre-compiled profiles on NZ, AU, CN, US, UK. These contain country-specific indicator mappings and institutional context that supplements the standardized brief.

## Red Flags
- Small countries' data may be sparse — note data gaps explicitly
- National definitions differ (e.g., what counts as "government debt")
- Exchange rate effects distort USD-denominated comparisons across time
- GDP revisions can substantially change the picture (Nigeria 2013: +89% overnight)
- Informal economy not captured — important for EM (India: ~40% informal)
