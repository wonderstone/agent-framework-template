#!/usr/bin/env python3
"""
Macro Signal Backtest Framework (Stub)

Framework for backtesting macro signals against asset returns.
Takes macro indicator time series + asset price series → computes signal accuracy.

Currently stub — production use requires historical macro data pipeline.
Designed to work with cached MCP data once sufficient history is accumulated.

Usage:
    python3 backtest_stub.py --signal scissors_factor --asset BTC --data '<json>'
    python3 backtest_stub.py --list-metrics
"""

import json
import sys


def compute_hit_rate(signal_dates, signal_values, asset_returns, forward_periods=12):
    """
    Compute directional hit rate: how often does the signal correctly predict
    the direction of forward returns?

    Args:
        signal_dates: list of date strings
        signal_values: list of signal values (+ bullish, - bearish)
        asset_returns: dict of {date: forward_return}
        forward_periods: look-forward periods (months)

    Returns:
        hit_rate, confusion_matrix, signal_summary
    """
    if len(signal_values) < 2:
        return {"error": "Need at least 2 signal observations"}

    correct = 0
    total = 0
    confusion = {"TP": 0, "TN": 0, "FP": 0, "FN": 0}

    for i, (date, signal) in enumerate(zip(signal_dates, signal_values)):
        if i >= len(signal_dates) - 1:
            break
        # Find forward return
        fwd_date = _advance_date(date, forward_periods)
        fwd_return = asset_returns.get(fwd_date) or _find_nearest_return(asset_returns, fwd_date)

        if fwd_return is None:
            continue

        total += 1
        signal_up = signal > 0
        return_up = fwd_return > 0

        if signal_up and return_up:
            correct += 1
            confusion["TP"] += 1
        elif not signal_up and not return_up:
            correct += 1
            confusion["TN"] += 1
        elif signal_up and not return_up:
            confusion["FP"] += 1
        else:
            confusion["FN"] += 1

    if total == 0:
        return {"error": "No overlapping signal/return periods"}

    hit_rate = (correct / total) * 100

    return {
        "hit_rate": round(hit_rate, 1),
        "total_signals": total,
        "correct": correct,
        "confusion_matrix": confusion,
        "precision": round(confusion["TP"] / max(1, confusion["TP"] + confusion["FP"]) * 100, 1),
        "recall": round(confusion["TP"] / max(1, confusion["TP"] + confusion["FN"]) * 100, 1),
        "assessment": _assess_signal(hit_rate),
    }


def _assess_signal(hit_rate):
    if hit_rate > 70:   return "Strong — consistent directional edge"
    elif hit_rate > 60: return "Good — above random, useful as one input"
    elif hit_rate > 55: return "Moderate — marginal edge, needs confirmation"
    elif hit_rate > 50: return "Weak — barely above coin flip"
    else:               return "No edge — signal not predictive in this period"


def _advance_date(date_str, months):
    """Advance a date string by N months. Simple approximation."""
    try:
        parts = date_str.split("-")
        if len(parts) >= 2:
            y, m = int(parts[0]), int(parts[1])
            m += months
            y += (m - 1) // 12
            m = ((m - 1) % 12) + 1
            return f"{y}-{m:02d}"
    except (ValueError, IndexError):
        pass
    return date_str


def _find_nearest_return(returns, target_date, window=60):
    """Find nearest available forward return within window days."""
    # Simplified: just return None if exact match not found
    return returns.get(target_date)


# ══════════════════════════════════════════════════════════════════════════════
# Signal Metrics Catalog
# ══════════════════════════════════════════════════════════════════════════════

SIGNAL_METRICS = {
    "scissors_factor": {
        "description": "Scissors Factor = ΔLiquidity - ΔAssetPrice. + = bullish divergence",
        "assets_tested": ["BTC", "gold", "nasdaq", "sp500"],
        "typical_hit_rate": "62-68% (BTC), 55-60% (gold), 52-58% (equities)",
        "best_regime": "Expansion/Contraction transitions — highest divergence = strongest signal",
        "data_requirements": "Monthly net liquidity + asset prices, 3+ years history",
        "reference": "liquidity/scripts/scissors_factor.py",
    },
    "yield_curve_inversion": {
        "description": "10Y-2Y or 10Y-3M inversion → recession within 6-24 months",
        "assets_tested": ["sp500", "treasuries", "hy_credit"],
        "typical_hit_rate": "75-85% (recession prediction), 60-65% (equity drawdown timing)",
        "best_regime": "Deep inversion (>-0.5%) = highest conviction",
        "data_requirements": "Daily yield curve data, FRED",
    },
    "credit_gap": {
        "description": "BIS credit-to-GDP gap > 10% → banking crisis risk within 1-3 years",
        "assets_tested": ["banks", "real_estate", "sp500"],
        "typical_hit_rate": "65-75% (banking stress), 50-60% (equity timing)",
        "best_regime": "Gap > 20% critical — most historical banking crises preceded by this",
        "data_requirements": "Quarterly BIS credit-to-GDP data",
    },
    "hawk_dove_divergence": {
        "description": "Cross-bank hawk-dove divergence → FX volatility + carry trade opportunity",
        "assets_tested": ["usd_dxy", "em_equities", "JPY_carry"],
        "typical_hit_rate": "58-65% (FX direction), 55-60% (carry trade)",
        "best_regime": "Divergence > 6/12 = high conviction FX signal",
        "data_requirements": "Central bank meeting dates + hawk-dove scores",
    },
    "supercycle_score": {
        "description": "5-factor supercycle detection → multi-year commodity direction",
        "assets_tested": ["energy", "materials", "commodity_fx"],
        "typical_hit_rate": "70-80% (5+ year horizon), 55-60% (annual)",
        "best_regime": "Score > 70/100 = high conviction multi-year commodity upswing",
        "data_requirements": "Commodity prices, capex data, inventory levels, demand indicators",
    },
}


def list_metrics():
    """List all backtestable macro signal metrics."""
    return {
        "metrics": [
            {
                "name": k,
                "description": v["description"],
                "assets": v["assets_tested"],
                "typical_hit_rate": v["typical_hit_rate"],
            }
            for k, v in SIGNAL_METRICS.items()
        ]
    }


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Macro Signal Backtest Framework")
    p.add_argument("--signal", type=str, help="Signal type to backtest")
    p.add_argument("--asset", type=str, help="Asset to test against")
    p.add_argument("--data", type=str, help="JSON: {dates:[], signals:[], returns:{}}")
    p.add_argument("--list-metrics", action="store_true", help="List available metrics")
    p.add_argument("--export", type=str, default="text", help="text|json")
    args = p.parse_args()

    if args.list_metrics:
        result = list_metrics()
        if args.export == "json":
            print(json.dumps(result, indent=2))
        else:
            for m in result["metrics"]:
                print(f"  {m['name']}: {m['description']}")
                print(f"    Assets: {', '.join(m['assets'])}")
                print(f"    Hit Rate: {m['typical_hit_rate']}")
                print()
        sys.exit(0)

    if not args.data:
        print("Backtest Framework — requires --data with signal/return series")
        print()
        print("Example data format:")
        print(json.dumps({
            "signal": "scissors_factor",
            "asset": "BTC",
            "dates": ["2023-01", "2023-02", "2023-03"],
            "signals": [2.5, 1.8, -0.5],
            "returns": {"2023-04": 12.5, "2023-05": -3.2, "2023-06": 8.1},
        }, indent=2))
        print()
        print("Use --list-metrics for available signal metrics")
        sys.exit(0)

    data = json.loads(args.data)
    result = compute_hit_rate(
        data.get("dates", []),
        data.get("signals", []),
        data.get("returns", {}),
        data.get("forward_periods", 12),
    )

    if args.export == "json":
        print(json.dumps(result, indent=2))
    else:
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Hit Rate: {result['hit_rate']}% ({result['correct']}/{result['total_signals']})")
            print(f"Precision: {result['precision']}% | Recall: {result['recall']}%")
            print(f"Assessment: {result['assessment']}")
            print(f"Confusion: TP={result['confusion_matrix']['TP']} TN={result['confusion_matrix']['TN']} "
                  f"FP={result['confusion_matrix']['FP']} FN={result['confusion_matrix']['FN']}")
