#!/usr/bin/env python3
"""
MCP Server: Bank for International Settlements (BIS) Statistics

Provides international banking, debt, credit gap, and property price statistics.
No API key required. Data via BIS SDMX REST API at stats.bis.org.

Key datasets:
  - WS_CREDIT_GAP: Credit-to-GDP gaps (early warning indicator for banking crises)
  - WS_SPP: Selected residential property prices
  - WS_TC: Total credit to non-financial sector
  - WS_DSR: Debt service ratios

Tools exposed:
  - get_credit_gap: fetch credit-to-GDP gap for a country
  - get_property_prices: fetch residential property price index
  - get_total_credit: fetch total credit statistics

Usage: python3 server.py <tool> '<json_arguments>'
"""

import csv
import io
import json
import sys
import urllib.error
import urllib.request

BIS_BASE = "https://stats.bis.org/api/v1"

DATAFLOWS = {
    "credit_gap": "WS_CREDIT_GAP",
    "property_prices": "WS_SPP",
    "total_credit": "WS_TC",
    "debt_service": "WS_DSR",
    "commercial_property": "WS_CPP",
}


def _bis_csv(url, timeout=30):
    """Fetch BIS CSV data."""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "AgentTools-Macro/1.0",
            "Accept": "text/csv",
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return [row for row in csv.DictReader(io.StringIO(resp.read().decode()))]
    except urllib.error.HTTPError as e:
        return [{"error": f"HTTP {e.code}: {e.reason}"}]
    except urllib.error.URLError as e:
        return [{"error": f"Connection error: {e.reason}"}]
    except Exception as e:
        return [{"error": str(e)}]


def get_credit_gap(country="US", limit=40):
    """
    Fetch credit-to-GDP gap data (BIS early warning indicator).

    Gap > 10% = elevated banking crisis risk within 1-3 years.
    Gap > 20% = critical warning level.

    Args:
        country: ISO 3166-1 alpha-2 code (US, CN, JP, DE, GB, NZ, AU, etc.)
        limit: max observations to return
    """
    # Key dimensions: FREQ.BORROWERS_CTY.TC_BORROWERS.TC_LENDERS.CG_DTYPE
    # P = Private non-financial sector, A = All sectors, E = End-of-period ratio
    country = country.upper()
    key = f"Q.{country}.P.A.A.E"
    url = f"{BIS_BASE}/data/BIS,WS_CREDIT_GAP,1.0/{key}/all?format=csv"

    rows = _bis_csv(url)
    if rows and "error" in rows[0]:
        return rows[0]

    if not rows:
        return {"error": f"No credit gap data for {country}", "url": url}

    observations = []
    for r in rows[-limit:]:
        try:
            observations.append({
                "date": r.get("TIME_PERIOD", ""),
                "value": float(r.get("OBS_VALUE", 0)),
            })
        except (ValueError, TypeError):
            pass

    return {
        "country": country,
        "indicator": "Credit-to-GDP Ratio (Private Non-Financial Sector)",
        "description": "Total credit to private non-financial sector as % of GDP. Gap = deviation from long-term trend (BIS uses HP filter). Credit/GDP > 100% is common in advanced economies.",
        "threshold": {"dm_avg": 120, "high": 160, "critical": 200},
        "count": len(observations),
        "observations": observations,
    }


def get_property_prices(country="US", limit=40):
    """
    Fetch selected residential property price index from BIS.

    Args:
        country: ISO 3166-1 alpha-2 code
        limit: max observations
    """
    country = country.upper()
    key = f"Q.{country}.N.628"
    url = f"{BIS_BASE}/data/BIS,WS_SPP,1.0/{key}/all?format=csv"

    rows = _bis_csv(url)
    if rows and "error" in rows[0]:
        return rows[0]

    if not rows:
        return {"error": f"No property price data for {country}", "url": url}

    observations = []
    for r in rows[-limit:]:
        try:
            observations.append({
                "date": r.get("TIME_PERIOD", ""),
                "value": float(r.get("OBS_VALUE", 0)),
            })
        except (ValueError, TypeError):
            pass

    return {
        "country": country,
        "indicator": "Residential Property Prices (Selected Series)",
        "source": "BIS",
        "count": len(observations),
        "observations": observations,
    }


def get_total_credit(country="US", sector="P", limit=20):
    """
    Fetch total credit to non-financial sector.

    Args:
        country: ISO 3166-1 alpha-2 code
        sector: P (Private), G (Government), A (All)
        limit: max observations
    """
    country = country.upper()
    key = f"Q.{country}.{sector}.A.770"
    url = f"{BIS_BASE}/data/BIS,WS_TC,1.0/{key}/all?format=csv"

    rows = _bis_csv(url)
    if rows and "error" in rows[0]:
        return rows[0]

    if not rows:
        return {"error": f"No total credit data for {country}", "url": url}

    observations = []
    for r in rows[-limit:]:
        try:
            observations.append({
                "date": r.get("TIME_PERIOD", ""),
                "value": float(r.get("OBS_VALUE", 0)),
            })
        except (ValueError, TypeError):
            pass

    sector_label = {"P": "Private non-financial", "G": "Government", "A": "All sectors"}
    return {
        "country": country,
        "indicator": f"Total Credit ({sector_label.get(sector, sector)})",
        "source": "BIS",
        "count": len(observations),
        "observations": observations,
    }


def list_dataflows():
    """List available BIS dataflows."""
    return {
        "dataflows": {
            "WS_CREDIT_GAP": "Credit-to-GDP gaps — early warning indicator for banking crises",
            "WS_SPP": "Selected residential property prices",
            "WS_CPP": "Commercial property prices",
            "WS_TC": "Total credit to the non-financial sector",
            "WS_DSR": "Debt service ratios for the private non-financial sector",
        },
        "base_url": BIS_BASE,
        "note": "No API key required. Use ISO 3166-1 alpha-2 country codes.",
    }


def handle_mcp_call(tool_name, arguments):
    tools = {
        "get_credit_gap": lambda: get_credit_gap(**arguments),
        "get_property_prices": lambda: get_property_prices(**arguments),
        "get_total_credit": lambda: get_total_credit(**arguments),
        "list_dataflows": lambda: list_dataflows(**arguments),
    }
    if tool_name not in tools:
        return {"error": f"Unknown tool: {tool_name}. Available: {list(tools.keys())}"}
    try:
        return tools[tool_name]()
    except TypeError as e:
        return {"error": f"Invalid arguments for {tool_name}: {e}"}
    except Exception as e:
        return {"error": f"Error calling {tool_name}: {e}"}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("BIS MCP Server for AgentTools Macro Skills")
        print("Data: Credit gaps, property prices, total credit, debt service ratios")
        print("Usage: python3 server.py <tool> '<json_arguments>'")
        print("Examples:")
        print('  python3 server.py get_credit_gap \'{"country":"NZ"}\'')
        print('  python3 server.py get_property_prices \'{"country":"US","limit":20}\'')
        print('  python3 server.py list_dataflows')
        sys.exit(1)

    tool = sys.argv[1]
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    result = handle_mcp_call(tool, args)
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
