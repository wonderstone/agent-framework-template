---
name: agri-macro
description: Agricultural commodity macro analysis — grains, oilseeds, softs, dairy, and livestock. Tracks weather patterns, supply-demand balances, and macro transmission to food inflation, trade balances, and commodity-exporting economies.
category: finance-macro
domain: commodity-macro
allowed-tools: Bash(python3:*) Read(*)
---

# Agricultural Macro Analysis

## Purpose

Analyze agricultural commodity markets through a macroeconomic lens. Agriculture is uniquely weather-driven but deeply macro-relevant — food inflation is politically explosive in EM, agri-exporting nations (NZ, Brazil, Argentina) have commodity-correlated currencies, and food security is becoming a strategic priority.

## When to Use

- "Food price outlook?"
- "Dairy price analysis (GDT auction)?"
- "Wheat/corn/soybean supply-demand"
- "Weather impact on agriculture?"
- "Agricultural commodity inflation?"
- "NZ dairy outlook?"

## Key Agricultural Commodities

### Grains & Oilseeds
| Commodity | Key Producers | Key Importers | Key Macro Link |
|-----------|-------------|--------------|---------------|
| Corn | US, CN, BR | JP, MX, KR, EG | Ethanol (US), feed, food |
| Wheat | CN, IN, RU, US, FR | EG, ID, TR, NG, BR | Food staple — EM political risk |
| Soybeans | BR, US, AR | CN (60%+ of imports) | China feed demand, biodiesel |
| Rice | CN, IN, ID, TH, VN | PH, NG, SA, CI | Asian food security |
| Palm Oil | ID, MY | IN, CN, EU | Biofuel mandate, food |

### Softs
| Commodity | Key Producers | Key Macro Link |
|-----------|-------------|---------------|
| Coffee | BR, VN, CO | Consumer staple, Brazil frost risk |
| Cocoa | CI, GH, ID, EC | West Africa political/weather risk |
| Sugar | BR, IN, TH, CN | Ethanol diversion (Brazil), energy link |
| Cotton | IN, CN, US, BR | Textile demand = consumer spending |

### Livestock & Dairy
| Commodity | Key Producers | Key Macro Link |
|-----------|-------------|---------------|
| Dairy (WMP, SMP, butter, cheese) | NZ, EU, US, AU | NZD driver (25% of exports), GDT auction |
| Beef | US, BR, CN, AR | Income-elastic demand |
| Pork | CN (50% of global) | China CPI (pork weight ~2.5% of CPI!) |
| Lamb/Mutton | NZ, AU, CN | NZ export value premium |

## Key Macro Transmission

### Food Inflation — EM Political Risk
```
Food CPI Weight:
  DM: 10-15% of CPI basket
  EM: 25-45% of CPI basket (India ~39%, Nigeria ~51%, Egypt ~38%)

Food Price +30% → EM:
  → CPI +7-15pp
  → Political instability risk elevated
  → Central bank forced to hike (even if economy weak)
  → Currency pressure (import cost spiral)
```

### Dairy — New Zealand's Macro Anchor
```
GDT Price Index = Weighted avg of WMP, SMP, AMF, butter, cheddar

GDT ↑ 10%:
  → Fonterra milk price forecast +NZ$0.80-1.20/kgMS
  → NZ farmgate injection +NZ$1.5-2.0B (~0.5% GDP)
  → NZD supported (commodity income, terms of trade)
  → Regional spending (Waikato, Canterbury, Southland) boosted

GDT ↓ 10%:
  → Farm income squeeze, rural spending decline
  → NZD depreciation pressure
  → RBNZ more likely to cut
```

## Weather Monitoring

| Region | Key Season | Commodity Risk |
|--------|-----------|---------------|
| US Midwest | Apr-Sep | Corn, soybeans |
| Brazil (Center-West) | Oct-Mar | Soybeans, corn (safrinha) |
| Argentina (Pampas) | Nov-Mar | Soybeans, corn, wheat |
| Black Sea | Jul-Aug (harvest) | Wheat, sunflower |
| SE Asia | Year-round | Palm oil (El Niño risk) |
| India | Jun-Sep (monsoon) | Rice, sugar, cotton |
| New Zealand | Sep-Apr (dairy season) | Milk production, pasture growth |
| West Africa | Oct-Mar (dry season) | Cocoa (Harmattan wind risk) |

**Key Climate Patterns to Monitor:**
- El Niño: Dry in SE Asia/India/Australia, wet in South America, warm globally
- La Niña: Wet in SE Asia/Australia, dry in South America, cool globally
- IOD (Indian Ocean Dipole): Positive = dry in Australia (wheat, canola risk)

## Output Template

```markdown
## Agricultural Macro Analysis — [Date]

### Key Price Dashboard
| Commodity | Price | YoY | 5Y Percentile | Key Driver |
|-----------|-------|-----|--------------|------------|
| Wheat | $X.XX/bu | ±X% | XX%ile | |
| Corn | $X.XX/bu | ±X% | XX%ile | |
| Soybeans | $X.XX/bu | ±X% | XX%ile | |
| Dairy (GDT Index) | XXX | ±X% | XX%ile | |
| Live Cattle | $X.XX/lb | ±X% | XX%ile | |

### Food Inflation Risk
| Region | Current Food CPI | Trend | Risk Level |
|--------|-----------------|-------|------------|
| EM Aggregate | +X.X% | ↑/↓/→ | |
| DM Aggregate | +X.X% | ↑/↓/→ | |

### Weather Watch
- Current Risk: [El Niño / La Niña / Neutral]
- Key Region Alert: [Region] — [Commodity] — [Risk level]
- Next 30 Days: [Outlook]

### NZ Dairy Focus
- GDT Index: XXX (Change: ±X.X%)
- WMP Price: $X,XXX/MT
- Fonterra Forecast Range: $X.XX-X.XX/kgMS
- NZD Implication: [Supportive / Neutral / Headwind]

### Assessment
- Agflation Risk: [Low / Moderate / High]
- Key Country Exposure: [Egypt — wheat, Nigeria — wheat, Philippines — rice]
```

## Red Flags
- Weather forecasts beyond 14 days have limited skill — use for awareness, not prediction
- El Niño/La Niña are probabilistic signals, not certainties — 60-70% historical accuracy
- Food export bans spread contagiously — India rice ban (2023), Russia wheat floor price
- Ag commodities are the most supply-inelastic in short run — small supply deficits = large price spikes
- China pork cycle dominates global protein markets — African Swine Fever changed everything
