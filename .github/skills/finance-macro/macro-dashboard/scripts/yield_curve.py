#!/usr/bin/env python3
"""
Yield Curve Analyzer — Shape classification + recession probability.

Based on the NY Fed model: 10Y-3M spread is the most reliable recession predictor.
Every US recession since 1950 was preceded by a 10Y-3M inversion.

Methodology from macro-dashboard/yield-curve/SKILL.md

Usage:
    python3 yield_curve.py --dgs2 4.85 --dgs10 4.60 --dgs30 4.80 --dtb3 5.30 \\
        --fedfunds 5.25 --tips10 2.10 --breakeven5 2.35 --bbb 1.85
"""

import json


def classify_curve(dgs2, dgs10, dgs30, dtb3):
    """
    Classify yield curve shape from key rates.

    Returns: shape, description, macro signal
    """
    spread_10y2y = dgs10 - dgs2
    spread_10y3m = dgs10 - dtb3
    spread_30y10y = dgs30 - dgs10

    if spread_10y2y < -0.5 or spread_10y3m < -0.5:
        shape = "Deeply Inverted"
        signal = "Strong recession warning — market pricing aggressive rate cuts"
    elif spread_10y2y < 0 or spread_10y3m < 0:
        shape = "Inverted"
        signal = "Recession signal active — watch labor market for confirmation"
    elif spread_10y2y < 0.3:
        shape = "Flat"
        signal = "Late cycle — market expects rate cuts, transition approaching"
    elif spread_10y2y < 0.8:
        if spread_30y10y > 0.5:
            shape = "Normal (Steepening)"
            signal = "Recovery pricing — growth expectations improving"
        else:
            shape = "Normal (Moderate)"
            signal = "Mid-cycle — steady growth, no imminent recession signal"
    elif spread_30y10y > 0.3:
        shape = "Steep"
        signal = "Early cycle — strong growth expectations, possible inflation concern"
    else:
        shape = "Normal"
        signal = "Balanced — no extremes in curve shape"

    return {
        "shape": shape,
        "signal": signal,
        "spreads": {
            "10y2y": round(spread_10y2y, 2),
            "10y3m": round(spread_10y3m, 2),
            "30y10y": round(spread_30y10y, 2),
        },
    }


def recession_probability_nyfed(spread_10y3m):
    """
    NY Fed recession probability model (simplified).

    Based on the historical relationship between 10Y-3M spread and
    12-month-ahead recession probability.
    """
    if spread_10y3m > 2.0:     return 1.0
    elif spread_10y3m > 1.5:   return 3.0
    elif spread_10y3m > 1.0:   return 7.0
    elif spread_10y3m > 0.5:   return 15.0
    elif spread_10y3m > 0.2:   return 25.0
    elif spread_10y3m > 0.0:   return 35.0
    elif spread_10y3m > -0.3:  return 45.0
    elif spread_10y3m > -0.6:  return 55.0
    elif spread_10y3m > -1.0:  return 65.0
    else:                      return 75.0


def analyze_yield_curve(
    dgs2, dgs10, dgs30=5.0, dtb3=5.0, fedfunds=5.0,
    tips10=2.0, breakeven5=2.3, breakeven10=None, bbb_spread=2.0,
):
    """
    Full yield curve analysis: shape, recession probability, real rates, credit.
    """
    curve = classify_curve(dgs2, dgs10, dgs30, dtb3)
    recess_prob = recession_probability_nyfed(curve["spreads"]["10y3m"])

    # Real rate assessment
    if tips10 > 2.5:
        real_rate_signal = "Restrictive — real rates well above neutral, weighing on growth"
    elif tips10 > 1.5:
        real_rate_signal = "Moderately tight — above estimated neutral rate (r*)"
    elif tips10 > 0.5:
        real_rate_signal = "Near neutral — consistent with trend growth"
    else:
        real_rate_signal = "Accommodative — below neutral, supporting growth/assets"

    # Inflation expectations
    if breakeven5 > 3.0:
        infl_signal = "Elevated — market pricing above-target inflation persisting"
    elif breakeven5 > 2.5:
        infl_signal = "Above target — inflation concerns not fully resolved"
    elif breakeven5 > 2.0:
        infl_signal = "Anchored — consistent with 2% target"
    else:
        infl_signal = "Low — disinflation/deflation concern"

    # Credit stress
    if bbb_spread > 3.0:
        credit_signal = "Stressed — significant credit risk pricing"
    elif bbb_spread > 2.0:
        credit_signal = "Moderate — some credit concern but not alarming"
    elif bbb_spread > 1.5:
        credit_signal = "Normal — healthy credit conditions"
    else:
        credit_signal = "Very loose — minimal credit risk pricing, risk-on"

    # Composite signal
    if recess_prob > 50:
        composite = "DEFENSIVE — High recession probability, favor duration + quality"
    elif recess_prob > 30:
        composite = "CAUTIOUS — Elevated recession risk, reduce cyclical exposure"
    elif recess_prob > 15:
        composite = "NEUTRAL — Moderate recession risk, balanced positioning"
    else:
        composite = "RISK-ON — Low recession risk, growth/assets supported"

    return {
        "curve_shape": curve["shape"],
        "curve_signal": curve["signal"],
        "spreads": curve["spreads"],
        "recession_probability_12m": round(recess_prob, 1),
        "composite_signal": composite,
        "real_rate": {
            "tips_10y": tips10,
            "assessment": real_rate_signal,
        },
        "inflation_expectations": {
            "breakeven_5y": breakeven5,
            "breakeven_10y": breakeven10,
            "assessment": infl_signal,
        },
        "credit_conditions": {
            "bbb_spread": bbb_spread,
            "assessment": credit_signal,
        },
        "key_levels": {
            "fed_funds": fedfunds,
            "dgs2": dgs2,
            "dgs10": dgs10,
            "dgs30": dgs30,
            "dtb3": dtb3,
        },
        "interpretation": _generate_interpretation(curve, recess_prob, tips10, bbb_spread),
    }


def _generate_interpretation(curve, recess_prob, tips10, bbb_spread):
    """Generate a plain-English interpretation of the yield curve signals."""
    parts = []

    # Curve shape
    shape = curve["shape"]
    if "Inverted" in shape:
        parts.append(f"The yield curve is {shape.lower()}, the most reliable recession indicator. ")
        parts.append(f"The 10Y-2Y spread at {curve['spreads']['10y2y']}% suggests markets expect the Fed to cut rates. ")
    elif "Flat" in shape:
        parts.append("The yield curve is nearly flat, typical of late-cycle dynamics. ")
    else:
        parts.append(f"The yield curve is {shape.lower()}, consistent with ongoing expansion. ")

    # Recession prob
    parts.append(f"The NY Fed model implies ~{recess_prob:.0f}% recession probability over the next 12 months. ")

    # Real rates
    if tips10 > 2.0:
        parts.append(f"Real 10Y yields at {tips10}% are restrictive — this is the true cost of capital for the economy. ")
    else:
        parts.append(f"Real 10Y yields at {tips10}% are not excessively restrictive. ")

    # Credit
    if bbb_spread > 2.5:
        parts.append(f"Credit spreads at {bbb_spread}% signal elevated stress — watch for further widening. ")
    else:
        parts.append(f"Credit spreads at {bbb_spread}% are orderly, suggesting no imminent credit event. ")

    return "".join(parts)


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Yield Curve Analyzer")
    p.add_argument("--dgs2", type=float, required=True, help="2-Year Treasury Yield (%)")
    p.add_argument("--dgs10", type=float, required=True, help="10-Year Treasury Yield (%)")
    p.add_argument("--dgs30", type=float, default=5.0, help="30-Year Treasury Yield (%)")
    p.add_argument("--dtb3", type=float, default=5.0, help="3-Month T-Bill Rate (%)")
    p.add_argument("--fedfunds", type=float, default=5.0, help="Fed Funds Rate (%)")
    p.add_argument("--tips10", type=float, default=2.0, help="10-Year TIPS Real Yield (%)")
    p.add_argument("--breakeven5", type=float, default=2.3, help="5-Year Breakeven Inflation (%)")
    p.add_argument("--breakeven10", type=float, help="10-Year Breakeven Inflation (%)")
    p.add_argument("--bbb", type=float, default=2.0, help="BBB-10Y Credit Spread (%)")
    p.add_argument("--export", type=str, default="text", help="text|json")
    args = p.parse_args()

    result = analyze_yield_curve(
        args.dgs2, args.dgs10, args.dgs30, args.dtb3, args.fedfunds,
        args.tips10, args.breakeven5, args.breakeven10, args.bbb,
    )

    if args.export == "json":
        print(json.dumps(result, indent=2, default=str))
    else:
        print(f"Yield Curve: {result['curve_shape']}")
        print(f"Signal: {result['curve_signal']}")
        print(f"Recession Probability (12M): {result['recession_probability_12m']}%")
        print(f"Composite: {result['composite_signal']}")
        print()
        print("Spreads:")
        for name, val in result["spreads"].items():
            print(f"  {name}: {val:+.2f}%")
        print()
        print(f"Real Rate (10Y TIPS): {result['real_rate']['tips_10y']}% — {result['real_rate']['assessment']}")
        print(f"Inflation Breakeven (5Y): {result['inflation_expectations']['breakeven_5y']}% — {result['inflation_expectations']['assessment']}")
        print(f"Credit (BBB): {result['credit_conditions']['bbb_spread']}% — {result['credit_conditions']['assessment']}")
        print()
        print("Interpretation:")
        print(f"  {result['interpretation']}")
