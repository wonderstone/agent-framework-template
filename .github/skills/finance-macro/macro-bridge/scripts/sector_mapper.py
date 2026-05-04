#!/usr/bin/env python3
"""
Sector Mapper — Map Macro Shocks to Sector/Asset Impact.

Translates macro events (rate changes, FX moves, commodity shocks, liquidity shifts)
into sector-level and asset-level impact scores using the Macro-Bridge sensitivity matrix.

Usage:
    python3 sector_mapper.py --shock rate --direction up --magnitude 50
    python3 sector_mapper.py --shock commodity --commodity oil --direction up --magnitude 20
    python3 sector_mapper.py --scenario fed-tightening
"""

import json
import sys

# Sector sensitivity matrix: {sector: {shock_type: sensitivity}}
# Sensitivity: -5 (very negative) to +5 (very positive)
SECTOR_SENSITIVITY = {
    # Liquidity convention: + = benefits from liquidity EXPANSION, - = hurt by CONTRACTION
    # Rate convention: + = benefits from higher rates, - = hurt by higher rates
    "technology":     {"rate": -4, "usd": -2, "oil": 0, "liquidity": +4, "commodity_broad": 0},
    "banks":          {"rate": +3, "usd": +2, "oil": 0, "liquidity": 0, "commodity_broad": 0},
    "real_estate":    {"rate": -4, "usd": 0, "oil": 0, "liquidity": +4, "commodity_broad": 0},
    "energy":         {"rate": 0, "usd": -3, "oil": +5, "liquidity": 0, "commodity_broad": +4},
    "consumer_disc":  {"rate": -3, "usd": -1, "oil": -3, "liquidity": +3, "commodity_broad": -2},
    "consumer_staple":{"rate": -1, "usd": 0, "oil": -1, "liquidity": -1, "commodity_broad": -1},
    "healthcare":     {"rate": -1, "usd": 0, "oil": 0, "liquidity": -1, "commodity_broad": 0},
    "industrials":    {"rate": -3, "usd": +2, "oil": -3, "liquidity": +2, "commodity_broad": -2},
    "materials":      {"rate": -2, "usd": -2, "oil": -1, "liquidity": +2, "commodity_broad": +3},
    "utilities":      {"rate": -3, "usd": 0, "oil": -1, "liquidity": -1, "commodity_broad": 0},
    "gold_miners":    {"rate": -1, "usd": -3, "oil": 0, "liquidity": -1, "commodity_broad": 0},
    "crypto":         {"rate": -5, "usd": -3, "oil": 0, "liquidity": +5, "commodity_broad": 0},
}

ASSET_SENSITIVITY = {
    # Liquidity: + = rallies on liquidity expansion, - = safe haven demand during contraction
    # commodity_broad: + = benefits from broad commodity upswing
    "BTC":          {"rate": -5, "usd": -3, "liquidity": +5, "oil": 0, "commodity_broad": 0},
    "gold":         {"rate": -2, "usd": -3, "liquidity": 0, "oil": +1, "commodity_broad": +1},
    "nasdaq":       {"rate": -4, "usd": -2, "liquidity": +4, "oil": -1, "commodity_broad": 0},
    "sp500":        {"rate": -3, "usd": -2, "liquidity": +3, "oil": -1, "commodity_broad": 0},
    "usd_dxy":      {"rate": +3, "usd": +5, "liquidity": -3, "oil": +1, "commodity_broad": -1},
    "em_equities":  {"rate": -3, "usd": -4, "liquidity": +4, "oil": +2, "commodity_broad": +3},
    "hy_credit":    {"rate": -2, "usd": -1, "liquidity": +3, "oil": -1, "commodity_broad": 0},
    "treasuries":   {"rate": -3, "usd": +1, "liquidity": -2, "oil": -1, "commodity_broad": -1},
}

SCENARIOS = {
    "fed-tightening": {
        "description": "Aggressive Fed tightening + QT",
        "shocks": {"rate": +1.5, "usd": +1.2, "oil": -0.5, "liquidity": -2.0},
    },
    "fed-easing": {
        "description": "Fed rate cuts + possible QE restart",
        "shocks": {"rate": -1.5, "usd": -1.0, "oil": +0.5, "liquidity": +2.0},
    },
    "china-reopening": {
        "description": "China stimulus boosts commodity demand and EM",
        "shocks": {"rate": +0.3, "usd": -1.0, "oil": +1.5, "liquidity": +1.0},
    },
    "global-recession": {
        "description": "Synchronized global downturn",
        "shocks": {"rate": -2.0, "usd": +1.5, "oil": -2.0, "liquidity": -3.0},
    },
    "commodity-supercycle": {
        "description": "Multi-year commodity upswing",
        "shocks": {"rate": +0.5, "usd": -1.5, "oil": +2.5, "liquidity": +0.5, "commodity_broad": +2.0},
    },
    "geopolitical-shock": {
        "description": "Geopolitical conflict / supply chain disruption",
        "shocks": {"rate": -0.5, "usd": +1.5, "oil": +3.0, "liquidity": -2.0},
    },
}


def map_shock_to_sectors(shocks):
    """Map a set of macro shocks to sector impact scores."""
    results = []
    for sector, sensitivities in SECTOR_SENSITIVITY.items():
        total_impact = 0
        components = {}
        for shock_type, magnitude in shocks.items():
            if shock_type in sensitivities and magnitude != 0:
                impact = sensitivities[shock_type] * magnitude
                total_impact += impact
                components[shock_type] = round(impact, 1)

        results.append({
            "sector": sector,
            "total_impact": round(total_impact, 1),
            "components": components,
            "signal": _classify_impact(total_impact),
        })

    results.sort(key=lambda x: x["total_impact"], reverse=True)
    return results


def map_shock_to_assets(shocks):
    """Map macro shocks to asset impact scores."""
    results = []
    for asset, sensitivities in ASSET_SENSITIVITY.items():
        total_impact = 0
        for shock_type, magnitude in shocks.items():
            if shock_type in sensitivities and magnitude != 0:
                total_impact += sensitivities[shock_type] * magnitude

        results.append({
            "asset": asset,
            "total_impact": round(total_impact, 1),
            "signal": _classify_impact(total_impact),
        })

    results.sort(key=lambda x: x["total_impact"], reverse=True)
    return results


def _classify_impact(score):
    if score > 2.0:
        return "Strong Positive"
    elif score > 0.5:
        return "Positive"
    elif score > -0.5:
        return "Neutral"
    elif score > -2.0:
        return "Negative"
    else:
        return "Strong Negative"


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Map macro shocks to sector/asset impacts")
    parser.add_argument("--scenario", type=str, help="Pre-built scenario name")
    parser.add_argument("--shock", type=str, help="Single shock type (rate/usd/oil/liquidity)")
    parser.add_argument("--direction", type=str, choices=["up", "down"])
    parser.add_argument("--magnitude", type=float, default=1.0, help="Shock magnitude (std dev units)")
    parser.add_argument("--target", type=str, default="both", choices=["sectors", "assets", "both"])
    parser.add_argument("--export", type=str, default="text", help="text|json")
    args = parser.parse_args()

    shocks = {}
    if args.scenario and args.scenario in SCENARIOS:
        scenario = SCENARIOS[args.scenario]
        shocks = scenario["shocks"]
        print(f"Scenario: {args.scenario} — {scenario['description']}\n")
    elif args.shock:
        direction = 1 if args.direction == "up" else -1
        shocks = {args.shock: direction * args.magnitude}
    else:
        print("Specify --scenario or --shock")
        sys.exit(1)

    output = {"shocks": shocks}

    if args.target in ("sectors", "both"):
        sector_results = map_shock_to_sectors(shocks)
        output["sectors"] = sector_results
        if args.export != "json":
            print(f"{'Sector':<20} {'Impact':<8} {'Signal':<18}")
            print("-" * 50)
            for r in sector_results:
                emoji = ""
                if r["total_impact"] > 2: emoji = "🟢"
                elif r["total_impact"] > 0: emoji = "🟡"
                elif r["total_impact"] > -2: emoji = "🟠"
                else: emoji = "🔴"
                print(f"{emoji} {r['sector']:<17} {r['total_impact']:+.1f}    {r['signal']:<18}")

    if args.target in ("assets", "both"):
        asset_results = map_shock_to_assets(shocks)
        output["assets"] = asset_results
        if args.export != "json":
            print(f"\n{'Asset':<15} {'Impact':<8} {'Signal'}")
            print("-" * 40)
            for r in asset_results:
                print(f"{r['asset']:<15} {r['total_impact']:+.1f}    {r['signal']}")

    if args.export == "json":
        print(json.dumps(output, indent=2, default=str))
