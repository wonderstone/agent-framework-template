#!/usr/bin/env bash
# validate-template.sh
#
# Checks that the agent framework template is internally consistent:
#   - All required framework files are present
#   - The docs/archive/ directory exists
#   - No broken file references in key documents
#
# Run from the repository root:
#   bash scripts/validate-template.sh

set -euo pipefail

ERRORS=0
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

check_file() {
  if [ ! -f "${ROOT}/$1" ]; then
    echo "  MISSING FILE: $1"
    ERRORS=$((ERRORS + 1))
  fi
}

check_dir() {
  if [ ! -d "${ROOT}/$1" ]; then
    echo "  MISSING DIR:  $1"
    ERRORS=$((ERRORS + 1))
  fi
}

echo "=== Agent Framework Template — Integrity Check ==="
echo ""

# ── Required framework files ──────────────────────────────────────────────────
echo "[ Required framework files ]"
check_file ".github/copilot-instructions.md"
check_file ".github/project-context.instructions.md"
check_file ".github/agents/architect.agent.md"
check_file ".github/agents/implementer.agent.md"
check_file ".github/instructions/backend.instructions.md"
check_file ".github/instructions/docs.instructions.md"
check_file "docs/INDEX.md"
check_file "docs/FRAMEWORK_ARCHITECTURE.md"
check_file "docs/ADOPTION_GUIDE.md"
check_file "docs/STRATEGY_MECHANISM_LAYERING.md"
check_file "docs/ROLE_STRATEGY_EXAMPLES.md"
check_file "docs/runbooks/resumable-git-audit-pipeline.md"
check_file "templates/session_state.template.md"
check_file "templates/project-context.template.md"
check_file "templates/roadmap.template.md"
check_file "templates/git_audit_task_packet.template.md"
check_file "templates/git_audit_receipt.template.md"
check_file "templates/git_audit_handoff_packet.template.md"
check_file "templates/reviewer_role_profile.template.md"
check_file "scripts/git_audit_pipeline.py"
check_file "examples/reviewer_roles/01_goal_acceptance_owner.md"
check_file "examples/reviewer_roles/02_plan_checkpoint_owner.md"
check_file "examples/reviewer_roles/03_runtime_correctness_reviewer.md"
check_file "examples/reviewer_roles/04_boundary_contract_reviewer.md"
check_file "examples/reviewer_roles/05_git_closeout_reviewer.md"
check_file "examples/reviewer_roles/06_maintainability_reviewer.md"
check_file "examples/reviewer_roles/07_observability_failure_path_reviewer.md"
check_file "examples/reviewer_roles/08_performance_benchmark_reviewer.md"
check_file "examples/reviewer_roles/09_migration_compatibility_reviewer.md"
check_file "examples/reviewer_roles/10_docs_spec_drift_reviewer.md"

# ── Required directories ──────────────────────────────────────────────────────
echo ""
echo "[ Required directories ]"
check_dir "docs/archive"

# ── Cross-references: files that docs/INDEX.md's Framework section points to ──
echo ""
echo "[ Cross-references: Framework docs listed in docs/INDEX.md ]"
FRAMEWORK_REFS=(
  "docs/FRAMEWORK_ARCHITECTURE.md"
  "docs/ADOPTION_GUIDE.md"
  "docs/STRATEGY_MECHANISM_LAYERING.md"
  "docs/ROLE_STRATEGY_EXAMPLES.md"
  "docs/runbooks/resumable-git-audit-pipeline.md"
)
for ref in "${FRAMEWORK_REFS[@]}"; do
  if [ ! -f "${ROOT}/${ref}" ]; then
    echo "  BROKEN REF in INDEX.md: ${ref}"
    ERRORS=$((ERRORS + 1))
  fi
done

# ── Consistency: State Model in FRAMEWORK_ARCHITECTURE.md ─────────────────────
echo ""
echo "[ Consistency checks ]"
if ! grep -q "Working Hypothesis" "${ROOT}/docs/FRAMEWORK_ARCHITECTURE.md"; then
  echo "  MISSING: 'Working Hypothesis' not found in FRAMEWORK_ARCHITECTURE.md State Model"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q "Rule 11" "${ROOT}/.github/copilot-instructions.md"; then
  echo "  MISSING: 'Rule 11' not found in copilot-instructions.md"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q "Rule 12" "${ROOT}/.github/copilot-instructions.md"; then
  echo "  MISSING: 'Rule 12' (Pre-Action Self-Check Gate) not found in copilot-instructions.md"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q "Rule 13" "${ROOT}/.github/copilot-instructions.md"; then
  echo "  MISSING: 'Rule 13' (Failure Recovery) not found in copilot-instructions.md"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q "Self-Check Stage" "${ROOT}/docs/FRAMEWORK_ARCHITECTURE.md"; then
  echo "  MISSING: 'Self-Check Stage' section not found in FRAMEWORK_ARCHITECTURE.md"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q "Failure Modes" "${ROOT}/docs/FRAMEWORK_ARCHITECTURE.md"; then
  echo "  MISSING: 'Failure Modes' section not found in FRAMEWORK_ARCHITECTURE.md"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q "Mid-Session Corrections" "${ROOT}/templates/session_state.template.md"; then
  echo "  MISSING: 'Mid-Session Corrections' section not found in session_state.template.md"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q "Rule 14" "${ROOT}/.github/copilot-instructions.md"; then
  echo "  MISSING: 'Rule 14' (Task Progression Loop) not found in copilot-instructions.md"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q "Rule 15" "${ROOT}/.github/copilot-instructions.md"; then
  echo "  MISSING: 'Rule 15' (Decomposition and Dispatch Decision) not found in copilot-instructions.md"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q "Progression Model" "${ROOT}/docs/FRAMEWORK_ARCHITECTURE.md"; then
  echo "  MISSING: 'Progression Model' section not found in FRAMEWORK_ARCHITECTURE.md"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q "Next Planned Step" "${ROOT}/templates/session_state.template.md"; then
  echo "  MISSING: 'Next Planned Step' field not found in session_state.template.md"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q "Next Actions" "${ROOT}/.github/agents/implementer.agent.md"; then
  echo "  MISSING: 'Next Actions' output contract not found in implementer.agent.md"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q "Next Actions" "${ROOT}/.github/agents/architect.agent.md"; then
  echo "  MISSING: 'Next Actions' output contract not found in architect.agent.md"
  ERRORS=$((ERRORS + 1))
fi

# ── Planning layer (Rule 16) ──────────────────────────────────────────────────
if ! grep -q "Rule 16" "${ROOT}/.github/copilot-instructions.md"; then
  echo "  MISSING: 'Rule 16' (Planning and Path Selection) not found in copilot-instructions.md"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q "Planning Layer" "${ROOT}/docs/FRAMEWORK_ARCHITECTURE.md"; then
  echo "  MISSING: 'Planning Layer' section not found in FRAMEWORK_ARCHITECTURE.md"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q "## Plan" "${ROOT}/templates/session_state.template.md"; then
  echo "  MISSING: '## Plan' section not found in session_state.template.md"
  ERRORS=$((ERRORS + 1))
fi

# ── Reality check layer (Rule 17) ─────────────────────────────────────────────
if ! grep -q "Rule 17" "${ROOT}/.github/copilot-instructions.md"; then
  echo "  MISSING: 'Rule 17' (Reality Check and Goal Alignment) not found in copilot-instructions.md"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q "Reality Check Layer" "${ROOT}/docs/FRAMEWORK_ARCHITECTURE.md"; then
  echo "  MISSING: 'Reality Check Layer' section not found in FRAMEWORK_ARCHITECTURE.md"
  ERRORS=$((ERRORS + 1))
fi

# ── Resumable audit workflow (Rule 18) ───────────────────────────────────────
if ! grep -q "Rule 18" "${ROOT}/.github/copilot-instructions.md"; then
  echo "  MISSING: 'Rule 18' (Resumable Audit Assets) not found in copilot-instructions.md"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q "Resumable Audit Artifacts" "${ROOT}/docs/FRAMEWORK_ARCHITECTURE.md"; then
  echo "  MISSING: 'Resumable Audit Artifacts' section not found in FRAMEWORK_ARCHITECTURE.md"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q "Strategy vs Mechanism Layering" "${ROOT}/docs/FRAMEWORK_ARCHITECTURE.md"; then
  echo "  MISSING: 'Strategy vs Mechanism Layering' section not found in FRAMEWORK_ARCHITECTURE.md"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q "STRATEGY_MECHANISM_LAYERING.md" "${ROOT}/README.md"; then
  echo "  MISSING: strategy/mechanism layering doc not surfaced in README.md"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q "ROLE_STRATEGY_EXAMPLES.md" "${ROOT}/README.md"; then
  echo "  MISSING: role strategy examples doc not surfaced in README.md"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q "examples/reviewer_roles" "${ROOT}/README.md"; then
  echo "  MISSING: starter role profiles not surfaced in README.md"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q "strategy\\|mechanism\\|review role\\|reviewer split\\|codex\\|claude" "${ROOT}/.github/project-context.instructions.md"; then
  echo "  MISSING: strategy/mechanism trigger row not found in project-context.instructions.md"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q "ROLE_STRATEGY_EXAMPLES.md" "${ROOT}/docs/ADOPTION_GUIDE.md"; then
  echo "  MISSING: role strategy examples doc not referenced in ADOPTION_GUIDE.md"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q "examples/reviewer_roles" "${ROOT}/docs/ADOPTION_GUIDE.md"; then
  echo "  MISSING: starter role profiles not referenced in ADOPTION_GUIDE.md"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q "resumable-git-audit-pipeline" "${ROOT}/docs/ADOPTION_GUIDE.md"; then
  echo "  MISSING: resumable git audit workflow not referenced in ADOPTION_GUIDE.md"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q "audit\\|handoff\\|receipt\\|packet" "${ROOT}/.github/project-context.instructions.md"; then
  echo "  MISSING: audit/handoff trigger row not found in project-context.instructions.md"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q "\*\*Alignment\*\*:" "${ROOT}/.github/agents/architect.agent.md"; then
  echo "  MISSING: 'Alignment' field not found in architect.agent.md Next Actions contract"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -q "\*\*Alignment\*\*:" "${ROOT}/.github/agents/implementer.agent.md"; then
  echo "  MISSING: 'Alignment' field not found in implementer.agent.md Next Actions contract"
  ERRORS=$((ERRORS + 1))
fi

# ── Result ────────────────────────────────────────────────────────────────────
echo ""
if [ "${ERRORS}" -eq 0 ]; then
  echo "✅  All checks passed."
else
  echo "❌  ${ERRORS} issue(s) found — fix the items above and re-run."
  exit 1
fi
