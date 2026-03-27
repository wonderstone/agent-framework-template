#!/usr/bin/env bash
# update_budget.sh
#
# Increments a budget counter in session_state.md.
#
# Usage:
#   bash scripts/execution_budget/update_budget.sh --loop
#   bash scripts/execution_budget/update_budget.sh --heavy
#   bash scripts/execution_budget/update_budget.sh --reality
#   bash scripts/execution_budget/update_budget.sh --stagnation
#
# Requires session_state.md to contain an "## Execution Budget" section
# with lines of the form:  **<Label>**: <current> / <limit>
#
# Requires: python3 (standard on macOS, Linux, and GitHub-hosted runners)
#
# Run from the repository root.

set -euo pipefail

# Pre-flight: python3 is required for in-place arithmetic editing
if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 is required but not found in PATH." >&2
  exit 1
fi

STATE_FILE="${STATE_FILE:-session_state.md}"

if [ ! -f "${STATE_FILE}" ]; then
  echo "ERROR: ${STATE_FILE} not found. Run from the repository root." >&2
  exit 1
fi

if [ $# -ne 1 ]; then
  echo "Usage: $0 --loop | --heavy | --reality | --stagnation" >&2
  exit 1
fi

# Map flag → label in session_state.md
case "$1" in
  --loop)       LABEL="Loop Count" ;;
  --heavy)      LABEL="Heavy Reasoning Calls" ;;
  --reality)    LABEL="Reality Checks" ;;
  --stagnation) LABEL="Stagnation Count" ;;
  *)
    echo "Unknown flag: $1" >&2
    echo "Usage: $0 --loop | --heavy | --reality | --stagnation" >&2
    exit 1
    ;;
esac

# Find the line, increment the current count, and write it back.
# Line format:  **Label**: <current> / <limit>
if ! grep -q "^\*\*${LABEL}\*\*:" "${STATE_FILE}"; then
  echo "ERROR: '**${LABEL}**:' not found in ${STATE_FILE}." >&2
  echo "  Ensure the file contains an '## Execution Budget' section." >&2
  exit 1
fi

# Use python3 for reliable in-place integer arithmetic (avoids sed -i portability issues)
python3 - "${STATE_FILE}" "${LABEL}" <<'PYEOF'
import sys, re

state_file = sys.argv[1]
label = sys.argv[2]

with open(state_file, "r") as f:
    content = f.read()

pattern = re.compile(
    r"^(\*\*" + re.escape(label) + r"\*\*:\s*)(\d+)(\s*/\s*\d+)",
    re.MULTILINE
)

match = pattern.search(content)
if not match:
    print(f"ERROR: could not parse '**{label}**:' line in {state_file}", file=sys.stderr)
    sys.exit(1)

current = int(match.group(2))
new_val = current + 1
new_content = pattern.sub(
    lambda m: m.group(1) + str(new_val) + m.group(3),
    content
)

with open(state_file, "w") as f:
    f.write(new_content)

print(f"  {label}: {current} → {new_val}")
PYEOF
