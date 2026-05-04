#!/usr/bin/env python3
"""
Property Cycle Phase Detector.

Scores 7 indicators to classify a property market as:
  Recovery | Boom (Early-Mid) | Boom (Late) | Transition | Bust (Early-Mid) | Stabilization

Usage:
    python3 cycle_score.py --price-yoy 5.2 --price-income-vs-lt 1.15 --credit-yoy 8.0 --approvals-yoy 12.0 --inventory-months 2.5 --auction-clearance 72 --investor-share 28
"""

import json
import sys


def score_cycle(price_yoy, price_income_vs_lt, credit_yoy, approvals_yoy, inventory_months, auction_clearance, investor_share):
    """
    Score each indicator -2 (bust) to +2 (boom) and return weighted total.
    """

    # 1. Real House Price Momentum (weight 25%)
    if price_yoy > 12:        price_score = 2.0
    elif price_yoy > 6:       price_score = 1.5
    elif price_yoy > 2:       price_score = 0.5
    elif price_yoy > -2:      price_score = 0.0
    elif price_yoy > -6:      price_score = -1.0
    elif price_yoy > -12:     price_score = -1.5
    else:                     price_score = -2.0

    # 2. Price-to-Income vs Long-Term Avg (weight 20%)
    if price_income_vs_lt > 1.30:     pi_score = 2.0
    elif price_income_vs_lt > 1.15:   pi_score = 1.5
    elif price_income_vs_lt > 1.05:   pi_score = 0.5
    elif price_income_vs_lt > 0.95:   pi_score = 0.0
    elif price_income_vs_lt > 0.85:   pi_score = -1.0
    else:                             pi_score = -2.0

    # 3. Housing Credit Growth YoY (weight 15%)
    if credit_yoy > 12:        credit_score = 2.0
    elif credit_yoy > 8:       credit_score = 1.5
    elif credit_yoy > 4:       credit_score = 0.5
    elif credit_yoy > 0:       credit_score = 0.0
    elif credit_yoy > -3:      credit_score = -0.5
    else:                      credit_score = -1.5

    # 4. Building Approvals YoY (weight 15%)
    if approvals_yoy > 20:     appr_score = 2.0
    elif approvals_yoy > 10:   appr_score = 1.0
    elif approvals_yoy > 0:    appr_score = 0.5
    elif approvals_yoy > -10:  appr_score = -0.5
    elif approvals_yoy > -25:  appr_score = -1.0
    else:                      appr_score = -2.0

    # 5. Months of Inventory (weight 10%)
    if inventory_months < 1.5:    inv_score = 2.0
    elif inventory_months < 3:     inv_score = 1.0
    elif inventory_months < 5:     inv_score = 0.0
    elif inventory_months < 8:     inv_score = -1.0
    else:                          inv_score = -2.0

    # 6. Auction Clearance Rate (weight 10%)
    if auction_clearance > 80:     auc_score = 2.0
    elif auction_clearance > 70:   auc_score = 1.0
    elif auction_clearance > 60:   auc_score = 0.0
    elif auction_clearance > 50:   auc_score = -0.5
    elif auction_clearance > 40:   auc_score = -1.0
    else:                          auc_score = -2.0

    # 7. Investor Activity % of Lending (weight 5%)
    if investor_share > 40:        inv_share_score = 2.0
    elif investor_share > 30:      inv_share_score = 1.0
    elif investor_share > 20:      inv_share_score = 0.0
    elif investor_share > 10:      inv_share_score = -0.5
    else:                          inv_share_score = -1.0

    weighted = (
        price_score * 0.25 +
        pi_score * 0.20 +
        credit_score * 0.15 +
        appr_score * 0.15 +
        inv_score * 0.10 +
        auc_score * 0.10 +
        inv_share_score * 0.05
    )

    if weighted > 1.0:
        phase = "Boom (Late) — Speculative excess, prepare for correction"
    elif weighted > 0.5:
        phase = "Boom (Early-Mid) — Momentum intact, hold"
    elif weighted > -0.5:
        phase = "Transition — Phase change approaching, monitor closely"
    elif weighted > -1.2:
        phase = "Bust (Early-Mid) — Correction underway, avoid"
    else:
        phase = "Stabilization — Bottom forming, screen for value"

    return {
        "weighted_score": round(weighted, 1),
        "phase": phase,
        "indicators": {
            "price_momentum": {"value": price_yoy, "score": price_score, "weight": 0.25},
            "price_income_vs_lt": {"value": price_income_vs_lt, "score": pi_score, "weight": 0.20},
            "credit_growth": {"value": credit_yoy, "score": credit_score, "weight": 0.15},
            "building_approvals": {"value": approvals_yoy, "score": appr_score, "weight": 0.15},
            "months_inventory": {"value": inventory_months, "score": inv_score, "weight": 0.10},
            "auction_clearance": {"value": auction_clearance, "score": auc_score, "weight": 0.10},
            "investor_share": {"value": investor_share, "score": inv_share_score, "weight": 0.05},
        },
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Property Cycle Phase Detector")
    parser.add_argument("--price-yoy", type=float, required=True, help="Real house price YoY %")
    parser.add_argument("--price-income-vs-lt", type=float, required=True, help="Price/Income ratio vs long-term average (1.0 = at avg)")
    parser.add_argument("--credit-yoy", type=float, required=True, help="Housing credit growth YoY %")
    parser.add_argument("--approvals-yoy", type=float, required=True, help="Building approvals YoY %")
    parser.add_argument("--inventory-months", type=float, required=True, help="Months of inventory")
    parser.add_argument("--auction-clearance", type=float, required=True, help="Auction clearance rate %")
    parser.add_argument("--investor-share", type=float, required=True, help="Investor share of new lending %")
    parser.add_argument("--export", type=str, default="text", help="text|json")
    args = parser.parse_args()

    result = score_cycle(
        args.price_yoy, args.price_income_vs_lt, args.credit_yoy,
        args.approvals_yoy, args.inventory_months, args.auction_clearance, args.investor_share
    )

    if args.export == "json":
        print(json.dumps(result, indent=2, default=str))
    else:
        print(f"Property Cycle Score: {result['weighted_score']:.1f}")
        print(f"Phase: {result['phase']}")
        print()
        print(f"{'Indicator':<30} {'Value':<10} {'Score':<8}")
        print("-" * 50)
        for name, data in result["indicators"].items():
            print(f"{name:<30} {data['value']:<10} {data['score']:+.1f}")
