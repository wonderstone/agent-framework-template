---
name: labor-market
description: Comprehensive labor market analysis covering unemployment rate, nonfarm payrolls, JOLTS openings, initial claims, wage growth, participation rate, and underemployment. Detects labor market turning points and slack.
category: finance-macro
domain: macro-dashboard
allowed-tools: Bash(python3:*) Read(*)
---

# Labor Market Analyzer

## Purpose

Comprehensive US labor market analysis. The labor market is the Fed's dual mandate pillar alongside price stability. This skill tracks employment quantity (jobs, unemployment), quality (wages, underemployment), and dynamics (flows, churn) to assess whether the labor market is tight, balanced, or slack.

## When to Use

- "How strong is the labor market?"
- "Is unemployment rising?"
- "What's the latest jobs report?"
- "Are wages growing faster than inflation?"
- "Is there labor market slack?"
- "What do JOLTS data show?"

## Indicator Framework

### Quantity Indicators

| Indicator | FRED Code | Frequency | Strong | Weak |
|-----------|-----------|-----------|--------|------|
| Unemployment Rate (U-3) | UNRATE | Monthly | < 4% | > 5.5% |
| Underemployment Rate (U-6) | U6RATE | Monthly | < 8% | > 10% |
| Nonfarm Payrolls (monthly change) | PAYEMS | Monthly | > 200K | < 50K |
| Labor Force Participation | CIVPART | Monthly | Rising | Falling |
| Employment-Population Ratio | EMRATIO | Monthly | > 60% | < 58% |

### Demand Indicators

| Indicator | FRED Code | Frequency | Strong | Weak |
|-----------|-----------|-----------|--------|------|
| JOLTS Job Openings | JTSJOL | Monthly | > 9M | < 6M |
| Initial Jobless Claims (4-wk) | ICSA | Weekly | < 220K | > 280K |
| Continuing Claims | CCSA | Weekly | < 1.5M | > 2M |
| NFIB Hiring Plans | — | Monthly | > 20% | < 10% |
| Temp Help Employment | TEMPHELPS | Monthly | Rising | Falling |

### Quality / Cost Indicators

| Indicator | FRED Code | Frequency | Sustainable | Overheating |
|-----------|-----------|-----------|-------------|-------------|
| Avg Hourly Earnings (YoY) | CES0500000003 | Monthly | 3-3.5% | > 4.5% |
| Employment Cost Index | ECIWAG | Quarterly | < 3.5% | > 4.5% |
| Quits Rate | JTSQUR | Monthly | ~2.5% | > 3% |
| Layoffs Rate | JTSLDR | Monthly | < 1.2% | > 1.5% |
| Median Duration Unemployment | UEMPMED | Monthly | < 10 wks | > 15 wks |

## Sahm Rule — Recession Indicator

The Sahm Rule identifies recessions in real time:
```
Sahm_Recession_Indicator = UNRATE_3mo_avg - min(UNRATE_3mo_avg[previous 12 months])
If > 0.50 percentage points → recession likely underway
```

- Never triggered outside a recession since 1950
- Zero false positives
- Typically triggers 2-3 months after recession starts (real-time, not leading)

## Labor Market Tightness Index

Composite 0-10 score:

- **0-3: Slack** — High unemployment, low openings, falling wages
- **4-6: Balanced** — Near NAIRU, normal churn
- **7-10: Extremely Tight** — Low unemployment, high openings, fast wage growth

## Output Template

```markdown
## Labor Market Dashboard — [Month YYYY]

### Headline
| Metric | Latest | Prior | 3-Mo Avg | Trend |
|--------|--------|-------|----------|-------|
| Nonfarm Payrolls | +XXXK | +XXXK | +XXXK | |
| Unemployment Rate | X.X% | X.X% | — | |
| U-6 Underemployment | X.X% | X.X% | — | |
| Participation Rate | XX.X% | XX.X% | — | |
| Avg Hourly Earnings (YoY) | X.X% | X.X% | — | |

### Demand Signals
| Metric | Latest | Prior |
|--------|--------|-------|
| JOLTS Openings | X.XM | X.XM |
| Openings per Unemployed | X.X | X.X |
| Initial Claims (4wk) | XXXK | XXXK |

### Dynamics
| Metric | Latest | Prior |
|--------|--------|-------|
| Quits Rate | X.X% | X.X% |
| Layoffs Rate | X.X% | X.X% |

### Key Ratios
| Ratio | Value | Interpretation |
|-------|-------|---------------|
| Job Openings / Unemployed | X.X | [Tight/Balanced/Slack] |
| Quits / Layoffs | X.X | [Worker confidence] |
| Wage Growth - Core PCE | +X.X% | [Real wage gain/loss] |

### Assessment
- Labor Market: [Tight / Balanced / Slack]
- Sahm Rule: [Not Triggered / Triggered — X.XXpp]
- Wage-Price Spiral Risk: [Low / Moderate / High]
- Fed Implication: [Can be patient / Needs to watch / Must act]
```

## Red Flags
- NFP initial print is often revised significantly — wait for revisions
- Unemployment can fall for the wrong reason (participation declining)
- JOLTS data has low response rates (~32%) — large confidence intervals
- Wage growth is a lagging indicator — jobs slowdown before wages
- Initial claims below 200K is historically exceptional — don't normalize it
- Temp help employment leads total employment by 3-6 months
