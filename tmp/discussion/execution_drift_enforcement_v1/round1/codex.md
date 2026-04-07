Verdict: `freeze-plan`

Top 3 findings

1. Category: prevention gap  
Why it matters: the template does not currently define a mechanical execution unit, checkpoint event, or required truth-surface update after that event, so drift is inevitable once work runs longer than one short batch.  
Smallest honest next step: add `progress_unit`, `checkpoint_rule`, `truth_surfaces`, and `closeout_boundary` fields to the execution contract and git-audit task packet templates.

2. Category: detection gap  
Why it matters: current enforcement is mostly closeout-time and heuristic; it catches false completion claims better than stale in-progress state, so mid-task drift can accumulate for hours or days before anyone notices.  
Smallest honest next step: ship a `state_sync_audit.py` script that compares declared scope, changed files, latest progress receipts, `session_state.md`, and `ROADMAP.md` for explicit contradictions and missing checkpoint reflection.

3. Category: recovery gap  
Why it matters: imperfect agents will still drift; if the only response is “fail validation,” teams either bypass the rule or get stuck with contradictory truth surfaces and no standard repair path.  
Smallest honest next step: add a drift packet plus a reconciliation command/runbook that must run before closeout when sync audit finds contradictions.

Proposed anti-drift mechanism table

| mechanism | template surface(s) | enforcement level | why this level is honest |
|---|---|---|---|
| Prevention: checkpointed execution contract with `progress_unit`, `checkpoint_rule`, `truth_surfaces`, `closeout_boundary` | `templates/execution_contract.template.md`, `templates/git_audit_task_packet.template.md`, `docs/DOC_FIRST_EXECUTION_GUIDELINES.md` | `hard-fail` | Validator can require the contract fields to exist and be well-formed; it cannot honestly guarantee behavior without them. |
| Prevention: structured progress receipt for each declared checkpoint | `templates/execution_progress_receipt.template.md`, `scripts/execution_progress_pipeline.py`, demo/example repos | `workflow-only` | The template can provide the path and examples, but cannot force every runtime to emit receipts unless the adopter routes work through the pipeline. |
| Prevention: helper that updates `session_state.md` from receipt fields | `scripts/reconcile_state_from_receipt.py`, `templates/session_state.template.md` | `advisory` | Tooling can reduce prose drift, but semantic state still needs human/agent judgment, especially for roadmap impact. |
| Detection: state-sync auditor comparing scope, changed files, receipts, and state surfaces | `scripts/state_sync_audit.py`, `.githooks/pre-commit`, `.githooks/pre-push`, CI wiring, tests | `hard-fail` | It can mechanically detect explicit contradictions, missing checkpoint receipts, and stale declared-next-step fields when a checkpointed task is in play. |
| Detection: root self-hosting stale-state audit for this repo and bootstrapped adopters that opt in | `scripts/validate_template.py`, adopter validator bootstrap | `hard-fail` | This is limited to declared truth surfaces and explicit freshness rules, not vague “state feels old” judgments. |
| Repair: drift packet opened on sync failure | `templates/drift_packet.template.md`, `docs/runbooks/state-reconciliation.md` | `repair-loop` | When drift exists, forcing closeout is dishonest; the right response is standardized reconciliation, not blind prohibition. |
| Repair: reconcile command that either updates truth surfaces or records explicit deferral/leftover unit | `scripts/execution_progress_pipeline.py reconcile`, `docs/LEFTOVER_UNIT_CONTRACT.md`, handoff packet template/runbook | `repair-loop` | Some drift can only be resolved by documenting residual mismatch and handing off safely. |
| Scope reduction: require bounded file/surface scope for long-running tasks | execution contract, task packet, examples | `hard-fail` | Narrower declared scope is validator-checkable and directly reduces opportunities for state divergence. |
| `ROADMAP.md` sync nudges for milestone-affecting work only | sync auditor rules, runbook guidance | `advisory` | Hard-failing every implementation diff on roadmap edits would create noise; roadmap updates are only mechanically justified for milestone or phase movement. |

Ordered rollout plan

1. Freeze the event model: define the checkpoint contract fields and truth-surface ownership in templates, docs, and examples.
2. Ship the structured receipt path: add progress-receipt and reconciliation scripts plus receipt and drift-packet templates.
3. Add detection: implement `state_sync_audit.py` and wire it into hooks and CI for tasks that declare checkpointed execution.
4. Add repair workflow: publish the state-reconciliation runbook and require drift reconciliation before closeout or next-stage execution.
5. Self-host and prove it: adopt the mechanism in this repo and the demo project, then add tests for happy path, stale-state failure, and repair-loop recovery.

One thing the template must explicitly avoid

Do not pretend the template can continuously orchestrate agent behavior at runtime or infer “fresh enough” state purely from code diffs; only hard-fail explicit, declared contracts and explicit contradictions.

Final recommendation in one sentence

Adopt Direction E asymmetrically: hard-fail on declared checkpoint contracts and explicit sync contradictions, keep state-mutation helpers advisory, and make drift resolution a first-class repair loop rather than a closeout-only scolding step.
