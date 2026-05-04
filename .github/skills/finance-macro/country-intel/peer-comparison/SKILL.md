---
name: peer-comparison
description: Cross-country economic benchmarking. Compare GDP growth, inflation, debt, current account, and structural indicators across peer groups using World Bank and IMF data.
category: finance-macro
domain: country-intel
allowed-tools: Bash(python3:*) Read(*)
---

# Peer Comparison

## Purpose

Benchmark a country against its economic peer group. Peer comparison contextualizes macro indicators — a 3% fiscal deficit means something very different in Japan (structural, domestic-funded) vs. Argentina (crisis-prone, FX debt). Uses World Bank and IMF data for standardized cross-country comparison.

## When to Use

- "Compare [Country A] vs [Country B]"
- "How does [Country] rank among peers?"
- "Which country is doing best in [region]?"
- "Peer group benchmarking"
- "Relative value across countries"

## Peer Groups

### By Development Level
| Group | Countries |
|-------|----------|
| Advanced Economies | US, JP, DE, UK, FR, IT, CA, AU, NL, CH, SE, NO, SG, KR, NZ... |
| Emerging Markets | CN, IN, BR, MX, ID, TR, TH, MY, PH, CO, CL, PE, PL, CZ, HU... |
| Frontier Markets | VN, BD, KE, NG, PK, EG, GH, LK, MA... |

### By Region
| Region | Countries |
|--------|----------|
| Asia-Pacific | CN, JP, KR, IN, AU, NZ, ASEAN |
| Europe | EU member states + UK, CH, NO |
| Americas | US, CA, MX, BR, AR, CL, CO, PE |
| Middle East & Africa | SA, AE, QA, IL, ZA, NG, KE, EG |

### By Economic Structure (Lens-based)
- Small Open Economies: NZ, SG, IE, DK, CH, NO, IL, IS, HK
- Commodity Exporters: AU, CA, BR, CL, NO, SA, RU, PE, ZA, ID
- Manufacturing Hubs: CN, VN, MX, KR, TW, DE, JP, TH, MY

## Comparison Dimensions

### Growth & Output
| Indicator | Country | Peer Avg | Peer Rank | Peer Best | Peer Worst |
|-----------|---------|----------|-----------|-----------|------------|
| Real GDP Growth (3Y avg) | | | | | |
| GDP per Capita (PPP) | | | | | |
| GDP per Capita Growth | | | | | |
| Output Gap (est.) | | | | | |

### Stability & Resilience
| Indicator | Country | Peer Avg | Peer Rank |
|-----------|---------|----------|-----------|
| CPI Inflation (YoY) | | | |
| Current Account (% GDP) | | | |
| Govt Debt (% GDP) | | | |
| FX Reserves (months) | | | |
| Sovereign Credit Rating | | | |

### Structural & Competitiveness
| Indicator | Country | Peer Avg | Peer Rank |
|-----------|---------|----------|-----------|
| Ease of Doing Business | | | |
| R&D Spending (% GDP) | | | |
| Infrastructure Quality | | | |
| Working-Age Population Growth | | | |

## Output Template

```markdown
## Peer Comparison: [Country] vs [Peer Group] — [Date]

### Peer Group: [Group Name] ([N] countries)

### Growth & Output
| Rank | Country | GDP Growth | GDP/Capita | Output Gap |
|------|---------|-----------|-----------|------------|
| 1 | [Country] | +X.X% | $XX,XXX | ±X.X% |
| 2 | | | | |
| ... | | | | |
| **X** | **[Target Country]** | **+X.X%** | **$XX,XXX** | **±X.X%** |

### Stability Metrics
| Indicator | Target | Peer Avg | Peer Median | Rank (1=best) |
|-----------|--------|----------|------------|---------------|
| CPI Inflation | X.X% | X.X% | X.X% | X/N |
| Govt Debt/GDP | XX% | XX% | XX% | X/N |
| Current Account | +X.X% | +X.X% | +X.X% | X/N |
| FX Reserves | X.X mo | X.X mo | X.X mo | X/N |

### Comparative Advantage / Disadvantage
**Relative Strengths:**
1. [Strength 1 — metric where country ranks top quartile]
2. [Strength 2]

**Relative Weaknesses:**
1. [Weakness 1 — metric where country ranks bottom quartile]
2. [Weakness 2]

### Key Differentiator
[What structural factor explains this country's divergence from the peer average?]

### Investment Implications
- Within peer group, [Country] offers [better/worse] risk-adjusted macro profile due to [reason].
- Key risk relative to peers: [risk factor]
```

## Red Flags
- Peer group selection fundamentally shapes conclusions — always justify the group
- Nominal GDP comparisons distorted by FX — use PPP for structural comparison
- Data recency varies across countries — note data vintage in comparisons
- Small countries can have large statistical revisions — be wary of ranking on small differences
- Ratings are lagging indicators — market pricing (CDS, spreads) leads ratings by 3-12 months
