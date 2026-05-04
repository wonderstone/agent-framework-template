# Macroeconomic Data Sources Reference

## Free Tier Sources (No API Key Required)

| Source | Coverage | Frequency | API | Notes |
|--------|----------|-----------|-----|-------|
| **World Bank** | 200+ countries, 1,400+ indicators | Annual, some quarterly | REST, no key needed (1k/day) | Best for cross-country comparison |
| **IMF Data** | 190+ countries, IFS, WEO, BOP | Monthly, quarterly, annual | REST, registration required | Gold standard for macro data |
| **BIS Statistics** | 40+ countries, banking, debt, derivatives | Quarterly, semi-annual | REST, no key | Best for financial stability data |
| **ECB SDW** | Eurozone, 20 countries | Daily to annual | REST, no key | Best for European macro data |
| **OECD Data** | 38 member countries | Monthly to annual | REST, no key | Policy-relevant indicators |
| **UN Comtrade** | All countries, trade flows | Annual | REST, registration | Trade by commodity (HS codes) |
| **Eurostat** | EU countries | Monthly to annual | REST, bulk download | EU-specific data |

## API-Key Required (Free Registration)

| Source | Coverage | Key Source | Notes |
|--------|----------|------------|-------|
| **FRED (St. Louis Fed)** | US economic data, 800k+ series | fred.stlouisfed.org | Best for US macro |
| **BLS (US Bureau of Labor Statistics)** | US employment, CPI, wages | bls.gov/developers | US labor market |
| **BEA (US Bureau of Economic Analysis)** | US GDP, trade, income | bea.gov/apitoken | US national accounts |

## National Statistics Offices

| Country | Source | API | Key Needed |
|---------|--------|-----|------------|
| New Zealand | Stats NZ (stats.govt.nz) | Aotearoa Data Explorer | No |
| Australia | ABS (abs.gov.au) | ABS.Stat API | Registration |
| United Kingdom | ONS (ons.gov.uk) | ONS API | No |
| Canada | Statistics Canada | Web Data Service | No |
| China | National Bureau of Statistics | data.stats.gov.cn | Registration |
| Japan | e-Stat (e-stat.go.jp) | e-Stat API | No |
| Singapore | SingStat (singstat.gov.sg) | SingStat API | Registration |

## Market/Pricing Data

| Source | Coverage | API | Key Needed |
|--------|----------|-----|------------|
| Yahoo Finance | Global stocks, ETFs, FX, crypto | Python yfinance | No |
| Alpha Vantage | Global stocks, FX, crypto | REST | Free key (25/day) |
| Polygon.io | US stocks, options, FX | REST | Free tier available |
| FRED | US Treasury yields, TIPS, spreads, corporate bonds | REST | Free key |

## Real-Time / Alternative Data

| Source | Coverage | Notes |
|--------|----------|-------|
| GDPLive (NZ) | NZ real-time GDP, CPI | ML-based nowcasting |
| Trading Economics | 196 countries, 20M indicators | Commercial, free trial |
| Google Trends | Search interest by topic/region | Free API |
| Wikipedia Pageviews | Topic attention proxy | Free API |

## Using the MCP Servers

Each data source has an MCP server in `mcp-servers/`:

```
mcp-servers/
├── fred-mcp/        # python3 server.py <tool> '<json_args>'
├── worldbank-mcp/   # python3 server.py <tool> '<json_args>'
├── imf-mcp/         # python3 server.py <tool> '<json_args>'
├── bis-mcp/         # python3 server.py <tool> '<json_args>'
└── stats-mcp/       # python3 server.py <tool> '<json_args>'
```

All MCP servers accept the same interface: `python3 server.py <tool_name> '<json_arguments>'`
