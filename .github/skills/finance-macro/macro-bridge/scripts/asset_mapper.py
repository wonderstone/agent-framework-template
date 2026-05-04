#!/usr/bin/env python3
"""
Asset Mapper — Sector Impact → ETF/Fund Allocation

Translates macro-bridge sector impact rankings into concrete asset allocation
signals. Maps sectors to liquid ETFs, generates allocation tilts, and produces
a portfolio-level summary.

The final link in the chain: Macro Event → Transmission → Sector Impact → ETF Allocation

Usage:
    python3 asset_mapper.py --scenario fed-tightening
    python3 asset_mapper.py --sectors '{"energy":5.0,"technology":-4.0,...}'
"""

import json
import sys

# Sector → ETF mapping (liquid, low-cost, US-listed)
SECTOR_ETFS = {
    "technology":     {"ticker": "XLK", "name": "Technology Select Sector SPDR", "fee": 0.09},
    "banks":          {"ticker": "XLF", "name": "Financial Select Sector SPDR", "fee": 0.09},
    "real_estate":    {"ticker": "XLRE", "name": "Real Estate Select Sector SPDR", "fee": 0.09},
    "energy":         {"ticker": "XLE", "name": "Energy Select Sector SPDR", "fee": 0.09},
    "consumer_disc":  {"ticker": "XLY", "name": "Consumer Discretionary SPDR", "fee": 0.09},
    "consumer_staple":{"ticker": "XLP", "name": "Consumer Staples SPDR", "fee": 0.09},
    "healthcare":     {"ticker": "XLV", "name": "Health Care Select Sector SPDR", "fee": 0.09},
    "industrials":    {"ticker": "XLI", "name": "Industrial Select Sector SPDR", "fee": 0.09},
    "materials":      {"ticker": "XLB", "name": "Materials Select Sector SPDR", "fee": 0.09},
    "utilities":      {"ticker": "XLU", "name": "Utilities Select Sector SPDR", "fee": 0.09},
    "gold_miners":    {"ticker": "GDX", "name": "VanEck Gold Miners ETF", "fee": 0.51},
    "crypto":         {"ticker": "IBIT", "name": "iShares Bitcoin Trust", "fee": 0.25},
}

ASSET_ETFS = {
    "BTC":          {"ticker": "IBIT", "name": "iShares Bitcoin Trust", "fee": 0.25},
    "gold":         {"ticker": "GLD", "name": "SPDR Gold Shares", "fee": 0.40},
    "nasdaq":       {"ticker": "QQQ", "name": "Invesco QQQ Trust", "fee": 0.20},
    "sp500":        {"ticker": "SPY", "name": "SPDR S&P 500 ETF", "fee": 0.09},
    "usd_dxy":      {"ticker": "UUP", "name": "Invesco DB USD Index Bullish", "fee": 0.77},
    "em_equities":  {"ticker": "EEM", "name": "iShares MSCI Emerging Markets", "fee": 0.69},
    "hy_credit":    {"ticker": "HYG", "name": "iShares iBoxx High Yield Corp Bond", "fee": 0.49},
    "treasuries":   {"ticker": "TLT", "name": "iShares 20+ Year Treasury Bond", "fee": 0.15},
}

# Country-specific ETFs (for scenario country analysis)
COUNTRY_ETFS = {
    "AUS": {"ticker": "EWA", "name": "iShares MSCI Australia", "fee": 0.50},
    "JPN": {"ticker": "EWJ", "name": "iShares MSCI Japan", "fee": 0.50},
    "CHN": {"ticker": "FXI", "name": "iShares China Large-Cap", "fee": 0.74},
    "NZL": {"ticker": "ENZL", "name": "iShares MSCI New Zealand", "fee": 0.50},
    "USA": {"ticker": "SPY", "name": "SPDR S&P 500 ETF", "fee": 0.09},
}


def map_to_etfs(sector_impacts, asset_impacts=None, country=None):
    """
    Convert sector/asset impact scores to ETF allocation signals.

    Returns allocation recommendations with tilt weights.
    """
    etf_signals = []

    # Sector ETFs
    for item in sector_impacts:
        sector = item.get("sector", "")
        impact = item.get("total_impact", 0)
        etf = SECTOR_ETFS.get(sector)
        if etf:
            etf_signals.append({
                "etf": etf["ticker"],
                "name": etf["name"],
                "category": "sector",
                "sector": sector,
                "impact_score": impact,
                "signal": _tilt_signal(impact),
            })

    # Asset ETFs
    if asset_impacts:
        for item in asset_impacts:
            asset = item.get("asset", "")
            impact = item.get("total_impact", 0)
            etf = ASSET_ETFS.get(asset)
            if etf:
                etf_signals.append({
                    "etf": etf["ticker"],
                    "name": etf["name"],
                    "category": "asset",
                    "asset": asset,
                    "impact_score": impact,
                    "signal": _tilt_signal(impact),
                })

    # Country ETF
    country_etf = None
    if country and country in COUNTRY_ETFS:
        ce = COUNTRY_ETFS[country]
        country_etf = {"ticker": ce["ticker"], "name": ce["name"]}

    # Deduplicate by ETF ticker (keep strongest signal)
    seen = set()
    deduped = []
    for e in sorted(etf_signals, key=lambda x: abs(x["impact_score"]), reverse=True):
        if e["etf"] not in seen:
            deduped.append(e)
            seen.add(e["etf"])
    etf_signals = deduped

    # Generate allocation tilts
    overweights = [e for e in etf_signals if e["signal"] == "Overweight"]
    underweights = [e for e in etf_signals if e["signal"] == "Underweight"]
    neutrals = [e for e in etf_signals if e["signal"] == "Neutral"]

    return {
        "allocation": {
            "overweight": overweights,
            "underweight": underweights,
            "neutral": neutrals,
        },
        "country_etf": country_etf,
        "summary": _generate_summary(overweights, underweights, country),
        "full_ranking": etf_signals,
    }


def _tilt_signal(impact):
    if impact > 2:       return "Overweight"
    elif impact > 0.5:   return "Overweight"
    elif impact > -0.5:  return "Neutral"
    elif impact > -2:    return "Underweight"
    else:                return "Underweight"


def _generate_summary(overweights, underweights, country):
    ow_names = [f"{e['etf']} ({e.get('sector', e.get('asset', ''))})" for e in overweights[:5]]
    uw_names = [f"{e['etf']} ({e.get('sector', e.get('asset', ''))})" for e in underweights[:5]]

    lines = []
    if ow_names:
        lines.append(f"Overweight: {', '.join(ow_names)}")
    if uw_names:
        lines.append(f"Underweight: {', '.join(uw_names)}")
    if country:
        lines.append(f"Country ETF: {country}")

    return "; ".join(lines) if lines else "No clear tilts — stay market weight"


def format_portfolio(allocation, fmt="text"):
    """Format allocation as markdown table or JSON."""
    if fmt == "json":
        return json.dumps(allocation, indent=2, default=str)

    lines = ["## ETF Allocation Signals", ""]
    lines.append(f"**Summary:** {allocation['summary']}")
    lines.append("")

    lines.append("| Signal | ETF | Name | Category | Impact |")
    lines.append("|--------|-----|------|----------|--------|")
    for e in allocation["full_ranking"]:
        emoji = "🟢" if e["signal"] == "Overweight" else ("🟠" if e["signal"] == "Underweight" else "⚪")
        lines.append(f"| {emoji} {e['signal']} | {e['etf']} | {e['name']} | {e['category']} | {e['impact_score']:+.1f} |")
    lines.append("")

    if allocation["country_etf"]:
        ce = allocation["country_etf"]
        lines.append(f"**Country ETF:** {ce['ticker']} — {ce['name']}")
        lines.append("")

    # Risk notes
    lines.append("### Risk Notes")
    extreme = [e for e in allocation["full_ranking"] if abs(e["impact_score"]) > 5]
    if extreme:
        for e in extreme:
            lines.append(f"- {e['etf']}: impact {e['impact_score']:+.1f} — extreme tilt, size accordingly")
    lines.append("- ETF fees impact long-term returns; consider fee differentials for strategic allocations")
    lines.append("- Sector ETFs assume US equity exposure; adjust for home-country bias")

    return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Macro → ETF Allocation Mapper")
    p.add_argument("--scenario", type=str, help="Pre-built macro scenario")
    p.add_argument("--sectors", type=str, help='JSON sector impacts: \'{"energy":5,"tech":-4}\'')
    p.add_argument("--country", type=str, help="Country for country-specific ETF")
    p.add_argument("--export", type=str, default="text", help="text|markdown|json")
    args = p.parse_args()

    sector_impacts = []
    asset_impacts = None

    if args.scenario:
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from stress_test import run_stress_test
        report = run_stress_test(scenario=args.scenario, country=args.country)
        if "error" in report:
            print(json.dumps(report))
            sys.exit(1)
        sector_impacts = report["sector_impact"]["full_ranking"]
        asset_impacts = report["asset_impact"]["full_ranking"]
    elif args.sectors:
        data = json.loads(args.sectors)
        if isinstance(data, dict):
            sector_impacts = [{"sector": k, "total_impact": v} for k, v in data.items()]
        else:
            sector_impacts = data

    if not sector_impacts:
        print("Error: provide --scenario or --sectors")
        sys.exit(1)

    allocation = map_to_etfs(sector_impacts, asset_impacts, args.country)

    if args.export == "json":
        print(format_portfolio(allocation, "json"))
    else:
        print(format_portfolio(allocation, "markdown"))
