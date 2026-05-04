#!/usr/bin/env python3
"""
Commodity Supercycle Detector — 5-Factor Scoring Model

Implements the 5/5 checklist from commodity-macro/commodity-supercycle/SKILL.md.
Scores each supercycle driver 0-20, then classifies the cycle phase.

Historical Supercycles:
  1st: 1890s-1910s — US industrialization (coal, steel, copper)
  2nd: 1940s-1970s — Post-war reconstruction (oil, steel, copper)
  3rd: 2000s-2014  — China industrialization (all commodities)
  4th: 2020s-?     — Energy transition + electrification candidate

Usage:
    python3 supercycle_scorer.py --industrialization 16 --underinvestment 18 \\
        --demand-shift 17 --inventory 12 --producer-discipline 14
    python3 supercycle_scorer.py --capex-gdp 4.2 --lme-inventory 55 \\
        --india-infra 220 --opec-compliance 85
"""

import json
import sys


def score_factor_1(industrialization_score, india_infra_spending=None, sea_urbanization=None):
    """
    Factor 1: Major economy industrializing/urbanizing? (0-20)

    Current drivers: India infrastructure buildout, SE Asia urbanization,
    China+1 supply chain diversification.
    """
    score = 0

    # India as potential next China-scale driver
    if india_infra_spending:
        if india_infra_spending > 250:  score += 8   # $250B+ annual infrastructure
        elif india_infra_spending > 150: score += 5
        elif india_infra_spending > 100: score += 3
    else:
        score += 5  # Default: India growing but not yet China-scale

    # SE Asia urbanization trend
    if sea_urbanization:
        if sea_urbanization > 65: score += 5     # >65% urbanisation rate
        elif sea_urbanization > 50: score += 3
    else:
        score += 3  # Default: moderate urbanization ongoing

    # Base industrialization assessment
    if industrialization_score > 16:   score += 7
    elif industrialization_score > 12: score += 5
    elif industrialization_score > 8:  score += 3
    else:                              score += 1

    return min(20, score)


def score_factor_2(capex_pct_gdp, mine_development_years=10, depletion_rate=None):
    """
    Factor 2: Supply underinvestment after previous bust? (0-20)

    Mining capex / GDP near multi-decade lows = bullish for future prices.
    Mine development timelines (10-15 years) mean supply response is very slow.
    """
    score = 0

    # Capex/GDP ratio — lower = more underinvestment
    if capex_pct_gdp:
        if capex_pct_gdp < 3.0:    score += 10   # Multi-decade low
        elif capex_pct_gdp < 4.5:  score += 7
        elif capex_pct_gdp < 6.0:  score += 4
        else:                      score += 1

    # Mine development timeline factor (longer = more bullish)
    if mine_development_years > 12: score += 6
    elif mine_development_years > 8: score += 4
    else:                            score += 2

    # Depletion — existing mines depleting faster than new discoveries
    if depletion_rate:
        if depletion_rate > 5.0:   score += 4
        elif depletion_rate > 3.0: score += 2
        else:                      score += 1
    else:
        score += 2  # Default: copper grades declining, depletion ongoing

    return min(20, score)


def score_factor_3(demand_shift_score, electrification_index=None, ev_penetration=None):
    """
    Factor 3: Structural demand shift? (0-20)

    Energy transition = massive electrification = copper, lithium, nickel, cobalt, rare earths.
    Unlike previous cycles, this is policy-driven AND technology-driven.
    """
    score = 0

    if demand_shift_score > 16:     score += 10
    elif demand_shift_score > 12:   score += 7
    elif demand_shift_score > 8:    score += 4
    else:                           score += 1

    # Electrification metric
    if electrification_index:
        if electrification_index > 80:  score += 6
        elif electrification_index > 60: score += 4
        else:                            score += 2
    else:
        score += 4  # Default: global electrification trend strong

    # EV penetration (catalytic for battery metals)
    if ev_penetration:
        if ev_penetration > 20:    score += 4
        elif ev_penetration > 10:  score += 3
        else:                      score += 1
    else:
        score += 2  # Default: EV adoption growing but moderating

    return min(20, score)


def score_factor_4(inventory_pct_5y_avg, strategic_stockpiling=False):
    """
    Factor 4: Inventories at cycle lows? (0-20)

    Low inventories = limited buffer against supply disruptions = price spike risk.
    Check LME, SHFE, CME warehouse data.
    """
    score = 0

    if inventory_pct_5y_avg:
        if inventory_pct_5y_avg < 60:     score += 12  # Critically low
        elif inventory_pct_5y_avg < 80:   score += 9
        elif inventory_pct_5y_avg < 100:  score += 6
        elif inventory_pct_5y_avg < 120:  score += 3
        else:                             score += 1
    else:
        score += 5  # Default: copper inventories low, others mixed

    # Strategic stockpiling (governments building reserves)
    if strategic_stockpiling:
        score += 8
    else:
        score += 3  # Default: some strategic buying (India, US SPR refill)

    return min(20, score)


def score_factor_5(opec_compliance=None, mining_consolidation=None, capital_discipline_score=12):
    """
    Factor 5: Producer discipline? (0-20)

    OPEC+ quota compliance, mining sector consolidation, shareholder return focus
    over growth capex — all supportive for prices.
    """
    score = 0

    # OPEC+ discipline (for oil)
    if opec_compliance:
        if opec_compliance > 90:    score += 7
        elif opec_compliance > 75:  score += 5
        elif opec_compliance > 60:  score += 3
        else:                       score += 1
    else:
        score += 4  # Default: OPEC+ managing market but cheating risk

    # Mining consolidation
    if mining_consolidation:
        if mining_consolidation > 60:  score += 6
        elif mining_consolidation > 40: score += 4
        else:                           score += 2
    else:
        score += 4  # Default: moderate consolidation (BHP, Rio, Glencore dominant)

    # Capital discipline (buybacks + dividends over growth capex)
    if capital_discipline_score > 15:   score += 7
    elif capital_discipline_score > 10: score += 5
    elif capital_discipline_score > 5:  score += 3
    else:                               score += 1

    return min(20, score)


def detect_supercycle(
    industrialization=14,
    capex_pct_gdp=4.5,
    demand_shift_score=14,
    inventory_pct_5y_avg=70,
    producer_discipline=14,
    # Extended parameters
    india_infra=None,
    sea_urbanization=None,
    mine_dev_years=10,
    depletion_rate=None,
    electrification_index=None,
    ev_penetration=None,
    strategic_stockpiling=False,
    opec_compliance=None,
    mining_consolidation=None,
):
    """
    Run the full 5-factor supercycle detection model.

    Returns total score (0-100), classification, and factor breakdown.
    """
    f1 = score_factor_1(industrialization, india_infra, sea_urbanization)
    f2 = score_factor_2(capex_pct_gdp, mine_dev_years, depletion_rate)
    f3 = score_factor_3(demand_shift_score, electrification_index, ev_penetration)
    f4 = score_factor_4(inventory_pct_5y_avg, strategic_stockpiling)
    f5 = score_factor_5(opec_compliance, mining_consolidation, producer_discipline)

    total = f1 + f2 + f3 + f4 + f5
    checks_passed = sum(1 for f in [f1, f2, f3, f4, f5] if f >= 12)

    # Classification
    if total >= 80 and checks_passed >= 4:
        phase = "Supercycle Confirmed (Active)"
        description = "Multiple drivers aligned — sustained commodity demand growth expected"
    elif total >= 60 and checks_passed >= 3:
        phase = "Supercycle Likely (Forming)"
        description = "Key drivers in place but not fully confirmed — build positions selectively"
    elif total >= 40 and checks_passed >= 2:
        phase = "Potential Supercycle (Early Signs)"
        description = "Some structural demand shifts visible but supply response still possible"
    elif total >= 20:
        phase = "No Clear Supercycle"
        description = "Mixed signals — cyclical more than structural forces at work"
    else:
        phase = "Supercycle Unlikely / Ending"
        description = "Supply abundant, demand growth moderate — commodity bear market regime"

    # Phase assessment
    if checks_passed >= 4:
        cycle_phase = "Phase 1-2: Demand Shock / Supply Response"
    elif checks_passed >= 2:
        cycle_phase = "Transition — Either early formation or late-stage moderation"
    else:
        cycle_phase = "Phase 3-4: Overinvestment / Purge"

    # Asset implications
    asset_signals = {}
    if f2 >= 14 and f3 >= 14:
        asset_signals["copper"] = "Strongly Bullish — electrification + supply deficit"
    elif f2 >= 12 or f3 >= 12:
        asset_signals["copper"] = "Bullish — structural demand growing"
    else:
        asset_signals["copper"] = "Neutral / Mixed"

    if f5 >= 14 or f4 >= 14:
        asset_signals["oil"] = "Bullish — supply constrained + producer discipline"
    elif f4 < 8:
        asset_signals["oil"] = "Bearish — ample supply, demand risk"
    else:
        asset_signals["oil"] = "Neutral — range-bound"

    if f3 >= 14:
        asset_signals["battery_metals"] = "Bullish — energy transition demand structural"
    elif f3 >= 10:
        asset_signals["battery_metals"] = "Constructive — growing but supply responding"
    else:
        asset_signals["battery_metals"] = "Neutral — supply growth matching demand"

    if total >= 60:
        asset_signals["gold"] = "Supportive — commodity cycle + geopolitical hedge demand"
    else:
        asset_signals["gold"] = "Idiosyncratic — driven by rates/USD, not commodity cycle"

    return {
        "total_score": total,
        "checks_passed": f"{checks_passed}/5",
        "phase": phase,
        "description": description,
        "cycle_phase": cycle_phase,
        "factors": {
            "industrialization": {"score": f1, "label": "Major economy industrializing/urbanizing"},
            "underinvestment":  {"score": f2, "label": "Supply underinvestment after bust"},
            "demand_shift":     {"score": f3, "label": "Structural demand shift (energy transition)"},
            "inventory":        {"score": f4, "label": "Inventories at cycle lows"},
            "producer_discipline": {"score": f5, "label": "Producer discipline / consolidation"},
        },
        "asset_signals": asset_signals,
        "references": {
            "historical_cycles": [
                "1st: 1890s-1910s — US industrialization",
                "2nd: 1940s-1970s — Post-war reconstruction",
                "3rd: 2000s-2014 — China industrialization",
                "4th: 2020s-? — Energy transition + electrification candidate",
            ],
        },
    }


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Commodity Supercycle Detector — 5-Factor Model")
    p.add_argument("--industrialization", type=float, default=14, help="Industrialization score (0-20)")
    p.add_argument("--capex-gdp", type=float, default=4.5, help="Mining capex as %% GDP")
    p.add_argument("--demand-shift", type=float, default=14, help="Structural demand shift score (0-20)")
    p.add_argument("--inventory", type=float, default=70, help="Inventory level as %% of 5Y avg")
    p.add_argument("--producer-discipline", type=float, default=14, help="Producer discipline score (0-20)")
    # Extended
    p.add_argument("--india-infra", type=float, help="India annual infrastructure spending ($B)")
    p.add_argument("--sea-urbanization", type=float, help="SE Asia urbanization rate (%)")
    p.add_argument("--mine-dev-years", type=float, default=10, help="Avg mine development timeline (years)")
    p.add_argument("--depletion-rate", type=float, help="Mine depletion rate (%/year)")
    p.add_argument("--electrification", type=float, help="Electrification index (0-100)")
    p.add_argument("--ev-penetration", type=float, help="Global EV penetration rate (%)")
    p.add_argument("--strategic-stockpiling", action="store_true", help="Strategic stockpiling active")
    p.add_argument("--opec-compliance", type=float, help="OPEC+ quota compliance rate (%)")
    p.add_argument("--mining-consolidation", type=float, help="Top-5 miner market share (%)")
    p.add_argument("--export", type=str, default="text", help="text|json")
    args = p.parse_args()

    result = detect_supercycle(
        industrialization=args.industrialization,
        capex_pct_gdp=args.capex_gdp,
        demand_shift_score=args.demand_shift,
        inventory_pct_5y_avg=args.inventory,
        producer_discipline=args.producer_discipline,
        india_infra=args.india_infra,
        sea_urbanization=args.sea_urbanization,
        mine_dev_years=args.mine_dev_years,
        depletion_rate=args.depletion_rate,
        electrification_index=args.electrification,
        ev_penetration=args.ev_penetration,
        strategic_stockpiling=args.strategic_stockpiling,
        opec_compliance=args.opec_compliance,
        mining_consolidation=args.mining_consolidation,
    )

    if args.export == "json":
        print(json.dumps(result, indent=2, default=str))
    else:
        print(f"Supercycle Score: {result['total_score']}/100 — {result['checks_passed']} checks passed")
        print(f"Phase: {result['phase']}")
        print(f"Cycle Position: {result['cycle_phase']}")
        print(f"Description: {result['description']}")
        print()
        print(f"{'Factor':<30} {'Score':<8} {'Bar'}")
        print("-" * 55)
        for name, data in result["factors"].items():
            bar = "█" * data["score"]
            print(f"{data['label']:<30} {data['score']:<8} {bar}")
        print()
        print("Asset Signals:")
        for asset, signal in result["asset_signals"].items():
            print(f"  {asset}: {signal}")
