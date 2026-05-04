#!/usr/bin/env python3
"""
Housing Affordability Calculator.

Calculates core affordability metrics:
  - Price-to-Income ratio
  - Price-to-Rent ratio
  - Mortgage burden (% of income)
  - Years to save deposit
  - Qualifying income vs actual income

Usage:
    python3 affordability_calc.py --price 800000 --income 95000 --rent 2800 --rate 6.5 --term 25
"""

import json
import sys


def monthly_payment(principal, annual_rate_pct, term_years=25):
    """Calculate monthly mortgage payment (principal + interest)."""
    monthly_rate = annual_rate_pct / 100 / 12
    n_payments = term_years * 12
    if monthly_rate == 0:
        return principal / n_payments
    return principal * (monthly_rate * (1 + monthly_rate) ** n_payments) / ((1 + monthly_rate) ** n_payments - 1)


def calculate_affordability(median_price, median_household_income, median_monthly_rent,
                            mortgage_rate_pct, term_years=25, deposit_pct=20,
                            savings_rate_pct=10, annual_rates=2000, annual_maintenance_pct=1.0):
    """
    Calculate housing affordability metrics.

    Args:
        median_price: Median house price
        median_household_income: Median household disposable income (annual)
        median_monthly_rent: Median monthly rent
        mortgage_rate_pct: Mortgage interest rate (%)
        term_years: Mortgage term in years
        deposit_pct: Deposit requirement (%)
        savings_rate_pct: Household savings rate (%)
        annual_rates: Annual council rates / property tax
        annual_maintenance_pct: Annual maintenance as % of property value
    """

    deposit = median_price * deposit_pct / 100
    loan_amount = median_price - deposit
    monthly_mortgage = monthly_payment(loan_amount, mortgage_rate_pct, term_years)

    # Monthly costs
    monthly_rates = annual_rates / 12
    monthly_maintenance = (median_price * annual_maintenance_pct / 100) / 12
    total_monthly_cost = monthly_mortgage + monthly_rates + monthly_maintenance
    monthly_income = median_household_income / 12

    # Price-to-Income
    price_to_income = median_price / median_household_income

    # Price-to-Rent
    annual_rent = median_monthly_rent * 12
    price_to_rent = median_price / annual_rent if annual_rent > 0 else float('inf')

    # Mortgage burden
    mortgage_burden_pct = (total_monthly_cost / monthly_income) * 100

    # Years to save deposit
    annual_savings = median_household_income * savings_rate_pct / 100
    years_to_deposit = deposit / annual_savings if annual_savings > 0 else float('inf')

    # Qualifying income (banks typically stress at rate + 2-3%)
    stress_rate = mortgage_rate_pct + 2.5
    stress_payment = monthly_payment(loan_amount, stress_rate, term_years)
    stress_total = stress_payment + monthly_rates + monthly_maintenance
    qualifying_income_required = stress_total * 12 / 0.35  # 35% DTI limit typical
    affordability_index = (median_household_income / qualifying_income_required) * 100

    # Classifications
    if price_to_income < 3: pi_status = "Affordable"
    elif price_to_income < 5: pi_status = "Moderately Unaffordable"
    elif price_to_income < 8: pi_status = "Seriously Unaffordable"
    else: pi_status = "Severely Unaffordable"

    if mortgage_burden_pct < 25: mb_status = "Affordable"
    elif mortgage_burden_pct < 35: mb_status = "Moderately Stressed"
    elif mortgage_burden_pct < 50: mb_status = "Stressed"
    else: mb_status = "Severely Stressed"

    if affordability_index > 120: ai_status = "Easily Affordable"
    elif affordability_index > 100: ai_status = "Affordable"
    elif affordability_index > 80: ai_status = "Difficult"
    else: ai_status = "Unaffordable for Median Household"

    return {
        "inputs": {
            "median_price": median_price,
            "median_income": median_household_income,
            "median_rent_monthly": median_monthly_rent,
            "mortgage_rate": mortgage_rate_pct,
            "term_years": term_years,
            "deposit_pct": deposit_pct,
        },
        "metrics": {
            "price_to_income": {"value": round(price_to_income, 1), "status": pi_status},
            "price_to_rent": {"value": round(price_to_rent, 1), "note": ">25x = renting cheaper than buying"},
            "mortgage_burden_pct": {"value": round(mortgage_burden_pct, 1), "status": mb_status},
            "years_to_save_deposit": {"value": round(years_to_deposit, 1)},
            "affordability_index": {"value": round(affordability_index, 0), "status": ai_status},
        },
        "breakdown": {
            "deposit_needed": round(deposit),
            "loan_amount": round(loan_amount),
            "monthly_mortgage": round(monthly_mortgage),
            "monthly_rates_maintenance": round(monthly_rates + monthly_maintenance),
            "total_monthly_cost": round(total_monthly_cost),
            "monthly_income": round(monthly_income),
            "qualifying_income_required": round(qualifying_income_required),
        },
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Housing Affordability Calculator")
    parser.add_argument("--price", type=float, required=True, help="Median house price")
    parser.add_argument("--income", type=float, required=True, help="Median household disposable income (annual)")
    parser.add_argument("--rent", type=float, required=True, help="Median monthly rent")
    parser.add_argument("--rate", type=float, default=6.5, help="Mortgage rate (%)")
    parser.add_argument("--term", type=int, default=25, help="Mortgage term (years)")
    parser.add_argument("--deposit", type=float, default=20, help="Deposit requirement (%)")
    parser.add_argument("--savings", type=float, default=10, help="Household savings rate (%)")
    parser.add_argument("--rates", type=float, default=2000, help="Annual property taxes/rates")
    parser.add_argument("--maintenance", type=float, default=1.0, help="Annual maintenance (% of value)")
    parser.add_argument("--export", type=str, default="text", help="text|json")
    args = parser.parse_args()

    result = calculate_affordability(
        args.price, args.income, args.rent, args.rate, args.term,
        args.deposit, args.savings, args.rates, args.maintenance
    )

    if args.export == "json":
        print(json.dumps(result, indent=2, default=str))
    else:
        m = result["metrics"]
        b = result["breakdown"]
        print(f"Housing Affordability Analysis")
        print(f"{'─' * 55}")
        print(f"Price: ${args.price:,.0f} | Income: ${args.income:,.0f} | Rate: {args.rate}%")
        print()
        print(f"{'Metric':<30} {'Value':<12} {'Status'}")
        print("-" * 55)
        print(f"{'Price-to-Income':<30} {m['price_to_income']['value']:<12.1f} {m['price_to_income']['status']}")
        print(f"{'Price-to-Rent':<30} {m['price_to_rent']['value']:<12.1f} {'Favor ' + ('buying' if m['price_to_rent']['value'] < 20 else 'renting')}")
        print(f"{'Mortgage Burden':<30} {m['mortgage_burden_pct']['value']:<12.1f}% {m['mortgage_burden_pct']['status']}")
        print(f"{'Years to Save Deposit':<30} {m['years_to_save_deposit']['value']:<12.1f}")
        print(f"{'Affordability Index':<30} {m['affordability_index']['value']:<12.0f} {m['affordability_index']['status']}")
        print()
        print("Monthly Breakdown:")
        print(f"  Mortgage Payment: ${b['monthly_mortgage']:,.0f}")
        print(f"  Rates + Maintenance: ${b['monthly_rates_maintenance']:,.0f}")
        print(f"  Total Cost: ${b['total_monthly_cost']:,.0f} (vs Income: ${b['monthly_income']:,.0f})")
        print(f"  Deposit Needed: ${b['deposit_needed']:,.0f}")
        print(f"  Bank Qualifying Income: ${b['qualifying_income_required']:,.0f}")
