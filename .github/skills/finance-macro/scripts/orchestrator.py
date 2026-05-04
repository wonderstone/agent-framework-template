#!/usr/bin/env python3
"""
Macro Analysis Orchestrator — General-Purpose Query Router

Connects the full pipeline: Query → Domain Router → MCP Data Fetch → Cache →
Model Execution → Output Formatting.

Design principle: framework, not hardcoded analyzer. Works for any country,
any domain, any indicator combination.

Usage:
    python3 orchestrator.py '{"domain":"country-intel","country":"JPN"}'
    python3 orchestrator.py '{"domain":"property-cycle","country":"AU"}'
    python3 orchestrator.py '{"domain":"liquidity","scope":"global"}'
    python3 orchestrator.py '{"domain":"macro-dashboard","country":"USA","indicators":["GDP","CPI","UNRATE"]}'
"""

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MCP_DIR = ROOT / "mcp-servers"
SCRIPTS_DIR = ROOT / "scripts"
MODEL_DIR = ROOT

# Import shared modules
sys.path.insert(0, str(SCRIPTS_DIR))
from cache_manager import get as cache_get, set as cache_set

# ══════════════════════════════════════════════════════════════════════════════
# Domain Configuration — defines data sources + models for each domain
# Add new domains here. Each entry specifies: MCP sources, model script, output.
# ══════════════════════════════════════════════════════════════════════════════

DOMAIN_CONFIG = {
    "country-intel": {
        "description": "Country macroeconomic health + lens analysis",
        "data_sources": [
            {
                "source": "worldbank",
                "tool": "get_indicator",
                "indicators": [
                    {"id": "NY.GDP.MKTP.KD.ZG", "name": "GDP_growth"},
                    {"id": "FP.CPI.TOTL.ZG", "name": "CPI_inflation"},
                    {"id": "BN.CAB.XOKA.GD.ZS", "name": "current_account"},
                    {"id": "GC.DOD.TOTL.GD.ZS", "name": "govt_debt"},
                    {"id": "SL.UEM.TOTL.ZS", "name": "unemployment"},
                ],
            },
        ],
        "optional_sources": [
            {"source": "bis", "tool": "get_credit_gap", "model_param": "credit_gap"},
        ],
        "models": [
            {
                "script": "country-intel/scripts/macro_score.py",
                "param_map": {
                    "growth": {"from": "GDP_growth", "transform": {"op": "avg", "n": 3}},
                    "inflation": {"from": "CPI_inflation", "transform": {"op": "deviation", "target": 2.0}},
                    "cagdp": {"from": "current_account", "transform": "latest"},
                    "debt": {"from": "govt_debt", "transform": "latest"},
                    "fiscal": {"value": -3.0},
                    "unemployment": {"from": "unemployment", "transform": "latest"},
                    "creditgap": {"from": "credit_gap", "transform": "latest"},
                },
            },
        ],
        "output_template": "country_intel",
    },

    "property-cycle": {
        "description": "Real estate cycle phase + affordability analysis",
        "data_sources": [
            {
                "source": "bis",
                "tool": "get_property_prices",
                "param": "country",
            },
            {
                "source": "bis",
                "tool": "get_credit_gap",
                "param": "country",
            },
        ],
        "models": [
            {
                "script": "property-cycle/scripts/cycle_score.py",
                "param_map": {
                    "price-yoy": {"from": "bis_get_property_prices", "transform": "yoy"},
                    "price-income-vs-lt": {"value": 1.18},
                    "credit-yoy": {"from": "bis_get_credit_gap", "transform": "yoy"},
                    "approvals-yoy": {"value": -10.0},
                    "inventory-months": {"value": 5.0},
                    "auction-clearance": {"value": 55.0},
                    "investor-share": {"value": 20.0},
                },
            },
            {
                "script": "property-cycle/scripts/affordability_calc.py",
                "param_map": {
                    "price": {"value": 800000},
                    "income": {"value": 95000},
                    "rent": {"value": 2600},
                    "rate": {"value": 6.0},
                },
            },
        ],
        "output_template": "property_cycle",
    },

    "liquidity": {
        "description": "Global central bank liquidity analysis",
        "data_sources": [
            {
                "source": "fred",
                "tool": "get_series",
                "series": [
                    {"id": "WALCL", "name": "Fed_total_assets"},
                    {"id": "TGA", "name": "Treasury_general_account"},
                    {"id": "RRPONTSYD", "name": "Overnight_RRP"},
                    {"id": "M2SL", "name": "M2_money_supply"},
                ],
            },
        ],
        "models": [
            {
                "script": "liquidity/scripts/net_liquidity.py",
                "param_map": {
                    "walcl": "Fed_total_assets",
                    "tga": "Treasury_general_account",
                    "rrp": "Overnight_RRP",
                },
            },
            {
                "script": "liquidity/scripts/scissors_factor.py",
                "param_map": {},
            },
        ],
        "output_template": "liquidity_dashboard",
    },

    "macro-dashboard": {
        "description": "Key macro indicators snapshot + recession risk",
        "data_sources": [
            {
                "source": "worldbank",
                "tool": "get_indicator",
                "indicators": [
                    {"id": "NY.GDP.MKTP.KD.ZG", "name": "GDP_growth"},
                    {"id": "FP.CPI.TOTL.ZG", "name": "CPI"},
                    {"id": "SL.UEM.TOTL.ZS", "name": "Unemployment"},
                ],
            },
            {
                "source": "fred",
                "tool": "get_series",
                "series": [
                    {"id": "UNRATE", "name": "US_unemployment"},
                    {"id": "DGS10", "name": "US_10Y"},
                    {"id": "DGS2", "name": "US_2Y"},
                    {"id": "T10Y2Y", "name": "10Y2Y_spread"},
                    {"id": "FEDFUNDS", "name": "Fed_funds"},
                ],
            },
        ],
        "models": [
            {
                "script": "macro-dashboard/scripts/indicator_hub.py",
                "param_map": {
                    "gdp": {"from": "GDP_growth", "transform": "latest"},
                    "unrate": {"from": "US_unemployment", "transform": "latest"},
                    "spread": {"from": "10Y2Y_spread", "transform": "latest"},
                    "fedfunds": {"from": "Fed_funds", "transform": "latest"},
                    "pmi": {"value": 50.0},
                    "core-pce": {"value": 2.5},
                    "indpro": {"value": 1.5},
                    "retail": {"value": 3.0},
                    "caputil": {"value": 78.0},
                    "core-cpi": {"value": 3.0},
                    "nfp": {"value": 150},
                    "claims": {"value": 250},
                    "bbb": {"value": 2.0},
                },
            },
            {
                "script": "macro-dashboard/scripts/yield_curve.py",
                "param_map": {
                    "dgs2": {"from": "US_2Y", "transform": "latest", "fallback": 4.85},
                    "dgs10": {"from": "US_10Y", "transform": "latest", "fallback": 4.55},
                    "fedfunds": {"from": "Fed_funds", "transform": "latest", "fallback": 5.25},
                    "dtb3": {"value": 5.30},
                    "bbb": {"value": 1.85},
                    "tips10": {"value": 2.10},
                },
            },
        ],
        "output_template": "dashboard",
    },

    "central-bank": {
        "description": "Central bank policy stance + hawk-dove scoring",
        "data_sources": [
            {
                "source": "fred",
                "tool": "get_series",
                "series": [
                    {"id": "FEDFUNDS", "name": "Fed_funds_rate"},
                    {"id": "DGS10", "name": "US_10Y"},
                    {"id": "T10Y2Y", "name": "10Y2Y_spread"},
                ],
            },
        ],
        "models": [
            {
                "script": "central-bank-watcher/scripts/hawk_dove_scorer.py",
                "param_map": {},
            },
        ],
        "output_template": "central_bank",
    },

    "fiscal-policy": {
        "description": "Fiscal position + debt sustainability analysis",
        "data_sources": [
            {
                "source": "worldbank",
                "tool": "get_indicator",
                "indicators": [
                    {"id": "GC.DOD.TOTL.GD.ZS", "name": "govt_debt"},
                    {"id": "NY.GDP.MKTP.KD.ZG", "name": "GDP_growth"},
                ],
            },
        ],
        "models": [
            {
                "script": "fiscal-policy/scripts/debt_dynamics.py",
                "param_map": {
                    "debt": "govt_debt",
                    "growth": "GDP_growth",
                },
            },
        ],
        "output_template": "fiscal_policy",
    },

    "commodity-macro": {
        "description": "Commodity price + supercycle analysis",
        "data_sources": [],
        "models": [
            {
                "script": "commodity-macro/scripts/supercycle_scorer.py",
                "param_map": {
                    "industrialization": {"value": 14},
                    "capex-gdp": {"value": 4.5},
                    "demand-shift": {"value": 14},
                    "inventory": {"value": 70},
                    "producer-discipline": {"value": 14},
                },
            },
        ],
        "output_template": "commodity",
        "note": "Commodity price data sources TBD. Currently uses manual parameter inputs.",
    },
}

# Country code mappings
ISO3_TO_ISO2 = {
    "NZL": "NZ", "AUS": "AU", "USA": "US", "GBR": "GB", "CAN": "CA",
    "JPN": "JP", "CHN": "CN", "DEU": "DE", "FRA": "FR", "ITA": "IT",
    "ESP": "ES", "KOR": "KR", "IND": "IN", "BRA": "BR", "RUS": "RU",
    "ZAF": "ZA", "MEX": "MX", "IDN": "ID", "TUR": "TR", "CHE": "CH",
    "SGP": "SG", "IRL": "IE", "DNK": "DK", "SWE": "SE", "NOR": "NO",
}

COUNTRY_NAMES = {
    "NZL": "New Zealand", "AUS": "Australia", "USA": "United States",
    "GBR": "United Kingdom", "CAN": "Canada", "JPN": "Japan",
    "CHN": "China", "DEU": "Germany", "FRA": "France", "ITA": "Italy",
    "ESP": "Spain", "KOR": "South Korea", "IND": "India", "BRA": "Brazil",
}


# ══════════════════════════════════════════════════════════════════════════════
# Data Transformer — computes derived indicators from raw observations
# ══════════════════════════════════════════════════════════════════════════════

def _extract_values(observations):
    """Extract numeric values from observation list of {date, value} dicts."""
    if not observations:
        return []
    vals = []
    for o in observations:
        if isinstance(o, dict):
            v = o.get("value")
        elif isinstance(o, (list, tuple)):
            v = o[1] if len(o) > 1 else o[0]
        else:
            v = o
        try:
            vals.append(float(v))
        except (ValueError, TypeError):
            pass
    return vals


def _sort_by_date(observations):
    """Sort observations by date ascending."""
    if not observations:
        return []
    return sorted(observations, key=lambda o: str(o.get("date", "")) if isinstance(o, dict) else "")


def transform_latest(observations):
    """Return most recent observation value."""
    vals = _extract_values(observations)
    return vals[-1] if vals else None


def transform_yoy(observations):
    """
    Compute YoY % change from latest two annual observations, or
    for quarterly data, compare latest to same quarter prior year.
    """
    sorted_obs = _sort_by_date(observations)
    if len(sorted_obs) < 2:
        vals = _extract_values(sorted_obs)
        return ((vals[-1] - vals[0]) / abs(vals[0]) * 100) if vals and vals[0] != 0 else None

    # For data with dates, find 12-month-apart pairs
    latest = sorted_obs[-1]
    latest_date = str(latest.get("date", "")) if isinstance(latest, dict) else ""

    # Find observation ~12 months prior
    year_ago = None
    for o in reversed(sorted_obs[:-1]):
        o_date = str(o.get("date", "")) if isinstance(o, dict) else ""
        if latest_date and o_date:
            # Match same quarter prior year or closest annual
            if latest_date[:4] != o_date[:4]:
                year_ago = o
                break
        else:
            year_ago = sorted_obs[-2]
            break

    if year_ago is None:
        year_ago = sorted_obs[-2]

    latest_val = float(latest.get("value", 0)) if isinstance(latest, dict) else float(latest)
    ago_val = float(year_ago.get("value", 0)) if isinstance(year_ago, dict) else float(year_ago)

    if ago_val == 0:
        return None
    return ((latest_val - ago_val) / abs(ago_val)) * 100


def transform_avg(observations, n=3):
    """Compute N-period average of observation values."""
    vals = _extract_values(observations)
    if not vals:
        return None
    window = vals[-n:] if len(vals) >= n else vals
    return sum(window) / len(window)


def transform_deviation(observations, target=2.0):
    """Compute absolute deviation of latest value from target."""
    latest = transform_latest(observations)
    if latest is None:
        return None
    return abs(latest - target)


def transform_ratio(observations, base_observations=None):
    """Compute ratio of latest values: observations / base_observations."""
    a = transform_latest(observations)
    b = transform_latest(base_observations) if base_observations else 1
    if a is None or b is None or b == 0:
        return None
    return a / b


# Registry of available transforms for param_map references
TRANSFORMS = {
    "latest": transform_latest,
    "yoy": transform_yoy,
    "avg": transform_avg,
    "deviation": transform_deviation,
    "ratio": transform_ratio,
}


def apply_transform(observations, transform_spec):
    """
    Apply a transformation to raw observations.

    transform_spec can be:
      - "yoy" → transform_yoy(obs)
      - {"op": "yoy"} → transform_yoy(obs)
      - {"op": "avg", "n": 5} → transform_avg(obs, n=5)
      - {"op": "deviation", "target": 2.0} → transform_deviation(obs, target=2.0)
    """
    if isinstance(transform_spec, str):
        fn = TRANSFORMS.get(transform_spec)
        return fn(observations) if fn else None

    if isinstance(transform_spec, dict):
        op = transform_spec.get("op", "latest")
        fn = TRANSFORMS.get(op)
        if fn is None:
            return None
        kwargs = {k: v for k, v in transform_spec.items() if k != "op"}
        return fn(observations, **kwargs)

    return None


# ══════════════════════════════════════════════════════════════════════════════
# MCP Server Caller
# ══════════════════════════════════════════════════════════════════════════════

def _call_mcp(server_name, tool, args_dict):
    """Call an MCP server and return parsed JSON result."""
    server_path = MCP_DIR / f"{server_name}-mcp" / "server.py"
    if not server_path.exists():
        return {"error": f"MCP server not found: {server_path}"}

    args_json = json.dumps(args_dict)
    try:
        result = subprocess.run(
            ["python3", str(server_path), tool, args_json],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            return {"error": f"MCP call failed", "stderr": result.stderr[:500]}
        return json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        return {"error": "MCP call timed out"}
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON from MCP server: {e}", "raw": result.stdout[:300]}


# ══════════════════════════════════════════════════════════════════════════════
# Data Fetcher — with cache
# ══════════════════════════════════════════════════════════════════════════════

def fetch_domain_data(domain, country=None, date_range=None, force_refresh=False):
    """
    Fetch all data needed for a domain analysis.

    Args:
        domain: domain key from DOMAIN_CONFIG
        country: ISO3 country code (e.g., 'NZL', 'JPN')
        date_range: 'start:end' year range (e.g., '2020:2024')
        force_refresh: skip cache if True

    Returns:
        dict of {param_name: value} ready for model consumption
    """
    config = DOMAIN_CONFIG.get(domain)
    if not config:
        return {"error": f"Unknown domain: {domain}", "available": list(DOMAIN_CONFIG.keys())}

    iso2 = ISO3_TO_ISO2.get(country, country) if country else None
    data_bundle = {"_meta": {"domain": domain, "country": country, "fetched_at": None}}

    for ds in config.get("data_sources", []):
        source = ds["source"]
        tool = ds["tool"]
        cache_key = f"{source}_{tool}_{country}_{date_range}"

        # Check cache
        if not force_refresh:
            cached = cache_get(source, cache_key)
            if cached:
                data_bundle.update(cached)
                continue

        # Fetch from MCP
        if "indicators" in ds:
            # WorldBank-style: multiple indicators per country
            for ind in ds["indicators"]:
                args = {"indicator": ind["id"], "country": country}
                if date_range:
                    args["date_range"] = date_range
                result = _call_mcp(source, tool, args)
                if "observations" in result:
                    data_bundle[ind["name"]] = result["observations"]
                elif "error" not in result:
                    data_bundle[ind["name"]] = result

        elif "series" in ds:
            # FRED-style: individual series
            for s in ds["series"]:
                args = {"series_id": s["id"], "limit": 24, "sort_order": "desc"}
                result = _call_mcp(source, tool, args)
                if "observations" in result:
                    data_bundle[s["name"]] = result["observations"]
                elif "error" not in result:
                    data_bundle[s["name"]] = result

        elif "param" in ds:
            # BIS-style: one tool call per country
            args = {"country": iso2, "limit": 40}
            result = _call_mcp(source, tool, args)
            key_name = f"{source}_{tool}"
            data_bundle[key_name] = result

        # Write to cache
        cache_set(source, cache_key, data_bundle)

    # Try optional sources
    for ds in config.get("optional_sources", []):
        source = ds["source"]
        tool = ds["tool"]
        try:
            result = _call_mcp(source, tool, {"country": iso2, "limit": 20})
            if "observations" in result:
                data_bundle[ds["model_param"]] = result["observations"]
        except Exception:
            pass  # Optional sources can fail silently

    return data_bundle


# ══════════════════════════════════════════════════════════════════════════════
# Model Runner
# ══════════════════════════════════════════════════════════════════════════════

def run_models(domain, data_bundle, extra_params=None):
    """
    Run domain-specific models with fetched data.

    Args:
        domain: domain key
        data_bundle: data from fetch_domain_data()
        extra_params: additional model parameters (e.g., mortgage_rate, lens)

    Returns:
        list of model results
    """
    config = DOMAIN_CONFIG.get(domain, {})
    models = config.get("models", [])
    results = []

    for model in models:
        script_path = ROOT / model["script"]
        if not script_path.exists():
            results.append({"model": model["script"], "error": f"Script not found: {script_path}"})
            continue

        # Resolve model parameters from data_bundle using param_map
        cli_args = []
        for param_name, mapping in model.get("param_map", {}).items():
            value = _resolve_param(mapping, data_bundle)
            if value is not None:
                cli_args.append(f"--{param_name.replace('_', '-')}")
                cli_args.append(str(value))

        # Add extra params (user-supplied overrides)
        if extra_params:
            for k, v in extra_params.items():
                cli_args.append(f"--{k.replace('_', '-')}")
                cli_args.append(str(v))

        try:
            result = subprocess.run(
                ["python3", str(script_path), "--export", "json"] + cli_args,
                capture_output=True, text=True, timeout=30,
            )
            if result.returncode == 0:
                results.append({
                    "model": model["script"],
                    "result": json.loads(result.stdout),
                })
            else:
                results.append({
                    "model": model["script"],
                    "error": result.stderr[:500] or "Model execution failed",
                })
        except subprocess.TimeoutExpired:
            results.append({"model": model["script"], "error": "Timeout"})
        except json.JSONDecodeError:
            results.append({"model": model["script"], "error": "Invalid model output"})

    return results


def _resolve_param(mapping, data_bundle):
    """
    Resolve a model parameter from the data bundle.

    mapping can be:
      - "data_key" → extract latest value from data_bundle[data_key]
      - {"from": "data_key", "transform": "yoy"} → apply transform to data
      - {"from": "data_key", "transform": {"op": "avg", "n": 3}}
      - {"value": 42} → literal value
    """
    if isinstance(mapping, str):
        # Simple key lookup → latest value
        raw = data_bundle.get(mapping)
        if raw is None:
            return None
        if isinstance(raw, dict) and "observations" in raw:
            raw = raw["observations"]
        if isinstance(raw, list):
            return transform_latest(raw)
        if isinstance(raw, dict) and "error" in raw:
            return None  # Data fetch error — skip this param
        return raw

    if isinstance(mapping, dict):
        if "value" in mapping:
            return mapping["value"]

        source_key = mapping.get("from")
        if source_key is None:
            return mapping.get("fallback")

        raw = data_bundle.get(source_key)
        if raw is None:
            # Try fuzzy match
            for k in data_bundle:
                if k.startswith("_") or k.startswith("bis_"):
                    continue
                if source_key.lower().replace("_", "") in k.lower().replace("_", ""):
                    raw = data_bundle.get(k)
                    break
        if raw is None:
            return mapping.get("fallback")  # Use fallback if data not found

        # Unwrap dict-wrapped data ({observations: [...], ...})
        if isinstance(raw, dict) and "observations" in raw:
            raw = raw["observations"]

        transform_spec = mapping.get("transform")
        if transform_spec and isinstance(raw, list):
            return apply_transform(raw, transform_spec)

        # No transform → return latest if list, else raw
        if isinstance(raw, list):
            return transform_latest(raw)
        return raw

    return mapping


# ══════════════════════════════════════════════════════════════════════════════
# Query Parser — handles natural-language-like structured queries
# ══════════════════════════════════════════════════════════════════════════════

def parse_query(query):
    """
    Parse and validate an analysis query.

    Accepted formats:
      - dict/JSON with keys: domain, country, indicators, lens, params
      - shorthand: "domain:country" string

    Returns validated query dict with defaults filled.
    """
    if isinstance(query, str):
        try:
            query = json.loads(query)
        except json.JSONDecodeError:
            # Try "domain:country" shorthand
            parts = query.split(":")
            if len(parts) == 2 and parts[0] in DOMAIN_CONFIG:
                query = {"domain": parts[0], "country": parts[1].upper()}
            else:
                return {"error": f"Invalid query string: {query}", "hint": "Use JSON: {\"domain\":\"...\", \"country\":\"...\"}"}

    if not isinstance(query, dict):
        return {"error": "Query must be a dict or JSON string"}

    domain = query.get("domain", "")
    if domain not in DOMAIN_CONFIG:
        return {
            "error": f"Unknown domain: '{domain}'",
            "available_domains": sorted(DOMAIN_CONFIG.keys()),
            "hint": "Pick one from available_domains",
        }

    country = query.get("country", "").upper() if query.get("country") else None
    if country and country not in ISO3_TO_ISO2 and country not in COUNTRY_NAMES:
        # Accept any valid 3-letter code or known country name
        pass  # Non-fatal — some domains don't need country

    return {
        "domain": domain,
        "country": country,
        "indicators": query.get("indicators", []),
        "lens": query.get("lens"),
        "params": query.get("params", {}),
        "date_range": query.get("date_range", "2020:2024"),
        "force_refresh": query.get("force_refresh", False),
    }


# ══════════════════════════════════════════════════════════════════════════════
# Main Pipeline
# ══════════════════════════════════════════════════════════════════════════════

def analyze(query):
    """
    Run a complete macro analysis pipeline.

    Args:
        query: dict with {domain, country, ...} or JSON string

    Returns:
        dict with {query, data, models, formatted_output}
    """
    parsed = parse_query(query)
    if "error" in parsed:
        return parsed

    domain = parsed["domain"]
    country = parsed["country"]
    date_range = parsed.get("date_range")

    # Step 1: Fetch data
    data_bundle = fetch_domain_data(domain, country, date_range, parsed.get("force_refresh"))

    # Step 2: Run models
    model_results = run_models(domain, data_bundle, parsed.get("params"))

    # Step 3: Format output
    output = format_output(domain, parsed, data_bundle, model_results)

    return {
        "query": parsed,
        "data_summary": summarize_data(data_bundle),
        "model_results": model_results,
        "output": output,
    }


def summarize_data(data_bundle):
    """Create a compact summary of fetched data (omit raw series)."""
    summary = {"_meta": data_bundle.get("_meta", {})}
    for key, value in data_bundle.items():
        if key.startswith("_"):
            continue
        if isinstance(value, list) and len(value) > 0:
            summary[key] = f"{len(value)} observations (latest: {value[-1]})"
        elif isinstance(value, dict):
            summary[key] = f"dict with {len(value)} keys"
        else:
            summary[key] = value
    return summary


def format_output(domain, query, data_bundle, model_results):
    """Format analysis results according to domain template."""
    country_name = COUNTRY_NAMES.get(query.get("country", ""), query.get("country", ""))

    output = {
        "domain": domain,
        "domain_description": DOMAIN_CONFIG.get(domain, {}).get("description", ""),
        "country": country_name,
        "timestamp": None,
        "sections": [],
    }

    # Generic structure — domain-specific formatting happens in the agent's
    # response layer where the SKILL.md output templates are applied
    for mr in model_results:
        if "result" in mr:
            output["sections"].append({
                "model": mr["model"],
                "data": mr["result"],
            })

    return output


# ══════════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Macro Analysis Orchestrator")
        print("")
        print("General-purpose query router for macro-finance analysis.")
        print("")
        print("Usage:")
        print("  python3 orchestrator.py '<json_query>'")
        print("")
        print("Examples:")
        print('  python3 orchestrator.py \'{"domain":"country-intel","country":"JPN"}\'')
        print('  python3 orchestrator.py \'{"domain":"property-cycle","country":"AUS","params":{"mortgage_rate":6.5}}\'')
        print('  python3 orchestrator.py \'{"domain":"liquidity"}\'')
        print('  python3 orchestrator.py \'{"domain":"macro-dashboard","country":"USA"}\'')
        print("")
        print("Available domains:")
        for d, cfg in sorted(DOMAIN_CONFIG.items()):
            print(f"  {d:<20} — {cfg['description']}")
        print("")
        print("Available countries (ISO3 codes):")
        print(f"  {', '.join(sorted(ISO3_TO_ISO2.keys())[:20])}")
        sys.exit(0)

    result = analyze(sys.argv[1])
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
