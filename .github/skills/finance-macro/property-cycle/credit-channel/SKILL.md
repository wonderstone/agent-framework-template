---
name: credit-channel
description: Mortgage credit channel analysis — LTV ratios, debt service ratios, credit impulse, and banking sector exposure. Links property markets to financial stability through the credit transmission mechanism.
category: finance-macro
domain: property-cycle
allowed-tools: Bash(python3:*) Read(*)
---

# Credit Channel — Mortgage & Banking Link

## Purpose

Analyze the credit channel connecting property markets to the banking system and broader financial stability. Housing is the most credit-intensive asset class — mortgage lending is the largest bank asset in most countries, and housing credit cycles are the most common cause of banking crises. This skill measures credit impulse, debt service burden, LTV exposure, and systemic risk.

## When to Use

- "Mortgage credit risk assessment?"
- "Household debt sustainability?"
- "Banking sector property exposure?"
- "LTV and leverage in housing?"
- "Are we in a credit-fueled housing bubble?"
- "Mortgage stress test scenarios?"

## Key Indicators

### Household Balance Sheet
| Indicator | Source | Healthy | Stressed | Crisis |
|-----------|--------|---------|---------|--------|
| Household Debt / GDP | BIS | < 60% | 60-100% | > 100% |
| Household Debt Service Ratio | BIS / Central Bank | < 10% income | 10-15% | > 15% |
| Mortgage Debt / GDP | Central Bank | < 40% | 40-70% | > 70% |
| Household Net Worth / GDP | National accounts | > 500% | 300-500% | < 300% |

### Mortgage Credit Flow
| Indicator | Source | Normal | Overheating | Crunch |
|-----------|--------|--------|------------|--------|
| Housing Credit Growth (YoY) | Central Bank | 3-8% | > 10% | < 0% |
| Housing Credit Impulse | Calculated | ±2% GDP | > +3% GDP | < -3% GDP |
| New Mortgage Approvals (value) | Bank surveys | Stable | Surge | Collapse |
| Investor Lending Share | Central Bank | < 30% | 30-40% | > 40% (speculative) |

### Lending Standards
| Indicator | Source | Loose | Normal | Tight |
|-----------|--------|-------|--------|-------|
| High-LTV Lending (% new loans > 80% LTV) | Central Bank | > 30% | 10-30% | < 10% |
| High-DTI Lending (% > 6x income) | Central Bank | > 20% | 10-20% | < 10% |
| Interest-Only Share | Central Bank | > 30% | 10-30% | < 10% |
| Bank Lending Survey (credit standards) | Central Bank | Easing | Neutral | Tightening |

### Banking System Exposure
| Indicator | Source | Low Risk | Medium Risk | High Risk |
|-----------|--------|---------|------------|-----------|
| Mortgage Loans / Total Bank Loans | Central Bank | < 30% | 30-50% | > 50% |
| Real Estate Exposure (mortgage + developer + CRE) | Central Bank | < 40% | 40-60% | > 60% |
| Loan/Deposit Ratio | Central Bank | < 90% | 90-120% | > 120% (wholesale funding reliance) |
| Bank CET1 Ratio | Regulatory filings | > 14% | 10-14% | < 10% |

## Credit Impulse — The Leading Indicator

```
Credit_Impulse(t) = (ΔHousingCredit(t) / GDP) - (ΔHousingCredit(t-1) / GDP)

Housing Credit Impulse > 0: New credit accelerating → property prices supported
Housing Credit Impulse < 0: New credit decelerating → property price headwind
```

Credit impulse typically leads house prices by 6-12 months — it's the most important single leading indicator for the property cycle.

## Debt Service Stress Test

### Rate Shock Scenario
```
Current: Mortgage Rate X.X%, Debt Service Ratio XX%
+100bp: Debt Service Ratio rises to XX%
+200bp: Debt Service Ratio rises to XX%
+300bp: Debt Service Ratio rises to XX% → stress threshold exceeded
```

### Income Shock Scenario
```
Baseline: Employment stable, wages +X%
Stress: Unemployment +3pp, wages 0%
→ Debt service ratio increases by X.Xpp
→ Mortgage arrears projected to rise from X.X% to X.X%
```

## Banking Crisis Link

Historical pattern (Reinhart & Rogoff):
```
Property Price Peak → (0-4 quarters) → Banking Crisis Symptoms
  → NPLs rise
  → Bank funding costs increase
  → Credit crunch → property prices fall further → NPLs rise further
  → Sovereign-bank doom loop (if banks hold govt bonds or govt guarantees banks)
```

### Systemic Risk Checklist
- [ ] Real house prices > 1σ above long-term trend?
- [ ] Housing credit growth > GDP growth + 5pp for 3+ years?
- [ ] Current account deficit > 5% GDP (foreign-funded credit boom)?
- [ ] Bank real estate exposure > 50% of total loans?
- [ ] High-LTV lending > 20% of new mortgages?
- [ ] Household DSR > 15% at current rates?

**4/6+ = Systemic risk from property-credit nexus is elevated**

## Country Risk Profiles

| Country | Mortgage Debt/GDP | High-LTV Share | DSR at Current Rates | Risk |
|---------|------------------|---------------|---------------------|------|
| Australia | ~110% | ~15% (APRA limited) | ~14% | Medium-High |
| New Zealand | ~100% | ~10% (LVR rules) | ~15% | Medium-High |
| Canada | ~105% | ~20% | ~16% | High |
| Norway | ~85% | ~25% | ~14% | Medium-High |
| UK | ~70% | ~10% | ~9% | Medium |
| US | ~50% | ~5% (post-GFC) | ~6% | Low |

## Red Flags
- DSR is rate-sensitive — a 200bp rate rise can shift a country from "manageable" to "stressed"
- Credit impulse turns negative BEFORE house prices fall — use as early warning, not confirmatory
- Foreign-currency mortgages (common in EM) = double risk (rate + FX)
- Commercial real estate often crashes before residential — watch CRE as leading indicator
- Macroprudential tools (LVR/DTI limits) can suppress lending but don't eliminate underlying risks
