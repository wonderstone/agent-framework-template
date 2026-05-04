#!/usr/bin/env python3
"""Unified data output formatters for macro-finance skills.

Converts raw economic data into consistent JSON (machine-readable) and
Markdown (human-readable) formats. All sub-domain skills use these formatters
for consistent output.

Usage:
    python3 data_formatters.py table '{"headers":["Date","GDP"],"rows":[["2024Q1",7.2],["2024Q2",7.0]]}' --format md
    python3 data_formatters.py indicator "US GDP Growth" 2.8 "%" QoQ --context "Above trend"
"""

import json
import sys
from datetime import datetime


def format_indicator(name, value, unit="", frequency="", context=""):
    """Format a single economic indicator as JSON."""
    return {
        "indicator": name,
        "value": value,
        "unit": unit,
        "frequency": frequency,
        "context": context,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


def format_indicator_md(name, value, unit="", frequency="", context=""):
    """Format a single economic indicator as Markdown."""
    lines = [f"### {name}", ""]
    lines.append(f"**Value:** {value}{f' {unit}' if unit else ''}")
    if frequency:
        lines.append(f"**Frequency:** {frequency}")
    if context:
        lines.append(f"**Context:** {context}")
    lines.append("")
    return "\n".join(lines)


def format_series(series_id, name, data_points, unit="", source=""):
    """Format a time series as JSON."""
    return {
        "series_id": series_id,
        "name": name,
        "unit": unit,
        "source": source,
        "observations": data_points,
        "count": len(data_points),
        "latest": data_points[-1] if data_points else None,
    }


def format_series_md(series_id, name, data_points, unit="", source=""):
    """Format a time series as Markdown table."""
    if not data_points:
        return f"### {name}\n\nNo data available.\n"

    lines = [f"### {name}", f"_Source: {source}_" if source else "", ""]
    lines.append("| Date | Value | Change |")
    lines.append("|------|-------|--------|")

    prev_val = None
    for i, point in enumerate(data_points[-20:]):  # last 20 points for readability
        if isinstance(point, dict):
            date = point.get("date", "")
            val = point.get("value", "")
        elif isinstance(point, (list, tuple)):
            date, val = point[0], point[1]
        else:
            date, val = "", point

        change = ""
        if prev_val is not None and isinstance(val, (int, float)) and isinstance(prev_val, (int, float)):
            pct = ((val - prev_val) / abs(prev_val)) * 100 if prev_val != 0 else 0
            change = f"{pct:+.2f}%"

        prev_val = val
        val_str = f"{val}{f' {unit}' if unit and i == len(data_points[-20:]) - 1 else ''}"
        lines.append(f"| {date} | {val_str} | {change} |")

    lines.append("")
    return "\n".join(lines)


def format_table(headers, rows, title=""):
    """Format a generic table as JSON."""
    return {
        "title": title,
        "headers": headers,
        "rows": rows,
        "row_count": len(rows),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


def format_table_md(headers, rows, title=""):
    """Format a generic table as Markdown."""
    lines = []
    if title:
        lines.append(f"### {title}")
        lines.append("")

    lines.append("| " + " | ".join(str(h) for h in headers) + " |")
    lines.append("|" + "|".join("-" * (len(str(h)) + 2) for h in headers) + "|")
    for row in rows:
        lines.append("| " + " | ".join(str(c) for c in row) + " |")
    lines.append("")
    return "\n".join(lines)


def format_risk_assessment(risks):
    """Format risk assessment as JSON. risks = list of {category, level, description}."""
    return {
        "assessment": risks,
        "overall_risk": _highest_risk(risks),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


def format_risk_assessment_md(risks):
    """Format risk assessment as Markdown table."""
    lines = ["### Risk Assessment", "", "| Category | Level | Description |", "|----------|-------|-------------|"]
    level_emoji = {"Low": "🟢", "Medium": "🟡", "High": "🟠", "Critical": "🔴"}
    for r in risks:
        emoji = level_emoji.get(r.get("level", ""), "")
        lines.append(f"| {r.get('category', '')} | {emoji} {r.get('level', '')} | {r.get('description', '')} |")
    lines.append("")
    return "\n".join(lines)


def _highest_risk(risks):
    levels = {"Low": 0, "Medium": 1, "High": 2, "Critical": 3}
    return max(risks, key=lambda r: levels.get(r.get("level", "Low"), 0))["level"] if risks else "Unknown"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: data_formatters.py <table|indicator|series|risk> <json_data> [--format json|md]")
        sys.exit(1)

    cmd = sys.argv[1]
    fmt = "json"
    if "--format" in sys.argv:
        idx = sys.argv.index("--format")
        fmt = sys.argv[idx + 1]

    if cmd == "json_to_md":
        raw = sys.stdin.read()
        data = json.loads(raw)
        print(format_series_md(data.get("series_id", ""), data.get("name", ""), data.get("data_points", [])))
    elif cmd == "indicator":
        raw = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
        if fmt == "md":
            print(format_indicator_md(**raw))
        else:
            print(json.dumps(format_indicator(**raw), indent=2, default=str))
    elif cmd == "series":
        raw = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
        if fmt == "md":
            print(format_series_md(**raw))
        else:
            print(json.dumps(format_series(**raw), indent=2, default=str))
    elif cmd == "table":
        data = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
        if fmt == "md":
            print(format_table_md(**data))
        else:
            print(json.dumps(format_table(**data), indent=2, default=str))
    elif cmd == "risk":
        risks = json.loads(sys.argv[2]) if len(sys.argv) > 2 else []
        if fmt == "md":
            print(format_risk_assessment_md(risks))
        else:
            print(json.dumps(format_risk_assessment(risks), indent=2, default=str))
