---
name: stress-test
description: Macroeconomic scenario stress testing for portfolios and businesses. Applies pre-built or custom macro scenarios to assess impact on sectors, assets, and business operations with probability-weighted outcomes.
category: finance-macro
domain: macro-bridge
allowed-tools: Bash(python3:*) Read(*)
---

# Stress Test — Macro Scenario Analysis

## Purpose

Apply macroeconomic scenarios to stress-test portfolios, sectors, or business plans. Combines pre-built scenarios from `scenarios/` with the transmission channel analysis from other macro-bridge sub-skills to produce probability-weighted impact assessments.

## When to Use

- "Stress test my portfolio for a recession"
- "What happens to my business if rates stay high for 2 years?"
- "Scenario analysis: Fed cuts vs Fed holds"
- "China hard landing impact on my holdings?"
- "Oil shock scenario — who survives?"

## Pre-Built Scenarios

| Scenario | Key Assumptions | Probability Guidance |
|----------|----------------|---------------------|
| Fed Soft Landing | Inflation → 2%, gradual cuts to 3%, no recession | Check market pricing |
| Fed Hard Landing | Recession forces aggressive cuts to 1-2% | Inversion duration > 12mo |
| China Reopening Boost | Fiscal stimulus, credit impulse +3%, commodity rally | PBOC policy stance |
| Commodity Supercycle | Supply underinvestment + demand growth, multi-year | Capex cycle analysis |
| Global Recession | Synchronized downturn, risk-off, flight to USD | PMI < 45 across G3 |
| Geopolitical Shock | Supply chain disruption, energy spike, safe havens | VIX > 40 |
| Stagflation | Inflation sticky > 3%, growth < 1%, Fed constrained | Core PCE + GDP combination |

## Stress Test Process

### Step 1: Define Scenario
- Use pre-built scenario or define custom
- Specify: rates, FX, commodities, GDP, inflation paths

### Step 2: Map Exposures
```
Portfolio / Business → Sector classification → Macro sensitivity profile
```

### Step 3: Apply Transmission Channels
- Rate channel → Duration/beta impact
- FX channel → Currency translation/transaction
- Commodity channel → Input cost impact
- Liquidity channel → Multiple compression/expansion

### Step 4: Aggregate Impact
```
Total_Impact = Σ (Channel_Impact × Exposure_Weight × Scenario_Probability)
```

### Step 5: Identify Tail Risks
- What breaks if the scenario is worse than expected?
- Which positions/divisions have asymmetric downside?
- Where are the correlations that could all go wrong together?

## Output Template

```markdown
## Stress Test: [Scenario Name]

### Scenario Definition
| Variable | Baseline | Scenario | Shock |
|----------|---------|----------|-------|
| Fed Funds Rate | X.XX% | X.XX% | ±XXbp |
| 10Y Yield | X.XX% | X.XX% | ±XXbp |
| USD (DXY) | XXX | XXX | ±X% |
| Oil (WTI) | $XX | $XX | ±XX% |
| GDP Growth | X.X% | X.X% | ±X.Xpp |
| CPI | X.X% | X.X% | ±X.Xpp |
| Unemployment | X.X% | X.X% | ±X.Xpp |

### Portfolio/Business Impact
| Position/Division | Exposure | Baseline Value | Scenario Value | Δ | % Impact |
|------------------|----------|---------------|----------------|---|----------|
| [Name] | [Sector] | $X | $X | ±$X | ±X% |

### Aggregate Impact
- Total Portfolio/Business Impact: ±$X (±X%)
- Best Case (95th percentile): ±$X
- Worst Case (5th percentile): ±$X

### Tail Risk Assessment
| Risk | Probability | Impact | Preparedness |
|------|-----------|--------|-------------|
| [Risk 1] | X% | $X | [High/Med/Low] |
| [Risk 2] | X% | $X | [High/Med/Low] |

### Scenario Probability
- Assigned Probability: XX%
- Key Assumptions That Must Hold:
  1. [Assumption 1]
  2. [Assumption 2]

### Recommendations
1. [Hedge / Reduce / Increase exposure to X]
2. [Prepare for Y scenario]
3. [Monitor Z trigger]
```

## Red Flags
- Scenarios are tools for thinking, not predictions — focus on the process, not the point estimate
- The most damaging scenarios are usually the ones you didn't model
- Correlation assumptions break in crises — everything can go down together
- Scenario probability assignment is subjective — be explicit about assumptions
- Stress tests reveal vulnerabilities, not certainties — use to build resilience, not to optimize
