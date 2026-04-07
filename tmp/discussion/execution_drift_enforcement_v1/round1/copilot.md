● Read INDEX.md
  │ docs/INDEX.md
  └ 52 lines read

● Read LEFTOVER_UNIT_CONTRACT.md
  │ docs/LEFTOVER_UNIT_CONTRACT.md
  └ 183 lines read

● Read session_state.md
  └ 144 lines read

● Read DOC_FIRST_EXECUTION_GUIDELINES.md
  │ docs/DOC_FIRST_EXECUTION_GUIDELINES.md
  └ 132 lines read

● Read execution_contract.template.md
  │ templates/execution_contract.template.md
  └ 163 lines read

● Read resumable-git-audit-pipeline.md
  │ docs/runbooks/resumable-git-audit-pipeline.md
  └ 82 lines read

● Read ROADMAP.md
  └ 92 lines read

I’ve got the current governance surfaces and state model. Next I’m checking what executable tooling already exists around receipts, closeout, and validation so the plan stays implementation-real rather than policy-only.

● Read git_audit_pipeline.py
  │ scripts/git_audit_pipeline.py
  └ L1:260 (250 lines read)

● Read validate_template.py
  │ scripts/validate_template.py
  └ L1:260 (260 lines read)

● Search (glob)
  │ "**/*state*" in scripts
  └ No matches found

● Search (glob)
  │ "**/*closeout*" in scripts
  └ 1 file found

● Search (grep)
  │ "session_state|ROADMAP|receipt|handoff|closeout|drift|state sync|state_sync|reconcile" (scripts)
  └ 7 lines found

I found the key constraint: the repo already has receipt tooling and closeout auditing, but nothing that mechanically ties *in-flight execution events* to `session_state.md` freshness. I’m reading those existing auditors now so the proposal can extend the current model instead of inventing a parallel one.

● Read closeout_truth_audit.py
  │ scripts/closeout_truth_audit.py
  └ L1:260 (132 lines read)

● Read preference_drift_audit.py
  │ scripts/preference_drift_audit.py
  └ L1:260 (107 lines read)

● Read active_docs_audit.py
  │ scripts/active_docs_audit.py
  └ L1:260 (156 lines read)

● Search (grep)
  │ "closeout_truth_audit|preference_drift_audit|active_docs_audit|session_state.md|ROADMAP.md"
  │ (tests)
  └ 23 lines found

● Read test_validate_template.py
  │ tests/test_validate_template.py
  └ L110:180 (71 lines read)

● Search (grep)
  │ "Current Step|Next Planned Step|User Acceptance Criteria|session_state"
  │ (scripts/validate_template.py)
  └ 16 lines found

● Search (grep)
  │ "closeout_truth_audit|preference_drift_audit|active_docs_audit" (.githooks)
  └ 2 lines found

● Read pre-commit
  │ .githooks/pre-commit
  └ L1:120 (12 lines read)

● Read validate_template.py
  │ scripts/validate_template.py
  └ L896:952 (57 lines read)

● Read session_state.template.md
  │ templates/session_state.template.md
  └ L1:220 (107 lines read)

Verdict: freeze-plan

Top 3 findings

1. Category: prevention
Why it matters: drift starts because execution events do not have a required, low-friction path into state surfaces. `session_state.md` and `ROADMAP.md` are currently prose-first truth surfaces, while the executable tooling is receipt-first only at audit/closeout boundaries.
Smallest honest next step: add one structured progress-receipt schema with `task_id`, `receipt_seq`, `progress_unit`, `touched_files`, `status`, and `expected_state_effect`, then add one helper that applies that event into `session_state.md` without claiming to fully author the narrative.

2. Category: detection
Why it matters: current checks are too narrow. The repo already catches some stale idle-state contradictions and receipt-free closeout claims, but it does not detect the common case of “execution moved forward, state surfaces did not.”
Smallest honest next step: add a `state_sync_audit.py` that compares the latest receipt sequence, handoff/leftover artifacts, touched files, and state fields in `session_state.md`/`ROADMAP.md`, and reports contradiction classes instead of trying to infer the one true fix.

3. Category: repair
Why it matters: perfect prevention is unrealistic; long tasks will still drift under imperfect agents. If the only response is a late hard fail, maintainers get blocked without a recovery path and will bypass the system.
Smallest honest next step: add a drift packet plus reconcile command that records the mismatch, proposes the required state edits, and blocks closeout or next-stage dispatch until the packet is resolved.

Proposed anti-drift mechanism table

| mechanism | template surface(s) | enforcement level | why this level is honest |
|---|---|---|---|
| Execution-unit progress receipt for every declared progress unit | extend `scripts/git_audit_pipeline.py` or add `scripts/state_sync_pipeline.py`; new receipt template; `templates/execution_contract.template.md`; `templates/session_state.template.md`; adoption guide/example repo | workflow-only | the template can ship the receipt path and make it the default, but it cannot guarantee every agent emits a receipt unless another gate checks for it |
| Structured state-mutation helper (`record-progress`, `record-blocker`, `record-complete`, `record-leftover`) | new script/tool; `templates/session_state.template.md`; `templates/roadmap.template.md`; example repo | advisory | scripts can reduce drift by making updates easier and more consistent, but they should not pretend they can fully rewrite truthful human-readable state from code alone |
| State sync auditor that compares receipts, handoffs, leftovers, `session_state.md`, `ROADMAP.md`, and changed files | new `scripts/state_sync_audit.py`; wire into `scripts/validate_template.py`; tests; optional pre-push hook | repair-loop | the auditor can reliably detect stale or contradictory surfaces, but in many cases it cannot know which truth surface is authoritative without a reconciliation step |
| Drift packet + reconcile workflow | `tmp/state_drift/<task>/drift_packet.md`; reconcile subcommand; new runbook; execution-contract references | repair-loop | this matches the real problem: drift is often recoverable, and the right response is “stop and reconcile” rather than “guess and overwrite” |
| Closeout and next-stage gate on unresolved drift | pre-push hook, validator integration, dispatch pipeline checks, execution contract | hard-fail | the template cannot orchestrate every mid-task moment, but it can honestly block boundary crossings it can observe: dispatch, handoff, closeout, push |
| Terminal-state coupling for `STUCK`/`ESCALATE`/live-blocked work | extend `docs/LEFTOVER_UNIT_CONTRACT.md`; `docs/runbooks/resumable-git-audit-pipeline.md`; helper commands and tests | hard-fail | terminal task states are explicit and artifact-based already, so requiring a matching leftover or handoff record is mechanically enforceable |
| ROADMAP claim guard requiring receipt linkage for status promotion | extend `scripts/closeout_truth_audit.py` or add focused roadmap-claim audit; tests | hard-fail | completed-phase or completed-item claims are diff-visible and should not be allowed without evidence plus a matching state update |

Ordered rollout plan

1. Add a minimal event model first: progress receipt schema, `receipt_seq`, and a small `State Sync` block in `session_state.md` such as `task_id`, `last_applied_receipt`, and `drift_status`.
2. Ship a state-mutation helper that updates `session_state.md` and optional `ROADMAP.md` fields from those events, plus an example adopted repo flow that uses it during a long task.
3. Add `state_sync_audit.py` and teach it only contradiction classes that are mechanically trustworthy: stale receipt sequence, unresolved blocker without leftover/handoff, roadmap completion claim without matching receipt/state update, and “no active work” contradictions.
4. Add the repair path: drift packet template, reconcile command, and runbook rules that say drift enters repair before closeout or next-stage dispatch.
5. Promote only the observable boundary checks to hard-fail in hooks/pipeline; keep in-loop freshness nudges advisory so the template does not overclaim runtime orchestration power.

One thing the template must explicitly avoid

Do not auto-infer or auto-overwrite the “correct” `session_state.md` or `ROADMAP.md` narrative directly from git diff or changed files; detection can be mechanical, but truth reconciliation still needs an explicit repair step.

Final recommendation in one sentence

Adopt Direction E asymmetrically: use structured progress receipts and a state-update helper for prevention, a contradiction-focused state-sync auditor for detection, and a mandatory drift-reconcile packet at dispatch/closeout boundaries for repair.

