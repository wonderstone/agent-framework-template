#!/usr/bin/env python3
"""
Macro Health Score Calculator.

Scores a country's macroeconomic health across 7 dimensions (0-100).
Growth, Inflation, External, Fiscal, Financial, Labor, Structural.

Usage:
    python3 macro_score.py --growth 2.5 --inflation 2.1 --cagdp -3.0 --debt 80 --fiscal -2.5 --unemployment 4.0 --creditgap 5
    python3 macro_score.py --country NZ  # (when integrated with data fetchers)
"""

import json
import sys


def score_dimension(value, thresholds, higher_is_better=True):
    """
    Score a single indicator 0-100 based on thresholds.
    thresholds: list of (value, score) tuples, sorted ascending
    """
    for v, s in thresholds:
        if higher_is_better and value <= v:
            return s
        elif not higher_is_better and value >= v:
            return s
    return thresholds[-1][1]  # last threshold score if beyond range


def macro_health(
    growth_3y, inflation_deviation, current_account_gdp, govt_debt_gdp,
    fiscal_balance_gdp, unemployment_rate, credit_gap, npl_ratio=3.0,
    lfpr=None, governance_score=None
):
    """
    Calculate composite macro health score (0-100).

    Args:
        growth_3y: Real GDP growth, 3-year average (%)
        inflation_deviation: Abs deviation of CPI from target (%)
        current_account_gdp: Current account balance (% GDP)
        govt_debt_gdp: Government debt (% GDP)
        fiscal_balance_gdp: Fiscal balance (% GDP, negative = deficit)
        unemployment_rate: Unemployment rate (%)
        credit_gap: BIS credit-to-GDP gap (%)
        npl_ratio: Bank NPL ratio (%)
        lfpr: Labor force participation rate (%)
        governance_score: WGI governance score (-2.5 to 2.5)
    """

    # 1. Growth (weight 20%)
    if growth_3y > 5:      growth_score = 100
    elif growth_3y > 3:    growth_score = 80
    elif growth_3y > 2:    growth_score = 60
    elif growth_3y > 1:    growth_score = 40
    elif growth_3y > 0:    growth_score = 25
    else:                  growth_score = 10

    # 2. Inflation (weight 15%) — deviation from target
    if inflation_deviation < 0.3:    infl_score = 100
    elif inflation_deviation < 0.5:  infl_score = 90
    elif inflation_deviation < 1.0:  infl_score = 75
    elif inflation_deviation < 2.0:  infl_score = 55
    elif inflation_deviation < 3.0:  infl_score = 35
    elif inflation_deviation < 5.0:  infl_score = 20
    else:                            infl_score = 5

    # 3. External (weight 15%)
    if current_account_gdp > 5:          ca_score = 95
    elif current_account_gdp > 2:        ca_score = 85
    elif current_account_gdp > -2:       ca_score = 70
    elif current_account_gdp > -5:       ca_score = 45
    elif current_account_gdp > -8:       ca_score = 20
    else:                                ca_score = 5

    # 4. Fiscal (weight 15%) — combines debt and balance
    debt_score = 100 if govt_debt_gdp < 30 else (85 if govt_debt_gdp < 60 else (60 if govt_debt_gdp < 90 else (35 if govt_debt_gdp < 120 else 15)))
    fiscal_score = 100 if fiscal_balance_gdp > 1 else (80 if fiscal_balance_gdp > -1 else (60 if fiscal_balance_gdp > -3 else (35 if fiscal_balance_gdp > -6 else 15)))
    combined_fiscal = debt_score * 0.5 + fiscal_score * 0.5

    # 5. Financial Stability (weight 15%)
    credit_score = 100 if credit_gap < 0 else (75 if credit_gap < 5 else (50 if credit_gap < 10 else (25 if credit_gap < 20 else 5)))
    npl_score = 100 if npl_ratio < 2 else (80 if npl_ratio < 4 else (50 if npl_ratio < 8 else (25 if npl_ratio < 12 else 5)))
    combined_financial = credit_score * 0.6 + npl_score * 0.4

    # 6. Labor (weight 10%)
    if unemployment_rate < 3:       labor_score = 95
    elif unemployment_rate < 4:     labor_score = 85
    elif unemployment_rate < 5.5:   labor_score = 70
    elif unemployment_rate < 8:    labor_score = 45
    elif unemployment_rate < 12:   labor_score = 20
    else:                          labor_score = 5

    # 7. Structural (weight 10%) — governance proxy
    if governance_score is not None:
        struct_score = 50 + (governance_score * 25)  # map -2.5..2.5 to 0..100
        struct_score = max(5, min(100, struct_score))
    else:
        struct_score = 55  # neutral default

    weights = [0.20, 0.15, 0.15, 0.15, 0.15, 0.10, 0.10]
    scores = [growth_score, infl_score, ca_score, combined_fiscal, combined_financial, labor_score, struct_score]

    composite = sum(w * s for w, s in zip(weights, scores))

    if composite > 80:  classification = "Excellent"
    elif composite > 65: classification = "Good"
    elif composite > 50: classification = "Fair"
    elif composite > 35: classification = "Weak"
    elif composite > 20: classification = "Poor"
    else:                classification = "Critical"

    return {
        "composite_score": round(composite, 1),
        "classification": classification,
        "dimensions": {
            "growth":     {"score": growth_score, "weight": 0.20, "weighted": round(growth_score * 0.20, 1)},
            "inflation":  {"score": infl_score, "weight": 0.15, "weighted": round(infl_score * 0.15, 1)},
            "external":   {"score": ca_score, "weight": 0.15, "weighted": round(ca_score * 0.15, 1)},
            "fiscal":     {"score": round(combined_fiscal, 1), "weight": 0.15, "weighted": round(combined_fiscal * 0.15, 1)},
            "financial":  {"score": round(combined_financial, 1), "weight": 0.15, "weighted": round(combined_financial * 0.15, 1)},
            "labor":      {"score": labor_score, "weight": 0.10, "weighted": round(labor_score * 0.10, 1)},
            "structural": {"score": round(struct_score, 1), "weight": 0.10, "weighted": round(struct_score * 0.10, 1)},
        },
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Macro Health Score Calculator")
    parser.add_argument("--growth", type=float, default=2.0, help="Real GDP growth 3Y avg (%)")
    parser.add_argument("--inflation", type=float, default=2.0, help="CPI deviation from target (pp)")
    parser.add_argument("--cagdp", type=float, default=-2.0, help="Current account (% GDP)")
    parser.add_argument("--debt", type=float, default=80, help="Govt debt (% GDP)")
    parser.add_argument("--fiscal", type=float, default=-2.0, help="Fiscal balance (% GDP)")
    parser.add_argument("--unemployment", type=float, default=5.0, help="Unemployment rate (%)")
    parser.add_argument("--creditgap", type=float, default=5.0, help="BIS credit-to-GDP gap (%)")
    parser.add_argument("--npl", type=float, default=3.0, help="Bank NPL ratio (%)")
    parser.add_argument("--governance", type=float, help="WGI governance score (-2.5 to 2.5)")
    parser.add_argument("--export", type=str, default="text", help="text|json")
    args = parser.parse_args()

    result = macro_health(
        args.growth, args.inflation, args.cagdp, args.debt, args.fiscal,
        args.unemployment, args.creditgap, args.npl, governance_score=args.governance
    )

    if args.export == "json":
        print(json.dumps(result, indent=2, default=str))
    else:
        print(f"Macro Health Score: {result['composite_score']:.0f}/100 — {result['classification']}")
        print()
        print(f"{'Dimension':<15} {'Score':<8} {'Weight':<8} {'Weighted':<8}")
        print("-" * 42)
        for name, data in result["dimensions"].items():
            bar = "█" * int(data["score"] / 10)
            print(f"{name:<15} {data['score']:<8.0f} {data['weight']:<8.2f} {data['weighted']:<8.1f} {bar}")
