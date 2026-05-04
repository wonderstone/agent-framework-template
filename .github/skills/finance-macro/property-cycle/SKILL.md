---
name: property-cycle
description: Real estate cycle analysis — phase detection (7-indicator model), affordability metrics, credit channel, cross-country comparison. Covers NZ, AU, US, UK, CN with country profiles.
category: finance-macro
domain: property-cycle
allowed-tools: Bash(python3:*) Read(*)
---

# Property Cycle Analyzer

## Purpose

Systematic real estate cycle analysis. Housing represents 50-70% of household wealth in most economies, construction is a major GDP driver, and mortgage credit is the largest bank asset. This domain detects cycle phases, measures affordability, and analyzes the credit transmission channel.

## How to Use

```bash
# Pipeline (auto-fetches BIS property prices + credit data)
python3 scripts/orchestrator.py '{"domain":"property-cycle","country":"AUS"}'
python3 scripts/orchestrator.py '{"domain":"property-cycle","country":"NZL","params":{"rate":"5.99","price":"820000","income":"98000","rent":"2650"}}'

# Standalone models
python3 property-cycle/scripts/cycle_score.py --price-yoy 1.5 --price-income-vs-lt 1.22 ...
python3 property-cycle/scripts/affordability_calc.py --price 820000 --income 98000 --rent 2650 --rate 5.99
```

## The Cycle Framework

The 7-indicator model scores each market on a -2 (bust) to +2 (boom) scale, weighted:
- Real house price momentum (25%), P/I vs long-term avg (20%), credit growth (15%), building approvals (15%), inventory (10%), auction clearance (10%), investor activity (5%)

The 18-year cycle model (Harrison) is an empirical observation, not a law — use as framework, not prediction. Policy intervention (macroprudential, tax) can accelerate or delay phase transitions.

## Key Structural Insight

Mortgage rate structure is the most important cross-country differentiator:
- **NZ/AU**: 1-2Y fixed + variable → fastest monetary policy transmission through housing
- **US**: 30Y fixed → existing homeowners insulated from rate changes
- **Canada**: 5Y fixed with renewal → rolling reset wall every 5 years

## Red Flags
- National averages mask city-level divergence — Auckland/Sydney distort national metrics
- Housing data is notoriously lagged (2-6 months) — use transaction data for real-time
- Government intervention can delay but rarely prevent cycle turns
- Banking crises and property cycles are tightly linked — monitor mortgage credit quality
- Affordability can remain "unaffordable" for years — it's a valuation metric, not a timing tool
