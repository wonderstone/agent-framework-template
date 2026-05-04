---
name: tax-policy
description: Tax structure analysis — tax/GDP ratio, tax mix, progressivity, corporate tax competitiveness, and tax expenditure analysis. Connects tax policy to growth, inequality, investment, and fiscal sustainability.
category: finance-macro
domain: fiscal-policy
allowed-tools: Bash(python3:*) Read(*)
---

# Tax Policy Analysis

## Purpose

Analyze a country's tax structure and its macroeconomic implications. Tax policy shapes incentives for work, saving, investment, and consumption. The structure of taxation — who pays, how much, and through what channels — determines economic efficiency, equity, and fiscal sustainability.

## When to Use

- "Tax system analysis for [Country]"
- "Corporate tax competitiveness?"
- "Tax-to-GDP ratio comparison"
- "Tax incidence analysis"
- "VAT vs income tax efficiency"
- "Tax expenditure analysis"

## Tax Structure Metrics

### Tax-to-GDP Ratio
| Country Group | Typical Range | Interpretation |
|--------------|--------------|---------------|
| Nordic model | 40-47% | High tax, high services |
| Western Europe | 35-45% | Comprehensive welfare state |
| Anglo-Saxon | 25-35% | Lower tax, mixed provision |
| EM Asia | 15-25% | Lower tax, developing infrastructure |
| EM LatAm | 15-25% | Tax evasion challenges |
| Tax Havens / Low-Tax | 5-15% | Financial center model |

### Tax Mix Efficiency

| Tax Type | Efficiency | Equity | Revenue Stability | Growth Impact |
|----------|-----------|--------|------------------|--------------|
| VAT / GST (broad-based) | High | Regressive | High | Low negative |
| Personal Income Tax (progressive) | Medium | Progressive | Medium | Medium negative |
| Corporate Income Tax | Low | Progressive | Low (cyclical) | High negative |
| Property / Land Tax | Very High | Progressive | High | Very Low negative |
| Social Security Contributions | Medium | Regressive (caps) | Medium | Medium negative |
| Excise / Pigouvian Taxes | High | Regressive | Medium | Can be positive |
| Financial Transaction Tax | Low | Progressive | Low | High negative |
| Wealth Tax | Medium-Low | Very Progressive | Low | Medium negative |

**Key Tradeoff**: VAT is economically efficient (doesn't distort saving/investment) but regressive. Income tax is progressive but has higher economic cost. Property/land tax is the "best" tax economically but politically difficult.

## Tax Competitiveness Indicators

### Corporate Tax

| Indicator | Competitive | Average | Uncompetitive |
|-----------|-----------|---------|---------------|
| Statutory CIT Rate | < 20% | 20-30% | > 30% |
| Effective Marginal Rate (EMTR) | < 20% | 20-30% | > 30% |
| R&D Tax Incentives (B-Index) | Generous | Average | None |
| Cross-Border Tax (WHT, CFC rules) | Territorial | Mixed | Worldwide |
| Digital Services Tax | No | — | Yes (adds complexity) |

### Personal Tax

| Indicator | Competitive | Average | Uncompetitive |
|-----------|-----------|---------|---------------|
| Top Marginal PIT Rate | < 40% | 40-50% | > 50% |
| Top Rate Threshold (× avg wage) | > 10× | 3-10× | < 3× |
| Capital Gains Tax Rate | < 20% | 20-30% | > 30% |
| Inheritance/Estate Tax | None | Modest | High |

## Tax Expenditure Analysis

Tax expenditures (deductions, credits, exemptions, deferrals) are "spending through the tax code":

| Common Tax Expenditure | Annual Cost (% GDP) | Primary Beneficiaries | Efficiency |
|----------------------|--------------------|----------------------|-----------|
| Mortgage Interest Deduction | 0.3-1.0% | High-income homeowners | Low |
| Retirement Savings Preference | 0.5-1.5% | High-income (biggest accounts) | Mixed |
| Employer Health Insurance Exclusion (US) | 1.0-1.5% | Middle-high income | Distortionary |
| R&D Tax Credit | 0.1-0.3% | Corporations | Moderate-High |
| Lower Capital Gains Rate | 0.2-0.5% | Top 1% (disproportionately) | Low |
| VAT Exemptions / Reduced Rates | 0.5-2.0% | Diffuse | Very Low |

**Key Insight**: Tax expenditures are equivalent to government spending but face less scrutiny — total tax expenditures often exceed the fiscal deficit.

## Country Tax Profiles

### New Zealand
- **Strengths**: Broad-base GST (15%), no payroll tax, no capital gains tax (broadly), simple system
- **Weaknesses**: High corporate tax (28%) vs OECD avg (~23%), no inflation indexation of brackets (fiscal drag), housing tax advantages (no CGT, no stamp duty)
- **Tax/GDP**: ~32% (OECD avg ~34%)
- **Key Issue**: Housing tax preference channels investment into property over productive assets

## Output Template

```markdown
## Tax Policy Analysis: [Country] — [Date]

### Tax Structure
| Tax | Rate | % Total Revenue | OECD/Regional Avg |
|-----|------|---------------|-------------------|
| VAT/GST | XX% | XX% | XX% |
| Personal Income (Top) | XX% | XX% | XX% |
| Corporate Income | XX% | XX% | XX% |
| Social Security | XX% | XX% | XX% |
| Property | X.X% effective | X% | X% |
| Other | | XX% | |

### Key Metrics
- Tax/GDP: XX% (Peer avg: XX%)
- Tax Mix Efficiency Score: XX/100
- Corporate Tax Competitiveness: [Competitive / Average / Uncompetitive]
- VAT Gap (compliance): XX% of theoretical revenue

### Key Tax Expenditures
| Expenditure | Est. Cost (% GDP) | Assessment |
|-----------|------------------|------------|
| [Expenditure 1] | X.X% | |
| [Expenditure 2] | X.X% | |

### Assessment
- Overall: [Efficient / Average / Distortionary] tax system
- Key Reform Opportunity: [Most impactful change with least political difficulty]
```

## Red Flags
- Tax-to-GDP < 15% in EM usually means state capacity is too weak for development needs
- Reliance on corporate tax > 25% of revenue = high fiscal volatility (profit cycle)
- Reliance on commodity royalties > 30% = extreme fiscal volatility
- Top PIT rate > 50% at < 3× average wage = brain drain risk (highly mobile workers leave)
- VAT compliance gap > 30% = fundamental administrative failure — fix before raising rates
