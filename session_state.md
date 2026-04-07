# session_state.md

> Cross-session state for agent-framework-template. Keep under ~100 lines.
> When over limit: archive old phase content to docs/archive/.

---

## Current Goal

No active implementation. The anti-drift mechanism wave is now shipped, and the repository truth surfaces, hooks, validator, bootstrap assets, and execution-lifecycle rules have been rebased onto those mechanism surfaces.

---

## Working Hypothesis

Execution drift stays manageable only when checkpoint contracts, progress receipts, sync auditing, and drift reconciliation are all present together; otherwise the rules regress back into prose-only reminders.

**Confidence**: High

**Evidence**:
- `templates/execution_contract.template.md`, `templates/git_audit_task_packet.template.md`, and `templates/session_state.template.md` now carry task ID, checkpoint rule, truth surfaces, and state-sync fields.
- `scripts/state_sync_pipeline.py` now creates progress receipts and drift reconciliation packets from the shipped templates.
- `scripts/state_sync_audit.py` now detects unresolved drift, missing progress receipts for active tasks, blocked progress without recovery artifacts, and unsynced checkpoint diffs.
- `.githooks/pre-commit`, `.githooks/pre-push`, `scripts/bootstrap_adoption.py`, `docs/runbooks/state-reconciliation.md`, and `.github/copilot-instructions.md` now point at and consume those new anti-drift surfaces.

**Contradictions**: None.

---

## Plan

**Approach**: Keep the anti-drift mechanism stack as the default execution-control surface for future work and only widen contradiction classes when real adopter evidence shows the current set is too weak.

**Steps**:
1. Keep the shipped checkpoint contract and state-sync artifacts stable.
2. Collect adopter feedback on noise level and missing contradiction classes.
3. Expand hard-fail coverage only when the evidence stays honest.

**Why this approach**: The repository now has a truthful minimum anti-drift stack; the next risk is overfitting the audit before adopter evidence exists.

---

## Active Work

**Active Task ID**: none

**Current Step**: No active work.

**Next Planned Step**: None until the next framework workstream is opened.

**Progress Unit**: n/a

**Checkpoint Rule**: n/a

**Truth Surfaces**: n/a

**State Sync Schedule**: n/a

**True Closeout Boundary**: n/a

**Host Closeout Action**: `task_complete`

---

## Recent Receipts

- Shipped the anti-drift checkpoint contract into `templates/execution_contract.template.md`, `templates/git_audit_task_packet.template.md`, `templates/session_state.template.md`, and the demo execution artifacts.
- Added `templates/execution_progress_receipt.template.md`, `templates/drift_reconciliation_packet.template.md`, `scripts/state_sync_pipeline.py`, and `scripts/state_sync_audit.py` as the new prevention, detection, and repair surfaces.
- Wired the state sync audit into `.githooks/pre-commit`, `.githooks/pre-push`, `scripts/bootstrap_adoption.py`, `docs/runbooks/state-reconciliation.md`, `README.md`, and `.github/instructions/project-context.instructions.md`.

---

## Completed This Phase

- Completed the anti-drift implementation wave across checkpoint contracts, progress receipts, sync auditing, drift reconciliation, bootstrap assets, hook wiring, and rule-layer rebase.

---

## Blocker / Decision Needed

- (none)

---

## Leftover Units

- (none)

---

## Mid-Session Corrections

- Corrected the initial anti-drift kickoff assumption that template-only edits would be enough; bootstrap assets, hooks, validator checks, and rule references also needed to move together to avoid a second drift layer.

---

## User Acceptance Criteria

- [x] When a maintainer declares a long-running task, the execution contract and task packet expose task ID, checkpoint rule, truth surfaces, and state-sync schedule.
- [x] When work crosses a checkpoint, the repository ships a receipt-bearing path for recording the expected truth-surface effect.
- [x] When drift remains unresolved, the repository can detect it mechanically and block closeout or next-stage dispatch.
- [x] When a maintainer bootstraps the standard profile, the new anti-drift docs, templates, scripts, and demo artifacts are present in the copied assets.

End-to-end scenario: a maintainer opens a long-running task, records a checkpoint in a progress receipt, the repository can audit whether `session_state.md` and related artifacts stayed in sync, and any contradiction is routed through a drift packet before closeout continues.

Agent cannot verify: which future contradiction classes should default to hard-fail for every adopter instead of advisory-first, because that still depends on real repository granularity and local noise tolerance.

---

## Phase Decisions

- Treat anti-drift as a mechanism stack, not a prose-only rule tightening exercise.
- Keep the first audit wave contradiction-focused and mechanical rather than trying to infer narrative intent automatically.
- Make execution-lifecycle rules depend on checkpoint contracts, progress receipts, sync audit, and drift reconciliation instead of trying to simulate those behaviors in prose.

---

## Technical Insights

- Self-hosting drift in the root repository damages framework trust faster than missing optional capabilities.
- Checkpoint contracts only become trustworthy when the task packet, session state, receipts, hooks, and rule layer all consume the same fields.
- Drift repair should stay distinct from leftover recording: contradictions are reconciled first, then intentional partial work can be preserved honestly.
