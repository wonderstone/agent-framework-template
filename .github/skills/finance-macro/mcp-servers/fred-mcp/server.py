#!/usr/bin/env python3
"""
MCP Server: Federal Reserve Economic Data (FRED)

Provides economic time series from the St. Louis Fed's FRED database.
Requires FRED_API_KEY environment variable (free from https://fred.stlouisfed.org/docs/api/api_key.html).

Tools exposed:
  - get_series: fetch observations for a FRED series
  - search_series: search FRED for series by keyword
  - get_series_info: get metadata for a series
  - get_category: list series within a FRED category

Key Series Quick Reference:
  GDP          → gdp/GDP         Real GDP
  GDPC1        → GDPC1          Real GDP (chained 2017 dollars)
  UNRATE       → UNRATE         Unemployment Rate
  CPIAUCSL     → CPIAUCSL       CPI All Urban Consumers
  PCEPI        → PCEPI          PCE Price Index
  FEDFUNDS     → FEDFUNDS       Federal Funds Rate
  M2SL         → M2SL           M2 Money Supply
  WALCL        → WALCL          Fed Total Assets
  TGA          → TGA            Treasury General Account
  RRPONTSYD    → RRPONTSYD      Overnight Reverse Repo
  DGS10        → DGS10           10-Year Treasury Yield
  DGS2         → DGS2            2-Year Treasury Yield
  T10Y2Y       → T10Y2Y         10Y-2Y Spread
  PAYEMS       → PAYEMS         Nonfarm Payrolls
  ICSA         → ICSA           Initial Jobless Claims
"""

import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

FRED_BASE = "https://api.stlouisfed.org/fred"

# Add parent scripts to path for shared imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
try:
    from env_setup import get_key, validate as env_validate
except ImportError:
    def get_key(k): return os.environ.get(k, "")
    def env_validate(**kw): return {"errors": [], "warnings": []}


def _get_api_key():
    return get_key("FRED_API_KEY")


def _fred_request(endpoint, params=None):
    """Make a FRED API request with error handling."""
    api_key = _get_api_key()
    if not api_key:
        return {"error": "FRED_API_KEY not set. Get one at https://fred.stlouisfed.org/docs/api/api_key.html"}

    base_params = {"api_key": api_key, "file_type": "json"}
    if params:
        base_params.update(params)

    url = f"{FRED_BASE}/{endpoint}?{urllib.parse.urlencode(base_params)}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "MacroFinance-MCP/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}", "url": url}
    except urllib.error.URLError as e:
        return {"error": f"Connection error: {e.reason}"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response from FRED"}


def get_series(series_id, observation_start=None, observation_end=None, sort_order="desc", limit=100, units=None, frequency=None):
    """
    Fetch observations for a FRED series.

    Args:
        series_id: FRED series ID (e.g., 'GDP', 'UNRATE', 'CPIAUCSL')
        observation_start: YYYY-MM-DD format
        observation_end: YYYY-MM-DD format
        sort_order: 'asc' or 'desc'
        limit: max observations to return
        units: 'lin' (levels), 'chg' (change), 'ch1' (percent change), 'pch' (percent change YoY), 'pc1' (percent change)
        frequency: 'd' (daily), 'w' (weekly), 'bw' (biweekly), 'm' (monthly), 'q' (quarterly), 'a' (annual)
    """
    params = {
        "series_id": series_id,
        "sort_order": sort_order,
        "limit": str(limit),
    }
    if observation_start:
        params["observation_start"] = observation_start
    if observation_end:
        params["observation_end"] = observation_end
    if units:
        params["units"] = units
    if frequency:
        params["frequency"] = frequency

    result = _fred_request("series/observations", params)
    if "error" in result:
        return result

    observations = result.get("observations", [])
    return {
        "series_id": series_id,
        "count": len(observations),
        "units": units or "lin",
        "observations": [
            {"date": o["date"], "value": o["value"]}
            for o in observations
            if o["value"] != "."
        ],
    }


def search_series(search_text, limit=20, order_by="search_rank"):
    """
    Search FRED for series by keyword or text.

    Args:
        search_text: search keywords
        limit: max results
        order_by: 'search_rank', 'popularity', 'title', 'units', 'frequency'
    """
    params = {"search_text": search_text, "limit": str(limit), "order_by": order_by}
    result = _fred_request("series/search", params)
    if "error" in result:
        return result

    series_list = result.get("seriess", [])
    return {
        "search": search_text,
        "count": len(series_list),
        "results": [
            {
                "id": s["id"],
                "title": s["title"],
                "frequency": s.get("frequency", ""),
                "units": s.get("units", ""),
                "popularity": s.get("popularity", 0),
                "observation_start": s.get("observation_start", ""),
                "observation_end": s.get("observation_end", ""),
            }
            for s in series_list
        ],
    }


def get_series_info(series_id):
    """Get metadata for a FRED series."""
    params = {"series_id": series_id}
    result = _fred_request("series", params)
    if "error" in result:
        return result

    series_list = result.get("seriess", [])
    if not series_list:
        return {"error": f"Series {series_id} not found"}

    s = series_list[0]
    return {
        "id": s["id"],
        "title": s["title"],
        "frequency": s.get("frequency", ""),
        "units": s.get("units", ""),
        "units_short": s.get("units_short", ""),
        "seasonal_adjustment": s.get("seasonal_adjustment", ""),
        "popularity": s.get("popularity", 0),
        "observation_start": s.get("observation_start", ""),
        "observation_end": s.get("observation_end", ""),
        "notes": s.get("notes", ""),
    }


def get_category(category_id=0, limit=50):
    """List series within a FRED category. category_id=0 returns root categories."""
    params = {"category_id": str(category_id), "limit": str(limit)}
    result = _fred_request("category/series", params)
    if "error" in result:
        return result

    series_list = result.get("seriess", [])
    return {
        "category_id": category_id,
        "count": len(series_list),
        "series": [
            {"id": s["id"], "title": s["title"]}
            for s in series_list
        ],
    }


# MCP-compatible dispatch
def handle_mcp_call(tool_name, arguments):
    """Dispatch MCP tool calls to the appropriate function."""
    tools = {
        "get_series": lambda: get_series(**arguments),
        "search_series": lambda: search_series(**arguments),
        "get_series_info": lambda: get_series_info(**arguments),
        "get_category": lambda: get_category(**arguments),
    }

    if tool_name not in tools:
        return {"error": f"Unknown tool: {tool_name}. Available: {list(tools.keys())}"}

    try:
        result = tools[tool_name]()
        return result
    except TypeError as e:
        return {"error": f"Invalid arguments for {tool_name}: {e}"}
    except Exception as e:
        return {"error": f"Error calling {tool_name}: {e}"}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("FRED MCP Server for Macro Finance Skills")
        print("Usage: python3 server.py <tool> <json_arguments>")
        print("Example: python3 server.py get_series '{\"series_id\": \"GDP\", \"limit\": 10}'")
        sys.exit(1)

    tool = sys.argv[1]
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    result = handle_mcp_call(tool, args)
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
