#!/usr/bin/env python3
"""
Macro Indicator Hub — Composite economic snapshot with recession risk scoring.

Scores 4 dimensions (Growth, Inflation, Labor, Financial Conditions) from
individual indicators, then aggregates into a composite assessment and
recession probability estimate.

Methodology from macro-dashboard/indicator-hub/SKILL.md

Usage:
    python3 indicator_hub.py --gdp 2.5 --indpro 1.8 --retail 3.2 --pmi 52 --caputil 78.5 \\
        --corepce 2.6 --corecpi 3.2 --unrate 4.2 --nfp 180 --claims 230 \\
        --fedfunds 5.25 --spread -0.35 --bbb 2.1
"""

import json
import sys


def score_growth(gdp, indpro, retail, pmi, caputil, income=2.0):
    """Score growth dimension (0-100) from 6 sub-indicators."""
    scores = []

    # GDP (QoQ annualized)
    if gdp > 3:         scores.append(95)
    elif gdp > 2:       scores.append(75)
    elif gdp > 1:       scores.append(55)
    elif gdp > 0:       scores.append(35)
    else:               scores.append(10)

    # Industrial Production YoY
    if indpro > 3:      scores.append(90)
    elif indpro > 1.5:  scores.append(70)
    elif indpro > 0:    scores.append(45)
    elif indpro > -2:   scores.append(25)
    else:               scores.append(10)

    # Retail Sales YoY
    if retail > 5:      scores.append(90)
    elif retail > 3:    scores.append(75)
    elif retail > 1:    scores.append(50)
    elif retail > -1:   scores.append(30)
    else:               scores.append(10)

    # ISM Manufacturing PMI
    if pmi > 55:        scores.append(90)
    elif pmi > 50:      scores.append(65)
    elif pmi > 45:      scores.append(35)
    elif pmi > 40:      scores.append(20)
    else:               scores.append(5)

    # Capacity Utilization
    if caputil > 80:    scores.append(85)
    elif caputil > 78:  scores.append(70)
    elif caputil > 75:  scores.append(45)
    elif caputil > 72:  scores.append(25)
    else:               scores.append(10)

    return round(sum(scores) / len(scores), 1)


def score_inflation(core_pce, core_cpi, ppi=3.0, breakeven=2.3):
    """Score inflation dimension — closer to 2% target = better."""
    scores = []

    # Core PCE (Fed's preferred)
    if 1.8 <= core_pce <= 2.2:   scores.append(95)
    elif 1.5 <= core_pce <= 2.5: scores.append(80)
    elif 1.0 <= core_pce <= 3.0: scores.append(55)
    elif core_pce > 4.0:         scores.append(10)
    else:                        scores.append(30)

    # Core CPI
    if 2.0 <= core_cpi <= 3.0:   scores.append(90)
    elif 1.5 <= core_cpi <= 3.5: scores.append(70)
    elif core_cpi > 5.0:         scores.append(10)
    else:                        scores.append(35)

    # 5y5y Breakeven
    if 2.0 <= breakeven <= 2.5:  scores.append(90)
    elif breakeven > 3.0:        scores.append(25)
    elif breakeven < 1.5:        scores.append(35)
    else:                        scores.append(60)

    return round(sum(scores) / len(scores), 1)


def score_labor(unrate, nfp_3m_avg, claims_4w_avg, jolts=8.0, wage_growth=3.5):
    """Score labor market dimension."""
    scores = []

    # Unemployment Rate
    if unrate < 3.5:     scores.append(95)
    elif unrate < 4.5:   scores.append(80)
    elif unrate < 5.5:   scores.append(55)
    elif unrate < 7.0:   scores.append(30)
    else:                scores.append(10)

    # Nonfarm Payrolls (3-month avg, thousands)
    if nfp_3m_avg > 200:  scores.append(90)
    elif nfp_3m_avg > 100: scores.append(65)
    elif nfp_3m_avg > 50:  scores.append(40)
    elif nfp_3m_avg > 0:   scores.append(25)
    else:                  scores.append(10)

    # Initial Claims (4-week avg)
    if claims_4w_avg < 220:  scores.append(90)
    elif claims_4w_avg < 260: scores.append(70)
    elif claims_4w_avg < 300: scores.append(45)
    elif claims_4w_avg < 350: scores.append(25)
    else:                     scores.append(10)

    # JOLTS Job Openings (millions)
    if jolts > 9:      scores.append(90)
    elif jolts > 7:    scores.append(65)
    elif jolts > 5:    scores.append(40)
    else:              scores.append(20)

    # Wage Growth YoY
    if 3.0 <= wage_growth <= 4.0: scores.append(90)
    elif 2.0 <= wage_growth <= 4.5: scores.append(70)
    elif wage_growth > 5.5:       scores.append(20)
    else:                         scores.append(35)

    return round(sum(scores) / len(scores), 1)


def score_financial(fed_funds, yc_spread, bbb_spread, vix=18):
    """Score financial conditions dimension."""
    scores = []

    # Yield curve spread (10Y-2Y)
    if yc_spread > 1.0:     scores.append(90)
    elif yc_spread > 0.5:   scores.append(75)
    elif yc_spread > 0:     scores.append(50)
    elif yc_spread > -0.5:  scores.append(25)
    else:                   scores.append(5)

    # BBB Corporate Spread
    if bbb_spread < 1.5:    scores.append(90)
    elif bbb_spread < 2.0:  scores.append(70)
    elif bbb_spread < 2.5:  scores.append(50)
    elif bbb_spread < 3.5:  scores.append(25)
    else:                   scores.append(5)

    # VIX
    if vix < 15:      scores.append(90)
    elif vix < 20:    scores.append(70)
    elif vix < 25:    scores.append(50)
    elif vix < 30:    scores.append(30)
    else:             scores.append(10)

    return round(sum(scores) / len(scores), 1)


def recession_probability(yc_spread, unrate, claims, pmi, cli=100):
    """
    Composite recession probability (0-100%).

    Combines signals from:
    - Yield curve (weight 40%): NY Fed model — 10Y-3M spread
    - Labor market (weight 30%): Sahm Rule + claims
    - Leading indicators (weight 20%): PMI, CLI
    - Financial stress (weight 10%): credit spreads
    """
    signals = []

    # Yield curve signal (40% weight)
    if yc_spread > 1.0:     yc_signal = 5
    elif yc_spread > 0.5:   yc_signal = 10
    elif yc_spread > 0:     yc_signal = 20
    elif yc_spread > -0.3:  yc_signal = 40
    elif yc_spread > -0.8:  yc_signal = 60
    else:                   yc_signal = 80
    signals.append(yc_signal * 0.40)

    # Labor market signal (30% weight) — Sahm Rule proxy
    if unrate < 4.0 and claims < 250:    labor_signal = 5
    elif unrate < 5.0 and claims < 300:  labor_signal = 20
    elif unrate < 6.0:                   labor_signal = 40
    elif unrate < 7.0:                   labor_signal = 60
    else:                                labor_signal = 80
    signals.append(labor_signal * 0.30)

    # Leading indicators (20% weight) — PMI proxy
    if pmi > 52:        pmi_signal = 10
    elif pmi > 48:      pmi_signal = 30
    elif pmi > 45:      pmi_signal = 50
    else:               pmi_signal = 70
    signals.append(pmi_signal * 0.20)

    # Financial stress (10% weight)
    if yc_spread > 0:   fin_signal = 10
    else:               fin_signal = 40
    signals.append(fin_signal * 0.10)

    return round(sum(signals), 1)


def indicator_snapshot(gdp, indpro, retail, pmi, caputil, core_pce, core_cpi,
                       unrate, nfp, claims, fed_funds, spread, bbb, vix=18,
                       jolts=8.0, wage_growth=3.5, income=2.0, ppi=3.0, breakeven=2.3):
    """
    Generate a full macro indicator snapshot with composite scores.
    """
    growth = score_growth(gdp, indpro, retail, pmi, caputil, income)
    inflation = score_inflation(core_pce, core_cpi, ppi, breakeven)
    labor = score_labor(unrate, nfp, claims, jolts, wage_growth)
    financial = score_financial(fed_funds, spread, bbb, vix)

    # Weighted composite
    weights = {"growth": 0.30, "inflation": 0.20, "labor": 0.25, "financial": 0.25}
    composite = round(
        growth * weights["growth"] +
        inflation * weights["inflation"] +
        labor * weights["labor"] +
        financial * weights["financial"], 1
    )

    recession = recession_probability(spread, unrate, claims, pmi)

    # Classification
    if composite > 75:     outlook = "Strong — above-trend growth, low recession risk"
    elif composite > 60:   outlook = "Moderate — near trend, watch for turning points"
    elif composite > 45:   outlook = "Mixed — significant headwinds, elevated uncertainty"
    elif composite > 30:   outlook = "Weak — below-trend, recession risk elevated"
    else:                  outlook = "Critical — severe stress, recession likely underway"

    if recession < 20:     recess_risk = "Low"
    elif recession < 35:   recess_risk = "Moderate"
    elif recession < 50:   recess_risk = "Elevated"
    else:                  recess_risk = "High"

    return {
        "composite_score": composite,
        "outlook": outlook,
        "recession_probability": recession,
        "recession_risk_level": recess_risk,
        "dimensions": {
            "growth": {"score": growth, "weight": 0.30, "weighted": round(growth * 0.30, 1)},
            "inflation": {"score": inflation, "weight": 0.20, "weighted": round(inflation * 0.20, 1)},
            "labor": {"score": labor, "weight": 0.25, "weighted": round(labor * 0.25, 1)},
            "financial": {"score": financial, "weight": 0.25, "weighted": round(financial * 0.25, 1)},
        },
        "signal_details": {
            "yield_curve": "Inverted — recession warning" if spread < 0 else ("Flat — late cycle" if spread < 0.5 else "Normal"),
            "labor_market": "Tight" if unrate < 4.5 else ("Balanced" if unrate < 5.5 else "Slack"),
            "inflation": "Above target" if core_pce > 2.5 else ("Near target" if core_pce > 1.8 else "Below target"),
        },
    }


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Macro Indicator Hub — Composite Snapshot")
    # Growth
    p.add_argument("--gdp", type=float, default=2.0, help="Real GDP QoQ annualized (%)")
    p.add_argument("--indpro", type=float, default=1.5, help="Industrial Production YoY (%)")
    p.add_argument("--retail", type=float, default=2.0, help="Retail Sales YoY (%)")
    p.add_argument("--pmi", type=float, default=50.0, help="ISM Manufacturing PMI")
    p.add_argument("--caputil", type=float, default=78.0, help="Capacity Utilization (%)")
    p.add_argument("--income", type=float, default=2.0, help="Real Personal Income YoY (%)")
    # Inflation
    p.add_argument("--core-pce", type=float, default=2.5, help="Core PCE YoY (%)")
    p.add_argument("--core-cpi", type=float, default=3.0, help="Core CPI YoY (%)")
    p.add_argument("--ppi", type=float, default=3.0, help="PPI YoY (%)")
    p.add_argument("--breakeven", type=float, default=2.3, help="5y5y Inflation Breakeven (%)")
    # Labor
    p.add_argument("--unrate", type=float, default=4.5, help="Unemployment Rate (%)")
    p.add_argument("--nfp", type=float, default=150, help="Nonfarm Payrolls 3M avg (K)")
    p.add_argument("--claims", type=float, default=250, help="Initial Claims 4W avg (K)")
    p.add_argument("--jolts", type=float, default=8.0, help="JOLTS Job Openings (M)")
    p.add_argument("--wage-growth", type=float, default=3.5, help="Wage Growth YoY (%)")
    # Financial
    p.add_argument("--fedfunds", type=float, default=5.0, help="Fed Funds Rate (%)")
    p.add_argument("--spread", type=float, default=0.0, help="10Y-2Y Spread (%)")
    p.add_argument("--bbb", type=float, default=2.0, help="BBB-10Y Credit Spread (%)")
    p.add_argument("--vix", type=float, default=20.0, help="VIX Volatility Index")
    p.add_argument("--export", type=str, default="text", help="text|json")
    args = p.parse_args()

    result = indicator_snapshot(
        args.gdp, args.indpro, args.retail, args.pmi, args.caputil,
        args.core_pce, args.core_cpi, args.unrate, args.nfp, args.claims,
        args.fedfunds, args.spread, args.bbb, args.vix, args.jolts,
        args.wage_growth, args.income, args.ppi, args.breakeven,
    )

    if args.export == "json":
        print(json.dumps(result, indent=2, default=str))
    else:
        print(f"Macro Composite Score: {result['composite_score']:.0f}/100")
        print(f"Outlook: {result['outlook']}")
        print(f"Recession Probability: {result['recession_probability']:.0f}% — {result['recession_risk_level']}")
        print()
        print(f"{'Dimension':<15} {'Score':<8} {'Weight':<8} {'Weighted':<8}")
        print("-" * 42)
        for name, data in result["dimensions"].items():
            bar = "█" * int(data["score"] / 10)
            print(f"{name:<15} {data['score']:<8.0f} {data['weight']:<8.2f} {data['weighted']:<8.1f} {bar}")
        print()
        for signal, status in result["signal_details"].items():
            print(f"  {signal}: {status}")
