#!/usr/bin/env python3
"""
MCP Server: World Bank API

Provides global development indicators for 200+ countries from the World Bank Data API.
No API key required for basic usage (free tier: 1,000 requests/day without key).

Tools exposed:
  - get_indicator: fetch indicator data for a country/countries
  - search_indicators: search World Bank indicators by keyword
  - get_country_list: list available countries with codes
  - get_indicator_info: get metadata for an indicator

Key Indicators Quick Reference:
  NY.GDP.MKTP.CD    → GDP (current USD)
  NY.GDP.MKTP.KD.ZG → GDP growth (annual %)
  NY.GDP.PCAP.CD    → GDP per capita (current USD)
  FP.CPI.TOTL.ZG    → Inflation, consumer prices (annual %)
  SL.UEM.TOTL.ZS    → Unemployment, total (% of labor force)
  NE.EXP.GNFS.ZS    → Exports of goods and services (% of GDP)
  NE.IMP.GNFS.ZS    → Imports of goods and services (% of GDP)
  GC.DOD.TOTL.GD.ZS → Central government debt (% of GDP)
  BN.CAB.XOKA.GD.ZS → Current account balance (% of GDP)
  BX.KLT.DINV.WD.GD.ZS → Foreign direct investment (% of GDP)
  SP.POP.TOTL       → Population, total
  NY.GSR.NFCY.CD    → Net income from abroad (current USD)
  PA.NUS.FCRF       → Official exchange rate (LCU per USD)
"""

import json
import sys
import urllib.request
import urllib.parse
import urllib.error

WB_BASE = "https://api.worldbank.org/v2"


def _wb_request(endpoint, params=None):
    """Make a World Bank API request."""
    base_params = {"format": "json", "per_page": 100}
    if params:
        base_params.update(params)

    url = f"{WB_BASE}/{endpoint}?{urllib.parse.urlencode(base_params)}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "MacroFinance-MCP/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            if isinstance(data, list) and len(data) > 1:
                return {"metadata": data[0], "data": data[1]}
            return data
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}"}
    except urllib.error.URLError as e:
        return {"error": f"Connection error: {e.reason}"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response"}


def get_indicator(indicator, country="all", date_range=None, per_page=50):
    """
    Fetch indicator data for given country/countries.

    Args:
        indicator: World Bank indicator code
        country: ISO 3166-1 alpha-3 code (e.g., 'NZL', 'USA', 'CHN') or 'all'
        date_range: '2010:2024' format for range, '2022' for single year
        per_page: results per page
    """
    params = {"per_page": str(per_page)}
    if date_range:
        params["date"] = date_range

    result = _wb_request(f"country/{country}/indicator/{indicator}", params)
    if "error" in result:
        return result

    if isinstance(result, dict) and "data" in result:
        observations = []
        for o in result["data"]:
            if o.get("value") is not None:
                observations.append({
                    "date": o.get("date", ""),
                    "value": float(o["value"]),
                    "country": o.get("country", {}).get("value", ""),
                    "country_code": o.get("countryiso3code", ""),
                })
        return {
            "indicator": indicator,
            "indicator_name": result["data"][0].get("indicator", {}).get("value", "") if result["data"] else "",
            "count": len(observations),
            "observations": observations,
        }

    return {"error": "Unexpected response format", "raw": result}


def search_indicators(search_text, limit=30):
    """Search World Bank indicators by keyword."""
    params = {"search": search_text, "per_page": str(limit)}
    result = _wb_request("indicator", params)
    if "error" in result:
        return result

    if isinstance(result, dict) and "data" in result:
        indicators = result.get("data", [])
        return {
            "search": search_text,
            "count": len(indicators),
            "results": [
                {
                    "id": i.get("id", ""),
                    "name": i.get("name", ""),
                    "source": i.get("source", {}).get("value", ""),
                }
                for i in indicators if i.get("id")
            ],
        }
    return {"error": "Unexpected response", "raw": result}


def get_country_list():
    """List all available countries with codes."""
    result = _wb_request("country", {"per_page": "300", "region": "WLD"})
    if isinstance(result, list) and len(result) > 1:
        countries = result[1]
        return {
            "count": len(countries),
            "countries": [
                {
                    "code": c.get("iso2Code", ""),
                    "name": c.get("name", ""),
                    "region": c.get("region", {}).get("value", ""),
                    "income_level": c.get("incomeLevel", {}).get("value", ""),
                }
                for c in countries
                if c.get("iso2Code") and c.get("region", {}).get("value") != "Aggregates"
            ],
        }
    return {"error": "Failed to fetch country list"}


def get_indicator_info(indicator):
    """Get metadata for a specific indicator."""
    params = {"per_page": "1"}
    result = _wb_request(f"indicator/{indicator}", params)
    if isinstance(result, dict) and "data" in result:
        data = result.get("data", [])
        if data:
            i = data[0]
            return {
                "id": i.get("id", ""),
                "name": i.get("name", ""),
                "source": i.get("source", {}).get("value", ""),
                "source_note": i.get("sourceNote", ""),
                "topics": [t.get("value", "") for t in i.get("topics", [])],
            }
    return {"error": f"Indicator {indicator} not found"}


def handle_mcp_call(tool_name, arguments):
    tools = {
        "get_indicator": lambda: get_indicator(**arguments),
        "search_indicators": lambda: search_indicators(**arguments),
        "get_country_list": lambda: get_country_list(**arguments),
        "get_indicator_info": lambda: get_indicator_info(**arguments),
    }
    if tool_name not in tools:
        return {"error": f"Unknown tool: {tool_name}"}
    try:
        return tools[tool_name]()
    except TypeError as e:
        return {"error": f"Invalid arguments: {e}"}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("World Bank MCP Server for Macro Finance Skills")
        print("Usage: python3 server.py <tool> <json_arguments>")
        print("Example: python3 server.py get_indicator '{\"indicator\": \"NY.GDP.MKTP.KD.ZG\", \"country\": \"NZL;USA;CHN\"}'")
        sys.exit(1)

    tool = sys.argv[1]
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    result = handle_mcp_call(tool, args)
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
