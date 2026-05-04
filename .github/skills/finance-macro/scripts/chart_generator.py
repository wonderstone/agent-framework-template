#!/usr/bin/env python3
"""
Chart Generator — Visual output layer for macro-finance analysis.

Generates publication-ready charts from model output JSON.
Supports: radar (macro health), bar (sector impact), line (time series),
          heatmap (cross-country), cycle (property phase).

Usage:
    # From model output
    python3 macro_score.py --growth 1.8 ... --export json | python3 chart_generator.py --type radar -o health.png

    # From stress test
    python3 stress_test.py --scenario fed-tightening --export json | python3 chart_generator.py --type bar -o sectors.png

    # Direct data
    python3 chart_generator.py --type line --data '[{"date":"2020","value":2.8},...]' -o trend.png \\
        --title "NZ GDP Growth" --ylabel "%"
"""

import json
import sys
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# Style defaults
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "#fafafa",
    "axes.edgecolor": "#cccccc",
    "axes.grid": True,
    "grid.alpha": 0.3,
    "font.family": "sans-serif",
    "font.size": 10,
    "figure.dpi": 150,
})

COLORS = {
    "blue": "#2563eb", "red": "#dc2626", "green": "#16a34a",
    "orange": "#ea580c", "purple": "#7c3aed", "teal": "#0d9488",
    "pink": "#db2777", "gray": "#6b7280", "yellow": "#ca8a04",
}

PALETTE = list(COLORS.values())


# ══════════════════════════════════════════════════════════════════════════════
# Chart Types
# ══════════════════════════════════════════════════════════════════════════════

def radar_chart(data, title="Macro Health Radar", output=None, labels=None, values=None, max_val=100):
    """
    Radar/spider chart for multi-dimensional scores.
    Expects: {"dimensions": {"name": {"score": N}, ...}} or direct labels+values.
    """
    if labels is None and values is None:
        dims = data.get("dimensions", {})
        labels = list(dims.keys())
        values = [d["score"] if isinstance(d, dict) else d for d in dims.values()]

    if not labels or not values:
        print("Error: radar chart needs labels and values")
        return None

    n = len(labels)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]  # Close the polygon

    values_plot = list(values) + [values[0]]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={"projection": "polar"})
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # Draw
    ax.fill(angles, values_plot, alpha=0.15, color=COLORS["blue"])
    ax.plot(angles, values_plot, color=COLORS["blue"], linewidth=2, marker="o", markersize=4)

    # Reference circles
    for level in [20, 40, 60, 80]:
        ax.plot(np.linspace(0, 2*np.pi, 100), [level]*100, color="#cccccc", linewidth=0.5, linestyle="--")

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([l.replace("_", " ").title() for l in labels], fontsize=9)
    ax.set_ylim(0, max_val)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(["20", "40", "60", "80", "100"], fontsize=7, color="#999999")

    # Composite score annotation
    composite = data.get("composite_score")
    classification = data.get("classification", "")
    if composite:
        ax.set_title(f"{title}\n{composite}/100 — {classification}", pad=25, fontsize=13, fontweight="bold")
    else:
        ax.set_title(title, pad=25, fontsize=13, fontweight="bold")

    return _save(fig, output, "radar")


def bar_chart(data, title="Impact Analysis", output=None, orientation="h", top_n=15):
    """
    Horizontal or vertical bar chart for rankings.
    Expects: {"sectors": [{"sector": "...", "total_impact": N}, ...]}  or  {"assets": [...]}
    """
    # Detect data structure
    items = []
    for key in ["sectors", "assets", "full_ranking", "sector_impact"]:
        if key in data:
            source = data[key]
            if isinstance(source, dict) and "full_ranking" in source:
                source = source["full_ranking"]
            if isinstance(source, list):
                for item in source:
                    name = item.get("sector") or item.get("asset") or item.get("name", "")
                    impact = item.get("total_impact") or item.get("impact") or item.get("score", 0)
                    if name:
                        items.append((name, impact))
                break

    # Fallback: try {"dimensions": ...}
    if not items and "dimensions" in data:
        for name, d in data["dimensions"].items():
            if isinstance(d, dict):
                items.append((name, d.get("score", d.get("weighted", 0))))
            else:
                items.append((name, d))

    if not items:
        # Last fallback: dict of name→value
        for k, v in data.items():
            if k.startswith("_"):
                continue
            if isinstance(v, (int, float)):
                items.append((k, v))

    if not items:
        print("Error: no plottable data found for bar chart")
        return None

    # Sort and limit
    items.sort(key=lambda x: x[1], reverse=True)
    items = items[:top_n]

    names = [item[0].replace("_", " ").title() for item in items]
    values = [item[1] for item in items]

    # Color coding: green for positive, red for negative, gray for neutral
    bar_colors = []
    for v in values:
        if v > 2:
            bar_colors.append(COLORS["green"])
        elif v > 0:
            bar_colors.append(COLORS["teal"])
        elif v > -2:
            bar_colors.append(COLORS["orange"])
        else:
            bar_colors.append(COLORS["red"])

    if orientation == "h":
        fig, ax = plt.subplots(figsize=(9, max(5, len(items) * 0.35)))
        bars = ax.barh(names, values, color=bar_colors, height=0.6)
        ax.axvline(x=0, color="black", linewidth=0.8)
        ax.invert_yaxis()
        ax.set_xlabel("Impact Score (σ units)")
    else:
        fig, ax = plt.subplots(figsize=(max(8, len(items) * 0.5), 5))
        bars = ax.bar(names, values, color=bar_colors, width=0.6)
        ax.axhline(y=0, color="black", linewidth=0.8)
        plt.xticks(rotation=45, ha="right")
        ax.set_ylabel("Impact Score (σ units)")

    # Value labels
    for bar, val in zip(bars, values):
        offset = 0.1 if val >= 0 else -0.3
        ax.text(val + offset, bar.get_y() + bar.get_height()/2,
                f"{val:+.1f}", va="center", fontsize=8, fontweight="bold")

    ax.set_title(title, fontsize=12, fontweight="bold")
    plt.tight_layout()
    return _save(fig, output, "bar")


def line_chart(data, title="Time Series", output=None, xlabel="", ylabel="", series=None):
    """
    Line chart for time series data.
    Expects: {"observations": [{"date": "...", "value": N}, ...]}  or  list of {date, value}
    """
    if series is None:
        # Auto-detect
        if isinstance(data, list):
            series = {"default": data}
        elif "observations" in data:
            series = {"default": data["observations"]}
        elif "data" in data and isinstance(data["data"], list):
            series = {"default": data["data"]}
        else:
            # Look for any list values
            for k, v in data.items():
                if k.startswith("_") or k == "observations":
                    continue
                if isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict) and "date" in v[0]:
                    series = {k: v}
                    break

    if not series:
        print("Error: no time series data found")
        return None

    fig, ax = plt.subplots(figsize=(10, 5))

    for i, (name, obs) in enumerate(series.items()):
        if not obs:
            continue
        color = PALETTE[i % len(PALETTE)]
        dates = [o.get("date", o.get("period", str(idx))) for idx, o in enumerate(obs)]
        values = [float(o.get("value", o.get("OBS_VALUE", 0))) for o in obs]

        # Truncate long date strings
        dates_display = [d[:7] if len(str(d)) > 7 else str(d) for d in dates]

        ax.plot(dates_display, values, color=color, linewidth=2, marker=".", markersize=3, label=name.replace("_", " ").title())

        # Fill below for single series
        if len(series) == 1 and len(values) > 5:
            ax.fill_between(range(len(values)), values, alpha=0.08, color=color)

    # X-axis labels — show every Nth to avoid crowding
    n_ticks = min(12, len(dates_display))
    tick_step = max(1, len(dates_display) // n_ticks)
    ax.set_xticks(range(0, len(dates_display), tick_step))
    ax.set_xticklabels([dates_display[i] for i in range(0, len(dates_display), tick_step)], rotation=45, ha="right", fontsize=8)

    if len(series) > 1:
        ax.legend(fontsize=8, loc="best")
    ax.set_title(title, fontsize=12, fontweight="bold")
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)

    # Add latest value annotation
    if values:
        ax.annotate(f"{values[-1]:.1f}", xy=(len(values)-1, values[-1]),
                    xytext=(5, 5), textcoords="offset points", fontsize=8, fontweight="bold", color=color)

    plt.tight_layout()
    return _save(fig, output, "line")


def heatmap_chart(data, title="Cross-Country Comparison", output=None, countries=None, metrics=None, values=None):
    """
    Heatmap for cross-country or cross-metric comparison.
    Expects: {"countries": {"NZL": {"metric1": val, ...}, ...}}
    """
    if values is None:
        matrix_data = data.get("countries") or data.get("matrix") or data.get("heatmap", {})
        if not matrix_data:
            # Try to construct from model output
            print("Error: heatmap needs country × metric matrix")
            return None

        countries = list(matrix_data.keys())
        if not metrics:
            # Extract common metrics from first country
            first = matrix_data[countries[0]]
            if isinstance(first, dict):
                metrics = [k for k in first.keys() if not k.startswith("_")]
                if "dimensions" in first:
                    metrics = list(first["dimensions"].keys())

        values = []
        for c in countries:
            row = []
            cd = matrix_data[c]
            for m in metrics:
                if isinstance(cd, dict):
                    if m in cd:
                        v = cd[m]
                        row.append(v.get("score", v) if isinstance(v, dict) else v)
                    elif "dimensions" in cd and m in cd["dimensions"]:
                        v = cd["dimensions"][m]
                        row.append(v.get("score", v) if isinstance(v, dict) else v)
                    else:
                        row.append(0)
                else:
                    row.append(cd)
            values.append(row)

    if not values or not countries or not metrics:
        print("Error: insufficient data for heatmap")
        return None

    values = np.array(values, dtype=float)

    fig, ax = plt.subplots(figsize=(max(6, len(metrics) * 1.2), max(4, len(countries) * 0.6)))
    im = ax.imshow(values, cmap="RdYlGn", aspect="auto", vmin=0, vmax=100)

    # Labels
    ax.set_xticks(range(len(metrics)))
    ax.set_xticklabels([m.replace("_", " ").title() for m in metrics], rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(len(countries)))
    ax.set_yticklabels(countries, fontsize=9)

    # Cell values
    for i in range(len(countries)):
        for j in range(len(metrics)):
            val = values[i, j]
            color = "white" if val < 50 else "black"
            ax.text(j, i, f"{val:.0f}", ha="center", va="center", fontsize=8, fontweight="bold", color=color)

    ax.set_title(title, fontsize=12, fontweight="bold")
    plt.colorbar(im, ax=ax, shrink=0.8, label="Score")
    plt.tight_layout()
    return _save(fig, output, "heatmap")


def cycle_phase_chart(data, title="Property Cycle Phase", output=None, phases=None):
    """
    Cycle phase visualization — timeline with phase bands.
    Expects: {"observations": [{date, value, phase?}, ...]} or manual phase list.
    """
    # Use time series + phase annotation
    if "observations" in data:
        line_chart(data, title=title, output=output, ylabel="Price Index")
        return output
    elif isinstance(data, dict) and "phase" in data:
        # Single phase classification — create phase bar
        fig, ax = plt.subplots(figsize=(10, 3))
        phase = data.get("phase", "")
        score = data.get("weighted_score", data.get("composite_score", 0))

        phases_all = ["Stabilization", "Recovery", "Boom (Early)", "Boom (Late)", "Bust (Early)", "Bust (Late)"]
        current_idx = next((i for i, p in enumerate(phases_all) if p.lower() in phase.lower()), 2)

        colors_bar = ["#16a34a", "#65a30d", "#ca8a04", "#dc2626", "#b91c1c", "#6b7280"]
        ax.barh([0], [1], color=colors_bar[current_idx], height=0.4)

        for i, p in enumerate(phases_all):
            ax.text(i/5.5, 0.35, p, ha="center", fontsize=8,
                    color="#333" if i != current_idx else "#000",
                    fontweight="bold" if i == current_idx else "normal")

        ax.set_xlim(0, 1)
        ax.set_ylim(-0.5, 0.8)
        ax.axis("off")
        ax.set_title(f"Property Cycle: {phase} (Score: {score:+.1f})", fontsize=13, fontweight="bold")
        plt.tight_layout()
        return _save(fig, output, "cycle")
    else:
        print("Error: cycle chart needs phase data")
        return None


# ══════════════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════════════

CHART_DIR = Path(__file__).resolve().parent.parent / ".charts"


def _save(fig, output, chart_type):
    """Save figure to file. Auto-generate path if not specified."""
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    path = output or str(CHART_DIR / f"{chart_type}_{_timestamp()}.png")
    fig.savefig(path, bbox_inches="tight", facecolor="white", edgecolor="none")
    plt.close(fig)
    return path


def _timestamp():
    from datetime import datetime
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def auto_detect(data):
    """Auto-detect best chart type from data structure."""
    if isinstance(data, dict):
        if "dimensions" in data:
            scores = data["dimensions"]
            if isinstance(scores, dict) and len(scores) >= 4:
                return "radar"
        if "phase" in data or "weighted_score" in data:
            return "cycle"
        if any(k in data for k in ["sectors", "assets", "sector_impact", "asset_impact", "full_ranking"]):
            return "bar"
        if "heatmap" in data or "countries" in data:
            return "heatmap"
        if "curve_shape" in data or "spreads" in data:
            return "bar"
    if isinstance(data, list):
        if len(data) > 0 and isinstance(data[0], dict) and "date" in data[0]:
            return "line"
    if isinstance(data, dict) and "observations" in data:
        return "line"
    return "bar"


# ══════════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Chart Generator for Macro-Finance Analysis")
    p.add_argument("--type", type=str, choices=["radar", "bar", "line", "heatmap", "cycle", "auto"],
                   default="auto", help="Chart type (default: auto-detect)")
    p.add_argument("--data", type=str, help="JSON data string or '-' for stdin")
    p.add_argument("--file", type=str, help="JSON data file path")
    p.add_argument("--output", "-o", type=str, help="Output file path (PNG)")
    p.add_argument("--title", type=str, default="", help="Chart title")
    p.add_argument("--ylabel", type=str, default="", help="Y-axis label")
    p.add_argument("--top-n", type=int, default=15, help="Max items for bar chart")
    args = p.parse_args()

    # Load data
    if args.file:
        with open(args.file) as f:
            data = json.load(f)
    elif args.data:
        if args.data == "-":
            data = json.load(sys.stdin)
        else:
            data = json.loads(args.data)
    else:
        # Read from stdin
        if not sys.stdin.isatty():
            data = json.load(sys.stdin)
        else:
            print("Error: provide --data, --file, or pipe JSON to stdin")
            sys.exit(1)

    chart_type = args.type
    if chart_type == "auto":
        chart_type = auto_detect(data)

    title = args.title

    # Dispatch
    if chart_type == "radar":
        path = radar_chart(data, title=title or "Macro Health Radar", output=args.output)
    elif chart_type == "bar":
        path = bar_chart(data, title=title or "Impact Analysis", output=args.output, top_n=args.top_n)
    elif chart_type == "line":
        path = line_chart(data, title=title or "Time Series", output=args.output, ylabel=args.ylabel)
    elif chart_type == "heatmap":
        path = heatmap_chart(data, title=title or "Cross-Country Comparison", output=args.output)
    elif chart_type == "cycle":
        path = cycle_phase_chart(data, title=title or "Property Cycle", output=args.output)
    else:
        print(f"Unknown chart type: {chart_type}")
        sys.exit(1)

    if path:
        print(f"Chart saved: {path}")
    else:
        print("Chart generation failed")
        sys.exit(1)
