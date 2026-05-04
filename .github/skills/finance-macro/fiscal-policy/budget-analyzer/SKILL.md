---
name: budget-analyzer
description: Government budget structure analysis — revenue composition, expenditure categories, mandatory vs discretionary spending, and fiscal impulse measurement. Connects budget structure to macro outcomes.
category: finance-macro
domain: fiscal-policy
allowed-tools: Bash(python3:*) Read(*)
---

# Budget Analyzer

## Purpose

Analyze government budget structure and its macroeconomic implications. Goes beyond headline deficit/surplus to understand revenue sources, expenditure rigidities, automatic stabilizers, and discretionary fiscal space. The structure of a budget often matters more than its balance — a country with 50% debt/GDP and rigid expenditures may be more vulnerable than one with 100% debt/GDP and flexible spending.

## When to Use

- "Analyze [Country]'s budget"
- "Government revenue structure?"
- "Fiscal space assessment"
- "Budget rigidity analysis"
- "Mandatory vs discretionary spending?"
- "Fiscal impulse calculation"

## Budget Structure Analysis

### Revenue Composition
| Category | Typical DM Share | Typical EM Share | Cyclical Sensitivity | Growth Trend |
|----------|-----------------|-----------------|---------------------|-------------|
| Personal Income Tax | 20-30% | 5-15% | High (progressive, cyclical) | Stable |
| Corporate Income Tax | 5-15% | 10-20% | Very High (profit cycle) | Stable to declining |
| VAT / GST / Sales Tax | 15-25% | 15-30% | Medium (consumption) | Stable |
| Social Security Contributions | 15-25% | 5-15% | Medium (employment) | Stable to rising |
| Property Tax | 1-5% | 1-3% | Low (slow assessment) | Rising |
| Commodity Royalties | 0-2% (DM) | 10-30% (commodity EM) | Very High (price-dependent) | Volatile |
| Excise / Sin Taxes | 2-5% | 3-8% | Low (inelastic demand) | Stable |

**Key Insight**: Revenue concentration matters — commodity exporters with 50%+ of revenue from royalties face extreme fiscal volatility.

### Expenditure Composition
| Category | Typical % of Total | Rigidity | Automatic Stabilizer? |
|----------|-------------------|----------|---------------------|
| Social Security / Pensions | 20-30% | Very High (entitlement) | No |
| Healthcare | 15-25% | High (demographic) | No |
| Education | 10-15% | Medium-High | No |
| Defense | 2-5% (DM) / 5-15% (some EM) | Medium | No |
| Interest Payments | 3-10% | Very High (contractual) | No |
| Public Investment (Infrastructure) | 3-8% | Low (discretionary) | Can be |
| Welfare / Unemployment | 5-15% | Medium | Yes |
| Public Sector Wages | 10-20% | Medium-High | No |

### Budget Rigidity Index
```
Rigidity = Mandatory Spending / Total Spending

Mandatory = Entitlements + Interest + Contractual Obligations

> 80% Mandatory → Very rigid — little fiscal flexibility
60-80% → Moderately rigid — some discretionary space
< 60% → Flexible — significant policy discretion
```

## Fiscal Impulse Calculation

The fiscal impulse measures whether fiscal policy is adding to or subtracting from aggregate demand:

```
Step 1: Calculate Cyclically-Adjusted Primary Balance (CAPB):
  CAPB = Actual Primary Balance - (ε × Output Gap)
  Where ε = automatic stabilizer coefficient (typically 0.3-0.5)

Step 2: Calculate Fiscal Impulse:
  Fiscal Impulse = -(Δ CAPB) / Potential GDP

Step 3: Classify:
  > +1.0% of potential GDP → Strong expansion
  +0.5% to +1.0% → Moderate expansion
  -0.5% to +0.5% → Neutral
  -1.0% to -0.5% → Moderate contraction
  < -1.0% → Strong contraction
```

## Fiscal Space Assessment

| Indicator | Ample Space | Limited Space | No Space |
|-----------|-----------|--------------|----------|
| Govt Debt / GDP | < 60% | 60-100% | > 100% |
| Interest / Revenue | < 5% | 5-15% | > 15% |
| Avg Maturity | > 10 years | 5-10 years | < 5 years |
| Foreign Currency Debt Share | < 10% | 10-30% | > 30% |
| Credible Fiscal Framework | Yes (rule, institution) | Partial | No |
| Market Access (spread) | < 100bp over Bund/UST | 100-400bp | > 400bp |

**5/6 "Ample" → Strong fiscal position, can respond to shocks**
**3-4/6 → Moderate constraints — targeted stimulus possible**
**< 3/6 → Severe constraints — pro-cyclical tightening during downturns likely**

## Output Template

```markdown
## Budget Analysis: [Country] — FY20XX

### Revenue Structure
| Source | Amount (bn) | % Total | Trend |
|--------|-----------|---------|-------|
| Income Tax | $XX | XX% | ↑/↓ |
| Corporate Tax | $XX | XX% | ↑/↓ |
| VAT/GST | $XX | XX% | ↑/↓ |
| Other | $XX | XX% | |

### Expenditure Structure
| Category | Amount (bn) | % Total | Mandatory? |
|----------|-----------|---------|------------|
| Social Protection | $XX | XX% | Yes |
| Health | $XX | XX% | Yes |
| Education | $XX | XX% | Mostly |
| Interest | $XX | XX% | Yes (contractual) |
| Investment | $XX | XX% | Discretionary |
| Other | $XX | XX% | Mixed |

### Budget Metrics
- Revenue / GDP: XX%
- Expenditure / GDP: XX%
- Fiscal Balance: -X.X% GDP
- Primary Balance: -X.X% GDP
- Cyclically-Adjusted Primary Balance: -X.X% potential GDP
- Fiscal Impulse: ±X.X% → [Expansionary / Neutral / Contractionary]
- Budget Rigidity: XX% mandatory

### Fiscal Space
- Debt / GDP: XX%
- Interest / Revenue: XX%
- Avg Maturity: X.X years
- FX Debt Share: XX%
- Assessment: [Ample / Limited / No space]
```

## Red Flags
- Off-budget spending (SOEs, PPPs, guarantees) can be 10-30% of GDP additional contingent liability
- Fiscal impulse estimates are sensitive to output gap estimates — large uncertainty
- Tax revenue is highly pro-cyclical — fiscal position deteriorates quickly in downturns
- Interest rate shocks flow through to budgets faster in countries with short-duration debt
- Creative accounting (below-the-line items, timing shifts) is common — especially in EM
