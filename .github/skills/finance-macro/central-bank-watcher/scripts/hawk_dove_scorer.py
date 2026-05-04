#!/usr/bin/env python3
"""
Hawk-Dove Index — Cross-Central Bank Policy Sentiment Scorer.

Scores central banks on a -3 (strongly dovish) to +3 (strongly hawkish) scale
across 5 dimensions: rate direction, inflation assessment, growth/labor,
balance sheet policy, and risk assessment.

Usage:
    python3 hawk_dove_scorer.py --bank fed --rate 1.0 --inflation 1.5 --growth 0.5 --bs 1.0 --risk 0.5
    python3 hawk_dove_scorer.py --compare
"""

import json
import sys
from datetime import datetime

BANKS = ["fed", "ecb", "pboc", "boj", "rbnz", "boe", "rba"]

DIMENSION_WEIGHTS = {
    "rate_direction": 0.30,
    "inflation_assessment": 0.25,
    "growth_labor": 0.20,
    "balance_sheet": 0.15,
    "risk_assessment": 0.10,
}


def score_bank(bank, rate_direction, inflation_assessment, growth_labor, balance_sheet, risk_assessment):
    """
    Score a central bank's hawk-dove stance.

    Args:
        rate_direction: -3 (cutting aggressively) to +3 (hiking aggressively)
        inflation_assessment: -3 (inflation well below target) to +3 (inflation well above, fighting)
        growth_labor: -3 (deep recession, high unemployment) to +3 (overheating)
        balance_sheet: -3 (QE expansion) to +3 (QT, balance sheet runoff)
        risk_assessment: -3 (risks to downside) to +3 (risks to upside)
    """
    dimensions = {
        "rate_direction": rate_direction,
        "inflation_assessment": inflation_assessment,
        "growth_labor": growth_labor,
        "balance_sheet": balance_sheet,
        "risk_assessment": risk_assessment,
    }

    weighted_score = sum(
        dimensions[dim] * DIMENSION_WEIGHTS[dim]
        for dim in DIMENSION_WEIGHTS
    )

    if weighted_score > 2.0:
        classification = "Strongly Hawkish"
    elif weighted_score > 1.0:
        classification = "Moderately Hawkish"
    elif weighted_score > 0.4:
        classification = "Slightly Hawkish"
    elif weighted_score > -0.3:
        classification = "Neutral"
    elif weighted_score > -0.9:
        classification = "Slightly Dovish"
    elif weighted_score > -1.9:
        classification = "Moderately Dovish"
    else:
        classification = "Strongly Dovish"

    return {
        "bank": bank.upper(),
        "weighted_score": round(weighted_score, 2),
        "classification": classification,
        "dimensions": dimensions,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


def compare_banks(bank_scores):
    """Compare hawk-dove scores across banks and compute divergence."""
    if not bank_scores:
        return {"error": "No bank scores provided"}

    max_divergence = 0
    most_hawkish = max(bank_scores, key=lambda x: x["weighted_score"])
    most_dovish = min(bank_scores, key=lambda x: x["weighted_score"])

    for i, b1 in enumerate(bank_scores):
        for b2 in bank_scores[i+1:]:
            divergence = abs(b1["weighted_score"] - b2["weighted_score"])
            if divergence > max_divergence:
                max_divergence = divergence

    return {
        "banks": bank_scores,
        "most_hawkish": most_hawkish["bank"],
        "most_dovish": most_dovish["bank"],
        "max_divergence": round(max_divergence, 2),
        "avg_score": round(sum(b["weighted_score"] for b in bank_scores) / len(bank_scores), 2),
        "convergence": "High" if max_divergence < 1.5 else ("Moderate" if max_divergence < 3.0 else "Low"),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Hawk-Dove Index Scorer")
    parser.add_argument("--bank", type=str, choices=BANKS, help="Single bank to score")
    parser.add_argument("--rate", type=float, default=0, help="Rate direction score (-3 to +3)")
    parser.add_argument("--inflation", type=float, default=0, help="Inflation assessment score (-3 to +3)")
    parser.add_argument("--growth", type=float, default=0, help="Growth/labor score (-3 to +3)")
    parser.add_argument("--bs", type=float, default=0, help="Balance sheet score (-3 to +3)")
    parser.add_argument("--risk", type=float, default=0, help="Risk assessment score (-3 to +3)")
    parser.add_argument("--compare", action="store_true", help="Compare multiple banks (provide JSON via stdin)")
    parser.add_argument("--export", type=str, default="text", help="text|json")
    args = parser.parse_args()

    if args.compare:
        input_data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else []
        scores = []
        for b in input_data:
            result = score_bank(**b)
            scores.append(result)
        result = compare_banks(scores)
    else:
        result = score_bank(args.bank or "fed", args.rate, args.inflation, args.growth, args.bs, args.risk)

    if args.export == "json":
        print(json.dumps(result, indent=2, default=str))
    else:
        if "banks" in result:
            print(f"Hawk-Dove Cross-Bank Comparison")
            print(f"Convergence: {result['convergence']} | Max Divergence: {result['max_divergence']:.1f} | Avg: {result['avg_score']:.1f}")
            print()
            for b in result["banks"]:
                bar_len = int((b["weighted_score"] + 3) * 5)
                bar = "█" * bar_len + "░" * (30 - bar_len)
                hawk_side = "🦅" if b["weighted_score"] > 0 else ""
                dove_side = "🕊️" if b["weighted_score"] < 0 else ""
                print(f"{b['bank']:<6} {b['weighted_score']:+4.1f} {bar} {hawk_side}{dove_side} {b['classification']}")
        else:
            print(f"{result['bank']}: {result['weighted_score']:+.1f} — {result['classification']}")
            for dim, val in result["dimensions"].items():
                print(f"  {dim}: {val:+.1f}")
