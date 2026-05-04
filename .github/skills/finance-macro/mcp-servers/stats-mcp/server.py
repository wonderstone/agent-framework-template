#!/usr/bin/env python3
"""
MCP Server: National Statistics Offices

Provides economic data from national statistics agencies.
Currently supports: Stats NZ (Aotearoa Data Explorer), ABS (Australia), ONS (UK).

API keys required (free upon registration):
  - Stats NZ: Register at https://data.stats.govt.nz/ → get API key → set STATS_NZ_API_KEY
  - ABS (Australia): Register at https://api.data.abs.gov.au/ → set ABS_API_KEY
  - ONS (UK): Register at https://api.ons.gov.uk/ → set ONS_API_KEY

Tools exposed:
  - get_nz_data: fetch data from Stats NZ Aotearoa Data Explorer
  - list_nz_datasets: list available NZ datasets
  - get_abs_data: fetch data from ABS (Australia)
  - get_ons_data: fetch data from ONS (UK)

Usage: python3 server.py <tool> '<json_arguments>'
"""

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

STATS_NZ_BASE = "https://api.stats.govt.nz/opendata/v1"
ABS_BASE = "https://api.data.abs.gov.au/v1"
ONS_BASE = "https://api.ons.gov.uk/v1"

# Try shared env loading
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
try:
    from env_setup import get_key
except ImportError:
    def get_key(k):
        return os.environ.get(k, "")


def _nz_request(endpoint, timeout=30):
    """Make a Stats NZ API request."""
    api_key = get_key("STATS_NZ_API_KEY")
    if not api_key:
        return {"error": "STATS_NZ_API_KEY not set", "action": "Register at https://data.stats.govt.nz/ for a free API key"}

    url = f"{STATS_NZ_BASE}/{endpoint}"
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "MacroFinance-MCP/1.0",
            "Ocp-Apim-Subscription-Key": api_key,
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:500] if e.fp else ""
        return {"error": f"HTTP {e.code}: {e.reason}", "detail": body}
    except urllib.error.URLError as e:
        return {"error": f"Connection error: {e.reason}"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response from Stats NZ"}


def _abs_request(endpoint, timeout=30):
    """Make an ABS API request."""
    api_key = get_key("ABS_API_KEY")
    if not api_key:
        return {"error": "ABS_API_KEY not set", "action": "Register at https://api.data.abs.gov.au/"}

    url = f"{ABS_BASE}/{endpoint}"
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "MacroFinance-MCP/1.0",
            "x-api-key": api_key,
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}"}
    except urllib.error.URLError as e:
        return {"error": f"Connection error: {e.reason}"}


def list_nz_datasets(limit=20):
    """List available Stats NZ datasets."""
    result = _nz_request(f"Data?$top={limit}")
    if "error" in result:
        return result

    datasets = result.get("value", [])
    return {
        "source": "Stats NZ",
        "count": len(datasets),
        "datasets": [
            {
                "id": d.get("id", ""),
                "name": d.get("name", ""),
                "description": d.get("description", ""),
            }
            for d in datasets
        ],
    }


def get_nz_data(dataset_id="GDP", limit=20):
    """Fetch observations for a Stats NZ dataset."""
    result = _nz_request(
        f"Observations?$filter=ResourceID eq '{dataset_id}'&$top={limit}"
    )
    if "error" in result:
        return result

    obs = result.get("value", [])
    return {
        "dataset_id": dataset_id,
        "source": "Stats NZ",
        "count": len(obs),
        "observations": [
            {
                "period": o.get("Period", ""),
                "value": o.get("Value", ""),
                "unit": o.get("Unit", ""),
            }
            for o in obs
        ],
    }


def get_abs_data(indicator="CPI", limit=20):
    """Fetch ABS (Australia) data."""
    result = _abs_request(f"data/{indicator}/all?format=jsondata&limit={limit}")
    if "error" in result:
        return result
    return {"indicator": indicator, "source": "ABS Australia", "data": result}


def get_ons_data(dataset_id="cpih", limit=20):
    """Fetch ONS (UK) data."""
    api_key = get_key("ONS_API_KEY")
    if not api_key:
        return {"error": "ONS_API_KEY not set", "action": "Register at https://api.ons.gov.uk/"}
    return {"error": "ONS API integration in progress", "dataset_id": dataset_id}


def list_providers():
    """List supported statistics offices and their API key requirements."""
    providers = {
        "stats_nz": {
            "name": "Stats NZ — Aotearoa Data Explorer",
            "url": "https://data.stats.govt.nz/",
            "env_var": "STATS_NZ_API_KEY",
            "notes": "Free registration. Covers: GDP, CPI, employment, housing, trade, population.",
        },
        "abs": {
            "name": "Australian Bureau of Statistics",
            "url": "https://api.data.abs.gov.au/",
            "env_var": "ABS_API_KEY",
            "notes": "Free registration. Covers: CPI, labour force, national accounts, trade.",
        },
        "ons": {
            "name": "UK Office for National Statistics",
            "url": "https://api.ons.gov.uk/",
            "env_var": "ONS_API_KEY",
            "notes": "Free registration. Covers: GDP, CPI, labour market, trade, population.",
        },
    }
    return {"providers": providers, "note": "All require free registration for API access"}


def handle_mcp_call(tool_name, arguments):
    tools = {
        "list_nz_datasets": lambda: list_nz_datasets(**arguments),
        "get_nz_data": lambda: get_nz_data(**arguments),
        "get_abs_data": lambda: get_abs_data(**arguments),
        "get_ons_data": lambda: get_ons_data(**arguments),
        "list_providers": lambda: list_providers(**arguments),
    }
    if tool_name not in tools:
        return {"error": f"Unknown tool: {tool_name}. Available: {list(tools.keys())}"}
    try:
        return tools[tool_name]()
    except TypeError as e:
        return {"error": f"Invalid arguments for {tool_name}: {e}"}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Stats MCP Server for Macro Finance Skills")
        print("Supported: Stats NZ, ABS (Australia), ONS (UK)")
        print("Usage: python3 server.py <tool> '<json_arguments>'")
        print("Examples:")
        print('  python3 server.py list_providers')
        print('  python3 server.py list_nz_datasets')
        print('  python3 server.py get_nz_data \'{"dataset_id":"CPI","limit":10}\'')
        sys.exit(1)

    tool = sys.argv[1]
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    result = handle_mcp_call(tool, args)
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
