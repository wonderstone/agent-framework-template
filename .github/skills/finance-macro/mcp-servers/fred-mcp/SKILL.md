---
name: fred-mcp
description: MCP server for Federal Reserve Economic Data (FRED). Provides 800,000+ US economic time series. Requires free FRED_API_KEY from fred.stlouisfed.org.
category: finance-macro
domain: mcp-server
---

# FRED MCP Server

US economic data from the St. Louis Fed. 800,000+ series covering GDP, inflation, employment, interest rates, money supply, and more.

## Setup

```bash
export FRED_API_KEY="your-key"  # Get from https://fred.stlouisfed.org/docs/api/api_key.html
```

## Key Series Quick Reference

See `mcp-servers/fred-mcp/server.py` for the full series reference. Key codes:

| Code | Description | Frequency |
|------|-------------|-----------|
| GDP | Gross Domestic Product | Quarterly |
| GDPC1 | Real GDP | Quarterly |
| UNRATE | Unemployment Rate | Monthly |
| CPIAUCSL | CPI All Urban | Monthly |
| PCEPILFE | Core PCE | Monthly |
| FEDFUNDS | Fed Funds Rate | Daily |
| WALCL | Fed Total Assets | Weekly |
| TGA | Treasury General Account | Daily |
| RRPONTSYD | Overnight Reverse Repo | Daily |
| M2SL | M2 Money Supply | Monthly |
| DGS10 | 10-Year Treasury | Daily |
| T10Y2Y | 10Y-2Y Spread | Daily |
