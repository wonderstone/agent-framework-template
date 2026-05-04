# Taylor Rule Reference

## Original Taylor Rule (1993)

```
i = r* + π + 0.5(π - π*) + 0.5(y - y*)

Where:
  i   = Nominal federal funds rate
  r*  = Equilibrium real interest rate (Taylor used 2%)
  π   = Current inflation rate (4-quarter PCE or GDP deflator)
  π*  = Target inflation rate (2%)
  y   = Log of real GDP
  y*  = Log of potential GDP
  (y - y*) = Output gap (%)
```

## Common Variants

### Balanced-Approach Rule (Yellen's preferred)
```
i = r* + π + 0.5(π - π*) + 1.0(y - y*)
```
Higher weight on output gap — more dovish during recessions.

### Inertial Rule (Gradualism / "Policy Smoothing")
```
i_t = ρ × i_(t-1) + (1-ρ) × [r* + π + 0.5(π - π*) + 0.5(y - y*)]
Where ρ typically 0.6-0.8 (high inertia — rates move slowly)
```

### First-Difference Rule
```
Δi = 0.5(π - π*) + 1.0(Δy)
```
Focuses on change in output, not output gap — avoids estimating potential GDP.

### Core PCE Version (Fed's preferred inflation metric)
```
i = r* + PCE_core + 0.5(PCE_core - 2%) + 0.5(y - y*)
```

## Parameter Sensitivities

| Parameter | Lower Value Implies | Higher Value Implies |
|-----------|-------------------|---------------------|
| r* (neutral rate) | Lower terminal rate, more dovish | Higher terminal rate, more hawkish |
| π weight | Less responsive to inflation deviations | More aggressive on inflation |
| y weight | Less responsive to growth | More aggressive on growth/employment |

## Interpretation

### Taylor Rule Residual
```
Residual = Actual Fed Funds Rate - Taylor Rule Prescription

Positive Residual: Policy is TIGHTER than Taylor Rule → Hawkish
Negative Residual: Policy is LOOSER than Taylor Rule → Dovish
```

### Historical Taylor Rule Residuals

| Period | Residual | Fed Label | Outcome |
|--------|---------|-----------|---------|
| 2003-2005 | -200bp (too loose) | "Measured pace" | Housing bubble |
| 2009-2015 | -300bp (too loose, ZLB) | ZIRP + QE | Slow recovery |
| 2018-2019 | +50bp (about right) | "Data dependent" | Soft landing (then COVID) |
| 2022-2023 | +100bp (tight) | "Higher for longer" | Inflation declining |

## Application to Other Central Banks

### ECB
```
ECB Taylor: i = r* + HICP_core + 0.5(HICP_core - 2%) + 1.0(y - y*)
```
ECB has traditionally been more growth-sensitive (higher y weight) due to Eurozone heterogeneity.

### RBNZ
```
RBNZ Taylor: OCR = r* + CPI_excl_food_energy + 0.5(CPI - 2%) + 0.5(y - y*)
```
RBNZ was the first to adopt inflation targeting (1990) and tends to follow the Taylor Rule more mechanically than peers.

### BOJ
Taylor Rule has limited applicability to BOJ — structural deflation, YCC framework, and large balance sheet make the rule less relevant until normalization is more advanced.

## Key Limitations

1. **r* is unobservable** — estimates range from 0.5% (secular stagnation) to 3% (pre-GFC)
2. **Output gap is estimated with large error** — real-time estimates are often revised by 2-3pp
3. **Doesn't capture financial stability concerns** — the rule ignores asset bubbles, credit cycles
4. **Single-equation** — doesn't capture the Fed's reaction to international developments
5. **No ZLB handling** — the rule prescribes negative rates during deep recessions

## Practical Usage

When analyzing whether a central bank is hawkish or dovish, the Taylor Rule provides a quantitative benchmark:

1. Calculate the rule-implied rate using latest inflation and output gap data
2. Compare to actual policy rate → calculate the Taylor Rule residual
3. A positive residual (> +50bp) strengthens the case for a hawkish classification
4. A negative residual (< -50bp) strengthens the case for a dovish classification
5. Track the residual over time — declining residual = central bank becoming relatively less hawkish
