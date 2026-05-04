#!/usr/bin/env python3
"""
Macro Stress Test Engine — Parametric Scenario Analysis

Connects pre-built macro scenarios to sector/asset impact matrices.
Accepts parameter overrides for interactive "what-if" analysis.

Combines:
  - sector_mapper.py: quantitative shock → sector/asset impact
  - scenario markdown files: qualitative context, playbooks, monitoring triggers
  - country_profiles: country-specific vulnerability assessment

Usage:
    python3 stress_test.py --scenario fed-tightening
    python3 stress_test.py --scenario global-recession --country NZL
    python3 stress_test.py --scenario geopolitical-shock --override oil=+3.5,usd=+2.0
    python3 stress_test.py --custom rate=+1.5,usd=+1.0,oil=-1.0,liquidity=-2.5
    python3 stress_test.py --list
"""

import json
import sys
from pathlib import Path

# Import sector mapper
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from sector_mapper import (
    SCENARIOS, SECTOR_SENSITIVITY, ASSET_SENSITIVITY,
    map_shock_to_sectors, map_shock_to_assets, _classify_impact,
)

# ══════════════════════════════════════════════════════════════════════════════
# Extended Scenario Context — Playbooks, Triggers, Country Impacts
# ══════════════════════════════════════════════════════════════════════════════

SCENARIO_CONTEXT = {
    "fed-tightening": {
        "trigger_conditions": [
            "Core PCE 3-month annualized > 3.5%",
            "Average hourly earnings > 5% YoY",
            "Fed rhetoric shift from 'patient' to 'vigilant'",
            "Market pricing > 50bp of additional hikes",
            "Initial claims rising above 280K (demand destruction taking hold)",
        ],
        "playbook": [
            "Reduce growth/duration exposure (tech, REITs, long-duration bonds)",
            "Rotate to floating-rate assets (bank loans, FRNs)",
            "Add USD exposure (strong dollar beneficiaries)",
            "Defensive equity rotation (staples, healthcare, utilities)",
            "Reduce crypto/EM exposure — most liquidity-sensitive",
        ],
        "winners": ["banks", "usd_dxy", "treasuries (front-end)", "defensive equities"],
        "losers": ["technology", "real_estate", "crypto", "em_equities", "consumer_disc"],
    },
    "fed-easing": {
        "trigger_conditions": [
            "Core PCE convincingly below 2.5%",
            "Unemployment rising > 0.5pp from trough",
            "Fed signals 'insurance cuts' or 'recalibration'",
            "Market pricing > 100bp of cuts over 12 months",
        ],
        "playbook": [
            "Extend duration (long bonds, growth stocks benefit from lower discount rates)",
            "Small caps and cyclicals benefit (funding costs decline)",
            "Gold and Bitcoin benefit (lower real rates, weaker USD)",
            "REITs recover (lower cap rates = higher property values)",
            "EM equities benefit (weaker USD, capital inflows)",
        ],
        "winners": ["technology", "real_estate", "gold", "BTC", "em_equities", "small_caps"],
        "losers": ["usd_dxy", "banks (NIM compression)", "cash/money-market"],
    },
    "global-recession": {
        "trigger_conditions": [
            "US ISM Manufacturing < 45",
            "Global PMI composite < 48",
            "Initial claims > 300K and rising",
            "HY OAS > 500bp",
            "Fed emergency cut or inter-meeting cut",
            "Sahm Rule triggered (unemployment +0.50pp from trough)",
        ],
        "playbook": [
            "Phase 1 (Pre-recession): Reduce cyclical, add duration, build cash",
            "Phase 2 (Early recession): Defensive rotation — staples, healthcare, gold",
            "Phase 3 (Mid recession): Start scaling into quality cyclicals, extend bond duration",
            "Phase 4 (Recovery): Aggressive risk-on — small caps, cyclicals, EM",
        ],
        "winners": ["treasuries (long end)", "gold", "gold_miners", "healthcare", "consumer_staple"],
        "losers": ["energy", "banks", "crypto", "industrials", "consumer_disc"],
    },
    "commodity-supercycle": {
        "trigger_conditions": [
            "Global copper inventories < 3 weeks of demand",
            "Mining capex / GDP at multi-year lows",
            "Multiple commodities above 90th percentile (5Y range)",
            "China + India combined commodity demand growth > 5% YoY",
            "Producer equity valuations implying commodity prices far below spot",
        ],
        "playbook": [
            "Overweight mining/energy equities — direct beneficiaries",
            "Long commodity FX (AUD, NZD, CAD, BRL, CLP) vs JPY/CHF",
            "Inflation hedge assets (TIPS, gold, commodity futures)",
            "Underweight EM manufacturing importers (INR, TRY, PHP)",
            "Watch for demand destruction in energy-intensive sectors (airlines, chemicals)",
        ],
        "winners": ["energy", "materials", "gold_miners", "AUD", "NZD", "CAD", "BRL"],
        "losers": ["consumer_disc", "em_manufacturing_importers", "airlines"],
    },
    "geopolitical-shock": {
        "trigger_conditions": [
            "US/NATO military posture change (DEFCON, troop movements)",
            "Shipping insurance premiums spiking (war risk premiums)",
            "Semiconductor export controls tightened (ASML, TSMC restrictions)",
            "Oil above $120/bbl sustained for > 2 weeks",
            "Taiwan Strait: PLA exercises inside ADIZ / territorial waters",
            "Gold above nominal ATH — risk-off signal confirmation",
        ],
        "playbook": [
            "Immediate: Flight to safety — gold, USD, CHF, JPY, Treasuries",
            "Defense sector overweight — spending supercycle in motion",
            "Energy overweight (supply disruption premium)",
            "Reduce Taiwan/Korea/Japan equity exposure",
            "Cybersecurity overweight (cyber warfare escalation)",
        ],
        "winners": ["defense", "energy", "gold", "gold_miners", "cybersecurity", "usd"],
        "losers": ["semiconductors", "airlines", "consumer_disc", "crypto", "em_equities"],
    },
    "china-reopening": {
        "trigger_conditions": [
            "China PMI above 52 for 3 consecutive months",
            "Credit impulse turning positive (> +3% of GDP)",
            "PBOC shifts from 'prudent' to 'moderately loose'",
            "Property sales volume stabilizing (3-month moving average)",
            "Commodity imports (copper, iron ore) rising > 10% YoY",
        ],
        "playbook": [
            "Overweight commodity exporters (AUD, NZD, CLP, BRL)",
            "Long industrial metals (copper, iron ore)",
            "China A-shares / H-shares re-rating potential",
            "Luxury goods / consumer (Chinese tourist spending)",
            "Watch for inflation impulse through commodity channel",
        ],
        "winners": ["materials", "energy", "luxury_goods", "AUD", "NZD", "em_equities"],
        "losers": ["usd_dxy (weaker on reflation)", "manufacturing_importers"],
    },
}

COUNTRY_VULNERABILITY = {
    "NZL": {
        "fed-tightening": "High — 1-2Y fixed mortgages = fast rate passthrough. RBNZ typically hikes alongside Fed.",
        "global-recession": "High — small open economy, commodity export dependent, chronic CA deficit",
        "commodity-supercycle": "Beneficiary — dairy/meat exporter, NZD rallies on commodity demand",
        "geopolitical-shock": "Moderate — remote location, food exporter, but supply chain dependent",
        "fed-easing": "Beneficiary — lower rates boost housing/consumption, NZD initially weakens then recovers",
        "china-reopening": "Strong beneficiary — dairy/meat/wood exports to China, tourism boost",
    },
    "AUS": {
        "fed-tightening": "High — similar mortgage structure to NZ, variable rate exposure",
        "global-recession": "Moderate — commodity exporter but China demand matters more",
        "commodity-supercycle": "Strong beneficiary — iron ore, coal, LNG exports surge",
        "geopolitical-shock": "Moderate — energy/minerals exporter benefits, but China proximity risk",
        "china-reopening": "Strong beneficiary — #1 commodity supplier to China",
    },
    "USA": {
        "fed-tightening": "Moderate — 30Y fixed mortgages insulate consumers, but growth/tech hit",
        "global-recession": "Moderate — safe haven inflows, but domestic demand hit",
        "commodity-supercycle": "Neutral/mixed — energy independent, but inflation headwind",
        "geopolitical-shock": "Beneficiary — safe haven inflows, defense industry, energy independent",
    },
    "JPN": {
        "fed-tightening": "Moderate — BOJ divergence, JPY weakness boosts exporters",
        "global-recession": "High — export-dependent, JPY strength on carry unwind",
        "commodity-supercycle": "Vulnerable — commodity importer, energy dependent (92% imported)",
        "geopolitical-shock": "Very high — Taiwan proximity, energy import dependency",
    },
    "CHN": {
        "fed-tightening": "Vulnerable — capital outflow pressure, CNY depreciation risk",
        "global-recession": "Moderate — domestic policy space, but export demand hit",
        "commodity-supercycle": "Vulnerable (consumer) but beneficiary if demand-driven",
        "geopolitical-shock": "Extreme (if Taiwan/South China Sea) — export collapse, supply chain disruption",
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# Stress Test Engine
# ══════════════════════════════════════════════════════════════════════════════

def run_stress_test(scenario=None, country=None, custom_shocks=None, overrides=None):
    """
    Run a complete macro stress test.

    Args:
        scenario: pre-built scenario name (fed-tightening, global-recession, etc.)
        country: ISO3 country code for country-specific vulnerability analysis
        custom_shocks: dict of {shock_type: magnitude} for fully custom scenarios
        overrides: dict of {shock_type: magnitude} to override scenario defaults

    Returns:
        Complete stress test report
    """
    # Resolve shocks
    if scenario and scenario in SCENARIOS:
        shocks = dict(SCENARIOS[scenario]["shocks"])
        description = SCENARIOS[scenario]["description"]
    elif custom_shocks:
        shocks = dict(custom_shocks)
        description = "Custom scenario"
        scenario = "custom"
    else:
        return {"error": "Specify --scenario or --custom shocks", "available": list(SCENARIOS.keys())}

    # Apply overrides
    if overrides:
        for k, v in overrides.items():
            shocks[k] = v
        description += " (with overrides)"

    # Run sector/asset mapping
    sector_impacts = map_shock_to_sectors(shocks)
    asset_impacts = map_shock_to_assets(shocks)

    # Get scenario context
    context = SCENARIO_CONTEXT.get(scenario, {})

    # Country vulnerability
    country_analysis = None
    if country and country in COUNTRY_VULNERABILITY:
        vuln = COUNTRY_VULNERABILITY[country]
        country_analysis = {
            "country": country,
            "scenario_vulnerability": vuln.get(scenario, "No specific data"),
        }

    # Build report
    report = {
        "scenario": scenario,
        "description": description,
        "shock_parameters": shocks,
        "sector_impact": {
            "top_winners": [s for s in sector_impacts if s["total_impact"] > 0.5][:5],
            "top_losers": [s for s in sector_impacts if s["total_impact"] < -0.5][-5:],
            "full_ranking": sector_impacts,
        },
        "asset_impact": {
            "top_winners": [a for a in asset_impacts if a["total_impact"] > 0.5][:5],
            "top_losers": [a for a in asset_impacts if a["total_impact"] < -0.5][-5:],
            "full_ranking": asset_impacts,
        },
        "context": {
            "trigger_conditions": context.get("trigger_conditions", []),
            "playbook": context.get("playbook", []),
            "natural_winners": context.get("winners", []),
            "natural_losers": context.get("losers", []),
        },
        "country_analysis": country_analysis,
        "sensitivity_note": _sensitivity_note(shocks, scenario),
    }

    return report


def _sensitivity_note(shocks, scenario):
    """Generate sensitivity/confidence assessment."""
    notes = []

    # Which channels are dominant in this scenario
    dominant = max(shocks.items(), key=lambda x: abs(x[1]))
    notes.append(f"Dominant channel: {dominant[0]} (magnitude: {dominant[1]:+.1f}σ)")

    # Confidence by channel
    high_conf = ["rate", "liquidity"]
    med_conf = ["usd", "oil"]
    if dominant[0] in high_conf:
        notes.append("Confidence: HIGH — this channel has well-established transmission mechanics")
    elif dominant[0] in med_conf:
        notes.append("Confidence: MEDIUM — direction clear, magnitude uncertain")
    else:
        notes.append("Confidence: MODERATE — second-order effects may dominate")

    # Scenario-specific
    if scenario == "global-recession" and shocks.get("rate", 0) < -1:
        notes.append("Rate cuts already priced — watch for 'priced in' risk")
    if scenario == "geopolitical-shock" and shocks.get("oil", 0) > 2:
        notes.append("Oil supply shock magnitude is inherently unpredictable — wide confidence bands")

    return notes


# ══════════════════════════════════════════════════════════════════════════════
# Formatter
# ══════════════════════════════════════════════════════════════════════════════

def format_report(report, fmt="markdown"):
    """Format stress test report as markdown or JSON."""
    if fmt == "json":
        return json.dumps(report, indent=2, default=str)

    lines = []
    lines.append(f"## Stress Test: {report['scenario']}")
    lines.append(f"**{report['description']}**")
    lines.append("")

    # Shock parameters
    lines.append("### Shock Parameters")
    lines.append("| Channel | Magnitude |")
    lines.append("|---------|-----------|")
    for ch, mag in report["shock_parameters"].items():
        direction = "↑" if mag > 0 else "↓"
        lines.append(f"| {ch} | {direction} {abs(mag):.1f}σ |")
    lines.append("")

    # Sector impact
    lines.append("### Sector Impact — Top Winners & Losers")
    lines.append("| Sector | Impact | Signal |")
    lines.append("|--------|--------|--------|")
    for s in report["sector_impact"]["full_ranking"]:
        emoji = "🟢" if s["total_impact"] > 2 else ("🟡" if s["total_impact"] > 0 else ("🟠" if s["total_impact"] > -2 else "🔴"))
        lines.append(f"| {emoji} {s['sector'].replace('_', ' ').title()} | {s['total_impact']:+.1f} | {s['signal']} |")
    lines.append("")

    # Asset impact
    lines.append("### Asset Impact — Top Winners & Losers")
    lines.append("| Asset | Impact | Signal |")
    lines.append("|-------|--------|--------|")
    for a in report["asset_impact"]["full_ranking"]:
        emoji = "🟢" if a["total_impact"] > 2 else ("🟡" if a["total_impact"] > 0 else ("🟠" if a["total_impact"] > -2 else "🔴"))
        lines.append(f"| {emoji} {a['asset']} | {a['total_impact']:+.1f} | {a['signal']} |")
    lines.append("")

    # Playbook
    if report["context"]["playbook"]:
        lines.append("### Playbook")
        for i, step in enumerate(report["context"]["playbook"], 1):
            lines.append(f"{i}. {step}")
        lines.append("")

    # Monitoring triggers
    if report["context"]["trigger_conditions"]:
        lines.append("### Monitoring Triggers")
        for trigger in report["context"]["trigger_conditions"]:
            lines.append(f"- [ ] {trigger}")
        lines.append("")

    # Country analysis
    if report.get("country_analysis"):
        ca = report["country_analysis"]
        lines.append(f"### Country Impact: {ca['country']}")
        lines.append(f"{ca['scenario_vulnerability']}")
        lines.append("")

    # Sensitivity notes
    if report.get("sensitivity_note"):
        lines.append("### Confidence Assessment")
        for note in report["sensitivity_note"]:
            lines.append(f"- {note}")
        lines.append("")

    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Macro Stress Test Engine")
    p.add_argument("--scenario", type=str, help="Pre-built scenario name")
    p.add_argument("--country", type=str, help="ISO3 country code for country-specific analysis")
    p.add_argument("--custom", type=str, help="Custom shocks: 'rate=+1.5,usd=+0.8,oil=-1.0'")
    p.add_argument("--override", type=str, help="Override scenario params: 'oil=+3.0,rate=-0.5'")
    p.add_argument("--list", action="store_true", help="List available scenarios")
    p.add_argument("--export", type=str, default="text", help="text|markdown|json")
    args = p.parse_args()

    if args.list:
        print("Available Scenarios:")
        for name, sc in SCENARIOS.items():
            ctx = SCENARIO_CONTEXT.get(name, {})
            triggers = len(ctx.get("trigger_conditions", []))
            print(f"  {name:<25} — {sc['description']}")
            print(f"    Shocks: {sc['shocks']}  |  Triggers: {triggers} conditions")
        print(f"\nAvailable countries: {', '.join(sorted(COUNTRY_VULNERABILITY.keys()))}")
        sys.exit(0)

    if not args.scenario and not args.custom:
        p.print_help()
        print("\nExample: python3 stress_test.py --scenario fed-tightening --country NZL")
        print("         python3 stress_test.py --list")
        sys.exit(1)

    # Parse custom/override shocks
    custom_shocks = None
    if args.custom:
        custom_shocks = {}
        for pair in args.custom.split(","):
            k, v = pair.strip().split("=")
            custom_shocks[k.strip()] = float(v.strip())

    overrides = None
    if args.override:
        overrides = {}
        for pair in args.override.split(","):
            k, v = pair.strip().split("=")
            overrides[k.strip()] = float(v.strip())

    report = run_stress_test(
        scenario=args.scenario,
        country=args.country,
        custom_shocks=custom_shocks,
        overrides=overrides,
    )

    if "error" in report:
        print(json.dumps(report, indent=2))
        sys.exit(1)

    if args.export == "json":
        print(format_report(report, "json"))
    else:
        print(format_report(report, "markdown"))
