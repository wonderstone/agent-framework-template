#!/usr/bin/env python3
"""
Snapshot tests for core macro-finance models.

Each test: known input → expected output range.
Run: python3 -m pytest tests/test_models.py -v
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"


def _run_model(script_rel_path, args_dict):
    """Run a model script with args, return parsed JSON result."""
    script = ROOT / script_rel_path
    cmd = ["python3", str(script), "--export", "json"]
    for k, v in args_dict.items():
        cmd.extend([f"--{k.replace('_', '-')}", str(v)])
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    assert result.returncode == 0, f"Model failed: {result.stderr[:300]}"
    return json.loads(result.stdout)


# ══════════════════════════════════════════════════════════════════════════════
# macro_score.py tests
# ══════════════════════════════════════════════════════════════════════════════

def test_macro_score_strong_economy():
    """Strong economy: high growth, low inflation, low unemployment."""
    result = _run_model("country-intel/scripts/macro_score.py", {
        "growth": 4.0, "inflation": 0.2, "cagdp": 3.0, "debt": 40,
        "fiscal": 1.0, "unemployment": 3.0, "creditgap": -5, "npl": 1.0, "governance": 1.8,
    })
    assert result["composite_score"] > 70, f"Expected >70, got {result['composite_score']}"
    assert result["classification"] in ("Good", "Excellent")
    assert result["dimensions"]["growth"]["score"] >= 80
    assert result["dimensions"]["inflation"]["score"] >= 80


def test_macro_score_weak_economy():
    """Weak economy: low growth, high inflation, high unemployment."""
    result = _run_model("country-intel/scripts/macro_score.py", {
        "growth": 0.5, "inflation": 5.0, "cagdp": -8.0, "debt": 130,
        "fiscal": -7.0, "unemployment": 10.0, "creditgap": 25, "npl": 10.0, "governance": -0.5,
    })
    assert result["composite_score"] < 45, f"Expected <45, got {result['composite_score']}"
    assert result["classification"] in ("Weak", "Poor", "Critical")
    assert result["dimensions"]["growth"]["score"] <= 40
    assert result["dimensions"]["external"]["score"] <= 25


# ══════════════════════════════════════════════════════════════════════════════
# cycle_score.py tests
# ══════════════════════════════════════════════════════════════════════════════

def test_cycle_score_boom():
    """Boom phase: high price momentum, strong credit, tight inventory."""
    result = _run_model("property-cycle/scripts/cycle_score.py", {
        "price-yoy": 12.0, "price-income-vs-lt": 1.35, "credit-yoy": 15.0,
        "approvals-yoy": 25.0, "inventory-months": 1.2, "auction-clearance": 85,
        "investor-share": 38,
    })
    assert result["weighted_score"] > 1.0, f"Expected boom signal, got {result['weighted_score']}"
    assert "Boom" in result["phase"] or "Transition" in result["phase"]
    assert result["indicators"]["price_momentum"]["score"] >= 1.5


def test_cycle_score_bust():
    """Bust phase: deeply negative price momentum, credit collapse, high inventory."""
    result = _run_model("property-cycle/scripts/cycle_score.py", {
        "price-yoy": -20.0, "price-income-vs-lt": 0.60, "credit-yoy": -12.0,
        "approvals-yoy": -50.0, "inventory-months": 15.0, "auction-clearance": 20,
        "investor-share": 5,
    })
    assert result["weighted_score"] < -0.5, f"Expected bust signal, got {result['weighted_score']}"
    assert "Bust" in result["phase"] or "Stabilization" in result["phase"]


def test_cycle_score_transition():
    """Transition: flat prices, moderate credit, mixed signals."""
    result = _run_model("property-cycle/scripts/cycle_score.py", {
        "price-yoy": 1.5, "price-income-vs-lt": 1.05, "credit-yoy": 2.0,
        "approvals-yoy": -5.0, "inventory-months": 5.0, "auction-clearance": 58,
        "investor-share": 22,
    })
    assert -3 <= result["weighted_score"] <= 4, f"Expected transition, got {result['weighted_score']}"


# ══════════════════════════════════════════════════════════════════════════════
# affordability_calc.py tests
# ══════════════════════════════════════════════════════════════════════════════

def test_affordability_affordable():
    """Affordable market: low P/I, low mortgage burden."""
    result = _run_model("property-cycle/scripts/affordability_calc.py", {
        "price": 300000, "income": 100000, "rent": 1500, "rate": 4.0, "term": 25,
    })
    m = result["metrics"]
    assert m["price_to_income"]["value"] < 4.0, f"Expected P/I<4, got {m['price_to_income']['value']}"
    assert m["mortgage_burden_pct"]["value"] < 30, f"Expected burden<30%, got {m['mortgage_burden_pct']['value']}"
    assert m["price_to_income"]["status"] in ("Affordable", "Moderately Unaffordable")


def test_affordability_severe():
    """Severely unaffordable: high P/I, high mortgage burden."""
    result = _run_model("property-cycle/scripts/affordability_calc.py", {
        "price": 1200000, "income": 85000, "rent": 3500, "rate": 7.0, "term": 25,
    })
    m = result["metrics"]
    assert m["price_to_income"]["value"] > 8.0, f"Expected P/I>8, got {m['price_to_income']['value']}"
    assert m["mortgage_burden_pct"]["value"] > 50, f"Expected burden>50%, got {m['mortgage_burden_pct']['value']}"
    assert m["affordability_index"]["value"] < 60, f"Expected index<60, got {m['affordability_index']['value']}"


# ══════════════════════════════════════════════════════════════════════════════
# supercycle_scorer.py tests
# ══════════════════════════════════════════════════════════════════════════════

def test_supercycle_active():
    """Active supercycle: strong across all factors."""
    result = _run_model("commodity-macro/scripts/supercycle_scorer.py", {
        "industrialization": 18, "capex-gdp": 2.5, "demand-shift": 18,
        "inventory": 50, "producer-discipline": 17,
        "india-infra": 260, "ev-penetration": 25, "opec-compliance": 90,
    })
    assert result["total_score"] > 70, f"Expected >70, got {result['total_score']}"
    assert "Confirmed" in result["phase"] or "Likely" in result["phase"]
    assert result["asset_signals"]["copper"].startswith("Strongly Bullish") or result["asset_signals"]["copper"].startswith("Bullish")


def test_supercycle_inactive():
    """No supercycle: weak across all factors."""
    result = _run_model("commodity-macro/scripts/supercycle_scorer.py", {
        "industrialization": 6, "capex-gdp": 8.0, "demand-shift": 5,
        "inventory": 130, "producer-discipline": 5,
        "opec-compliance": 40, "ev-penetration": 5,
    })
    assert result["total_score"] < 45, f"Expected <45, got {result['total_score']}"
    assert "No Clear" in result["phase"] or "Unlikely" in result["phase"]


# ══════════════════════════════════════════════════════════════════════════════
# indicator_hub.py tests
# ══════════════════════════════════════════════════════════════════════════════

def test_indicator_hub_strong():
    """Strong macro: high growth, low inflation, tight labor, easy financial."""
    result = _run_model("macro-dashboard/scripts/indicator_hub.py", {
        "gdp": 3.5, "indpro": 3.0, "retail": 5.0, "pmi": 56, "caputil": 80,
        "core-pce": 2.0, "core-cpi": 2.5, "unrate": 3.5, "nfp": 250, "claims": 200,
        "fedfunds": 3.0, "spread": 1.2, "bbb": 1.3, "vix": 14,
    })
    assert result["composite_score"] > 65
    assert result["recession_probability"] < 20
    assert result["recession_risk_level"] == "Low" or result["recession_risk_level"] == "Moderate"


def test_indicator_hub_weak():
    """Weak macro: negative growth, high inflation, rising unemployment, inverted curve."""
    result = _run_model("macro-dashboard/scripts/indicator_hub.py", {
        "gdp": -1.0, "indpro": -3.0, "retail": -2.0, "pmi": 43, "caputil": 72,
        "core-pce": 4.5, "core-cpi": 5.5, "unrate": 6.5, "nfp": 20, "claims": 320,
        "fedfunds": 5.5, "spread": -0.8, "bbb": 3.5, "vix": 32,
    })
    assert result["composite_score"] < 40
    assert result["recession_probability"] > 50
    assert result["recession_risk_level"] in ("Elevated", "High")


# ══════════════════════════════════════════════════════════════════════════════
# yield_curve.py tests
# ══════════════════════════════════════════════════════════════════════════════

def test_yield_curve_inverted():
    """Inverted curve: 2Y > 10Y, high recession probability."""
    result = _run_model("macro-dashboard/scripts/yield_curve.py", {
        "dgs2": 5.50, "dgs10": 4.80, "dtb3": 5.75, "fedfunds": 5.50,
        "tips10": 2.50, "breakeven5": 2.30, "bbb": 2.50,
    })
    assert "Inverted" in result["curve_shape"]
    assert result["recession_probability_12m"] > 50
    assert result["spreads"]["10y2y"] < 0


def test_yield_curve_normal():
    """Normal curve: 10Y > 2Y, low recession probability."""
    result = _run_model("macro-dashboard/scripts/yield_curve.py", {
        "dgs2": 3.50, "dgs10": 4.50, "dtb3": 3.00, "fedfunds": 3.25,
        "tips10": 1.50, "breakeven5": 2.20, "bbb": 1.50,
    })
    assert "Normal" in result["curve_shape"] or "Steep" in result["curve_shape"]
    assert result["recession_probability_12m"] < 20
    assert result["spreads"]["10y2y"] > 0


# ══════════════════════════════════════════════════════════════════════════════
# Cross-domain schemas tests
# ══════════════════════════════════════════════════════════════════════════════

def test_schema_validation():
    sys.path.insert(0, str(SCRIPTS))
    from schemas import validate_output, link_domains, list_all_linkages

    # Validate valid output
    valid_data = {"composite_score": 70, "classification": "Good", "dimensions": {}}
    ok, errs = validate_output("country-intel", valid_data)
    assert ok, f"Should be valid: {errs}"

    # Validate invalid output
    invalid_data = {"classification": "Good"}
    ok, errs = validate_output("country-intel", invalid_data)
    assert not ok

    # Test linkage
    liquidity_output = {
        "net_liquidity": 5.8, "regime": "Expansion",
        "scissors_factor": {"btc": 2.5, "gold": 1.8, "nasdaq": 0.5},
        "global_liquidity_proxy": 12.0,
    }
    params = link_domains("liquidity", "macro-bridge", liquidity_output)
    assert params["scissors_btc"] == 2.5
    assert params["scissors_gold"] == 1.8
    assert params["scissors_btc"] == 2.5

    # Verify all linkages defined
    flows = list_all_linkages()
    assert len(flows) >= 6


# ══════════════════════════════════════════════════════════════════════════════
# Stress test engine tests
# ══════════════════════════════════════════════════════════════════════════════

def test_stress_test_scenarios():
    sys.path.insert(0, str(ROOT / "macro-bridge" / "scripts"))
    from stress_test import run_stress_test

    # Pre-built scenario
    report = run_stress_test(scenario="fed-tightening", country="NZL")
    assert "error" not in report
    assert len(report["sector_impact"]["full_ranking"]) == 12
    assert len(report["asset_impact"]["full_ranking"]) == 8
    assert report["country_analysis"]["country"] == "NZL"
    assert len(report["context"]["playbook"]) >= 3

    # Custom scenario
    report2 = run_stress_test(custom_shocks={"rate": 1.0, "usd": 0.5, "oil": -2.0, "liquidity": -1.5})
    assert report2["shock_parameters"]["rate"] == 1.0

    # Override
    report3 = run_stress_test(scenario="global-recession", overrides={"oil": -4.0})
    assert report3["shock_parameters"]["oil"] == -4.0


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v", "--tb=short"]))
