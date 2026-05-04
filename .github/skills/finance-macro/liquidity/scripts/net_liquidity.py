#!/usr/bin/env python3
"""Calculate US net liquidity: WALCL - TGA - RRPONTSYD.

Usage:
    python3 net_liquidity.py --latest     # latest observation only
    python3 net_liquidity.py --months 12   # last 12 months
    python3 net_liquidity.py --export json # JSON output for consumption
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "mcp-servers" / "fred-mcp"))

try:
    from cache_manager import get as cache_get, set as cache_set
    HAS_CACHE = True
except ImportError:
    HAS_CACHE = False

# Import FRED MCP as local module
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "mcp-servers" / "fred-mcp"))
try:
    from server import get_series as fred_get_series
except ImportError:
    # Fallback: use subprocess
    import subprocess
    def fred_get_series(series_id, **kwargs):
        args = json.dumps({"series_id": series_id, **kwargs})
        cmd = ["python3", str(Path(__file__).resolve().parent.parent.parent / "mcp-servers" / "fred-mcp" / "server.py"), "get_series", args]
        r = subprocess.run(cmd, capture_output=True, text=True)
        return json.loads(r.stdout)


def fetch_liquidity_components(months=12):
    """Fetch WALCL, TGA, RRPONTSYD and calculate net liquidity."""
    components = {
        "WALCL": {"name": "Fed Total Assets", "frequency": "w"},
        "TGA": {"name": "Treasury General Account", "frequency": "d"},
        "RRPONTSYD": {"name": "Overnight Reverse Repo", "frequency": "d"},
    }

    results = {}
    for series_id, info in components.items():
        cache_key = f"{series_id}_{months}m"
        if HAS_CACHE:
            cached = cache_get("fred", cache_key)
            if cached:
                results[series_id] = cached
                continue

        data = fred_get_series(series_id, limit=months * 5, sort_order="desc")
        if "error" in data:
            print(f"[WARN] Failed to fetch {series_id}: {data['error']}", file=sys.stderr)
            results[series_id] = {"observations": [], "name": info["name"]}
            continue

        results[series_id] = {
            "name": info["name"],
            "observations": data.get("observations", []),
        }

        if HAS_CACHE:
            cache_set("fred", cache_key, results[series_id])

    return results


def calculate_net_liquidity(components):
    """Align dates and calculate Net Liquidity = WALCL - TGA - RRP."""
    walcl = {o["date"]: float(o["value"]) for o in components.get("WALCL", {}).get("observations", []) if o["value"] != "."}
    tga = {o["date"]: float(o["value"]) for o in components.get("TGA", {}).get("observations", []) if o["value"] != "."}
    rrp = {o["date"]: float(o["value"]) for o in components.get("RRPONTSYD", {}).get("observations", []) if o["value"] != "."}

    # Use WALCL dates as anchor (weekly, most meaningful)
    results = []
    for date in sorted(walcl.keys(), reverse=True):
        walcl_val = walcl.get(date)
        # Find nearest TGA and RRP to WALCL date
        tga_val = tga.get(date, _nearest_date(tga, date))
        rrp_val = rrp.get(date, _nearest_date(rrp, date))

        if walcl_val and tga_val is not None and rrp_val is not None:
            net_liq = walcl_val - tga_val - rrp_val
            results.append({
                "date": date,
                "WALCL": walcl_val,
                "TGA": tga_val,
                "RRP": rrp_val,
                "NetLiquidity": net_liq,
            })

        if len(results) >= 52:  # cap at ~1 year weekly
            break

    # Sort ascending for trend display
    results.reverse()
    return results


def _nearest_date(data_dict, target_date):
    """Find value for date closest to target."""
    if not data_dict:
        return None
    dates = sorted(data_dict.keys())
    # Return exact match or nearest
    if target_date in data_dict:
        return data_dict[target_date]
    # Binary search for nearest
    import bisect
    idx = bisect.bisect_left(dates, target_date)
    if idx == 0:
        return data_dict[dates[0]]
    if idx >= len(dates):
        return data_dict[dates[-1]]
    # Return closer of two neighbors
    return data_dict[dates[idx]]


def calculate_yoy_change(data):
    """Calculate year-over-year change for the latest observation vs 52 weeks ago."""
    if len(data) < 2:
        return None
    latest = data[-1]["NetLiquidity"]
    # Find ~1 year ago
    year_ago = None
    target_date = datetime.strptime(data[-1]["date"], "%Y-%m-%d")
    from datetime import timedelta
    threshold = target_date - timedelta(days=365)
    for d in data:
        dt = datetime.strptime(d["date"], "%Y-%m-%d")
        if dt >= threshold:
            year_ago = d["NetLiquidity"]
            break
    if year_ago:
        return ((latest - year_ago) / abs(year_ago)) * 100
    return None


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Calculate US Net Liquidity")
    parser.add_argument("--latest", action="store_true", help="Only latest observation")
    parser.add_argument("--months", type=int, default=12, help="Months of data")
    parser.add_argument("--export", type=str, default="text", help="Output format: text|json")
    args = parser.parse_args()

    components = fetch_liquidity_components(args.months)
    data = calculate_net_liquidity(components)
    yoy = calculate_yoy_change(data)

    if args.export == "json":
        output = {
            "latest": data[-1] if data else None,
            "yoy_change_pct": yoy,
            "series": data,
        }
        print(json.dumps(output, indent=2, default=str))
    else:
        if not data:
            print("No data available")
            sys.exit(1)

        latest = data[-1]
        print(f"Net Liquidity Dashboard (as of {latest['date']})")
        print(f"{'─' * 50}")
        print(f"Fed Total Assets (WALCL):  ${latest['WALCL'] / 1_000_000_000:,.1f}B")
        print(f"Treasury General Account:   ${latest['TGA'] / 1_000_000_000:,.1f}B")
        print(f"Overnight Reverse Repo:     ${latest['RRP'] / 1_000_000_000:,.1f}B")
        print(f"{'─' * 50}")
        print(f"Net Liquidity:              ${latest['NetLiquidity'] / 1_000_000_000:,.1f}B")

        if yoy is not None:
            direction = "↑" if yoy > 0 else "↓"
            print(f"YoY Change:                 {direction} {abs(yoy):.1f}%")

        # Trend
        if len(data) >= 12:
            recent = sum(d["NetLiquidity"] for d in data[-4:]) / 4
            prior = sum(d["NetLiquidity"] for d in data[-12:-4]) / 8
            trend = (recent - prior) / abs(prior) * 100
            direction = "Expanding" if trend > 0 else "Contracting"
            print(f"3-Month Trend:              {direction} ({trend:+.1f}%)")
