#!/usr/bin/env python3
"""
MCP Server: IMF Data API (SDMX 3.0)

Provides macroeconomic data from the International Monetary Fund.
Registration required at https://data.imf.org/ (free).

IMPORTANT: The old IMF API at dataservices.imf.org was DECOMMISSIONED in 2025.
The new API at data.imf.org uses SDMX 3.0 and requires registration.

Key datasets:
  - IFS (International Financial Statistics): Exchange rates, reserves, interest rates
  - WEO (World Economic Outlook): GDP, inflation, current account, fiscal data
  - BOP (Balance of Payments): Current/capital/financial accounts

Common WEO codes:
  NGDP_RPCH    → GDP growth (% change)
  PCPIEPCH     → Inflation, avg consumer prices (% change)
  BCA_NGDPD    → Current account balance (% GDP)
  GGSB_NPGDP   → Fiscal balance (% potential GDP)
  GGXWDN_NGDP  → Net government debt (% GDP)
  GGXWDG_NGDP  → Gross government debt (% GDP)
  LE           → Unemployment rate (%)
  TMG_RPCH     → Import volume (% change)
  TXG_RPCH     → Export volume (% change)

Tools exposed:
  - get_weo: fetch WEO indicators for a country
  - get_ifs: fetch IFS exchange rate data
  - list_weo_codes: list common WEO indicator codes
  - search_weo: search WEO codes by keyword

Usage: python3 server.py <tool> '<json_arguments>'
"""

import json
import sys
import urllib.error
import urllib.request

IMF_BASE = "https://data.imf.org/api/v1"

# Common WEO indicator codes (maintained reference)
WEO_CODES = {
    "NGDP_RPCH": "Gross domestic product, constant prices (% change)",
    "NGDPD": "Gross domestic product, current prices (USD billions)",
    "NGDPRPPPPC": "GDP per capita, PPP (current international $)",
    "PCPIEPCH": "Inflation, average consumer prices (% change)",
    "PCPIPCH": "Inflation, end of period consumer prices (% change)",
    "BCA_NGDPD": "Current account balance (% GDP)",
    "GGSB_NPGDP": "General government structural balance (% potential GDP)",
    "GGXWDN_NGDP": "General government net debt (% GDP)",
    "GGXWDG_NGDP": "General government gross debt (% GDP)",
    "LE": "Unemployment rate (% of labor force)",
    "TMG_RPCH": "Imports of goods and services (% change)",
    "TXG_RPCH": "Exports of goods and services (% change)",
    "NGAP_NPGDP": "Output gap (% potential GDP)",
    "NID_NGDP": "Investment (% GDP)",
    "LUR": "Unemployment rate (ILO definition)",
}

ISO3_CODES = {
    "NZL": "New Zealand", "AUS": "Australia", "USA": "United States",
    "GBR": "United Kingdom", "CAN": "Canada", "JPN": "Japan",
    "CHN": "China", "DEU": "Germany", "FRA": "France", "ITA": "Italy",
    "ESP": "Spain", "KOR": "South Korea", "IND": "India", "BRA": "Brazil",
    "RUS": "Russia", "ZAF": "South Africa", "MEX": "Mexico", "IDN": "Indonesia",
    "TUR": "Turkey", "SAU": "Saudi Arabia", "CHE": "Switzerland", "SGP": "Singapore",
    "IRL": "Ireland", "DNK": "Denmark", "SWE": "Sweden", "NOR": "Norway",
}


def get_weo(country="NZL", indicator="NGDP_RPCH", limit=10):
    """
    Fetch WEO data for a country.

    IMPORTANT: Requires registration at https://data.imf.org/
    The old dataservices.imf.org endpoint was decommissioned in 2025.

    Args:
        country: 3-letter ISO code (NZL, USA, CHN, etc.)
        indicator: WEO indicator code (see list_weo_codes)
        limit: max observations
    """
    if country.upper() not in ISO3_CODES:
        return {
            "error": f"Unknown country code: {country}",
            "valid_codes": list(ISO3_CODES.keys())[:15],
        }

    if indicator not in WEO_CODES:
        return {
            "error": f"Unknown WEO code: {indicator}",
            "tip": "Use list_weo_codes or search_weo to find valid codes",
        }

    country = country.upper()

    # Try new SDMX 3.0 API endpoint
    url = f"{IMF_BASE}/data/WEO/{country}.{indicator}?format=json"
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "AgentTools-Macro/1.0", "Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return {
                "country": country,
                "country_name": ISO3_CODES.get(country, country),
                "indicator": indicator,
                "indicator_name": WEO_CODES.get(indicator, indicator),
                "source": "IMF WEO",
                "count": len(data.get("observations", [])),
                "observations": data.get("observations", [])[-limit:],
            }
    except urllib.error.HTTPError as e:
        if e.code == 403:
            return {
                "error": f"IMF API registration required ({e.code})",
                "message": "The old dataservices.imf.org API was decommissioned in 2025.",
                "action": "Register for free at https://data.imf.org/ to get API access",
                "indicator_code": indicator,
                "indicator_name": WEO_CODES.get(indicator, indicator),
                "country": country,
            }
        return {"error": f"HTTP {e.code}: {e.reason}"}
    except urllib.error.URLError as e:
        return {
            "error": f"Connection failed: {e.reason}",
            "message": "The IMF API at data.imf.org requires registration.",
            "action": "Visit https://data.imf.org/ to register for API access",
        }


def get_ifs(indicator="ENDA_XDC_USD_RATE", country="NZ", limit=12):
    """
    Fetch IFS exchange rate data. Requires IMF API registration.

    Args:
        indicator: IMF IFS indicator code
        country: 2-letter ISO country code
        limit: max observations
    """
    url = f"{IMF_BASE}/data/IFS/M.{country}.{indicator}?format=json"
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "AgentTools-Macro/1.0", "Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return {
                "indicator": indicator,
                "country": country,
                "source": "IMF IFS",
                "count": len(data.get("observations", [])),
                "observations": data.get("observations", [])[-limit:],
            }
    except urllib.error.HTTPError as e:
        if e.code == 403:
            return {
                "error": "IMF API registration required",
                "action": "Register at https://data.imf.org/",
                "note": "The old dataservices.imf.org was decommissioned in 2025.",
            }
        return {"error": f"HTTP {e.code}: {e.reason}"}
    except urllib.error.URLError as e:
        return {"error": f"Connection failed: {e.reason}"}


def list_weo_codes():
    """List all common WEO indicator codes with descriptions."""
    return {
        "source": "IMF World Economic Outlook",
        "count": len(WEO_CODES),
        "codes": {k: v for k, v in sorted(WEO_CODES.items())},
        "note": "IMF API registration required at https://data.imf.org/",
    }


def search_weo(keyword=""):
    """Search WEO codes by keyword in code or description."""
    kw = keyword.lower()
    matches = {
        k: v for k, v in WEO_CODES.items()
        if kw in k.lower() or kw in v.lower()
    }
    return {
        "search": keyword,
        "count": len(matches),
        "results": [{"code": k, "description": v} for k, v in matches.items()],
        "note": "IMF API registration required at https://data.imf.org/",
    }


def handle_mcp_call(tool_name, arguments):
    tools = {
        "get_weo": lambda: get_weo(**arguments),
        "get_ifs": lambda: get_ifs(**arguments),
        "list_weo_codes": lambda: list_weo_codes(**arguments),
        "search_weo": lambda: search_weo(**arguments),
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
        print("IMF MCP Server for AgentTools Macro Skills")
        print("IMPORTANT: Requires free registration at https://data.imf.org/")
        print("Common WEO codes: NGDP_RPCH (GDP growth), PCPIEPCH (CPI), BCA_NGDPD (Current Account)")
        print("Usage: python3 server.py <tool> '<json_arguments>'")
        print("Examples:")
        print('  python3 server.py list_weo_codes')
        print('  python3 server.py search_weo \'{"keyword":"GDP"}\'')
        print('  python3 server.py get_weo \'{"country":"NZL","indicator":"NGDP_RPCH"}\'')
        sys.exit(1)

    tool = sys.argv[1]
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    result = handle_mcp_call(tool, args)
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
