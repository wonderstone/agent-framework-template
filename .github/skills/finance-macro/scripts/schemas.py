#!/usr/bin/env python3
"""
Output Schemas & Cross-Domain Linker

Defines standard JSON output formats for each domain, enabling automated
cross-domain data flow. Each schema includes version, required fields,
and downstream consumers — so liquidity output can feed macro-bridge, etc.

Usage:
    from schemas import validate_output, link_domains
    validated = validate_output("country-intel", model_output)
    bridge_input = link_domains("liquidity", "macro-bridge", liquidity_output)
"""

# ══════════════════════════════════════════════════════════════════════════════
# Domain Output Schemas (v1.0)
# ══════════════════════════════════════════════════════════════════════════════

SCHEMAS = {
    "country-intel": {
        "version": "1.0",
        "required": ["composite_score", "classification", "dimensions"],
        "optional": ["country", "lens", "risk_assessment"],
        "dimensions_schema": {
            "growth": {"score", "weight", "weighted"},
            "inflation": {"score", "weight", "weighted"},
            "external": {"score", "weight", "weighted"},
            "fiscal": {"score", "weight", "weighted"},
            "financial": {"score", "weight", "weighted"},
            "labor": {"score", "weight", "weighted"},
            "structural": {"score", "weight", "weighted"},
        },
        "consumers": ["macro-bridge.stress-test", "macro-dashboard.indicator-hub"],
        "provides": {"composite_score": "float", "dimension_scores": "dict[str,float]"},
    },

    "property-cycle": {
        "version": "1.0",
        "required": ["weighted_score", "phase", "indicators"],
        "optional": ["country", "affordability"],
        "consumers": ["country-intel.macro-health", "macro-bridge.stress-test"],
        "provides": {"cycle_phase": "str", "price_momentum": "float", "credit_growth": "float"},
    },

    "liquidity": {
        "version": "1.0",
        "required": ["net_liquidity", "regime"],
        "optional": ["scissors_factor", "global_liquidity_proxy"],
        "consumers": ["macro-bridge.liquidity-to-assets", "central-bank-watcher"],
        "provides": {"net_liquidity": "float", "regime": "str", "scissors_factor_btc": "float"},
    },

    "macro-dashboard": {
        "version": "1.0",
        "required": ["composite_score", "outlook", "dimensions"],
        "optional": ["recession_probability", "yield_curve"],
        "consumers": ["country-intel.macro-health", "macro-bridge.stress-test"],
        "provides": {"composite_score": "float", "recession_probability": "float"},
    },

    "central-bank": {
        "version": "1.0",
        "required": ["hawk_dove_score", "stance", "bank"],
        "optional": ["divergence_score", "rate_path_expectation"],
        "consumers": ["macro-bridge.rate-path", "country-intel.policy-stance", "liquidity"],
        "provides": {"hawk_dove_score": "float", "stance": "str"},
    },

    "commodity-macro": {
        "version": "1.0",
        "required": ["total_score", "phase", "factors"],
        "optional": ["asset_signals"],
        "consumers": ["macro-bridge.commodity-shock", "country-intel"],
        "provides": {"supercycle_score": "float", "phase": "str", "asset_signals": "dict"},
    },

    "fiscal-policy": {
        "version": "1.0",
        "required": ["debt_gdp_ratio", "fiscal_balance", "r_minus_g"],
        "optional": ["debt_projection", "fiscal_stance"],
        "consumers": ["country-intel.macro-health", "macro-bridge.stress-test"],
        "provides": {"debt_gdp": "float", "r_minus_g": "float", "fiscal_stance": "str"},
    },

    "macro-bridge": {
        "version": "1.0",
        "required": ["scenario", "sector_impact", "asset_impact"],
        "optional": ["country_analysis", "playbook"],
        "consumers": [],  # Terminal domain — feeds investment decisions
        "provides": {"sector_ranking": "list", "asset_ranking": "list"},
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# Cross-Domain Linker — Maps one domain's output to another's input params
# ══════════════════════════════════════════════════════════════════════════════

LINKAGES = {
    ("liquidity", "macro-bridge"): {
        "description": "Liquidity conditions → asset price signals",
        "mapping": {
            "liquidity_regime": "net_liquidity.regime",
            "scissors_btc": "scissors_factor.btc",
            "scissors_gold": "scissors_factor.gold",
            "scissors_nasdaq": "scissors_factor.nasdaq",
            "global_liquidity": "global_liquidity_proxy",
        },
    },
    ("central-bank", "macro-bridge"): {
        "description": "Central bank stance → rate path transmission",
        "mapping": {
            "rate_direction": "hawk_dove_score",
            "fed_stance": "hawk_dove_score",
            "ecb_stance": "hawk_dove_score",
            "policy_divergence": "divergence_score",
        },
    },
    ("macro-dashboard", "country-intel"): {
        "description": "Macro indicators → country health scoring",
        "mapping": {
            "growth_input": "dimensions.growth.score",
            "inflation_input": "dimensions.inflation.score",
            "labor_input": "dimensions.labor.score",
            "financial_input": "dimensions.financial.score",
        },
    },
    ("property-cycle", "country-intel"): {
        "description": "Property cycle → financial stability dimension",
        "mapping": {
            "credit_gap": "indicators.credit_growth.score",
            "price_momentum": "indicators.price_momentum.score",
            "cycle_phase": "phase",
        },
    },
    ("commodity-macro", "macro-bridge"): {
        "description": "Commodity supercycle → commodity shock transmission",
        "mapping": {
            "supercycle_phase": "phase",
            "oil_signal": "asset_signals.oil",
            "copper_signal": "asset_signals.copper",
            "battery_metals_signal": "asset_signals.battery_metals",
        },
    },
    ("fiscal-policy", "country-intel"): {
        "description": "Fiscal analysis → country health fiscal dimension",
        "mapping": {
            "debt_gdp_ratio": "debt_gdp_ratio",
            "fiscal_balance": "fiscal_balance",
            "r_minus_g": "r_minus_g",
            "fiscal_stance": "fiscal_stance",
        },
    },
}


def validate_output(domain, data):
    """Validate model output against domain schema. Returns (valid, errors)."""
    schema = SCHEMAS.get(domain)
    if not schema:
        return False, [f"Unknown domain: {domain}"]

    errors = []
    for field in schema["required"]:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    return len(errors) == 0, errors


def link_domains(source_domain, target_domain, source_output):
    """
    Transform one domain's output into another's input parameters.

    Args:
        source_domain: domain that produced the output
        target_domain: domain that will consume it
        source_output: dict output from source domain's model

    Returns:
        dict of parameters ready for target domain's model
    """
    key = (source_domain, target_domain)
    linkage = LINKAGES.get(key)
    if not linkage:
        return {"error": f"No linkage defined: {source_domain} → {target_domain}"}

    params = {"_linkage": linkage["description"]}

    for target_param, source_path in linkage["mapping"].items():
        value = _resolve_path(source_output, source_path)
        if value is not None:
            params[target_param] = value

    return params


def _resolve_path(data, path):
    """Resolve a dotted path in a nested dict. E.g., 'dimensions.growth.score'."""
    try:
        current = data
        for key in path.split("."):
            if isinstance(current, dict):
                current = current.get(key)
            elif isinstance(current, list):
                current = current[int(key)]
            else:
                return None
            if current is None:
                return None
        return current
    except (KeyError, IndexError, TypeError, ValueError):
        return None


def get_downstream_consumers(domain):
    """Get all domains that can consume output from this domain."""
    consumers = []
    for (src, tgt), linkage in LINKAGES.items():
        if src == domain:
            consumers.append({"domain": tgt, "description": linkage["description"]})
    return consumers


def get_upstream_providers(domain):
    """Get all domains that can provide input to this domain."""
    providers = []
    for (src, tgt), linkage in LINKAGES.items():
        if tgt == domain:
            providers.append({"domain": src, "description": linkage["description"]})
    return providers


def list_all_linkages():
    """List all cross-domain data flows."""
    flows = []
    for (src, tgt), linkage in sorted(LINKAGES.items()):
        flows.append({
            "from": src,
            "to": tgt,
            "description": linkage["description"],
            "params": list(linkage["mapping"].keys()),
        })
    return flows


if __name__ == "__main__":
    import sys, json

    if len(sys.argv) < 2:
        print("Cross-Domain Schema Validator & Linker")
        print("Usage:")
        print("  python3 schemas.py list                                    # List all linkages")
        print("  python3 schemas.py validate <domain> '<json_data>'        # Validate output")
        print("  python3 schemas.py link <source> <target> '<json_data>'   # Cross-domain link")
        print("  python3 schemas.py consumers <domain>                     # Show downstream consumers")
        print("  python3 schemas.py providers <domain>                     # Show upstream providers")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "list":
        for flow in list_all_linkages():
            print(f"  {flow['from']} → {flow['to']}: {flow['description']}")
            print(f"    Params: {', '.join(flow['params'])}")

    elif cmd == "validate":
        domain = sys.argv[2]
        data = json.loads(sys.argv[3]) if len(sys.argv) > 3 else json.load(sys.stdin)
        valid, errors = validate_output(domain, data)
        if valid:
            print(f"✅ {domain}: Valid")
        else:
            print(f"❌ {domain}: Invalid — {', '.join(errors)}")

    elif cmd == "link":
        src, tgt = sys.argv[2], sys.argv[3]
        data = json.loads(sys.argv[4]) if len(sys.argv) > 4 else json.load(sys.stdin)
        result = link_domains(src, tgt, data)
        print(json.dumps(result, indent=2, default=str))

    elif cmd == "consumers":
        domain = sys.argv[2]
        consumers = get_downstream_consumers(domain)
        for c in consumers:
            print(f"  → {c['domain']}: {c['description']}")

    elif cmd == "providers":
        domain = sys.argv[2]
        providers = get_upstream_providers(domain)
        for p in providers:
            print(f"  ← {p['domain']}: {p['description']}")
