---
name: country-intel
description: Country economic intelligence — macro health scoring (7 dimensions), analytical lenses, risk radar. Combines WorldBank/BIS data with lens-based qualitative analysis.
category: finance-macro
domain: country-intel
allowed-tools: Bash(python3:*) Read(*)
---

# Country Intelligence System

## Purpose

Structured country economic analysis using a lens-based framework. Combines quantitative data with analytical lenses (Small Open Economy, Commodity Exporter, Emerging Market Debt, Manufacturing Hub) that activate different interpretation frameworks for the same indicator values.

## How to Use

```bash
# Full pipeline (auto-fetches WorldBank + BIS data)
python3 scripts/orchestrator.py '{"domain":"country-intel","country":"JPN"}'
python3 scripts/orchestrator.py '{"domain":"country-intel","country":"BRA"}'

# Standalone model
python3 country-intel/scripts/macro_score.py --growth 1.8 --inflation 0.2 --cagdp -4.5 --debt 45 ...
```

## Analytical Lenses

Lenses change how the same numbers are interpreted. A -5% current account deficit means different things:
- **Small Open Economy** (NZ, SG, IE): Chronic but manageable for OECD DM
- **Emerging Market Debt** (TR, AR, PK): Funding vulnerability, rollover risk
- **Commodity Exporter** (AU, BR, CL): Depends on terms of trade direction

## Red Flags
- Scores are relative — adjust thresholds for development level
- Data lags 6-12 months for some indicators — note explicitly
- One weak dimension (e.g., external) can override all other strengths in a crisis
- GDP revisions can substantially change the picture (e.g., Nigeria 2013: +89% overnight)
- Informal economy not captured — important for EM (India: ~40% informal)
