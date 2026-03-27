#!/usr/bin/env bash
# enforce_pipeline.sh
#
# Atomic pipeline enforcement wrapper.
#
# Runs update_budget.sh (for the given event type) then check_budget.sh, prints
# a formatted Pipeline Status Summary, and hard-fails (exit 1) when the pipeline
# is BLOCKED or DEGRADED to indicate the agent must stop or operate in lightweight
# mode.
#
# Usage:
#   bash scripts/execution_budget/enforce_pipeline.sh --loop
#   bash scripts/execution_budget/enforce_pipeline.sh --heavy
#   bash scripts/execution_budget/enforce_pipeline.sh --reality
#   bash scripts/execution_budget/enforce_pipeline.sh --stagnation
#
# Optional positional argument: path to session_state.md
#   bash scripts/execution_budget/enforce_pipeline.sh --loop path/to/session_state.md
#
# Exit codes:
#   0 — PIPELINE OK (healthy; full execution permitted)
#   2 — PIPELINE DEGRADED: constrained (lightweight execution only)
#   1 — PIPELINE BLOCKED: exhausted (must stop; do not continue)
#
# Run from the repository root.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Argument parsing ──────────────────────────────────────────────────────────

if [ $# -lt 1 ]; then
  echo "Usage: $0 --loop | --heavy | --reality | --stagnation [session_state.md]" >&2
  exit 1
fi

EVENT_FLAG="$1"
STATE_FILE="${2:-${STATE_FILE:-session_state.md}}"

case "${EVENT_FLAG}" in
  --loop|--heavy|--reality|--stagnation) ;;
  *)
    echo "Unknown event flag: ${EVENT_FLAG}" >&2
    echo "Usage: $0 --loop | --heavy | --reality | --stagnation [session_state.md]" >&2
    exit 1
    ;;
esac

# ── Stage 1 — Update Budget State ────────────────────────────────────────────

echo "━━━ Pipeline Enforcement ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Stage 1 — Update Budget State (${EVENT_FLAG})"
STATE_FILE="${STATE_FILE}" bash "${SCRIPT_DIR}/update_budget.sh" "${EVENT_FLAG}"

# ── Stage 2 — Check Budget (capture output) ──────────────────────────────────

echo ""
echo "Stage 2 — Budget Check"
BUDGET_OUTPUT="$(STATE_FILE="${STATE_FILE}" bash "${SCRIPT_DIR}/check_budget.sh" "${STATE_FILE}" 2>&1)" || BUDGET_EXIT=$?
BUDGET_EXIT="${BUDGET_EXIT:-0}"

echo "${BUDGET_OUTPUT}"

# ── Parse key fields ─────────────────────────────────────────────────────────

EXECUTION_MODE="$(echo "${BUDGET_OUTPUT}" | grep -m1 '^- Execution Mode:' | sed 's/- Execution Mode: //')"
HEAVY_ALLOWED="$(echo "${BUDGET_OUTPUT}" | grep -m1 '^- Heavy reasoning allowed:' | sed 's/- Heavy reasoning allowed: //')"
REALITY_ALLOWED="$(echo "${BUDGET_OUTPUT}" | grep -m1 '^- Reality check allowed:' | sed 's/- Reality check allowed: //')"
PIPELINE_LINE="$(echo "${BUDGET_OUTPUT}" | grep -m1 '^PIPELINE')"

# ── Stage 3 — Pipeline Status Summary ────────────────────────────────────────

echo ""
echo "━━━ Pipeline Status Summary ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Mode             : ${EXECUTION_MODE}"
echo "Heavy reasoning  : ${HEAVY_ALLOWED}"
echo "Reality check    : ${REALITY_ALLOWED}"
echo ""

case "${EXECUTION_MODE}" in
  healthy)
    echo "✅  ${PIPELINE_LINE}"
    echo ""
    echo "Allowed actions  : full execution"
    echo "Next required    : proceed with task"
    ;;
  constrained)
    echo "⚠️   ${PIPELINE_LINE}"
    echo ""
    echo "Allowed actions  : direct continuation only"
    echo "Blocked actions  : Architect invocation, Rule 17 (reality check), multi-step planning"
    echo "Next required    : proceed with lightweight continuation"
    ;;
  exhausted)
    echo "🛑  ${PIPELINE_LINE}"
    echo ""
    echo "Allowed actions  : NONE — agent must stop"
    echo "Next required    : summarize state → surface blocker → ask user for input"
    ;;
  *)
    echo "❓  Unknown execution mode: ${EXECUTION_MODE}" >&2
    exit 1
    ;;
esac

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── Hard gate exit codes ──────────────────────────────────────────────────────
# 0 = healthy (OK to proceed)
# 2 = constrained (lightweight only; caller checks this)
# 1 = exhausted (must stop; non-zero so shell pipelines break naturally)

case "${EXECUTION_MODE}" in
  healthy)    exit 0 ;;
  constrained) exit 2 ;;
  exhausted)  exit 1 ;;
  *)          exit 1 ;;
esac
