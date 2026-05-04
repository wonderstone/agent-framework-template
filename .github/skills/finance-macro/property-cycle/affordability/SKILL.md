---
name: affordability
description: Housing affordability metrics — price-to-income, price-to-rent, mortgage burden, deposit saving time. Cross-country affordability comparison with historical context and overvaluation signals.
category: finance-macro
domain: property-cycle
allowed-tools: Bash(python3:*) Read(*)
---

# Affordability Metrics

## Purpose

Measure housing affordability using a multi-metric framework. Affordability is the key constraint on house price growth — when prices detach from incomes and rents, a correction becomes increasingly likely. This skill calculates the core affordability metrics and compares them to historical norms.

## Core Metrics

### 1. Price-to-Income Ratio
```
P/I = Median House Price / Median Household Disposable Income
```
- < 3.0x: Affordable
- 3.0-5.0x: Moderately unaffordable (typical DM range)
- 5.0-8.0x: Seriously unaffordable
- > 8.0x: Severely unaffordable (e.g., HK ~20x, Sydney ~13x, Vancouver ~12x)

### 2. Price-to-Rent Ratio
```
P/R = Median House Price / Annual Median Rent
```
- < 15x: Favor buying (low P/R)
- 15-20x: Neutral zone
- 20-25x: Favor renting
- > 25x: Strongly favor renting (bubble territory)
- Like P/E for housing — higher = more overvalued

### 3. Mortgage Burden
```
Mortgage Burden = (Monthly Mortgage Payment / Median Household Income) × 100
```
- < 25%: Affordable
- 25-35%: Moderately stressed
- 35-50%: Stressed
- > 50%: Severely stressed

### 4. Deposit Saving Time
```
Years = (20% Deposit) / (Household Savings Rate × Disposable Income)
```
- < 5 years: Attainable
- 5-10 years: Difficult
- > 10 years: Unattainable for median household

### 5. Affordability Index (NAR Method)
```
Index = (Median Family Income / Qualifying Income) × 100
Where Qualifying Income = income needed for 20% down, 30Y mortgage on median home

Index > 100: Median family can afford median home
Index < 100: Cannot afford (lower = worse)
```

## Overvaluation Detection

| Metric | Fair Value | 1σ Overvalued | 2σ Overvalued | Bubble |
|--------|-----------|---------------|---------------|--------|
| P/I vs 20Y Avg | Within 10% | +10-25% | +25-40% | > +40% |
| P/R vs 20Y Avg | Within 10% | +10-25% | +25-40% | > +40% |
| Real Price vs 20Y trend | ±5% | +5-15% | +15-25% | > +25% |

**Rule of thumb**: When 2/3 metrics are > 1σ overvalued → correction probability elevated within 2-3 years.

## Country Benchmarks (2024 estimates)

| Country | P/I Ratio | P/R Ratio | Mortgage Burden | Affordability Status |
|---------|----------|----------|----------------|---------------------|
| New Zealand | ~7-9x | ~25-30x | ~40-50% | Severely unaffordable |
| Australia | ~8-10x | ~25-30x | ~40-50% | Severely unaffordable |
| Canada | ~8-12x (Vancouver/Toronto) | ~25-30x | ~45-55% | Severely unaffordable |
| USA | ~4-5x (national) | ~15-20x | ~25-30% | Moderately unaffordable |
| UK | ~6-8x | ~20-25x | ~35-45% | Seriously unaffordable |
| China | ~20-30x (Tier 1) | ~40-60x | ~60-80% | Extremely unaffordable |

## Red Flags
- P/I > 8x historically associated with subsequent price corrections
- P/R > 25x = renting is cheaper than buying — speculative premium priced in
- Mortgage burden > 40% at average rates means rate hikes will cause stress
- Affordability can remain "unaffordable" for years — it's a valuation metric, not a timing tool
- Affordability can improve via falling rates OR falling prices — different macro implications
