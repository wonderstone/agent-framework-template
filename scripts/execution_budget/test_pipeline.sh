#!/usr/bin/env bash
# test_pipeline.sh
#
# Edge-case tests for the pipeline enforcement system.
#
# Tests:
#   1. Cooldown Active → always PIPELINE BLOCKED across multiple iterations
#   2. Constrained mode → Heavy reasoning blocked; progression allowed
#   3. Transition: healthy → constrained → exhausted
#
# Each test creates an isolated copy of session_state.md in /tmp, runs the
# scripts against it, and checks output + exit codes.
#
# Usage:
#   bash scripts/execution_budget/test_pipeline.sh
#
# Exit codes:
#   0 — all tests passed
#   1 — one or more tests failed

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE="${SCRIPT_DIR}/../../templates/session_state.template.md"
TMPDIR_BASE="/tmp/pipeline_tests_$$"
mkdir -p "${TMPDIR_BASE}"

PASS=0
FAIL=0

# ── Helpers ───────────────────────────────────────────────────────────────────

pass() { echo "  ✅  PASS: $1"; PASS=$((PASS + 1)); }
fail() { echo "  ❌  FAIL: $1"; FAIL=$((FAIL + 1)); }

# Create a fresh state file with optional field overrides.
# Usage: make_state <dest> [sed_expression ...]
make_state() {
  local dest="$1"
  shift
  cp "${TEMPLATE}" "${dest}"
  for expr in "$@"; do
    python3 -c "
import sys, re
with open('${dest}') as f: c = f.read()
c = re.sub(${expr})
with open('${dest}', 'w') as f: f.write(c)
"
  done
}

run_check() {
  local state_file="$1"
  # Returns exit code without causing set -e to abort
  STATE_FILE="${state_file}" bash "${SCRIPT_DIR}/check_budget.sh" "${state_file}" 2>&1 || true
}

run_enforce() {
  local flag="$1"
  local state_file="$2"
  # Capture output + exit code; do not abort on non-zero
  local out
  out="$(STATE_FILE="${state_file}" bash "${SCRIPT_DIR}/enforce_pipeline.sh" "${flag}" "${state_file}" 2>&1)" || true
  echo "${out}"
}

# ─────────────────────────────────────────────────────────────────────────────
# Test 1 — Cooldown Active → always PIPELINE BLOCKED across multiple iterations
# ─────────────────────────────────────────────────────────────────────────────

echo ""
echo "Test 1: Cooldown Active → PIPELINE BLOCKED across multiple iterations"

STATE1="${TMPDIR_BASE}/test1.md"
cp "${TEMPLATE}" "${STATE1}"

# Activate cooldown
python3 - "${STATE1}" <<'PY'
import sys, re
with open(sys.argv[1]) as f: c = f.read()
c = re.sub(r'\*\*Cooldown Active\*\*: no', '**Cooldown Active**: yes', c)
c = re.sub(r'\*\*Last Platform Event\*\*: none', '**Last Platform Event**: rate-limit received — test', c)
with open(sys.argv[1], 'w') as f: f.write(c)
PY

# Run three consecutive --loop iterations; each must be BLOCKED
ALL_BLOCKED=true
for iter in 1 2 3; do
  output="$(run_enforce --loop "${STATE1}")"
  if echo "${output}" | grep -q "PIPELINE BLOCKED"; then
    : # expected
  else
    ALL_BLOCKED=false
    echo "    Iteration ${iter} was NOT blocked. Output:"
    echo "${output}" | head -5
  fi
  # Verify exit code 1
  set +e
  STATE_FILE="${STATE1}" bash "${SCRIPT_DIR}/enforce_pipeline.sh" --loop "${STATE1}" >/dev/null 2>&1
  ec=$?
  set -e
  if [ "${ec}" -ne 1 ]; then
    ALL_BLOCKED=false
    echo "    Iteration ${iter}: expected exit 1, got ${ec}"
  fi
done

if ${ALL_BLOCKED}; then
  pass "Cooldown active → BLOCKED on all 3 iterations (exit 1 each time)"
else
  fail "Cooldown did not block all iterations"
fi

# ─────────────────────────────────────────────────────────────────────────────
# Test 2 — Constrained mode: heavy reasoning blocked, progression allowed
# ─────────────────────────────────────────────────────────────────────────────

echo ""
echo "Test 2: Constrained mode → heavy reasoning blocked, progression allowed"

STATE2="${TMPDIR_BASE}/test2.md"
cp "${TEMPLATE}" "${STATE2}"

# Exhaust heavy reasoning and reality checks (constrained, not exhausted)
python3 - "${STATE2}" <<'PY'
import sys, re
with open(sys.argv[1]) as f: c = f.read()
c = re.sub(r'\*\*Heavy Reasoning Calls\*\*: 0 / 2', '**Heavy Reasoning Calls**: 2 / 2', c)
c = re.sub(r'\*\*Reality Checks\*\*: 0 / 3', '**Reality Checks**: 3 / 3', c)
with open(sys.argv[1], 'w') as f: f.write(c)
PY

output="$(run_check "${STATE2}")"

# Must be constrained, not exhausted
if echo "${output}" | grep -q "PIPELINE DEGRADED: constrained"; then
  pass "PIPELINE DEGRADED: constrained reported"
else
  fail "Expected PIPELINE DEGRADED: constrained; got: $(echo "${output}" | grep PIPELINE)"
fi

# Autonomous progression must still be allowed
if echo "${output}" | grep -q "Autonomous progression allowed: YES"; then
  pass "Autonomous progression allowed in constrained mode"
else
  fail "Autonomous progression should be YES in constrained mode"
fi

# Heavy reasoning must be blocked
if echo "${output}" | grep -q "Heavy reasoning allowed: NO"; then
  pass "Heavy reasoning blocked in constrained mode"
else
  fail "Heavy reasoning should be NO in constrained mode"
fi

# Exit code must be 0 (not blocked, constrained is ok to continue)
set +e
STATE_FILE="${STATE2}" bash "${SCRIPT_DIR}/check_budget.sh" "${STATE2}" >/dev/null 2>&1
ec=$?
set -e
if [ "${ec}" -eq 0 ]; then
  pass "check_budget.sh exits 0 in constrained mode (progression allowed)"
else
  fail "check_budget.sh should exit 0 in constrained mode; got ${ec}"
fi

# enforce_pipeline exits 2 in constrained mode
set +e
STATE_FILE="${STATE2}" bash "${SCRIPT_DIR}/enforce_pipeline.sh" --loop "${STATE2}" >/dev/null 2>&1
ec=$?
set -e
if [ "${ec}" -eq 2 ]; then
  pass "enforce_pipeline.sh exits 2 in constrained mode"
else
  fail "enforce_pipeline.sh should exit 2 in constrained mode; got ${ec}"
fi

# ─────────────────────────────────────────────────────────────────────────────
# Test 3 — Transition: healthy → constrained → exhausted
# ─────────────────────────────────────────────────────────────────────────────

echo ""
echo "Test 3: Transition — healthy → constrained → exhausted"

STATE3="${TMPDIR_BASE}/test3.md"
cp "${TEMPLATE}" "${STATE3}"

# ── 3a: Baseline healthy ──
output="$(run_check "${STATE3}")"
if echo "${output}" | grep -q "PIPELINE OK"; then
  pass "3a: baseline is PIPELINE OK (healthy)"
else
  fail "3a: expected PIPELINE OK; got: $(echo "${output}" | grep PIPELINE)"
fi

# ── 3b: Exhaust heavy reasoning → constrained ──
python3 - "${STATE3}" <<'PY'
import sys, re
with open(sys.argv[1]) as f: c = f.read()
c = re.sub(r'\*\*Heavy Reasoning Calls\*\*: 0 / 2', '**Heavy Reasoning Calls**: 2 / 2', c)
with open(sys.argv[1], 'w') as f: f.write(c)
PY

output="$(run_check "${STATE3}")"
if echo "${output}" | grep -q "PIPELINE DEGRADED: constrained"; then
  pass "3b: after heavy exhausted → PIPELINE DEGRADED: constrained"
else
  fail "3b: expected PIPELINE DEGRADED; got: $(echo "${output}" | grep PIPELINE)"
fi

# ── 3c: Exhaust loop count → exhausted ──
python3 - "${STATE3}" <<'PY'
import sys, re
with open(sys.argv[1]) as f: c = f.read()
c = re.sub(r'\*\*Loop Count\*\*: 0 / 5', '**Loop Count**: 5 / 5', c)
with open(sys.argv[1], 'w') as f: f.write(c)
PY

output="$(run_check "${STATE3}")"
if echo "${output}" | grep -q "PIPELINE BLOCKED: exhausted"; then
  pass "3c: after loop exhausted → PIPELINE BLOCKED: exhausted"
else
  fail "3c: expected PIPELINE BLOCKED: exhausted; got: $(echo "${output}" | grep PIPELINE)"
fi

# Exit code must be 1
set +e
STATE_FILE="${STATE3}" bash "${SCRIPT_DIR}/check_budget.sh" "${STATE3}" >/dev/null 2>&1
ec=$?
set -e
if [ "${ec}" -eq 1 ]; then
  pass "3c: check_budget exits 1 when exhausted"
else
  fail "3c: expected exit 1; got ${ec}"
fi

# ── 3d: Resetting loop counter → back to constrained ──
python3 - "${STATE3}" <<'PY'
import sys, re
with open(sys.argv[1]) as f: c = f.read()
c = re.sub(r'\*\*Loop Count\*\*: 5 / 5', '**Loop Count**: 2 / 5', c)
with open(sys.argv[1], 'w') as f: f.write(c)
PY

output="$(run_check "${STATE3}")"
if echo "${output}" | grep -q "PIPELINE DEGRADED: constrained"; then
  pass "3d: after loop reset → back to PIPELINE DEGRADED: constrained"
else
  fail "3d: expected PIPELINE DEGRADED after reset; got: $(echo "${output}" | grep PIPELINE)"
fi

# ─────────────────────────────────────────────────────────────────────────────
# Results
# ─────────────────────────────────────────────────────────────────────────────

echo ""
echo "━━━ Test Results ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Passed : ${PASS}"
echo "  Failed : ${FAIL}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Cleanup
rm -rf "${TMPDIR_BASE}"

if [ "${FAIL}" -gt 0 ]; then
  exit 1
fi
exit 0
