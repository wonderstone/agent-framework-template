---
name: risk-radar
description: Country risk radar covering sovereign, currency, political, banking, and external risk dimensions. Five-axis risk assessment with trend indicators and trigger levels for each risk category.
category: finance-macro
domain: country-intel
allowed-tools: Bash(python3:*) Read(*)
---

# Risk Radar — Country Risk Assessment

## Purpose

Five-dimensional country risk assessment modeled on institutional risk frameworks. Scores each risk category: Sovereign, Currency, Political, Banking, and External — with trend direction and specific trigger levels for escalation. Designed for investors, credit analysts, and business decision-makers assessing country exposure.

## When to Use

- "What are the risks for [Country]?"
- "Country risk assessment for investment decision"
- "Early warning check for [Country]"
- "Is [Country] at risk of a crisis?"
- "Monitor my exposure to [Country]"

## Five Risk Dimensions

### 1. Sovereign Risk
Risk that the government defaults or restructures debt obligations.

| Indicator | Low Risk | Medium Risk | High Risk |
|-----------|----------|------------|-----------|
| Govt Debt / GDP | < 60% | 60-100% | > 100% |
| FX Debt / Total Debt | < 20% | 20-50% | > 50% |
| CDS Spread (5Y) | < 100bp | 100-300bp | > 300bp |
| Credit Rating | Investment Grade | BB+/BB | < BB- |
| IMF Program | No | Precautionary | Active / Off-track |

### 2. Currency Risk
Risk of sharp depreciation, devaluation, or convertibility restriction.

| Indicator | Low Risk | Medium Risk | High Risk |
|-----------|----------|------------|-----------|
| REER vs 10Y Avg | ±5% | ±5-15% | > ±15% |
| FX Reserves / Short-term Debt | > 200% | 100-200% | < 100% |
| Import Cover | > 6 months | 3-6 months | < 3 months |
| FX Regime Flexibility | Floating | Managed float | Fixed / Pegged |
| 3M Implied Volatility | < 8% | 8-15% | > 15% |
| Parallel Market Premium | 0% | < 5% | > 5% |

### 3. Political Risk
Risk of adverse policy change, expropriation, sanctions, or civil unrest.

| Indicator | Low Risk | Medium Risk | High Risk |
|-----------|----------|------------|-----------|
| Government Stability | Stable majority | Coalition / fragile | Minority / crisis |
| Rule of Law (WGI) | > 1.0 | 0 to 1.0 | < 0 |
| Upcoming Elections (12 mo) | None | Competitive | High-stakes / contentious |
| Geopolitical Alignment | Aligned with West | Neutral | Sanctioned / adversarial |
| Corruption Perception Index | > 60 | 30-60 | < 30 |

### 4. Banking Risk
Risk of systemic banking crisis, credit crunch, or deposit flight.

| Indicator | Low Risk | Medium Risk | High Risk |
|-----------|----------|------------|-----------|
| NPL Ratio | < 3% | 3-8% | > 8% |
| Capital Adequacy (CET1) | > 14% | 10-14% | < 10% |
| Credit / GDP Gap | < 0 | 0-10% | > 10% |
| Loan / Deposit Ratio | < 90% | 90-120% | > 120% |
| Foreign Funding Reliance | < 15% | 15-30% | > 30% |
| Real Estate Exposure | < 20% of loans | 20-40% | > 40% |

### 5. External Risk
Risk from external shocks: capital flow reversal, commodity price collapse, global recession.

| Indicator | Low Risk | Medium Risk | High Risk |
|-----------|----------|------------|-----------|
| Current Account (% GDP) | Surplus | -2 to -5% | < -5% |
| External Debt / GDP | < 40% | 40-80% | > 80% |
| Export Concentration (top 3) | < 40% | 40-60% | > 60% |
| Trade Partner Concentration | < 30% to any one | 30-50% | > 50% |
| Remittance Dependence | < 5% GDP | 5-15% | > 15% |
| Food/Energy Import Dependence | Net exporter | Balanced | Net importer > 20% |

## Risk Radar Output

### Overall Risk Level
| Score | Classification | Action |
|-------|---------------|--------|
| 80-100 | Critical Risk | Avoid exposure or full hedge |
| 60-80 | High Risk | Reduce, shorten duration, hedge |
| 40-60 | Medium Risk | Normal exposure with monitoring |
| 20-40 | Low Risk | Standard exposure |
| 0-20 | Minimal Risk | Core holding eligible |

## Output Template

```markdown
## Risk Radar: [Country] — [Date]

### Overall Risk Score: XX/100 — [Classification]

### Radar Map
| Risk Category | Score | Level | Trend | Trigger Event |
|--------------|-------|-------|-------|---------------|
| Sovereign | XX/100 | [Low...Critical] | ↑/↓/→ | [Specific trigger] |
| Currency | XX/100 | | | |
| Political | XX/100 | | | |
| Banking | XX/100 | | | |
| External | XX/100 | | | |

### Top 3 Risks
1. **[Risk Name]** — [Description, probability, impact, trigger level]
2. **[Risk Name]**
3. **[Risk Name]**

### Risk Outlook (6-12 months)
- Improving: [Risks that are likely to decrease]
- Stable: [Risks likely unchanged]
- Worsening: [Risks likely to increase]

### Mitigants
- [Country-specific shock absorbers: reserves, flexible FX, fiscal space, IMF program, diversified exports]
```

## Red Flags
- Risk scores change slowly, then all at once — crises are non-linear
- Banking crises are the most costly (avg 20% of GDP) — don't underweight this dimension
- Political risk is the hardest to quantify — use multiple sources
- Contagion = correlated risks across countries that otherwise look uncorrelated
- Single trigger can cascade across dimensions (e.g., FX collapse → sovereign downgrade → banking run)
