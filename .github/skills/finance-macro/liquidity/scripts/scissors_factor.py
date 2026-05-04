#!/usr/bin/env python3
"""
Scissors Factor Calculator.

Methodology: Liquidity YoY% - Asset Price YoY%
  SF > 0 → Liquidity growing faster than asset price → Bullish signal
  SF < 0 → Asset price outrunning liquidity → Bearish divergence

Three-component weighted signal:
  - Regime (50%): Is net liquidity expanding or contracting?
  - Threshold (30%): Is SF above/below key thresholds?
  - Momentum (20%): Is SF accelerating or decelerating?

Usage:
    python3 scissors_factor.py --assets BTC-USD,GC=F,^IXIC
    python3 scissors_factor.py --all
"""

import json
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "mcp-servers" / "fred-mcp"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from net_liquidity import fetch_liquidity_components, calculate_net_liquidity
except ImportError:
    def calculate_net_liquidity(*a, **kw): return []

DEFAULT_ASSETS = {
    "BTC-USD": {"name": "Bitcoin", "type": "crypto"},
    "GC=F": {"name": "Gold", "type": "commodity"},
    "^IXIC": {"name": "Nasdaq", "type": "equity"},
    "DX-Y.NYB": {"name": "US Dollar Index", "type": "fx"},
    "^GSPC": {"name": "S&P 500", "type": "equity"},
}


def get_asset_price_yoy(symbol, months=12):
    """Get YoY price change for an asset using Yahoo Finance."""
    try:
        import yfinance as yf
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=f"{months+1}mo")
        if len(hist) < 2:
            return None
        latest = hist["Close"].iloc[-1]
        year_ago = hist["Close"].iloc[0]
        return ((latest - year_ago) / year_ago) * 100
    except ImportError:
        return None
    except Exception as e:
        print(f"[WARN] Failed to get {symbol}: {e}", file=sys.stderr)
        return None


def calculate_scissors_factor(liquidity_yoy, asset_yoy):
    """SF = Liquidity_YoY% - AssetPrice_YoY%"""
    if liquidity_yoy is None or asset_yoy is None:
        return None
    return liquidity_yoy - asset_yoy


def classify_regime(sf_value):
    """Classify the scissors factor reading."""
    if sf_value is None:
        return "Unknown"
    if sf_value > 5:
        return "Strong Bullish (Liquidity leading)"
    elif sf_value > 0:
        return "Bullish"
    elif sf_value > -5:
        return "Bearish Divergence"
    elif sf_value > -10:
        return "Bearish"
    else:
        return "Strong Bearish (Liquidity collapsing)"


def weighted_signal(sf_value, sf_prev=None, liquidity_yoy=None):
    """
    Three-component weighted signal:
    - Regime (50%): Direction and magnitude of SF
    - Threshold (30%): SF above/below ±5% thresholds
    - Momentum (20%): SF acceleration/deceleration vs prior period
    """
    if sf_value is None:
        return {"signal": "Unknown", "score": 0}

    # Regime component (50%)
    if sf_value > 5:
        regime_score = 1.0
    elif sf_value > 0:
        regime_score = 0.6
    elif sf_value > -5:
        regime_score = 0.3
    elif sf_value > -10:
        regime_score = 0.1
    else:
        regime_score = 0.0
    regime = regime_score * 0.5

    # Threshold component (30%)
    if sf_value > 10:
        threshold_score = 1.0
    elif sf_value > 5:
        threshold_score = 0.8
    elif sf_value > 0:
        threshold_score = 0.5
    elif sf_value > -5:
        threshold_score = 0.3
    else:
        threshold_score = 0.0
    threshold = threshold_score * 0.3

    # Momentum component (20%)
    if sf_prev is not None:
        delta = sf_value - sf_prev
        if delta > 3:
            momentum_score = 1.0
        elif delta > 0:
            momentum_score = 0.7
        elif delta > -3:
            momentum_score = 0.3
        else:
            momentum_score = 0.0
    else:
        momentum_score = 0.5  # neutral if no history
    momentum = momentum_score * 0.2

    total = regime + threshold + momentum
    if total > 0.7:
        signal = "Strong Buy"
    elif total > 0.5:
        signal = "Buy"
    elif total > 0.35:
        signal = "Hold / Neutral"
    elif total > 0.2:
        signal = "Reduce"
    else:
        signal = "Sell / Avoid"

    return {"signal": signal, "score": round(total, 3), "components": {"regime": regime, "threshold": threshold, "momentum": momentum}}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Calculate Scissors Factor for assets")
    parser.add_argument("--assets", type=str, help="Comma-separated asset symbols")
    parser.add_argument("--all", action="store_true", help="Calculate for all default assets")
    parser.add_argument("--export", type=str, default="text", help="text|json")
    args = parser.parse_args()

    # Get liquidity data
    components = fetch_liquidity_components(12)
    nl_data = calculate_net_liquidity(components)
    net_liquidity_yoy = None
    if len(nl_data) >= 52:
        latest_year = [d["NetLiquidity"] for d in nl_data[-52:]]
        if len(latest_year) >= 2:
            net_liquidity_yoy = ((latest_year[-1] - latest_year[0]) / abs(latest_year[0])) * 100

    assets = list(DEFAULT_ASSETS.keys()) if args.all else (
        args.assets.split(",") if args.assets else list(DEFAULT_ASSETS.keys())[:3]
    )

    results = []
    for symbol in assets:
        asset_info = DEFAULT_ASSETS.get(symbol, {"name": symbol, "type": "unknown"})
        price_yoy = get_asset_price_yoy(symbol)
        sf = calculate_scissors_factor(net_liquidity_yoy, price_yoy)
        regime = classify_regime(sf)
        signal = weighted_signal(sf)

        result = {
            "symbol": symbol,
            "name": asset_info["name"],
            "type": asset_info["type"],
            "liquidity_yoy_pct": round(net_liquidity_yoy, 2) if net_liquidity_yoy else None,
            "price_yoy_pct": round(price_yoy, 2) if price_yoy else None,
            "scissors_factor": round(sf, 2) if sf else None,
            "regime": regime,
            "signal": signal,
        }
        results.append(result)

    if args.export == "json":
        print(json.dumps(results, indent=2, default=str))
    else:
        print(f"Scissors Factor Analysis")
        print(f"{'─' * 60}")
        print(f"Net Liquidity YoY: {net_liquidity_yoy:+.1f}%" if net_liquidity_yoy else "Net Liquidity YoY: N/A")
        print()
        print(f"{'Asset':<15} {'Price YoY':<12} {'SF':<10} {'Regime':<30} {'Signal':<15}")
        print("-" * 82)
        for r in results:
            price = f"{r['price_yoy_pct']:+.1f}%" if r['price_yoy_pct'] else "N/A"
            sf = f"{r['scissors_factor']:+.1f}" if r['scissors_factor'] else "N/A"
            print(f"{r['name']:<15} {price:<12} {sf:<10} {r['regime']:<30} {r['signal']['signal']:<15}")
