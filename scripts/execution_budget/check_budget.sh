#!/usr/bin/env bash
# check_budget.sh
#
# Reads the Execution Budget section from session_state.md, compares
# current counts against limits, and prints a structured report.
#
# Exit codes:
#   0 — budget healthy or constrained (agent may continue with restrictions)
#   1 — budget exhausted (autonomous progression must stop)
#
# Usage:
#   bash scripts/execution_budget/check_budget.sh
#   bash scripts/execution_budget/check_budget.sh session_state.md
#
# Run from the repository root.

set -euo pipefail

STATE_FILE="${1:-${STATE_FILE:-session_state.md}}"

if [ ! -f "${STATE_FILE}" ]; then
  echo "ERROR: ${STATE_FILE} not found. Run from the repository root." >&2
  exit 1
fi

python3 - "${STATE_FILE}" <<'PYEOF'
import sys, re

state_file = sys.argv[1]

with open(state_file, "r") as f:
    content = f.read()

def read_counter(label):
    """Return (current, limit) for a budget label, or None if not found."""
    pattern = re.compile(
        r"^\*\*" + re.escape(label) + r"\*\*:\s*(\d+)\s*/\s*(\d+)",
        re.MULTILINE
    )
    m = pattern.search(content)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))

LABELS = [
    ("Loop Count",            "loop"),
    ("Heavy Reasoning Calls", "heavy"),
    ("Reality Checks",        "reality"),
    ("Stagnation Count",      "stagnation"),
]

counters = {}
missing = []
for label, key in LABELS:
    result = read_counter(label)
    if result is None:
        missing.append(label)
    else:
        counters[key] = (label, result[0], result[1])

if missing:
    print("ERROR: Missing budget fields in session_state.md:", file=sys.stderr)
    for m in missing:
        print(f"  - **{m}**", file=sys.stderr)
    print("  Ensure the file contains an '## Execution Budget' section.", file=sys.stderr)
    sys.exit(1)

# ── Evaluate budget ───────────────────────────────────────────────────────────

def pct(current, limit):
    return current / limit if limit > 0 else 1.0

heavy_blocked    = counters["heavy"][1]    >= counters["heavy"][2]
reality_blocked  = counters["reality"][1]  >= counters["reality"][2]
stagnation_warn  = counters["stagnation"][1] >= counters["stagnation"][2]
loop_exhausted   = counters["loop"][1]     >= counters["loop"][2]

autonomous_progression_allowed = not loop_exhausted and not stagnation_warn

# Overall status
if loop_exhausted or stagnation_warn:
    status = "exhausted"
elif heavy_blocked or reality_blocked:
    status = "constrained"
else:
    status = "healthy"

# ── Print report ──────────────────────────────────────────────────────────────

print("Execution Budget Report")
for label, key in [
    ("Loop Count",            "loop"),
    ("Heavy Reasoning Calls", "heavy"),
    ("Reality Checks",        "reality"),
    ("Stagnation Count",      "stagnation"),
]:
    _, current, limit = counters[key]
    print(f"- {label}: {current} / {limit}")

print(f"- Budget Status: {status}")
print()
print("Budget Enforcement")
print(f"- Autonomous progression allowed: {'YES' if autonomous_progression_allowed else 'NO'}")
print(f"- Heavy reasoning allowed: {'YES' if not heavy_blocked else 'NO'}")
print(f"- Reality check allowed: {'YES' if not reality_blocked else 'NO'}")

if stagnation_warn:
    required = "STOP"
elif loop_exhausted:
    required = "STOP"
else:
    required = "CONTINUE or ESCALATE"

print(f"- Required action if no progress next cycle: {required}")

# Exit 1 when progression must stop
if not autonomous_progression_allowed:
    sys.exit(1)

sys.exit(0)
PYEOF
