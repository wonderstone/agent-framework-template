#!/usr/bin/env python3
"""
Debt Dynamics Calculator.

Projects debt/GDP path under baseline, optimistic, and stress scenarios.
Calculates debt-stabilizing primary balance and fiscal gap.

Usage:
    python3 debt_dynamics.py --debt 100 --rate 3.5 --growth 2.0 --primary -1.0 --years 5
    python3 debt_dynamics.py --country NZ --years 5
"""

import json
import sys


def project_debt(debt_gdp, nominal_rate, nominal_growth, primary_balance_pct, years=5, sfa=0):
    """
    Project debt/GDP forward using debt dynamics equation.

    dt = dt-1 × (1 + r) / (1 + g) - pb + sfa
    """
    path = [debt_gdp]
    for _ in range(years):
        next_debt = path[-1] * (1 + nominal_rate/100) / (1 + nominal_growth/100) - primary_balance_pct + sfa
        path.append(round(next_debt, 2))
    return path


def stabilizing_balance(debt_gdp, nominal_rate, nominal_growth):
    """Calculate primary balance (% GDP) needed to stabilize debt/GDP."""
    # pb* = (r - g) × d / (1 + g) ≈ (r - g) × d
    return round((nominal_rate - nominal_growth) / 100 * debt_gdp, 2)


def fiscal_gap(debt_gdp, nominal_rate, nominal_growth, actual_primary):
    """Fiscal gap = stabilizing balance - actual balance."""
    stab = stabilizing_balance(debt_gdp, nominal_rate, nominal_growth)
    return round(stab - actual_primary, 2)


def scenario_projections(debt_gdp, rate, growth, primary, years=5):
    """Project debt under multiple scenarios."""
    scenarios = {
        "baseline": project_debt(debt_gdp, rate, growth, primary, years),
        "optimistic": project_debt(debt_gdp, rate - 0.5, growth + 1.0, primary + 0.5, years),
        "rate_shock": project_debt(debt_gdp, rate + 2.0, growth - 1.0, primary - 0.5, years),
        "growth_shock": project_debt(debt_gdp, rate + 1.0, growth, primary - 2.0, years),
        "combined_shock": project_debt(debt_gdp, rate + 2.0, growth - 1.5, primary - 2.5, years),
    }

    return {
        "input": {
            "debt_gdp": debt_gdp,
            "nominal_rate": rate,
            "nominal_growth": growth,
            "primary_balance": primary,
            "r_minus_g": round(rate - growth, 2),
        },
        "stabilizing_primary": stabilizing_balance(debt_gdp, rate, growth),
        "fiscal_gap": fiscal_gap(debt_gdp, rate, growth, primary),
        "projections": scenarios,
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Debt dynamics calculator")
    parser.add_argument("--debt", type=float, default=100, help="Debt/GDP ratio (%)")
    parser.add_argument("--rate", type=float, default=3.5, help="Effective nominal interest rate (%)")
    parser.add_argument("--growth", type=float, default=2.0, help="Nominal GDP growth (%)")
    parser.add_argument("--primary", type=float, default=-1.0, help="Primary balance (% GDP, negative = deficit)")
    parser.add_argument("--years", type=int, default=5, help="Projection horizon")
    parser.add_argument("--export", type=str, default="text", help="text|json")
    args = parser.parse_args()

    result = scenario_projections(args.debt, args.rate, args.growth, args.primary, args.years)

    if args.export == "json":
        print(json.dumps(result, indent=2, default=str))
    else:
        inp = result["input"]
        print(f"Debt Dynamics Analysis")
        print(f"{'─' * 55}")
        print(f"Debt/GDP: {inp['debt_gdp']}% | r: {inp['nominal_rate']}% | g: {inp['nominal_growth']}%")
        print(f"r - g: {inp['r_minus_g']:+.1f}% {'(UNFAVORABLE — debt dynamics working against you)' if inp['r_minus_g'] > 0 else '(FAVORABLE — debt dynamics working for you)'}")
        print()
        print(f"Debt-Stabilizing Primary Balance: {result['stabilizing_primary']:+.1f}% of GDP")
        print(f"Actual Primary Balance: {inp['primary_balance']:+.1f}% of GDP")
        print(f"Fiscal Gap: {result['fiscal_gap']:+.1f}% of GDP {'(ADJUSTMENT NEEDED)' if result['fiscal_gap'] > 0 else '(FISCAL SPACE AVAILABLE)'}")
        print()
        print(f"{'Scenario':<20} {'Y1':<8} {'Y3':<8} {'Y5':<8} {'Direction':<12}")
        print("-" * 56)
        for name, path in result["projections"].items():
            direction = "↑" if path[-1] > path[0] else ("↓" if path[-1] < path[0] else "→")
            print(f"{name:<20} {path[1]:<8.1f} {path[min(3,len(path)-1)]:<8.1f} {path[-1]:<8.1f} {direction:<12}")
