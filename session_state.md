# session_state.md

> Cross-session state for agent-framework-template. Keep under ~100 lines.
> When over limit: archive old phase content to docs/archive/.

---

## Current Goal
No active implementation. The anti-drift mechanism wave is shipped, and the repository now runs on checkpoint contracts, sync auditing, drift reconciliation, and the rebased execution-rule layer.

---

## Working Hypothesis
Execution drift stays manageable only when checkpoint contracts, progress receipts, sync auditing, and drift reconciliation are all present together; otherwise the rules regress back into prose-only reminders.

**Confidence**: High

**Evidence**:
- Templates and scripts now carry task ID, checkpoint rule, truth surfaces, state-sync fields, progress receipts, and drift reconciliation support.
- Hooks, bootstrap assets, runbooks, and `.github/copilot-instructions.md` now point at and consume those anti-drift surfaces end-to-end.

**Contradictions**: None.

---

## Plan
**Approach**: Keep the anti-drift mechanism stack as the default execution-control surface for future work and only widen contradiction classes when real adopter evidence shows the current set is too weak.

**Steps**:
1. Keep the shipped checkpoint contract and state-sync artifacts stable.
2. Widen hard-fail coverage only when adopter evidence shows the current contradiction set is insufficient.

**Why this approach**: The repository now has a truthful minimum anti-drift stack; the next risk is overfitting the audit before adopter evidence exists.

---

## Active Work
**Active Task ID**: none

**Current Step**: No active work.

**Next Planned Step**: None until the next framework workstream is opened.

**Progress Unit / Checkpoint Rule / Truth Surfaces / State Sync Schedule**: n/a

**True Closeout Boundary / Host Closeout Action**: n/a / `task_complete`

---

## Recent Receipts
- Completed round-seven cleanup of `.github/copilot-instructions.md`: reduced early checkpoint reminders in Rules 4 and 5 to pure Rule 18 pointers, and rolled older receipt history into `docs/archive/Copilot_Instructions_Refactor_Closeout_2026-04-08.md` so `session_state.md` returns to a scan-friendly receipt window.
- Completed round-six refactor of `.github/copilot-instructions.md`: added an execution-state reading map near Rule 18 and clarified Rule 24 as the owner of scope-state classification and leftovers, without changing runtime policy.
- Completed round-five refactor of `.github/copilot-instructions.md`: added an output-and-closeout reading map plus scope-clarifying lines for Rules 14, 22, and 25 so the response and closeout chain is easier to scan without semantic changes.

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

End-to-end scenario: a maintainer opens a long-running task, records a checkpoint in a progress receipt, the repository audits truth-surface sync, and any contradiction is routed through a drift packet before closeout continues.

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
