# session_state.md

> Cross-session state for agent-framework-template. Keep under ~100 lines.
> When over limit: archive old phase content to docs/archive/.

---

## Current Goal
Wave 2 of the execution-proof stack is shipped and validated; no follow-on workstream is currently open.

---

## Working Hypothesis
Execution-proof credibility improves only when strict adoption, runtime toolchain truth, independent evaluation, and local executor review all have durable artifacts rather than policy-only expectations.

**Confidence**: High

**Evidence**:
- Wave 1 already proved strict-adoption attestation and toolchain probe receipts can ship cleanly through bootstrap, manifest, validator, and tests.
- The next missing surfaces named repeatedly in the 4-CLI discussion were the runner, evaluator pipeline, and local executor review loop.

**Contradictions**: None.

---

## Plan
**Approach**: Ship the next three highest-value execution surfaces as one bounded Wave 2: Developer Toolchain runner, independent-evaluation pipeline, and local executor review loop, then wire them through bootstrap, manifest, validation, and tests.

**Steps**:
1. Land a Wave 2 design doc and new templates for runner, evaluation, and executor review.
2. Implement the three Wave 2 scripts with bounded receipt or packet outputs.
3. Extend bootstrap and manifest contracts to ship the new assets for standard and full adopters.
4. Extend validator coverage and add regression tests.
5. Run repository validation, full tests, then git closeout.

**Why this approach**: These are the highest-consensus post-Wave-1 gaps and they materially reduce downstream claims that the template lacks enough execution-layer support.

---

## Active Work
**Active Task ID**: (none)

**Current Step**: No active work.

**Next Planned Step**: None until the next framework workstream is opened.

**Progress Unit / Checkpoint Rule / Truth Surfaces / State Sync Schedule**: n/a / n/a / `session_state.md`, `docs/EXECUTION_PROOF_WAVE_2_PLAN.md`, validator and tests / update when the next bounded workstream starts

**True Closeout Boundary / Host Closeout Action**: n/a / `task_complete`

---

## Recent Receipts
- Completed the final independent evaluation closeout for Wave 2 in `tmp/evaluation/execution_proof_wave_2/`: `evaluation_request.md` and `evaluation_report.md` now form a bounded PASS verdict pair backed by validator clean, `111 passed`, and standard dry-run smoke clean.
- Completed Wave 2 of the execution-proof stack: shipped the Developer Toolchain runner, independent-evaluation pipeline, and local executor review loop through docs, templates, bootstrap, manifest schema 4, validator rules, strict-adoption mechanism definitions, targeted regressions, full tests, and bootstrap smoke validation (`111 passed`, validator clean, standard dry-run smoke clean).
- Completed a 4-CLI discussion on downstream execution-layer support in `tmp/discussion/strict_execution_support_for_adopters_v1/discussion_packet.md`: all substantive reviewers converged on an execution-proof first wave centered on strict adoption attestation, Developer Toolchain probe receipts, a machine-facing toolchain runner, independent evaluation, and a local executor review loop.
- Completed a narrow second-round acceptance pass for `.github/copilot-instructions.md`: fixed `Core Truth Surfaces` ownership, restored Rule 10 badge symmetry, repaired the resulting Rule 10 navigation anchor, and closed the topic as fully accepted.
- Completed a 4-CLI acceptance review for the `.github/copilot-instructions.md` refactor in `tmp/discussion/copilot_instructions_refactor_acceptance_v1/discussion_packet.md`: verdict was passed in substance, with 3 `conditional-accept`, 1 `accept`, and only optional micro-polish remaining.
- Completed round-seven cleanup of `.github/copilot-instructions.md`: reduced early checkpoint reminders in Rules 4 and 5 to pure Rule 18 pointers, and rolled older receipt history into `docs/archive/Copilot_Instructions_Refactor_Closeout_2026-04-08.md` so `session_state.md` returns to a scan-friendly receipt window.
- Completed round-six refactor of `.github/copilot-instructions.md`: added an execution-state reading map near Rule 18 and clarified Rule 24 as the owner of scope-state classification and leftovers, without changing runtime policy.

---

## Completed This Phase
- Completed the anti-drift implementation wave across checkpoint contracts, progress receipts, sync auditing, drift reconciliation, bootstrap assets, hook wiring, and rule-layer rebase.
- Completed the Wave 2 execution-proof rollout across runner, evaluation, local executor review, bootstrap, manifest schema 4, validator enforcement, and regression coverage.

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
- [x] When a standard or full adopter is bootstrapped, it receives the Wave 2 runner, evaluation, and executor-review assets with explicit manifest contract sections.
- [x] When a maintainer runs the Developer Toolchain runner, the repository records a durable run receipt for the selected surface.
- [x] When a maintainer opens and records an independent evaluation, the repository receives bounded request and report artifacts with PASS / CONDITIONAL / FAIL.
- [x] When a maintainer probes and dispatches local executor review, the repository receives a durable packet that records availability and raw output paths honestly.
- [x] When validation runs against the template repo or a bootstrapped adopter, missing Wave 2 assets are detected mechanically.

End-to-end scenario: a maintainer bootstraps a standard adopter, runs the Developer Toolchain runner for one surface, opens an evaluation request and report, dispatches one local review loop through the executor registry, and then validates the target repo with all Wave 2 assets present.

Agent cannot verify: which executor commands a future adopter machine actually has installed, because Wave 2 can only ship the registry and honest probe or dispatch surfaces, not guarantee the host tooling itself.

---

## Phase Decisions
- Treat anti-drift as a mechanism stack, not a prose-only rule tightening exercise.
- Keep the first audit wave contradiction-focused and mechanical rather than trying to infer narrative intent automatically.
- Make execution-lifecycle rules depend on checkpoint contracts, progress receipts, sync audit, and drift reconciliation instead of trying to simulate those behaviors in prose.
- The next framework execution wave should prioritize downstream execution-proof surfaces over more design-only guidance: strict adoption attestation, toolchain probes and runners, independent evaluation, and auditable local multi-CLI review.
- Wave 2 will treat independent evaluation and local executor review as packetized execution surfaces, not as implicit trust in the implementing thread.

---

## Technical Insights
- Self-hosting drift in the root repository damages framework trust faster than missing optional capabilities.
- Checkpoint contracts only become trustworthy when the task packet, session state, receipts, hooks, and rule layer all consume the same fields.
- Drift repair should stay distinct from leftover recording: contradictions are reconciled first, then intentional partial work can be preserved honestly.
